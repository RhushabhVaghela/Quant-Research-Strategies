"""
    Title: Sample MLP Classifier Trading Strategy 
    Description: The strategy will implement a classification model using 
                 Multi-layer Perceptron (MLP) classifier. This is a long only 
                 strategy which rebalances portfolio weights daily and retrains
                 model every month. 
    Style tags: Systematic
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

# Import machine learning libraries
from sklearn.preprocessing import StandardScaler
from sklearn.neural_network import MLPClassifier
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
    context.security = symbol('AMZN')

    # Lookback to fetch data
    context.lookback = 200

    # The flag variable used to check whether to retrain the model or not
    context.retrain_flag = True

    # Instantiate the StandardScaler
    context.scaler = StandardScaler()

    # Variable to store train and test dataset
    context.X_train = None
    context.X_test = None
    context.y_train = None
    context.y_test = None

    # The variable to store the classifier
    context.mlp = None

    # Schedule the retrain_model function every month
    schedule_function(
        retrain_model,
        date_rule=date_rules.month_start(),
        time_rule=time_rules.market_open()
    )

    # Schedule the rebalance function to run daily at the market close
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
        data = data.history(
            context.security,
            ['open', 'high', 'low', 'close', 'volume'],
            context.lookback,
            '1d')
    except IndexError:
        return
    # Create predictor variables and a target variable

    # Returns
    data['ret1'] = data['close'].pct_change()
    data['ret5'] = data.ret1.rolling(5).sum()

    # Standard Deviation
    data['std5'] = data.ret1.rolling(5).std()

    # Volume by ADV20
    data['volume_by_adv20'] = data['volume']/data.volume.rolling(20).mean()

    # High - low
    data['H-L'] = data['high'] - data['low']

    # Open - Close
    data['O-C'] = data['close'] - data['open']

    # Future returns
    data['retFut1'] = data.ret1.shift(-1)

    # Drop NAN values
    data = data.dropna()

    # Define predictor variables (X)
    data = data.dropna()
    predictor_list = ['H-L', 'O-C', 'ret5', 'std5', 'volume_by_adv20']
    X = data[predictor_list]

    if context.retrain_flag:
        context.retrain_flag = False

        # Store target variable in y
        y = np.where(data.retFut1 > 0.0, 1.0, 0)
        
        # Split the data into train and test dataset
        train_length = int(len(data)*0.80)

        context.X_train = X[:train_length]
        context.X_test = X[train_length:]

        context.y_train = y[:train_length]
        context.y_test = y[train_length:]

        # Create the scaler model using train data
        context.scaler.fit(context.X_train)
        
        # Transform the training and test data using the scaler model created above
        context.X_train = context.scaler.transform(context.X_train)
        context.X_test = context.scaler.transform(context.X_test)
        
        # Create classification tree model
        # Seed is initialized to 1
        seed = 1

        # Create the MLPClassifier model
        context.mlp = MLPClassifier(activation='logistic', hidden_layer_sizes=(
            19,), random_state=seed, solver='sgd')

        # Fit the model on train dataset
        context.mlp.fit(context.X_train, context.y_train)

    # Test accuracy
    accuracy_test = accuracy_score(context.y_test, 
                                   context.mlp.predict(context.X_test))
    
    # Predicted Signal
    data['predicted_signal'] = context.mlp.predict(X)

    print("{} Check long or hold {}".format(get_datetime(), data['predicted_signal'][-1]))
    
    # Place the orders
    if accuracy_test > 0.5:
        if data['predicted_signal'][-1] == 1:
            print("{} Going long or hold {}".format(get_datetime(), context.security))
            order_target_percent(context.security, 1)
        else:
            order_target_percent(context.security, 0)
    else:
        order_target_percent(context.security, 0)