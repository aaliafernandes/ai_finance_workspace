# Lab 11 — Part V: Result Check

**Company:** Apple Inc. (AAPL)  
**Purpose:** Educational finance coursework only; not personalized investment advice. Amounts are USD millions unless stated otherwise.

## My model checks

| Check | Evidence | Result |
|---|---|---|
| Base before and after analysis | Initial base final-year operating profit = $163,536.4; FCFF proxy = $121,397.9. Restored-base final-year operating profit = $163,536.4; FCFF proxy = $121,397.9. | Pass, within $0.1 million printed-rounding tolerance. |
| Revenue-growth higher run changes only the selected input | Base revenue growth = 6%, 5%, 4%, 3%, 3%; higher revenue growth = 8%, 7%, 6%, 5%, 5%. Operating margin remains 32%, 32%, 32%, 32%, 32%; all other inputs are fresh copies of base. | Pass. |
| Linked quantities recalculate | Higher revenue growth produces final-year revenue of $562,022.1, operating profit of $179,847.1, and FCFF proxy of $133,505.9. | Pass. |
| Calculation checks | The script reports PASS in every year for the revenue-to-operating-profit link and the operating-profit-to-FCFF-proxy link in every usable lower, base, and higher run. | Pass. |
| Accounting checks | This is an operating/FCFF-proxy forecast rather than a full three-statement balance-sheet model, so assets = liabilities + equity is not applicable. The two linked calculation checks above are visible instead. | Limitation recorded. |
| Signed change from base | $179,847.1 − $163,536.4 = +$16,310.7 operating profit; $133,505.9 − $121,397.9 = +$12,107.9 FCFF proxy, using unrounded model values. | Pass. |

## Selected changed result and trace

**Selected run:** Revenue-growth higher case; operating margin held at the 32% base path.

| Item | Base | Higher revenue-growth case | Change from base |
|---|---:|---:|---:|
| Final-year revenue | 511,051.1 | 562,022.1 | +50,971.0 |
| Final-year operating profit | 163,536.4 | 179,847.1 | +16,310.7 |
| Final-year FCFF proxy | 121,397.9 | 133,505.9 | +12,107.9 |
| Value per share | Unavailable | Unavailable | Unavailable |

Trace: Higher revenue growth increases forecast revenue. With operating margin
fixed at 32%, higher revenue increases operating profit. The model then applies
the fixed historical cash-flow conversion factor to operating profit, increasing
the FCFF proxy.

## Locked Changed-Input Record — actual result

The prediction was directionally correct: the higher revenue-growth path
increased final-year operating profit by $16,310.7 million and FCFF proxy by
$12,107.9 million. No prediction error occurred in direction; no rough numeric
amount was predicted before the run, so there is no predicted numeric amount to
compare with the actual result.

The result does **not** change the valuation conclusion because value per share
remains unavailable. The research priority remains to resolve Apple’s FCFF
definition (including cash interest paid) and estimate WACC from dated inputs
before using a per-share valuation.

## Partner exchange 2 — my evidence and question

I will show my partner the base and higher revenue-growth result above. My
partner should recompute the two changes, verify that operating margin remained
at 32% in every forecast year, and ask me to trace revenue through operating
profit to FCFF proxy.

**Question to ask my partner:**

> Using the base and higher revenue-growth results, can you recompute the
> $16,310.7 million change in final-year operating profit and confirm that I
> held operating margin at 32% in every year? What part of my revenue →
> operating profit → FCFF-proxy link would you question or correct?

**Partner’s response and any correction:** My partner recomputed the displayed
changes, agreed with the results, and confirmed that operating margin remained
at 32% in each forecast year. No correction was identified.

## What I checked on my partner’s model

I compared my partner’s stated base and changed case, recomputed the reported
difference, and checked that their other independent assumptions remained at
base. I also asked whether revenue growth was the only important driver. We
agreed it was important, but that margin, costs, and other operating assumptions
can also affect the result. No correction was identified.

## Source and model limitation

The run results come from `apple_proforma_sensitivity.py`. Historical Apple
values are sourced from Apple’s FY2025 Form 10-K, filed October 31, 2025,
accessed September 24, 2026, as documented in `Lab-05-DCF-Apple.md`.
“FCFF proxy” equals FY2025 operating cash flow less capital spending before the
unresolved cash-interest-paid add-back; it is not a fully defined FCFF measure.
