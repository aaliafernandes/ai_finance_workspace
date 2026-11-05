# Lab 19 - Legend Panel

> Educational coursework only; this is not investment advice.

## Question

When three investor skills read the same 10-K facts, where do they agree,
where do they split, and would I trust the panel?

## What was built

The existing Lab 18 Streamlit app now uses one five-year annual-10-K fact set
for Buffett, Graham, and Burry. The extraction script adds `Liabilities`,
`AssetsCurrent`, and `LiabilitiesCurrent`; it computes current ratio and
liabilities-to-equity in code. Each memo is generated only from values printed
in that fact set. The app presents the check table, three side-by-side memos,
and a number-audit flag for every memo.

The local Graham and Burry skill instructions are in this Lab 19 folder.

## Known answer: COST

| Investor | Check | Result |
| --- | --- | --- |
| Buffett | ROE of 15% or more every year | pass |
| Buffett | Owner earnings positive every year | pass |
| Buffett | Owner earnings grew, first year to last | pass |
| Graham | Current ratio of 2.0 or more, latest year | fail (1.06) |
| Graham | Net income positive every year | pass |
| Graham | Net income grew, first year to last | pass |
| Burry | Operating cash flow at least net income every year | pass |
| Burry | Liabilities no more than twice equity, latest year | pass (1.49) |

The default panel is therefore Buffett 3 of 3, Graham 2 of 3, and Burry 2 of 2.

### Threshold probe

Changing Graham's slider from 2.0 to 1.0 changes COST's 1.06 current-ratio
result from fail to pass. I retained **2.0** because it is the stated Graham
liquidity rule; the probe demonstrates that the screen result depends on the
chosen threshold.

## Project 2 company: NVDA

The Project 2 equity fund selected in prework is VT. Its largest disclosed
holding was NVIDIA Corp. (NVDA), 4.52% of fund assets as of September 30, 2026.
NVDA files annual 10-K reports, so no substitute holding was needed.

| Investor | Panel result | Evidence from the printed five-year data |
| --- | --- | --- |
| Buffett | 3 of 3 pass | ROE is above 15% each year; owner earnings rise from 8,132.0 to 96,676.0 USD millions. |
| Graham | 3 of 3 pass | Latest current ratio is 3.91; net income rises from 9,752.0 to 120,067.0 USD millions. |
| Burry | 1 of 2 pass | Operating cash flow is not at least net income in every year; latest liabilities-to-equity is 0.31. |

**Bull case:** Buffett and Graham agree that NVDA's five-year profitability,
growth, and latest balance-sheet liquidity clear their limited screens.

**Bear case:** Burry's cash-flow check fails in part of the five-year record,
so reported earnings were not always matched by operating cash flow. These
screens also do not value the shares or test whether AI demand, margins,
customer concentration, or competitive conditions can persist.

**Decision:** I would allow the panel to screen companies for Project 2 **only
with the condition** that every `not found`/`not known` result remains visible
and any passing name receives valuation and 10-K risk/footnote review.

## Reproduction and limitation

Run `streamlit run Labs/Lab-19/app.py`. For a fresh
EDGAR run, enter a personal SEC User-Agent in the app. The checked-in NVDA
fixture is labeled as an offline transcription because this workspace has no
configured SEC User-Agent and no Python command available; replace it by
running the script before submitting if possible.

## Sources (retrieved November 5, 2026)

- [SEC EDGAR API documentation](https://www.sec.gov/search-filings/edgar-application-programming-interfaces)
- [NVIDIA 2026 Form 10-K](https://www.sec.gov/Archives/edgar/data/1045810/000104581026000021/nvda-20260125.htm)
- [Vanguard VT holdings page](https://advisors.vanguard.com/investments/products/vt/vanguard-total-world-stock-etf)
- [Ben Graham FAskills page](https://github.com/CinderZhang/FAskills/blob/main/financial-researcher/experts/ben_graham.md)
- [Michael Burry FAskills page](https://github.com/CinderZhang/FAskills/blob/main/financial-researcher/experts/michael_burry.md)
- [Streamlit dataframe documentation](https://docs.streamlit.io/develop/api-reference/data/st.dataframe) and [columns documentation](https://docs.streamlit.io/develop/api-reference/layout/st.columns)
