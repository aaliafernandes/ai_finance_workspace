# Lab 17 data card

**Download date:** 29 October 2026. Each current-vintage download is from FRED;
each point-in-time download is from ALFRED, both published by the Federal
Reserve Bank of St. Louis.

| Series | Source and what it measures | Units and frequency | Publication/revision notes |
| --- | --- | --- | --- |
| BAA | [FRED BAA](https://fred.stlouisfed.org/series/BAA), Moody's seasoned Baa corporate-bond yield. | Percent, monthly. | Monthly observation; use ALFRED to determine what value was published by a past date. Historical values can be revised. |
| FEDFUNDS | [FRED FEDFUNDS](https://fred.stlouisfed.org/series/FEDFUNDS), effective federal funds rate. | Percent, monthly. | Monthly observation; the rate is published after the measurement month and may be revised. |
| DGS10 | [FRED DGS10](https://fred.stlouisfed.org/series/DGS10), 10-year Treasury constant-maturity rate. | Percent, daily. | Daily market-rate series; it generally has little publication lag and typically few historical revisions. |
| MORTGAGE30US | [FRED MORTGAGE30US](https://fred.stlouisfed.org/series/MORTGAGE30US), 30-year fixed-rate mortgage average. | Percent, weekly. | Weekly observation; the ALFRED comparison makes its historical availability explicit. |

## My prework series

- **FRED ID:** `BAMLC0A0CM`
- **Source and link:** [ICE BofA US Corporate Index Option-Adjusted
  Spread](https://fred.stlouisfed.org/series/BAMLC0A0CM), sourced from ICE Data
  Indices, LLC and released as part of ICE BofA Indices.
- **What it measures and units:** The option-adjusted spread of a
  capitalization-weighted index of U.S.-dollar investment-grade corporate debt
  versus a spot Treasury curve. Units are percent, not seasonally adjusted.
- **Why it is relevant:** This is a credit-risk measure—not a fund price. A
  wider spread generally signals higher required compensation for corporate
  credit risk and can affect the investment-grade bond sleeve (LQD); Treasury
  and cash sleeves provide a useful contrast.
- **Frequency / publication lag:** Daily close. The FRED page showed the 28
  October 2026 close updated on 29 October 2026, with the next release dated
  30 October 2026; the typical lag is about one business day.
- **Revisions:** The app's vintage comparison should normally show little
  release lag and few revisions for this daily market-rate series. The FRED
  page notes that the series has only three years of observations from April
  2026 onward and that all FRED data may be revised.
- **Three values checked against the FRED page on 29 October 2026:** 28 October
  2026 = 0.86%; 27 October 2026 = 0.88%; 26 October 2026 = 0.90%.
