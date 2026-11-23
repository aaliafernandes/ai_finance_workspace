"""Point-in-time provenance checks for the monitor-only credit-spread signal."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from typing import Iterable


class SignalAvailabilityError(ValueError):
    """Raised when no documented signal observation was available at cutoff."""


@dataclass(frozen=True)
class SignalObservation:
    measured_date: date
    value_percent: float
    vintage_date: date
    source_url: str


def latest_available_signal(observations: Iterable[SignalObservation], decision_cutoff: date) -> SignalObservation:
    eligible = [
        item
        for item in observations
        if item.measured_date <= decision_cutoff and item.vintage_date <= decision_cutoff
    ]
    if not eligible:
        raise SignalAvailabilityError("STOP: no documented signal vintage was available by the decision cutoff")
    return max(eligible, key=lambda item: (item.measured_date, item.vintage_date))
