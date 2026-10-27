"""Reproducible checks for the Lab 16 known answer.

Run with: python verify_known_answer.py
"""

from datetime import date
from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path


# Load the adjacent script by path so this check also works with the local
# embedded Python runtime, whose isolated configuration omits the script folder
# from the normal import search path.
source_path = Path(__file__).with_name("asof.py")
source_spec = spec_from_file_location("asof", source_path)
asof = module_from_spec(source_spec)
source_spec.loader.exec_module(asof)

DECISION_DATE = asof.DECISION_DATE
TABLE = asof.TABLE
as_of_filter = asof.as_of_filter
make_rows = asof.make_rows
naive_filter = asof.naive_filter
signals = asof.signals


def signal_map(panel):
    """Keep just the values used in the instructor's signal table."""
    return {ticker: (month, round(change, 2)) for ticker, month, change, _, _ in signals(panel)}


def main():
    rows = make_rows(TABLE)
    as_of_panel, funnel = as_of_filter(rows, DECISION_DATE)

    assert [row["row"] for row in as_of_panel] == [1, 4, 5, 6, 9, 12]
    assert [row_numbers for _, removed in funnel for row_numbers in [
        [row["row"] for row in sorted(removed, key=lambda item: item["row"])]
    ]] == [[11], [7], [3, 8, 10], [2]]
    assert signal_map(as_of_panel) == {
        "AAA": ("2026-02", 1.98),
        "BBB": ("2026-02", -1.02),
        "CCC": ("2026-02", 0.91),
    }

    naive_panel = naive_filter(rows)
    assert signal_map(naive_panel) == {
        "AAA": ("2026-03", 5.83),
        "BBB": ("2026-03", -5.15),
        "CCC": ("2026-02", 1.82),
    }

    later_panel, _ = as_of_filter(rows, date.fromisoformat("2026-04-15"))
    assert signal_map(later_panel) == signal_map(naive_panel)

    print("Known-answer check passed.")
    print("Later-date check passed: 2026-04-15 as-of signals equal naive signals.")


if __name__ == "__main__":
    main()
