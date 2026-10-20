# Lab 07 — Comparable-Company Policy and Implied Range: Asbury

Educational valuation exercise only; this is not personalized investment advice.

## Reopen and explain

My Week 3 model is an Apple discounted cash flow (DCF) model, run with
`python dcf.py`. Its value range is driven mainly by starting free cash flow to
the firm (FCFF), the five annual growth assumptions, WACC, terminal growth,
and the cash/debt/share-count bridge from enterprise value to equity value.
The model currently has a material limitation: its starting FCFF and WACC are
labelled training placeholders, so its resulting per-share value is not a
reliable Apple conclusion.

Question investigated: *What would a target company's share be worth if its
earnings were valued at the P/E multiples used by comparable companies?*

## P/E in plain language

Price-to-earnings (P/E) is share price divided by earnings per share (EPS).
Price per share is the market price of one common share. Diluted EPS is annual
GAAP profit attributable to common shareholders divided by the diluted
weighted-average shares; it reflects potentially dilutive shares. A P/E of 10x
means investors are valuing each $1 of annual earnings at $10 of share price.

Comparing P/E lets companies of different sizes be compared on a per-dollar of
earnings basis. It provides a market-based cross-check on a DCF: instead of
forecasting cash flows and discounting them, it asks how the market priced
similar companies' reported earnings. It does not replace the DCF because the
multiple embeds market expectations and may be distorted by accounting results
or temporary market prices.

A lower P/E does **not** automatically make an investment better. It could
reflect weaker expected growth, more leverage or risk, declining earnings, or
an unusual earnings period. P/E is most useful when firms have comparable
operations, earnings quality, growth prospects, risk, capital structure, and
accounting. It is misleading with negative EPS (the usual P/E is not
meaningful), unusual one-time profit/losses, or materially different growth and
business mix.

## Peer policy before seeing the result

| Company | Decision | Business rationale |
|---|---|---|
| AutoNation (AN) | Use | It is a large franchised vehicle retailer with dealership operations and recurring service/parts activity, which aligns with the core economics being compared. |
| Group 1 Automotive (GPI) | Qualify / use | It also operates franchised dealerships and service/parts businesses, so it is relevant. It is qualified because its geographic footprint, brand mix, acquisition activity, and other business mix can differ from Asbury and affect its multiple. |

Franchised vehicle retail and service/parts matter more than a broad “auto”
label because they determine revenue sources, margins, cyclicality, and the
recurring earnings that P/E is comparing. Neither peer decision is based on
which result produces a preferred price.

## Reproduced frozen case calculation

The calculator is [lab_07_asbury_pe.py](lab_07_asbury_pe.py). Run it with:

```powershell
python lab_07_asbury_pe.py
```

It uses the frozen case inputs below and retains full precision in calculations;
it only rounds display values.

| Company / role | December 31, 2024 close | FY2024 GAAP diluted EPS | P/E |
|---|---:|---:|---:|
| Asbury Automotive (ABG), target | $243.03 | $21.50 | Target, not included as a peer |
| AutoNation (AN), peer | $169.84 | $16.92 | 10.037825x |
| Group 1 Automotive (GPI), qualified peer | $421.48 | $36.81 | 11.450149x |

The two-peer median is 10.743987x. Applying the minimum, median, and maximum
peer multiples to Asbury's $21.50 diluted EPS gives a peer-implied range of
**$215.81 to $246.18** and a median-implied price of **$231.00**.

## Changed-peer result and interpretation

Before checking the output, I predicted that removing Group 1 would lower the
implied value because Group 1 has the higher P/E. The leave-one-out calculation
confirms this: removing GPI leaves AutoNation's 10.037825x P/E and an implied
Asbury reference estimate of **$215.81**, a **−$15.18** change from the
full-peer median estimate. With only one usable peer there is no observed
minimum-to-maximum peer range; it is a single reference estimate, not a range.

This comparison does not prove that Asbury is fairly valued. It is a
retrospective, point-in-time comparison using year-end prices paired with
subsequently reported annual GAAP EPS. Differences in expected growth, risk,
earnings quality, leverage, and business mix can justify different P/E values.
No cash/debt bridge is used in this equity P/E method.

## Sources and reproducibility

- Frozen inputs and expected checks: Lab 07 assignment handout, “Comparable-Company Policy and Implied Range,” provided in class and accessed September 24, 2026; the handout identifies `teach-comps-worked-example.md` as the case source and definition record.
- Method: P/E = closing price / FY2024 total GAAP diluted EPS; implied price = peer P/E × Asbury FY2024 diluted EPS. Inputs are stored at the top of the Python file, with no downloaded data or external packages.
