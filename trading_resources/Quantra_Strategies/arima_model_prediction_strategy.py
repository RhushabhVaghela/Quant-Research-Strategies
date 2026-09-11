"""
    Title: ARIMA Prediction Strategy Template
    Description: This strategy uses the ARIMA model to make a prediction
    and then take a position accordingly. The best fit ARIMA model is
    selected using the AIC criterion.
    Dataset: Forex

    ############################# DISCLAIMER #############################
    This is a strategy template only and should not be
    used for live trading without appropriate backtesting and tweaking of
    the strategy parameters.
    ######################################################################
"""

# Data manipulation
import pandas as pd

# For statistical analysis
from statsmodels.tsa.arima.model import ARIMA

# blueshift
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

    # Define the asset
    context.asset = symbol('AUD/USD')

    # The lookback window
    context.lookback = 252

    # Call rebalance function every day 15 minutes before market close
    schedule_function(
                        rebalance,
                        date_rules.every_day(),
                        time_rules.market_close(hours=0, minutes=15)
                     )


def rebalance(context, data):
    """
        A function to rebalance the portfolio based on the ARIMA prediction.
    """

    try:
        # Fetch lookback no. days data for the asset
        prices = data.history(
            context.asset,
            ['close'],
            context.lookback,
            '1d')
    except IndexError:
        return

    # The p,d and q values
    aic = []
    p = range(1, 3)
    d = range(1, 2)
    q = range(1, 3)

    # Empty list to store p,q,dist
    p_q_dist = []

    # Get the aic score for different values of p, d and q
    for i in p:
        for j in d:
            for k in q:
                try:
                    gm = ARIMA(prices['close'], order=(i, j, k))
                    gm_fit = gm.fit()
                    print(gm_fit)
                    aic_temp = gm_fit.aic
                    keys_temp = (i, j, k)
                    p_q_dist.append(keys_temp)
                    aic.append(aic_temp)
                except:
                    pass

    # Store values in dictionary
    aic_dict = {'p_q_dist': p_q_dist, 'aic': aic}

    # Create DataFrame from dictionary
    df = pd.DataFrame(aic_dict)

    # Get the minimum AIC value with the p,d and q values
    df = df[df['aic'] == df['aic'].min()].reset_index()

    # Only performing trade if the ARIMA model could be fit
    if len(df) > 0:
        # Fitting the optimum model
        gm = ARIMA(prices['close'], order=df.p_q_dist[0])
        gm_fit = gm.fit()
        predicted_price = gm_fit.forecast()

        # Placing the order
        long_entry = predicted_price.values[0] > prices['close'][-1]
        print("{} Long entry condition {}".format(get_datetime(),long_entry))
        if long_entry:
            print("{} Entering long position in {}".format(get_datetime(), context.asset))
            order_target_percent(context.asset, 1)
        else:
            print("{} Entering short position in {}".format(get_datetime(), context.asset))
            order_target_percent(context.asset, -1)