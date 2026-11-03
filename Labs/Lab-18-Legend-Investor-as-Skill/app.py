"""Streamlit interface for the Lab 18 reproducible 10-K analysis."""
from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

import pandas as pd
import streamlit as st

ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / ".codex" / "skills" / "buffett-10k-analysis" / "scripts" / "edgar_10k_facts.py"
OUTPUTS = Path(__file__).parent / "outputs"


def run_analysis(ticker: str) -> dict:
    output = OUTPUTS / f"{ticker}_facts.json"
    result = subprocess.run([sys.executable, str(SCRIPT), ticker, "--json", str(output)], capture_output=True, text=True, check=False)
    if result.returncode:
        raise RuntimeError(result.stderr.strip() or result.stdout.strip())
    return json.loads(output.read_text(encoding="utf-8"))


def unprinted_numbers(memo: str, facts: dict) -> list[str]:
    """Flag numeric strings in the memo that do not occur in script output."""
    numeric = r"(?<![\w.])-?\d[\d,]*(?:\.\d+)?%?"
    normalize = lambda value: value.replace(",", "").removesuffix("%")
    allowed = {normalize(value) for value in re.findall(numeric, json.dumps(facts))}
    seen = re.findall(numeric, memo)
    return sorted({value for value in seen if normalize(value) not in allowed})


st.set_page_config(page_title="Buffett 10-K Skill", layout="wide")
st.title("Buffett 10-K Skill")
st.caption("Data from SEC EDGAR; built with AI help, a learning demonstration, not investment advice.")
ticker = st.text_input("Ticker", value="COST").strip().upper()

if st.button("Download 10-K facts and run checks", type="primary"):
    try:
        st.session_state["facts"] = run_analysis(ticker)
        st.success(f"Downloaded five annual 10-K rows for {ticker}.")
    except RuntimeError as error:
        st.error(error)

facts = st.session_state.get("facts")
if facts:
    table = pd.DataFrame(facts["rows"])
    chart = table.set_index("fiscal_year_end")[["owner_earnings_usd_millions", "net_income_usd_millions"]].apply(pd.to_numeric, errors="coerce")
    st.subheader("Owner earnings and net income (USD millions)")
    st.line_chart(chart, y_label="USD millions")
    st.subheader("Five annual 10-K rows and XBRL tags")
    st.dataframe(table, use_container_width=True, hide_index=True)
    st.subheader("Buffett checks computed by code")
    st.dataframe(pd.DataFrame(facts["checks"].items(), columns=["Check", "Result"]), use_container_width=True, hide_index=True)

    memo_path = OUTPUTS / f"{facts['ticker']}_memo.md"
    memo = memo_path.read_text(encoding="utf-8") if memo_path.exists() else "No memo file yet. Ask the skill to write one using only these printed facts."
    st.subheader("Buffett-style memo")
    st.markdown(memo)
    unverified = unprinted_numbers(memo, facts)
    if unverified:
        st.warning("Numbers in the memo not printed by the script: " + ", ".join(unverified))
    else:
        st.success("All numbers in the memo appear in the script output.")
