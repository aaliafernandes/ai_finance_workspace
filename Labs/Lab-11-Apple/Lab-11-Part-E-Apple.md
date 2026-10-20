# Lab 11 — Part E: Find the Driver and Reflection

**Company:** Apple Inc. (AAPL)  
**Purpose:** Educational finance coursework only; not personalized investment advice. Amounts are USD millions unless stated otherwise.

## Sensitivity comparison

| Driver | Operating-profit span | FCFF-proxy span | Value-per-share span |
|---|---:|---:|---|
| Total revenue growth | 31,416.0 | 23,321.0 | Unavailable |
| Operating margin | 20,442.0 | 15,174.7 | Unavailable |

**Over these ranges, total revenue growth is the larger driver** for both
final-year operating profit and FCFF proxy. Value per share cannot be ranked
because it is unavailable in every run: the FCFF definition remains incomplete
and WACC remains unresolved.

This ranking is limited to the selected ranges. A larger span can reflect a
wider or differently shaped input range rather than an inherently more
important Apple driver. The tested revenue-growth and operating-margin paths
each use stated judgment ranges; they are not probabilities.

## Causal explanation using the actual results

In the higher revenue-growth case, Apple’s final-year revenue rose from
$511,051.1 million in the base case to $562,022.1 million. Because operating
margin stayed fixed at 32%, final-year operating profit rose by $16,310.7
million, from $163,536.4 million to $179,847.1 million. The fixed historical
cash-flow conversion factor then increased FCFF proxy by $12,107.9 million,
from $121,397.9 million to $133,505.9 million.

## Sensitivity — learn on your own

**1. What is one-at-a-time sensitivity?**  
One-at-a-time sensitivity changes one independent assumption to a lower or
higher case while holding all other independent assumptions at their base
values. The linked forecast calculations then recalculate. This isolates the
effect of that selected assumption over the tested range.

**2. How does the chosen input range affect the ranking?**  
The span is the highest output minus the lowest output across the lower, base,
and higher cases. A wider range usually produces a wider output span even if
the underlying business relationship is unchanged. Therefore, the ranking says
which driver produced the larger change **over these tested ranges**, not which
driver is always most important.

**Why a sensitivity table is not a forecast probability**  
A sensitivity table shows conditional results: what the model produces if a
chosen assumption changes. It does not estimate the chance that any lower,
base, or higher case will occur, and it does not assign probabilities to those
cases. Forecast probability would require separate evidence, a probability
method, and assumptions about uncertainty.

## Reflection

Over the tested ranges, total revenue growth mattered most for Apple’s
final-year operating profit and FCFF proxy. The result that surprised me was
that revenue growth produced the larger span even though operating margin is
also important; this result reflects both the compounding five-year revenue
paths and the particular ranges selected. The result does not change my
valuation conclusion because value per share remains unavailable. My research
priority remains resolving fully defined FCFF and WACC before relying on a
per-share valuation.

## Partner exchange 3 — discussion script and record

**My explanation to my partner:**

> Over my tested Apple ranges, revenue growth was the larger driver. In the
> higher revenue-growth case, final-year revenue increased from $511,051.1M to
> $562,022.1M. With operating margin fixed at 32%, operating profit increased
> by $16,310.7M and FCFF proxy increased by $12,107.9M. This does not prove
> revenue growth is always Apple’s most important driver; the result could
> reflect my selected ranges.

**Question for my partner:**

> Could my ranking of revenue growth over operating margin mainly reflect the
> ranges I selected rather than an inherent difference in importance? Please
> summarize my conclusion in your own words.

**My answer to the range question:**

> Yes. The larger revenue-growth span may partly result from five years of
> compounded growth changes and the chosen lower/base/higher paths. The proper
> conclusion is only that revenue growth was larger **over these ranges**.

**Comparison with Abercrombie & Fitch:**

Apple and Abercrombie & Fitch can both be affected by sales growth, but their
drivers can differ. Apple’s result is tied to its forecast revenue path and a
fixed operating-margin assumption; Services mix and operating margin remain
important limitations. Abercrombie & Fitch’s revenue growth can depend more on
apparel demand, pricing, promotions, inventory, and store performance. The two
companies should not be ranked against each other using raw dollar changes.

**Partner’s summary/response:** My partner agreed that, over my stated Apple
ranges, revenue growth produced the larger operating-profit and FCFF-proxy
spans. My partner also agreed that this ranking could partly reflect the chosen
five-year revenue-growth paths and ranges, rather than proving revenue growth
is always Apple’s most important driver. No correction was identified.

## Source and limitation

Output spans are from `apple_proforma_sensitivity.py`, run in the terminal.
Historical Apple values are documented from Apple’s FY2025 Form 10-K in
`Lab-05-DCF-Apple.md`. FCFF proxy equals operating cash flow less capital
spending before the unresolved cash-interest-paid add-back; it is not fully
defined FCFF.

## Lab 11 progress count

| Item | Status |
|---|---|
| D — question and Partner Exchange 1 | Complete |
| R — inputs, ranges, locked prediction, and pre-run confirmation | Complete |
| I — sensitivity analysis and restored base | Complete |
| V — own-result checks, evidence, and partner check | Complete |
| E — driver comparison, reflection, and partner summary | Complete |

**Completed: 5 of 5 Lab 11 sections.**
