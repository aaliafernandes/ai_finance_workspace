# Project 2 — Portfolio Stability Decision

> Educational coursework only. This is a learning demonstration, not
> personalized investment advice or a recommendation to buy or sell any fund.

## Illustrative mandate

**Objective:** find the lowest-volatility long-only mix with a historical
annualized expected-return estimate of at least **6.5%**.

**Hard constraint:** at least **10%** of the portfolio must be in the
reserve-eligible cash sleeve (BIL). The 10% threshold is an illustrative
coursework assumption, not a real client mandate.

## Fund universe and roles

| Ticker | Fund name | Role |
| --- | --- | --- |
| BIL | State Street SPDR Bloomberg 1-3 Month T-Bill ETF | Cash and reserve sleeve; reserve eligible |
| IEF | iShares 7-10 Year Treasury Bond ETF | Government-bond sleeve |
| LQD | iShares iBoxx $ Investment Grade Corporate Bond ETF | Investment-grade fixed-income sleeve |
| VT | Vanguard Total World Stock Index Fund ETF Shares | Broad global-equity sleeve |

The funds are a compact, role-based practice universe. They are not
recommendations. BIL is used instead of a money-market fund because its market
price history can be used to calculate monthly total returns from adjusted
close prices.

## Price-data source and transformation

| Ticker | Source | Frequency and field | Retrieval date |
| --- | --- | --- | --- |
| BIL | Yahoo Finance Historical Data | Monthly adjusted close | 2026-10-22 |
| IEF | Yahoo Finance Historical Data | Monthly adjusted close | 2026-10-22 |
| LQD | Yahoo Finance Historical Data | Monthly adjusted close | 2026-10-22 |
| VT | Yahoo Finance Historical Data | Monthly adjusted close | 2026-10-22 |

Raw Yahoo API responses are retained in `data/raw/`. Run
`python src/download_prices.py` to reproduce the processed file at
`data/processed/prices.csv`. It has the date first, oldest month first, and one
adjusted-close column per ticker. The script retains the most recent 61 monthly
observations, which produces 60 monthly returns (about five years).

Historical average returns, volatility, and correlations calculated from this
file describe the sample period; they are not forecasts.
