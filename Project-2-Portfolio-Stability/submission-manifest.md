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

## Videos and corrected transcripts

| Deliverable | Required form | URL / path | Duration / timestamp index / status |
| --- | --- | --- | --- |
| Video 1 | YouTube link; <= 3:00; system/thinking evolution and an independently checked AI output | <https://youtu.be/hToZmeVKMwE> | Final duration reported by student: **3:18** — **exceeds the 3:00 limit by 18 seconds**. Source-recording index: 00:00 opening disclosures; 00:00:57 locked-prediction commit; 00:02:08 prediction; 00:03:15 final rejection. See transcript 1 timing limitation below. |
| Corrected transcript 1 | `transcript-video-1.txt` from actual recording | `transcript-video-1.txt` | Reviewed automated transcript with obvious finance/product-name corrections. It retains source-recording timestamps only; final YouTube alignment is **UNVERIFIED** because the silent-pause trim intervals are unknown. |
| Video 2 | YouTube link; <= 5:00; code and validation walkthrough | <https://youtu.be/sGohfiQHt2w> | Final duration reported by student: **5:37** — **exceeds the 5:00 limit by 37 seconds**. Source-recording index: 00:00 opening disclosures; 00:02:14 app walkthrough; 00:04:22 locked experiment; 00:05:20 manual testing / clean run. See transcript 2 timing limitation below. |
| Corrected transcript 2 | `transcript-video-2.txt` from actual recording | `transcript-video-2.txt` | Reviewed automated transcript with obvious finance/product-name corrections. It retains source-recording timestamps only; final YouTube alignment is **UNVERIFIED** because the silent-pause trim intervals are unknown. |
| Video 3 | YouTube link; <= 5:00; opens with live app and committee defense | <https://youtu.be/8ux-MGTgkI8> | Final duration reported by student: **4:29** — within the 5:00 limit. Source-recording index: 00:00 recommendation; 00:01:07 portfolios; 00:02:14 unresolved evidence; 00:03:21 0% / conditional pilot; 00:04:05 support/research tool. |
| Corrected transcript 3 | `transcript-video-3.txt` from actual recording | `transcript-video-3.txt` | Reported untrimmed; source timestamps are provisional YouTube timestamps pending playback confirmation. |

Video titles and unlisted-video accessibility have not been independently verified in YouTube. The required opening statements must be confirmed by playing each final YouTube upload; transcript review is not a substitute for final-video verification. For Videos 1 and 2, exact YouTube timestamps require either the final edited YouTube file or the exact source intervals removed in YouTube Studio. Without that evidence, timestamps must remain explicitly labelled source-recording indices.

## Brightspace checklist

- [ ] Submit the repository URL above and verify instructor access while logged out / in the required course context.
- [ ] Attach the same Markdown files `docs/decision-memo.md` and `docs/validation-and-ai-use.md`.
- [x] Add the three actual YouTube links and student-reported durations to this manifest. Video titles and access confirmations remain unverified.
- [x] Link the three corrected transcript files. Review the unclear/echo-affected passages against the final uploads before submission.
- [ ] Confirm the visible output, memo, transcripts, and validation record agree on the 0% decision, 8.15% prediction, 6.703604% actual result, and evidence limitations.
- [ ] Confirm no credentials, private information, temporary files, or unstated local paths are committed.
- [ ] Confirm all final links render from GitHub and all unlisted videos can be opened by the instructional team.
- [ ] Resolve or obtain instructor direction on the Video 1 (3:18) and Video 2 (5:37) duration-limit exceptions.

## Current frozen-file status

- [x] Project-owned app, source, tests, approved data/lineage, stress evidence, locked record, decision memo, validation record, and PDF companions exist.
- [x] Final clean-checkout record.
- [x] Stable source package pushed and verified from a clean remote clone.
- [ ] Logged-out browser and instructional-team access checks.
- [x] Video links and corrected source-recording transcripts.
- [ ] Final-video timestamp alignment, video title/access confirmation, Brightspace upload, and access confirmation.
