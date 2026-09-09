"""
    Title: Bullish Marubozu Trading Strategy
    Description: A long-only strategy wherein a long position is taken upon
    formation of a bullish marubozu and it is exited when SL or TP gets hit.
    Style tags: Momentum
    Asset class: Equities
    Dataset: US Equities

    ############################# DISCLAIMER #############################
    This is a strategy template only and should not be
    used for live trading without appropriate backtesting and tweaking of
    the strategy parameters.
    ######################################################################
"""

import pandas as pd
import talib as ta

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
    context.stock = symbol('AAPL')

    # Define lookback
    context.lookback = 100

    # Initialize SL and TP
    context.SL = 0
    context.TP = 0

    # Set current position to 0
    context.curr_pos = 0

    # Rebalance every day at open
    schedule_function(
        rebalance,
        date_rules.every_day(),
        time_rules.market_open(minutes=0, hours=0)
    )


def rebalance(context, data):
    # Fetch minute data of the security defined in initialize
    data = data.history(context.stock, ['open', 'high', 'low', 'close'],
                        context.lookback * 15, '1m')

    # Resample the data to hourly data
    price_mapping = {
        "open": "first",
        "high": "max",
        "low": "min",
        "close": "last"
    }

    data_15min = pd.DataFrame()
    data_15min = data.resample("1h").agg(price_mapping).dropna()

    # Calculate Marubozu signal
    data_15min['pattern_signal'] = ta.CDLMARUBOZU(data_15min['open'], data_15min['high'], data_15min['low'],
                                                  data_15min['close'])

    # Take long position if the previous candle is a bullish marubozu and there is no open position
    if data_15min['pattern_signal'][-2] == 100 and context.curr_pos == 0:
        order_target_percent(context.stock, 1)

        # Set SL as the low price of the Marubozu candle
        context.SL = data_15min['low'][-2]

        # Set TP as 3 times the difference between entry price and SL
        context.TP = data_15min['open'][-2] + 3 * (data_15min['open'][-2] - context.SL)

        # Update current position to 1
        context.curr_pos = 1

    # Exit the trade if SL or TP conditions are met
    elif context.curr_pos == 1:
        if data_15min['close'][-1] <= context.SL:
            order_target_percent(context.stock, 0)
            context.curr_pos = 0

        elif data_15min['close'][-1] >= context.TP:
            order_target_percent(context.stock, 0)
            context.curr_pos = 0
