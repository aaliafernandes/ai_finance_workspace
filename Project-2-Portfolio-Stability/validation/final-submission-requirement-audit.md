# Final Submission Requirement Audit

**Audit date:** 2026-11-23  
**Official requirements checked:** The official course repository was cloned and read at commit `bb73c5fe49648b5076e8419ff3dd095ffdc13f45`:

- `projects/project-2-investment-management-application.md`
- `projects/major-project-student-checklist.md`

This audit distinguishes a runnable/analytical artifact from evidence sufficient for a live investment decision. `UNVERIFIED` is never treated as `PASS` by the application.

## Project 2 base requirements

| Requirement | Exact project evidence | Status | Required action |
| --- | --- | --- | --- |
| Python web app that a stranger can start from the README | `README.md`; `app/streamlit_app.py`; `app/app_model.py`; `validation/phase-4-validation-report.md`; `validation/final-cold-run-report.md` | PASS | Preserve the clean-run record; video 3 must open with the app running live. |
| Lab 13 mandate: objective, universe, benchmark, risk measure, and limits | `Project-2-Mandate.md`; `docs/portfolio-engine-methodology.md`; `src/mandate_verdicts.py` | PARTIAL | Client/source evidence is still needed for reserve, redemption, issuer look-through, CPI/net objective, calendar-loss, and signal definitions. |
| Equal-weight baseline, second transparent baseline, and constrained portfolio; each has rule verdicts in app | `src/portfolio_engine.py`; `src/mandate_verdicts.py`; `app/streamlit_app.py`; `docs/decision-memo.md` | PASS for gross analytics and displayed verdicts | Keep NOT DECISION-READY framing; do not describe unresolved gates as compliance. |
| One point-in-time signal and data card | `docs/data-integrity-and-point-in-time.md`; `src/credit_signal.py`; `src/cpi.py`; `tests/test_phase2b.py` | PARTIAL | Archive actual CPI releases and ALFRED vintages, then approve an action rule before any trading use. Signal is correctly monitor-only now. |
| Stresses of estimates, window, costs, and constraints plus stop condition | `src/stress_tests.py`; `src/run_approved_stresses.py`; `docs/stress-testing-methodology.md`; `outputs/phase-5b-stress-results.md` | PASS for required infrastructure and executed cases | Hypothetical cost results must remain labelled hypothetical; add evidence-backed costs only if sourced. |
| Locked Changed-Input Record committed before run | `validation/locked-changed-input-prediction.md`; immutable commit `0f1c1da43b7958be8ae82e8e5b3f8b2712aebdbc`; `validation/phase-5b-validation-report.md` | PASS | Preserve the original commit and file unchanged. |
| Recommendation, allocation range, and monitoring/reversal triggers | `docs/decision-memo.md`; `docs/Decision-Memo.pdf`; `app/streamlit_app.py` | PASS | Current recommendation remains reject live allocation / 0%. The future 0%-5% pilot is conditional student-proposed language only. |
| Two opening statements in README, memo, and each video | `README.md`; `docs/decision-memo.md`; `docs/validation-and-ai-use.md`; `docs/Decision-Memo.pdf`; `docs/Validation-and-AI-Use.pdf` | PARTIAL | Open each actual video with both statements and verify against corrected transcripts. |

## Final frozen-package checklist

| Requirement | Exact project evidence | Status | Required action |
| --- | --- | --- | --- |
| Accessible repository; README, pinned dependencies, source, visible output, docs records | `README.md`; `requirements.txt`; `app/`; `src/`; `outputs/`; `docs/`; `validation/final-cold-run-report.md` | PARTIAL | Complete final push and repository-access check after the manifest-only commit. No `.env.example` is needed because the project uses no credentials. |
| Visible output shows material inputs, as-of date, and decision without running code | `outputs/phase-5b-stress-results.md`; `docs/decision-memo.md` | PASS | Preserve the files and confirm their GitHub rendering after push. |
| Decision Memo PDF, maximum two pages | `docs/Decision-Memo.pdf` | PASS | Visually checked; one page. |
| Validation and AI Use PDF including tools, checks, limitations, and locked record | `docs/Validation-and-AI-Use.pdf`; `docs/validation-and-ai-use.md` | PASS | Visually checked; one page. |
| Research-evolution / Edition A / Edition B item | Course checklist says to skip the research-evolution item for Project 2 | NOT APPLICABLE | Retain private editions only; do not submit them. |
| Video 1 <= 3 minutes and corrected transcript | Placeholder in `submission-manifest.md` | MISSING | Record and upload YouTube video, then create transcript from recording. |
| Video 2 <= 5 minutes and corrected transcript | Placeholder in `submission-manifest.md` | MISSING | Record and upload YouTube video, then create transcript from recording. |
| Video 3 <= 5 minutes, opens with app live, and corrected transcript | Placeholder in `submission-manifest.md` | MISSING | Record with live app opening, upload, and create transcript from recording. |
| Brightspace manifest with stable repository/video URLs, duration, indices, access confirmation, frozen-file checklist | `submission-manifest.md` | PARTIAL | Insert actual YouTube URLs, titles, durations, timestamp indices, and logged-out/access confirmations after recording. |
| Attach same two Markdown records to Brightspace | `docs/decision-memo.md`; `docs/validation-and-ai-use.md` | MISSING | Attach exactly those Markdown files to Brightspace. |
| Clean-user check and first failure/resolution record | `validation/final-cold-run-report.md` | PASS | Preserve the report; it discloses the host `venv` bootstrap limitation and successful clean project run. |
| No secrets, keys, private data, or undocumented local paths | `Project-2-Portfolio-Stability/.gitignore`; repository scan recorded in cold-run report | PARTIAL | Repeat final scan just before submission and avoid adding credentials. |

## Rubric-oriented evidence check

| Area | Evidence | Status | Required action |
| --- | --- | --- | --- |
| Problem definition and decision usefulness (45) | Mandate, decision memo, app overview, `docs/development-plan.md` | PARTIAL | Evidence gates prevent an adopted/live process, but the rejection recommendation is decision-useful. |
| Data integrity and traceability (45) | Raw JSON, approved data/lineage, data card, Phase 2B report/tests | PARTIAL | Archive primary-source live CPI, ALFRED, product, liquidity, and cost evidence with dates/licensing notes. |
| Financial soundness and judgment (60) | Engine methodology, three-portfolio comparison, stress output, decision memo | PARTIAL | No sourced net cost or validated CPI/net evaluation; unresolved rules cannot be passed. |
| Technical execution and usability (45) | Streamlit app, pinned requirements, unit/app tests, Phase 4 report | PARTIAL | Final clean-user run and manual live-demo check still needed. |
| Validation, sensitivity, reproducibility (75) | Tests, known answers, negative cases, locked record/result, stress reports | PARTIAL | Keep final cold-run evidence; source evidence, not just synthetic gates, remains incomplete. |
| Professional communication (30) | README, memo/validation Markdown and PDFs, manifest | PARTIAL | Finish actual videos, corrected transcripts, YouTube links, and Brightspace steps. |

## Conclusion

The package is analytically reproducible and contains the required written Project 2 artifacts, including the committed-before-run locked record, a passing clean-checkout record, and an honest 0% reject-live-allocation recommendation. It is **not fully submission-complete** until the final push/access check, three real videos/transcripts, manifest completion, and Brightspace attachments are completed. It is **not decision-ready for a live allocation** while the documented evidence gates are unresolved.
