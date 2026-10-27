# Lab 16 Checkout — Provenance Gate

## Evidence

Command run from this folder:

```powershell
python asof.py
python verify_known_answer.py
```

`asof.py` produces the expected funnel: row 11 is quarantined, row 7 is the
duplicate, rows 3/8/10 are published after 31 March 2026, and row 2 is
replaced by the later, decision-date-available revision in row 4. The final
as-of panel is rows 1, 4, 5, 6, 9, and 12.

| Ticker | As-of signal | Naive signal |
| --- | ---: | ---: |
| AAA | +1.98% (February) | +5.83% (March) |
| BBB | -1.02% (February) | -5.15% (March) |
| CCC | +0.91% (February) | +1.82% (February, revised) |

With the decision date moved to 15 April 2026, the as-of signals equal the
naive signals ticker-for-ticker. The verification script asserts both results.

## Rule 4 in plain language

`keep_latest_vintage` first groups rows by `(ticker, month)`. In each group it
uses `max` on the publication date, so one later revision replaces an earlier
vintage of the same month. In the as-of workflow, this happens only **after**
late publications are removed. Therefore, AAA's February row 4 (published
25 March) replaces row 2 (published 10 March), while AAA's March row 3 cannot
enter a 31 March decision because it was published on 10 April.

## Learning reflection

**What is look-ahead bias?** It is using information in an analysis that was
not actually available at the time a decision would have been made. It makes a
historical strategy appear more informed or successful than it could have
been in real time.

**How do event time, publication time, and revisions create it?** The measured
month is the event time; the published-on date is when the value becomes
available. A later release can report a new month, and a revision can change a
previous month. A point-in-time filter must use the publication date, retain
only information available at the decision date, and then choose the newest
available vintage for each ticker/month.

**AAA example.** On 31 March, the latest knowable AAA month was February and
its latest available value was 103.0, so the signal was `(103 / 101 - 1)`, or
`+1.98%`. The apparently better `+5.83%` uses March's 109.0 value, which was
not published until 10 April. It therefore could not have informed a trade on
31 March.

## Source

Lab 16 — Provenance Gate course prompt, retrieved 2026-10-27.
