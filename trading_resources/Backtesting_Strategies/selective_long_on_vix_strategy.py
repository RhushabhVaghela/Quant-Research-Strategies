"""
    Title: Exit Using ATR.
    Description: In this strategy, we are generating long positions using 
    moving average crossover and we are exiting using ATR. We are setting 
    stop-loss and take-profit using a multiple of ATR.

    ############################# DISCLAIMER #############################
    This is a strategy template only and should not be used for live
    trading without appropriate backtesting and tweaking of the strategy
    parameters.
    ######################################################################
"""

# Import libraries
import numpy as np
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
    context.security = symbol('V')

    # Variable to keep track of the open position.
    context.position = 0

    # Define short term window size
    context.short_term_window = 9

    # Define long term window size
    context.long_term_window = 21

    # Define lookback
    context.lookback = context.long_term_window + 1

    # Variable to set stop-loss price
    context.stop_loss = np.nan

    # Variable to set take profit price.
    context.take_profit = np.nan

    # Setting multiple for Take profit and stop-loss
    context.take_profit_multiple = 6
    context.stop_loss_multiple = 2

    # Schedule the rebalance function
    schedule_function(
        rebalance,
        date_rule=date_rules.every_day(),
        time_rule=time_rules.market_close(minutes=1)
    )


def rebalance(context, data):
    """
        A function to rebalance the portfolio. This function is called by the
        schedule_function above.
    """

    try:
        # Fetch lookback no. days data for the given security
        prices = data.history(
            context.security,
            ['open', 'high', 'low', 'close'],
            context.lookback,
            '1d')
    except IndexError:
        return

    # Calculate SMA over the time period of 9 days and store it in the column 'SMA_9'
    prices.loc[:, 'SMA_9'] = prices['close'].rolling(
        context.short_term_window).mean()

    # Calculate SMA over the time period of 21 days and store it in the column 'SMA_21'
    prices.loc[:, 'SMA_21'] = prices['close'].rolling(
        context.long_term_window).mean()

    # Generate long entry signals
    # Check if previous day's SMA_9 is below previous day's SMA_21 
    # And current day's SMA_9 is above current day's SMA_21
    prices.loc[:, 'signal'] = np.where(
        (prices['SMA_9'].shift(1) < prices['SMA_21'].shift(1)) &
        (prices['SMA_9'] > prices['SMA_21']), 1, 0)

    # Calculate the Average True Range (ATR) over the period of 14 days
    prices['ATR'] = ta.ATR(prices['high'].values, prices['low'].values,
                           prices['close'].values, timeperiod=14)

    # Store the last generated signal in latest_signal variable
    latest_signal = prices.loc[:, 'signal'][-1]

    # Store the last close price in latest_close_price variable
    latest_close_price = prices.loc[:, 'close'][-1]

    # Store the last ATR value in latest_atr variable
    latest_atr = prices.loc[:, 'ATR'][-1]

    # Place the order
    # Check if we have any open position or not and if latest_signal is equal to 1
    if (context.position == 0) and (latest_signal == 1):
        print("{} Going long".format(get_datetime()))

        # Set stop-loss and take profit levels using a multiple of ATR value
        context.stop_loss = latest_close_price - \
            (latest_atr * context.stop_loss_multiple)
        context.take_profit = latest_close_price + \
            (latest_atr * context.take_profit_multiple)

        # Set context.position equal to 1 since we are entering a long position
        context.position = 1

        # Call order_target_percent to take a long position with 100% of available capital
        order_target_percent(context.security, 1)

    # Check if we have an open position
    elif (context.position == 1):
        # Check if the close price of the latest candle is less than the stop-loss or greater than the take profit level
        if (latest_close_price < context.stop_loss) or (latest_close_price > context.take_profit):
            print("{} Exiting long position".format(get_datetime()))

            # Set context.position equal to 0 since we are exiting a long position
            context.position = 0

            # Call order_target_percent to exit a long position
            order_target_percent(context.security, 0)
    