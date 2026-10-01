"""Lab 05 FCFF DCF training-case validation.

All amounts are USD millions except per-share value. This model uses only the
standard library and intentionally retains the Lab 05 training inputs.
"""

starting_fcff = 100.0
yearly_growth_rates = [0.08, 0.06, 0.05, 0.04, 0.03]
wacc = 0.10
terminal_growth = 0.03
non_operating_cash = 50.0
debt = 300.0
diluted_shares = 50.0


def calculate_dcf():
    """Calculate the required five-year FCFF DCF outputs."""
    if terminal_growth >= wacc:
        raise ValueError("Terminal growth must be less than WACC.")

    fcff_by_year = []
    fcff = starting_fcff
    for growth_rate in yearly_growth_rates:
        fcff *= 1 + growth_rate
        fcff_by_year.append(fcff)

    pv_explicit_fcff = sum(
        fcff / (1 + wacc) ** year
        for year, fcff in enumerate(fcff_by_year, start=1)
    )
    terminal_value_year_5 = fcff_by_year[-1] * (1 + terminal_growth) / (wacc - terminal_growth)
    pv_terminal_value = terminal_value_year_5 / (1 + wacc) ** 5
    enterprise_value = pv_explicit_fcff + pv_terminal_value
    equity_value = enterprise_value + non_operating_cash - debt
    value_per_share = equity_value / diluted_shares
    terminal_value_share = pv_terminal_value / enterprise_value
    return (
        fcff_by_year,
        pv_explicit_fcff,
        terminal_value_year_5,
        pv_terminal_value,
        enterprise_value,
        equity_value,
        value_per_share,
        terminal_value_share,
    )


def main():
    try:
        (
            fcff_by_year,
            pv_explicit_fcff,
            terminal_value_year_5,
            pv_terminal_value,
            enterprise_value,
            equity_value,
            value_per_share,
            terminal_value_share,
        ) = calculate_dcf()
    except ValueError as error:
        print(f"Error: {error}")
        return

    for year, fcff in enumerate(fcff_by_year, start=1):
        print(f"FCFF Year {year}: {fcff:.4f}")
    print(f"Present value of five explicit FCFF: {pv_explicit_fcff:.4f}")
    print(f"Terminal value at Year 5: {terminal_value_year_5:.4f}")
    print(f"Present value of terminal value: {pv_terminal_value:.4f}")
    print(f"Enterprise value: {enterprise_value:.4f}")
    print(f"Equity value: {equity_value:.4f}")
    print(f"Value per diluted share: {value_per_share:.4f}")
    print(f"PV terminal value as share of enterprise value: {terminal_value_share:.4f}")


if __name__ == "__main__":
    main()
