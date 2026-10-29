# Lab 15 — Portfolio Stability Decision

This folder holds the Lab 15 evidence separately from Project 2.

## Contents

| File or folder | Purpose |
| --- | --- |
| `Meridian-Flowchart.md` | Mermaid diagram of the Meridian engine |
| `Meridian-Known-Answer-Verification.md` | Required Meridian verification runs |
| `Lab-15-Illustrative-Universe.md` | Standalone practice mandate, sources, results, and completion checklist |
| `data/processed/prices.csv` | Five years of aligned monthly adjusted-close prices for the practice universe |
| `data/raw/` | Original Yahoo Finance responses and retrieval metadata |
| `src/download_prices.py` | Reproducible data-download script |

The Streamlit app remains at `../Lab-14-Meridian/app.py` because it must import
the engine and Meridian inputs from `../Lab-14-Meridian/portfolio.py` rather
than copy the math.

## Run the app and upload the Lab 15 data

From the workspace root in PowerShell, run:

```powershell
& .\.tools\python-3.13.15\python.exe -m streamlit run .\Labs\Lab-14-Meridian\app.py
```

Then open the local URL Streamlit displays and upload
`Labs/Lab-15-Portfolio-Stability/data/processed/prices.csv` using **Upload
monthly prices.csv** in the sidebar. The app reports that it is using uploaded
historical estimates after the file is accepted. These estimates are historical
and are not forecasts or investment advice.

The app's project configuration disables Streamlit usage telemetry so it does
not need to write to the Windows user profile; this fixes the prior startup
error that prevented the upload control from working.
