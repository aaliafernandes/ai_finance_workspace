# Lab 15 — Meridian Known-Answer Verification

- **Date:** 2026-10-22
- **Engine:** `../Lab-14-Meridian/portfolio.py`
- **App:** `../Lab-14-Meridian/app.py`
- **Method:** long-only 5-percentage-point search, 6.5% return objective, and
  3% reserve-eligible minimum.

## Required runs

| Run | Bills | 10-year | IG | Equity | Return | Volatility | Result |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| As loaded | 0% | 20% | 25% | 55% | 6.51% | 9.44% | Matches |
| Equity expected return changed from 8.0% to 7.0% | 0% | 10% | 10% | 80% | 6.53% | 12.94% | Matches |
| IG–equity correlation changed to 0.50 in both cells | 0% | 40% | 0% | 60% | 6.52% | 9.73% | Matches |

The largest change between the first two runs is **25 points**: equity rises
from 55% to 80%. This illustrates estimation risk: a one-percentage-point
change in one expected-return input can materially alter the lowest-risk
feasible mix.

## Engine linkage check

`app.py` imports `CORRELATIONS`, `SLEEVES`,
`estimate_from_prices_csv`, and `find_lowest_risk_mix` from `portfolio.py`.
The app calls `find_lowest_risk_mix` for both displayed answers; it does not
copy the portfolio-return, covariance, volatility, or search math.

## Restoration check

The saved `portfolio.py` correlation is restored to **0.25** in both the
investment-grade-bond / global-equity and global-equity /
investment-grade-bond cells.
