# FIN 439 Project 2 Submission Manifest

**Project:** Meridian Foundation Reserve Investment Management Application  
**Repository:** <https://github.com/aaliafernandes/ai_finance_workspace>  
**Project folder in repository:** `Project-2-Portfolio-Stability/`  
**Stable package source commit:** [`46acffaab7e8b69ee6f94fa7950176c704aebfe7`](https://github.com/aaliafernandes/ai_finance_workspace/commit/46acffaab7e8b69ee6f94fa7950176c704aebfe7) (`Correct final Project 2 submission wording`). The final manifest metadata commit is reported separately after push to avoid a self-referential commit loop.
**Remote verification:** This stable source revision was successfully pushed and checked in a fresh remote clone. Logged-out browser access and instructional-team access remain **PENDING STUDENT VERIFICATION**.
**Decision:** REJECT live allocation or process deployment; approved allocation range 0%. A future 0%-5% pilot is conditional student-proposed language only.

## Written materials and evidence

| Item | Stable GitHub location | Verification status |
| --- | --- | --- |
| README / launch instructions | [README.md](https://github.com/aaliafernandes/ai_finance_workspace/blob/46acffaab7e8b69ee6f94fa7950176c704aebfe7/Project-2-Portfolio-Stability/README.md) | Clean remote clone passed; logged-out browser rendering pending |
| Decision memo (Markdown) | [docs/decision-memo.md](https://github.com/aaliafernandes/ai_finance_workspace/blob/46acffaab7e8b69ee6f94fa7950176c704aebfe7/Project-2-Portfolio-Stability/docs/decision-memo.md) | Present in clean remote clone; logged-out browser rendering pending |
| Decision memo (PDF) | [docs/Decision-Memo.pdf](https://github.com/aaliafernandes/ai_finance_workspace/blob/46acffaab7e8b69ee6f94fa7950176c704aebfe7/Project-2-Portfolio-Stability/docs/Decision-Memo.pdf) | Present in clean remote clone; logged-out download pending |
| Validation and AI-use record (Markdown) | [docs/validation-and-ai-use.md](https://github.com/aaliafernandes/ai_finance_workspace/blob/46acffaab7e8b69ee6f94fa7950176c704aebfe7/Project-2-Portfolio-Stability/docs/validation-and-ai-use.md) | Present in clean remote clone; logged-out browser rendering pending |
| Validation and AI-use record (PDF) | [docs/Validation-and-AI-Use.pdf](https://github.com/aaliafernandes/ai_finance_workspace/blob/46acffaab7e8b69ee6f94fa7950176c704aebfe7/Project-2-Portfolio-Stability/docs/Validation-and-AI-Use.pdf) | Present in clean remote clone; logged-out download pending |
| Mandate | [Project-2-Mandate.md](https://github.com/aaliafernandes/ai_finance_workspace/blob/46acffaab7e8b69ee6f94fa7950176c704aebfe7/Project-2-Portfolio-Stability/Project-2-Mandate.md) | Present in clean remote clone; logged-out browser rendering pending |
| Requirement audit | [final-submission-requirement-audit.md](https://github.com/aaliafernandes/ai_finance_workspace/blob/46acffaab7e8b69ee6f94fa7950176c704aebfe7/Project-2-Portfolio-Stability/validation/final-submission-requirement-audit.md) | Present in clean remote clone; logged-out browser rendering pending |
| Visible output | [visible-output-summary.md](https://github.com/aaliafernandes/ai_finance_workspace/blob/46acffaab7e8b69ee6f94fa7950176c704aebfe7/Project-2-Portfolio-Stability/outputs/visible-output-summary.md) | Present in clean remote clone; logged-out browser rendering pending |
| Stress output | [phase-5b-stress-results.md](https://github.com/aaliafernandes/ai_finance_workspace/blob/46acffaab7e8b69ee6f94fa7950176c704aebfe7/Project-2-Portfolio-Stability/outputs/phase-5b-stress-results.md) | Present in clean remote clone; logged-out browser rendering pending |
| Locked prediction | [locked-changed-input-prediction.md](https://github.com/aaliafernandes/ai_finance_workspace/blob/46acffaab7e8b69ee6f94fa7950176c704aebfe7/Project-2-Portfolio-Stability/validation/locked-changed-input-prediction.md) | Immutable pre-run blob matched in clean remote clone |
| Locked prediction commit | [`0f1c1da43b7958be8ae82e8e5b3f8b2712aebdbc`](https://github.com/aaliafernandes/ai_finance_workspace/commit/0f1c1da43b7958be8ae82e8e5b3f8b2712aebdbc) | Verified unchanged in clean remote clone |
| Locked-result verification | [phase-5b-validation-report.md](https://github.com/aaliafernandes/ai_finance_workspace/blob/46acffaab7e8b69ee6f94fa7950176c704aebfe7/Project-2-Portfolio-Stability/validation/phase-5b-validation-report.md) | Present in clean remote clone; logged-out browser rendering pending |
| Cold-run record | [final-cold-run-report.md](https://github.com/aaliafernandes/ai_finance_workspace/blob/46acffaab7e8b69ee6f94fa7950176c704aebfe7/Project-2-Portfolio-Stability/validation/final-cold-run-report.md) | Present in clean remote clone; logged-out browser rendering pending |

## Run the application

From `Project-2-Portfolio-Stability/` using Python 3.11 or later:

```powershell
python -m pip install -r requirements.txt
python src/data_pipeline.py
python -m unittest discover -s tests -v
python -m streamlit run app/streamlit_app.py
```

No credentials or `.env` file are required. The data pipeline retains the raw JSON and legacy processed file while recreating the validated approved data and lineage.

## Videos and corrected transcripts - PENDING STUDENT COMPLETION

| Deliverable | Required form | URL / path | Title, duration, timestamps, and access confirmation |
| --- | --- | --- | --- |
| Video 1 | YouTube link; <= 3:00; system/thinking evolution and an independently checked AI output | **PENDING - record first** | **PENDING** |
| Corrected transcript 1 | `transcript-video-1.txt` from actual recording | **PENDING - create after recording** | **PENDING** |
| Video 2 | YouTube link; <= 5:00; code and validation walkthrough | **PENDING - record first** | **PENDING** |
| Corrected transcript 2 | `transcript-video-2.txt` from actual recording | **PENDING - create after recording** | **PENDING** |
| Video 3 | YouTube link; <= 5:00; opens with live app and committee defense | **PENDING - record first** | **PENDING** |
| Corrected transcript 3 | `transcript-video-3.txt` from actual recording | **PENDING - create after recording** | **PENDING** |

Each video must begin with the two required AI-use/student-ownership and educational-not-advice statements. Do not create transcripts or timestamp indices before the actual recordings exist.

## Brightspace checklist - PENDING STUDENT COMPLETION

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
- [x] Stable source package pushed and verified from a clean remote clone.
- [ ] Logged-out browser and instructional-team access checks.
- [ ] Videos, corrected transcripts, YouTube metadata, Brightspace upload, and access confirmation.
