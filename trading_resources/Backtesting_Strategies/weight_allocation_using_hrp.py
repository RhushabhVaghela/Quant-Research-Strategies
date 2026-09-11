"""
    Title: Weight allocation using Hierarchical Risk Parity (HRP)
    Description: Hierarchical Risk Parity (HRP) is a portfolio 
    construction method that uses hierarchical clustering to 
    group similar assets and optimally allocates weights. The 
    HRP weights are calculated monthly from the asset returns.
    Dataset: US Equities

    ############################# DISCLAIMER #############################
    This is a strategy template only and should not be
    used for live trading without appropriate backtesting and tweaking of
    the strategy parameters.
    ######################################################################
"""

# Import numpy, pandas and cvxpy libraries
import numpy as np
import pandas as pd

# Library to scale data
from sklearn.preprocessing import StandardScaler

# Library for AgglomerativeClustering
from sklearn.cluster import AgglomerativeClustering

# Import blueshift libraries
from blueshift.api import (
                            symbol,
                            symbols,
                            order_target_percent,
                            schedule_function,
                            date_rules,
                            time_rules,
                            get_datetime
                        )


def initialize(context):

    # Define symbols
    context.security_list = [symbol('AMZN'),
                    symbol('VLO'),
                    symbol('GOOG'),
                    symbol('NOC'),
                    symbol('KR'),
                    symbol('ORLY'),
                    symbol('EXPE'),
                    symbol('EQIX'),
                    symbol('TMUS'),
                    symbol('NFLX'),
                    symbol('DIS'),
                    symbol('NKE'),
                    symbol('EA'),
                    symbol('MDLZ'),
                    symbol('ATVI'),
                    symbol('NVDA'),
                ]

    # The lookback for the historical data
    context.lookback = 225

    # Dataframe with all the securities and their weights
    # Weights are assigned 0 right now
    context.weights_hrp = pd.DataFrame([1]*len(context.security_list), index=context.security_list, columns=['HRP'])

    # Schedule the rebalance function
    schedule_function(
                        rebalance,
                        date_rule=date_rules.month_start(),
                        time_rule=time_rules.market_close(minutes=30)
                     )

# Function to scale the data
def scale_data(df):
    # Standardising the dataset using StandardScaler
    scaler = StandardScaler()
    scaled_array = scaler.fit_transform(df)
    df = pd.DataFrame(scaled_array, index=df.index, columns=df.columns)

    # Returning scaled data
    return df

# Function to calculate cluster volatility
def calculate_cluster_volatility(returns_data, tickers):

    # Calculating the volatility of stocks in the tickers list
    vol = returns_data[tickers].std()

    # Calculate the weights of stocks using inverse volatility method
    weights = (1/vol)/np.sum(1/vol)

    # Multiply the returns data with weights calculated
    cluster_returns = returns_data[tickers].dot(weights)

    # Calculate the volatility of cluster
    cluster_volatility = cluster_returns.std()

    return cluster_volatility


def hrp_weights(context, data, tickers, dataset, returns_data):

    if len(tickers) > 1:

        # Filtering the stocks in the dataset
        filter_dataset = dataset.loc[tickers]

        # Hierarchical clustering using agglomerative clustering

        # Generate two clusters (cluster_0 and cluster_1) using euclidean distance and ward linkage method
        cluster = AgglomerativeClustering(
            n_clusters=2, affinity='euclidean', linkage='ward')

        output = cluster.fit_predict(filter_dataset)
        
        # Get cluster 0 tickers
        cluster_0 = filter_dataset.loc[output == 0,:].index
        
        # Get cluster 1 tickers
        cluster_1 = filter_dataset.loc[output != 0,:].index

        # Get weight allocation factor for cluster_0 and cluster_1
        factor_0 = 1 - calculate_cluster_volatility(returns_data, cluster_0)/(calculate_cluster_volatility(
            returns_data, cluster_0) + calculate_cluster_volatility(returns_data, cluster_1))

        factor_1 = 1 - factor_0

        # Multiply the weights of tickers in 'weights_hrp' dataframe with respective allocation factors
        context.weights_hrp.loc[cluster_0, 'HRP'] *= factor_0
        context.weights_hrp.loc[cluster_1, 'HRP'] *= factor_1
        
        # Run the clustering algorithm on the new clusters
        # use the list above
        hrp_weights(context, data, cluster_0, dataset, returns_data)
        hrp_weights(context, data, cluster_1, dataset, returns_data)


def rebalance(context, data):
    """
        A function to rebalance the portfolio. This function is called by the
        schedule_function in the initialize function above.
    """

    try:
        # Fetch lookback no. days data for the first security
        df = data.history(
            context.security_list,
            'close',
            context.lookback,
            '1d')
    except IndexError:
        return df

    # Create a dataframe with percentage change of close prices
    returns_data = df.pct_change()
    
    # Scale the data
    returns_data = scale_data(returns_data)

    # Drop null values
    returns_data = returns_data.dropna()

    # Transpose the return data dataframe
    dataset = returns_data.T

    # Reinitialize context.weights_hrp so that it does not have old weights
    context.weights_hrp = pd.DataFrame([1]*len(context.security_list), index=context.security_list, columns=['HRP'])

    # Call hrp_weights function to allocate weights to the securities
    hrp_weights(context, data, context.security_list, dataset, returns_data)
    
    # Rebalancing the portfolio
    for security in context.security_list:
        order_target_percent(security,
                             context.weights_hrp.loc[security, 'HRP'])

        print("{} Security {} weights: {}".format(get_datetime(), 
                security,
                context.weights_hrp.loc[security, 'HRP']))