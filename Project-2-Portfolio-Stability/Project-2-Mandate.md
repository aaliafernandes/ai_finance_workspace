# Project 2 mandate specification — Meridian Foundation Reserve

> **Status: Phase 1 proposed specification.** This document distinguishes the fictional client's confirmed Lab 13 statements from student-proposed analytical implementation choices. A proposed choice is not client-approved policy.

> **Educational purpose:** This is a learning demonstration, not personalized investment advice or a recommendation to buy or sell any fund.

## Decision and intended user

**Intended user:** the fictional Meridian Foundation Reserve investment committee.

**Decision:** whether to adopt, allocate to, rebalance, pilot, or reject a long-only portfolio-construction process. No decision has been selected in advance.

## Mandate decision table

| Topic | Rule / definition | Source and status | Units | Enforceable with currently available Project 2 data? | Classification | Required evidence, assumption, or client approval |
| --- | --- | --- | --- | --- | --- | --- |
| Horizon and cadence | Seven-year horizon; annual rebalancing. | Lab 13 S1 — confirmed fictional-client statement. | Years; rebalance events. | Yes for documentation; no portfolio history is yet approved. | Governance rule. | None to retain as the case assumption. |
| Return objective | CPI + 4% annually, net of costs, over rolling five-year periods. | Lab 13 S2 — confirmed fictional-client statement. | Annual total return, percent; five-year rolling period. | No. CPI series, timing, net-cost methodology, and portfolio return history remain to be defined. | Objective and monitoring criterion; not yet a pre-trade optimizer constraint. | Select CPI source and vintage/lag rule; define compounded versus arithmetic comparison and cost treatment. |
| Universe | BIL, IEF, LQD, and VT only. | Student-proposed implementation universe based on existing Project 2/Lab 15 work. | Eligible tickers. | Partially. Existing price data exist but are not yet Project 2-approved. | Hard implementation constraint after approval. | Committee confirmation that four ETFs are permissible vehicles; Phase 2 source and product documentation. |
| Benchmark | 60% VT / 40% LQD, mapping Lab 13's 60% global equity / 40% U.S. investment-grade bonds benchmark. | Lab 13 S4 benchmark plus student-proposed transparent ETF mapping. | Portfolio weights, percent. | Yes mathematically. | Benchmark/comparator, not a required portfolio allocation. | Confirm mapping. It must display its own mandate verdict and may fail liquidity rules. |
| Construction process | Long-only constrained minimum-volatility portfolio using annualized historical volatility. | Long-only: Lab 13 S5 — confirmed. Minimum-volatility and risk measure: student-proposed. | Weights; annualized sample standard deviation, percent. | Partially. Lab prototype works; project-owned logic and approved inputs do not yet exist. | Long-only is hard; risk measure is proposed analytical design. | Approve annualized historical volatility as the selection metric; disclose it is historical, not a forecast. |
| Liquidity reserve | Cover four $0.75m quarterly payouts from a $100m reserve: minimum 3.0% in cash or daily-liquid government securities. | Lab 13 S3 — confirmed fictional-client statement. | USD millions; percent of portfolio. | Partially. Formula is available; live ETF eligibility and liquidity evidence have not been documented. | Hard constraint once eligible instruments are verified. | Verify BIL/IEF eligibility and relevant liquidity characteristics from primary fund sources. |
| Additional BIL scenario | At least 10% BIL. | Existing Project 2 draft; reclassified by student as a stress/scenario assumption. | BIL weight, percent. | Yes mathematically. | Scenario only; not a mandate rule. | No client-policy claim. Show separately from the 3% reserve test. |
| Redemption liquidity | At least 90% redeemable within five business days. | Lab 13 S8 — confirmed fictional-client statement. | Portfolio weight, percent; business days. | No. Lab 13 training values are not live ETF evidence. | Hard constraint once operational definition is approved. | Determine whether exchange-traded liquidity or fund redemption is the intended measure; cite primary sources. |
| Issuer concentration | No single issuer above 8%; securities of one issuer aggregate. | Lab 13 S6 — confirmed fictional-client statement. | Issuer exposure, percent. | Only provisionally at ETF-wrapper level. | Hard constraint, subject to approved measurement scope. | Confirm whether the Lab 13 diversified-fund exemption applies to ETFs. |
| ETF look-through | Existing Lab 13 diversified-fund exemption is provisionally used; underlying issuer compliance is not verified. | Lab 13 exemption plus student-proposed provisional treatment. | Underlying issuer exposure, percent. | No. Fund holdings and a methodology are absent. | Disclosure / unresolved policy issue. | Client must approve wrapper-level exemption, look-through methodology, or an alternative fund-level limit. |
| Turnover | Annual turnover = 0.5 × sum of absolute changes in portfolio weights; maximum 25% without committee approval. Initial demonstration compares to a hypothetical 60% VT / 40% LQD portfolio. | 25% limit: Lab 13 S7 — confirmed. Formula and starting portfolio: student-proposed. | Portfolio turnover, percent of portfolio per annual rebalance. | Partially. Calculation can be implemented after portfolio outputs exist. | Hard constraint in applicable runs; initial starting weights are hypothetical demonstration only. | Confirm turnover formula, starting portfolio, cash-flow treatment, and approval process. |
| Trading costs | Portfolio evaluation must be net of costs. | Lab 13 S2 — confirmed objective language; Project 2 stress requirement. | Basis points, dollars, and/or percent return. | No. No cost assumptions or sources are currently approved. | Required stress/monitoring input. | Select defensible sources and record retrieval date, definition, availability, and limitations. |
| Calendar-year loss | Greater than 10% net calendar-year loss triggers committee review and potential suspension of the process. It is not a promised loss limit. | Lab 13 S9 was explicitly undefined; review/suspension treatment is student-proposed. | Net calendar-year total return, percent. | No. Return method, dates, cash-flow treatment, and response process are unresolved. | Monitor-only condition until client approval. | Client must approve measurement and breach response; do not code as a guaranteed or hard pre-trade loss limit. |
| Credit-spread signal | Prepare to use ALFRED/FRED investment-grade credit spread data as a point-in-time risk gate. No threshold or trading action is set. | Lab 17 selected series; student-proposed future integration. | Percent spread; as-of date/vintage. | No. Vintage timing and decision rule need validation. | Unresolved analytical component. | Validate vintage availability and define rule before use. |

## Explicitly unresolved client questions

1. Which CPI series, publication lag, and vintage will measure the CPI + 4% objective?
2. Does the 8% issuer cap apply only to ETF wrappers under the diversified-fund exemption, or does it require look-through holdings?
3. What does “redeemable within five business days” mean for exchange-traded funds in this mandate?
4. How is the calendar-year loss calculated, and does a breach suspend the process, require review, or both?
5. Is the 0.5 × absolute-weight-change turnover formula acceptable, and how are cash flows treated?
6. Is 60% VT / 40% LQD an approved ETF implementation of the policy benchmark?
7. Are BIL and IEF eligible daily-liquid government securities for the reserve calculation?

## Known limitations at Phase 1

- The stored price data are Lab 15 practice inputs, not yet validated Project 2 source data.
- The historical annualized mean return used in the earlier Lab 15 prototype is not a forecast and does not establish the CPI + 4% objective.
- The current project has no cost assumptions, current holdings, approved CPI input, point-in-time signal rule, or committee recommendation.
- No Locked Changed-Input Record has been created or run. It must be completed prospectively and independently after the project has a stable baseline.
