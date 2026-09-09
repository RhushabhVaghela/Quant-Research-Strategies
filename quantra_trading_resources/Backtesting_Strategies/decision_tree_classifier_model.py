"""
    Title: Sample Decision Tree Classifier Model
    Description: This is a decision tree classifier model which predicts next day's
                 price movement. This is a long only strategy which rebalances 
                 the portfolio weights every day and retrains model every month.
    Style tags: Systematic
    Asset class: Equities
    Dataset: NSE

    ############################# DISCLAIMER #############################
    This is a strategy template only and should not be
    used for live trading without appropriate backtesting and tweaking of
    the strategy parameters.
    ######################################################################
"""
# Import numpy
import numpy as np

# Import talib
import talib as ta

# Import machine learning libraries
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score

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
    context.security = symbol('ACC')

    # Lookback to fetch data
    context.lookback = 200

    # The train-test split
    context.split_percentage = 0.8

    # Variable to store train and test dataset
    context.X_train = None
    context.X_test = None
    context.y_train = None
    context.y_test = None

    # The flag variable is used to check whether to retrain the model or not
    context.retrain_flag = True

    # The variable to store the classifier
    context.clf = None

    # Schedule the retrain_model function every month
    schedule_function(
        retrain_model,
        date_rule=date_rules.month_start(),
        time_rule=time_rules.market_open()
    )

    # Schedule the rebalance function to run daily at market close
    schedule_function(
        rebalance,
        date_rule=date_rules.every_day(),
        time_rule=time_rules.market_close()
    )


def retrain_model(context, data):
    """
        A function to retrain the  model. This function is called by
        the schedule_function in the initialize function.
    """
    context.retrain_flag = True


def rebalance(context, data):
    try:
        df = data.history(
            context.security,
            ['open', 'high', 'low', 'close', 'volume'],
            context.lookback,
            '1d')
    except IndexError:
        return

    # Create predictor variables and a target variable
    df['ADX'] = ta.ADX(df['high'].values, df['low'].values,
                       df['close'].values, timeperiod=14)
    df['RSI'] = ta.RSI(df['close'].values, timeperiod=14)
    df['SMA'] = ta.SMA(df['close'].values, timeperiod=20)

    df['Return'] = df['close'].pct_change(1).shift(-1)
    df['target'] = np.where(df.Return > 0, 1, 0)

    # Drop NAN values
    df = df.dropna()

    # Store all predictor variables in a variable X
    predictors_list = ['ADX', 'RSI', 'SMA']
    X = df[predictors_list]

    if context.retrain_flag:
        context.retrain_flag = False

        # Store target variable in y
        y = df.target

        # Split the data into train and test dataset
        split = int(context.split_percentage*len(X))

        context.X_train = X[:split]
        context.X_test = X[:split]

        context.y_train = y[:split]
        context.y_test = y[:split]

        # Create classification tree model
        context.clf = DecisionTreeClassifier(
            criterion='gini', max_depth=3, min_samples_leaf=5)
        context.clf = context.clf.fit(context.X_train, context.y_train)

    # Test accuracy
    accuracy_test = accuracy_score(context.y_test, 
                                   context.clf.predict(context.X_test))

    # Predicted Signal
    y_pred = context.clf.predict(context.X_test)[-1]
    print("{} Accuracy test: {}, Prediction: {}".format(
        get_datetime(), accuracy_test, y_pred))

    # Place the orders
    if accuracy_test > 0.5:
        if y_pred == 1:
            order_target_percent(context.security, 1)
        else:
            order_target_percent(context.security, 0)
    else:
        order_target_percent(context.security, 0)