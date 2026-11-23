# Phase 5B validation report — locked experiment and approved-data stresses

## Locked experiment pre-execution record

- Locked prediction commit: `0f1c1da43b7958be8ae82e8e5b3f8b2712aebdbc`
- Locked file: `validation/locked-changed-input-prediction.md`
- Prediction-file status before execution: unchanged relative to the locked commit by `git diff`.
- Intended execution timestamp: `2026-11-23T13:21:22-05:00`

## Initial execution failure before calculation

The exact requested command was attempted once:

```powershell
python src/run_stress.py --name "Locked estimation-window test" --description "Prospective one-input window test." --window-returns 36
```

It failed before `run_stress.py` began because this terminal reported that `python` was not recognized on `PATH`. No input was loaded, no portfolio calculation occurred, and no locked result was produced. Per the locked-test procedure, this failure is documented before a single equivalent retry with the project runtime explicitly addressed.

## Successful locked execution

- Retry execution timestamp: `2026-11-23T13:22:22-05:00`
- Runtime: project-available Python 3.13.15 invoked explicitly because `python` was absent from `PATH`.
- Command inputs: unchanged from the locked command: name `Locked estimation-window test`, description `Prospective one-input window test.`, and 36 trailing returns.
- Input coverage: approved 2023-09-01 through 2026-09-01 source labels, 36 monthly returns.
- Run status: `STOP_UNVERIFIED_MANDATE_EVIDENCE`.

The constrained minimum-volatility portfolio selected 25% BIL, 0% IEF, 40% LQD, and 35% VT. Its annualized sample volatility was **6.703604%**. This is -1.446396 percentage points from the locked 8.15% prediction and -2.000461 percentage points from the 8.704065% full-window baseline. The allocation did not change from the full-window constrained allocation.

The constrained result was feasible. Turnover was 25.0000% for the hypothetical initial trade at 2023-09-01, 3.7125% at 2024-09-01, and 2.8789% at 2025-09-01; no event exceeded the 25% cap. Mathematical universe, long-only, weight-sum, and turnover rules passed. Reserve, redemption, issuer/look-through, CPI/net-cost, calendar-loss, and credit-spread rules stayed UNVERIFIED, so no portfolio is decision-ready.

## Independent volatility verification

The 36 monthly constrained returns printed by the successful locked run were independently checked outside the project engine using the standard sample formula `sqrt(sum((r - mean(r))^2) / (n - 1)) * sqrt(12)`. With `n = 36`, the independent result was 0.067036042519, matching the engine's 0.06703604251932854 to displayed precision. This checks arithmetic from the emitted return path only; it is not a second market-data source or mandate-evidence check.

## Non-locked approved-data cases

At `2026-11-23T13:24:51-05:00`, the generic non-locked runner executed five student-proposed, one-input cases over the approved 59-return history: a -10 bps monthly return shift, 1.25x risk scaling, 25 bps hypothetical one-way cost, a 20% turnover cap, and a 10% BIL scenario floor. Full results are preserved in `outputs/phase-5b-stress-results.md`.

Every case returned `STOP_UNVERIFIED_MANDATE_EVIDENCE`. The 20% turnover cap reran the optimizer and selected 20% BIL / 0% IEF / 40% LQD / 40% VT with 9.42% volatility and 20.00% highest turnover. The 10% BIL scenario did not bind because the base constrained allocation already held 25% BIL. Return/risk/cost cases retain the same selection weights by design; their assumptions are hypothetical analytical sensitivities, not forecasts, actual transaction-cost estimates, or client policy.

## Streamlit communication update

The app now provides an on-demand **Non-locked stress tests** section. It calls the project-owned non-locked catalog and displays compact constrained-portfolio summaries plus the mandatory NOT DECISION-READY message. It does not display, call, or expose the locked case.

## Regression results

The full ordinary suite, including the app's on-demand non-locked stress-panel interaction test, completed with **42 passed, 0 failed, 0 errors** in 33.561 seconds. The Streamlit test harness emits a harmless bare-mode `ScriptRunContext` warning; no app page exception occurred. `python -m pip check` reported no broken requirements, and `git diff --check -- .` passed.

## Phase 5B limitations and process implication

The shorter window's lower historical volatility is not a future-risk conclusion. The sensitivity results do not establish net performance, reserve eligibility, ETF redemption, issuer look-through, CPI+4% performance, a loss-rule result, or a credit-spread action. The investment process must stop at its evidence gates; no committee recommendation, allocation range, or reversal trigger has been created in this phase.
