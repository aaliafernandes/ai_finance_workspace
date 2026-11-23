# Meridian Foundation Reserve — Committee Decision Memo

**Date:** 2026-11-23  
**Decision owner:** Fictional Meridian Foundation Reserve investment committee  
**Status:** Educational coursework; not personalized investment advice.

## Required opening statements

**AI use:** OpenAI Codex assisted with project planning, code structure, testing, documentation formatting, and app development. Material outputs were retained in the repository and independently checked as described in [validation-and-ai-use.md](validation-and-ai-use.md).

**Student ownership and educational purpose:** The analysis and investment decision are the student's own. This project is educational coursework only, not personalized investment advice or a recommendation to buy or sell any security.

## Recommendation

**REJECT a live allocation or process deployment at this time; allocation range: 0%.**

This is not a rejection of further research. It is a rejection of capital deployment while material mandate conditions are unresolved. A **future conditional pilot range of 0%–5%** may be reconsidered only after the evidence checklist below is closed, the committee approves the ETF implementation and operating definitions, and the process passes a fresh cold run. This conditional range is a student-proposed governance discussion point, not client-approved policy or a current allocation recommendation.

## Mandate and decision problem

Meridian is a fictional $100 million reserve with a seven-year horizon and annual rebalancing. The confirmed case objective is CPI + 4% annualized, net of costs, over rolling five-year periods. The documented benchmark maps to 60% VT / 40% LQD; the implementation universe is BIL, IEF, LQD, and VT. The project compares equal weight, the policy benchmark, and a long-only 5% grid constrained minimum-volatility process. See [Project-2-Mandate.md](../Project-2-Mandate.md).

The 3.0% reserve need arises from four $0.75 million quarterly payouts. The 25% turnover cap uses one-way turnover, `0.5 × sum(abs(weight change))`, against a hypothetical 60% VT / 40% LQD initial allocation. The 10% BIL floor is a separately labelled student-proposed scenario, not a client mandate.

## Data, timing, and limitations

The engine accepts only `data/processed/approved_monthly_prices.csv`: 60 completed Yahoo adjusted-close source-label observations from 2021-10-01 through 2026-09-01, producing 59 adjacent-period returns. The preserved legacy `prices.csv` is quarantined because it included an incomplete October 2026 observation under a monthly label. The approved loader rejects missing, duplicate, nonpositive, nonfinite, noncontiguous, and misaligned observations. See [data-integrity-and-point-in-time.md](data-integrity-and-point-in-time.md).

These source labels and adjusted closes are not guaranteed point-in-time executable prices. Results are gross historical analytics, not net return, forecasts, or investment advice. CPI release/vintage evidence, ALFRED credit-spread vintages, and dated trading-cost evidence are absent. ETF expense ratios are not subtracted again from adjusted-close returns because that could double count fund expenses.

## Gross historical comparison

The base history covers 59 returns. Annual holdings drift between annual rebalances; it is not monthly constant-weight rebalancing.

| Portfolio | Target allocation | Gross geometric annualized return | Annualized sample volatility | Downside deviation | Maximum drawdown | Highest modeled turnover | Status |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| Equal weight | 25% each | 2.87% | 7.52% | 4.98% | -15.49% | 50.00% | FAIL turnover; NOT DECISION-READY |
| Policy benchmark | 0% BIL / 0% IEF / 40% LQD / 60% VT | 5.73% | 12.35% | 8.07% | -23.81% | 3.31% | NOT DECISION-READY |
| Constrained minimum-volatility | 25% BIL / 0% IEF / 40% LQD / 35% VT | 4.23% | 8.70% | 5.62% | -17.31% | 25.00% | NOT DECISION-READY |

Equal weight has the lowest reported volatility but is not feasible under the applicable initial hypothetical turnover cap: moving from 60% VT / 40% LQD to 25% each requires 50% turnover. The constrained portfolio minimizes realized annual-rebalance-path volatility only among feasible 5% grid candidates; it is an analytical candidate, not a recommendation.

## Mandate compliance and evidence gates

The engine can PASS the approved four-ETF universe, long-only weights, 100% weight sum, and modeled turnover where arithmetic is available. It must not PASS these unresolved conditions:

- BIL/IEF eligibility for the 3% reserve;
- 90% redeemable within five business days;
- 8% issuer concentration and ETF look-through treatment;
- CPI + 4% net rolling-five-year objective;
- net calendar-year-loss review/suspension definition;
- ALFRED vintage evidence and an approved credit-spread action rule.

Consequently, all three portfolios remain NOT DECISION-READY. The credit-spread series is monitor-only; no threshold or trade action is asserted.

## Stress findings

The locked historical-window test reduced the return history from 59 to 36 returns (2023-09-01 through 2026-09-01). The constrained allocation remained 25% BIL / 0% IEF / 40% LQD / 35% VT. Its observed historical annualized sample volatility was 6.703604%, versus the 8.15% locked prediction and 8.704065% full-window baseline. The actual result was -1.446396 percentage points from the prediction and -2.000461 percentage points from baseline. No locked-window turnover event exceeded 25%.

The non-locked approved-data sensitivities were all student-proposed and all returned `STOP_UNVERIFIED_MANDATE_EVIDENCE`. A 20% turnover cap changed the constrained allocation to 20% BIL / 0% IEF / 40% LQD / 40% VT and increased observed volatility to 9.42%. A 10% BIL floor did not bind because the base allocation already held 25% BIL. The -10 bps monthly return, 1.25× risk, and 25 bps hypothetical cost cases are analytical sensitivities only; the cost case is not a sourced cost estimate. Full results: [phase-5b-stress-results.md](../outputs/phase-5b-stress-results.md).

The stress set is sufficient to demonstrate the required one-input categories and stop behavior, but it is not sufficient to support a live allocation. It has one locked historical-window comparison, no verified net-cost implementation, no live CPI/vintage evaluation, and no client-approved definitions for several hard rules.

## Monitoring, STOP, and reversal framework

### Immediate STOP triggers before any allocation

1. Approved-price integrity failure, including an incomplete retrieval month, missing/duplicate/misaligned period, or invalid numerical value.
2. No feasible constrained portfolio under committee-approved constraints.
3. Missing CPI release/vintage, ALFRED vintage, or dated trading-cost evidence needed for the selected decision date.
4. Unresolved reserve eligibility, redemption, issuer look-through, or client definitions required to evaluate a hard mandate rule.

### Conditional future-pilot monitoring

Only after the pre-allocation gates close, monitor: CPI + 4% net over rolling five-year periods using approved release timing; each rebalance turnover against the approved cap; verified reserve/liquidity and issuer treatment; verified net calendar-year loss against the approved review/suspension definition; and any subsequently approved point-in-time credit-spread rule. Do not invent a credit-spread threshold before validation and committee approval.

### Conditional reversal triggers

For a future committee-approved pilot, pause or unwind the pilot if a verified hard mandate condition fails, approved data integrity fails, a rebalance becomes infeasible, turnover exceeds the approved cap without approval, or the committee-approved net-loss or signal rule triggers its documented action. The current 0% recommendation needs no reversal action.

## Evidence required before any live allocation

1. Archived BLS CPI-U values, release dates, vintage/availability rule, and a net-cost five-year hurdle calculation.
2. Primary-source evidence and committee approval for reserve eligibility, redemption measurement, ETF mapping, and issuer look-through/exemption scope.
3. Dated bid/ask, commission, and market-impact evidence in the transaction-cost ledger.
4. ALFRED vintage data, annual decision cutoff, and a committee-approved monitor/action rule if credit spread will affect trading.
5. Committee-approved calendar-year net-loss calculation and breach response.
6. A fresh clean checkout/cold run, post-evidence stress outputs, and a reviewed implementation package.

Until then, 0% is the only defensible live allocation range.
