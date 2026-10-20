"""Simple five-year discounted cash flow (DCF) model.

All dollar amounts are in USD millions unless noted otherwise.
This educational example is not investment advice.
"""

import sys


# -------------------- Editable inputs --------------------
# Apple Inc. inputs. Starting FCFF and WACC remain labelled training placeholders;
# see Lab-05-DCF-Apple.md for sources, estimates, and limitations.
starting_fcff = 100.0
yearly_growth_rates = [0.06, 0.05, 0.04, 0.03, 0.03]
wacc = 0.10
terminal_growth = 0.03
non_operating_cash = 35934.0
debt = 98657.0
diluted_shares = 15004.697

# Sensitivity and reverse-DCF controls.  Rates are decimals: 0.09 means 9%.
wacc_sensitivity_values = [0.09, 0.10, 0.11]
terminal_growth_sensitivity_values = [0.02, 0.03, 0.04]
target_share_price = 315.34
reverse_shift_lower_bound = -0.05
reverse_shift_upper_bound = 0.10
# ---------------------------------------------------------


def calculate_dcf(growth_rates, discount_rate, perpetual_growth_rate):
    """Return the DCF outputs used by the base case, grid, and reverse DCF."""
    if perpetual_growth_rate >= discount_rate:
        raise ValueError("terminal growth must be less than WACC for the Gordon-growth formula.")

    fcff_by_year = []
    fcff = starting_fcff
    for growth_rate in growth_rates:
        fcff *= 1 + growth_rate
        fcff_by_year.append(fcff)

    present_values = [
        cash_flow / (1 + discount_rate) ** year
        for year, cash_flow in enumerate(fcff_by_year, start=1)
    ]
    pv_explicit_fcff = sum(present_values)
    terminal_value_year_5 = fcff_by_year[-1] * (1 + perpetual_growth_rate) / (
        discount_rate - perpetual_growth_rate
    )
    pv_terminal_value = terminal_value_year_5 / (1 + discount_rate) ** 5
    enterprise_value = pv_explicit_fcff + pv_terminal_value
    equity_value = enterprise_value + non_operating_cash - debt
    value_per_diluted_share = equity_value / diluted_shares
    pv_terminal_value_share = pv_terminal_value / enterprise_value
    return {
        "fcff_by_year": fcff_by_year,
        "pv_explicit_fcff": pv_explicit_fcff,
        "terminal_value_year_5": terminal_value_year_5,
        "pv_terminal_value": pv_terminal_value,
        "enterprise_value": enterprise_value,
        "equity_value": equity_value,
        "value_per_diluted_share": value_per_diluted_share,
        "pv_terminal_value_share": pv_terminal_value_share,
    }


def value_with_uniform_growth_shift(shift):
    """Value the company after adding one shift to all explicit growth rates."""
    shifted_growth_rates = [rate + shift for rate in yearly_growth_rates]
    if any(rate <= -1.0 for rate in shifted_growth_rates):
        raise ValueError("a shifted annual growth rate would be -100% or below")
    return calculate_dcf(shifted_growth_rates, wacc, terminal_growth)["value_per_diluted_share"]


def solve_uniform_growth_shift(target, lower_bound, upper_bound, tolerance=1e-8, max_iterations=200):
    """Use bisection; return None when the target is not bracketed."""
    if lower_bound >= upper_bound:
        raise ValueError("reverse-DCF lower bound must be below the upper bound")

    lower_value = value_with_uniform_growth_shift(lower_bound)
    upper_value = value_with_uniform_growth_shift(upper_bound)
    if not min(lower_value, upper_value) <= target <= max(lower_value, upper_value):
        return None

    for _ in range(max_iterations):
        midpoint = (lower_bound + upper_bound) / 2
        midpoint_value = value_with_uniform_growth_shift(midpoint)
        if abs(midpoint_value - target) < tolerance:
            return midpoint
        if midpoint_value < target:
            lower_bound = midpoint
        else:
            upper_bound = midpoint
    return (lower_bound + upper_bound) / 2


try:
    base_case = calculate_dcf(yearly_growth_rates, wacc, terminal_growth)
except ValueError as error:
    sys.exit(f"Error: {error}")

fcff_by_year = base_case["fcff_by_year"]
pv_explicit_fcff = base_case["pv_explicit_fcff"]
terminal_value_year_5 = base_case["terminal_value_year_5"]
pv_terminal_value = base_case["pv_terminal_value"]
enterprise_value = base_case["enterprise_value"]
equity_value = base_case["equity_value"]
value_per_diluted_share = base_case["value_per_diluted_share"]
pv_terminal_value_share = base_case["pv_terminal_value_share"]

for year, cash_flow in enumerate(fcff_by_year, start=1):
    print(f"FCFF Year {year}: {cash_flow:.4f}")

print(f"Present value of five explicit FCFF: {pv_explicit_fcff:.4f}")
print(f"Terminal value at Year 5: {terminal_value_year_5:.4f}")
print(f"Present value of terminal value: {pv_terminal_value:.4f}")
print(f"Enterprise value: {enterprise_value:.4f}")
print(f"Equity value: {equity_value:.4f}")
print(f"Value per diluted share: {value_per_diluted_share:.4f}")
print(f"PV terminal value as share of enterprise value: {pv_terminal_value_share:.4f}")

print("\nSensitivity grid: value per diluted share ($)")
header = "WACC \\ terminal growth".ljust(24) + "".join(
    f"{growth:.0%}".rjust(10) for growth in terminal_growth_sensitivity_values
)
print(header)
for sensitivity_wacc in wacc_sensitivity_values:
    row = f"{sensitivity_wacc:.0%}".ljust(24)
    for sensitivity_growth in terminal_growth_sensitivity_values:
        if sensitivity_growth >= sensitivity_wacc:
            cell = "invalid"
        else:
            cell = f"{calculate_dcf(yearly_growth_rates, sensitivity_wacc, sensitivity_growth)['value_per_diluted_share']:.2f}"
        row += cell.rjust(10)
    print(row)

print("\nReverse DCF: uniform shift to all five explicit growth rates")
try:
    solved_shift = solve_uniform_growth_shift(
        target_share_price, reverse_shift_lower_bound, reverse_shift_upper_bound
    )
except ValueError as error:
    sys.exit(f"Reverse DCF error: {error}")

if solved_shift is None:
    print(
        f"No solution for target price ${target_share_price:.2f} within "
        f"{reverse_shift_lower_bound:+.2%} to {reverse_shift_upper_bound:+.2%}."
    )
else:
    print(f"Solved uniform growth-rate shift: {solved_shift:+.2%}")
    print(f"Target share price: ${target_share_price:.2f}")
print(
    "Held fixed: starting FCFF, WACC, terminal growth, cash, debt, diluted shares, "
    "and the enterprise-to-equity bridge."
)
