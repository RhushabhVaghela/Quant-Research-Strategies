"""
    Title: Short Selling in Trading
    Description: A long-short strategy using regime identification and swings.
    The strategy as discussed in the course rebases the asset on the basis of
    the FX pair as well, but to keep things simple, we have made this template
    without rebasing on the basis of currency.
    Dataset: US Equities

    ############################# DISCLAIMER #############################
    This is a strategy template only and should not be
    used for live trading without appropriate backtesting and tweaking of
    the strategy parameters.
    ######################################################################
"""
# Data numpy and pandas
import numpy as np
import pandas as pd

# Calculates swing highs and lows
from scipy.signal import argrelextrema

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
    context.security_sym = symbol('BAC')
    context.benchmark_sym = symbol("SPY")

    # The lookback period
    context.lookback = 252

    # The parameters for moving average
    context.st = 30
    context.mt = 160

    # Schedule the rebalance function every day
    schedule_function(
        rebalance,
        date_rule=date_rules.every_day(),
        time_rule=time_rules.market_close(minutes=5)
    )


def relative(stock_dataframe, benchmark_dataframe, benchmark_name, start, end):
    # Slice dataframe from start to end period: either offset or datetime
    stock_dataframe = stock_dataframe[start:end]

    # Join the dataset: Concatenation of benchmark and stock
    data = pd.concat([stock_dataframe, benchmark_dataframe], axis=1).dropna()

    # Adjustment factor: Calculate the product of the benchmark
    data['adjustment_factor'] = data[benchmark_name]

    # Relative series: Calculate the relative series by dividing the OHLC
    # stock data with the adjustment factor
    data['relative_open'] = data['open'] / data['adjustment_factor']
    data['relative_high'] = data['high'] / data['adjustment_factor']
    data['relative_low'] = data['low'] / data['adjustment_factor']
    data['relative_close'] = data['close'] / data['adjustment_factor']

    # Rebased series: Multiply relative series with the first value of the
    # adjustment factor to get the rebased series
    data['rebased_open'] = data['relative_open'] * \
        data['adjustment_factor'].iloc[0]
    data['rebased_high'] = data['relative_high'] * \
        data['adjustment_factor'].iloc[0]
    data['rebased_low'] = data['relative_low'] * \
        data['adjustment_factor'].iloc[0]
    data['rebased_close'] = data['relative_close'] * \
        data['adjustment_factor'].iloc[0]

    return (data)


# Calculate swings
def swings(df, high, low, argrel_window):
    # Create swings:

    # Step 1: Copy the existing df. We will manipulate and reduce this df and
    # want to preserve the original
    high_low = df[[high, low]]

    # Step 2: build 2 lists of highs and lows using argrelextrema
    highs_list = argrelextrema(
        high_low[high].values, np.greater, order=argrel_window)
    lows_list = argrelextrema(
        high_low[low].values, np.less, order=argrel_window)

    # Step 3: Create swing high and low columns and assign values from the
    # lists
    swing_high = 's' + str(high)[-12:]
    swing_low = 's' + str(low)[-12:]
    high_low[swing_low] = high_low.iloc[lows_list[0], 1]
    high_low[swing_high] = high_low.iloc[highs_list[0], 0]

    # Alternation: We want highs to follow lows and keep the most extreme values

    # Step 4. Create a unified column with peaks<0 and troughs>0
    swing_high_low = str(high)[:2] + str(low)[:2]
    high_low[swing_high_low] = high_low[swing_low].sub(
        high_low[swing_high], fill_value=0)

    # Step 5: Reduce dataframe and alternation loop
    # Instantiate start
    i = 0

    # Drops all rows with no swing
    high_low = high_low.dropna(subset=[swing_high_low])
    if ((high_low[swing_high_low].shift(1) *
            high_low[swing_high_low] > 0).any()):
        
        for i in range(0,4):
            # eliminate lows higher than highs
            high_low.loc[
                (high_low[swing_high_low].shift(1) * high_low[swing_high_low] < 0) &
                (high_low[swing_high_low].shift(1) < 0) &
                (np.abs(high_low[swing_high_low].shift(1)) < high_low[swing_high_low]),
                swing_high_low] = np.nan
            # eliminate earlier lower values
            high_low.loc[
                (high_low[swing_high_low].shift(1) * high_low[swing_high_low] > 0) &
                (high_low[swing_high_low].shift(1) < high_low[swing_high_low]),
                swing_high_low] = np.nan
            # eliminate subsequent lower values
            high_low.loc[
                (high_low[swing_high_low].shift(-1) * high_low[swing_high_low] > 0) &
                (high_low[swing_high_low].shift(-1) < high_low[swing_high_low]),
                swing_high_low] = np.nan
            # reduce dataframe
            high_low = high_low.dropna(subset=[swing_high_low])

    # Step 6: Join with existing dataframe as pandas cannot join columns with
    # the same headers
    # First, we check if the columns are in the dataframe
    if swing_low in df.columns:
        # If so, drop them
        df.drop([swing_low, swing_high], axis=1, inplace=True)
    # Then, join columns
    df = df.join(high_low[[swing_low, swing_high]])

    # Last swing adjustment:

    # Step 7: Preparation for the Last swing adjustment
    high_low[swing_high_low] = np.where(
        np.isnan(high_low[swing_high_low]), 0, high_low[swing_high_low])
    # If last_sign <0: swing high, if > 0 swing low
    last_sign = np.sign(high_low[swing_high_low][-1])

    # Step 8: Instantiate last swing high and low dates
    last_slo_dt = df[df[swing_low] > 0].index.max()
    last_shi_dt = df[df[swing_high] > 0].index.max()

    # Step 9: Test for extreme values
    if (last_sign == -1) & (last_shi_dt !=
                            df[last_slo_dt:][swing_high].idxmax()):
        # Reset swing_high to nan
        df.loc[last_shi_dt, swing_high] = np.nan
    elif (last_sign == 1) & \
            (last_slo_dt != df[last_shi_dt:][swing_low].idxmax()):
        # Reset swing_low to nan
        df.loc[last_slo_dt, swing_low] = np.nan

    return (df)


# Calculate regime floor ceiling
def regime_fc(df, close, swing_low, swing_high, threshold, t_dev):
    # 1. copy swing lows and highs to a smaller df called regime
    regime = df[(df[swing_low] > 0) | (df[swing_high] > 0)
                ][[close, swing_low, swing_high]]

    # 2. calculate volatility from main df and populate regime df
    stdev = 'stdev'
    regime[stdev] = rolling_stdev(df=df, price=close, t_dev=t_dev, min_per=1)

    # 3. Variables declaration
    floor_ix, ceiling_ix, floor_test, ceiling_test = [], [], [], []

    ceiling_found = False
    floor_found = False

    # 4.  instantiate columns based on absolute or relative series
    if str(close)[
            0] == 'r':  # a) test the first letter of the cl input variable
        # if 1st letter =='r', relative series, add 'r_' prefix
        rg_cols = [
            'r_floor',
            'r_ceiling',
            'r_regime_change',
            'r_regime_floorceiling',
            'r_floorceiling',
            'r_regime_breakout']
    else:  # absolute series
        rg_cols = [
            'floor',
            'ceiling',
            'regime_change',
            'regime_floorceiling',
            'floorceiling',
            'regime_breakout']

    # b) instantiate columns by concatenation
    regime = pd.concat([regime,  # existing df
                        # temporary df with same index, regime columns
                        # initialised at nan
                        pd.DataFrame(
                            np.nan,
                            index=regime.index,
                            columns=rg_cols)],  # temp df
                       axis=1)  # along the vertical axis

    # c) column variables names instantiation via a list comprehension
    floor, ceiling, regime_change, regime_floorceiling, floorceiling, regime_breakout = [
        list(rg_cols)[n] for n in range(len(rg_cols))]

    # 5. Range initialisation to 1st swing
    floor_ix = regime.index[0]
    ceiling_ix = regime.index[0]

    # 6. Loop through swings
    for i in range(1, len(regime)):

        if regime[swing_high][i] > 0:  # ignores swing lows
            # highest swing high from range[floor_ix:swing[i]]
            top = regime[floor_ix:regime.index[i]][swing_high].max()
            ceiling_test = round(
                (regime[swing_high][i] - top) / regime[stdev][i],
                1)  # test vs highest

            if ceiling_test <= -threshold:  # if swing <= top - x * stdev
                ceiling = regime[floor_ix:regime.index[i]
                                 ][swing_high].max()  # ceiling = top
                ceiling_ix = regime[floor_ix:regime.index[i]
                                    ][swing_high].idxmax()  # ceiling index
                regime.loc[ceiling_ix, ceiling] = ceiling  # assign ceiling

                if not ceiling_found:  # test met == ceiling found
                    rg_chg_ix = regime[swing_high].index[i]
                    dun_rg_chg = regime[swing_high][i]
                    # prints where/n ceiling found
                    regime.loc[rg_chg_ix, regime_change] = dun_rg_chg
                    regime.loc[rg_chg_ix,
                               regime_floorceiling] = -1  # regime change
                    # used in floor/ceiling breakout test
                    regime.loc[rg_chg_ix, floorceiling] = ceiling

                    # forces alternation btwn Floor & ceiling
                    ceiling_found = True
                    floor_found = False

        if regime[swing_low][i] > 0:  # ignores swing highs
            # lowest swing low from ceiling
            bottom = regime[ceiling_ix:regime.index[i]][swing_low].min()
            floor_test = round(
                (regime[swing_low][i] - bottom) / regime[stdev][i],
                1)  # test vs lowest

            if floor_test >= threshold:  # if swing > bottom + n * stdev
                floor = regime[ceiling_ix:regime.index[i]
                               ][swing_low].min()  # floor = bottom
                floor_ix = regime[ceiling_ix:regime.index[i]
                                  ][swing_low].idxmin()
                regime.loc[floor_ix, floor] = floor  # assign floor

                if not floor_found:  # test met == floor found
                    rg_chg_ix = regime[swing_low].index[i]
                    dun_rg_chg = regime[swing_low][i]
                    # prints where/n floor found
                    regime.loc[rg_chg_ix, regime_change] = dun_rg_chg
                    regime.loc[rg_chg_ix,
                               regime_floorceiling] = 1  # regime change
                    # used in floor/ceiling breakdown test
                    regime.loc[rg_chg_ix, floorceiling] = floor

                    # forces alternation btwn floor/ceiling
                    ceiling_found = False
                    floor_found = True

    # 7. join regime to df

    # 8. drop rg_cols if already in df to avoid overlap error
    # drop columns if already in df before join, otherwise overlap error
    if regime_floorceiling in df.columns:
        df = df.drop(rg_cols, axis=1)
    df = df.join(regime[rg_cols], how='outer')

    # 9. forward fill regime 'rg_fc','rg_chg','fc', then fillna(0) from start
    # to 1st value
    df[regime_floorceiling] = df[regime_floorceiling].fillna(
        method='ffill').fillna(0)  # regime
    df[regime_change] = df[regime_change].fillna(
        method='ffill').fillna(0)  # rg_chg
    df[floorceiling] = df[floorceiling].fillna(
        method='ffill').fillna(0)  # floor ceiling continuous line

    # 10. test reakout/down: if price crosses floor/ceiling, regime change
    # look for highest close for every floor/ceiling
    close_max = df.groupby([floorceiling])[close].cummax()
    # look for lowest close for every floor/ceiling
    close_min = df.groupby([floorceiling])[close].cummin()

    # 11. if rgme bull: assign lowest close, elif bear: highest close
    rgme_close = np.where(
        df[floorceiling] < df[regime_change],
        close_min,
        np.where(
            df[floorceiling] > df[regime_change],
            close_max,
            0))

    # subtract from floor/ceiling & replace nan with 0
    df[regime_breakout] = (rgme_close - df[floorceiling]).fillna(0)
    # if sign == -1 : bull breakout or bear breakdown
    df[regime_breakout] = np.sign(df[regime_breakout])
    df[regime_change] = np.where(
        np.sign(
            df[regime_floorceiling] *
            df[regime_breakout]) == -
        1,
        df[floorceiling],
        df[regime_change])  # re-assign fc
    df[regime_floorceiling] = np.where(
        np.sign(
            df[regime_floorceiling] *
            df[regime_breakout]) == -
        1,
        df[regime_breakout],
        df[regime_floorceiling])  # rgme chg

    return df


# Calculate rolling standard deviation
def rolling_stdev(df, price, t_dev, min_per):
    '''
    Rolling volatility rounded at 'decimals', starting at percentage 'min_per'
    of window 't_dev'
    '''
    df[price].apply(lambda x: float(x))
    stdev = df[price].rolling(
        window=t_dev,
        min_periods=int(
            round(
                t_dev *
                min_per,
                0))).std(
        ddof=0)
    return stdev


# Calculates the returns
def returns(prices):
    '''
    calculates log returns based on price series
    '''
    rets = pd.Series(prices)
    log_returns = np.log(rets / rets.shift(1))
    return log_returns


# Calculate simple moving average
def sma(df, price, ma_per, min_per):
    '''
    Returns the simple moving average.
    price: column within the df
    ma_per: moving average periods
    min_per: minimum periods (expressed as 0<pct<1) to calculate moving average
    decimals: rounding number of decimals
    '''
    sma = df[price].rolling(
        window=ma_per,
        min_periods=int(
            round(
                ma_per *
                min_per,
                0))).mean()
    return sma


def cum_return_percent(returns):
    '''
    Calculates cumulative returns and returns as percentage
    '''
    rets = pd.Series(returns)
    cum_log_returns = round((rets.cumsum().apply(np.exp) - 1) * 100, 1)
    return cum_log_returns


def signal_fcstmt(regime, st, mt):

    # Calculate the sign of the stmt delta
    stmt_sign = np.sign((st - mt).fillna(0))

    # Calculate entries/exits based on regime and stmt delta
    active = np.where(np.sign(regime * stmt_sign) == 1, 1, np.nan)
    signal = regime * active

    return signal


def stop_loss(signal, close, s_low, s_high):

    # Stop loss calculation
    stoploss = (s_low.add(s_high, fill_value=0)).fillna(
        method='ffill')  # join all swings in 1 column
    stoploss[~((np.isnan(signal.shift(1))) & (~np.isnan(signal)))
             ] = np.nan  # keep 1st sl by signal
    # Extend first value with fillna
    stoploss = stoploss.fillna(method='ffill')

    # Bull: lowest close, Bear: highest close
    close_max = close.groupby(stoploss).cummax()
    close_min = close.groupby(stoploss).cummin()

    if len(close_min) == 0:
        pass
    else:
        cum_close = np.where(signal == 1, close_min,
                             np.where(signal == -1, close_max, 0))

        # Reset signal where stop loss is breached
        sl_delta = (cum_close - stoploss).fillna(0)
        sl_sign = signal * np.sign(sl_delta)
        signal[sl_sign == -1] = np.nan

    return stoploss


def rebalance(context, data):
    """
        A function to rebalance the portfolio. This function is called by the
        schedule_function in the initialize function.
    """
    try:
        # Fetch lookback no. days data for the security
        stock = data.history(
            context.security_sym,
            ['open', 'high', 'low', 'close'],
            context.lookback,
            '1d')
    except IndexError:
        return
        
    benchmark = data.history(
        context.benchmark_sym,
        ['close'],
        context.lookback,
        '1d')

    benchmark.columns = [context.benchmark_sym.symbol]

    # Create a relative series
    new = relative(stock_dataframe=stock, benchmark_dataframe=benchmark,
                   benchmark_name='SPY', start=None, end=None)

    # Calculate the swings
    new = swings(
        df=new,
        high='rebased_high',
        low='rebased_low',
        argrel_window=20)

    # Calculate the stock regime
    new = regime_fc(df=new, close='rebased_close', swing_low='srebased_low',
                    swing_high='srebased_high', threshold=1.5, t_dev=63)

    # Calculate returns for the relative closed price
    new['r_return_1d'] = returns(new['rebased_close'])

    # Calculate returns for the absolute closed price
    new['return_1d'] = returns(new['close'])

    # Create dataframe
    data = pd.DataFrame()
    data[['rebased_close',
          'close',
          'r_return_1d',
          'return_1d',
          'r_regime_floorceiling',
          'srebased_low',
          'srebased_high']] = new[['rebased_close',
                                   'close',
                                   'r_return_1d',
                                   'return_1d',
                                   'r_regime_floorceiling',
                                   'srebased_low',
                                   'srebased_high']]

    # Calculate moving averages
    st_mt = str(context.st) + ' ' + str(context.mt)
    r_st_ma = sma(df=data, price='rebased_close',
                  ma_per=context.st, min_per=1)
    r_mt_ma = sma(df=data, price='rebased_close',
                  ma_per=context.mt, min_per=1)

    # Calculate positions based on regime and moving average crossovers
    data['s_' + st_mt] = signal_fcstmt(
        regime=data['r_regime_floorceiling'], st=r_st_ma, mt=r_mt_ma)

    data['stop_loss_' + st_mt] = stop_loss(signal=data['s_' + st_mt],
                                           close=data['rebased_close'],
                                           s_low=data['srebased_low'],
                                           s_high=data['srebased_high'])

    signal_latest = data['s_' + st_mt][-1]

    # Place orders
    if signal_latest == 1:
        print("{} Going long on {}".format(get_datetime(), context.security_sym))
        order_target_percent(context.security_sym, 1)
    elif signal_latest == -1:
        print("{} Going short on {}".format(get_datetime(), context.security_sym))
        order_target_percent(context.security_sym, -1)
    else:
        order_target_percent(context.security_sym, 0)