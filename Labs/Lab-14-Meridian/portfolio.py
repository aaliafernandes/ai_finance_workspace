"""Portfolio baseline calculations for the fictional Meridian Foundation Reserve.

Course-authored training inputs only. This calculates expected return and risk;
it is not a forecast or personalized investment advice.
"""

from math import sqrt

# Editable inputs: returns and volatilities are decimal annual rates.
SLEEVES = {
    "Treasury bills": {"expected_return": 0.035, "volatility": 0.005},
    "Treasury 10-year note": {"expected_return": 0.043, "volatility": 0.070},
    "Investment-grade bond fund": {"expected_return": 0.050, "volatility": 0.060},
    "Global equity index fund": {"expected_return": 0.080, "volatility": 0.160},
}

CORRELATIONS = {
    "Treasury bills": {"Treasury bills": 1.00, "Treasury 10-year note": 0.10,
                       "Investment-grade bond fund": 0.05, "Global equity index fund": 0.00},
    "Treasury 10-year note": {"Treasury bills": 0.10, "Treasury 10-year note": 1.00,
                               "Investment-grade bond fund": 0.80, "Global equity index fund": -0.10},
    "Investment-grade bond fund": {"Treasury bills": 0.05, "Treasury 10-year note": 0.80,
                                    "Investment-grade bond fund": 1.00, "Global equity index fund": 0.25},
    "Global equity index fund": {"Treasury bills": 0.00, "Treasury 10-year note": -0.10,
                                  "Investment-grade bond fund": 0.25, "Global equity index fund": 1.00},
}

OBJECTIVE_RETURN = 0.065  # CPI estimate of 2.5% + 4.0%, annual
RESERVE_ELIGIBLE = {"Treasury bills", "Treasury 10-year note"}


def validate_correlations(sleeves, correlations):
    """Refuse invalid or non-symmetric correlation inputs before calculation."""
    names = list(sleeves)
    for left in names:
        if left not in correlations:
            raise ValueError(f"Correlation table is missing row: {left}")
        for right in names:
            if right not in correlations[left]:
                raise ValueError(f"Correlation table is missing {left}/{right}")
            value = correlations[left][right]
            if not -1 <= value <= 1:
                raise ValueError(f"Correlation {left}/{right} is outside -1 to 1: {value}")
            if abs(value - correlations.get(right, {}).get(left, float("inf"))) > 1e-12:
                raise ValueError(f"Correlation table is not symmetric at {left}/{right}")


def build_covariance_matrix(sleeves, correlations):
    """Return covariance[i][j] = correlation[i][j] * volatility[i] * volatility[j]."""
    return {
        left: {
            right: correlations[left][right] * sleeves[left]["volatility"] * sleeves[right]["volatility"]
            for right in sleeves
        }
        for left in sleeves
    }


def equal_weight_portfolio(sleeves):
    """Assign an equal decimal weight to every sleeve."""
    return {name: 1 / len(sleeves) for name in sleeves}


def inverse_volatility_portfolio(sleeves):
    """Scale 1 / volatility weights so they sum to one."""
    inverse_volatilities = {name: 1 / data["volatility"] for name, data in sleeves.items()}
    total = sum(inverse_volatilities.values())
    return {name: inverse_volatilities[name] / total for name in sleeves}


def expected_return(weights, sleeves):
    """Calculate the weighted expected return."""
    return sum(weights[name] * sleeves[name]["expected_return"] for name in sleeves)


def portfolio_volatility(weights, covariance_matrix):
    """Calculate sqrt(sum_i(sum_j(w_i * covariance_i,j * w_j)))."""
    variance = sum(
        weights[left] * covariance_matrix[left][right] * weights[right]
        for left in weights
        for right in weights
    )
    return sqrt(variance)


def reserve_eligible_weight(weights):
    """Return the decimal portfolio weight in Meridian reserve-eligible sleeves."""
    return sum(weights[name] for name in RESERVE_ELIGIBLE)


def print_portfolio(name, weights, sleeves, covariance_matrix, objective_return):
    """Print a baseline's calculated weights and mandate-relevant measures."""
    weight_text = " / ".join(f"{weights[sleeve] * 100:.1f}" for sleeve in sleeves)
    result_return = expected_return(weights, sleeves)
    result_volatility = portfolio_volatility(weights, covariance_matrix)
    reserve_weight = reserve_eligible_weight(weights)
    meets_objective = "yes" if result_return >= objective_return else "no"
    print(f"\n{name}")
    print(f"Weights (bills / 10-year / IG / equity): {weight_text}%")
    print(f"Expected return: {result_return * 100:.2f}%")
    print(f"Volatility: {result_volatility * 100:.2f}%")
    print(f"Reserve-eligible weight: {reserve_weight * 100:.1f}%")
    print(f"Meets {objective_return * 100:.1f}% objective? {meets_objective}")


def main():
    try:
        validate_correlations(SLEEVES, CORRELATIONS)
    except ValueError as error:
        print(f"Refusing to run: {error}")
        return

    covariance_matrix = build_covariance_matrix(SLEEVES, CORRELATIONS)
    portfolios = {
        "Benchmark": {"Treasury bills": 0, "Treasury 10-year note": 0,
                      "Investment-grade bond fund": 0.40, "Global equity index fund": 0.60},
        "Equal weight": equal_weight_portfolio(SLEEVES),
        "Inverse volatility": inverse_volatility_portfolio(SLEEVES),
    }
    for name, weights in portfolios.items():
        print_portfolio(name, weights, SLEEVES, covariance_matrix, OBJECTIVE_RETURN)


if __name__ == "__main__":
    main()
