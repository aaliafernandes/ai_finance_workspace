# Lab 14 — Portfolio Baselines

## Scope and inputs

This is an educational exercise using course-authored training values, not market estimates or personalized investment advice. The expected-return objective is CPI + 4.0%; CPI is a labelled 2.5% estimate, so the comparison objective is 6.5% annually.

## Why diversification can reduce risk

Two risky assets can be less risky together than either asset alone when they do not move in perfect lockstep. The covariance term includes correlation: when correlation is below +1, the assets' moves partly offset each other, reducing the weighted portfolio variance.

For the 40% IG bond / 60% equity benchmark, using the handout inputs:

```
variance = (0.40² × 0.06²) + (0.60² × 0.16²)
           + (2 × 0.40 × 0.60 × 0.25 × 0.06 × 0.16)
         = 0.010944
volatility = √0.010944 = 0.1046 = 10.46%
```

The 0.25 correlation, rather than +1.00, is why the combined risk is lower than a simple perfectly-correlated combination would imply.

## Engine

The reusable standard-library-only engine is [portfolio.py](portfolio.py). It validates that every correlation is within -1 to +1 and that the table is symmetric before it builds covariance values as `correlation × volatility × volatility`.

Run from this folder:

```powershell
..\..\.tools\python-3.13.15\python.exe portfolio.py
```

Each calculation has its own function: input validation, covariance construction, each weighting scheme, expected return, portfolio volatility, reserve-eligible weight, and printing.

## Known-answer verification

| Portfolio | Weights: bills / 10-year / IG / equity | Return | Volatility | Reserve-eligible | Meets 6.5%? |
|---|---|---:|---:|---:|---|
| Benchmark | 0.0 / 0.0 / 40.0 / 60.0 | 6.80% | 10.46% | 0.0% | yes |
| Equal weight | 25.0 / 25.0 / 25.0 / 25.0 | 5.20% | 5.21% | 50.0% | no |
| Inverse volatility | 84.3 / 6.0 / 7.0 / 2.6 | 3.77% | 1.05% | 90.3% | no |

The benchmark meets the return objective but fails the Lab 13 reserve requirement because it has 0.0% in reserve-eligible bills or Treasury notes. Candidate E was added to the Lab 13 checker to prove this.

## Required tests

### Correlation sensitivity

I changed the IG bond fund/equity correlation from 0.25 to 0.50 in both mirrored cells, reran the program, and obtained a 11.00% benchmark volatility. I restored both values to 0.25.

### Invalid-input refusal

I changed the IG bond fund/equity correlation to 1.3. The program refused to run with a message that the correlation was outside -1 to 1. I restored the course input.

### Mandate check

Candidate E in [Lab 13 mandate.py](../Lab-13-Meridian/mandate.py) is the 40% IG bond fund / 60% global equity index fund benchmark. It produces a 0.0% reserve-eligible weight and fails the 3.0% reserve rule. The client benchmark therefore is not itself a mandate-compliant portfolio.

## Explain the code and self-quiz

The volatility function multiplies every pair of portfolio weights by the matching covariance and adds the results. It then takes the square root because the sum is variance, measured in squared return units. A partner question I could answer from the code: the double loop is necessary because covariance includes both diagonal asset-variance terms and cross-asset covariance terms.

Question: Why does inverse volatility assign so much to bills?

My answer: its 0.5% volatility makes `1 ÷ volatility` much larger than the corresponding values for the other sleeves. Scaling those inverse-volatility values to 100% therefore gives bills about 84.3%, even though this approach does not target the 6.5% return objective.

## Reflection

I would show the CIO the benchmark first because it directly connects to S4 and is the only baseline that reaches the stated 6.5% expected-return objective. I would immediately show its 0.0% reserve-eligible weight beside it, because the comparison reveals that a stated benchmark can conflict with a hard liquidity constraint. The equal-weight and inverse-volatility baselines are useful contrasts: equal weight reduces concentration, while inverse volatility strongly prioritizes low-risk bills and falls well short of the return objective.
