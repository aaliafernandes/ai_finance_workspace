"""Known-answer and negative tests for the Phase 3B portfolio engine."""

from __future__ import annotations

import sys
import unittest
from datetime import date
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from portfolio_engine import (
    APPROVED_PRICES,
    EngineInputError,
    InfeasiblePortfolioError,
    PriceTable,
    annualized_sample_volatility,
    annualized_zero_target_downside_deviation,
    baseline_results,
    constrained_minimum_volatility,
    load_approved_prices,
    maximum_drawdown,
    _parse_price_rows,
    simulate_annual_rebalance_path,
    validate_weights,
)


TARGET = {"BIL": 0.0, "IEF": 0.0, "LQD": 0.40, "VT": 0.60}


def price_table(labels: list[date], prices: dict[str, list[float]]) -> PriceTable:
    return PriceTable(tuple(labels), {ticker: tuple(prices[ticker]) for ticker in ("BIL", "IEF", "LQD", "VT")})


class PortfolioMetricKnownAnswerTests(unittest.TestCase):
    def test_100_to_110_is_ten_percent_monthly_return(self) -> None:
        table = price_table(
            [date(2026, 1, 1), date(2026, 2, 1), date(2026, 3, 1)],
            {ticker: [100.0, 110.0, 110.0] for ticker in TARGET},
        )
        result = simulate_annual_rebalance_path(table, TARGET)
        self.assertAlmostEqual(result.monthly_returns[0], 0.10, places=12)

    def test_weighted_one_period_return_is_two_percent(self) -> None:
        table = price_table(
            [date(2026, 1, 1), date(2026, 2, 1), date(2026, 3, 1)],
            {
                "BIL": [100.0, 100.0, 100.0],
                "IEF": [100.0, 100.0, 100.0],
                "LQD": [100.0, 90.0, 90.0],
                "VT": [100.0, 110.0, 110.0],
            },
        )
        result = simulate_annual_rebalance_path(table, TARGET)
        self.assertAlmostEqual(result.monthly_returns[0], 0.02, places=12)

    def test_sample_volatility_and_zero_target_downside_known_answers(self) -> None:
        returns = (0.01, -0.01, 0.01, -0.01)
        self.assertAlmostEqual(annualized_sample_volatility(returns), 0.04, places=12)
        self.assertAlmostEqual(annualized_zero_target_downside_deviation(returns), 0.0244948974, places=10)

    def test_maximum_drawdown_known_answer(self) -> None:
        # 1.00 -> 1.10 -> 0.99 -> 1.089: trough is 10% below the peak.
        returns = (0.10, -0.10, 0.10)
        self.assertAlmostEqual(maximum_drawdown(returns), -0.10, places=12)

    def test_initial_turnover_to_equal_weight_is_fifty_percent(self) -> None:
        table = price_table(
            [date(2026, 1, 1), date(2026, 2, 1), date(2026, 3, 1)],
            {ticker: [100.0, 100.0, 100.0] for ticker in TARGET},
        )
        equal = {ticker: 0.25 for ticker in TARGET}
        result = simulate_annual_rebalance_path(table, equal)
        self.assertAlmostEqual(result.turnover_events[0].turnover, 0.50, places=12)

    def test_drift_and_subsequent_annual_turnover_known_answer(self) -> None:
        labels = [date(2021, month, 1) for month in (10, 11, 12)]
        labels += [date(2022, month, 1) for month in range(1, 12)]
        prices = {ticker: [100.0] * len(labels) for ticker in TARGET}
        # A 10% LQD move after initial allocation drifts LQD to 44/104.
        prices["LQD"] = [100.0, 110.0] + [110.0] * (len(labels) - 2)
        result = simulate_annual_rebalance_path(price_table(labels, prices), TARGET)
        self.assertEqual([event.kind for event in result.turnover_events], ["initial_hypothetical", "annual_drift_rebalance"])
        self.assertAlmostEqual(result.turnover_events[0].turnover, 0.0, places=12)
        self.assertAlmostEqual(result.turnover_events[1].turnover, 0.023076923076923, places=12)

    def test_complete_calendar_year_compounds_twelve_intervals(self) -> None:
        labels = [date(2025, 12, 1)] + [date(2026, month, 1) for month in range(1, 13)]
        prices = {ticker: [100.0 * 1.01**index for index in range(13)] for ticker in TARGET}
        result = simulate_annual_rebalance_path(price_table(labels, prices), TARGET)
        self.assertAlmostEqual(result.complete_calendar_year_gross_returns["2026"], 1.01**12 - 1, places=12)


class PortfolioEngineInputAndOptimizationTests(unittest.TestCase):
    def test_approved_dataset_and_baselines_are_loadable(self) -> None:
        table = load_approved_prices()
        self.assertEqual(table.labels[0], date(2021, 10, 1))
        self.assertEqual(table.labels[-1], date(2026, 9, 1))
        self.assertEqual(len(table.labels), 60)
        equal, benchmark = baseline_results(table)
        self.assertEqual(equal.weights, {ticker: 0.25 for ticker in TARGET})
        self.assertEqual(benchmark.weights, TARGET)

    def test_loader_rejects_any_nonapproved_path(self) -> None:
        with self.assertRaises(EngineInputError):
            load_approved_prices(PROJECT_ROOT / "data" / "processed" / "prices.csv")

    def test_parser_rejects_bad_header_and_misaligned_month(self) -> None:
        with self.assertRaises(EngineInputError):
            _parse_price_rows([{"PeriodLabel": "2026-01-01", "BIL": "1", "IEF": "1", "LQD": "1", "BAD": "1"}])
        with self.assertRaises(EngineInputError):
            _parse_price_rows(
                [
                    {"PeriodLabel": "2026-01-01", "BIL": "1", "IEF": "1", "LQD": "1", "VT": "1"},
                    {"PeriodLabel": "2026-03-01", "BIL": "1", "IEF": "1", "LQD": "1", "VT": "1"},
                    {"PeriodLabel": "2026-04-01", "BIL": "1", "IEF": "1", "LQD": "1", "VT": "1"},
                ]
            )

    def test_invalid_weights_fail(self) -> None:
        with self.assertRaises(EngineInputError):
            validate_weights({"BIL": 0.25, "IEF": 0.25, "LQD": 0.25, "VT": 0.20})
        with self.assertRaises(EngineInputError):
            validate_weights({"BIL": 0.25, "IEF": 0.25, "LQD": -0.25, "VT": 0.75})

    def test_infeasible_turnover_constraint_does_not_fallback(self) -> None:
        table = load_approved_prices()
        with self.assertRaises(InfeasiblePortfolioError):
            constrained_minimum_volatility(table, turnover_cap=0.0)

    def test_grid_optimizer_is_deterministic_and_uses_five_point_weights(self) -> None:
        table = load_approved_prices()
        first = constrained_minimum_volatility(table)
        second = constrained_minimum_volatility(table)
        self.assertEqual(first.weights, second.weights)
        self.assertAlmostEqual(first.optimizer_rank_volatility or 0, first.analytics.annualized_sample_volatility, places=15)
        self.assertTrue(all(round(weight / 0.05) * 0.05 == weight for weight in first.weights.values()))
        self.assertTrue(all(event.turnover <= 0.25 + 1e-12 for event in first.analytics.turnover_events))

    def test_two_asset_theoretical_minimum_variance_sanity_check(self) -> None:
        # Independent monthly volatilities 1% and 2% imply w_A = .02^2/(.01^2+.02^2) = 80%.
        variance_a, variance_b = 0.01**2, 0.02**2
        weight_a = variance_b / (variance_a + variance_b)
        self.assertAlmostEqual(weight_a, 0.80, places=12)
        # The production optimizer intentionally does not rank this covariance shortcut;
        # it ranks the annual-rebalance realized-path volatility tested immediately above.

