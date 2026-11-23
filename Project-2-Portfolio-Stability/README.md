# FIN 439 Project 2 — Meridian Foundation Reserve Application

## Required opening statements

**AI use:** OpenAI Codex assisted with project planning, code structure, test design, debugging, Streamlit implementation, and documentation formatting. Material AI uses, independent checks, and the available tool/version disclosure are documented in `docs/validation-and-ai-use.md`.

**Student ownership and educational purpose:** The analysis and investment decision are the student's own. This project is educational coursework only, not personalized investment advice or a recommendation to buy or sell any security.

## Completed application and decision

This completed application evaluates whether the fictional Meridian Foundation Reserve committee should adopt, allocate to, rebalance, pilot, or reject a long-only portfolio-construction process. It compares two transparent baselines with a constrained minimum-volatility portfolio under the documented mandate.

**Final committee decision: REJECT live allocation or process deployment; current allocation: 0%.** The rejection applies to live capital deployment while evidence-dependent mandate gates remain unresolved. A **conditional future 0%-5% pilot discussion range** may be reconsidered only after the evidence gates close, the committee approves the operating definitions and ETF implementation, and a fresh cold run passes. That future range is student-proposed discussion language, not client-approved policy or a current recommendation.

All implementation choices marked **student-proposed** are analytical assumptions for this coursework project, not client-approved policy. See [Project-2-Mandate.md](Project-2-Mandate.md).

## Status

The completed package includes the runnable app, approved data/lineage, portfolio engine, visible results, stress evidence, locked-test evidence, decision memo, validation/AI-use record, submission audit, and manifest.

Only the project-owned approved dataset and engine outputs are Project 2 results. The retained Lab 15-era raw data and legacy `prices.csv` are historical evidence, not approved analytics inputs.

## Install and launch

From this directory in a clean checkout with Python 3.11 or later:

```powershell
python -m pip install -r requirements.txt
```

Launch with this single command:

```powershell
python -m streamlit run app/streamlit_app.py
```

The verified Phase 4 isolated-copy launch used `python -m streamlit run app/streamlit_app.py --server.headless true`. Browse to the local URL Streamlit prints (normally `http://localhost:8501`). No untracked Python runtime is required by the project.

## Phase 2B reproducibility commands

From this directory, in a clean checkout with Python 3.11 or later:

```powershell
python -m pip install -r requirements.txt
python src/data_pipeline.py
python -m unittest discover -s tests -v
python src/portfolio_engine.py
```

The first command writes **new** files, `data/processed/approved_monthly_prices.csv` and `data/processed/approved_monthly_lineage.csv`. It never changes the preserved Lab 15-era `data/processed/prices.csv` or any raw JSON file.

The approved output contains completed Yahoo source-label months only. Yahoo's monthly timestamp is preserved as a `PeriodLabel` and the raw UTC timestamp appears in the lineage file; neither is represented as a guaranteed month-end or tradable execution price.

## Project map

| Location | Purpose | Status |
| --- | --- | --- |
| `Project-2-Mandate.md` | Mandate specification, classifications, and unresolved questions | Complete; evidence-dependent rules remain UNVERIFIED |
| `docs/` | Decision memo, validation/AI-use record, methodology, source records, and submission PDFs | Complete written package; videos and transcripts remain student tasks |
| `app/` | Project-owned Streamlit user interface and presentation model | Complete and regression-tested |
| `src/` | Project-owned data integrity, CPI, signal-provenance, cost-evidence, portfolio, verdict, and stress logic | Complete analytical implementation; no live primary-source integrations |
| `tests/` | Project-owned integrity, provenance, portfolio, verdict, app-render, and synthetic stress tests | 42 passing tests in the final clean run |
| `outputs/` | Tracked visible portfolio and stress outputs | Complete visible-output and stress records |
| `validation/` | Locked record, phase reports, final audit, and cold-run evidence | Complete non-video validation package |
| `data/raw/` | Preserved source responses without transformation | Retained historical evidence |
| `data/processed/` | Validated price inputs and lineage used by the application | Complete approved dataset and lineage |

## Current data boundary

The existing BIL, IEF, LQD, and VT adjusted-close data were retrieved from Yahoo Finance on 2026-10-22 for Lab 15 practice. They are retained as original evidence. Phase 2B found that the preserved `prices.csv` carries an incomplete current-month observation under a monthly label, so it is not approved for decision use. The new approved dataset excludes the retrieval month and records raw-to-output lineage. See [docs/data-integrity-and-point-in-time.md](docs/data-integrity-and-point-in-time.md).

## Reuse boundary

Completed labs are source evidence and prototypes. Project 2 reuses documented concepts through project-owned files and does not depend on lab-relative imports. See [docs/reusable-components.md](docs/reusable-components.md).

## Submission status

The runnable app, gross portfolio logic, stress evidence, locked record, decision memo, validation/AI-use record, submission audit, and manifest are included. A clean remote clone passed the pipeline, 42 tests, and headless app probe; see [final-cold-run-report.md](validation/final-cold-run-report.md). Required student actions remain: record three videos, create corrected transcripts from those recordings, add YouTube URLs and timestamp indices to the manifest, attach the two required Markdown records to Brightspace, and perform final instructor-access checks. The process remains blocked from live allocation by the documented source-evidence gates. See the [decision memo](docs/decision-memo.md), [validation record](docs/validation-and-ai-use.md), [visible output](outputs/visible-output-summary.md), [submission audit](validation/final-submission-requirement-audit.md), and [submission manifest](submission-manifest.md).
