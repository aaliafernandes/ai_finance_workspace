"""Project 2 gross historical portfolio analytics and transparent grid search.

This module reads only the approved Phase 2B price dataset. It applies target
weights at the first source-label date, lets holdings drift between annual
rebalance labels, and restores targets before the next interval at each later
annual rebalance. No costs, CPI, signal threshold, or recommendation is added.
"""

from __future__ import annotations

import csv
import json
import math
import sys
from dataclasses import asdict, dataclass
from datetime import date
from itertools import product
from pathlib import Path
from statistics import stdev
from typing import Iterable

# Permit the documented ``python src/portfolio_engine.py`` command in runtimes
# configured with safe-path imports. Tests add this same project-owned directory.
SRC_DIRECTORY = Path(__file__).resolve().parent
if str(SRC_DIRECTORY) not in sys.path:
    sys.path.insert(0, str(SRC_DIRECTORY))

from costs import turnover


TICKERS = ("BIL", "IEF", "LQD", "VT")
PROJECT_ROOT = Path(__file__).resolve().parents[1]
APPROVED_PRICES = PROJECT_ROOT / "data" / "processed" / "approved_monthly_prices.csv"
HYPOTHETICAL_START = {"BIL": 0.0, "IEF": 0.0, "LQD": 0.40, "VT": 0.60}
EQUAL_WEIGHT = {ticker: 0.25 for ticker in TICKERS}
POLICY_BENCHMARK = {"BIL": 0.0, "IEF": 0.0, "LQD": 0.40, "VT": 0.60}


class EngineInputError(ValueError):
    """The approved price file or a portfolio definition cannot be used."""


class InfeasiblePortfolioError(ValueError):
    """No candidate satisfies the explicitly selected mathematical constraints."""


@dataclass(frozen=True)
class PriceTable:
    labels: tuple[date, ...]
    prices: dict[str, tuple[float, ...]]


@dataclass(frozen=True)
class TurnoverEvent:
    label: date
    turnover: float
    kind: str


@dataclass(frozen=True)
class Analytics:
    return_count: int
    gross_geometric_annualized_return: float
    annualized_sample_volatility: float
    annualized_zero_target_downside_deviation: float
    maximum_drawdown: float
    complete_calendar_year_gross_returns: dict[str, float]
    turnover_events: tuple[TurnoverEvent, ...]
    monthly_returns: tuple[float, ...]
    wealth_index: tuple[float, ...]
    drawdown_series: tuple[float, ...]


@dataclass(frozen=True)
class PortfolioResult:
    name: str
    weights: dict[str, float]
    analytics: Analytics
    optimizer_rank_volatility: float | None = None
    scenario_label: str | None = None


def _month_after(value: date) -> date:
    return date(value.year + (value.month == 12), 1 if value.month == 12 else value.month + 1, 1)


def validate_weights(weights: dict[str, float]) -> None:
    if tuple(weights) != TICKERS:
        raise EngineInputError(f"weights must use exactly this ordered universe: {', '.join(TICKERS)}")
    if any(not math.isfinite(value) or value < 0 for value in weights.values()):
        raise EngineInputError("weights must be finite and long-only")
    if abs(sum(weights.values()) - 1.0) > 1e-10:
        raise EngineInputError("weights must sum to 1.0")


def _parse_price_rows(rows: Iterable[dict[str, str]]) -> PriceTable:
    rows = list(rows)
    if not rows:
        raise EngineInputError("approved prices file has no rows")
    expected = ["PeriodLabel", *TICKERS]
    if list(rows[0]) != expected:
        raise EngineInputError(f"approved prices headers must be exactly {expected}")
    labels: list[date] = []
    prices = {ticker: [] for ticker in TICKERS}
    for row in rows:
        try:
            label = date.fromisoformat(row["PeriodLabel"])
        except (KeyError, ValueError) as error:
            raise EngineInputError("PeriodLabel must be an ISO date") from error
        if label.day != 1:
            raise EngineInputError("PeriodLabel must be a source month label on day 1")
        labels.append(label)
        for ticker in TICKERS:
            try:
                value = float(row[ticker])
            except (KeyError, TypeError, ValueError) as error:
                raise EngineInputError(f"{ticker} has a nonnumeric price") from error
            if not math.isfinite(value) or value <= 0:
                raise EngineInputError(f"{ticker} has a nonpositive or nonfinite price")
            prices[ticker].append(value)
    if len(labels) < 3:
        raise EngineInputError("at least three approved prices are required")
    for left, right in zip(labels, labels[1:]):
        if _month_after(left) != right:
            raise EngineInputError("PeriodLabel values must be unique, ascending, and monthly contiguous")
    return PriceTable(tuple(labels), {ticker: tuple(values) for ticker, values in prices.items()})


def load_approved_prices(path: Path = APPROVED_PRICES) -> PriceTable:
    """Load the sole permitted price input for Project 2 analytics."""
    if path.resolve() != APPROVED_PRICES.resolve():
        raise EngineInputError("Project 2 analytics may load only approved_monthly_prices.csv")
    with path.open(newline="", encoding="utf-8") as handle:
        return _parse_price_rows(csv.DictReader(handle))


def asset_returns(table: PriceTable) -> dict[str, tuple[float, ...]]:
    return {
        ticker: tuple(current / previous - 1 for previous, current in zip(values, values[1:]))
        for ticker, values in table.prices.items()
    }


def annualized_sample_volatility(returns: Iterable[float]) -> float:
    values = tuple(returns)
    if len(values) < 2:
        raise EngineInputError("at least two returns are required for sample volatility")
    return stdev(values) * math.sqrt(12)


def annualized_zero_target_downside_deviation(returns: Iterable[float]) -> float:
    values = tuple(returns)
    if not values:
        raise EngineInputError("at least one return is required for downside deviation")
    return math.sqrt(sum(min(0.0, value) ** 2 for value in values) / len(values)) * math.sqrt(12)


def maximum_drawdown(returns: Iterable[float]) -> float:
    return min(drawdown_series(returns))


def wealth_index(returns: Iterable[float]) -> tuple[float, ...]:
    """Cumulative gross wealth beginning at 1.0 for display and validation."""
    wealth = 1.0
    values = [wealth]
    for value in returns:
        wealth *= 1 + value
        values.append(wealth)
    return tuple(values)


def drawdown_series(returns: Iterable[float]) -> tuple[float, ...]:
    """Drawdowns aligned with ``wealth_index``; initial value is zero."""
    peak = 1.0
    values: list[float] = []
    for wealth in wealth_index(returns):
        peak = max(peak, wealth)
        values.append(wealth / peak - 1)
    return tuple(values)


def _calendar_year_returns(labels: tuple[date, ...], returns: tuple[float, ...]) -> dict[str, float]:
    periods: dict[int, list[tuple[date, float]]] = {}
    # Return t belongs to the interval ending at labels[t + 1].
    for ending_label, value in zip(labels[1:], returns):
        periods.setdefault(ending_label.year, []).append((ending_label, value))
    result: dict[str, float] = {}
    for year, items in periods.items():
        if {item[0].month for item in items} == set(range(1, 13)) and len(items) == 12:
            gross = math.prod(1 + item[1] for item in items) - 1
            result[str(year)] = gross
    return result


def analytics_from_return_path(
    labels: tuple[date, ...],
    returns: Iterable[float],
    turnover_events: tuple[TurnoverEvent, ...] = (),
) -> Analytics:
    """Calculate gross path analytics for an already-defined monthly return path.

    This is used by the annual-rebalance simulation and by clearly labelled
    hypothetical stress transformations. It does not source prices or select
    portfolio weights.
    """
    values = tuple(returns)
    if len(labels) != len(values) + 1:
        raise EngineInputError("return path must have exactly one fewer value than labels")
    if len(values) < 2:
        raise EngineInputError("at least two returns are required for portfolio analytics")
    if any(not math.isfinite(value) or value <= -1 for value in values):
        raise EngineInputError("returns must be finite and greater than -100%")
    path_wealth = wealth_index(values)
    path_drawdowns = drawdown_series(values)
    return Analytics(
        return_count=len(values),
        gross_geometric_annualized_return=math.prod(1 + value for value in values) ** (12 / len(values)) - 1,
        annualized_sample_volatility=annualized_sample_volatility(values),
        annualized_zero_target_downside_deviation=annualized_zero_target_downside_deviation(values),
        maximum_drawdown=min(path_drawdowns),
        complete_calendar_year_gross_returns=_calendar_year_returns(labels, values),
        turnover_events=turnover_events,
        monthly_returns=values,
        wealth_index=path_wealth,
        drawdown_series=path_drawdowns,
    )


def simulate_annual_rebalance_path(
    table: PriceTable,
    target_weights: dict[str, float],
    starting_weights: dict[str, float] = HYPOTHETICAL_START,
    annual_rebalance_month: int | None = None,
) -> Analytics:
    """Apply targets at the first label and yearly before the next price interval.

    The first period label is the hypothetical initial-trade date. Holdings are
    then allowed to drift. At each later label sharing that month, target weights
    are restored before returns accrue into the following source-label period.
    """
    validate_weights(target_weights)
    validate_weights(starting_weights)
    if annual_rebalance_month is None:
        annual_rebalance_month = table.labels[0].month
    if not 1 <= annual_rebalance_month <= 12:
        raise EngineInputError("annual rebalance month must be 1 through 12")

    first_prices = {ticker: table.prices[ticker][0] for ticker in TICKERS}
    wealth = 1.0
    units = {ticker: target_weights[ticker] / first_prices[ticker] for ticker in TICKERS}
    events = [TurnoverEvent(table.labels[0], turnover(starting_weights, target_weights), "initial_hypothetical")]
    returns: list[float] = []

    for index in range(len(table.labels) - 1):
        label = table.labels[index]
        if index > 0 and label.month == annual_rebalance_month:
            current_values = {ticker: units[ticker] * table.prices[ticker][index] for ticker in TICKERS}
            wealth = sum(current_values.values())
            pretrade = {ticker: current_values[ticker] / wealth for ticker in TICKERS}
            events.append(TurnoverEvent(label, turnover(pretrade, target_weights), "annual_drift_rebalance"))
            units = {ticker: target_weights[ticker] * wealth / table.prices[ticker][index] for ticker in TICKERS}
        before = sum(units[ticker] * table.prices[ticker][index] for ticker in TICKERS)
        after = sum(units[ticker] * table.prices[ticker][index + 1] for ticker in TICKERS)
        returns.append(after / before - 1)

    return analytics_from_return_path(table.labels, tuple(returns), tuple(events))


def grid_weights(step: float = 0.05) -> Iterable[dict[str, float]]:
    if not 0 < step <= 1 or abs(round(1 / step) * step - 1) > 1e-10:
        raise EngineInputError("grid step must divide 1 exactly")
    count = round(1 / step)
    for bil, ief, lqd in product(range(count + 1), repeat=3):
        vt = count - bil - ief - lqd
        if vt >= 0:
            yield {"BIL": bil * step, "IEF": ief * step, "LQD": lqd * step, "VT": vt * step}


def constrained_minimum_volatility(
    table: PriceTable,
    turnover_cap: float = 0.25,
    step: float = 0.05,
    bil_scenario_floor: float | None = None,
) -> PortfolioResult:
    """Rank feasible candidates by realized annual-rebalance path volatility.

    Constraints here are only mathematical: approved universe, long-only,
    weights summing to one, turnover at every modeled rebalance, and optional
    *scenario* BIL floor. Evidence-dependent mandate rules remain outside the
    optimizer and receive UNVERIFIED verdicts.
    """
    if not 0 <= turnover_cap <= 1:
        raise EngineInputError("turnover cap must be between zero and one")
    if bil_scenario_floor is not None and not 0 <= bil_scenario_floor <= 1:
        raise EngineInputError("BIL scenario floor must be between zero and one")
    feasible: list[PortfolioResult] = []
    rejection_counts = {"turnover": 0, "bil_scenario": 0}
    for weights in grid_weights(step):
        if bil_scenario_floor is not None and weights["BIL"] + 1e-12 < bil_scenario_floor:
            rejection_counts["bil_scenario"] += 1
            continue
        analytics = simulate_annual_rebalance_path(table, weights)
        if any(event.turnover > turnover_cap + 1e-12 for event in analytics.turnover_events):
            rejection_counts["turnover"] += 1
            continue
        feasible.append(
            PortfolioResult(
                "Constrained minimum-volatility",
                weights,
                analytics,
                analytics.annualized_sample_volatility,
                "10% BIL scenario" if bil_scenario_floor is not None else None,
            )
        )
    if not feasible:
        raise InfeasiblePortfolioError(
            "INFEASIBLE: no grid candidate survived turnover"
            + (" and BIL scenario" if bil_scenario_floor is not None else "")
            + f" constraints; rejections={rejection_counts}"
        )
    return min(
        feasible,
        key=lambda result: (
            result.analytics.annualized_sample_volatility,
            sum(event.turnover for event in result.analytics.turnover_events),
            tuple(result.weights[ticker] for ticker in TICKERS),
        ),
    )


def baseline_results(table: PriceTable) -> tuple[PortfolioResult, PortfolioResult]:
    return (
        PortfolioResult("Equal weight", EQUAL_WEIGHT, simulate_annual_rebalance_path(table, EQUAL_WEIGHT)),
        PortfolioResult("Policy benchmark", POLICY_BENCHMARK, simulate_annual_rebalance_path(table, POLICY_BENCHMARK)),
    )


def result_as_dict(result: PortfolioResult) -> dict[str, object]:
    data = asdict(result)
    data["analytics"]["turnover_events"] = [asdict(event) for event in result.analytics.turnover_events]
    return data


def main() -> None:
    # Local import avoids a module-level cycle: verdicts validate engine types.
    from mandate_verdicts import assessment_as_dict, assess

    table = load_approved_prices()
    equal, benchmark = baseline_results(table)
    constrained = constrained_minimum_volatility(table)
    results = (equal, benchmark, constrained)
    print(
        json.dumps(
            [
                {
                    "portfolio": result_as_dict(item),
                    "mandate_assessment": assessment_as_dict(assess(item.weights, item.analytics.turnover_events)),
                }
                for item in results
            ],
            indent=2,
            default=str,
        )
    )


if __name__ == "__main__":
    main()
