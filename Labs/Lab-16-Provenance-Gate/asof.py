"""Lab 16 — Provenance Gate.

Run from this folder with: python asof.py

The data below are the fictional training-table inputs supplied in the lab.
"""

from collections import defaultdict
from datetime import date


# Editable inputs -----------------------------------------------------------
DECISION_DATE = date.fromisoformat("2026-03-31")

# row, ticker, month measured, published on, index
TABLE = [
    (1, "AAA", "2026-01", "2026-02-10", 101.0),
    (2, "AAA", "2026-02", "2026-03-10", 104.0),
    (3, "AAA", "2026-03", "2026-04-10", 109.0),
    (4, "AAA", "2026-02", "2026-03-25", 103.0),
    (5, "BBB", "2026-01", "2026-02-10", 98.0),
    (6, "BBB", "2026-02", "2026-03-10", 97.0),
    (7, "BBB", "2026-02", "2026-03-10", 97.0),
    (8, "BBB", "2026-03", "2026-04-10", 92.0),
    (9, "CCC", "2026-01", "2026-02-10", 110.0),
    (10, "CCC", "2026-02", "2026-04-05", 112.0),
    (11, "", "2026-02", "2026-03-10", 99.0),
    (12, "CCC", "2026-02", "2026-03-10", 111.0),
]


def make_rows(table):
    """Convert editable table tuples to rows with comparable publication dates."""
    return [
        {
            "row": row_number,
            "ticker": ticker,
            "month": month,
            "published": date.fromisoformat(published),
            "index": index_value,
        }
        for row_number, ticker, month, published, index_value in table
    ]


def row_numbers(rows):
    """Return a readable, stable list of source-row numbers."""
    return ", ".join(str(row["row"]) for row in sorted(rows, key=lambda item: item["row"])) or "none"


def quarantine_missing_tickers(rows):
    removed = [row for row in rows if not row["ticker"].strip()]
    kept = [row for row in rows if row["ticker"].strip()]
    return kept, removed


def remove_exact_duplicates(rows):
    """Keep the first copy; a row number is metadata, not part of its contents."""
    seen = set()
    kept, removed = [], []
    for row in rows:
        contents = (row["ticker"], row["month"], row["published"], row["index"])
        if contents in seen:
            removed.append(row)
        else:
            seen.add(contents)
            kept.append(row)
    return kept, removed


def remove_late_publications(rows, decision_date):
    removed = [row for row in rows if row["published"] > decision_date]
    kept = [row for row in rows if row["published"] <= decision_date]
    return kept, removed


def keep_latest_vintage(rows):
    """For each ticker/month, retain the latest publication available in this input."""
    groups = defaultdict(list)
    for row in rows:
        groups[(row["ticker"], row["month"])].append(row)

    kept, removed = [], []
    for group in groups.values():
        # A row-number tie-breaker makes the result reproducible if dates tie.
        latest = max(group, key=lambda item: (item["published"], -item["row"]))
        kept.append(latest)
        removed.extend(row for row in group if row is not latest)
    return sorted(kept, key=lambda item: item["row"]), removed


def as_of_filter(rows, decision_date):
    """Apply the four lab rules in their required order and return a funnel."""
    current, no_ticker = quarantine_missing_tickers(rows)
    current, duplicates = remove_exact_duplicates(current)
    current, late = remove_late_publications(current, decision_date)
    current, older_vintages = keep_latest_vintage(current)
    funnel = [
        ("Quarantined: no ticker", no_ticker),
        ("Exact duplicate", duplicates),
        (f"Published after {decision_date:%d %B}", late),
        ("Older vintage replaced by a revision", older_vintages),
    ]
    return current, funnel


def naive_filter(rows):
    """Use the same hygiene rules but deliberately ignore publication timing."""
    current, _ = quarantine_missing_tickers(rows)
    current, _ = remove_exact_duplicates(current)
    current, _ = keep_latest_vintage(current)
    return current


def signals(panel):
    """Return latest-month percent changes, using the prior measured month as base."""
    by_ticker = defaultdict(list)
    for row in panel:
        by_ticker[row["ticker"]].append(row)

    results = []
    for ticker in sorted(by_ticker):
        history = sorted(by_ticker[ticker], key=lambda item: item["month"])
        if len(history) < 2:
            continue
        previous, latest = history[-2], history[-1]
        percent_change = (latest["index"] / previous["index"] - 1) * 100
        results.append((ticker, latest["month"], percent_change, previous["index"], latest["index"]))
    return results


def print_funnel(funnel):
    print("ROW FUNNEL")
    for label, removed in funnel:
        print(f"- {label}: {len(removed)} removed (row(s): {row_numbers(removed)})")


def print_panel(panel, title):
    print(f"\n{title}")
    print("row  ticker  month measured  published on  index")
    for row in sorted(panel, key=lambda item: item["row"]):
        print(
            f"{row['row']:>3}  {row['ticker']:<6}  {row['month']:<14}  "
            f"{row['published'].isoformat()}    {row['index']:.1f}"
        )


def print_signals(title, panel):
    print(f"\n{title}")
    for ticker, month, change, previous_index, latest_index in signals(panel):
        print(
            f"- {ticker}: {change:+.2f}% to {month} "
            f"({previous_index:.1f} -> {latest_index:.1f})"
        )


def main():
    rows = make_rows(TABLE)
    as_of_panel, funnel = as_of_filter(rows, DECISION_DATE)

    print(f"Decision date: {DECISION_DATE.isoformat()}")
    print_funnel(funnel)
    print_panel(as_of_panel, "AS-OF PANEL")
    print_signals("AS-OF SIGNALS (only information published by the decision date)", as_of_panel)
    print_signals("NAIVE SIGNALS (publication date ignored)", naive_filter(rows))


if __name__ == "__main__":
    main()
