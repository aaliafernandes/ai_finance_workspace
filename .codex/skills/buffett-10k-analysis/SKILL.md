---
name: buffett-10k-analysis
description: Analyze a US public company from its last five annual 10-K SEC EDGAR facts using Buffett-style quality checks; use when the user gives a ticker and wants reproducible financial evidence before qualitative judgment.
---

# Buffett 10-K analysis

Use this skill for an educational, five-year business-quality review. It is not
investment advice and it does not use market-price data.

1. Set `SEC_USER_AGENT` to your name and email, then run
   `python scripts/edgar_10k_facts.py TICKER --json outputs/TICKER.json`.
   The script is the sole source of all numbers. Do not calculate, round, add,
   or infer financial values yourself.
2. Read the generated table and checks. Preserve `not found` and `not known`
   exactly; they mean the evidence is insufficient, not zero.
3. Write `outputs/TICKER_memo.md` using only numbers and tags printed by the
   script. Make a concise Buffett-style business-quality judgment: **own the
   business**, **watch it**, or **pass**. Judge the business, not its share
   price. State any check that is not known and do not fill its gap.
4. Include a one-line trust decision below the memo, explaining whether the
   verdict is warranted by the five-year evidence.

The code determines facts, calculations, and pass/not-known checks. The model
may only judge qualitative matters such as durability of a moat, management,
predictability, and the limits of the available evidence.
