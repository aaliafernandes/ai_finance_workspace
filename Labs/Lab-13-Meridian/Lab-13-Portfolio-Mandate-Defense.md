# Lab 13 — Portfolio Mandate Defense

## Purpose and scope

This is an educational mandate-checking exercise for the fictional Meridian Foundation Reserve. It tests only rules that can be calculated from the supplied holdings and weights; it does not make a return forecast or investment recommendation.

## Statement classification and IPS map

An investment policy statement (IPS) is the client-approved document that turns an investor's goals, risk tolerance, liquidity needs, and investment restrictions into guidance for managing a portfolio. Objectives state the desired outcome; constraints set boundaries; preferences guide choices when more than one acceptable portfolio exists.

| Statement | Type | IPS component | Reason |
|---|---|---|---|
| S1: Seven-year horizon; annual rebalancing | Hard constraint | Time horizon / governance | It specifies the planning period and a required rebalancing cadence. |
| S2: CPI + 4% net of costs over rolling five years | Objective | Return objective | It states the desired long-run, after-cost outcome. |
| S3: $0.75m quarterly payout; one year held in cash or daily-liquid government securities | Hard constraint | Liquidity / spending | It gives a measurable payout and reserve requirement. |
| S4: 60% global equities / 40% U.S. investment-grade bonds | Preference | Benchmark / evaluation | It is a comparison benchmark, not a portfolio weight requirement. |
| S5: Long-only; no borrowing, shorts, or derivatives | Hard constraint | Legal / investment restriction | These are explicit prohibited activities. |
| S6: No single issuer above 8% | Hard constraint | Diversification | It is a measurable issuer concentration cap. |
| S7: Turnover at most 25% without committee approval | Hard constraint | Governance / trading | It is a measurable trading limit unless approval is given. |
| S8: At least 90% redeemable within five business days | Hard constraint | Liquidity | It supplies a measurable liquidity floor. |
| S9: No calendar-year loss greater than 10%, with no measure or breach rule | Unverifiable promise | Risk management | The return measure, treatment of valuations/cash flows, and breach response are unspecified, so it cannot be coded responsibly. |
| S10: No sector, ESG, tax, or home-bias preference; pilot objective not named | Missing | Preferences / implementation | The CIO has not said what trade-off or pilot objective should be optimized. |

## Checker and known-answer verification

The checker is [mandate.py](mandate.py). Run it from this folder with:

```powershell
python mandate.py
```

The computed reserve minimum is 3.0%: `(4 quarters × $0.75m) ÷ $100m × 100`.

| Rule | A | B | C |
|---|---|---|---|
| Weights sum to 100 | 100.0 pass | 100.0 pass | 100.0 pass |
| Long-only (lowest weight) | 0.0 pass | 0.0 pass | 0.0 pass |
| Reserve >= 3.0% | 14.0 pass | 1.0 FAIL | 2.0 FAIL |
| Redeemable in 5 days >= 90% | 100.0 pass | 85.0 FAIL | 100.0 pass |
| Largest single company <= 8% | 0.0 pass | 9.0 FAIL | 8.0 pass |
| Calendar-year loss | requires CIO clarification | requires CIO clarification | requires CIO clarification |
| Verdict | passes every checkable rule | fails 3 rule(s) | fails 1 rule(s) |

Acme Corp bonds and stock are combined for the issuer test, which is why B measures 9.0%.

### Long-only probe

I temporarily changed candidate A's Cash from 2 to -2 and Global equity index fund from 60 to 64, then reran the checker. The lowest weight was -2.0 and failed; the reserve weight remained 10.0 and passed, and no other rule failed. I restored the original values afterward.

### Self-quiz

Question: Why is the reserve minimum multiplied by 100 in the code?

My answer: the payout calculation produces a decimal share of the reserve (0.03), while portfolio weights and thresholds are expressed as percentages, so it becomes 3.0%.

## Attack candidate D

Candidate D holds 3% Cash and 97% Global equity index fund. It passes every checkable rule in `mandate.py`: it has the required reserve, is liquid within five business days, and the diversified fund is issuer-exempt.

The objection holds: a 97% global-equity reserve could plausibly lose more than 10% in a calendar year, so the CIO could reject it. S9 decides the objection, but it first needs a defined loss measurement and breach rule. If a partner instead proposed a 100% cash portfolio, I would cite S2 because it is unlikely to support the CPI + 4% net-of-costs objective over rolling five-year periods.

## Question for the CIO before optimization

How exactly should S9's “no calendar-year loss greater than 10%” be measured and enforced—for example, which return calculation and valuation dates apply, and is it a hard pre-trade risk limit or a reporting/breach rule?

If the CIO answers that it is a hard 10% calendar-year loss limit based on total return, the portfolio would need an explicit risk-control design and could not simply be optimized for the return objective. If instead it is a reporting threshold with committee review after a breach, the model can pursue S2 subject to the other hard constraints while monitoring losses.

## Reflection

A portfolio can pass every checkable rule and still be wrong because mechanical constraints do not establish whether its risk and expected return fit the foundation's purpose. Candidate D illustrates this gap: it is technically liquid and diversified under the coded tests but may conflict with the intended loss tolerance.

I was least certain about S4. I classified the benchmark as a preference/evaluation reference because the CIO did not say that the portfolio must hold 60/40; turning it into a binding allocation would be an additional instruction.
