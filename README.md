# Monte Carlo Visual Playground

A beginner-readable Streamlit app for exploring Monte Carlo simulation with random walks and simulated investment outcomes.

This project is for educational purposes only and is not financial advice.

## What the App Demonstrates

The app shows how one set of assumptions can lead to many possible outcomes. You can adjust the starting value, expected annual return, volatility, time period, number of simulations, and random seed.

It is not a trading tool, prediction engine, or investment recommendation. It is a learning project about randomness, uncertainty, volatility, and simulation.

## Screenshot

Add a screenshot here after running the app locally or deploying it.

Suggested image path:

```md
![App screenshot](screenshots/app-screenshot.png)
```

## Features

- Interactive Streamlit sidebar controls
- Monthly Monte Carlo simulation paths
- Sample path line chart
- Final value histogram
- Summary metrics for simulated outcomes
- Plain-English educational explanation
- Clean project structure for GitHub and Streamlit Community Cloud

## Tech Stack

- Python
- Streamlit
- NumPy
- Pandas
- Matplotlib

## How to Run Locally

1. Clone or download this repository.

2. Open a terminal in the project folder:

```bash
cd monte-carlo-visual-playground
```

3. Create a virtual environment:

```bash
python3 -m venv .venv
```

4. Activate the virtual environment:

```bash
source .venv/bin/activate
```

5. Install the required packages:

```bash
pip install -r requirements.txt
```

6. Run the Streamlit app:

```bash
streamlit run app.py
```

Streamlit will open the app in your browser. If it does not open automatically, copy the local URL from the terminal into your browser.

## How to Deploy on Streamlit Community Cloud

1. Push this project to a GitHub repository.
2. Go to [Streamlit Community Cloud](https://streamlit.io/cloud).
3. Sign in with GitHub.
4. Choose the repository for this project.
5. Set the main file path to:

```text
app.py
```

6. Deploy the app.

Streamlit Community Cloud will install the packages listed in `requirements.txt`.

## Simple Explanation of the Math

The app uses a simple geometric Brownian motion-style model. That means the investment value changes by a random percentage each month.

The expected annual return is divided into a monthly expected return. The annual volatility is converted into monthly volatility by dividing by the square root of 12.

For each month and each simulation, the app randomly generates a monthly return. It then multiplies the portfolio value by:

```text
1 + monthly_return
```

Repeating this process creates a path. Running many paths creates a distribution of possible outcomes.

## Limitations

- The model is simplified and does not predict real markets.
- It assumes returns are normally distributed.
- It does not include taxes, fees, inflation, deposits, withdrawals, or changing market conditions.
- Extreme assumptions can create unrealistic results.
- The results depend on the random seed and model assumptions.

## Future Improvements

- Add deposits or withdrawals over time
- Add inflation adjustment
- Compare multiple strategies
- Add downloadable results as a CSV file
- Add more charts for risk and drawdowns
- Add explanations for normal distributions and percentiles
