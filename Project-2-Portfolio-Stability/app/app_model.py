"""Presentation data for the Streamlit app; portfolio arithmetic stays in src/."""

from __future__ import annotations

import sys
from dataclasses import dataclass
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_DIRECTORY = PROJECT_ROOT / "src"
if str(SRC_DIRECTORY) not in sys.path:
    sys.path.insert(0, str(SRC_DIRECTORY))

from mandate_verdicts import MandateAssessment, assess
from portfolio_engine import Analytics, PortfolioResult, PriceTable, baseline_results, constrained_minimum_volatility, load_approved_prices

CHART_LABELS = {
    "Equal weight": "Equal Weight",
    "Policy benchmark": "60/40 Benchmark",
    "Constrained minimum-volatility": "Constrained",
}


@dataclass(frozen=True)
class DashboardState:
    table: PriceTable
    results: tuple[PortfolioResult, ...]
    assessments: tuple[MandateAssessment, ...]
    bil_scenario_enabled: bool


def build_dashboard_state(bil_scenario_enabled: bool = False) -> DashboardState:
    """Load all displayed analytics through the validated project engine."""
    table = load_approved_prices()
    equal_weight, policy_benchmark = baseline_results(table)
    constrained = constrained_minimum_volatility(table, bil_scenario_floor=0.10 if bil_scenario_enabled else None)
    results = (equal_weight, policy_benchmark, constrained)
    return DashboardState(
        table=table,
        results=results,
        assessments=tuple(assess(result.weights, result.analytics.turnover_events) for result in results),
        bil_scenario_enabled=bil_scenario_enabled,
    )


def metric_rows(state: DashboardState) -> list[dict[str, object]]:
    """Return presentation values only; calculations originate in portfolio_engine."""
    rows: list[dict[str, object]] = []
    for result, assessment in zip(state.results, state.assessments):
        analytics = result.analytics
        rows.append(
            {
                "Portfolio": result.name,
                "Gross geometric annualized return": analytics.gross_geometric_annualized_return,
                "Annualized sample volatility": analytics.annualized_sample_volatility,
                "Zero-target downside deviation": analytics.annualized_zero_target_downside_deviation,
                "Maximum drawdown": analytics.maximum_drawdown,
                "Highest modeled turnover": max(event.turnover for event in analytics.turnover_events),
                "Decision status": assessment.summary,
            }
        )
    return rows


def allocation_rows(state: DashboardState) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for result in state.results:
        for ticker, weight in result.weights.items():
            rows.append({"Portfolio": CHART_LABELS[result.name], "ETF": ticker, "Weight": weight})
    return rows


def path_rows(state: DashboardState, metric: str) -> list[dict[str, object]]:
    if metric not in {"Wealth index", "Drawdown"}:
        raise ValueError("metric must be Wealth index or Drawdown")
    rows: list[dict[str, object]] = []
    for result in state.results:
        values = result.analytics.wealth_index if metric == "Wealth index" else result.analytics.drawdown_series
        if len(values) != len(state.table.labels):
            raise ValueError("engine path and approved labels are misaligned")
        for label, value in zip(state.table.labels, values):
            rows.append({"Date": label, "Portfolio": CHART_LABELS[result.name], metric: value})
    return rows


def verdict_rows(assessment: MandateAssessment) -> list[dict[str, str]]:
    return [
        {"Rule": rule.rule, "Status": rule.status, "Measurement": rule.measurement, "Reason": rule.reason}
        for rule in assessment.rules
    ]


def turnover_rows(analytics: Analytics) -> list[dict[str, object]]:
    return [
        {"Date": event.label, "Type": event.kind.replace("_", " "), "Turnover": event.turnover}
        for event in analytics.turnover_events
    ]
