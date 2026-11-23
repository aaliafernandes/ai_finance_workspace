"""One-input-at-a-time Project 2 stress-test infrastructure.

This module deliberately produces analytical-only gross results. It never
claims that a stressed case is decision-ready and contains no locked changed-
input case or prediction.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, replace
from enum import Enum

from mandate_verdicts import MandateAssessment, assess
from portfolio_engine import (
    Analytics,
    EngineInputError,
    InfeasiblePortfolioError,
    PortfolioResult,
    PriceTable,
    TurnoverEvent,
    analytics_from_return_path,
    baseline_results,
    constrained_minimum_volatility,
    load_approved_prices,
)


class StressStatus(str, Enum):
    ANALYTICAL_ONLY = "ANALYTICAL_ONLY"
    STOP_DATA_INTEGRITY = "STOP_DATA_INTEGRITY"
    STOP_INFEASIBLE = "STOP_INFEASIBLE"
    STOP_INVALID_STRESS_INPUT = "STOP_INVALID_STRESS_INPUT"
    STOP_UNVERIFIED_MANDATE_EVIDENCE = "STOP_UNVERIFIED_MANDATE_EVIDENCE"


@dataclass(frozen=True)
class StressInputs:
    """Exactly one non-base field is allowed in a reproducible sensitivity run."""

    estimation_window_returns: int | None = None
    monthly_return_shift: float = 0.0
    monthly_risk_multiplier: float = 1.0
    hypothetical_one_way_cost_bps: float = 0.0
    turnover_cap: float = 0.25
    bil_scenario_floor: float | None = None


BASE_INPUTS = StressInputs()


@dataclass(frozen=True)
class StressCase:
    name: str
    inputs: StressInputs
    description: str


@dataclass(frozen=True)
class StressPortfolio:
    name: str
    weights: dict[str, float]
    analytics: Analytics
    selection_volatility: float | None


@dataclass(frozen=True)
class StressRun:
    case: StressCase
    status: StressStatus
    stop_reasons: tuple[str, ...]
    portfolios: tuple[StressPortfolio, ...]
    assessment: tuple[MandateAssessment, ...]
    source_start: str | None
    source_end: str | None
    return_count: int | None


APPROVED_NONLOCKED_CASES = (
    StressCase(
        "Hypothetical return shift: -10 bps monthly",
        StressInputs(monthly_return_shift=-0.001),
        "Student-proposed analytical downside return sensitivity; not a forecast.",
    ),
    StressCase(
        "Hypothetical risk scale: 1.25x",
        StressInputs(monthly_risk_multiplier=1.25),
        "Student-proposed dispersion sensitivity; not a covariance forecast.",
    ),
    StressCase(
        "Hypothetical one-way trading cost: 25 bps",
        StressInputs(hypothetical_one_way_cost_bps=25.0),
        "Unsourced transaction-cost sensitivity; not an observed cost estimate.",
    ),
    StressCase(
        "Turnover constraint: 20%",
        StressInputs(turnover_cap=0.20),
        "Student-proposed tighter turnover constraint sensitivity.",
    ),
    StressCase(
        "BIL scenario floor: 10%",
        StressInputs(bil_scenario_floor=0.10),
        "Student-proposed BIL scenario; not a client mandate.",
    ),
)


def changed_input_names(inputs: StressInputs) -> tuple[str, ...]:
    return tuple(
        name
        for name in (
            "estimation_window_returns",
            "monthly_return_shift",
            "monthly_risk_multiplier",
            "hypothetical_one_way_cost_bps",
            "turnover_cap",
            "bil_scenario_floor",
        )
        if getattr(inputs, name) != getattr(BASE_INPUTS, name)
    )


def validate_stress_case(case: StressCase) -> str:
    if not case.name.strip() or not case.description.strip():
        raise ValueError("stress case needs a nonempty name and description")
    changed = changed_input_names(case.inputs)
    if len(changed) != 1:
        raise ValueError("one-input-at-a-time stress case must change exactly one base input")
    inputs = case.inputs
    if inputs.estimation_window_returns is not None and inputs.estimation_window_returns < 2:
        raise ValueError("estimation window must contain at least two returns")
    if not math.isfinite(inputs.monthly_return_shift):
        raise ValueError("monthly return shift must be finite")
    if not math.isfinite(inputs.monthly_risk_multiplier) or inputs.monthly_risk_multiplier <= 0:
        raise ValueError("monthly risk multiplier must be finite and positive")
    if not math.isfinite(inputs.hypothetical_one_way_cost_bps) or inputs.hypothetical_one_way_cost_bps < 0:
        raise ValueError("hypothetical cost must be finite and nonnegative")
    if not 0 <= inputs.turnover_cap <= 1:
        raise ValueError("turnover cap must be between zero and one")
    if inputs.bil_scenario_floor is not None and not 0 <= inputs.bil_scenario_floor <= 1:
        raise ValueError("BIL scenario floor must be between zero and one")
    return changed[0]


def trailing_window(table: PriceTable, returns: int | None) -> PriceTable:
    if returns is None:
        return table
    if returns >= len(table.labels):
        raise EngineInputError("estimation window must be shorter than the available return history")
    labels = table.labels[-(returns + 1) :]
    prices = {ticker: values[-(returns + 1) :] for ticker, values in table.prices.items()}
    return PriceTable(labels, prices)


def apply_return_risk_stress(analytics: Analytics, labels: tuple, shift: float, multiplier: float) -> Analytics:
    """Stylized return/risk sensitivity on a fixed engine-produced return path."""
    returns = analytics.monthly_returns
    mean_return = sum(returns) / len(returns)
    stressed = tuple(mean_return + multiplier * (value - mean_return) + shift for value in returns)
    return analytics_from_return_path(labels, stressed, analytics.turnover_events)


def apply_hypothetical_cost_stress(analytics: Analytics, labels: tuple, one_way_cost_bps: float) -> Analytics:
    """Apply unsourced hypothetical costs to intervals beginning on trade labels.

    This is a sensitivity only. It is not a cost estimate and never substitutes
    for the dated cost-evidence ledger required by the mandate.
    """
    if not math.isfinite(one_way_cost_bps) or one_way_cost_bps < 0:
        raise ValueError("hypothetical cost must be finite and nonnegative")
    turnover_by_label = {event.label: event.turnover for event in analytics.turnover_events}
    cost_rate = one_way_cost_bps / 10_000
    stressed = tuple(
        (1 + gross_return) * (1 - turnover_by_label.get(label, 0.0) * cost_rate) - 1
        for label, gross_return in zip(labels, analytics.monthly_returns)
    )
    return analytics_from_return_path(labels, stressed, analytics.turnover_events)


def _as_stress_portfolio(result: PortfolioResult, analytics: Analytics | None = None) -> StressPortfolio:
    final_analytics = result.analytics if analytics is None else analytics
    return StressPortfolio(result.name, result.weights, final_analytics, result.optimizer_rank_volatility)


def run_stress_case(table: PriceTable, case: StressCase) -> StressRun:
    """Run one permitted sensitivity while retaining a mandatory decision STOP gate."""
    try:
        changed = validate_stress_case(case)
        working_table = trailing_window(table, case.inputs.estimation_window_returns)
        equal_weight, benchmark = baseline_results(working_table)
        constrained = constrained_minimum_volatility(
            working_table,
            turnover_cap=case.inputs.turnover_cap,
            bil_scenario_floor=case.inputs.bil_scenario_floor,
        )
        portfolio_results = (equal_weight, benchmark, constrained)
        stressed: list[StressPortfolio] = []
        for result in portfolio_results:
            analytics = result.analytics
            if changed in {"monthly_return_shift", "monthly_risk_multiplier"}:
                analytics = apply_return_risk_stress(
                    analytics,
                    working_table.labels,
                    case.inputs.monthly_return_shift,
                    case.inputs.monthly_risk_multiplier,
                )
            elif changed == "hypothetical_one_way_cost_bps":
                analytics = apply_hypothetical_cost_stress(
                    analytics,
                    working_table.labels,
                    case.inputs.hypothetical_one_way_cost_bps,
                )
            stressed.append(_as_stress_portfolio(result, analytics))
        assessments = tuple(assess(result.weights, result.analytics.turnover_events, case.inputs.turnover_cap) for result in portfolio_results)
        evidence_reasons = tuple(
            f"{portfolio.name}: unresolved evidence-dependent mandate rules"
            for portfolio, assessment in zip(stressed, assessments)
            if not assessment.decision_ready
        )
        return StressRun(
            case=case,
            status=StressStatus.STOP_UNVERIFIED_MANDATE_EVIDENCE if evidence_reasons else StressStatus.ANALYTICAL_ONLY,
            stop_reasons=evidence_reasons,
            portfolios=tuple(stressed),
            assessment=assessments,
            source_start=working_table.labels[0].isoformat(),
            source_end=working_table.labels[-1].isoformat(),
            return_count=len(working_table.labels) - 1,
        )
    except InfeasiblePortfolioError as error:
        return StressRun(case, StressStatus.STOP_INFEASIBLE, (str(error),), (), (), None, None, None)
    except (EngineInputError, ValueError) as error:
        return StressRun(case, StressStatus.STOP_INVALID_STRESS_INPUT, (str(error),), (), (), None, None, None)


def run_project_stress_case(case: StressCase) -> StressRun:
    """Load only the approved project input and stop on its validation failure."""
    try:
        table = load_approved_prices()
    except (EngineInputError, OSError) as error:
        return StressRun(case, StressStatus.STOP_DATA_INTEGRITY, (str(error),), (), (), None, None, None)
    return run_stress_case(table, case)


def stress_summary(run: StressRun) -> dict[str, object]:
    """Compact, presentation-safe stress record; no additional finance calculation."""
    return {
        "case": run.case.name,
        "changed_input": changed_input_names(run.case.inputs),
        "status": run.status.value,
        "stop_reasons": run.stop_reasons,
        "source_start": run.source_start,
        "source_end": run.source_end,
        "return_count": run.return_count,
        "portfolios": [
            {
                "name": portfolio.name,
                "weights": portfolio.weights,
                "annualized_sample_volatility": portfolio.analytics.annualized_sample_volatility,
                "gross_geometric_annualized_return": portfolio.analytics.gross_geometric_annualized_return,
                "maximum_drawdown": portfolio.analytics.maximum_drawdown,
                "highest_modeled_turnover": max(event.turnover for event in portfolio.analytics.turnover_events),
            }
            for portfolio in run.portfolios
        ],
    }
