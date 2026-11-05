# Burry panel skill

Use only the printed five annual 10-K rows. Do not estimate a missing input.

Checks implemented in `app.py`:

1. Operating cash flow is at least net income in every reported year.
2. Latest total liabilities divided by equity is no more than 2.0.

Output a short memo using only printed values. A missing value remains `not
found` or `not known`; it does not become a pass. This is a limited accounting
screen, not a substitute for Burry's broader filing and footnote review.

Source: [Michael Burry FAskills page](https://github.com/CinderZhang/FAskills/blob/main/financial-researcher/experts/michael_burry.md), retrieved 2026-11-05.
