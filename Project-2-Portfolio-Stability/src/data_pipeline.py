"""Validate archived Yahoo monthly data without overwriting the Lab 15 dataset.

Yahoo's ``interval=1mo`` timestamps are retained as source period labels. This
module does not call a label a month-end close. It excludes every observation
whose period label falls in the retrieval month because that period can be
incomplete and may contain more than one raw observation.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
from collections import defaultdict
from dataclasses import dataclass
from datetime import UTC, date, datetime
from pathlib import Path
from typing import Iterable


TICKERS = ("BIL", "IEF", "LQD", "VT")


class DataGateError(ValueError):
    """A data-quality gate failed; no approved dataset may be produced."""


@dataclass(frozen=True)
class RawObservation:
    ticker: str
    timestamp_utc: datetime
    period_label: date
    adjusted_close: float


def month_start(value: date) -> date:
    return value.replace(day=1)


def next_month(value: date) -> date:
    return date(value.year + (value.month == 12), 1 if value.month == 12 else value.month + 1, 1)


def read_retrieval_date(metadata_path: Path) -> date:
    payload = json.loads(metadata_path.read_text(encoding="utf-8"))
    try:
        return datetime.fromisoformat(payload["retrieved_utc"]).astimezone(UTC).date()
    except (KeyError, TypeError, ValueError) as error:
        raise DataGateError("retrieval_metadata.json needs a valid retrieved_utc timestamp") from error


def parse_yahoo_file(path: Path, ticker: str) -> list[RawObservation]:
    """Parse paired Yahoo timestamps and adjusted-close values without relabeling dates."""
    try:
        result = json.loads(path.read_text(encoding="utf-8"))["chart"]["result"][0]
        timestamps = result["timestamp"]
        adjusted = result["indicators"]["adjclose"][0]["adjclose"]
    except (KeyError, IndexError, TypeError, json.JSONDecodeError) as error:
        raise DataGateError(f"{path.name} has an unexpected Yahoo chart structure") from error
    if len(timestamps) != len(adjusted):
        raise DataGateError(f"{path.name} timestamps and adjusted closes have different lengths")

    observations: list[RawObservation] = []
    for timestamp, value in zip(timestamps, adjusted):
        if value is None:
            continue
        try:
            timestamp_utc = datetime.fromtimestamp(timestamp, UTC)
            numeric_value = float(value)
        except (TypeError, ValueError, OSError) as error:
            raise DataGateError(f"{path.name} has an invalid timestamp or adjusted close") from error
        if not math.isfinite(numeric_value) or numeric_value <= 0:
            raise DataGateError(f"{path.name} has a nonpositive or nonfinite adjusted close")
        observations.append(
            RawObservation(ticker, timestamp_utc, month_start(timestamp_utc.date()), numeric_value)
        )
    if not observations:
        raise DataGateError(f"{path.name} has no usable adjusted-close observations")
    return observations


def completed_monthly_observations(
    observations: Iterable[RawObservation], retrieval_date: date
) -> dict[date, RawObservation]:
    """Keep one unambiguous observation for each completed source-label month.

    Current-month labels are intentionally excluded. They are not assumed to be
    completed periods, even if Yahoo supplies a numeric adjusted close.
    """
    cutoff = month_start(retrieval_date)
    grouped: dict[date, list[RawObservation]] = defaultdict(list)
    for observation in observations:
        grouped[observation.period_label].append(observation)

    completed: dict[date, RawObservation] = {}
    for label, rows in grouped.items():
        if label >= cutoff:
            continue
        if len(rows) != 1:
            raise DataGateError(f"duplicate completed-period label {label.isoformat()}")
        completed[label] = rows[0]
    if not completed:
        raise DataGateError("no completed monthly observations remain after the cutoff")
    labels = sorted(completed)
    for left, right in zip(labels, labels[1:]):
        if next_month(left) != right:
            raise DataGateError(f"missing or misaligned monthly label between {left} and {right}")
    return completed


def validate_and_align(raw_dir: Path, metadata_path: Path) -> tuple[dict[str, dict[date, RawObservation]], date]:
    retrieval_date = read_retrieval_date(metadata_path)
    by_ticker = {
        ticker: completed_monthly_observations(
            parse_yahoo_file(raw_dir / f"{ticker}_yahoo_monthly.json", ticker), retrieval_date
        )
        for ticker in TICKERS
    }
    expected_labels = set(next(iter(by_ticker.values())))
    for ticker, observations in by_ticker.items():
        if set(observations) != expected_labels:
            raise DataGateError(f"{ticker} does not share the same completed monthly labels")
    return by_ticker, retrieval_date


def write_approved_dataset(
    by_ticker: dict[str, dict[date, RawObservation]], output_dir: Path, raw_dir: Path
) -> tuple[Path, Path]:
    """Write new approved data and a raw-to-output lineage table; never touch prices.csv."""
    output_dir.mkdir(parents=True, exist_ok=True)
    prices_path = output_dir / "approved_monthly_prices.csv"
    lineage_path = output_dir / "approved_monthly_lineage.csv"
    labels = sorted(next(iter(by_ticker.values())))

    with prices_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["PeriodLabel", *TICKERS])
        for label in labels:
            writer.writerow([label.isoformat(), *(f"{by_ticker[ticker][label].adjusted_close:.6f}" for ticker in TICKERS)])

    with lineage_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=["Ticker", "PeriodLabel", "SourceTimestampUtc", "AdjustedClose", "RawFile", "RawSha256"],
        )
        writer.writeheader()
        for ticker in TICKERS:
            raw_file = raw_dir / f"{ticker}_yahoo_monthly.json"
            raw_hash = hashlib.sha256(raw_file.read_bytes()).hexdigest()
            for label in labels:
                row = by_ticker[ticker][label]
                writer.writerow(
                    {
                        "Ticker": ticker,
                        "PeriodLabel": label.isoformat(),
                        "SourceTimestampUtc": row.timestamp_utc.isoformat(),
                        "AdjustedClose": f"{row.adjusted_close:.6f}",
                        "RawFile": f"data/raw/{raw_file.name}",
                        "RawSha256": raw_hash,
                    }
                )
    return prices_path, lineage_path


def build(raw_dir: Path, metadata_path: Path, output_dir: Path) -> tuple[Path, Path, int, date, date]:
    by_ticker, _ = validate_and_align(raw_dir, metadata_path)
    prices_path, lineage_path = write_approved_dataset(by_ticker, output_dir, raw_dir)
    labels = sorted(next(iter(by_ticker.values())))
    return prices_path, lineage_path, len(labels), labels[0], labels[-1]


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    parser = argparse.ArgumentParser(description="Build the approved Project 2 monthly price dataset.")
    parser.add_argument("--raw-dir", type=Path, default=root / "data" / "raw")
    parser.add_argument("--metadata", type=Path, default=root / "data" / "raw" / "retrieval_metadata.json")
    parser.add_argument("--output-dir", type=Path, default=root / "data" / "processed")
    args = parser.parse_args()
    prices_path, lineage_path, count, first, last = build(args.raw_dir, args.metadata, args.output_dir)
    print(f"APPROVED: {count} completed source-label months, {count - 1} monthly returns")
    print(f"Coverage: {first.isoformat()} through {last.isoformat()}")
    print(f"Prices: {prices_path}")
    print(f"Lineage: {lineage_path}")


if __name__ == "__main__":
    main()
