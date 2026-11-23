# Project 2 development plan and evidence checklist

**Current status:** Phase 3B implements gross historical portfolio analytics and rule-specific verdicts. No committee recommendation exists.

## Eight requirements

## Phase 3B update

Phase 3B now provides the approved-price-only, annual-drift portfolio engine; equal-weight and policy-baseline calculations; a constrained 5% grid; rule-specific verdicts; and known-answer/negative tests. The engine produces gross historical analytics only. It deliberately cannot make a portfolio fully mandate-compliant or decision-ready while CPI, cost, liquidity, redemption, issuer/look-through, and signal evidence remains unresolved.

| Requirement | Planned evidence | Phase 1 status | Next phase |
| --- | --- | --- | --- |
| 1. Runnable Python web app | `app/`, pinned `requirements.txt`, verified README command, cold-run record | Structure and Streamlit pin only | Phases 3–5 |
| 2. Mandate | `Project-2-Mandate.md`; rule engine; app verdicts | Data gates documented; live eligibility remains unresolved | Phases 2–3 |
| 3. Two baselines plus constrained portfolio | Project-owned engine, comparison table, rule-level PASS/FAIL verdicts | Candidate components mapped only | Phase 3 |
| 4. Point-in-time signal and data card | Raw vintage data, data card, timing test, documented decision rule | Monitor-only provenance interface and negative tests complete; live vintage evidence/rule pending | Phase 2 |
| 5. Stress tests and process stop condition | One-input-at-a-time stress outputs for estimates, window, costs, constraints; stop condition | Phase 5A infrastructure and synthetic validation complete; non-locked approved-data cases remain pending | Phase 5B |
| 6. Locked Changed-Input Record | Human-authored AI-off prediction, pre-run commit, results, decision effect | Complete: prediction commit preserved, execution and arithmetic check documented | Preserve record; do not rewrite prediction |
| 7. Recommendation / allocation range / triggers | `docs/decision-memo.md`, app decision panel, visible output | Partial: memo recommends 0% live allocation and conditional future-pilot framing | Evidence gates and client approvals required before any live allocation |
| 8. Required opening statements | README, memo, three videos | README complete; remaining future items pending | Phases 7–8 |

## 300-point rubric map

| Criterion | Points | Planned evidence | Current status |
| --- | ---: | --- | --- |
| Problem definition and decision usefulness | 45 | Mandate, intended user, recommendation, allocation range, triggers | Partial: mandate classifications documented; no decision yet. |
| Data integrity and traceability | 45 | Data cards, raw/processed lineage, as-of rules, source dates, exclusions | Partial: approved price pipeline and gates exist; live CPI/ALFRED/cost evidence remains missing. |
| Financial soundness and judgment | 60 | Baselines, constrained weights, benchmark, risk/cost/turnover calculations, scenarios | Partial: gross analytics, annual drift, grid feasibility, and verdict boundary implemented; net evidence and stress pending. |
| Technical execution and usability | 45 | Web app, README command, dependencies, missing-data handling, visible output | Partial: Phase 4 app, smoke tests, and isolated startup complete; live evidence and submission-ready output remain pending. |
| Validation, sensitivity, and reproducibility | 75 | Known answers, independent checks, high-risk failure test, stress tests, cold run, AI check, prospective locked record | Partial: stress infrastructure, synthetic known answers, negative STOP tests, and app regressions complete; approved-data stress record, cold run, AI check, and locked record remain. |
| Professional communication | 30 | README, memo, transcripts, manifest, videos, consistent terms and numbers | Partial: README opening statements and planning documents only. |

## Phased implementation sequence

### Phase 4 completion note

The bounded Streamlit interface now has a Reset to Base control, approved-data error handling, three engine-driven portfolios, visual comparisons, rule-specific verdicts, a separately labeled BIL scenario, and provenance/blocker panels. It displays NOT DECISION-READY rather than a recommendation.

1. **Phase 2 — data integrity and mandate operationalization:** Phase 2B completed the price-data repair, validation interfaces, source documentation, and synthetic negative tests. Remaining work is live CPI/ALFRED/cost evidence and client decisions.
2. **Phase 3 — portfolio engine:** implement project-owned mandate verdicts, equal weight, approved second baseline, constrained portfolio, turnover calculation, and known-answer tests.
3. **Phase 4 — web application:** build the bounded Streamlit interface, Reset to Base, error handling, and committee layout.
4. **Phase 5 — validation and stress:** create visible outputs, independent/known-answer checks, high-risk failure test, one-input-at-a-time stress tests, and cold-run procedure.
5. **Phase 6 — prospective locked test:** student writes AI-off prediction, commits it before the isolated changed-input execution, then documents the real outcome.
6. **Phase 7 — decision documentation:** prepare the memo and validation/AI-use record after results are final.
7. **Phase 8 — submission evidence:** genuine cold review, corrected transcripts, YouTube links, manifest, repository/video access checks, and Brightspace attachments.

## Completion gate before Phase 2

- [x] The mandate distinguishes confirmed client statements from student-proposed assumptions.
- [x] The 10% BIL rule is classified as a scenario, not client policy.
- [x] The undefined calendar-loss statement remains monitor-only.
- [x] No Locked Changed-Input Record or test has been created.
- [ ] Student approves unresolved mandate/data decisions before source or engine work begins.
