# Visible Output Summary - Meridian Foundation Reserve

**As-of boundary:** Approved completed Yahoo adjusted-close source labels from 2021-10-01 through 2026-09-01; 60 labels and 59 adjacent-period returns. The source labels are not guaranteed executable prices.  
**Decision:** **REJECT live allocation or process deployment; approved allocation range: 0%.** This is educational coursework, not investment advice.

| Portfolio | Target weights (BIL / IEF / LQD / VT) | Gross geometric annualized return | Annualized sample volatility | Maximum drawdown | Highest modeled turnover | Decision status |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| Equal weight | 25% / 25% / 25% / 25% | 2.87% | 7.52% | -15.49% | 50.00% | FAIL hypothetical initial 25% turnover cap; not decision-ready |
| Policy benchmark | 0% / 0% / 40% / 60% | 5.73% | 12.35% | -23.81% | 3.31% | Not decision-ready |
| Constrained minimum-volatility candidate | 25% / 0% / 40% / 35% | 4.23% | 8.70% | -17.31% | 25.00% | Not decision-ready |

The portfolio engine uses annual rebalancing with drift between rebalances and only the approved dataset. The constrained candidate is an analytical result, not a recommendation.

## Executed stress evidence

The committed-before-run window test reduced 59 returns to 36 trailing returns. The student prediction was 8.15% constrained annualized volatility; the observed result was 6.703604%, versus the 8.704065% 59-return baseline. The allocation stayed 25% / 0% / 40% / 35%. See [Phase 5B stress results](phase-5b-stress-results.md).

All approved-data stress cases are `STOP_UNVERIFIED_MANDATE_EVIDENCE`, not trade instructions. CPI release/vintage evidence, dated transaction costs, reserve/redemption evidence, issuer look-through, calendar-loss definitions, and a credit-spread action rule remain unresolved. Therefore no portfolio can be presented as fully mandate compliant.
