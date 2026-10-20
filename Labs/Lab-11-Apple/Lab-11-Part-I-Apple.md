# Lab 11 — Part I: Apple Sensitivity Analysis

**Company:** Apple Inc. (AAPL)  
**Purpose:** Educational finance coursework only; not personalized investment advice.

## Added model and method

The sensitivity model is [apple_proforma_sensitivity.py](apple_proforma_sensitivity.py).
It keeps an immutable base input set and uses a fresh deep copy for every
lower, base, and higher run. The only changed input in a given set of runs is
the selected driver from Part R.

The model links forecast revenue to operating profit and then to an **FCFF
proxy**:

1. Revenue = prior-year revenue × (1 + revenue-growth assumption).
2. Operating profit = forecast revenue × operating-margin assumption.
3. FCFF proxy = operating profit × historical conversion factor.

The conversion factor is $98,767 million divided by $133,050 million. The
$98,767 million amount is FY2025 operating cash flow of $111,482 million less
capital spending of $12,715 million. It is a proxy—not fully defined FCFF—because
Apple’s cash-interest-paid add-back is unresolved in the existing DCF record.

## Inputs and outputs

The driver paths are exactly the Part R paths; no ranges were added or changed.

| Driver | Lower | Base | Higher | Unit |
|---|---|---|---|---|
| Total revenue growth, Years 1–5 | 4%, 3%, 2%, 1%, 1% | 6%, 5%, 4%, 3%, 3% | 8%, 7%, 6%, 5%, 5% | Percent of prior-year revenue |
| Operating margin, Years 1–5 | 30% each year | 32% each year | 34% each year | Percent of revenue |

Each run reports final-year operating profit and final-year FCFF proxy in USD
millions. Value per diluted share is **unavailable** because the existing
Apple DCF identifies both starting FCFF and WACC as unresolved placeholders.
No terminal value was invented.

## Run instruction and current execution status

The standard course command was attempted first:

```powershell
python Lab-11-Apple/apple_proforma_sensitivity.py
```

It could not run because Python is not available on PATH:

```text
python : The term 'python' is not recognized as the name of a cmdlet, function, script file, or operable program.
```

The model was then run successfully from the terminal using a portable Python
copy stored inside this workspace:

```powershell
& '.tools\python-3.13.15\python.exe' 'Lab-11-Apple\apple_proforma_sensitivity.py'
```

## Actual sensitivity results

All runs passed their revenue-to-operating-profit and operating-profit-to-FCFF-
proxy calculation checks. Amounts are USD millions; signed changes are relative
to the base case for the same driver.

### Revenue-growth sensitivity (operating margin held at 32%)

| Case | Revenue-growth path | Final-year operating profit | Change from base | Final-year FCFF proxy | Change from base | Value per share |
|---|---|---:|---:|---:|---:|---|
| Lower | 4%, 3%, 2%, 1%, 1% | 148,431.1 | (15,105.3) | 110,184.8 | (11,213.1) | Unavailable |
| Base | 6%, 5%, 4%, 3%, 3% | 163,536.4 | 0.0 | 121,397.9 | 0.0 | Unavailable |
| Higher | 8%, 7%, 6%, 5%, 5% | 179,847.1 | +16,310.7 | 133,505.9 | +12,107.9 | Unavailable |
| **Span** | — | **31,416.0** | — | **23,321.0** | — | Unavailable |

### Operating-margin sensitivity (revenue growth held at base)

| Case | Operating-margin path | Final-year operating profit | Change from base | Final-year FCFF proxy | Change from base | Value per share |
|---|---|---:|---:|---:|---:|---|
| Lower | 30%, 30%, 30%, 30%, 30% | 153,315.3 | (10,221.0) | 113,810.6 | (7,587.4) | Unavailable |
| Base | 32%, 32%, 32%, 32%, 32% | 163,536.4 | 0.0 | 121,397.9 | 0.0 | Unavailable |
| Higher | 34%, 34%, 34%, 34%, 34% | 173,757.4 | +10,221.0 | 128,985.3 | +7,587.4 | Unavailable |
| **Span** | — | **20,442.0** | — | **15,174.7** | — | Unavailable |

The initial base run and restored base run both report final-year operating
profit of $163,536.4 million and final-year FCFF proxy of $121,397.9 million.
The script printed: `Restored-base check: PASS`.

## Source and limitation

Source: Apple Inc. FY2025 Form 10-K, filed October 31, 2025, accessed
September 24, 2026. The historical values used above are documented in
`Lab-05-DCF-Apple.md` and `Apple proforma.md` with their Form 10-K locators.
The forecast inputs are the labeled judgment ranges selected in Part R.

## Lab 11 progress count

| Item | Status |
|---|---|
| D — question and Partner Exchange 1 | Complete |
| R — inputs, ranges, locked prediction, and pre-run confirmation | Complete |
| I — analysis code, terminal run, results, and restored-base check | Complete |
| V — own-result verification and partner check | Complete |
| E — identify the driver, reflection, and partner summary | Complete |

**Completed: 5 of 5 Lab 11 sections.**
