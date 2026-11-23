# Phase 2B validation report

**Run date:** 2026-11-22  
**Scope:** Project-owned data integrity, CPI hurdle interface, credit-spread provenance interface, and transaction-cost evidence gate. No portfolio optimization, app, live CPI evaluation, live ALFRED download, or Locked Changed-Input test was run.

## Commands run

From `Project-2-Portfolio-Stability`:

```powershell
python src/data_pipeline.py
python -m unittest discover -s tests -v
```

The audit environment used its available local Python 3.13.15 runtime. The pipeline and tests use only the Python standard library; `requirements.txt` pins Streamlit for the future app. A separate clean-user cold run remains a required future validation artifact.

An isolated temporary copy of the complete `Project-2-Portfolio-Stability` folder also ran the same pipeline and all nine tests successfully. That check confirms the Phase 2B code has no lab-relative imports or dependency on files inside the ignored `.tools` directory; the interpreter itself was supplied by the audit environment and is not part of the project submission.

## Results

| Check | Result |
| --- | --- |
| Build approved monthly prices | PASS |
| Approved coverage | 2021-10-01 through 2026-09-01 |
| Completed source-label observations | 60 |
| Adjacent monthly returns | 59 |
| Output files | `data/processed/approved_monthly_prices.csv`; `data/processed/approved_monthly_lineage.csv` |
| Automated tests | PASS — 9 passed, 0 failed, 0 errors |
| Original raw JSON files | Preserved unchanged |
| Original `data/processed/prices.csv` | Preserved unchanged and quarantined from decision use |

## Tests that passed

1. Archived raw data exclude the retrieval month and produce 60 aligned approved observations plus 240 lineage rows.
2. Two approved-data builds produce byte-identical price and lineage outputs.
3. A duplicate completed-period label raises `DataGateError` and stops processing.
4. A labeled synthetic CPI fixture produces the expected compounded five-year CPI + 4% hurdle.
5. A CPI observation published after cutoff raises `CpiAvailabilityError`.
6. Only a credit-spread observation with measurement and vintage dates at or before cutoff is selected.
7. No qualifying credit-spread vintage raises `SignalAvailabilityError`.
8. Turnover and evidence-backed synthetic trade-cost arithmetic are correct.
9. Missing cost evidence raises `CostEvidenceError`.

## Independently checked arithmetic

The synthetic CPI test checks:

`(110 / 100) × 1.04^5 − 1`

against the reusable hurdle function. The synthetic turnover test checks:

`0.5 × (|0.50 − 0.60| + |0.50 − 0.40|) = 0.10`.

Synthetic fixtures are not market data and are labeled accordingly in `tests/fixtures/`.

## Unresolved data gates

- No archived BLS `CUUR0000SA0` values/releases or historical vintages are stored. Live CPI evaluation remains blocked.
- No ALFRED payload/vintage evidence is stored for BAMLC0A0CM. The signal remains monitor-only and threshold-free.
- No dated bid/ask, commission, or market-impact ledger entries exist. Costs cannot be applied to a portfolio run.
- ETF five-business-day redemption, reserve eligibility, and wrapper-versus-look-through issuer treatment remain UNVERIFIED pending client definitions and dated primary evidence.
- Yahoo adjusted-close licensing/methodology and the economic meaning of its monthly interval label require final source evidence. The approved output therefore retains `PeriodLabel` rather than asserting month-end closes.

## Conclusion

Phase 2B validation code passes, but the unresolved gates above prohibit a live allocation recommendation or a PASS verdict for the affected mandate rules.
