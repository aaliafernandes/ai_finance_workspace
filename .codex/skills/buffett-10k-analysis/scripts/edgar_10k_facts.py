"""Download five annual 10-K financial rows from SEC EDGAR company facts.

Usage: python edgar_10k_facts.py COST --json outputs/COST.json
All dollars are printed in USD millions. This educational script deliberately
prints missing XBRL concepts as "not found" rather than estimating them.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.request
from datetime import date
from pathlib import Path

TICKERS_URL = "https://www.sec.gov/files/company_tickers.json"
FACTS_URL = "https://data.sec.gov/api/xbrl/companyfacts/CIK{cik:010d}.json"
# The SEC requests an identifying User-Agent for automated access. The caller
# must set this to their own name and email; a placeholder is never sent.
USER_AGENT = os.getenv("SEC_USER_AGENT", "").strip()

METRICS = {
    "revenue": ["RevenueFromContractWithCustomerExcludingAssessedTax", "Revenues"],
    "net_income": ["NetIncomeLoss"],
    "operating_cash_flow": ["NetCashProvidedByUsedInOperatingActivities"],
    "capital_spending": ["PaymentsToAcquirePropertyPlantAndEquipment", "PaymentsToAcquireProductiveAssets"],
    "equity": ["StockholdersEquity"],
}


def fetch_json(url: str) -> dict:
    if not USER_AGENT:
        raise ValueError("Set SEC_USER_AGENT to your name and email before downloading EDGAR data.")
    # Do not request compressed content: urllib's JSON loader expects decoded text.
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(request, timeout=30) as response:
        return json.load(response)


def cik_for_ticker(ticker: str) -> int:
    for item in fetch_json(TICKERS_URL).values():
        if item["ticker"].upper() == ticker.upper():
            return int(item["cik_str"])
    raise ValueError(f"Ticker {ticker.upper()} was not found in SEC company_tickers.json")


def facts_for_tag(facts: dict, tag: str) -> list[dict]:
    concept = facts.get("facts", {}).get("us-gaap", {}).get(tag, {})
    return concept.get("units", {}).get("USD", [])


def annual_candidates(facts: dict, tag: str, instant: bool = False) -> list[dict]:
    """Keep only annual 10-K values, excluding quarters and prior-year comparisons."""
    selected = []
    for fact in facts_for_tag(facts, tag):
        if fact.get("form") != "10-K" or fact.get("fp") != "FY" or not fact.get("end"):
            continue
        if not instant:
            start = fact.get("start")
            if not start:
                continue
            days = (date.fromisoformat(fact["end"]) - date.fromisoformat(start)).days
            if not 300 <= days <= 380:
                continue
        selected.append(fact)
    return selected


def latest_for_end(facts: dict, tags: list[str], end: str, instant: bool = False) -> tuple[dict | None, str | None]:
    """For one fiscal-year end choose the preferred tag and newest filing."""
    for tag in tags:
        matches = [fact for fact in annual_candidates(facts, tag, instant) if fact["end"] == end]
        if matches:
            return max(matches, key=lambda fact: fact.get("filed", "")), tag
    return None, None


def display(value: float | None) -> float | str:
    return "not found" if value is None else round(value / 1_000_000, 1)


def calc_roe(net_income: float | None, equity: float | None) -> float | str:
    if net_income is None or equity is None or equity <= 0:
        return "not known"
    return round(net_income / equity * 100, 1)


def calc_owner_earnings(ocf: float | None, capex: float | None) -> float | str:
    if ocf is None or capex is None:
        return "not found"
    return round((ocf - capex) / 1_000_000, 1)


def evaluate(rows: list[dict]) -> dict[str, str]:
    roe = [row["roe_percent"] for row in rows]
    owner = [row["owner_earnings_usd_millions"] for row in rows]
    return {
        "roe_15_percent_every_year": "not known" if any(value == "not known" for value in roe) else ("pass" if all(value >= 15 for value in roe) else "fail"),
        "owner_earnings_positive_every_year": "not known" if any(value == "not found" for value in owner) else ("pass" if all(value > 0 for value in owner) else "fail"),
        "owner_earnings_grew_first_to_last": "not known" if any(value == "not found" for value in owner) else ("pass" if owner[-1] > owner[0] else "fail"),
    }


def build_rows(ticker: str, facts: dict) -> list[dict]:
    # Revenue establishes the five fiscal-year-end dates, with the latest 10-K winning.
    # The allowed revenue tags establish fiscal-year dates.  The preferred tag
    # always wins; filing date resolves duplicates within that same tag.
    candidate_ends = set()
    for tag in METRICS["revenue"]:
        candidate_ends.update(fact["end"] for fact in annual_candidates(facts, tag))
    fiscal_ends = sorted(candidate_ends)[-5:]
    if len(fiscal_ends) < 5:
        raise ValueError("Fewer than five annual 10-K revenue facts were available.")

    rows = []
    for end in fiscal_ends:
        raw, tags = {}, {}
        for name, candidates in METRICS.items():
            fact, tag = latest_for_end(facts, candidates, end, instant=(name == "equity"))
            raw[name] = fact.get("val") if fact else None
            tags[name] = tag or "not found"
        rows.append({
            "fiscal_year_end": end,
            "revenue_usd_millions": display(raw["revenue"]),
            "revenue_tag": tags["revenue"],
            "net_income_usd_millions": display(raw["net_income"]),
            "net_income_tag": tags["net_income"],
            "operating_cash_flow_usd_millions": display(raw["operating_cash_flow"]),
            "operating_cash_flow_tag": tags["operating_cash_flow"],
            "capital_spending_usd_millions": display(raw["capital_spending"]),
            "capital_spending_tag": tags["capital_spending"],
            "equity_usd_millions": display(raw["equity"]),
            "equity_tag": tags["equity"],
            "roe_percent": calc_roe(raw["net_income"], raw["equity"]),
            "owner_earnings_usd_millions": calc_owner_earnings(raw["operating_cash_flow"], raw["capital_spending"]),
        })
    return rows


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("ticker")
    parser.add_argument("--json", dest="json_path")
    args = parser.parse_args()
    ticker = args.ticker.upper()
    cik = cik_for_ticker(ticker)
    facts = fetch_json(FACTS_URL.format(cik=cik))
    rows = build_rows(ticker, facts)
    result = {
        "ticker": ticker,
        "cik": f"{cik:010d}",
        "source": "SEC EDGAR companyfacts; 10-K annual facts only",
        "retrieved": date.today().isoformat(),
        "check_rules": {"roe_minimum_percent": 15, "owner_earnings_must_be_positive": True, "owner_earnings_must_grow_first_to_last": True},
        "rows": rows,
        "checks": evaluate(rows),
    }
    print(json.dumps(result, indent=2))
    if args.json_path:
        path = Path(args.json_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(result, indent=2), encoding="utf-8")


if __name__ == "__main__":
    try:
        main()
    except (ValueError, OSError, urllib.error.URLError) as error:
        print(f"EDGAR download failed: {error}", file=sys.stderr)
        raise SystemExit(1)
