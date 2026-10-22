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
