"""
    Title: Time-Series Momentum Strategy
    Description: This is a long-only strategy based on time-series momentum which rebalances the portfolio every month.
    Style tags: Momentum
    Asset class: Equities
    Dataset: US Equities
    
    ############################# DISCLAIMER #############################
    This is a strategy template only and should not be
    used for live trading without appropriate backtesting and tweaking of
    the strategy parameters.
    ######################################################################   
        
"""

# Import numpy
import numpy as np
import pandas as pd

# Import blueshift libraries
from blueshift.pipeline import Pipeline
from blueshift.pipeline.factors import AverageDollarVolume, CustomFactor, Returns
from blueshift.pipeline.data import EquityPricing
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
    """
        A function to define things to do at the start of the strategy.
    """

    # Define lookback period
    context.lookback = 90

    # Volatility adjusted returns threshold
    context.threshold = 0.05

    # Attach pipeline
    attach_pipeline(make_strategy_pipeline(context), name='strategy_pipeline')

    # Rebalance every month
    schedule_function(
        rebalance,
        date_rules.month_start(),
        time_rules.market_close(hours=0, minutes=5)
    )

class StdDev(CustomFactor):
    def compute(self, today, asset_ids, out, values):

        # Calculate the percentage changes
        pct_changes = np.diff(values, axis=0) / values[:-1]

        # Calculates the column-wise standard deviation, ignoring NaNs
        out[:] = np.nanstd(pct_changes, axis=0)

# The strategy requires context.lookback number of days.
def make_strategy_pipeline(context):
    """
        A function to make the pipeline.
    """
    dollar_volume_filter = AverageDollarVolume(window_length=252).top(100)
    lookback_returns = Returns(window_length=context.lookback)
    std_dev = StdDev(inputs=[EquityPricing.close], window_length=context.lookback)   
    pipe = Pipeline(
        screen=dollar_volume_filter,
        columns={
            'lookback_returns': lookback_returns, 
            'std_dev': std_dev
        }   
    )

    return pipe

# Function to get the type of the asset
def get_instrument_type(asset):
    return asset.name.instrument_type

def rebalance(context, data):
    """
       This function is called by the schedule_function in the initialize function.
    """

    # Exit existing open positions
    for security in context.portfolio.positions.keys():
        order_target_percent(security, 0)

    # Get the pipeline results
    pipeline_results = pipeline_output('strategy_pipeline')

    # Get the instrument type. 0 is for Equity and 4 is for ETF
    pipeline_results['instrument_type'] = pipeline_results.apply(
        get_instrument_type, axis=1)

    # Remove ETFs from the list
    pipeline_results = pipeline_results[pipeline_results['instrument_type'] != 4]

    # Filter high momentum stocks (vol_adjusted returns > 0.05)
    selected_stocks = pipeline_results.lookback_returns[(pipeline_results.lookback_returns/pipeline_results.std_dev) > context.threshold]

    # Take long position in high momentum stocks
    for security in selected_stocks.index:
        order_target_percent(security, 1/len(selected_stocks.index))
