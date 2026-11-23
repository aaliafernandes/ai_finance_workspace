# Phase 5B stress results — educational gross analytics

This record uses only the approved monthly dataset. It is educational coursework, not investment advice, a net-performance claim, or an investment-committee recommendation.

## Locked estimation-window experiment

| Item | Record |
| --- | --- |
| Prediction commit | `0f1c1da43b7958be8ae82e8e5b3f8b2712aebdbc` |
| Successful execution timestamp | 2026-11-23T13:22:22-05:00 |
| Input change | All 59 approved monthly returns to the most recent 36 approved monthly returns |
| Window coverage | 2023-09-01 through 2026-09-01; 36 returns |
| Predicted constrained volatility | 8.15% |
| Actual constrained volatility | 6.703604% |
| Actual minus prediction | -1.446396 percentage points |
| Actual minus 59-return baseline (8.704065%) | -2.000461 percentage points |

The constrained allocation remained 25% BIL, 0% IEF, 40% LQD, and 35% VT. It was feasible under the 25% turnover cap. Its turnover events were 25.0000% at the hypothetical initial 2023-09-01 trade, 3.7125% at 2024-09-01, and 2.8789% at 2025-09-01. No modeled event exceeded the cap.

The constrained portfolio passed the mathematical universe, long-only, weight-sum, and turnover checks. It remained **NOT DECISION-READY** because the reserve, redemption, issuer/look-through, CPI/net-cost, calendar-loss, and credit-spread conditions remain UNVERIFIED. The 10% BIL statement remains a SCENARIO, not a client-approved mandate rule.

## Independent volatility check

The 36 monthly constrained-portfolio returns emitted by the successful locked run were independently entered into a standard-library calculation outside the project engine. The check used:

`sqrt(sum((r - mean(r))^2) / (n - 1)) * sqrt(12)` with `n = 36`.

It returned 0.067036042519, matching the engine's 0.06703604251932854 to the displayed precision. This verifies the annualized sample-volatility arithmetic from the captured return path; it does not independently validate market data, mandate evidence, or future performance.

## Non-locked approved-data sensitivities

All cases use the full approved 2021-10-01 through 2026-09-01 history (59 returns). Assumptions are student-proposed sensitivity inputs, not forecasts, client requirements, or sourced transaction costs.

| One input changed | Constrained allocation (BIL / IEF / LQD / VT) | Gross annualized return | Annualized volatility | Maximum drawdown | Highest turnover | Status |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| Hypothetical monthly return shift: -10 bps | 25% / 0% / 40% / 35% | 2.99% | 8.70% | -18.07% | 25.00% | STOP_UNVERIFIED_MANDATE_EVIDENCE |
| Hypothetical risk scale: 1.25x | 25% / 0% / 40% / 35% | 4.01% | 10.88% | -21.98% | 25.00% | STOP_UNVERIFIED_MANDATE_EVIDENCE |
| Hypothetical one-way cost: 25 bps | 25% / 0% / 40% / 35% | 4.21% | 8.70% | -17.31% | 25.00% | STOP_UNVERIFIED_MANDATE_EVIDENCE |
| Turnover constraint: 20% | 20% / 0% / 40% / 40% | 4.54% | 9.42% | -18.62% | 20.00% | STOP_UNVERIFIED_MANDATE_EVIDENCE |
| BIL scenario floor: 10% | 25% / 0% / 40% / 35% | 4.23% | 8.70% | -17.31% | 25.00% | STOP_UNVERIFIED_MANDATE_EVIDENCE |

The 10% BIL floor did not bind because the base constrained allocation already held 25% BIL. The 25 bps cost case is illustrative only; it applies a hypothetical cost to modeled turnover and does not represent observed spreads, commissions, market impact, or a net-return conclusion. Expense ratios were not subtracted again from adjusted-close results.

## Process implication

The shorter historical window produced a lower observed historical volatility than both the prediction and the full-window baseline. That outcome is a sensitivity result, not evidence that future risk is lower or that the process should be adopted. The unresolved mandate gates and explicit STOP statuses prohibit a committee allocation recommendation at this stage.
