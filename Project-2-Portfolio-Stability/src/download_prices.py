"""Download reproducible monthly Yahoo Finance adjusted-close data for Project 2.

The source is Yahoo Finance's public chart endpoint. The script writes raw API
responses separately from the processed, aligned CSV used by the Streamlit app.
"""

import csv
import json
from datetime import UTC, datetime
from pathlib import Path
from urllib.request import urlopen


TICKERS = ("BIL", "IEF", "LQD", "VT")
ROOT = Path(__file__).resolve().parents[1]
RAW_DIR = ROOT / "data" / "raw"
PROCESSED_FILE = ROOT / "data" / "processed" / "prices.csv"


def fetch_monthly_history(ticker):
    """Fetch Yahoo monthly adjusted-close observations for one ticker."""
    url = (
        f"https://query1.finance.yahoo.com/v8/finance/chart/{ticker}"
        "?period1=1633046400&period2=1792713600&interval=1mo"
        "&events=history&includeAdjustedClose=true"
    )
    with urlopen(url, timeout=30) as response:
        payload = json.load(response)
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    (RAW_DIR / f"{ticker}_yahoo_monthly.json").write_text(json.dumps(payload, indent=2), encoding="utf-8")

    result = payload["chart"]["result"][0]
    adjusted = result["indicators"]["adjclose"][0]["adjclose"]
    observations = {}
    for timestamp, value in zip(result["timestamp"], adjusted):
        if value is not None:
            month = datetime.fromtimestamp(timestamp, UTC).date().replace(day=1).isoformat()
            observations[month] = value
    return observations


def main():
    """Create an aligned 61-observation CSV from the four fund histories."""
    histories = {ticker: fetch_monthly_history(ticker) for ticker in TICKERS}
    shared_dates = sorted(set.intersection(*(set(history) for history in histories.values())))
    shared_dates = shared_dates[-61:]
    if len(shared_dates) < 61:
        raise ValueError("Yahoo Finance returned fewer than 61 aligned monthly observations")

    PROCESSED_FILE.parent.mkdir(parents=True, exist_ok=True)
    with PROCESSED_FILE.open("w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Date", *TICKERS])
        for date in shared_dates:
            writer.writerow([date, *(f"{histories[ticker][date]:.6f}" for ticker in TICKERS)])

    metadata = {
        "source": "Yahoo Finance public chart endpoint",
        "retrieved_utc": datetime.now(UTC).isoformat(),
        "tickers": TICKERS,
        "observations": len(shared_dates),
        "processed_file": str(PROCESSED_FILE.relative_to(ROOT)),
    }
    (RAW_DIR / "retrieval_metadata.json").write_text(json.dumps(metadata, indent=2), encoding="utf-8")
    print(f"Wrote {len(shared_dates)} monthly observations to {PROCESSED_FILE}")


if __name__ == "__main__":
    main()
