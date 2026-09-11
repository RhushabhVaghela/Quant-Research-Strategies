"""
    Title: Rebalancing Using the Kelly Criteria
    Description: A Kelly portfolio is created by assigning the weights to
    two assets. The Kelly weights are calculated monthly from the asset
    returns.
    Dataset: US Equities

    ############################# DISCLAIMER #############################
    This is a strategy template only and should not be
    used for live trading without appropriate backtesting and tweaking of
    the strategy parameters.
    ######################################################################
"""

# Import libraries
import numpy as np
from scipy.optimize import minimize

# Import blueshift libraries
from blueshift.api import (
                            symbol,
                            symbols,
                            order_target_percent,
                            schedule_function,
                            date_rules,
                            time_rules,
                            get_datetime
                        )


def initialize(context):
    # Define Symbols
    context.security_list = ['AAPL', 'MSFT']

    # The lookback for the historical data
    context.lookback = 90

    # Define the weights
    context.rounded_weights = None

    # Schedule the calculate_kelly_weights function
    schedule_function(
                        calculate_kelly_weights,
                        date_rule=date_rules.month_start(),
                        time_rule=time_rules.market_close(minutes=30)
                     )

    # Schedule the rebalance function
    schedule_function(
                        rebalance,
                        date_rule=date_rules.every_day(),
                        time_rule=time_rules.market_close(minutes=5)
                     )
                     
# Function to calculate the kelly_weights
def calculate_kelly_weights(context, data):
    """
        A function to calculate the Kelly weights using SciPy's minimize function.
    """
    try:
        # Fetch lookback no. days data for the first security
        df = data.history(
            symbols(context.security_list),
            'close',
            context.lookback,
            '1d')
    except IndexError:
        return

    # Get percentage change for the stock data
    df_change = df.pct_change()

    # Drop the first row containing NaN values
    df_change.dropna(inplace=True)

    no_of_stocks = df_change.shape[1]

    # Objective function: We want to maximize log of portfolio return
    # scipy minimizes, so we'll define the negative log-return
    def neg_kelly_criterion(weights):
        portfolio_returns = np.dot(df_change.values, weights)
        log_returns = np.log(1 + portfolio_returns)
        return -np.sum(log_returns)  # Negative to minimize it

    # Constraints: sum of weights = 1, no short selling (weights >= 0)
    constraints = ({
        'type': 'eq', 'fun': lambda weights: np.sum(weights) - 1  # Weights sum to 1
    })

    bounds = [(0, 1) for _ in range(no_of_stocks)]  # No short selling: weights between 0 and 1

    # Initial guess for weights (equal allocation)
    initial_weights = np.ones(no_of_stocks) / no_of_stocks

    # Use SciPy's minimize function
    result = minimize(neg_kelly_criterion, initial_weights, bounds=bounds, constraints=constraints)

    # If optimization is successful, assign the rounded weights
    if result.success:
        context.rounded_weights = [round(weight, 2) for weight in result.x]
    else:
        # In case of an error, set equal weights
        context.rounded_weights = [1/no_of_stocks] * no_of_stocks

def rebalance(context, data):
    """
        A function to rebalance the portfolio. This function is called by the
        schedule_function in the initialize function above.
    """

    # Calculate the weights if not present
    if context.rounded_weights is None:
        calculate_kelly_weights(context, data)

    # Rebalancing the portfolio
    for i in range(len(context.security_list)):
        order_target_percent(symbol(context.security_list[i]),
                             context.rounded_weights[i])
    print("{} Security weights: {}".format(get_datetime(), context.rounded_weights))