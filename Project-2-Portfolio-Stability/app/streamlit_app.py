"""Meridian Foundation Reserve educational Streamlit demonstration."""

from __future__ import annotations

import sys
from pathlib import Path

import altair as alt
import pandas as pd
import streamlit as st

APP_DIRECTORY = Path(__file__).resolve().parent
if str(APP_DIRECTORY) not in sys.path:
    sys.path.insert(0, str(APP_DIRECTORY))

from app_model import allocation_rows, build_dashboard_state, metric_rows, path_rows, turnover_rows, verdict_rows
from portfolio_engine import EngineInputError, InfeasiblePortfolioError
from stress_tests import APPROVED_NONLOCKED_CASES, run_project_stress_case, stress_summary


PROJECT_ROOT = APP_DIRECTORY.parents[0]
PROJECT_DOCUMENTS = (
    ("Data integrity and point-in-time", PROJECT_ROOT / "docs" / "data-integrity-and-point-in-time.md"),
    ("Portfolio-engine methodology", PROJECT_ROOT / "docs" / "portfolio-engine-methodology.md"),
    ("Phase 3B validation report", PROJECT_ROOT / "validation" / "phase-3b-validation-report.md"),
)


def _currency_percent(value: float) -> str:
    return f"{value:.2%}"


def read_project_document(path: Path) -> str:
    """Read only the three trusted, repository-owned documents shown in the app."""
    resolved = path.resolve()
    allowed = {document_path.resolve() for _, document_path in PROJECT_DOCUMENTS}
    if resolved not in allowed:
        raise ValueError("unapproved project documentation path")
    return resolved.read_text(encoding="utf-8")


def _documentation_viewer() -> None:
    """Render repository Markdown in-app; Streamlit does not serve local .md URLs."""
    with st.expander("Read project documentation", expanded=False):
        tabs = st.tabs([title for title, _ in PROJECT_DOCUMENTS])
        for tab, (title, path) in zip(tabs, PROJECT_DOCUMENTS):
            with tab:
                st.caption(f"Repository file: {path.relative_to(PROJECT_ROOT)}")
                try:
                    st.markdown(read_project_document(path))
                except (OSError, UnicodeError, ValueError) as error:
                    st.error(f"STOP — project documentation could not be displayed: {error}")


def _reset_to_base() -> None:
    """Widget callback runs before checkbox instantiation on the following rerun."""
    st.session_state["bil_scenario"] = False


def _display_mandate() -> None:
    st.subheader("Meridian Foundation Reserve mandate")
    st.markdown(
        "**Objective:** CPI + 4% annualized, net of costs, over rolling five-year periods.  "
        "**Horizon:** seven years. **Cadence:** annual rebalance.  "
        "**Benchmark:** 60% VT / 40% LQD. **Turnover cap:** 25% per modeled rebalance without committee approval."
    )
    st.markdown(
        "**Liquidity reserve:** four $0.75m quarterly payouts from a $100m reserve (3.0%), subject to unresolved "
        "vehicle-eligibility evidence. The 10% BIL control is a student-proposed scenario—not client policy."
    )
    with st.expander("Unresolved mandate definitions", expanded=False):
        st.markdown(
            "Reserve eligibility; 90% redemption within five business days; ETF issuer look-through; CPI vintage, lag, "
            "and net-cost methodology; calendar-year net-loss measurement; and ALFRED credit-spread timing/threshold."
        )
        st.caption("The mandate specification is available as `Project-2-Mandate.md` in this repository.")


def _portfolio_comparison(state) -> None:
    st.subheader("Portfolio comparison — gross historical analytics")
    st.caption(
        f"Approved source labels: {state.table.labels[0].isoformat()} through {state.table.labels[-1].isoformat()}; "
        f"{len(state.table.labels) - 1} monthly returns. All results are gross historical calculations."
    )
    metrics = pd.DataFrame(metric_rows(state))
    for column in (
        "Gross geometric annualized return",
        "Annualized sample volatility",
        "Zero-target downside deviation",
        "Maximum drawdown",
        "Highest modeled turnover",
    ):
        metrics[column] = metrics[column].map(_currency_percent)
    st.dataframe(metrics, hide_index=True, width="stretch")
    st.info(
        "Equal weight is a required baseline, but it fails the applicable initial turnover cap: moving from the hypothetical "
        "60% VT / 40% LQD start to 25% each requires 50% one-way turnover. It is therefore not feasible in the constrained search."
    )
    st.warning("CONSTRAINED PORTFOLIO: ANALYTICAL CANDIDATE, NOT RECOMMENDATION.")


def _charts(state) -> None:
    st.subheader("Historical comparisons")
    allocation = pd.DataFrame(allocation_rows(state))
    allocation_chart = (
        alt.Chart(allocation)
        .mark_bar()
        .encode(
            x=alt.X("Weight:Q", title="Target weight", axis=alt.Axis(format="%")),
            y=alt.Y("Portfolio:N", title=None),
            color=alt.Color("ETF:N", title="ETF"),
            tooltip=["Portfolio:N", "ETF:N", alt.Tooltip("Weight:Q", format=".1%")],
        )
        .properties(title="Target allocations", height=170)
    )
    st.altair_chart(allocation_chart, width="stretch")

    wealth = pd.DataFrame(path_rows(state, "Wealth index"))
    wealth_chart = (
        alt.Chart(wealth)
        .mark_line()
        .encode(
            x=alt.X("Date:T", title="Approved source-label date", axis=alt.Axis(format="%Y", tickCount="year", labelAngle=0)),
            y=alt.Y("Wealth index:Q", title="Gross wealth index (start = 1.00)", scale=alt.Scale(zero=False)),
            color=alt.Color("Portfolio:N", title="Portfolio"),
            tooltip=["Date:T", "Portfolio:N", alt.Tooltip("Wealth index:Q", format=".3f")],
        )
        .properties(title="Historical gross wealth growth", height=300)
    )
    st.altair_chart(wealth_chart, width="stretch")

    drawdown = pd.DataFrame(path_rows(state, "Drawdown"))
    drawdown_chart = (
        alt.Chart(drawdown)
        .mark_line()
        .encode(
            x=alt.X("Date:T", title="Approved source-label date", axis=alt.Axis(format="%Y", tickCount="year", labelAngle=0)),
            y=alt.Y("Drawdown:Q", title="Drawdown from prior peak", axis=alt.Axis(format="%")),
            color=alt.Color("Portfolio:N", title="Portfolio"),
            tooltip=["Date:T", "Portfolio:N", alt.Tooltip("Drawdown:Q", format=".2%")],
        )
        .properties(title="Historical gross drawdown", height=300)
    )
    st.altair_chart(drawdown_chart, width="stretch")


def _mandate_compliance(state) -> None:
    st.subheader("Mandate compliance status")
    st.error("NOT DECISION-READY — UNVERIFIED evidence-dependent gates prevent full mandate compliance.")
    for result, assessment in zip(state.results, state.assessments):
        with st.expander(result.name, expanded=result.name == "Constrained minimum-volatility"):
            st.markdown(f"**{assessment.summary}**")
            verdicts = pd.DataFrame(verdict_rows(assessment))
            st.dataframe(verdicts, hide_index=True, width="stretch")
            turnover = pd.DataFrame(turnover_rows(result.analytics))
            if not turnover.empty:
                turnover["Turnover"] = turnover["Turnover"].map(_currency_percent)
            st.caption("Modeled initial and annual drift-rebalance turnover")
            st.dataframe(turnover, hide_index=True, width="stretch")


def _provenance_and_evidence(state) -> None:
    st.subheader("Data provenance, validation, and limitations")
    st.markdown(
        f"The engine accepts only the approved dataset, containing **{len(state.table.labels)} completed monthly source labels** and "
        f"**{len(state.table.labels) - 1} returns**. The preserved earlier `prices.csv` contained an incomplete retrieval-month "
        "observation under a monthly label; it is retained as evidence and is not used by this app."
    )
    st.warning(
        "Adjusted-close source labels are not guaranteed point-in-time tradable prices. Results are historical gross analytics, "
        "not net or fully point-in-time-verified results."
    )
    _documentation_viewer()
    st.markdown(
        "**Unresolved blockers:** official CPI availability and net-hurdle evaluation; dated transaction-cost evidence; reserve and liquidity "
        "eligibility; redemption definition; issuer look-through; and ALFRED vintage/credit-spread rule. The credit-spread signal remains monitor-only."
    )
    with st.expander("Reproducibility", expanded=False):
        st.code(
            "python -m pip install -r requirements.txt\n"
            "python src/data_pipeline.py\n"
            "python -m unittest discover -s tests -v\n"
            "streamlit run app/streamlit_app.py",
            language="powershell",
        )


def _stress_test_section() -> None:
    st.subheader("Non-locked stress tests")
    st.caption(
        "These are student-proposed analytical sensitivities using approved data. They are not forecasts, sourced trading costs, "
        "client-approved mandate rules, or the locked changed-input experiment."
    )
    if st.button("Run approved non-locked stress tests", key="run_nonlocked_stresses"):
        summaries = [stress_summary(run_project_stress_case(case)) for case in APPROVED_NONLOCKED_CASES]
        rows = []
        for summary in summaries:
            constrained = next((item for item in summary["portfolios"] if item["name"] == "Constrained minimum-volatility"), None)
            row = {
                "Case": summary["case"],
                "Status": summary["status"],
                "Coverage": f"{summary['source_start']} to {summary['source_end']} ({summary['return_count']} returns)",
            }
            if constrained is not None:
                row.update(
                    {
                        "Constrained weights": ", ".join(f"{ticker} {weight:.0%}" for ticker, weight in constrained["weights"].items()),
                        "Volatility": _currency_percent(constrained["annualized_sample_volatility"]),
                        "Gross annualized return": _currency_percent(constrained["gross_geometric_annualized_return"]),
                        "Maximum drawdown": _currency_percent(constrained["maximum_drawdown"]),
                        "Highest turnover": _currency_percent(constrained["highest_modeled_turnover"]),
                    }
                )
            rows.append(row)
        st.error("All displayed stress cases remain NOT DECISION-READY while evidence-dependent mandate gates are unresolved.")
        st.dataframe(pd.DataFrame(rows), hide_index=True, width="stretch")


def main() -> None:
    st.set_page_config(page_title="Meridian Reserve | FIN 439", page_icon="📊", layout="wide")
    st.title("Meridian Foundation Reserve")
    st.caption("FIN 439 Project 2 — investment-management process demonstration")
    st.info(
        "AI use: OpenAI Codex assisted with project planning, documentation structure, and technical development. "
        "The student documents material AI use and independent checks."
    )
    st.info(
        "Student ownership and educational purpose: the analysis and decision are the student's own. This is educational coursework only, "
        "not personalized investment advice or a recommendation to buy or sell any security."
    )

    with st.sidebar:
        st.header("Scenario controls")
        st.button("Reset to base", on_click=_reset_to_base)
        bil_scenario = st.checkbox("Apply 10% BIL minimum scenario", value=False, key="bil_scenario")
        st.caption("Student-proposed stress scenario only; not a client-approved mandate rule.")
        st.caption("Credit spread is monitor-only. No threshold or trading action is applied.")

    try:
        state = build_dashboard_state(bil_scenario)
    except (EngineInputError, InfeasiblePortfolioError, FileNotFoundError, ValueError) as error:
        st.error(f"STOP — the approved-data or constraint gate prevented analysis: {error}")
        st.stop()

    if state.bil_scenario_enabled:
        st.warning("Scenario active: constrained search requires at least 10% BIL. This is not a client mandate.")

    _display_mandate()
    _portfolio_comparison(state)
    _charts(state)
    _mandate_compliance(state)
    _provenance_and_evidence(state)
    _stress_test_section()


if __name__ == "__main__":
    main()
