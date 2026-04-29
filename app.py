"""Streamlit app for the Monte Carlo Visual Playground."""

import matplotlib.pyplot as plt
import streamlit as st

from src.metrics import calculate_summary_metrics
from src.simulation import simulate_investment_paths

st.markdown("""
<style>
.footer {
    margin-top: 2rem;
    text-align: center;
    color: #6B7280;
    font-size: 0.85rem;
}
.footer a {
    color: #2563EB;
    text-decoration: none;
}
.footer a:hover {
    text-decoration: underline;
}
</style>
""", unsafe_allow_html=True)


DEFAULT_STARTING_VALUE = 10_000
DEFAULT_EXPECTED_RETURN = 7
DEFAULT_VOLATILITY = 15
DEFAULT_YEARS = 10
DEFAULT_SIMULATIONS = 1_000
DEFAULT_RANDOM_SEED = 42
MAX_SAMPLE_PATHS = 50


def validate_inputs(starting_value, annual_volatility, years, simulations):
    """Return a list of validation error messages."""
    errors = []

    if starting_value <= 0:
        errors.append("Starting value must be greater than 0.")

    if annual_volatility < 0:
        errors.append("Annual volatility cannot be negative.")

    if years <= 0:
        errors.append("Number of years must be positive.")

    if simulations > 10_000:
        errors.append("Number of simulations cannot exceed 10,000.")

    return errors


def format_money(value):
    """Format a number as dollars for easier reading."""
    return f"${value:,.2f}"


def plot_sample_paths(paths, max_paths):
    """Create a matplotlib chart showing a sample of simulated paths."""
    sample_paths = paths.iloc[:, :max_paths]

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(sample_paths.index, sample_paths, linewidth=1, alpha=0.55)
    ax.set_title("Sample Simulated Investment Paths")
    ax.set_xlabel("Year")
    ax.set_ylabel("Portfolio Value")
    ax.grid(True, alpha=0.25)

    return fig


def plot_final_value_histogram(final_values, starting_value):
    """Create a matplotlib histogram of final simulated values."""
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.hist(final_values, bins=40, color="#4C78A8", edgecolor="white")
    ax.axvline(
        starting_value,
        color="#D62728",
        linestyle="--",
        linewidth=2,
        label="Starting value",
    )
    ax.set_title("Distribution of Final Values")
    ax.set_xlabel("Final Portfolio Value")
    ax.set_ylabel("Number of Simulations")
    ax.grid(True, axis="y", alpha=0.25)
    ax.legend()

    return fig

def show_footer():
    st.markdown(
        """
        <div class="footer">
            Educational simulation tool · Not financial advice · 
            <a href="https://github.com/aneesh-6220/monte-carlo-visual-playground" target="_blank">
                Source code
            </a>
        </div>
        """,
        unsafe_allow_html=True,
    )


st.set_page_config(
    page_title="Monte Carlo Visual Playground",
    page_icon=":chart_with_upwards_trend:",
    layout="wide",
)

st.title("Monte Carlo Visual Playground")
st.write(
    "Explore how randomness, return, and volatility can create many possible "
    "investment outcomes from the same starting assumptions."
)

with st.sidebar:
    st.header("Simulation Settings")

    starting_value = st.number_input(
        "Starting value ($)",
        min_value=1.0,
        value=float(DEFAULT_STARTING_VALUE),
        step=500.0,
    )

    expected_return_percent = st.slider(
        "Expected annual return",
        min_value=-20,
        max_value=30,
        value=DEFAULT_EXPECTED_RETURN,
        format="%d%%",
    )

    volatility_percent = st.slider(
        "Annual volatility",
        min_value=0,
        max_value=80,
        value=DEFAULT_VOLATILITY,
        format="%d%%",
    )

    years = st.slider(
        "Number of years",
        min_value=1,
        max_value=50,
        value=DEFAULT_YEARS,
    )

    simulations = st.slider(
        "Number of simulations",
        min_value=100,
        max_value=10_000,
        value=DEFAULT_SIMULATIONS,
        step=100,
    )

    random_seed = st.number_input(
        "Random seed",
        min_value=0,
        value=DEFAULT_RANDOM_SEED,
        step=1,
    )

annual_return = expected_return_percent / 100
annual_volatility = volatility_percent / 100

validation_errors = validate_inputs(
    starting_value=starting_value,
    annual_volatility=annual_volatility,
    years=years,
    simulations=simulations,
)

if validation_errors:
    for error in validation_errors:
        st.error(error)
    st.stop()

paths = simulate_investment_paths(
    starting_value=starting_value,
    expected_annual_return=annual_return,
    annual_volatility=annual_volatility,
    years=years,
    simulations=simulations,
    random_seed=random_seed,
)

metrics = calculate_summary_metrics(
    paths=paths,
    starting_value=starting_value,
)

st.subheader("Simulation Results")

metric_columns = st.columns(4)
metric_columns[0].metric("Mean final value", format_money(metrics["mean_final_value"]))
metric_columns[1].metric("Median final value", format_money(metrics["median_final_value"]))
metric_columns[2].metric("5th percentile", format_money(metrics["percentile_5"]))
metric_columns[3].metric("95th percentile", format_money(metrics["percentile_95"]))

metric_columns = st.columns(3)
metric_columns[0].metric(
    "Probability below start",
    f"{metrics['probability_below_starting_value']:.1%}",
)
metric_columns[1].metric("Best final value", format_money(metrics["best_final_value"]))
metric_columns[2].metric("Worst final value", format_money(metrics["worst_final_value"]))

st.caption(
    "This project is for educational purposes only and is not financial advice."
)

chart_column_1, chart_column_2 = st.columns(2)

with chart_column_1:
    paths_to_show = min(MAX_SAMPLE_PATHS, simulations)
    sample_paths_figure = plot_sample_paths(paths, paths_to_show)
    st.pyplot(sample_paths_figure)

with chart_column_2:
    final_values = paths.iloc[-1]
    histogram_figure = plot_final_value_histogram(final_values, starting_value)
    st.pyplot(histogram_figure)

with st.expander("What this simulation means", expanded=True):
    st.markdown(
        """
        **Monte Carlo simulation** means running the same model many times with
        random changes each time. Instead of giving one answer, it shows a range
        of possible outcomes.

        **Volatility** is a way to describe how much values can bounce around.
        Higher volatility usually means the paths spread out more. Some paths
        may end much higher, while others may end much lower.

        Different paths happen because each simulation receives different random
        monthly returns. The assumptions stay the same, but the random sequence
        of good and bad months changes.

        This is **not a prediction**. It does not know what the market will do.
        It is only a learning tool for thinking about uncertainty and risk.

        The **5th percentile** means about 5% of simulations ended below that
        value. The **95th percentile** means about 95% of simulations ended below
        that value. Together, they give a rough sense of a lower and upper range
        in the simulated outcomes.
        """
    )
show_footer()
