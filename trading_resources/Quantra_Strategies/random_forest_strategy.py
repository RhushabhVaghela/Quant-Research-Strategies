"""
    Title: Random Forest Classifier Strategy
    Description: This is a long only strategy. The random forest classification
    model is used to predict the trading action for the selected asset.
    Dataset: US Equities

    ############################# DISCLAIMER #############################
    This is a strategy template only and should not be
    used for live trading without appropriate backtesting and tweaking of
    the strategy parameters.
    ######################################################################
"""

# For data manipulation
import numpy as np
# Library for technical indicators
import talib as ta
# Import sklearn's train-test split module
from sklearn.model_selection import train_test_split
# Libraries for evaluating the model
from sklearn.metrics import classification_report
# Import sklearn's Random Forest Classifier
from sklearn.ensemble import RandomForestClassifier
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
    context.security = symbol('NFLX')

    # The lookback for historical data
    context.lookback = 990

    # The train-test split
    context.split_ratio = 0.80

    # The machine learning regressor accuracy
    context.accuracy = None
    
    # Create the machine learning model
    context.rf_model = RandomForestClassifier(
        n_estimators=3, max_features=3, max_depth=2, random_state=4)
    
    # Schedule the rebalance function every day
    schedule_function(
                        rebalance,
                        date_rule=date_rules.every_day(),
                        time_rule=time_rules.market_close(minutes=5)
                     )
         
"""
Function to resample the minute data into 15-minute data.
"""
def resample_min_data(raw_data):
    # Mapper for resampling
    mapper = {
                'open': 'first',
                'high': 'max',
                'low': 'min',
                'close': 'last',
             }

    # Resample price data to hourly frequency
    resampled_data = raw_data.resample(
        '15min', label='right', closed='right').agg(mapper).dropna()   

    # Return the resampled data
    return resampled_data


"""
Function to get the features and the target from the data.
"""
def get_features_target(asset_data):
    # Create a column 'future_returns' with the calculation of percentage change
    asset_data['future_returns'] = asset_data['close'].pct_change().shift(-1)
    
    # Create the signal column
    asset_data['signal'] = np.where(asset_data['future_returns'] > 0, 1, 0)

    # Create a column 'pct_change' with the 15-minute prior percentage change
    asset_data['pct_change'] = asset_data['close'].pct_change()
    
    # Create a column 'pct_change2' with the half an hour prior percentage change
    asset_data['pct_change2'] = asset_data['close'].pct_change(2)
    
    # Create a column 'pct_change5' with the 75-minute prior percentage change
    asset_data['pct_change5'] = asset_data['close'].pct_change(5)
    
    # Create a column by the name RSI, and assign the RSI values to it
    asset_data['rsi'] = ta.RSI(asset_data['close'].values, timeperiod=int(6.5*4))

    # Create a column by the name ADX, and assign the ADX values to it
    asset_data['adx'] = ta.ADX(asset_data['high'].values, asset_data['low'].values,
                         asset_data['open'].values, timeperiod=int(6.5*4))
                         
    # Create a column by the name sma, and assign the SMA values to it
    asset_data['sma'] = asset_data['close'].rolling(window=int(6.5*4)).mean()

    # Create a column by the name corr, and assign the correlation values to it
    asset_data['corr'] = asset_data['close'].rolling(window=int(6.5*4)).corr(asset_data['sma'])
    
    # Calculate volatility
    asset_data['volatility'] = asset_data.rolling(
        int(6.5*4), min_periods=int(6.5*4))['pct_change'].std()*100
        
    # Drop the missing values
    asset_data.dropna(inplace=True)

    # Target
    y = asset_data[['signal']].copy()
    
    # Features
    X = asset_data[['pct_change', 'pct_change2', 'pct_change5', 'rsi',
           'adx', 'corr', 'volatility']].copy()
    
    # Return the features and target
    return X, y

    
def rebalance(context, data):
    """
        A function to rebalance the portfolio. This function is called by the
        schedule_function in the initialize function.
    """
    
    # Fetch lookback no. days data for the security
    try:
        minute_data = data.history(
            context.security,
            ['high', 'low', 'open', 'close'],
            context.lookback,
            '1m')
    except IndexError:
        return
    
    # Resample the data to 15-minute frequency
    resampled_data = resample_min_data(minute_data)
    
    # Get the features and target
    X, y = get_features_target(resampled_data)
    
    # Get the data after train-test split
    try:
            X_train, X_test, y_train, y_test = train_test_split(X,
                                                        y,
                                                        train_size=context.split_ratio,
                                                        shuffle=False)
    
    except ValueError:
        return
    
    # Fit the model on the training data
    context.rf_model.fit(X_train, y_train['signal'])
    
    # Use the model and predict the values for the test data
    y_pred = context.rf_model.predict(X_test)
    
    # Get the latest signal
    latest_signal = y_pred[-1]
    print("{} Signal value {}".format(get_datetime(), latest_signal))

    
    # Place the orders
    # Place a long order if the model prediction is 1
    if latest_signal == 1:
        order_target_percent(context.security, 1)
    # Keep no position if the model predicts 0
    else:
        order_target_percent(context.security, 0)
