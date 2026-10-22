"""Create a standalone Lab 15 practice prices.csv from Yahoo Finance data."""

import csv
import json
from datetime import UTC, datetime
from pathlib import Path
from time import sleep
from urllib.error import HTTPError
from urllib.request import Request, urlopen


TICKERS = ("BIL", "IEF", "LQD", "VT")
ROOT = Path(__file__).resolve().parents[1]
RAW_DIR = ROOT / "data" / "raw"
PROCESSED_FILE = ROOT / "data" / "processed" / "prices.csv"


def fetch_monthly_history(ticker):
    """Fetch public monthly adjusted-close observations for one fund."""
    url = (
        f"https://query1.finance.yahoo.com/v8/finance/chart/{ticker}"
        "?period1=1633046400&period2=1792713600&interval=1mo"
        "&events=history&includeAdjustedClose=true"
    )
    request = Request(url, headers={"User-Agent": "Mozilla/5.0 (Lab 15 coursework)"})
    for attempt in range(3):
        try:
            with urlopen(request, timeout=30) as response:
                payload = json.load(response)
            break
        except HTTPError as error:
            if error.code != 429 or attempt == 2:
                raise
            sleep(3 * (attempt + 1))

    RAW_DIR.mkdir(parents=True, exist_ok=True)
    (RAW_DIR / f"{ticker}_yahoo_monthly.json").write_text(json.dumps(payload, indent=2), encoding="utf-8")
    result = payload["chart"]["result"][0]
    adjusted = result["indicators"]["adjclose"][0]["adjclose"]
    return {
        datetime.fromtimestamp(timestamp, UTC).date().replace(day=1).isoformat(): value
        for timestamp, value in zip(result["timestamp"], adjusted)
        if value is not None
    }


def main():
    """Write 61 aligned monthly prices, yielding 60 monthly returns."""
    histories = {ticker: fetch_monthly_history(ticker) for ticker in TICKERS}
    dates = sorted(set.intersection(*(set(history) for history in histories.values())))[-61:]
    if len(dates) < 61:
        raise ValueError("Yahoo Finance returned fewer than 61 aligned monthly observations")
    PROCESSED_FILE.parent.mkdir(parents=True, exist_ok=True)
    with PROCESSED_FILE.open("w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Date", *TICKERS])
        for date in dates:
            writer.writerow([date, *(f"{histories[ticker][date]:.6f}" for ticker in TICKERS)])
    metadata = {
        "source": "Yahoo Finance public chart endpoint",
        "retrieved_utc": datetime.now(UTC).isoformat(),
        "tickers": TICKERS,
        "observations": len(dates),
    }
    (RAW_DIR / "retrieval_metadata.json").write_text(json.dumps(metadata, indent=2), encoding="utf-8")
    print(f"Wrote {len(dates)} monthly observations to {PROCESSED_FILE}")


if __name__ == "__main__":
    main()
