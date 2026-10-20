# Lab 05 — FCFF DCF Training-Case Validation

Educational finance coursework only; not investment advice.

## Deliverable

The reproducible Lab 05 model is [lab_05_dcf_training.py](lab_05_dcf_training.py).
It uses only the Python standard library and keeps the required training inputs
separate from the Apple inputs used in Lab 06.

Run it with the working Python command on the course computer, for example:

```powershell
python lab_05_dcf_training.py
```

## Training inputs

| Input | Value |
|---|---:|
| Starting FCFF | $100.0 million |
| Growth, Years 1–5 | 8%, 6%, 5%, 4%, 3% |
| WACC | 10% |
| Terminal growth | 3% |
| Cash / debt / diluted shares | $50.0m / $300.0m / 50.0m |

The model forecasts FCFF at each year-end, calculates terminal value at the
end of Year 5 using the Gordon-growth formula, discounts that terminal value
five years, then bridges enterprise value to equity value using cash less debt.
It stops with an error if terminal growth is at or above WACC.

## Required known-answer validation

The model is designed to reproduce the published Lab 05 values to four
decimals:

| Output | Expected value |
|---|---:|
| FCFF, Years 1–5 | 108.0000; 114.4800; 120.2040; 125.0122; 128.7625 |
| PV of explicit FCFF | 448.4408 |
| Terminal value at Year 5 | 1,894.6486 |
| PV of terminal value | 1,176.4277 |
| Enterprise value | 1,624.8685 |
| Equity value | 1,374.8685 |
| Value per diluted share | $27.4974 |
| PV terminal value / enterprise value | 72.40% |

The terminal value is discounted five years—not six—because it is measured at
the end of Year 5. Increasing WACC to 11%, while holding the other training
inputs fixed, lowers the value per diluted share to approximately $23.41. This
is consistent with the financial logic: a higher discount rate reduces the
present value of future cash flows.

## Reverse DCF in plain language

A reverse DCF starts with a market price and solves backwards for an assumption
that would make the model equal that price. It does not prove the market is
right or wrong; it describes one conditional set of assumptions. The separate
Lab 06 Apple model implements this as a uniform change to the five explicit
growth rates while holding the remaining inputs fixed.

Source: FIN 43900 Lab 05 — Build and Validate an FCFF DCF, class GitHub,
retrieved September 24, 2026.
