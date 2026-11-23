"""Tests that UNVERIFIED evidence cannot become a mandate PASS."""

from __future__ import annotations

import sys
import unittest
from datetime import date
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from mandate_verdicts import assess
from portfolio_engine import TurnoverEvent


VALID = {"BIL": 0.0, "IEF": 0.0, "LQD": 0.40, "VT": 0.60}


class MandateVerdictTests(unittest.TestCase):
    def test_math_rules_pass_but_evidence_rules_remain_unverified(self) -> None:
        assessment = assess(VALID, [TurnoverEvent(date(2026, 10, 1), 0.10, "initial_hypothetical")])
        by_rule = {item.rule: item for item in assessment.rules}
        self.assertEqual(by_rule["Approved four-ETF universe"].status, "PASS")
        self.assertEqual(by_rule["Annual turnover <= 25%"].status, "PASS")
        self.assertEqual(by_rule["CPI + 4% net rolling five-year objective"].status, "UNVERIFIED")
        self.assertFalse(assessment.decision_ready)

    def test_turnover_breach_fails(self) -> None:
        assessment = assess(VALID, [TurnoverEvent(date(2026, 10, 1), 0.251, "annual_drift_rebalance")])
        turnover_rule = next(item for item in assessment.rules if item.rule == "Annual turnover <= 25%")
        self.assertEqual(turnover_rule.status, "FAIL")
        self.assertFalse(assessment.decision_ready)

    def test_invalid_weights_fail_and_empty_events_do_not_pass(self) -> None:
        invalid = {"BIL": 0.0, "IEF": 0.0, "LQD": 0.4, "OTHER": 0.6}
        assessment = assess(invalid, [])
        by_rule = {item.rule: item for item in assessment.rules}
        self.assertEqual(by_rule["Approved four-ETF universe"].status, "FAIL")
        self.assertEqual(by_rule["Annual turnover <= 25%"].status, "FAIL")

