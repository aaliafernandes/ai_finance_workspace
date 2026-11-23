# Phase 5A stress-testing methodology and locked-test protection

This Phase 5A infrastructure produces gross, analytical-only sensitivity results for coursework. It does not make an investment recommendation, establish a net result, or convert an UNVERIFIED rule into PASS.

## Requirement basis and official-source limitation

The locally retained development plan maps the course requirement to one-input-at-a-time stress tests for estimates, historical window, costs, and constraints, with an explicit process stop condition. It also requires a prospective Locked Changed-Input Record with a human-authored AI-OFF prediction before execution. The official Project 2 brief and student checklist URLs were requested on 2026-11-23 but were unavailable through the accessible browser, so their current text could not be independently rechecked in this phase. This document relies on the locally retained mandate, plan, and prior audit until the official pages can be accessed again.

## Approved-data and modeling boundary

`src/run_stress.py` calls `run_project_stress_case`, which loads only `data/processed/approved_monthly_prices.csv` through the existing validated loader. It preserves the four-ETF universe, annual holdings drift, annual rebalance convention, long-only grid, and rule-verdict logic. Synthetic unit tests use clearly labelled in-memory price tables only; they do not run a Project 2 stress case or use the pending locked input.

## One-input-at-a-time cases

Each `StressCase` must change exactly one field from `StressInputs` base values. Combining changes stops as invalid rather than producing a confounded conclusion.

| Sensitivity | Changed input | Treatment | Boundary |
| --- | --- | --- | --- |
| Historical estimation window | `estimation_window_returns` | Takes the trailing requested count of approved monthly returns and reruns the engine selection. | At least two returns; must be shorter than available history. |
| Return assumption | `monthly_return_shift` | Adds a clearly hypothetical monthly shift after the engine generates each fixed portfolio return path. | Not a forecast, price rewrite, or reoptimization. |
| Risk assumption | `monthly_risk_multiplier` | Multiplies deviations around each path's sample mean; the mean itself is retained before any separate return shift. | Positive finite scalar; not a covariance model or a forecast. |
| Transaction cost | `hypothetical_one_way_cost_bps` | Applies unsourced one-way bps times modeled turnover at each trade label. | Sensitivity only; does not substitute for the dated cost ledger or deduct ETF expenses again. |
| Turnover constraint | `turnover_cap` | Reruns the constrained grid and stops if no candidate is feasible. | Decimal between zero and one. |
| BIL constraint scenario | `bil_scenario_floor` | Reruns the constrained grid with a separately labelled BIL floor. | Student-proposed scenario, not a client mandate. |

For return/risk and cost sensitivities, the selected weights remain the engine-selected weights from the same approved historical window. This separates path-assumption effects from a portfolio reoptimization. The optimizer's stored selection volatility remains the original realized-path selection metric; transformed analytics are reported as hypothetical sensitivity results only.

## STOP conditions

| Condition | Stress-run status | Required action |
| --- | --- | --- |
| Approved file missing or fails validated loader | `STOP_DATA_INTEGRITY` | Stop the process; repair and validate data lineage before rerun. |
| Invalid case, confounded multi-input change, invalid window, or invalid assumption | `STOP_INVALID_STRESS_INPUT` | Correct the specification; do not silently relax it. |
| No grid portfolio survives a constraint case | `STOP_INFEASIBLE` | Report infeasibility; do not substitute a fallback allocation. |
| Any evidence-dependent mandate rule remains unresolved | `STOP_UNVERIFIED_MANDATE_EVIDENCE` | Gross analytics may be displayed for diagnosis, but the investment process is not decision-ready. |

The current project is expected to carry the final STOP status until CPI/net-cost, reserve/liquidity, redemption, issuer look-through, calendar-loss, and credit-spread vintage/rule evidence is available.

## Reproducible commands

Install and ordinary-test commands:

```powershell
python -m pip install -r requirements.txt
python -m unittest discover -s tests -v
python src/run_stress.py --help
```

After a non-locked, student-approved one-input case is specified, use one `src/run_stress.py` option only. The runner prints a self-describing JSON record with input, status, stop reasons, coverage, portfolio weights, and gross analytics. No actual pending locked-case input or result is included in this repository, test fixture, example, log, or command history.

## Locked Changed-Input procedure — no case stored here

1. The student selects one input and independently writes a quantitative AI-OFF prediction with mechanism, units, expected magnitude, and expected decision effect.
2. The student places the exact baseline and changed values, the output metric, and the intended command in the required locked record; this repository deliberately does not store those pending values in Phase 5A.
3. The student commits the record to Git before any execution. Record the real pre-test commit hash and timestamp.
4. Only after that commit, run the one specified changed-input command once, save actual output, independently compare it with the prediction, and state the decision effect.
5. Preserve the initial record. Do not replace it with an after-the-fact prediction.

No locked case was executed, previewed, simulated, or placed in tests, fixtures, examples, logs, or this documentation.
