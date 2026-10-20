# Lab 06 — Sensitivity, Reverse DCF, and Conditional Recommendation: Apple

Educational finance coursework only; not investment advice.

## Reproducible company model

The Lab 06 company model is [dcf.py](dcf.py). It contains Apple’s five-year
FCFF forecast, the required WACC/terminal-growth grid, and the reverse-DCF
search. The inputs, sources, calculations, reasonableness check, grid, and
interpretation are documented in [Lab-05-DCF-Apple.md](Lab-05-DCF-Apple.md),
which is retained as the underlying Apple input record.

Run the model with:

```powershell
python dcf.py
```

## Required Lab 06 checks

| Requirement | Where it is shown |
|---|---|
| Five company input rows, units, as-of dates, and locators | `Lab-05-DCF-Apple.md` — “Required inputs and evidence” |
| Unresolved or estimated inputs labelled | Starting FCFF and WACC are explicitly labelled placeholders; growth and terminal growth are labelled estimates |
| Company per-share value compared with price | “Reasonableness (V)” |
| WACC / terminal-growth sensitivity grid | “Sensitivity grid and reverse DCF (E)” |
| Reverse DCF, solved variable, and held-fixed inputs | “Reverse DCF” section and `dcf.py` output |
| Conditional call and monitor | Below |

## Conditional call

**Watch — defer initiation.** I would reconsider only after Apple’s starting
FCFF is rebuilt on a consistent USD-million basis and WACC is estimated from
dated, sourced inputs. I will monitor reported operating cash flow, capital
spending, and Services growth because they affect the FCFF forecast and whether
the current placeholder-based DCF becomes usable.

## Limitation

The result is not a defensible Apple fair-value estimate yet. The model uses a
$100 million FCFF training placeholder while Apple’s reported operating cash
flow is much larger. This scale mismatch causes the negative per-share output,
so it is documented rather than adjusted to match the market price.

Sources retrieved September 10, 2026: Apple FY2025 Form 10-K and market-price
source links recorded in `Lab-05-DCF-Apple.md`. Lab requirements: FIN 43900
Lab 06, class GitHub, retrieved September 24, 2026.
