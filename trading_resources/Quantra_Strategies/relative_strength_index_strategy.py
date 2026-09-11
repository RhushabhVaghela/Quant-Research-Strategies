"""
    Title: RSI Strategy for Time Series Alphas
    Description: A long-only strategy wherein a long entry position 
    is taken when the value of RSI lies below 40, and is held as 
    long as RSI is below 40. 
    Style tags: Momentum
    Asset class: Equities
    Dataset: US Equities

    ############################# DISCLAIMER #############################
    This is a strategy template only and should not be
    used for live trading without appropriate backtesting and tweaking of
    the strategy parameters.
    ######################################################################
"""
# Import libraries
import pandas as pd
import talib

# Import blueshift libraries
from blueshift.api import(
                            symbol,
                            order_target_percent,
                            schedule_function,
                            date_rules,
                            time_rules,
                            get_datetime
                        )

def initialize(context):
    # Define symbol
    context.stocks = [
                        symbol("AAPL"),
                        symbol("CSCO"),
                        symbol("IBM"),
                        symbol("MSFT"),
                        ]
 
    # Define lookback in days
    context.lookback = 14    

    # Rebalance every day
    schedule_function(
        rebalance,
        date_rules.every_day(),
        time_rules.market_open(hours=1, minutes=0)
    )

def rebalance(context, data):
    for ticker in context.stocks:
        # Fetch daily data of the security defined in initialize
        stk = data.history(ticker, ['close'],
                        context.lookback*2, '1d').pct_change()

        # Calculate RSI
        rsi = talib.RSI(stk.close.dropna().cumsum(), context.lookback)
        
        # Generate trading signals
        rsi_signal = rsi < 40
        if rsi_signal[-1]:
            order_target_percent(ticker, 0.25)
        else:
            order_target_percent(ticker, 0)