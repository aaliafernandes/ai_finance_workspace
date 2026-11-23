# Phase 3B validation report — portfolio engine

Run date: 2026-11-22. This report documents an educational, gross historical calculation; it is not investment advice, a net-performance claim, or a committee recommendation.

## Commands run

From `Project-2-Portfolio-Stability` with the declared clean-checkout command form:

```powershell
python -m pip install -r requirements.txt
python src/data_pipeline.py
python -m unittest discover -s tests -v
python src/portfolio_engine.py
```

The validation execution used the workspace's Python 3.13.15 runtime. The project itself requires Python 3.11 or later and has no Phase 3B third-party import beyond the pinned future-app dependency in `requirements.txt`.

## Test result

`python -m unittest discover -s tests -v` completed with **26 passed, 0 failed, 0 errors**.

Phase 3B added 17 tests. Together with the retained Phase 2B tests, the run checked:

- sole approved-price-file boundary, exact headers, positive values, first-of-month labels, and contiguous labels;
- a 100 to 110 price movement as a 10% monthly return;
- a 60% +10% / 40% -10% one-period portfolio return as +2%;
- the specified +1%, -1%, +1%, -1% sequence as 4.00% sample annualized volatility and 2.44948974% annualized zero-target downside deviation;
- the 1.00 → 1.10 → 0.99 → 1.089 path as -10% maximum drawdown;
- compounding exactly 12 monthly intervals for a complete calendar-year gross return;
- 50% initial turnover from the hypothetical 60% VT / 40% LQD start to equal weight;
- hand-calculated annual drift turnover of 2.30769231% after LQD rises from 100 to 110 and then holds;
- deterministic five-point-grid selection and turnover enforcement at every modeled event;
- no allocation fallback when a zero-turnover cap makes the grid infeasible;
- invalid weights and every UNVERIFIED/FAIL verdict boundary;
- the 80%/20% independent two-asset theoretical minimum-variance calculation as a separate covariance sanity check. The production objective remains realized annual-rebalance-path volatility, not this shortcut.

## Approved input and executed coverage

The engine loaded only `data/processed/approved_monthly_prices.csv`: 60 completed monthly source labels from 2021-10-01 through 2026-09-01, producing 59 monthly portfolio returns. It did not read the preserved Lab 15-era `data/processed/prices.csv` or any raw JSON directly. The approved source-label convention remains documented in `docs/data-integrity-and-point-in-time.md`; neither the labels nor adjusted closes are presented as guaranteed tradable prices.

## Executed gross analytics

Values below are rounded for readability. The source period is incomplete at both ends for calendar-year reporting, so only 2022–2025 complete calendar years appear. Costs, taxes, CPI, and signal rules are excluded.

| Portfolio | Gross geometric annualized return | Annualized sample volatility | Zero-target downside deviation | Maximum drawdown | Highest modeled turnover |
| --- | ---: | ---: | ---: | ---: | ---: |
| Equal weight | 2.87% | 7.52% | 4.98% | -15.49% | 50.00% initial hypothetical trade |
| Policy benchmark | 5.73% | 12.35% | 8.07% | -23.81% | 3.31% |
| Constrained minimum-volatility | 4.23% | 8.70% | 5.62% | -17.31% | 25.00% initial hypothetical trade |

The constrained grid selected 25% BIL, 0% IEF, 40% LQD, and 35% VT. Its rank metric equals its reported 8.70406495% realized annual-rebalance-path volatility. This is an execution record, not a recommendation or a claim that this allocation is client-suitable.

The executed verdicts show equal weight as **FAIL** on the applicable 25% initial-turnover cap (50% from the hypothetical starting portfolio). The policy benchmark and constrained grid pass the mathematical universe, long-only, weight-sum, and modeled-turnover checks. All three are **NOT DECISION-READY** because the evidence-dependent rules remain UNVERIFIED.

## Defects found and fixed during Phase 3B

The first direct command run found that the workspace Python runtime uses safe-path imports and did not automatically place `src` on `sys.path`. `src/portfolio_engine.py` now explicitly adds its own project-owned `src` directory before importing the Phase 2B cost helper, so the README command is independent of VS Code import settings. No external data, lab, Project 1, raw file, or preserved defective price file was changed.

## Remaining hard gates

The verdict engine correctly returns NOT DECISION-READY because these remain UNVERIFIED: BIL eligibility for the 3% reserve, 90% redemption, issuer concentration/ETF look-through, official CPI availability and net five-year hurdle, net calendar-year-loss trigger definition, and approved ALFRED vintage evidence/credit-spread threshold. Transaction costs remain unsupported by evidence; adjusted-close results should not have ETF expense ratios deducted again. The 10% BIL floor remains a separately labelled student-proposed scenario.

Phase 3B did not run a locked changed-input test, create an AI-off prediction, build Streamlit, commit, or push.
