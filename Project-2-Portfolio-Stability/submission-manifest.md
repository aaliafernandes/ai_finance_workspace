# FIN 439 Project 2 Submission Manifest

**Project:** Meridian Foundation Reserve Investment Management Application  
**Repository:** <https://github.com/aaliafernandes/ai_finance_workspace>  
**Project folder in repository:** `Project-2-Portfolio-Stability/`  
**Package source commit:** `81e3957044f4646e2eb182a70765a2af5f63ad0c` (`Finalize Project 2 submission package`). The final repository HEAD is reported separately after this manifest-only update to avoid a self-referential commit loop.
**Decision:** REJECT live allocation or process deployment; approved allocation range 0%. A future 0%-5% pilot is conditional student-proposed language only.

## Written materials and evidence

| Item | Repository path | GitHub location after push | Access check |
| --- | --- | --- | --- |
| README / launch instructions | `README.md` | `Project-2-Portfolio-Stability/README.md` | Clean-clone command check passed; final GitHub rendering check pending |
| Decision memo (Markdown) | `docs/decision-memo.md` | `Project-2-Portfolio-Stability/docs/decision-memo.md` | Pending final GitHub check |
| Decision memo (PDF) | `docs/Decision-Memo.pdf` | `Project-2-Portfolio-Stability/docs/Decision-Memo.pdf` | Pending final GitHub check |
| Validation and AI-use record (Markdown) | `docs/validation-and-ai-use.md` | `Project-2-Portfolio-Stability/docs/validation-and-ai-use.md` | Pending final GitHub check |
| Validation and AI-use record (PDF) | `docs/Validation-and-AI-Use.pdf` | `Project-2-Portfolio-Stability/docs/Validation-and-AI-Use.pdf` | Pending final GitHub check |
| Mandate | `Project-2-Mandate.md` | `Project-2-Portfolio-Stability/Project-2-Mandate.md` | Pending final GitHub check |
| Requirement audit | `validation/final-submission-requirement-audit.md` | `Project-2-Portfolio-Stability/validation/final-submission-requirement-audit.md` | Pending final GitHub check |
| Visible output | `outputs/visible-output-summary.md` | `Project-2-Portfolio-Stability/outputs/visible-output-summary.md` | Pending final GitHub check |
| Stress output | `outputs/phase-5b-stress-results.md` | `Project-2-Portfolio-Stability/outputs/phase-5b-stress-results.md` | Pending final GitHub check |
| Locked prediction | `validation/locked-changed-input-prediction.md` | `Project-2-Portfolio-Stability/validation/locked-changed-input-prediction.md` | Immutable pre-run commit below |
| Locked prediction commit | `0f1c1da43b7958be8ae82e8e5b3f8b2712aebdbc` | Repository commit | Verified locally; final remote check pending |
| Locked-result verification | `validation/phase-5b-validation-report.md` | `Project-2-Portfolio-Stability/validation/phase-5b-validation-report.md` | Pending final GitHub check |
| Cold-run record | `validation/final-cold-run-report.md` | `Project-2-Portfolio-Stability/validation/final-cold-run-report.md` | Clean clone passed; final GitHub rendering check pending |

## Run the application

From `Project-2-Portfolio-Stability/` using Python 3.11 or later:

```powershell
python -m pip install -r requirements.txt
python src/data_pipeline.py
python -m unittest discover -s tests -v
python -m streamlit run app/streamlit_app.py
```

No credentials or `.env` file are required. The data pipeline retains the raw JSON and legacy processed file while recreating the validated approved data and lineage.

## Videos and corrected transcripts - student completion required

| Deliverable | Required form | URL / path | Title, duration, timestamps, and access confirmation |
| --- | --- | --- | --- |
| Video 1 | YouTube link; <= 3:00; system/thinking evolution and an independently checked AI output | **TBD after recording** | **TBD** |
| Corrected transcript 1 | `transcript-video-1.txt` from actual recording | **TBD after recording** | **TBD** |
| Video 2 | YouTube link; <= 5:00; code and validation walkthrough | **TBD after recording** | **TBD** |
| Corrected transcript 2 | `transcript-video-2.txt` from actual recording | **TBD after recording** | **TBD** |
| Video 3 | YouTube link; <= 5:00; opens with live app and committee defense | **TBD after recording** | **TBD** |
| Corrected transcript 3 | `transcript-video-3.txt` from actual recording | **TBD after recording** | **TBD** |

Each video must begin with the two required AI-use/student-ownership and educational-not-advice statements. Do not create transcripts or timestamp indices before the actual recordings exist.

## Brightspace submission checklist

- [ ] Submit the repository URL above and verify instructor access while logged out / in the required course context.
- [ ] Attach the same Markdown files `docs/decision-memo.md` and `docs/validation-and-ai-use.md`.
- [ ] Add the three actual YouTube links, titles, durations, timestamp indices, and access confirmations to this manifest.
- [ ] Attach or link the three corrected transcripts after comparing them against recordings.
- [ ] Confirm the visible output, memo, transcripts, and validation record agree on the 0% decision, 8.15% prediction, 6.703604% actual result, and evidence limitations.
- [ ] Confirm no credentials, private information, temporary files, or unstated local paths are committed.
- [ ] Confirm all final links render from GitHub and all unlisted videos can be opened by the instructional team.

## Current frozen-file status

- [x] Project-owned app, source, tests, approved data/lineage, stress evidence, locked record, decision memo, validation record, and PDF companions exist.
- [x] Final clean-checkout record.
- [ ] Final GitHub access checks after the manifest-only push.
- [ ] Videos, corrected transcripts, YouTube metadata, Brightspace upload, and access confirmation.
