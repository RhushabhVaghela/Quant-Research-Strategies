"""
    Title: Support Level Strategy
    Description: This is a long only strategy that takes trades based on the support levels
    Style tags: Momentum
    Asset class: Equities
    Dataset: US
    
    ############################# DISCLAIMER #############################
    This is a strategy template only and should not be
    used for live trading without appropriate backtesting and tweaking of
    the strategy parameters.
    ######################################################################
"""

import numpy as np
import pandas as pd
from scipy.signal import argrelextrema
import math

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
    """
        A function to define things to do at the start of the strategy
    """

    # Define symbol
    context.stock = symbol('C')
                
    # Define lookback
    context.lookback = 990

    # Initialize SL and TP
    context.SL = 0
    context.TP = 0

    # Set current position to 0
    context.curr_pos = 0

    # Rebalance every nth minute
    schedule_function(
        rebalance,
        date_rules.every_day(),
        time_rules.every_nth_minute(minutes=30)
    )


# Function to get the nearest support level
def get_support(price_data, argrel_window = 25):   
    
    # Check whether the length of data is greater than the argel_window
    assert price_data.shape[0] > argrel_window, "Length of data is less then argel_window"        

    # Determine the indices of all support levels
    support_list = argrelextrema(
        price_data['low'].values, np.less, order=argrel_window)[0]

    # Get support levels
    price_data['support'] = price_data.iloc[support_list, 2]

    # Fetch the last traded price
    ltp = price_data.close.iloc[-1]
    
    # Get the nearest support level
    price_data['support'] = np.where(price_data['support'] < ltp, price_data['support'], np.nan)

    try:
        return price_data.loc[price_data.support.dropna().index.max(), 'support']    
    except:
        return np.nan


def rebalance(context, data):
    # Fetch daily data of the security defined in initialize
    data_daily = data.history(context.stock, ['open', 'high', 'low', 'close'], 
                context.lookback, '1d')

    # Create and initialise columns with NaN values
    data_daily['Support'] = np.nan

    price_data = data_daily.iloc[-50:]

    # Support level
    support = get_support(price_data)

    # Check for NaN values
    if math.isnan(support):
        return            

    # Fetch LTP
    ltp = data.current(context.stock, "close")

    # Generate signal
    signal = ltp < support

    # Take long position if the close price is less than support
    if signal and context.curr_pos == 0:
        print(f"{get_datetime()} Going long as ltp {ltp} less than support {support}")
        order_target_percent(context.stock, 1)

        # Set SL
        context.SL = ltp*0.98

        # Set TP
        context.TP = ltp*1.10

        # Update current position to 1
        context.curr_pos = 1

        print(f"Take profit {context.TP} & SL {context.SL}")

    # Exit the trade if SL or TP conditions are met
    elif context.curr_pos == 1:
        if ltp <= context.SL:
            print(f"{get_datetime()} Exit - SL {ltp}")
            order_target_percent(context.stock, 0)
            context.curr_pos = 0

        elif ltp >= context.TP:
            print(f"{get_datetime()} Exit - TP {ltp}")
            order_target_percent(context.stock, 0)
            context.curr_pos = 0

    
