"""CPI + 4% hurdle logic; live CPI loading is deliberately out of scope."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime


class CpiAvailabilityError(ValueError):
    """Raised when a CPI observation was not public by the evaluation cutoff."""


@dataclass(frozen=True)
class CpiObservation:
    measured_month: date
    index_value: float
    published_at: datetime
    source_label: str


def months_between(start: date, end: date) -> int:
    return (end.year - start.year) * 12 + end.month - start.month


def compounded_five_year_hurdle(
    start: CpiObservation, end: CpiObservation, evaluation_cutoff: datetime, real_return_target: float = 0.04
) -> float:
    """Return the 60-month nominal hurdle implied by CPI inflation plus 4% annually."""
    if months_between(start.measured_month, end.measured_month) != 60:
        raise ValueError("CPI observations must be exactly 60 months apart")
    if start.index_value <= 0 or end.index_value <= 0:
        raise ValueError("CPI index values must be positive")
    if start.published_at > evaluation_cutoff or end.published_at > evaluation_cutoff:
        raise CpiAvailabilityError("CPI observation was not public by the evaluation cutoff")
    return (end.index_value / start.index_value) * (1 + real_return_target) ** 5 - 1
