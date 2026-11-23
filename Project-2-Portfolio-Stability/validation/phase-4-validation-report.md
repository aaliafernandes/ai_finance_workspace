# Phase 4 validation report — Streamlit application

Run date: 2026-11-23. This report documents a coursework application and gross historical analytics only; it is not investment advice or a committee recommendation.

## Files implemented

- `app/streamlit_app.py` — Streamlit presentation and bounded scenario control.
- `app/app_model.py` — presentation model that obtains all analytics and verdicts through project-owned engine modules.
- `tests/test_app_model.py` — state, scenario, presentation alignment, import, and rendered-page smoke tests.
- `src/portfolio_engine.py` — engine-owned wealth-index and drawdown-path series for charts; the UI does not calculate financial metrics.
- `requirements.txt` — explicit pins for Streamlit and its directly imported chart/data packages.
- `README.md` and `docs/development-plan.md` — verified launch and phase status.

## Commands and results

From the project root:

```powershell
python -m pip install -r requirements.txt
python -m unittest discover -s tests -v
python -m streamlit run app/streamlit_app.py
```

The full suite completed with **31 passed, 0 failed, 0 errors**. It includes the retained Phase 2B/3B tests plus app-model tests confirming the three engine-driven results, 60 approved labels, 59 returns, non-decision-ready statuses, path alignment, scenario labeling, verdict display data, module import, and a Streamlit `AppTest` render with no page exception.

An isolated temporary copy of the complete Project 2 folder was launched with:

```powershell
python -m streamlit run app/streamlit_app.py --server.headless true --server.port 8517 --browser.gatherUsageStats false
```

It returned local HTTP status **200** and the Streamlit startup log reported its local URL. The temporary copy and its logs were removed after the check. No project data, raw JSON, or preserved legacy `prices.csv` was rewritten during validation.

## Functional scope confirmed

The app shows the required opening statements; mandate summary; equal-weight, policy-benchmark, and constrained-candidate comparison; allocations; gross wealth and drawdown charts; rule-specific PASS/FAIL/UNVERIFIED/SCENARIO tables; gross-data provenance; test/reproduction instructions; and unresolved evidence gates. The BIL control is visibly described as a student-proposed scenario and calls the existing constrained engine with the scenario floor. It does not insert a credit-spread threshold or trading rule.

## Remaining limitations and manual demonstration checks

- Every displayed result remains NOT DECISION-READY because reserve/liquidity, redemption, issuer look-through, CPI/net-cost objective, calendar-loss definition, transaction costs, and ALFRED-vintage/credit-spread evidence are unresolved.
- The app uses source labels and adjusted-close history, not guaranteed executable prices; results are gross, not net.
- The base-to-scenario toggle changes the constrained search constraint only. It is not client mandate approval.
- Before recording Video 3, manually open the app, toggle the 10% BIL scenario, use Reset to Base, expand each verdict panel, and confirm the live browser display is readable at the intended screen size. Verify the displayed local data range remains 2021-10-01 through 2026-09-01 and that no browser warning/error is shown.

Phase 4 did not create or execute the Locked Changed-Input test, create an AI-off prediction, commit, push, or state a committee recommendation.

## 2026-11-23 reset-control regression fix

### Confirmed bug and cause

Manual testing confirmed that selecting **Apply 10% BIL minimum scenario** and then clicking **Reset to base** raised `StreamlitAPIException`. The original button body assigned `st.session_state["bil_scenario"] = False` after the checkbox with that key had already been instantiated in the same script run. Streamlit prohibits that mutation order.

### Fix

`app/streamlit_app.py` now registers Reset to base before the checkbox with an `on_click=_reset_to_base` callback. Streamlit runs that callback before the next script execution and before the checkbox is instantiated. The callback clears only the scenario widget state. The resulting base state again calls the existing engine without a BIL scenario floor, so it does not change portfolio calculations, source data, or mandate rules.

Chart-only presentation improvements in the same fix map legends to **Equal Weight**, **60/40 Benchmark**, and **Constrained**. Wealth and drawdown date axes now use annual ticks and four-digit year labels. No financial calculation changed.

### Regression evidence

The targeted app suite was run with:

```powershell
python -m unittest discover -s tests -p test_app_model.py -v
```

Result: **6 passed, 0 failed, 0 errors**. The new interaction test executes the exact sequence: base page → check scenario → click Reset to base → check scenario again. It verifies no exception, checkbox state changes on each action, the scenario banner appears when enabled, and it disappears after reset.

The complete project suite was then run with:

```powershell
python -m unittest discover -s tests -v
```

Result: **32 passed, 0 failed, 0 errors**. `git diff --check -- .` also passed. Streamlit emits a harmless `ScriptRunContext` warning during its test harness's bare-mode execution; no page exception occurred.

## 2026-11-23 in-app documentation viewer fix

### Confirmed manual finding and cause

The three Markdown items under **Data provenance, validation, and limitations** were clickable but displayed no document content in the browser. The prior implementation emitted relative Markdown hyperlinks such as `../docs/...`. Streamlit serves the application, not arbitrary repository Markdown files at those browser routes, so navigating to a link did not load the local document.

### Fix

The app now uses a **Read project documentation** expandable in-app viewer with three tabs: Data integrity and point-in-time, Portfolio-engine methodology, and Phase 3B validation report. It reads only an explicit allowlist of those three repository-owned paths with UTF-8 decoding and renders their Markdown with `st.markdown`. A missing, unreadable, or non-allowlisted document produces a visible STOP error rather than a misleading empty page.

### Regression evidence

`tests/test_app_model.py` now verifies that all three allowlisted files can be read, their known headings are present, and those headings are present in the rendered Streamlit page. The targeted command was:

```powershell
python -m unittest discover -s tests -p test_app_model.py -v
```

Result: **7 passed, 0 failed, 0 errors**.

The full project command, `python -m unittest discover -s tests`, then completed with **33 passed, 0 failed, 0 errors**. `git diff --check -- .` passed as well.
