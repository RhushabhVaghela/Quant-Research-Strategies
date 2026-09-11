"""
    Title: Technical Indicators Based Momentum Strategy Template
    Description: The momentum trading strategy is implemented using
    the two indicators from TA-Lib, Parabolic SAR and Stochastic Oscillator.
    Dataset: US Equities

    ############################# DISCLAIMER #############################
    This is a strategy template only and should not be
    used for live trading without appropriate backtesting and tweaking of
    the strategy parameters.
    ######################################################################
"""

# Import TA-lib
import talib

# Import blueshift libraries
from blueshift.api import (
    symbol,
    order_target_percent,
    schedule_function,
    date_rules,
    time_rules,
    get_datetime
)


def initialize(context):
    # Define symbol
    context.security = symbol('AAPL')

    # Define lookback
    context.lookback = 30

    # Define the indicator parameters
    context.acceleration = 0.02
    context.maximum = 0.2
    context.fastk_period = 5
    context.slowk_period = 3
    context.fastd_period = 3
    context.slowd_period = 3

    # Schedule the rebalance function
    schedule_function(
        rebalance,
        date_rule=date_rules.every_day(),
        time_rule=time_rules.market_close(minutes=5)
    )


def rebalance(context, data):
    """
        A function to rebalance the portfolio. This function is called by the
        schedule_function above.
    """

    try:
        # Fetch lookback no. days data for the given security
        stock_data = data.history(
            context.security,
            ['open', 'high', 'low', 'close'],
            context.lookback,
            '1d')
    except IndexError:
        return

    # Calculate the parabolic SAR
    stock_data['SAR'] = talib.SAR(
        (stock_data['high'].values),
        (stock_data['low'].values),
        acceleration=context.acceleration,
        maximum=context.maximum
    )

    # Calculate the slow and fast stochastic oscillator.
    stock_data['slowk'], stock_data['slowd'] = talib.STOCH(
        stock_data['high'].values,
        stock_data['low'].values,
        stock_data['close'].values,
        fastk_period=context.fastk_period,
        slowk_period=context.slowk_period,
        slowd_matype=context.slowd_period
    )

    stock_data['fastk'], stock_data['fastd'] = talib.STOCHF(
        stock_data['high'].values,
        stock_data['low'].values,
        stock_data['close'].values,
        fastk_period=context.fastk_period,
        fastd_period=context.fastd_period
    )

    # Get the latest signal
    long_entry = (
            (stock_data['SAR'] < stock_data['close']) &
            (stock_data['fastk'] > stock_data['slowd'])
            )[-1]
    print("{} Long entry signal {}".format(get_datetime(), long_entry))
    long_exit = (
            (stock_data['SAR'] > stock_data['close']) &
            (stock_data['fastk'] < stock_data['slowd'])
            )[-1]
    print("{} Long exit signal {}".format(get_datetime(), long_exit))
    # Place the order
    if long_entry:
        print("{} Going long on {}".format(get_datetime(), context.security))
        order_target_percent(context.security, 1)

    elif long_exit:
        print("{} Exiting long or no position in {}".format(get_datetime(), context.security))
        order_target_percent(context.security, 0)