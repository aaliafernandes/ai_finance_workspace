# Phase 5A validation report — stress infrastructure and locked-test protection

Run date: 2026-11-23. This phase adds educational stress-test infrastructure only. It does not execute an approved-data stress case, a locked changed-input case, an AI-OFF prediction, or a committee recommendation.

## Official-source check

The official Project 2 brief and major-project checklist URLs were requested through the available browser on 2026-11-23. Both fetches failed with a cache/access error, so their current text could not be reverified. The implementation uses the locally retained development plan and mandate requirements: one-input-at-a-time window, assumptions, costs, and constraint sensitivities; STOP behavior; and a prospective locked record with a human-authored AI-OFF prediction before execution. Recheck the official pages before final submission.

## Implemented infrastructure

- `src/stress_tests.py` defines one-input `StressCase` inputs, window selection, hypothetical return/risk and cost transformations, constraint reruns, and STOP statuses.
- `src/run_stress.py` is a generic one-case runner. Its mutually exclusive command options prevent combining stress inputs. It contains no pending locked-case values.
- `src/portfolio_engine.py` now exposes `analytics_from_return_path`, used by both existing annual-rebalance simulation and stress transformations so return, drawdown, and risk conventions remain engine-owned.
- `tests/test_stress_tests.py` uses synthetic in-memory data only. It contains no approved-data stress case or pending locked input.
- `docs/stress-testing-methodology.md` documents methods, units, limitations, STOP behavior, and the generic locked procedure without storing the pending case.

## STOP statuses

| Status | Meaning |
| --- | --- |
| `STOP_DATA_INTEGRITY` | The approved loader cannot provide validated Project 2 input. |
| `STOP_INVALID_STRESS_INPUT` | The case is malformed, changes more than one input, or has an invalid value/window. |
| `STOP_INFEASIBLE` | No constrained-grid candidate survives the selected constraints. |
| `STOP_UNVERIFIED_MANDATE_EVIDENCE` | Gross analytics can be diagnostic, but mandatory evidence gates still block a decision process. |

## Ordinary validation performed

The synthetic stress suite command was:

```powershell
python -m unittest discover -s tests -p test_stress_tests.py -v
```

It completed with **7 passed, 0 failed, 0 errors**. It covers window selection, return/risk arithmetic, turnover-based hypothetical cost arithmetic, turnover infeasibility, BIL-scenario labeling, multi-input rejection, invalid window rejection, and approved-loader failure.

`python src/run_stress.py --help` was also checked without executing any case. The first direct invocation exposed the workspace Python safe-path import setting; the runner was corrected to add its own project-owned `src` directory, matching the established direct-script pattern. The help command then completed successfully.

The complete ordinary command, `python -m unittest discover -s tests -v`, completed with **40 passed, 0 failed, 0 errors**. No locked test was run or previewed.

## Current limitations

- Return/risk and cost values are hypothetical sensitivities, not forecasts, sourced transaction-cost estimates, or net performance.
- The cost sensitivity cannot replace the Phase 2B dated cost-evidence ledger and does not subtract ETF expense ratios again.
- Current UNVERIFIED mandate rules force a STOP status even when a mathematical grid result exists.
- No stress output can be interpreted as a recommendation, allocation range, or evidence that the process may be adopted.
