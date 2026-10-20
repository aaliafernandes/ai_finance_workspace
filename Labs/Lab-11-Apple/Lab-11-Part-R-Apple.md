# Lab 11 — Part R: Inputs and Comparison

**Company:** Apple Inc. (AAPL)  
**Purpose:** Educational finance coursework only; not personalized investment advice.

## Chosen independent operating drivers

The two inputs are **total revenue growth** and **operating margin**. They are
independent assumptions: revenue growth sets the sales forecast, while
operating margin sets the share of revenue remaining as operating profit. They
are not calculated statement totals.

| Driver | Lower case | Base case | Higher case | Units | Affected forecast years | Reason for the range |
|---|---|---|---|---|---|---|
| Total revenue growth | 4%, 3%, 2%, 1%, 1% | 6%, 5%, 4%, 3%, 3% | 8%, 7%, 6%, 5%, 5% | Percent of prior-year revenue, by year | Years 1–5 | The base path is the existing Apple DCF growth path and tapers over time. Apple reported 6% FY2025 total net-sales growth. The lower and higher paths are **labeled judgment ranges** of 2 percentage points below or above base in each year, reflecting potential changes in product demand and Services growth. |
| Operating margin | 30%, 30%, 30%, 30%, 30% | 32%, 32%, 32%, 32%, 32% | 34%, 34%, 34%, 34%, 34% | Percent of revenue, by year | Years 1–5 | The 32% base is a rounded FY2025 historical operating-margin reference. The lower and higher cases are **labeled judgment ranges** of 2 percentage points below or above base, reflecting potential changes in Services mix, product mix, pricing, and operating costs. |

The changes above are **percentage-point** changes, not percent changes. For
example, Year 1 revenue growth changes from 6% to 8%, which is an increase of
2 percentage points.

## Comparable outputs for every run

Use these outputs for the lower, base, and higher run of each driver:

| Output | Unit | Current status |
|---|---|---|
| Final-year operating profit | USD millions | To be produced by the Apple pro-forma. |
| Final-year free cash flow to the firm (FCFF) | USD millions | To be produced by the Apple pro-forma. |
| Value per diluted share | USD per share | Unavailable until the FCFF model is rebuilt on a consistent Apple scale. The existing DCF labels starting FCFF of $100 million as a training placeholder, so its per-share output is not a defensible Apple valuation. |

## Locked Changed-Input Record

**Saved before running any changed case**  
**Timestamp:** 2026-09-29 14:01:02 -04:00

| Item | Record |
|---|---|
| Input change | Total revenue growth: base path of 6%, 5%, 4%, 3%, 3% to the higher path of 8%, 7%, 6%, 5%, 5%. |
| Units | Percent of prior-year revenue; +2 percentage points in each forecast year. |
| Prediction | Final-year operating profit and FCFF should increase. Value per diluted share should increase once the FCFF valuation is valid. |
| Rough expected size | Positive but not estimated before running; the model will determine the amount. |
| Why | Higher sales should increase gross profit and operating profit when operating margin is held at the 32% base assumption. More operating profit should increase FCFF. |
| Held at base | Operating margin and every other independent assumption. Only revenue growth changes. |
| Actual result | Higher revenue growth produced final-year operating profit of $179,847.1 million (+$16,310.7 million from base) and FCFF proxy of $133,505.9 million (+$12,107.9 million from base). The predicted direction was correct. |

## Pre-run partner exchange — my part

**What I showed my partner:** I selected Apple total revenue growth and
operating margin as two independent operating drivers. Revenue-growth paths are
4%, 3%, 2%, 1%, 1% (lower); 6%, 5%, 4%, 3%, 3% (base); and 8%, 7%, 6%, 5%, 5%
(higher). Operating-margin paths are 30% (lower), 32% (base), and 34%
(higher) in each forecast year. All figures are percentages; each lower or
higher case changes the base by 2 percentage points.

**My prediction:** If I change only Apple’s total revenue-growth path from the
base case to the higher case, final-year operating profit and FCFF should
increase. Operating margin remains at the 32% base assumption, so the higher
sales forecast should flow through to higher profit and cash flow.

**My question to my partner:** Do the percentage units and the 2-percentage-
point shifts make sense? Do you confirm that this run changes only total
revenue growth and leaves operating margin and every other independent input at
base?

**Partner’s response:** Confirmed. My partner agreed that the inputs are
percentages, the stated changes are percentage-point changes, and each
sensitivity run will change only one independent input while all other
assumptions remain at base.

## Source and limitation

Source: Apple Inc. FY2025 Form 10-K, filed October 31, 2025, accessed
September 24, 2026. The filing reports FY2025 total net sales of $416,161
million, 6% year-over-year growth, and operating income of $133,050 million.
The rounded 32% operating-margin base is calculated as operating income divided
by total net sales. The lower and higher values are clearly labeled judgment
ranges, not company guidance.

## Lab 11 progress count

| Item | Status |
|---|---|
| D — question and Partner Exchange 1 | Complete |
| R — two inputs, ranges, outputs, and locked prediction | Complete |
| I — run sensitivity analysis | Complete |
| V — own-result verification and partner check | Complete |
| E — identify the driver, reflection, and partner summary | Complete |

**Completed: 5 of 5 Lab 11 sections.**
