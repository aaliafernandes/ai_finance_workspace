# Week 10 Prework — ALFRED and the Project 2 driver

**Completed:** 29 October 2026.

## ALFRED Help reading notes

I read the required ALFRED Help headings. ALFRED is a collection of historical
vintages: it preserves the values reported on past dates even when later
revisions replace them on current data pages. A release is the mechanism by
which a source first makes data available. ALFRED uses the source's release
date when available, then a data-provider date, and finally the date the series
first appeared in FRED. Analysts add new or revised observations as soon as
possible after release, usually within one business day. When possible, ALFRED
checks a vintage against the original source; where old source estimates are no
longer retained, it uses third-party data services.

For a decision date, the knowable information is the latest vintage released
on or before that date. A current FRED page can contain later observations and
revisions, which are visible only because I am looking after the decision date.
The Lab 17 app uses ALFRED for the former and FRED for the latter.

## Chosen Project 2 driver

I selected `BAMLC0A0CM`, the ICE BofA US Corporate Index Option-Adjusted
Spread. It is a daily, percent, not-seasonally-adjusted corporate-credit spread
from ICE Data Indices. It is relevant to the investment-grade corporate-bond
role in the Project 2 universe (LQD) without using any fund's own price. The
series details and three checked values are recorded in [DATA-CARD.md](DATA-CARD.md).

## Sources

- [ALFRED Help](https://alfred.stlouisfed.org/help), retrieved 29 October 2026.
- [FRED BAMLC0A0CM](https://fred.stlouisfed.org/series/BAMLC0A0CM), retrieved
  29 October 2026.
