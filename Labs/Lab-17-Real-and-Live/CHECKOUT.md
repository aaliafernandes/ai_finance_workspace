# Lab 17 checkout — Point-in-Time Audit

**Status:** App, known-answer evidence, PAYEMS probe, prework series, and data
card are complete. The partner review must be completed in person and recorded
in [PARTNER-REVIEW.md](PARTNER-REVIEW.md); it is deliberately not fabricated
here.

## Question

**Was each number in my selected series knowable on the day Project 2 would
have traded on it, and may Project 2 use it?**

The point-in-time rule is to use the ALFRED vintage available on or before the
decision date. Current FRED values are used only for comparison, never as a
substitute for a historical vintage.

## App evidence

- App: [asof_app.py](asof_app.py)
- Run command:

  ```powershell
  & .\.tools\python-3.13.15\python.exe -m streamlit run .\Labs\Lab-17-Real-and-Live\asof_app.py
  ```

- Uses one cached current-vintage FRED download and one cached ALFRED-vintage
  download for each selected ID. It excludes `.` missing values.
- The sidebar contains the required multi-select, typed ID field, start date,
  and as-known-on date. The page's **Choose the series to graph** component
  switches the displayed generated chart while the comparison table retains all
  selected IDs.
- An invalid ID was tested on 29 October 2026: it produced a series-specific
  error while BAA, FEDFUNDS, DGS10, and MORTGAGE30US continued to populate the
  comparison table.

## Known-answer evidence

On 29 October 2026, with **As known on = 5 October 2026**, the app returned:

| Series | Last measurement known then | Value known then |
| --- | --- | ---: |
| BAA | 1 September 2026 | 6.47 |
| FEDFUNDS | 1 September 2026 | 3.75 |
| DGS10 | 2 October 2026 | 5.28 |
| MORTGAGE30US | 1 October 2026 | 7.28 |

## PAYEMS revision probe

With `PAYEMS` added and **As known on = 15 January 2025**, the app returned
December 2024 at **159,536**. The current FRED value was **159,044**, lower
than the historical vintage, and the app counted **381** revised same-date
observations. This demonstrates that the app is comparing ALFRED's vintage to
today's FRED data rather than downloading today's data twice.

## My Project 2 series and call

The selected series is `BAMLC0A0CM`, the ICE BofA U.S. Corporate
Option-Adjusted Spread. It is a daily investment-grade credit-spread measure,
not a fund price, and is relevant to the LQD role in Project 2. Its complete
source, measure, units, timing, revision note, download date, and three
hand-checked values are in [DATA-CARD.md](DATA-CARD.md).

On the last day of the prior month (**30 September 2026**), the app showed
`BAMLC0A0CM` at **0.84**; today's 28 October 2026 observation was **0.86**.
There were 20 newer observations and 0 same-date revisions in that comparison.

**Call: Admit, with an as-of rule.** Project 2 may use the series only after a
value is available on or before the decision date, as established by the
ALFRED vintage. The current FRED history must not be substituted into a
historical backtest. I would quarantine the series if its release timing became
unclear, if the needed vintage were unavailable, or if a future ALFRED check
showed material revisions that changed the decision.

## Fresh-eyes code explanation preparation

`download_vintage(series_id, vintage_date)` performs the point-in-time step:

1. It standardizes the typed ID with `clean_series_id`.
2. It builds ALFRED's CSV URL with `vintage_date=YYYY-MM-DD`.
3. It calls the cached `download_csv` helper to retrieve that public CSV.
4. It passes the response to `parse_fred_csv`, which handles ALFRED's dated
   value-column name and removes `.` missing observations.
5. `summarize_series` then limits the result to measurement dates on or before
   the selected as-known-on date before identifying the latest known value.

This ordering prevents later measurements and later revisions from entering
the historical decision panel.

## Remaining live-class task

Use [PARTNER-REVIEW.md](PARTNER-REVIEW.md) to record the actual partner attack,
the response, and the partner's question about the code. This must be based on
the real conversation, not generated after the fact.
