# Validation and AI Use Record — Project 2

## Required opening statements

**AI use:** OpenAI Codex assisted with planning, code structure, test design, documentation formatting, debugging, and Streamlit implementation. Material AI-assisted work is retained as project-owned code and documentation, with checks described below.

**Student ownership and educational purpose:** The analysis and investment decision are the student's own. This project is educational coursework only, not personalized investment advice or a recommendation to buy or sell any security.

## AI-use boundary

Codex helped organize and implement the project. The student selected the fictional mandate assumptions, selected the locked numerical prediction, reviewed outputs, and is responsible for the committee conclusion. The locked record states that AI helped organize and format it; it does not claim the record was entirely AI-free. No AI-generated output is treated as source evidence for market data, ETF eligibility, CPI, transaction costs, ALFRED vintages, or mandate compliance.

**Material tool disclosure:** OpenAI Codex was used through the coursework workspace on 2026-11-23 for planning, project-owned Python/Streamlit implementation, test design, debugging, documentation formatting, and final package checks. The interface did not expose a stable model/version identifier to record; the tool is therefore identified as **OpenAI Codex (model/version not exposed in the interface)**. The student independently checked the raw-to-lineage tests, known-answer/negative tests, manual Streamlit interactions, the emitted locked return-path volatility arithmetic, and the resulting decision framing. Material AI-assisted outputs were accepted only with the qualification that unresolved primary-source evidence stays UNVERIFIED.

## Data-integrity validation

### October 2026 partial-month issue

The original Yahoo monthly raw data included observations labelled 2026-10-01 and a 2026-10-22 retrieval-day observation. The earlier processing collapsed timestamps to month keys and allowed the incomplete retrieval-month figure into the preserved `data/processed/prices.csv`. Phase 2B preserved both raw files and the defective CSV, then created an approved pipeline that retains source timestamps, excludes the retrieval month, and writes `approved_monthly_prices.csv` plus lineage. Approved coverage is 2021-10-01 through 2026-09-01, with 60 labels and 59 returns. This was independently checked through raw-to-lineage validation tests; it is not described as guaranteed executable pricing.

### Point-in-time controls

The project includes interfaces that reject CPI observations published after a cutoff and credit-spread observations lacking an available vintage. Live CPI release/vintage files and live ALFRED vintage evidence have not been stored, so live evaluation remains blocked. The credit-spread signal remains monitor-only and threshold-free.

## Independent and known-answer checks

- Known answers verify a 100-to-110 price move as +10%, a 60% +10% / 40% -10% portfolio return as +2%, the required volatility/downside examples, maximum drawdown, turnover, annual holdings drift, invalid inputs, and infeasibility.
- Synthetic Phase 2B tests verify timestamp parsing, completeness, lineage, deterministic output, CPI publication cutoff, signal availability cutoff, and transaction-cost evidence gates.
- Synthetic Phase 5 stress tests verify one-input enforcement, trailing windows, return/risk transformations, turnover-based hypothetical-cost arithmetic, infeasibility, and STOP statuses.
- Streamlit `AppTest` checks page rendering, scenario enable/reset/reenable behavior, in-app documentation rendering, and the on-demand non-locked stress panel.
- At the latest Phase 5B run, the full suite reported **42 passed, 0 failed, 0 errors**. The test harness emits a benign bare-mode `ScriptRunContext` warning; no page exception occurred.

## Manual application validation and corrections

### Reset-to-base correction

Manual testing found that resetting the BIL scenario after the checkbox existed raised `StreamlitAPIException`. The cause was direct mutation of `st.session_state["bil_scenario"]` after widget instantiation. The app now uses a pre-widget `on_click` callback. The interaction test verifies enable → reset → enable again without exception.

### Documentation-viewer correction

Manual testing found that relative Markdown links under data provenance were clickable but did not load local Markdown documents through the Streamlit server. The app now renders the three trusted repository documents in an in-app expandable tabbed viewer. A regression test verifies file access and rendered headings.

## Locked changed-input record

The student-selected prediction was committed and pushed before the experiment:

| Item | Record |
| --- | --- |
| Commit | `0f1c1da43b7958be8ae82e8e5b3f8b2712aebdbc` on `origin/main` |
| Prediction | 8.15% annualized sample volatility |
| Change | All 59 approved monthly returns to the most recent 36 returns |
| Actual | 6.703604% annualized sample volatility |
| Actual minus prediction | -1.446396 percentage points |
| Actual minus 59-return baseline | -2.000461 percentage points |
| Decision impact | Lower observed historical volatility did not close evidence gates; the recommendation remains 0% live allocation. |

Before execution, the locked file was checked unchanged against the commit and `origin/main` resolved to the same SHA. The initially requested `python ...` command failed before execution because `python` was absent from `PATH`; that failure was documented before one equivalent retry with the project runtime. The retry ran at 2026-11-23T13:22:22-05:00. The independent arithmetic check recalculated sample volatility from the 36 emitted monthly returns using `sqrt(sum((r - mean(r))^2)/(n - 1))*sqrt(12)` and produced 0.067036042519, matching the engine at displayed precision.

## Remaining limitations

- The historical analyses are gross and use adjusted-close source labels, not guaranteed executable prices.
- No dated, sourced transaction-cost ledger supports net results.
- CPI release/vintage evidence, ALFRED vintages, reserve eligibility, redemption treatment, issuer look-through, calendar-loss definition, and a credit-spread action rule remain unresolved.
- The official Project 2 brief and student checklist were read from a clean clone of the course repository on 2026-11-23. Video, transcript, YouTube, Brightspace, and final access-confirmation work still requires student action.
- The project cannot claim full mandate compliance, a live allocation, or an investment recommendation until these gaps close.
