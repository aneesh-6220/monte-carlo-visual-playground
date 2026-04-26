"""Summary metrics for Monte Carlo simulation results."""

import numpy as np


def calculate_summary_metrics(paths, starting_value):
    """Calculate useful summary statistics from simulated paths."""
    final_values = paths.iloc[-1]

    probability_below_start = np.mean(final_values < starting_value)

    return {
        "mean_final_value": final_values.mean(),
        "median_final_value": final_values.median(),
        "percentile_5": np.percentile(final_values, 5),
        "percentile_95": np.percentile(final_values, 95),
        "probability_below_starting_value": probability_below_start,
        "best_final_value": final_values.max(),
        "worst_final_value": final_values.min(),
    }
