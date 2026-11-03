# Lab 18 — Legend Investor as Skill

Educational workflow only; it is not personalized investment advice.

## Run the reproducible facts script

From the workspace root:

```powershell
$env:SEC_USER_AGENT = "Your Name your.email@purdue.edu"
python .codex/skills/buffett-10k-analysis/scripts/edgar_10k_facts.py COST --json Labs/Lab-18-Legend-Investor-as-Skill/outputs/COST_facts.json
```

The script uses only SEC EDGAR company facts and only annual 10-K values. The
latest filing wins when EDGAR provides the same fiscal period more than once.

## Memo

After running the script, invoke the `buffett-10k-analysis` skill and ask it
to create `outputs/COST_memo.md`. It must use only the generated JSON facts.
The skill owns no arithmetic: code calculates every value and every check;
the model supplies only a short qualitative business judgment.

## Run the app

```powershell
pip install -r Labs/Lab-18-Legend-Investor-as-Skill/requirements.txt
streamlit run Labs/Lab-18-Legend-Investor-as-Skill/app.py
```

## Sources

- SEC EDGAR [data APIs](https://www.sec.gov/search-filings/edgar-application-programming-interfaces), retrieved 2026-11-03.
- [FAskills README](https://github.com/CinderZhang/FAskills/blob/main/README.md) and [Buffett page](https://github.com/CinderZhang/FAskills/blob/main/financial-researcher/experts/warren_buffett.md), course-provided links, retrieved 2026-11-03.
- [Streamlit line charts](https://docs.streamlit.io/develop/api-reference/charts/st.line_chart), retrieved 2026-11-03.
