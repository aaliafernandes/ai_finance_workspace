"""Synthetic-only tests for Phase 5A stress infrastructure.

These tests deliberately do not load or execute any proposed locked changed-input
case against the approved Project 2 dataset.
"""

from __future__ import annotations

import sys
import unittest
from datetime import date
from unittest.mock import patch
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from portfolio_engine import EngineInputError, PriceTable, TurnoverEvent, analytics_from_return_path
from stress_tests import (
    APPROVED_NONLOCKED_CASES,
    StressCase,
    StressInputs,
    StressStatus,
    apply_hypothetical_cost_stress,
    apply_return_risk_stress,
    changed_input_names,
    run_project_stress_case,
    run_stress_case,
    stress_summary,
    trailing_window,
)


def monthly_labels(start_year: int, start_month: int, count: int) -> tuple[date, ...]:
    labels = []
    year, month = start_year, start_month
    for _ in range(count):
        labels.append(date(year, month, 1))
        year += month == 12
        month = 1 if month == 12 else month + 1
    return tuple(labels)


def synthetic_table(count: int = 25) -> PriceTable:
    labels = monthly_labels(2024, 1, count)
    # LQD and VT vary so that a zero turnover cap is infeasible after drift.
    return PriceTable(
        labels,
        {
            "BIL": tuple(100.0 + index * 0.05 for index in range(count)),
            "IEF": tuple(100.0 + (-1) ** index * 0.4 for index in range(count)),
            "LQD": tuple(100.0 * 1.01**index for index in range(count)),
            "VT": tuple(100.0 * 0.995**index for index in range(count)),
        },
    )


class StressInfrastructureTests(unittest.TestCase):
    def test_window_uses_last_requested_returns_and_stops_for_unverified_evidence(self) -> None:
        table = synthetic_table()
        case = StressCase("synthetic window", StressInputs(estimation_window_returns=12), "Synthetic window test.")
        run = run_stress_case(table, case)
        self.assertEqual(run.return_count, 12)
        self.assertEqual(run.source_start, table.labels[-13].isoformat())
        self.assertEqual(run.status, StressStatus.STOP_UNVERIFIED_MANDATE_EVIDENCE)
        self.assertTrue(run.stop_reasons)

    def test_return_and_risk_transform_has_known_answer(self) -> None:
        labels = (date(2025, 1, 1), date(2025, 2, 1), date(2025, 3, 1))
        analytics = analytics_from_return_path(labels, (0.01, -0.01))
        stressed = apply_return_risk_stress(analytics, labels, shift=0.001, multiplier=2.0)
        self.assertEqual(stressed.monthly_returns, (0.021, -0.019))

    def test_hypothetical_cost_has_known_turnover_based_effect(self) -> None:
        labels = (date(2025, 1, 1), date(2025, 2, 1), date(2025, 3, 1))
        analytics = analytics_from_return_path(
            labels,
            (0.0, 0.0),
            (TurnoverEvent(labels[0], 0.50, "initial_hypothetical"),),
        )
        stressed = apply_hypothetical_cost_stress(analytics, labels, one_way_cost_bps=100.0)
        self.assertAlmostEqual(stressed.monthly_returns[0], -0.005, places=12)
        self.assertAlmostEqual(stressed.monthly_returns[1], 0.0, places=12)

    def test_constraint_cases_cover_turnover_and_separate_bil_scenario(self) -> None:
        table = synthetic_table()
        turnover_case = StressCase("synthetic zero turnover", StressInputs(turnover_cap=0.0), "Synthetic infeasibility test.")
        self.assertEqual(run_stress_case(table, turnover_case).status, StressStatus.STOP_INFEASIBLE)

        bil_case = StressCase("synthetic BIL scenario", StressInputs(bil_scenario_floor=0.10), "Synthetic BIL scenario test.")
        run = run_stress_case(table, bil_case)
        self.assertEqual(run.status, StressStatus.STOP_UNVERIFIED_MANDATE_EVIDENCE)
        self.assertEqual(run.portfolios[-1].name, "Constrained minimum-volatility")

    def test_multiple_changed_inputs_and_invalid_window_stop(self) -> None:
        table = synthetic_table()
        combined = StressCase("combined", StressInputs(monthly_return_shift=0.001, turnover_cap=0.20), "Must stop.")
        self.assertEqual(run_stress_case(table, combined).status, StressStatus.STOP_INVALID_STRESS_INPUT)

        invalid_window = StressCase("too long", StressInputs(estimation_window_returns=30), "Must stop.")
        self.assertEqual(run_stress_case(table, invalid_window).status, StressStatus.STOP_INVALID_STRESS_INPUT)

    def test_project_loader_failure_is_data_integrity_stop(self) -> None:
        case = StressCase("loader failure", StressInputs(monthly_return_shift=0.001), "Synthetic loader gate test.")
        with patch("stress_tests.load_approved_prices", side_effect=EngineInputError("invalid approved input")):
            run = run_project_stress_case(case)
        self.assertEqual(run.status, StressStatus.STOP_DATA_INTEGRITY)

    def test_window_helper_and_changed_input_labels(self) -> None:
        table = synthetic_table()
        self.assertEqual(len(trailing_window(table, 8).labels), 9)
        self.assertEqual(changed_input_names(StressInputs(hypothetical_one_way_cost_bps=25.0)), ("hypothetical_one_way_cost_bps",))

    def test_nonlocked_catalog_and_summary_are_one_input_only(self) -> None:
        self.assertEqual(len(APPROVED_NONLOCKED_CASES), 5)
        self.assertTrue(all(len(changed_input_names(case.inputs)) == 1 for case in APPROVED_NONLOCKED_CASES))
        run = run_stress_case(synthetic_table(), APPROVED_NONLOCKED_CASES[0])
        summary = stress_summary(run)
        self.assertEqual(summary["case"], APPROVED_NONLOCKED_CASES[0].name)
        self.assertEqual(summary["changed_input"], ("monthly_return_shift",))
        self.assertEqual(len(summary["portfolios"]), 3)

