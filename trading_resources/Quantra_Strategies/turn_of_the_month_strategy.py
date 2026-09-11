"""
    Title: Turn of the Month Strategy Template
    Description: The strategy buys the asset on the last day of a month and
    sells the asset on the first day of the next month. If the asset price
    is greater than the 200-day SMA then the strategy continues to hold the
    asset.
    Dataset: US Equities

    ############################# DISCLAIMER #############################
    This is a strategy template only and should not be
    used for live trading without appropriate backtesting and tweaking of
    the strategy parameters.
    ######################################################################
"""

# Import numpy
import numpy as np

# Import the blueshift libraries
from blueshift.api import (
                            symbol,
                            order_target_percent,
                            schedule_function,
                            date_rules,
                            time_rules,
                            get_datetime
                        )

def initialize(context):
    # Define the symbol
    context.security = symbol('AAPL')

    # Define the SMA window
    context.sma_window = 200

    # Schedule the place_sell_order function
    schedule_function(
                        place_sell_order,
                        date_rule=date_rules.month_start(),
                        time_rule=time_rules.market_close(minutes=5)
                     )

    # Schedule the place_buy_order function
    schedule_function(
                        place_buy_order,
                        date_rule=date_rules.month_end(),
                        time_rule=time_rules.market_close(minutes=5)
                     )


def place_buy_order(context, data):
    """
        A function to place the buy order.
    """

    # Getting the price data
    try:
        prices = data.history(
            context.security,
            ['close'],
            context.sma_window + 1,
            '1d')
    except IndexError:
        return

    # Calculate the rolling mean of asset close prices based on the sma_window
    prices['sma'] = prices['close'].rolling(window=context.sma_window).mean()

    # Generate the SMA signals
    prices['sma_signal'] = np.where(
        prices['close'] > prices['sma'], 1, 0)

    # Get the SMA signal
    sma_signal = prices['sma_signal'][-1]

    # Place the buy order
    if sma_signal == 1:
        # Place the order if the price is greater than the rolling SMA
        print("{} Long entry condition is True in: {}".format(get_datetime(), context.security.symbol))
        order_target_percent(context.security, 1)

def place_sell_order(context, data):
    """
        A function to place the sell order.
    """
    # Place the sell order
    print("{} Exit condition is True in: {}".format(get_datetime(), context.security.symbol))
    order_target_percent(context.security, 0)
