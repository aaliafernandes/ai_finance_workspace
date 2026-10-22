"""Portfolio baseline calculations for the fictional Meridian Foundation Reserve.

Course-authored training inputs only. This calculates expected return and risk;
it is not a forecast or personalized investment advice.
"""

import csv
from math import sqrt
from pathlib import Path

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


def find_lowest_risk_mix(
    sleeves,
    correlations,
    objective_return,
    reserve_eligible,
    minimum_reserve,
    step=0.05,
):
    """Return the lowest-volatility long-only mix meeting both constraints.

    Every weight is an integer multiple of ``step`` and all weights add to one.
    Returns ``None`` when the requested objective and reserve minimum cannot be
    met by any of those mixes.
    """
    if not 0 < step <= 1:
        raise ValueError("step must be greater than zero and no more than one")
    steps = round(1 / step)
    if abs(steps * step - 1) > 1e-9:
        raise ValueError("step must divide one exactly")
    if not 0 <= minimum_reserve <= 1:
        raise ValueError("minimum_reserve must be between zero and one")

    validate_correlations(sleeves, correlations)
    names = list(sleeves)
    covariance_matrix = build_covariance_matrix(sleeves, correlations)
    best = None

    def evaluate(counts):
        nonlocal best
        weights = {name: count * step for name, count in zip(names, counts)}
        result_return = expected_return(weights, sleeves)
        reserve_weight = sum(weights[name] for name in reserve_eligible)
        if result_return + 1e-12 < objective_return or reserve_weight + 1e-12 < minimum_reserve:
            return
        result_volatility = portfolio_volatility(weights, covariance_matrix)
        if best is None or result_volatility < best["volatility"] - 1e-12:
            best = {
                "weights": weights,
                "expected_return": result_return,
                "volatility": result_volatility,
                "reserve_eligible_weight": reserve_weight,
            }

    def build_counts(index, remaining, counts):
        if index == len(names) - 1:
            evaluate(counts + [remaining])
            return
        for count in range(remaining + 1):
            build_counts(index + 1, remaining - count, counts + [count])

    build_counts(0, steps, [])
    return best


def estimate_from_prices_csv(csv_source, last_36_months=False):
    """Estimate annualized inputs from monthly adjusted-close prices in a CSV.

    The CSV must have a date column first (oldest date first) and one positive
    price column per ticker. Arithmetic monthly means and sample standard
    deviations are annualized. These are historical estimates, not forecasts.
    """
    if hasattr(csv_source, "getvalue"):
        text = csv_source.getvalue().decode("utf-8-sig")
        rows = list(csv.DictReader(text.splitlines()))
    else:
        with Path(csv_source).open(newline="", encoding="utf-8-sig") as file:
            rows = list(csv.DictReader(file))

    if not rows or not rows[0]:
        raise ValueError("prices CSV has no data rows")
    columns = list(rows[0])
    if len(columns) < 4:
        raise ValueError("prices CSV needs a date column and at least three ticker columns")
    tickers = columns[1:]
    try:
        prices = {ticker: [float(row[ticker]) for row in rows] for ticker in tickers}
    except (KeyError, TypeError, ValueError) as error:
        raise ValueError("every price cell must contain a number") from error
    if any(price <= 0 for values in prices.values() for price in values):
        raise ValueError("all prices must be greater than zero")
    if len(rows) < 3:
        raise ValueError("prices CSV needs at least three monthly prices")

    monthly_returns = {
        ticker: [current / previous - 1 for previous, current in zip(values, values[1:])]
        for ticker, values in prices.items()
    }
    if last_36_months:
        monthly_returns = {ticker: values[-36:] for ticker, values in monthly_returns.items()}
    observations = len(next(iter(monthly_returns.values())))
    if observations < 2:
        raise ValueError("at least two monthly returns are required")

    means = {ticker: sum(values) / observations for ticker, values in monthly_returns.items()}
    standard_deviations = {
        ticker: sqrt(sum((value - means[ticker]) ** 2 for value in values) / (observations - 1))
        for ticker, values in monthly_returns.items()
    }
    if any(value == 0 for value in standard_deviations.values()):
        raise ValueError("each ticker needs more than one distinct monthly return")

    sleeves = {
        ticker: {
            "expected_return": means[ticker] * 12,
            "volatility": standard_deviations[ticker] * sqrt(12),
        }
        for ticker in tickers
    }
    correlations = {
        left: {
            right: (
                1.0
                if left == right
                else sum(
                    (left_value - means[left]) * (right_value - means[right])
                    for left_value, right_value in zip(monthly_returns[left], monthly_returns[right])
                )
                / ((observations - 1) * standard_deviations[left] * standard_deviations[right])
            )
            for right in tickers
        }
        for left in tickers
    }
    return sleeves, correlations


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
