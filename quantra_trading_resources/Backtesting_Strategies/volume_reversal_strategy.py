"""
    Title: Volume Reversal Strategy Template
    Description: The volume reversal strategy is based upon the price
    movements corresponding to the trading volume of the security. The
    trade is exit on the 5th day or if a contrarian signal is observed.
    Dataset: US Equities

    ############################# DISCLAIMER #############################
    This is a strategy template only and should not be
    used for live trading without appropriate backtesting and tweaking of
    the strategy parameters.
    ######################################################################
"""

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
    # Define Symbol
    context.security = symbol('K')

    # The current position
    context.position = 0

    # The threshold for exit
    context.exit_limit = 5

    # The days held
    context.days_held = 5

    # The lookback for price and volume
    context.pv_lookback = 5

    # The lookback for standard deviation
    context.std_lookback = 100

    # The lookback for data
    context.lookback = context.std_lookback + context.pv_lookback + 2

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
        # Fetch lookback no. days data for the first security
        data_df = data.history(
            context.security,
            ['close', 'volume'],
            context.lookback,
            '1d')
    except IndexError:
        return
    # Price change for the last 5 days
    data_df['pr_chg'] = data_df['close'].shift(1) - \
        data_df['close'].shift(1 + context.pv_lookback)

    # Standard deviation of price change
    data_df['std_day'] = data_df['pr_chg'].rolling(
        window=context.std_lookback).std()

    # Average volume traded
    data_df['avg_vol'] = data_df['volume'].shift(1).rolling(
        window=context.pv_lookback).mean()

    # Average volume traded between last 5 to 10 days
    data_df['past avg_vol'] = data_df['avg_vol'].shift(context.pv_lookback)

    # Get the signal
    long_entry = (
                    (data_df['pr_chg'].abs() > data_df['std_day']) &
                    (data_df['avg_vol'] < data_df['past avg_vol']) &
                    (data_df['pr_chg'] < 0)
                 )[-1]
    print("{} Long entry: {}".format(
        get_datetime(), 
        long_entry))
    short_entry = (
                    (data_df['pr_chg'].abs() > data_df['std_day']) &
                    (data_df['avg_vol'] < data_df['past avg_vol']) &
                    (data_df['pr_chg'] > 0)
                  )[-1]
    print("{} Short entry: {}".format(
        get_datetime(), 
        short_entry))
    # Place the order
    if context.position == 0:
        if long_entry:
            print("{} Going long on {}".format(get_datetime(), context.security))
            order_target_percent(context.security, 1)
            context.position = 1
            context.days_held = 0
        elif short_entry:
            print("{} Going short on {}".format(get_datetime(), context.security))
            order_target_percent(context.security, -1)
            context.position = -1
            context.days_held = 0
    else:
        if long_entry and context.position == 1:
            context.days_held += 1
            print("{} Long: {} Days held {}".format(get_datetime(), context.security, context.days_held))
            
        elif short_entry and context.position == -1:
            context.days_held += 1
            print("{} Short: {} Days held {}".format(get_datetime(), context.security, context.days_held))
        elif (long_entry and context.position == -1) or \
            (short_entry and context.position == 1) or \
                (context.days_held > context.exit_limit):
            order_target_percent(context.security, 0)
            context.position = 0
        else:
            context.days_held += 1
    