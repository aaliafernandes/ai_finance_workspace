# Phase 2B data integrity and point-in-time documentation

**Retrieval/audit date:** 2026-11-22. This document records verified facts separately from proposed methods. It does not supply an allocation, signal threshold, or investment recommendation.

## Price data inventory and approved transformation

| Item | Verified fact | Status / limitation |
| --- | --- | --- |
| Original source | Yahoo Finance public chart endpoint, `interval=1mo`, stored in `data/raw/*_yahoo_monthly.json`. Retrieval metadata records 2026-10-22 17:55:40 UTC. | Preserved evidence; Yahoo source/licensing and adjustment methodology still require review before final submission. |
| Original processed file | `data/processed/prices.csv`, 61 labels from 2021-10-01 through 2026-10-01. | Preserved but quarantined from decision use. Do not overwrite or delete. |
| Timing defect | Raw files contain both a 2026-10 period label and a 2026-10-22 retrieval-day observation. The earlier downloader reduced both to the same month key. | The resulting latest row is not a safely completed monthly period. |
| Approved pipeline | `src/data_pipeline.py` retains raw UTC timestamp and period label, excludes every period labeled in the retrieval month, checks completed-period uniqueness/continuity/alignment, and writes a price plus lineage file. | Does not assert that Yahoo's `1mo` period label is a month-end close. |
| Corrected coverage | 2021-10-01 through 2026-09-01: 60 completed source-label observations and 59 adjacent-period returns. | Historical adjusted-close data are not guaranteed point-in-time tradable execution prices. |

The approved output records `PeriodLabel` as Yahoo's month-level source label and `SourceTimestampUtc` in its lineage file. It does not rename either field to “month-end close.” A missing, duplicated, nonpositive, nonfinite, noncontiguous, or misaligned completed period raises `DataGateError` and stops output generation.

## Source cards

### ETFs — verified descriptive facts, retrieved 2026-11-22

| Ticker | Primary source / role | Field used or disclosed | Verified fact | Constraint status |
| --- | --- | --- | --- | --- |
| BIL | [State Street BIL](https://www.ssga.com/us/en/individual/etfs/state-street-spdr-bloomberg-1-3-month-t-bill-etf-bil) | Fund objective, gross expense ratio, holdings characteristics, ETF redemption disclosure | Seeks 1–3 month U.S. Treasury-bill exposure; page shows gross expense ratio 0.1352%. | **Conditional** reserve sleeve: client must confirm eligibility. ETF shares are not individually redeemable except in creation-unit aggregations. |
| IEF | [iShares IEF](https://www.ishares.com/us/products/239456/ishares-7-10-year-treasury-bond-etf-ief) | Fund objective, expense ratio, liquidity metrics | Tracks U.S. Treasury bonds with 7–10 years remaining maturity; page shows 0.15% expense ratio. | **Conditional** government-security sleeve; not yet proven to meet the mandate’s redemption wording. |
| LQD | [iShares LQD](https://www.ishares.com/us/products/239566/ishares-iboxx-investment-grade-corporate-bond-etf) | Fund objective, expense ratio, bid/ask display | Tracks U.S.-dollar investment-grade corporate bonds; page shows 0.14% expense ratio. | **Verified role; unresolved** look-through issuer treatment and liquidity-rule applicability. |
| VT | [Vanguard VT](https://advisors.vanguard.com/investments/products/vt/vanguard-total-world-stock-etf) | Fund objective, expense ratio, holdings disclosure | Tracks FTSE Global All Cap Index; official page reports 0.06% expense ratio. | **Verified role; unresolved** look-through issuer treatment and liquidity-rule applicability. |

Fund page metrics are dynamic. Record a dated copy or extracted evidence whenever a figure is used in a decision or cost ledger. ETF issuer pages describe exchange trading and/or creation-unit redemption, not a proof that a retail/committee portfolio is “redeemable within five business days.” Therefore that mandate rule remains **UNVERIFIED**, not PASS.

### CPI — official source of record, live evaluation blocked

| Field | Verified fact / proposed rule |
| --- | --- |
| Official source | U.S. Bureau of Labor Statistics CPI-U All Items, U.S. City Average, not seasonally adjusted: `CUUR0000SA0`. [BLS series definition](https://www.bls.gov/cpi/factsheets/cpi-series-ids.htm?form=MG0AV3) |
| Units / frequency | Index, 1982–84=100; monthly. |
| Publication timing | BLS publishes after the measurement month; consult and archive the release calendar for each decision date. [BLS release calendar](https://www.bls.gov/schedule/news_release/cpi.htm) |
| Point-in-time rule — proposed | Use only an archived BLS release/value public on or before the documented evaluation cutoff. Do not backfill a historical evaluation from a later database download. |
| Current implementation | `src/cpi.py` calculates the CPI + 4% five-year compounded hurdle and rejects observations published after the cutoff. |
| Evidence boundary | No live CPI observations, release-date archive, or historical vintage set was downloaded in Phase 2B. The tests use clearly labeled synthetic fixtures only. Live CPI evaluation is blocked. |

### Credit spread — monitor-only provenance interface

| Field | Verified fact / proposed rule |
| --- | --- |
| Source | [FRED BAMLC0A0CM](https://fred.stlouisfed.org/series/BAMLC0A0CM), sourced from ICE Data Indices. |
| Definition | ICE BofA U.S. Corporate Index Option-Adjusted Spread; percent, not seasonally adjusted, daily close. |
| Point-in-time source | [ALFRED](https://alfred.stlouisfed.org/help/downloaddata) is the historical-vintage source. |
| Proposed timing | At annual review, freeze the information set at a documented cutoff after the relevant market close. Select only an observation whose measurement date and ALFRED vintage date are both no later than that cutoff. Execute no earlier than the next trading session. |
| Current implementation | `src/credit_signal.py` rejects absent or future-dated vintage evidence. |
| Evidence boundary | No live ALFRED payload or trading threshold is stored. The signal is monitor-only and evaluation is blocked pending actual vintage evidence and an approved rule. |

### Costs and fees

ETF expense ratios are fund-level operating costs. Do not subtract a stated expense ratio again from an adjusted-close return series, because that would double count the economic effect already reflected in fund NAV/market performance. For a rebalancing study, deduct only separately evidenced trading costs.

The proposed one-way trade-cost formula is:

`abs(new_weight - old_weight) × (0.5 × bid_ask_spread + commission_rate + market_impact_rate)`.

`src/costs.py` requires ticker, source URL, as-of date, and nonnegative documented spread, commission, and impact rates. No historical values are supplied in Phase 2B. The initial 60% VT / 40% LQD position remains hypothetical.

## Hard data gates

- Stop if the current/incomplete source-label month would enter the approved dataset.
- Stop if a completed period has duplicate, missing, nonpositive, nonfinite, noncontiguous, or unaligned observations.
- Stop if CPI values were not public by the evaluation cutoff.
- Stop if no ALFRED vintage existed by the signal decision cutoff.
- Stop if a transaction-cost entry lacks dated source evidence.
- Report liquidity, ETF redemption, look-through concentration, and reserve eligibility as UNVERIFIED until the committee-approved operational definition and evidence exist.
