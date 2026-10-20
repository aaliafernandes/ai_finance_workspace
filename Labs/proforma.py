"""Five-year three-statement pro-forma for the ABG training case.

All amounts are USD millions unless stated otherwise.  This is an educational
model, not investment advice.  The inputs below come from Lab 09.
"""

# ---------- Assumptions ----------
YEARS = [2026, 2027, 2028, 2029, 2030]
ORGANIC_REVENUE_GROWTH = 0.018
GROSS_MARGIN = 0.1705
SGA_TO_GROSS_PROFIT = [0.665, 0.655, 0.645, 0.645, 0.645]
DEPRECIATION_TO_OPENING_PPE = 82.4 / 3070.4
IMPAIRMENT = 120.0
CAPEX = 250.0
TAX_RATE = 0.255
INVENTORY_DAYS = 2135.8 / (17999.0 - 3071.7) * 365
FLOOR_PLAN_TO_INVENTORY = 2027.0 / 2135.8
OTHER_WORKING_CAPITAL_RATE = 0.008
MINIMUM_CASH = 25.0
REVOLVER_LIMIT = 850.0
REVOLVER_RATE = 0.06
DEBT_REPAYMENT = 150.0
SHARE_BUYBACK = 150.0
FLOOR_PLAN_RATE = 0.0467
TERM_DEBT_RATE = 0.0544
COST_OF_EQUITY = 0.10
TERMINAL_GROWTH = 0.025
SHARES_OUTSTANDING = 17.951349

# ---------- FY2025 opening balance sheet ----------
opening = {
    "revenue": 17999.0,
    "inventory": 2135.8,
    "ppe": 3070.4,
    "other_assets": 6371.6,
    "cash": 40.4,
    "floor_plan": 2027.0,
    "term_debt": 3572.0,
    "revolver": 0.0,
    "other_liabilities": 2127.5,
    "equity": 3891.7,
}


def assert_balanced(year, statement, tolerance=1e-6):
    """Raise an informative error when the balance sheet or cash floor fails."""
    assets = statement["inventory"] + statement["ppe"] + statement["other_assets"] + statement["cash"]
    liabilities_and_equity = (
        statement["floor_plan"]
        + statement["term_debt"]
        + statement["revolver"]
        + statement["other_liabilities"]
        + statement["equity"]
    )
    gap = assets - liabilities_and_equity
    if abs(gap) > tolerance:
        raise ValueError(f"FY{year}E is not balanced: assets minus liabilities minus equity = {gap:.1f}")
    if statement["cash"] < MINIMUM_CASH - tolerance:
        raise ValueError(f"FY{year}E cash is below the minimum: {statement['cash']:.1f}")


def project_year(year_index, prior):
    """Project one year in the sequence required by the lab instruction."""
    revenue = prior["revenue"] * (1 + ORGANIC_REVENUE_GROWTH)
    gross_profit = revenue * GROSS_MARGIN
    sga = gross_profit * SGA_TO_GROSS_PROFIT[year_index]
    depreciation = prior["ppe"] * DEPRECIATION_TO_OPENING_PPE
    operating_income = gross_profit - sga - depreciation - IMPAIRMENT
    interest = (
        prior["floor_plan"] * FLOOR_PLAN_RATE
        + prior["term_debt"] * TERM_DEBT_RATE
        + prior["revolver"] * REVOLVER_RATE
    )
    pretax_income = operating_income - interest
    tax = max(0.0, pretax_income) * TAX_RATE
    net_income = pretax_income - tax

    inventory = (revenue - gross_profit) * INVENTORY_DAYS / 365
    floor_plan = inventory * FLOOR_PLAN_TO_INVENTORY
    ppe = prior["ppe"] + CAPEX - depreciation
    change_in_revenue = revenue - prior["revenue"]
    change_in_other_working_capital = OTHER_WORKING_CAPITAL_RATE * change_in_revenue
    other_assets = prior["other_assets"] + change_in_other_working_capital - IMPAIRMENT
    term_debt = prior["term_debt"] - DEBT_REPAYMENT
    other_liabilities = prior["other_liabilities"]
    equity = prior["equity"] + net_income - SHARE_BUYBACK

    fcfe = (
        net_income
        + depreciation
        + IMPAIRMENT
        - CAPEX
        - (inventory - prior["inventory"])
        - change_in_other_working_capital
        + (floor_plan - prior["floor_plan"])
        - DEBT_REPAYMENT
    )
    cash = prior["cash"] + fcfe - SHARE_BUYBACK
    revolver = prior["revolver"]

    # Borrow only to reach the cash floor; use excess cash to repay first.
    if cash < MINIMUM_CASH:
        draw = MINIMUM_CASH - cash
        if revolver + draw > REVOLVER_LIMIT:
            raise ValueError(f"FY{YEARS[year_index]}E revolver exceeds its {REVOLVER_LIMIT:.1f} limit")
        revolver += draw
        cash += draw
    elif revolver > 0.0:
        revolver_repayment = min(revolver, cash - MINIMUM_CASH)
        revolver -= revolver_repayment
        cash -= revolver_repayment

    return {
        "revenue": revenue,
        "gross_profit": gross_profit,
        "sga": sga,
        "depreciation": depreciation,
        "impairment": IMPAIRMENT,
        "operating_income": operating_income,
        "interest": interest,
        "pretax_income": pretax_income,
        "tax": tax,
        "net_income": net_income,
        "inventory": inventory,
        "ppe": ppe,
        "other_assets": other_assets,
        "cash": cash,
        "floor_plan": floor_plan,
        "term_debt": term_debt,
        "revolver": revolver,
        "other_liabilities": other_liabilities,
        "equity": equity,
        "change_in_inventory": inventory - prior["inventory"],
        "change_in_other_working_capital": change_in_other_working_capital,
        "change_in_floor_plan": floor_plan - prior["floor_plan"],
        "capex": CAPEX,
        "debt_repayment": DEBT_REPAYMENT,
        "share_buyback": SHARE_BUYBACK,
        "fcfe": fcfe,
    }


def print_table(title, rows, projections):
    print(f"\n{title}")
    print(f"{'Line':<38}" + "".join(f"FY{year}E".rjust(12) for year in YEARS))
    for label, key in rows:
        print(f"{label:<38}" + "".join(f"{year[key]:>12.1f}" for year in projections))


projections = []
prior = opening
for index, year in enumerate(YEARS):
    current = project_year(index, prior)
    assert_balanced(year, current)
    projections.append(current)
    prior = current

print_table(
    "Income Statement (USD millions)",
    [
        ("Revenue", "revenue"), ("Gross profit", "gross_profit"), ("SG&A", "sga"),
        ("Depreciation", "depreciation"), ("Impairment", "impairment"),
        ("Operating income", "operating_income"), ("Interest", "interest"),
        ("Pretax income", "pretax_income"), ("Tax", "tax"), ("Net income", "net_income"),
    ],
    projections,
)
print_table(
    "Balance Sheet (USD millions)",
    [
        ("Inventory", "inventory"), ("PP&E, net", "ppe"), ("Other assets", "other_assets"),
        ("Cash", "cash"), ("Floor-plan debt", "floor_plan"), ("Term debt", "term_debt"),
        ("Revolver", "revolver"), ("Other liabilities", "other_liabilities"), ("Equity", "equity"),
    ],
    projections,
)
print_table(
    "Cash Flow / FCFE (USD millions)",
    [
        ("Net income", "net_income"), ("Depreciation", "depreciation"), ("Impairment", "impairment"),
        ("Capital spending", "capex"), ("Change in inventory", "change_in_inventory"),
        ("Change in other working capital", "change_in_other_working_capital"),
        ("Change in floor-plan debt", "change_in_floor_plan"), ("Debt repayment", "debt_repayment"),
        ("Share buyback", "share_buyback"), ("Free cash flow to equity", "fcfe"),
    ],
    projections,
)

print("\nChecks")
print(f"{'Line':<38}" + "".join(f"FY{year}E".rjust(12) for year in YEARS))
for label, values in [
    ("Assets - liabilities - equity", [
        p["inventory"] + p["ppe"] + p["other_assets"] + p["cash"]
        - p["floor_plan"] - p["term_debt"] - p["revolver"] - p["other_liabilities"] - p["equity"]
        for p in projections
    ]),
    ("Cash at or above minimum", [p["cash"] - MINIMUM_CASH for p in projections]),
]:
    print(f"{label:<38}" + "".join(f"{value:>12.1f}" for value in values))

present_value_fcfe = sum(
    projection["fcfe"] / (1 + COST_OF_EQUITY) ** year_number
    for year_number, projection in enumerate(projections, start=1)
)
terminal_fcfe = projections[-1]["fcfe"] + projections[-1]["debt_repayment"]
terminal_value_2030 = terminal_fcfe * (1 + TERMINAL_GROWTH) / (COST_OF_EQUITY - TERMINAL_GROWTH)
present_value_terminal = terminal_value_2030 / (1 + COST_OF_EQUITY) ** 5
equity_value = present_value_fcfe + present_value_terminal

print("\nEquity Valuation (USD millions, except per-share amount)")
print(f"Equity value: {equity_value:.1f}")
print(f"Share of value after 2030: {present_value_terminal / equity_value:.1%}")
print(f"Value per share: ${equity_value / SHARES_OUTSTANDING:.2f}")
