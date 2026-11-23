"""Phase 2B validation tests. Fixtures are synthetic unless a test names archived raw data."""

from __future__ import annotations

import csv
import hashlib
import json
import sys
import tempfile
import unittest
from datetime import UTC, date, datetime
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from costs import CostEvidenceError, CostLedgerEntry, trade_cost, turnover
from cpi import CpiAvailabilityError, CpiObservation, compounded_five_year_hurdle
from data_pipeline import DataGateError, TICKERS, build, validate_and_align
from credit_signal import SignalAvailabilityError, SignalObservation, latest_available_signal


class PricePipelineTests(unittest.TestCase):
    def test_archived_data_excludes_retrieval_month_and_writes_lineage(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            prices, lineage, count, first, last = build(
                PROJECT_ROOT / "data" / "raw",
                PROJECT_ROOT / "data" / "raw" / "retrieval_metadata.json",
                Path(directory),
            )
            self.assertEqual((count, first, last), (60, date(2021, 10, 1), date(2026, 9, 1)))
            with prices.open(newline="", encoding="utf-8") as handle:
                rows = list(csv.DictReader(handle))
            self.assertEqual(len(rows), 60)
            self.assertEqual(rows[-1]["PeriodLabel"], "2026-09-01")
            with lineage.open(newline="", encoding="utf-8") as handle:
                lineage_rows = list(csv.DictReader(handle))
            self.assertEqual(len(lineage_rows), 240)
            self.assertTrue(all(row["RawSha256"] for row in lineage_rows))

    def test_archived_output_is_deterministic(self) -> None:
        with tempfile.TemporaryDirectory() as first, tempfile.TemporaryDirectory() as second:
            first_paths = build(PROJECT_ROOT / "data" / "raw", PROJECT_ROOT / "data" / "raw" / "retrieval_metadata.json", Path(first))
            second_paths = build(PROJECT_ROOT / "data" / "raw", PROJECT_ROOT / "data" / "raw" / "retrieval_metadata.json", Path(second))
            self.assertEqual(first_paths[0].read_bytes(), second_paths[0].read_bytes())
            self.assertEqual(first_paths[1].read_bytes(), second_paths[1].read_bytes())

    def test_duplicate_completed_period_stops_pipeline(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            raw = root / "raw"
            raw.mkdir()
            timestamps = [1754006400, 1755216000, 1756684800]  # Aug 1, Aug 15, Sep 1 2025 UTC
            for ticker in TICKERS:
                payload = {"chart": {"result": [{"timestamp": timestamps, "indicators": {"adjclose": [{"adjclose": [100, 101, 102]}]}}]}}
                (raw / f"{ticker}_yahoo_monthly.json").write_text(json.dumps(payload), encoding="utf-8")
            (raw / "retrieval_metadata.json").write_text('{"retrieved_utc":"2025-10-22T00:00:00+00:00"}', encoding="utf-8")
            with self.assertRaisesRegex(DataGateError, "duplicate completed-period"):
                validate_and_align(raw, raw / "retrieval_metadata.json")


class CpiTests(unittest.TestCase):
    def test_compounded_hurdle_from_labeled_synthetic_fixture(self) -> None:
        fixture = PROJECT_ROOT / "tests" / "fixtures" / "cpi_synthetic.csv"
        with fixture.open(encoding="utf-8", newline="") as handle:
            rows = list(csv.DictReader(handle))
        start, end = [
            CpiObservation(
                date.fromisoformat(row["measured_month"]),
                float(row["index_value"]),
                datetime.fromisoformat(row["published_at"]),
                row["source_label"],
            )
            for row in rows
        ]
        result = compounded_five_year_hurdle(start, end, datetime(2026, 2, 15, tzinfo=UTC))
        self.assertAlmostEqual(result, (110 / 100) * 1.04**5 - 1)

    def test_unpublished_cpi_stops_evaluation(self) -> None:
        start = CpiObservation(date(2020, 1, 1), 100, datetime(2020, 2, 10, tzinfo=UTC), "SYNTHETIC")
        end = CpiObservation(date(2025, 1, 1), 110, datetime(2025, 2, 12, tzinfo=UTC), "SYNTHETIC")
        with self.assertRaises(CpiAvailabilityError):
            compounded_five_year_hurdle(start, end, datetime(2025, 2, 11, tzinfo=UTC))


class SignalTests(unittest.TestCase):
    def test_signal_selects_only_available_vintage(self) -> None:
        values = [
            SignalObservation(date(2026, 9, 30), 0.84, date(2026, 10, 1), "SYNTHETIC"),
            SignalObservation(date(2026, 10, 2), 0.90, date(2026, 10, 6), "SYNTHETIC"),
        ]
        selected = latest_available_signal(values, date(2026, 10, 3))
        self.assertEqual(selected.measured_date, date(2026, 9, 30))

    def test_unavailable_signal_stops(self) -> None:
        future = [SignalObservation(date(2026, 10, 1), 0.9, date(2026, 10, 6), "SYNTHETIC")]
        with self.assertRaises(SignalAvailabilityError):
            latest_available_signal(future, date(2026, 10, 3))


class CostTests(unittest.TestCase):
    def test_turnover_and_evidence_backed_cost(self) -> None:
        old = {"VT": 0.6, "LQD": 0.4}
        new = {"VT": 0.5, "LQD": 0.5}
        self.assertAlmostEqual(turnover(old, new), 0.1)
        ledger = {
            ticker: CostLedgerEntry(ticker, 0.0002, 0.0, 0.0, date(2026, 10, 1), "https://example.invalid/SYNTHETIC", "Synthetic fixture")
            for ticker in old
        }
        self.assertAlmostEqual(trade_cost(old, new, ledger), 0.00002)

    def test_missing_cost_evidence_stops(self) -> None:
        old = {"VT": 0.6, "LQD": 0.4}
        new = {"VT": 0.5, "LQD": 0.5}
        ledger = {
            ticker: CostLedgerEntry(ticker, None, 0.0, 0.0, None, "", "missing evidence")
            for ticker in old
        }
        with self.assertRaises(CostEvidenceError):
            trade_cost(old, new, ledger)


if __name__ == "__main__":
    unittest.main(verbosity=2)
