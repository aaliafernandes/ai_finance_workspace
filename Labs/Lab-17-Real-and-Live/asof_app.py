"""Lab 17 — compare today's FRED data with an ALFRED vintage.

Run from the workspace root:
  & .\\.tools\\python-3.13.15\\python.exe -m streamlit run .\\Labs\\Lab-17-Real-and-Live\\asof_app.py

Educational demonstration only; it is not investment advice or a forecast.
"""

from __future__ import annotations

import csv
from datetime import date
from io import StringIO
from urllib.error import HTTPError, URLError
from urllib.parse import quote
from urllib.request import urlopen

import pandas as pd
import streamlit as st


SERIES = {
    "BAA": "Moody's Baa corporate bond yield",
    "FEDFUNDS": "Effective federal funds rate",
    "DGS10": "10-year Treasury yield",
    "MORTGAGE30US": "30-year fixed mortgage rate",
}
FRED_CSV = "https://fred.stlouisfed.org/graph/fredgraph.csv?id={series_id}"
ALFRED_CSV = "https://alfred.stlouisfed.org/graph/alfredgraph.csv?id={series_id}&vintage_date={vintage_date}"


def clean_series_id(series_id: str) -> str:
    """Return the FRED identifier in the conventional uppercase form."""
    return series_id.strip().upper()


def parse_fred_csv(text: str, series_id: str) -> list[tuple[date, float]]:
    """Parse a FRED/ALFRED graph CSV, dropping FRED's '.' missing values."""
    rows = csv.DictReader(StringIO(text))
    if not rows.fieldnames or "observation_date" not in rows.fieldnames:
        raise ValueError("FRED returned a CSV without an observation-date column.")
    # FRED uses the ID as the value column (for example, BAA). ALFRED appends
    # the selected vintage date (for example, BAA_20261005), even for one ID.
    value_columns = [column for column in rows.fieldnames if column != "observation_date"]
    if len(value_columns) != 1:
        raise ValueError("FRED returned an unexpected number of value columns.")
    value_column = value_columns[0]
    observations = []
    for row in rows:
        observation_date = row.get("observation_date")
        value = row.get(value_column)
        if not observation_date or value in (None, "", "."):
            continue
        try:
            observations.append((date.fromisoformat(observation_date), float(value)))
        except ValueError as error:
            raise ValueError("FRED returned a CSV with an invalid date or value.") from error
    if not observations:
        raise ValueError("FRED returned no numeric observations for this series.")
    return observations


def download_csv(url: str) -> str:
    """Fetch a public CSV with a clear error for an unavailable or invalid ID."""
    try:
        with urlopen(url, timeout=30) as response:  # nosec B310: fixed FRED/ALFRED URLs
            return response.read().decode("utf-8-sig")
    except HTTPError as error:
        raise ValueError(f"FRED/ALFRED returned HTTP {error.code}.") from error
    except URLError as error:
        raise ValueError("Could not reach FRED/ALFRED. Check your internet connection and retry.") from error


@st.cache_data(show_spinner=False, ttl=3600)
def download_today(series_id: str) -> list[tuple[date, float]]:
    """Download the current, revised FRED series (one request per series)."""
    series_id = clean_series_id(series_id)
    return parse_fred_csv(download_csv(FRED_CSV.format(series_id=quote(series_id))), series_id)


@st.cache_data(show_spinner=False, ttl=3600)
def download_vintage(series_id: str, vintage_date: str) -> list[tuple[date, float]]:
    """Download the ALFRED values that were available on ``vintage_date``."""
    series_id = clean_series_id(series_id)
    url = ALFRED_CSV.format(series_id=quote(series_id), vintage_date=quote(vintage_date))
    return parse_fred_csv(download_csv(url), series_id)


def observations_through(observations: list[tuple[date, float]], end_date: date) -> list[tuple[date, float]]:
    """Keep measurements dated on or before the stated information date."""
    return [(measured, value) for measured, value in observations if measured <= end_date]


def format_measurement_date(measured: date) -> str:
    """Use a readable date while retaining daily/weekly/monthly precision."""
    return measured.strftime("%d %B %Y")


def summarize_series(
    series_id: str,
    today_values: list[tuple[date, float]],
    vintage_values: list[tuple[date, float]],
    as_known_on: date,
) -> dict[str, object]:
    """Build the Lab 17 point-in-time comparison for one series."""
    vintage_panel = observations_through(vintage_values, as_known_on)
    if not vintage_panel:
        raise ValueError("No numeric observations were available by the selected as-known-on date.")

    old_date, old_value = vintage_panel[-1]
    today_panel = observations_through(today_values, date.today())
    if not today_panel:
        raise ValueError("Today's FRED download has no numeric observations.")
    current_date, current_value = today_panel[-1]
    today_by_date = dict(today_panel)
    vintage_by_date = dict(vintage_panel)
    common_dates = set(today_by_date) & set(vintage_by_date)
    revised = sum(abs(today_by_date[measured] - vintage_by_date[measured]) > 1e-12 for measured in common_dates)
    later_values = sum(measured > old_date for measured, _ in today_panel)

    return {
        "series_id": series_id,
        "vintage_date": old_date,
        "vintage_value": old_value,
        "current_date": current_date,
        "current_value": current_value,
        "later_values": later_values,
        "revised_values": revised,
    }


def linked_series_id(series_id: str) -> str:
    """Return a Markdown link to the public FRED series page."""
    return f"[{series_id}](https://fred.stlouisfed.org/series/{quote(series_id)})"


def comparison_markdown(rows: list[dict[str, object]], as_known_on: date) -> str:
    """Create the required linked comparison table without extra packages."""
    header = (
        f"| Series | Last known on {as_known_on:%d %b %Y} | Latest today | "
        "Today's values after then | Revised values on the same dates |"
    )
    divider = "| --- | --- | --- | ---: | ---: |"
    body = []
    for row in rows:
        body.append(
            "| "
            f"{linked_series_id(str(row['series_id']))} | "
            f"{format_measurement_date(row['vintage_date'])}: {row['vintage_value']:,.3f} | "
            f"{format_measurement_date(row['current_date'])}: {row['current_value']:,.3f} | "
            f"{row['later_values']} | {row['revised_values']} |"
        )
    return "\n".join([header, divider, *body])


st.set_page_config(page_title="Interest-Rate Vintage Viewer", layout="wide")
st.title("Interest-Rate Vintage Viewer")
st.caption(
    "Data from FRED and ALFRED, Federal Reserve Bank of St. Louis, downloaded "
    f"{date.today():%d %B %Y}; built with AI help, a learning demonstration, not investment advice."
)

with st.sidebar:
    st.header("Data controls")
    selected = st.multiselect(
        "Series",
        options=list(SERIES),
        default=list(SERIES),
        format_func=lambda series_id: f"{series_id} — {SERIES[series_id]}",
    )
    additional_id = clean_series_id(st.text_input("Add another FRED series ID", placeholder="Example: PAYEMS"))
    if additional_id and additional_id not in selected:
        selected.append(additional_id)
    start_date = st.date_input("Start date", value=date(2020, 1, 1))
    as_known_on = st.date_input("As known on", value=date.today(), max_value=date.today())

if not selected:
    st.info("Select at least one FRED series ID.")
    st.stop()

st.subheader("Rate charts")
chart_choice = st.selectbox(
    "Generated chart component",
    options=["All selected series", *selected],
    format_func=lambda choice: (
        "All selected series" if choice == "All selected series"
        else f"{choice} — {SERIES.get(choice, 'Custom FRED series')}"
    ),
    help="The default shows one generated chart for every selected series. Choose one ID to focus on its chart.",
)

comparison_rows = []
for series_id in selected:
    label = SERIES.get(series_id, "Custom FRED series")
    show_chart = chart_choice == "All selected series" or chart_choice == series_id
    if show_chart:
        st.subheader(f"{series_id} — {label}")
    try:
        current = download_today(series_id)
        vintage = download_vintage(series_id, as_known_on.isoformat())
        if show_chart:
            chart_values = [(measured, value) for measured, value in current if measured >= start_date]
            if not chart_values:
                st.warning("Today's download has no numeric values on or after the selected start date.")
            else:
                chart_frame = pd.DataFrame(chart_values, columns=["Date", series_id]).set_index("Date")
                st.line_chart(chart_frame, width="stretch")

        summary = summarize_series(series_id, current, vintage, as_known_on)
        if show_chart:
            st.caption(
                f"Last measurement known on {as_known_on:%d %B %Y}: "
                f"{format_measurement_date(summary['vintage_date'])} — {summary['vintage_value']:,.3f}"
            )
        comparison_rows.append(summary)
    except ValueError as error:
        st.error(f"{series_id}: {error}")

st.subheader("Vintage comparison")
if comparison_rows:
    st.markdown(comparison_markdown(comparison_rows, as_known_on))
else:
    st.warning("No selected series returned usable data.")

st.divider()
st.caption(
    "Method: FRED supplies today's revised history; ALFRED supplies the historical vintage. "
    "A revision is counted when a numeric value available by the selected date differs from today's value "
    "on the same measurement date. Missing values (.) are excluded."
)
