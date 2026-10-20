# Lab 09 — Five-Year Pro Forma: Asbury Automotive Group

Educational finance coursework only; this is not personalized investment advice.

## Submission and reproducibility

This written record accompanies [proforma.py](proforma.py). Run the model with
the Python command required by the course environment:

```powershell
python proforma.py
```

All amounts are USD millions except the final per-share amount. The script uses
the ABG training-case assumptions coded at the top of the file and produces
FY2026E through FY2030E income-statement, balance-sheet, cash-flow/FCFE, and
equity-valuation tables.

## Method in plain language

A pro forma is a five-year set of forecast financial statements built from a
consistent set of operating and financing assumptions. Revenue is forecast from
organic growth. Gross profit, selling/general/administrative expense,
depreciation, impairment, interest, tax, working capital, capital spending,
debt repayment, and share repurchases are then reflected in the statements.

Free cash flow to equity (FCFE) is the cash available to common shareholders
after operating needs, capital spending, working-capital changes, and net debt
financing. The script discounts forecast FCFE at the cost of equity and adds a
terminal value based on terminal FCFE growth to estimate an educational
per-share equity value.

## Assumptions and model checks

The model uses the following training-case assumptions: 1.8% annual organic
revenue growth; a 17.05% gross margin; declining SG&A as a percentage of gross
profit; $250 million annual capital spending; a 25.5% tax rate; $150 million
annual term-debt repayment; $150 million annual share buybacks; a 6% revolver
rate; a 10% cost of equity; and 2.5% terminal growth.

Inventory is tied to cost of sales using historical inventory days, and
floor-plan debt is tied to inventory. The model maintains at least $25 million
of cash and draws its revolver only when necessary, up to its $850 million
limit. For each projected year, the script checks that assets equal liabilities
plus equity and that cash does not fall below the required minimum.

## Interpretation and limitations

The output is a scenario based on class training inputs, not a forecast of what
ABG will actually earn or a recommendation to buy or sell its shares. Results
are particularly sensitive to organic revenue growth, gross margin, working
capital/inventory needs, the debt and repurchase policy, the cost of equity, and
the terminal-growth assumption. The terminal value can represent a substantial
part of a five-year valuation, so the per-share result should not be used
without sensitivity analysis and comparison with the course case materials.

## Source and transformation record

Source: Lab 09 ABG training-case inputs provided in class, accessed September
24, 2026. Transformations are fully documented in `proforma.py`: historical
ratios are calculated once from the FY2025 opening balance sheet, then applied
sequentially to the FY2026E–FY2030E forecasts. No external data are downloaded
by the script.
