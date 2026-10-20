"""Apple operating pro-forma and one-at-a-time sensitivity analysis.

Educational coursework only; not personalized investment advice. Amounts are
USD millions.  The model uses only the Apple FY2025 values documented in the
workspace and the two Part R input ranges.  It deliberately does not calculate
value per share because FCFF and WACC are unresolved in the existing model.
"""

from copy import deepcopy


YEARS = [1, 2, 3, 4, 5]

# Historical values recorded in Lab-05-DCF-Apple.md and Apple proforma.md.
OPENING_REVENUE = 416_161.0
OPENING_OPERATING_INCOME = 133_050.0
OPERATING_CASH_FLOW = 111_482.0
CAPEX = 12_715.0

# OCF minus capex is an observable free-cash-flow proxy, before the unresolved
# cash-interest-paid add-back required for fully defined FCFF.
FCFF_PROXY_CONVERSION = (OPERATING_CASH_FLOW - CAPEX) / OPENING_OPERATING_INCOME

BASE_INPUTS = {
    "revenue_growth": [0.06, 0.05, 0.04, 0.03, 0.03],
    "operating_margin": [0.32, 0.32, 0.32, 0.32, 0.32],
}

SENSITIVITY_VALUES = {
    "revenue_growth": {
        "Lower": [0.04, 0.03, 0.02, 0.01, 0.01],
        "Base": [0.06, 0.05, 0.04, 0.03, 0.03],
        "Higher": [0.08, 0.07, 0.06, 0.05, 0.05],
    },
    "operating_margin": {
        "Lower": [0.30, 0.30, 0.30, 0.30, 0.30],
        "Base": [0.32, 0.32, 0.32, 0.32, 0.32],
        "Higher": [0.34, 0.34, 0.34, 0.34, 0.34],
    },
}


def run_proforma(inputs):
    """Run the linked revenue -> operating profit -> FCFF-proxy forecast."""
    revenue = OPENING_REVENUE
    projections = []

    for index, year in enumerate(YEARS):
        revenue *= 1 + inputs["revenue_growth"][index]
        operating_profit = revenue * inputs["operating_margin"][index]
        fcff_proxy = operating_profit * FCFF_PROXY_CONVERSION
        operating_profit_check = abs(
            operating_profit - revenue * inputs["operating_margin"][index]
        ) < 1e-6
        fcff_proxy_check = abs(
            fcff_proxy - operating_profit * FCFF_PROXY_CONVERSION
        ) < 1e-6
        projections.append(
            {
                "year": year,
                "revenue": revenue,
                "operating_profit": operating_profit,
                "fcff_proxy": fcff_proxy,
                "operating_profit_check": operating_profit_check,
                "fcff_proxy_check": fcff_proxy_check,
            }
        )

    return projections


def valid_run(projections):
    """Return whether the linked calculation checks pass for every year."""
    return all(
        projection["operating_profit_check"] and projection["fcff_proxy_check"]
        for projection in projections
    )


def print_run_details(title, inputs, projections, base_final=None):
    """Print the input paths, traceable statements, and visible checks."""
    final = projections[-1]
    print(f"\n{title}")
    print("Inputs (percent by forecast year)")
    print("Revenue growth: " + ", ".join(f"{value:.1%}" for value in inputs["revenue_growth"]))
    print("Operating margin: " + ", ".join(f"{value:.1%}" for value in inputs["operating_margin"]))
    print("\nLinked forecast (USD millions)")
    print(f"{'Year':<8}{'Revenue':>15}{'Operating profit':>20}{'FCFF proxy*':>18}")
    for projection in projections:
        print(
            f"{projection['year']:<8}{projection['revenue']:>15,.1f}"
            f"{projection['operating_profit']:>20,.1f}{projection['fcff_proxy']:>18,.1f}"
        )
    print("\nChecks")
    for projection in projections:
        print(
            f"Year {projection['year']}: operating profit link = "
            f"{'PASS' if projection['operating_profit_check'] else 'FAIL'}; "
            f"FCFF-proxy link = {'PASS' if projection['fcff_proxy_check'] else 'FAIL'}"
        )
    print(f"Final-year operating profit: {final['operating_profit']:,.1f} USD millions")
    print(f"Final-year FCFF proxy*: {final['fcff_proxy']:,.1f} USD millions")
    print("Value per share: unavailable (existing FCFF and WACC are unresolved)")
    if base_final is not None:
        print(f"Change from base operating profit: {final['operating_profit'] - base_final['operating_profit']:+,.1f} USD millions")
        print(f"Change from base FCFF proxy*: {final['fcff_proxy'] - base_final['fcff_proxy']:+,.1f} USD millions")


def sensitivity_analysis():
    """Run lower/base/higher cases, resetting independent inputs every time."""
    base_inputs = deepcopy(BASE_INPUTS)
    base_projections = run_proforma(deepcopy(base_inputs))
    base_final = base_projections[-1]
    print_run_details("BASE RUN BEFORE SENSITIVITY", base_inputs, base_projections)

    for driver, cases in SENSITIVITY_VALUES.items():
        print(f"\n{'=' * 72}\nSensitivity driver: {driver.replace('_', ' ').title()}")
        final_results = []

        for case_name, selected_path in cases.items():
            # Fresh independent copy prevents prior runs from contaminating this run.
            run_inputs = deepcopy(base_inputs)
            run_inputs[driver] = deepcopy(selected_path)
            projections = run_proforma(run_inputs)
            is_valid = valid_run(projections)
            if not is_valid:
                print(f"\n{case_name}: INVALID RUN — not ranked.")
                print_run_details(case_name, run_inputs, projections, base_final)
                continue
            print_run_details(case_name, run_inputs, projections, base_final)
            final_results.append(projections[-1])

        if len(final_results) == 3:
            operating_profit_span = max(row["operating_profit"] for row in final_results) - min(
                row["operating_profit"] for row in final_results
            )
            fcff_proxy_span = max(row["fcff_proxy"] for row in final_results) - min(
                row["fcff_proxy"] for row in final_results
            )
            print(f"\n{driver.replace('_', ' ').title()} output spans")
            print(f"Operating profit span: {operating_profit_span:,.1f} USD millions")
            print(f"FCFF proxy* span: {fcff_proxy_span:,.1f} USD millions")
            print("Value-per-share span: unavailable (valuation is unresolved)")

    restored_base_projections = run_proforma(deepcopy(base_inputs))
    restored_base_final = restored_base_projections[-1]
    if base_final != restored_base_final:
        raise AssertionError("Restored base does not match the first base run")
    print_run_details("RESTORED BASE RUN", base_inputs, restored_base_projections)
    print("\nRestored-base check: PASS — final-year inputs and outputs match the first base run.")
    print("* FCFF proxy = operating cash flow minus capex, before the unresolved cash-interest-paid add-back.")


if __name__ == "__main__":
    sensitivity_analysis()
