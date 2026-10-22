# Lab 15 — Illustrative Fund Universe

> Educational coursework only. This practice mandate and fund universe are not
> personalized investment advice or a recommendation to buy or sell securities.

## Mandate

- **Objective:** select the lowest-volatility long-only 5-point mix whose
  historical annualized mean-return estimate is at least **6.5%**.
- **Hard constraint:** at least **10%** of the portfolio must be in BIL, the
  reserve-eligible sleeve.
- **Important limitation:** the historical five-year return estimate is history,
  not a forecast.

## Assets and roles

| Ticker | Fund name | Role |
| --- | --- | --- |
| BIL | State Street SPDR Bloomberg 1-3 Month T-Bill ETF | Cash and reserve; reserve eligible |
| IEF | iShares 7-10 Year Treasury Bond ETF | Government bonds |
| LQD | iShares iBoxx $ Investment Grade Corporate Bond ETF | Investment-grade fixed income |
| VT | Vanguard Total World Stock Index Fund ETF Shares | Broad global equity |

## Data source and reproducibility

Each series was retrieved from Yahoo Finance's monthly historical adjusted-close
data on **2026-10-22**. Raw responses are in `data/raw/`; the processed file is
`data/processed/prices.csv`. The processed CSV has the date first, is oldest
month first, and contains one adjusted-close column per ticker.

Run the following from the workspace root to refresh the public data:

```powershell
.\.tools\python-3.13.15\python.exe .\Labs\Lab-15-Portfolio-Stability\src\download_prices.py
```

## App inputs and results

Upload `data/processed/prices.csv` to `../Lab-14-Meridian/app.py`, set the
objective to 6.5%, set the reserve minimum to 10%, and tick BIL only.

| Sample | BIL | IEF | LQD | VT | Expected return | Volatility | Reserve weight |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| All 60 monthly returns | 55% | 0% | 0% | 45% | 6.81% | 6.74% | 55% |
| Last 36 monthly returns | 85% | 0% | 0% | 15% | 6.80% | 1.78% | 85% |

The largest weight change is **30 points**. Changing the estimation window
substantially changes the selected mix, illustrating estimation risk.

## Individual completion checklist

- [ ] Draw the engine by hand and explain the mandate to a partner without a screen.
- [ ] Explain `find_lowest_risk_mix` line by line to a partner.
- [ ] Record the partner's actual changed estimate and resulting mix below.
- [ ] Write your own adopt, pilot, or reject decision.
- [ ] Complete the Brightspace quiz.

## Partner attack record

- **Date:**
- **Partner:**
- **Estimate changed:**
- **Before / after answer:**
- **Two-sentence response:**

## Your call

**Illustrative draft:** Pilot, not adopt: changing the historical sample from
all months to the last 36 months moves 30 percentage points from VT to BIL.
Reconsider only after validating the return assumptions, reserve requirement,
and whether the shorter sample is representative. This is a coursework example,
not investment advice.

Replace this draft with your own decision before submitting.
