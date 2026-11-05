# Graham panel skill

Use only the printed five annual 10-K rows. Do not estimate a missing input.

Checks implemented in `app.py`:

1. Latest current ratio (AssetsCurrent / LiabilitiesCurrent) is at least 2.0.
2. Net income is positive in every reported year.
3. Net income grew from the first reported year to the last.

Output a short memo using only printed values. A missing value remains `not
found` or `not known`; it does not become a pass. The default threshold is 2.0.
The app exposes a 1.0-to-2.0 threshold probe but records 2.0 as the retained
rule, matching the Lab 19 instruction.

Source: [Ben Graham FAskills page](https://github.com/CinderZhang/FAskills/blob/main/financial-researcher/experts/ben_graham.md), retrieved 2026-11-05.
