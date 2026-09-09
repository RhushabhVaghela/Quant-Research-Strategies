"""
    Title: Mean Reversion Strategy Template
    Description: The mean reversion strategy is implemented on using Bollinger
    Bands on the selected asset.
    Dataset: Forex

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
    context.security = symbol('EUR/CHF')

    # Define lookback
    context.lookback = 5

    # Define position
    context.position = 0

    # Define standard deviation multiplier
    context.mult = 0.5

    # Schedule the rebalance function
    schedule_function(
                        rebalance,
                        date_rule=date_rules.every_day(),
                        time_rule=time_rules.market_close(minutes=1)
                     )


def rebalance(context, data):
    """
        A function to rebalance the portfolio is passed on to the call
        of schedule_function above.
    """

    try:
        # Fetch lookback no. days data for the given security
        prices = data.history(
            context.security,
            ['close'],
            context.lookback,
            '1d')
    except IndexError:
        return

    # Calculate the moving average
    prices['SMA'] = talib.SMA(
                                prices['close'].values,
                                timeperiod=context.lookback
                             )

    # Calculate the standard deviation
    prices['STDDEV'] = talib.STDDEV(
                                    prices['close'].values,
                                    timeperiod=context.lookback
                                   )

    # Calculate the bollinger bands
    prices['upper_band'] = prices['SMA'] + context.mult * prices['STDDEV']
    prices['lower_band'] = prices['SMA'] - context.mult * prices['STDDEV']

    # Get the latest signal
    long_entry = (prices['close'] < prices['lower_band'])[-1]
    print("{} Long entry condition {}".format(get_datetime(), long_entry))
    
    long_exit = (prices['close'] >= prices['SMA'])[-1]
    print("{} Long exit condition {}".format(get_datetime(), long_exit))
    
    short_entry = (prices['close'] > prices['upper_band'])[-1]
    print("{} Short entry condition {}".format(get_datetime(), short_entry))
    
    short_exit = (prices['close'] <= prices['SMA'])[-1]
    print("{} Short exit condition {}".format(get_datetime(), short_exit))

    # Place the order
    if long_entry and context.position == 0:
        print("{} Going long on {}".format(get_datetime(), context.security))
        order_target_percent(context.security, 1)
        context.position = 1

    elif short_entry and context.position == 0:
        print("{} Going short on {}".format(get_datetime(), context.security))
        order_target_percent(context.security, -1)
        context.position = -1

    elif long_exit and context.position == 1:
        print("{} Exiting long position in {}".format(get_datetime(), context.security))
        order_target_percent(context.security, 0)
        context.position = 0

    elif short_exit and context.position == -1:
        print("{} Exiting short position in {}".format(get_datetime(), context.security))
        order_target_percent(context.security, 0)
        context.position = 0
