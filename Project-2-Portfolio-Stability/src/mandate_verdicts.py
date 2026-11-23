"""Rule-specific portfolio verdicts that preserve FAIL and UNVERIFIED states."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Iterable

from portfolio_engine import TICKERS, TurnoverEvent, validate_weights


@dataclass(frozen=True)
class RuleVerdict:
    rule: str
    status: str  # PASS, FAIL, UNVERIFIED, or SCENARIO
    measurement: str
    reason: str


@dataclass(frozen=True)
class MandateAssessment:
    rules: tuple[RuleVerdict, ...]
    decision_ready: bool
    summary: str


def assess(weights: dict[str, float], turnover_events: Iterable[TurnoverEvent], turnover_cap: float = 0.25) -> MandateAssessment:
    rules: list[RuleVerdict] = []
    try:
        validate_weights(weights)
        rules.extend(
            [
                RuleVerdict("Approved four-ETF universe", "PASS", ", ".join(weights), "Exact approved ticker set."),
                RuleVerdict("Long-only", "PASS", f"minimum weight={min(weights.values()):.2%}", "All weights are nonnegative."),
                RuleVerdict("Weights sum to 100%", "PASS", f"sum={sum(weights.values()):.2%}", "Mathematical weight check."),
            ]
        )
    except ValueError as error:
        rules.extend(
            [
                RuleVerdict("Approved four-ETF universe", "FAIL", "invalid", str(error)),
                RuleVerdict("Long-only", "FAIL", "invalid", str(error)),
                RuleVerdict("Weights sum to 100%", "FAIL", "invalid", str(error)),
            ]
        )
    events = tuple(turnover_events)
    highest = max((item.turnover for item in events), default=float("inf"))
    rules.append(
        RuleVerdict(
            "Annual turnover <= 25%",
            "PASS" if highest <= turnover_cap + 1e-12 else "FAIL",
            "no events" if not events else f"highest modeled turnover={highest:.2%}",
            "Uses hypothetical 60% VT / 40% LQD initial weights; later events reflect modeled drift.",
        )
    )
    rules.extend(
        [
            RuleVerdict("3% liquidity reserve", "UNVERIFIED", "not calculated", "BIL/IEF reserve eligibility is not client-approved."),
            RuleVerdict("90% redeemable within five business days", "UNVERIFIED", "not calculated", "ETF redemption/liquidity definition is unresolved."),
            RuleVerdict("8% issuer concentration / ETF look-through", "UNVERIFIED", "not calculated", "Wrapper versus look-through policy is unresolved."),
            RuleVerdict("CPI + 4% net rolling five-year objective", "UNVERIFIED", "59 gross monthly returns", "CPI release evidence, costs, and a full 60-return period are unavailable."),
            RuleVerdict("Calendar-year net loss review trigger", "UNVERIFIED", "gross data only", "Net-return definition and breach rule are unresolved."),
            RuleVerdict("Credit-spread signal", "UNVERIFIED", "monitor only", "No approved ALFRED vintage evidence or threshold exists."),
            RuleVerdict("10% BIL minimum", "SCENARIO", f"BIL weight={weights.get('BIL', 0):.2%}", "Student-proposed scenario, not a client mandate."),
        ]
    )
    has_fail = any(rule.status == "FAIL" for rule in rules)
    has_unverified = any(rule.status == "UNVERIFIED" for rule in rules)
    summary = "NOT DECISION-READY: " + ("a mathematical rule failed" if has_fail else "required mandate evidence is unresolved")
    return MandateAssessment(tuple(rules), not has_fail and not has_unverified, summary)


def assessment_as_dict(assessment: MandateAssessment) -> dict[str, object]:
    return {"rules": [asdict(rule) for rule in assessment.rules], "decision_ready": assessment.decision_ready, "summary": assessment.summary}
