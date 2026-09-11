"""
    Title: Pair Trading Strategy Code Template
    Description: The pair trading strategy is implemented after using a
    cointegration test and z-score.
    Dataset: US Equities

    ############################# DISCLAIMER #############################
    This is a strategy template only and should not be
    used for live trading without appropriate backtesting and tweaking of
    the strategy parameters.
    ######################################################################
"""

# Import numpy and pandas
import numpy as np
import pandas as pd

# Import statsmodel
import statsmodels.api as stat
import statsmodels.tsa.stattools as ts


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
    # Define Symbols
    context.security_1 = symbol('AAPL')
    context.security_2 = symbol('AMZN')

    # The lookback for calculating the hedge ratio
    context.lookback = 100

    # Percentage wealth to use
    context.pf_fraction = 1.0

    # The strategy parameters
    context.end = context.lookback-1
    context.start = context.end - 10
    context.status = ""
    context.prev_status = ""
    context.mtm = ""
    context.prev_sell_price = ""
    context.sell_price = ""
    context.prev_buy_price = ""
    context.buy_price = ""

    # The take profit and stop loss criteria
    context.SL = -0.03
    context.TP = 0.075

    # The standard deviation multiplier
    context.threshold = 1

    # Lot/Quantity size for data1
    context.N = 0.5
    context.M = 0.3

    # Schedule the rebalance function
    schedule_function(
                        rebalance,
                        date_rule=date_rules.every_day(),
                        time_rule=time_rules.market_close(minutes=5)
                     )


def cointegration_test(x, y):
    """
        A function to find the cointegration.
    """

    # Use OLS method to find the spread of the two series
    result = stat.OLS(x['close'], y['close']).fit()
    # Check for stationarity of the spread using adfuller test
    return ts.adfuller(result.resid)


def zscore_cal(data1, data2, start, end):
    """
        A function to find the z-score.
    """

    s1 = pd.Series(data1['close'][start:end])
    s2 = pd.Series(data2['close'][start:end])

    # Compute mean of the spread till now
    mvavg_old = np.mean(np.log(s1/s2))

    # Compute stdev of the spread till now
    std_old = np.std(np.log(s1/s2))

    # Compute spread
    current_spread = np.log(
        data1['close'][end]/data2['close'][end])

    # Compute z-score
    zscore = (current_spread - mvavg_old) / std_old if std_old > 0 else 0

    return zscore


def signal_cal(zscore, threshold, adftest):
    """
        A function to find the trading signal.
    """

    if zscore > threshold and adftest == 'Yes':
        # Z-score is greater than threshold, the spread shall fall towards mean
        signal = 'SELL'

    elif zscore < -threshold and adftest == 'Yes':
        # Z-score is smaller than threshold, the spread shall rise towards mean
        signal = 'BUY'

    else:
        signal = 'No position'

    return signal


def status_cal(prev_status, mtm, SL, TP, signal, adftest):
    """
        A function to find the trade status.
    """

    if prev_status in ["", "SL", "TP", "CB"]:
        status = signal
    else:
        if adftest == "No":
            status = "CB"   # Break in the cointegration status of the pair
        else:
            if mtm == "":
                status = ""
            else:
                if mtm < SL:
                    status = "SL"   # Stop loss status
                else:
                    if mtm > TP:
                        status = "TP"  # Take profit status
                    else:
                        status = prev_status

    return status


# Calculating buy price
def buy_price_cal(
                    prev_status,
                    prev_buy_price,
                    buy_price,
                    signal,
                    status,
                    data1,
                    data2,
                    end
                 ):

    if status == prev_status:
        buy_price = prev_buy_price

    else:
        if status in ["SL", "TP", "CB", ""]:
            buy_price = ""
        else:
            if signal == "BUY":    # Signal is to buy the spread
                # Hence, buy price = close of first security
                buy_price = data1['close'][end]
            else:
                if signal == "SELL":  # Signal is to sell the spread
                    # Hence, buy price = close of second security
                    buy_price = data2['close'][end]
                else:
                    buy_price = ""   # no signal hence no buy price

    return buy_price


# Calculating sell price
def sell_price_cal(
                    prev_status,
                    prev_sell_price,
                    sell_price,
                    signal,
                    status,
                    data1,
                    data2,
                    end
                  ):
    if status == prev_status:
        sell_price = prev_sell_price
    else:
        if status in ["SL", "TP", "CB", ""]:
            sell_price = ""
        else:
            if signal == "BUY":  # Signal is to buy the spread
                # Hence sell price = close of second security
                sell_price = data2['close'][end]
            else:
                if signal == "SELL":  # signal is to sell the spread
                    # Hence sell price = close of first security
                    sell_price = data1['close'][end]
                else:
                    sell_price = ""  # No signal hence no sell price either

    return sell_price


# Calculating mtm
def mtm_cal(
            data1,
            data2,
            prev_status,
            prev_sell_price,
            prev_buy_price,
            M,
            N,
            end
           ):

    if prev_status == "BUY":
        # Calculate mtm of the trades using their lot sizes
        mtm = (prev_sell_price-data2['close'][end])*M + \
                        (data1['close'][end] - prev_buy_price)*N
        mtm_percentage = mtm/(prev_sell_price*M+prev_buy_price*N)
        return mtm_percentage

    elif prev_status == "SELL":
        mtm = (prev_sell_price-data2['close'][end])*M + \
                        (data1['close'][end] - prev_buy_price)*N
        mtm_percentage = mtm/(prev_sell_price*M+prev_buy_price*N)
        return -mtm_percentage

    else:
        return ""


def rebalance(context, data):
    """
        A function to rebalance the portfolio. This function is called by the
        schedule_function in the initialize function.
    """

    try:
        # Fetch lookback no. days data for the first security
        data1 = data.history(
            context.security_1,
            ['close'],
            context.lookback,
            '1m')
    except IndexError:
        return

    try:
        # Fetch lookback no. days data for the second security
        data2 = data.history(
            context.security_2,
            ['close'],
            context.lookback,
            '1m')
    except IndexError:
        return
    
    # Check for cointegration
    c_t = cointegration_test(data1, data2)
    if c_t[1] <= 0.05:
        adftest = "Yes"
    else:
        adftest = "No"

    # Calculate z-score for the spread
    zscore = zscore_cal(data1, data2, context.start, context.end)

    # Generating trading signals
    signal = signal_cal(zscore, context.threshold, adftest)

    # Calculating mtm
    context.mtm = mtm_cal(
                            data1,
                            data2,
                            context.prev_status,
                            context.prev_sell_price,
                            context.prev_buy_price,
                            context.M,
                            context.N,
                            context.end
                         )

    # Assigning status
    context.status = status_cal(
                                context.prev_status,
                                context.mtm,
                                context.SL,
                                context.TP,
                                signal,
                                adftest
                               )

    # Assigning buy_price
    context.buy_price = buy_price_cal(
                                        context.prev_status,
                                        context.prev_buy_price,
                                        context.buy_price,
                                        signal,
                                        context.status,
                                        data1,
                                        data2,
                                        context.end
                                     )

    # Assigning sell_price
    context.sell_price = sell_price_cal(
                                        context.prev_status,
                                        context.prev_sell_price,
                                        context.sell_price,
                                        signal,
                                        context.status,
                                        data1,
                                        data2,
                                        context.end
                                       )

    print("{} Status: {}".format(get_datetime(), context.status))

    # Place the order
    if context.status == "BUY":
        print("{} Going long on {}".format(get_datetime(), context.security_1))
        order_target_percent(
                                context.security_1,
                                context.pf_fraction*context.N
                            )
        print("{} Going long on {}".format(get_datetime(), context.security_2))
        order_target_percent(
                                context.security_2,
                                -context.pf_fraction*context.M
                            )

    elif context.status == "SELL":
        print("{} Going short on {}".format(get_datetime(), context.security_1))
        order_target_percent(
                                context.security_1,
                                -context.pf_fraction*context.N
                            )
        print("{} Going short on {}".format(get_datetime(), context.security_2))
        order_target_percent(
                                context.security_2,
                                context.pf_fraction*context.M
                            )

    elif context.status in ["SL", "TP", "CB"]:
        print("{} Exiting position in {}".format(get_datetime(), context.security_1))
        order_target_percent(context.security_1, 0)
        print("{} Exiting position in {}".format(get_datetime(), context.security_2))
        order_target_percent(context.security_2, 0)

    # Assigning the previous values
    context.prev_sell_price = context.sell_price
    context.prev_status = context.status
    context.prev_buy_price = context.buy_price
