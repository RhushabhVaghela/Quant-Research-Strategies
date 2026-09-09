"""
    Title: SMA-Price Crossover Strategy
    Description: A long-only strategy wherein a long position is held
    for as long as the SMA line is below the price line.
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
    context.stock = symbol('AAPL')

    # Define lookback
    context.lookback = 100       

    # Rebalance every 15 minute
    schedule_function(
        rebalance,
        date_rules.week_start(days_offset=0),
        time_rules.every_nth_minute(15)        
    )

def rebalance(context, data):
    # Fetch minute data of the security defined in initialize
    data = data.history(context.stock, 'close',
                        context.lookback*15, '1m')
    
    # Resample the data
    data_15min = pd.DataFrame()
    data_15min['close'] = data.resample('15min').last().dropna()

    # Calculate SMA
    data_15min['sma'] = data_15min['close'].rolling(context.lookback).mean()

    # Generate and print signals
    print(f"{get_datetime()}: Crossover {data_15min['close'][-1] > data_15min['sma'][-1]}")
    if data_15min['close'][-1] > data_15min['sma'][-1]:                
        order_target_percent(context.stock, 1)    
    else:
        order_target_percent(context.stock, 0)