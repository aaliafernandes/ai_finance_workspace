# Final Cold-Run Report

**Run date:** 2026-11-23
**Source commit cloned:** `81e3957044f4646e2eb182a70765a2af5f63ad0c` from `origin/main`
**Clean location:** a newly created temporary directory outside the workspace, with a newly created virtual environment. The temporary directory is not part of the submission.

## Exact project workflow exercised

From the fresh clone's `Project-2-Portfolio-Stability/` directory, the README workflow was exercised with the new environment's `python` executable:

```powershell
python -m pip install -r requirements.txt
python src/data_pipeline.py
python -m unittest discover -s tests -v
python -m streamlit run app/streamlit_app.py --server.headless true --server.port 8510
```

The commands use the exact README module/script entry points. The explicit headless/port arguments are test-only additions to avoid opening a browser and to make the startup probe deterministic.

## First failure and resolution

The host Python 3.13.15 runtime available to the test harness lacked the standard-library `venv` module, so the initial attempt to create a fresh environment with `python -m venv` failed **before any Project 2 command ran**. This is a test-harness bootstrap limitation, not an application or README failure: the README does not require the project to create a virtual environment. A temporary, isolated `virtualenv` bootstrap was used solely to create the clean environment. No project files, dependencies, or local paths were borrowed from the workspace afterward.

The dependency installer also exceeded the automation wrapper's short foreground-output window. It was allowed to finish as a hidden background process in the same temporary environment; `python -m pip check` then reported `No broken requirements found.` This is documented so the run is reproducible and its limitation is visible.

## Results

| Check | Result | Evidence |
| --- | --- | --- |
| Clone of remote source commit | PASS | Shallow clone of `origin/main` at `81e3957044f4646e2eb182a70765a2af5f63ad0c` |
| Pinned dependency install | PASS | Completed in fresh environment; `python -m pip check` reported no broken requirements |
| Approved-data pipeline | PASS | `APPROVED: 60 completed source-label months, 59 monthly returns`; coverage `2021-10-01` through `2026-09-01` |
| Automated tests | PASS | `Ran 42 tests in 35.664s` and `OK` |
| Streamlit launch | PASS | Headless server started at `http://localhost:8510`; HTTP probe returned `200` and Streamlit content |
| Visible results reproducible | PASS | Pipeline rebuilt approved data/lineage and app/test paths used the clean clone's files |
| Credentials/manual repair | PASS | No `.env`, API key, credential, or manual data repair was needed |

## Scope and remaining limitation

This cold run verifies reproducibility of the tracked package at the stated source commit. It does not convert the gross, source-label historical analytics into executable prices, sourced costs, a live CPI/ALFRED evaluation, or verified mandate compliance. Those investment-process evidence gates remain UNVERIFIED and the decision remains 0% live allocation.
