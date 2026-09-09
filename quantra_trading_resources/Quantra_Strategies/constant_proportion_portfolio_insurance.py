"""
Title: Constant Proportion Portfolio Insurance (CPPI)
Description: CPPI is a position sizing strategy that enables 
            an investor to enjoy the upside potential of a risky asset 
            while hedging the exposure to downside risk.
Dataset: US Equities
"""
# Import blueshift libraries
from blueshift.api import(symbol,
                        order_target_value,
                        schedule_function,
                        date_rules,
                        time_rules,
                        get_datetime
                        )

# Import libraries
import numpy as np
import pandas as pd


def initialize(context):
    """
    A function to define things to do at the start of the strategy
    """

    # Select security
    context.security = symbol('AAPL')

    # Set multiplier
    context.multiplier = 4

    # Set floor percentage
    context.floor_percent = 0.90
    context.floor_value = context.portfolio.portfolio_value * context.floor_percent

    # Call strategy function everyday, 5 minutes before close
    schedule_function(strategy,
                      date_rules.every_day(),
                      time_rules.market_close(minutes=5))


def run_cppi(context):
    # Calculate leverage based on fixed floor value
    leverage = (context.portfolio.portfolio_value -
                context.floor_value) * context.multiplier
    return leverage


def strategy(context, data):
    """
    A function to rebalance the portfolio is passed on to the call
    of schedule_function above.
    """
    # Place order
    position = run_cppi(context)
    print("{} Signal value {}".format(get_datetime(), position))
    order_target_value(context.security, position)