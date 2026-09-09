"""
    Title: Sample Technical Indicator Strategy
    Description: This is a long-only strategy based on a simple moving average 
                 and volatility which rebalances the portfolio weights every day.
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
import numpy as np
import pandas as pd

# Import blueshift libraries
from blueshift.pipeline import Pipeline
from blueshift.pipeline.factors import AverageDollarVolume, CustomFactor, Returns
from blueshift.api import(
    symbol,
    order_target_percent,
    schedule_function,
    date_rules,
    time_rules,
    attach_pipeline,
    pipeline_output,
    get_datetime
)


def initialize(context):

    context.lookback = 20
    attach_pipeline(make_strategy_pipeline(
        context), name='volatility_pipeline')

    # Rebalance every day
    schedule_function(rebalance,
                      date_rules.every_day(),
                      time_rules.market_open(hours=0, minutes=1))


class ComputeVol(CustomFactor):
    inputs = [Returns(window_length=2)]
    window_length = 90

    def compute(self, today, assets, out, returns):
        out[:] = np.nanstd(returns, axis=0) * np.sqrt(250)


def make_strategy_pipeline(context):
    """
        A function to make the pipeline.
    """
    dollar_volume_filter = AverageDollarVolume(window_length=252).top(500)
    volatility = ComputeVol()
    pipe = Pipeline(
        screen=dollar_volume_filter,
        columns={
            'volatility': volatility
        }
    )
    return pipe


# Function to get the type of the asset
def get_instrument_type(asset):
    return asset.name.instrument_type


def rebalance(context, data):
    # Get the pipeline results
    pipeline_results = pipeline_output('volatility_pipeline')

    # Get the instrument type. 0 is for Equity and 4 is for ETF
    pipeline_results['instrument_type'] = pipeline_results.apply(
        get_instrument_type, axis=1)

    # Remove ETFs from the list
    pipeline_results = pipeline_results[pipeline_results['instrument_type'] != 4]

    # Sort the stocks on the bases of their volatility
    vol_sorted = pipeline_results.sort_values('volatility', ascending=False)

    # Get the top ten most volatile stocks
    top_decile = vol_sorted[:int(len(vol_sorted)*0.1)]

    # Get the data for the pipeline output
    try:
        data = data.history(top_decile.index, 'close', context.lookback, '1d')
    except IndexError:
        return

    data.dropna(inplace=True, axis='columns')

    # Calculate daily percentage change of prices
    stock_data_pc = data.pct_change()

    # Create new dataframe called portfolio
    portfolio = pd.DataFrame()

    # Calculate average returns of stocks
    portfolio['returns'] = stock_data_pc.mean(axis=1)

    # Calculate cumulative returns of portfolio
    portfolio['value'] = (portfolio+1).cumprod()

    # Calculate simple moving average of period 10
    portfolio['sma10'] = portfolio.value.rolling(window=10).mean()

    # Remove the symbols not part of top deciles but part of portfolio
    for security in context.portfolio.positions.keys():
        if security not in top_decile.index:
            order_target_percent(security, 0)

    # Place orders
    long_entry = portfolio.value.iloc[-1] > portfolio.sma10.iloc[-1]
    long_exit = portfolio.value.iloc[-1] < portfolio.sma10.iloc[-1]

    if long_entry:
        print('Placing Long Order')
        for security in top_decile.index:
            # Taking long position in the top 10 stocks using order_target_percent method
            order_target_percent(security, 1.0/len(top_decile))

    elif long_exit:
        print("Portfolio value is less than SMA. No positions to take.")
        for security in context.portfolio.positions.keys():
            # Closing open position using order_target_percent method
            order_target_percent(security, 0)