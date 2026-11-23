# Locked Changed-Input Prediction — Project 2

**Date:** November 23, 2026
**Experiment:** Historical estimation-window sensitivity

## 1. Experiment Details

- **Original input:** All 59 approved monthly returns.
- **Changed input:** Most recent 36 approved monthly returns.
- **Metric:** Annualized sample volatility (%) of the constrained minimum-volatility portfolio.
- **Original volatility:** 8.70%.

## 2. My Prediction

I predict that the constrained portfolio's annualized volatility will decrease slightly to **8.15%** when the estimation window is shortened from 59 to 36 monthly returns.

## 3. My Reasoning

The full 59-month window likely captures earlier market shocks or rate-hike periods that have since stabilized, meaning the most recent 36 months may reflect a calmer market environment. Because those earlier 23 months are removed from the estimation window, some extreme monthly returns could fall out of the sample, bringing the annualized volatility slightly below the original 8.70%.

This is my expectation, not a verified result.

## 4. How This Affects My Decision

If the volatility changes significantly when the historical window is shortened, I would be less confident in how stable the strategy is. I would want to test it further before recommending it to the investment committee.

Even if the volatility decreases as predicted, the strategy would still need to satisfy its other mandate requirements before being considered ready for investment.

## 5. Prediction Record and AI Use

I selected the numerical prediction of 8.15% before running or viewing the changed-input experiment. I used AI assistance to organize and format this record, so I am not claiming that the entire document was prepared without AI assistance.

## 6. Experiment Status

**NOT YET EXECUTED**

This prediction must be committed and pushed to GitHub before the changed-input experiment is run.
