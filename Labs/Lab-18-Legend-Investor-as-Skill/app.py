"""Lab 19 Legend Panel: three code-based checks, one shared 10-K fact set."""
from __future__ import annotations

import json
import os
import re
import subprocess
import sys
from pathlib import Path

import pandas as pd
import streamlit as st

ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / ".codex" / "skills" / "buffett-10k-analysis" / "scripts" / "edgar_10k_facts.py"
OUTPUTS = Path(__file__).parent / "outputs"
GRAHAM_THRESHOLD_KEPT = 2.0


def run_analysis(ticker: str, user_agent: str) -> dict:
    if "@" not in user_agent or len(user_agent.split()) < 2:
        raise RuntimeError("Enter an SEC User-Agent containing your name and email before downloading.")
    output = OUTPUTS / f"{ticker}_facts.json"
    environment = {**os.environ, "SEC_USER_AGENT": user_agent}
    result = subprocess.run([sys.executable, str(SCRIPT), ticker, "--json", str(output)], capture_output=True, text=True, check=False, env=environment)
    if result.returncode:
        raise RuntimeError(result.stderr.strip() or result.stdout.strip())
    return json.loads(output.read_text(encoding="utf-8"))


def saved_analysis(ticker: str) -> dict | None:
    path = OUTPUTS / f"{ticker}_facts.json"
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else None


def is_number(value: object) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool)


def graham_checks(facts: dict, threshold: float) -> dict[str, str]:
    """Turn Graham's checks into pass/fail/not known without filling missing facts."""
    rows = facts["rows"]
    latest_ratio = rows[-1].get("current_ratio", "not known")
    income = [row.get("net_income_usd_millions", "not found") for row in rows]
    return {
        f"Current ratio of {threshold:.1f} or more, latest year": "not known" if not is_number(latest_ratio) else "pass" if latest_ratio >= threshold else "fail",
        "Net income positive every year": "not known" if not all(is_number(value) for value in income) else "pass" if all(value > 0 for value in income) else "fail",
        "Net income grew, first year to last": "not known" if not all(is_number(value) for value in income) else "pass" if income[-1] > income[0] else "fail",
    }


def burry_checks(facts: dict) -> dict[str, str]:
    rows = facts["rows"]
    cash = [row.get("operating_cash_flow_usd_millions", "not found") for row in rows]
    income = [row.get("net_income_usd_millions", "not found") for row in rows]
    latest_ratio = rows[-1].get("liabilities_to_equity", "not known")
    return {
        "Operating cash flow at least net income every year": "not known" if not all(is_number(value) for value in cash + income) else "pass" if all(flow >= profit for flow, profit in zip(cash, income)) else "fail",
        "Liabilities no more than twice equity, latest year": "not known" if not is_number(latest_ratio) else "pass" if latest_ratio <= 2 else "fail",
    }


def buffett_checks(facts: dict) -> dict[str, str]:
    checks = facts["checks"]
    return {
        "ROE of 15% or more every year": checks["roe_15_percent_every_year"],
        "Owner earnings positive every year": checks["owner_earnings_positive_every_year"],
        "Owner earnings grew, first year to last": checks["owner_earnings_grew_first_to_last"],
    }


def verdict(checks: dict[str, str], favorable: str) -> str:
    if all(result == "pass" for result in checks.values()):
        return favorable
    if any(result == "not known" for result in checks.values()):
        return "watch - evidence gap"
    return "fail - screen only"


def printed_memos(facts: dict, threshold: float) -> dict[str, str]:
    """Build prose only from values that are already in the printed JSON/table."""
    first, latest = facts["rows"][0], facts["rows"][-1]
    w_checks, g_checks, b_checks = buffett_checks(facts), graham_checks(facts, threshold), burry_checks(facts)
    return {
        "Buffett": f"**Verdict: {verdict(w_checks, 'own the business')}.** Net income moved from {first['net_income_usd_millions']} to {latest['net_income_usd_millions']} USD millions, and owner earnings moved from {first['owner_earnings_usd_millions']} to {latest['owner_earnings_usd_millions']} USD millions. The printed Buffett checks are {', '.join(w_checks.values())}. This is a business-quality screen, not a price judgment.",
        "Graham": f"**Verdict: {verdict(g_checks, 'screen passes')}.** Latest current ratio is {latest.get('current_ratio', 'not known')} against the {threshold:.1f} threshold. Net income moved from {first['net_income_usd_millions']} to {latest['net_income_usd_millions']} USD millions. The printed Graham checks are {', '.join(g_checks.values())}.\n\n*Threshold kept: {GRAHAM_THRESHOLD_KEPT:.1f}; it preserves Graham's requested liquidity rule. The slider above records the threshold probe.*",
        "Burry": f"**Verdict: {verdict(b_checks, 'screen passes')}.** Latest liabilities-to-equity is {latest.get('liabilities_to_equity', 'not known')}. Latest operating cash flow is {latest['operating_cash_flow_usd_millions']} USD millions and latest net income is {latest['net_income_usd_millions']} USD millions. The printed Burry checks are {', '.join(b_checks.values())}. This does not replace filing-footnote review.",
    }


def panel_table(facts: dict, threshold: float) -> pd.DataFrame:
    panel = {"Buffett": buffett_checks(facts), "Graham": graham_checks(facts, threshold), "Burry": burry_checks(facts)}
    return pd.DataFrame({"Investor": investor, "Check": check, "Result": result} for investor, checks in panel.items() for check, result in checks.items())


def unprinted_numbers(memo: str, facts: dict) -> list[str]:
    numeric = r"(?<![\w.])-?\d[\d,]*(?:\.\d+)?%?"
    def normalize(value: str) -> str:
        raw = value.replace(",", "").removesuffix("%")
        try:
            return str(float(raw))
        except ValueError:
            return raw
    allowed = {normalize(value) for value in re.findall(numeric, json.dumps(facts))}
    return sorted({value for value in re.findall(numeric, memo) if normalize(value) not in allowed})


st.set_page_config(page_title="Lab 19 Legend Panel", layout="wide")
st.title("Lab 19 - Legend Panel")
st.caption("Shared SEC EDGAR facts; educational demonstration, not investment advice.")
ticker = st.text_input("Ticker", value="COST").strip().upper()
user_agent = st.text_input("SEC User-Agent (needed only for a fresh download)", value=os.getenv("SEC_USER_AGENT", ""), placeholder="Your Name your.email@purdue.edu")

loaded = st.session_state.get("facts")
if not loaded or loaded.get("ticker") != ticker:
    st.session_state["facts"] = saved_analysis(ticker)
if st.button("Download five annual 10-K facts and run panel", type="primary"):
    try:
        st.session_state["facts"] = run_analysis(ticker, user_agent)
        st.success(f"Downloaded five annual 10-K rows for {ticker}.")
    except RuntimeError as error:
        st.error(error)

facts = st.session_state.get("facts")
if not facts:
    st.info("Enter a ticker and download its annual 10-K facts.")
    st.stop()

threshold = st.slider("Graham current-ratio probe", min_value=1.0, max_value=2.0, value=GRAHAM_THRESHOLD_KEPT, step=0.1)
st.subheader("Printed five-year 10-K facts (USD millions unless noted)")
st.dataframe(pd.DataFrame(facts["rows"]), use_container_width=True, hide_index=True)
st.subheader("Panel table")
st.dataframe(panel_table(facts, threshold), use_container_width=True, hide_index=True)

memos = printed_memos(facts, threshold)
st.subheader("Three investor memos")
for column, (investor, memo) in zip(st.columns(3), memos.items()):
    with column:
        st.markdown(f"### {investor}")
        st.markdown(memo)
        unknown = unprinted_numbers(memo, facts)
        st.warning("Unprinted-number flag: " + ", ".join(unknown)) if unknown else st.success("Unprinted-number flag: clear")

all_unprinted = {investor: unprinted_numbers(memo, facts) for investor, memo in memos.items()}
st.subheader("Shared number audit")
st.warning("Numbers not printed in facts: " + json.dumps(all_unprinted)) if any(all_unprinted.values()) else st.success("All memo numbers occur in the printed script output.")
st.caption("Sources: SEC EDGAR companyfacts; Graham and Burry FAskills pages; Streamlit documentation.")
