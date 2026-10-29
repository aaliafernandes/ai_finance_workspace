# Lab 17 — The Data, Real and Live

## Run

From the workspace root in PowerShell:

```powershell
& .\.tools\python-3.13.15\python.exe -m streamlit run .\Labs\Lab-17-Real-and-Live\asof_app.py
```

The sidebar begins with BAA, FEDFUNDS, DGS10, and MORTGAGE30US. Add a custom
FRED ID (for example, `PAYEMS`) in the text box. The generated **Rate chart**
component has a **Choose the series to graph** dropdown directly above it. The
comparison table still includes every selected series. The app makes one cached
FRED download and one cached ALFRED vintage download per selected series; it
needs no API key or account.

## Known-answer check

Set **As known on** to 5 October 2026. The app should report:

| Series | Last date known | Value |
| --- | --- | ---: |
| BAA | September 2026 | 6.47 |
| FEDFUNDS | September 2026 | 3.75 |
| DGS10 | 2 October 2026 | 5.28 |
| MORTGAGE30US | 1 October 2026 | 7.28 |

For the revision probe, add `PAYEMS` and set **As known on** to 15 January
2025. The expected point-in-time observation is December 2024 at 159,536.
Today's value for that measurement should be lower, with revised values above
zero.

## Method and limitations

- A date is an observation/measurement date, not necessarily a publication
  date. ALFRED's vintage selection represents the values available on the
  chosen information date.
- The app excludes FRED's `.` missing values, and counts revisions only when
  both downloads contain a numeric observation on the same date.
- Charts and comparisons are descriptive educational outputs, not forecasts or
  personalized investment advice.

See [Week-10-Prework.md](Week-10-Prework.md) and [DATA-CARD.md](DATA-CARD.md)
for the prework notes, sources, frequency, units, and revision notes.
