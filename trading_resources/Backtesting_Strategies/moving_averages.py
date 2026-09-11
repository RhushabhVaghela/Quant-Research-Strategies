"""
    Title: Moving Average Crossover Strategy.
    Description: In this strategy, we will generate the entry and exit signals using 
    moving average crossovers. When the short moving average crosses the long moving 
    average from below, you will enter. And if the short term moving average crosses 
    the long term moving average from above, you will exit. We are setting stop-loss 
    and take-profit at a static value which can be changed. 
    Asset class: Equities
    Dataset: US Equities
    Start and end date: Keep the backtesting date range small (1 or 2 years) 
                        to avoid time out error.

    ############################# DISCLAIMER #############################
    This is a strategy template only and should not be used for live
    trading without appropriate backtesting and tweaking of the strategy
    parameters.
    ######################################################################
"""

# Import blueshift libraries
from blueshift.api import(
                                symbol,
                                order_target_percent,
                                schedule_function,
                                date_rules,
                                time_rules,
                                get_datetime
                        )

# Import libraries
import numpy as np
import talib
from datetime import datetime

def initialize(context):

    # Define symbol
    context.security = symbol('MSFT')

    # Define stop-loss and take-profit thresholds
    context.stop_loss_threshold = 0.05
    context.take_profit_threshold = 0.05

    # Variable to set stop-loss price
    context.stop_loss = np.nan
    # Variable to set take profit price
    context.take_profit = np.nan

    context.position = 0

    # Schedule strategy logic
    schedule_function(strategy,
                     date_rule=date_rules.every_day(),
                     time_rule=time_rules.market_close(minutes=10))

def strategy(context, data):

    # Fetch the data
    try:
        # Fetch lookback no. days data for the given security
        prices = data.history(context.security, 'close', 21, '1d')
        if len(prices) < 21:
            return 
    except IndexError:
        return

    # Calculate SMA over the time period of 9 days and store it in the column 'short_ma'
    short_ma = prices.iloc[-9:].mean()
    # Calculate SMA over the time period of 21 days and store it in the column 'long_ma'
    long_ma = prices.iloc[-21:].mean()    

    # Entry condition
    long_entry = short_ma > long_ma

    # Exit condition
    long_exit = short_ma < long_ma

    last_traded_price = data.current(context.security, 'close')

    # Place the order if entry condition is met
    # And there is no open position
    if long_entry and context.position == 0:
        print(f"Opening long position at {get_datetime()}")
        # Call order_target_percent to take a long position with 100% of available capital
        order_target_percent(context.security, 1)
        
        # Set context.position equal to 1 since we are entering a long position
        context.position = 1

        # Set stop-loss and take profit levels
        context.stop_loss = last_traded_price * (1-context.stop_loss_threshold)
        context.take_profit = last_traded_price * (1+context.take_profit_threshold)

    # Check if we have an open position
    elif context.position == 1:
        # Check conditions for exit
        if long_exit or last_traded_price < context.stop_loss \
                     or last_traded_price > context.take_profit:
            print(f"Closing long position at {get_datetime()}")
            # Call order_target_percent to exit a long position
            order_target_percent(context.security, 0)

            # Set context.position equal to 0 since we are exiting a long position
            context.position = 0
            context.stop_loss = np.nan
            context.take_profit = np.nan