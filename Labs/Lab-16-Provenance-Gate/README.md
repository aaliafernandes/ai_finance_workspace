# Lab 16 — Provenance Gate

## Purpose

This lab separates **when a number measures activity** from **when the number
became public**. A decision dated 31 March 2026 may use only a row published
on or before that date. Later March data and later revisions are not
knowable on that decision date.

## Run

```powershell
cd Labs\Lab-16-Provenance-Gate
python asof.py
python verify_known_answer.py
```

## Method

`asof.py` uses only the Python standard library and applies the supplied rules
in this order:

1. Quarantine blank tickers.
2. Remove an exact duplicate, treating the source-row number as metadata.
3. Remove publications after 31 March 2026.
4. Within each ticker and measured month, retain the latest publication that
   was knowable by the decision date.

The as-of signal is the percent change from the prior measured month to the
latest month remaining after the filter. The naive comparison intentionally
ignores publication dates after the basic data-hygiene checks, illustrating
the look-ahead bias that a provenance gate prevents.

## Known-answer check

The expected as-of panel contains rows `1, 4, 5, 6, 9, 12`. The expected
as-of signals are AAA `+1.98%` to 2026-02, BBB `-1.02%` to 2026-02, and CCC
`+0.91%` to 2026-02.

`verify_known_answer.py` also checks the naive signals and proves that moving
the decision date to 2026-04-15 makes the as-of signals match the naive ones.
See `CHECKOUT.md` for the full evidence and plain-language explanation.

## Assumptions and limitations

- The table is fictional training data supplied in the Lab 16 prompt; no
  external market or company data are used.
- If two same-date revisions appeared, the script keeps the lower source-row
  number solely as a deterministic tie-breaker.
- A percent change is descriptive for this exercise, not investment advice or
  a forecast.

## Source

Lab 16 — Provenance Gate course prompt, retrieved 2026-10-27.
