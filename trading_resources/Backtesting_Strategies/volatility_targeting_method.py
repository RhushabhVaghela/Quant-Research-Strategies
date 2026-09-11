"""
Title: Volatility Targeting
Description: In this method, we use the volatility of the underlying as the leverage
            for our position. This helps us smoothen strategy performance.
Dataset: US Equities
"""

# Import blueshift libraries
from blueshift.api import(symbol,
                        order_target_percent,
                        schedule_function,
                        date_rules,
                        time_rules,
                        get_datetime
                        )

# Import libraries
import numpy as np
import pandas as pd


def initialize(context):
    """
    A function to define things to do at the start of the strategy
    """

    # Select security
    context.security = symbol('AAPL')

    # Define lookback
    # It implies we read data for 990 candles back
    context.lookback = 990

    # Define volatility target
    context.volatility_target = 0.01

    # Define leverage cap
    context.leverage_cap = 2

    # Define window
    context.window = 20

    # Call strategy function every day, 5 minutes before close
    schedule_function(strategy,
                      date_rules.every_day(),
                      time_rules.market_close(minutes=5))


def run_vol_targeting(context, data):
    # Read historical data
    try:
        hist_data = data.history(
            context.security, ['close'], context.lookback, '1d')
    except IndexError:
        return

    # Calculate volatility
    hist_data['volatility'] = hist_data['close'].pct_change().rolling(
        context.window).std()
    hist_data.dropna(inplace=True)
    

    # Calculate leverage
    hist_data['leverage'] = context.volatility_target / \
        hist_data['volatility'].shift(1)
    hist_data['leverage'] = np.where(
        hist_data['leverage'] > context.leverage_cap, context.leverage_cap, hist_data['leverage'])
    hist_data.dropna(inplace=True)

    leverage = hist_data['leverage'].iloc[-1]
    
    return leverage


def strategy(context, data):
    """
    A function to rebalance the portfolio, passed on to the call
    of schedule_function above.
    """
    # Place order
    position = run_vol_targeting(context, data)
    if position is not None:
        print("{} Signal value {}".format(get_datetime(), position))
        order_target_percent(context.security, position)