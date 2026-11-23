"""Evidence gates for transaction-cost inputs; no historical costs are assumed."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date


class CostEvidenceError(ValueError):
    """Raised when a trade-cost assumption lacks dated source evidence."""


@dataclass(frozen=True)
class CostLedgerEntry:
    ticker: str
    bid_ask_spread: float | None
    commission_rate: float | None
    market_impact_rate: float | None
    as_of_date: date | None
    source_url: str
    notes: str


def validate_cost_entry(entry: CostLedgerEntry) -> None:
    if not entry.ticker or not entry.source_url or entry.as_of_date is None:
        raise CostEvidenceError("STOP: cost entry needs ticker, source URL, and as-of date")
    for name, value in (
        ("bid_ask_spread", entry.bid_ask_spread),
        ("commission_rate", entry.commission_rate),
        ("market_impact_rate", entry.market_impact_rate),
    ):
        if value is None or value < 0:
            raise CostEvidenceError(f"STOP: {name} needs a nonnegative documented value")


def turnover(old_weights: dict[str, float], new_weights: dict[str, float]) -> float:
    if set(old_weights) != set(new_weights):
        raise ValueError("old and new weights must contain the same tickers")
    return 0.5 * sum(abs(new_weights[ticker] - old_weights[ticker]) for ticker in old_weights)


def trade_cost(old_weights: dict[str, float], new_weights: dict[str, float], ledger: dict[str, CostLedgerEntry]) -> float:
    if set(old_weights) != set(new_weights) or set(ledger) != set(new_weights):
        raise ValueError("weights and cost ledger must contain the same tickers")
    total = 0.0
    for ticker, new_weight in new_weights.items():
        entry = ledger[ticker]
        validate_cost_entry(entry)
        one_way_cost = 0.5 * entry.bid_ask_spread + entry.commission_rate + entry.market_impact_rate
        total += abs(new_weight - old_weights[ticker]) * one_way_cost
    return total
