"""Simulation logic for Monte Carlo investment paths."""

import numpy as np
import pandas as pd


def simulate_investment_paths(
    starting_value,
    expected_annual_return,
    annual_volatility,
    years,
    simulations,
    random_seed=None,
):
    """Simulate investment paths using monthly random returns.

    Parameters
    ----------
    starting_value : float
        The initial portfolio value.
    expected_annual_return : float
        The expected yearly return written as a decimal. For example, 0.07
        means 7%.
    annual_volatility : float
        The yearly volatility written as a decimal. For example, 0.15 means 15%.
    years : int
        Number of years to simulate.
    simulations : int
        Number of random paths to create.
    random_seed : int or None
        Makes the random results repeatable when a number is provided.

    Returns
    -------
    pandas.DataFrame
        Rows are time steps in years. Columns are simulation paths.
    """
    months_per_year = 12
    total_months = years * months_per_year

    # Convert annual assumptions into monthly assumptions.
    monthly_expected_return = expected_annual_return / months_per_year
    monthly_volatility = annual_volatility / np.sqrt(months_per_year)

    random_generator = np.random.default_rng(random_seed)

    # Each random return is one possible monthly move for one simulation path.
    random_monthly_returns = random_generator.normal(
        loc=monthly_expected_return,
        scale=monthly_volatility,
        size=(total_months, simulations),
    )

    # Geometric growth means each month grows from the previous month's value.
    monthly_growth_factors = 1 + random_monthly_returns
    cumulative_growth = np.cumprod(monthly_growth_factors, axis=0)

    simulated_values = starting_value * cumulative_growth

    # Add the starting value as the first row so every path begins together.
    starting_row = np.full((1, simulations), starting_value)
    simulated_values = np.vstack([starting_row, simulated_values])

    time_index = np.arange(total_months + 1) / months_per_year
    column_names = [f"Simulation {number + 1}" for number in range(simulations)]

    return pd.DataFrame(
        simulated_values,
        index=time_index,
        columns=column_names,
    )
