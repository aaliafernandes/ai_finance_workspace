"""Streamlit learning demonstration for the Meridian portfolio-stability lab."""

from copy import deepcopy

import streamlit as st

from portfolio import (
    CORRELATIONS,
    RESERVE_ELIGIBLE,
    SLEEVES,
    estimate_from_prices_csv,
    find_lowest_risk_mix,
)


st.set_page_config(page_title="Portfolio Stability Decision", layout="wide")
st.title("Portfolio Stability Decision")
st.caption("Built with AI help, a learning demonstration, not investment advice.")


def show_mix(title, mix, sleeves):
    """Display one search result in a compact, readable form."""
    st.subheader(title)
    if mix is None:
        st.warning("No mix meets the objective.")
        return
    st.dataframe(
        {
            "Asset": list(sleeves),
            "Weight": [f"{mix['weights'][name] * 100:.0f}%" for name in sleeves],
        },
        hide_index=True,
        use_container_width=True,
    )
    first, second, third = st.columns(3)
    first.metric("Expected return", f"{mix['expected_return'] * 100:.2f}%")
    second.metric("Volatility", f"{mix['volatility'] * 100:.2f}%")
    third.metric("Reserve-eligible", f"{mix['reserve_eligible_weight'] * 100:.0f}%")


with st.sidebar:
    st.header("Mandate controls")
    objective = st.number_input("Objective expected return (%)", value=6.5, step=0.1) / 100
    reserve_minimum = st.number_input("Minimum reserve-eligible weight (%)", value=3.0, step=1.0) / 100
    uploaded_prices = st.file_uploader("Upload monthly prices.csv", type="csv")
    last_36_months = st.toggle("Use only the last 36 monthly returns")

try:
    if uploaded_prices is None:
        loaded_sleeves = deepcopy(SLEEVES)
        loaded_correlations = deepcopy(CORRELATIONS)
        active_sleeves = deepcopy(SLEEVES)
        active_correlations = deepcopy(CORRELATIONS)
        source_label = "Meridian training inputs"
    else:
        loaded_sleeves, loaded_correlations = estimate_from_prices_csv(uploaded_prices)
        if last_36_months:
            active_sleeves, active_correlations = estimate_from_prices_csv(uploaded_prices, last_36_months=True)
        else:
            active_sleeves, active_correlations = deepcopy(loaded_sleeves), deepcopy(loaded_correlations)
        source_label = "Uploaded CSV: historical estimates, not forecasts"
except ValueError as error:
    st.error(f"Could not estimate inputs from the CSV: {error}")
    st.stop()

st.write(source_label)
st.subheader("Expected-return estimates")
st.caption("Edit an estimate to test stability. Historical CSV estimates are not forecasts.")
edited_sleeves = deepcopy(active_sleeves)
return_columns = st.columns(len(active_sleeves))
for column, name in zip(return_columns, active_sleeves):
    with column:
        edited_sleeves[name]["expected_return"] = (
            st.number_input(
                name,
                value=float(active_sleeves[name]["expected_return"] * 100),
                step=0.1,
                key=f"return_{name}",
            )
            / 100
        )

st.subheader("Reserve eligibility")
reserve_columns = st.columns(len(active_sleeves))
reserve_eligible = set()
for column, name in zip(reserve_columns, active_sleeves):
    with column:
        if st.checkbox(name, value=name in RESERVE_ELIGIBLE, key=f"reserve_{name}"):
            reserve_eligible.add(name)

loaded_mix = find_lowest_risk_mix(
    loaded_sleeves, loaded_correlations, objective, reserve_eligible, reserve_minimum
)
edited_mix = find_lowest_risk_mix(
    edited_sleeves, active_correlations, objective, reserve_eligible, reserve_minimum
)

current_title = "Current answer" if not last_36_months else "Current answer: last 36 months"
left, right = st.columns(2)
with left:
    show_mix(current_title, edited_mix, edited_sleeves)
with right:
    show_mix("Answer for inputs as loaded (all months)", loaded_mix, loaded_sleeves)

if loaded_mix is not None and edited_mix is not None:
    largest_change = max(
        abs(edited_mix["weights"][name] - loaded_mix["weights"][name]) for name in edited_sleeves
    )
    st.info(f"Largest weight change: {largest_change * 100:.0f} points.")

st.divider()
st.caption(
    "Method: every long-only mix in 5-point weight increments is tested; the app selects the feasible mix with "
    "the lowest annualized volatility. Returns and risk from uploaded data are historical estimates."
)
