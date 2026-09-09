# For data manipulation
import numpy as np
import pandas as pd
from datetime import timedelta
from scipy.optimize import minimize

# For technical indicator values calculation
import talib

# Get options data
def get_contract(context, strike, option_type):
    option_symbol = superSymbol(
        secType='OPT',
        symbol=context.symbol,
        exchange='NSE',
        currency='INR',
        expiry=context.expiry,
        strike=strike,
        right=option_type)

    return option_symbol

# Estimate GARCH(1,1) Parameters Using Log-Likelihood Function                      
def garch_likelihood(parameters, returns, parkinson):
    gamma = parameters[0]
    alpha = parameters[1]
    beta = parameters[2]

    # Initialize the log-likelihood and initial volatility
    log_likelihood = 0

    # Calculate the log-likelihood
    for t in range(1, len(returns)):
        sigma2 = gamma * parkinson[0] + alpha * \
            returns[t-1]**2 + beta * parkinson[t]
        log_likelihood += -np.log(sigma2) - returns[t]**2 / sigma2

    return -log_likelihood

# Function to forecast volatility using GARCH(1,1)
def forecast_volatility(parameters, returns, parkinson):
    gamma = parameters[0]
    alpha = parameters[1]
    beta = parameters[2]

    # Calculate the forecasted volatility for the subsequent month
    forecasted_volatility = gamma * parkinson[0] + alpha * returns[-1]**2 + beta * parkinson[-1]

    return forecasted_volatility

# Function to close all open positions
def close_out(context, data):
    positions = context.portfolio.positions
    if positions:
        for asset in positions:
            order(asset, 0)       

def initialize(context):
    """
        A function to define things to do at the start of the strategy
    """
    
    # Define assets
    context.stock = superSymbol(
        secType='FUT',
        symbol='NIFTY50',
        exchange='NSE',
        currency='INR',
        expiry='20230727',
        includeExpired=True)

    context.atm_call = 0
    context.atm_put = 0
    context.lookback = 100
    context.forecasted_volatility = 0
    context.atm_strike = 0
    context.strike_difference = 50
    
    # Call rebalance function on the last trading day of each week after 30 minutes from market open
    schedule_function(rebalance,
                    date_rules.week_end(days_offset=0),
                    time_rules.market_open(hours=0, minutes=30))

    # Call enter function on the last trading day of the week (1 hour after market open)
    schedule_function(
        enter, date_rules.week_end(days_offset=0), 
        time_rules.market_open(hours=1))

    # Call close_out function on the last trading day of the week (30 mins before market close)
    schedule_function(
            close_out, date_rules.week_end(days_offset=1), 
            time_rules.market_close(hours=0, minutes=30))


def rebalance(context,data):

    data_daily = data.history(context.stock, ['open', 'high', 'low', 'close'],
                              context.lookback, '1d') 

    # Create 'ohlc_dict' dictionary
    ohlc_dict = {'open': 'first', 'high': 'max', 'low': 'min', 'close': 'last'}

    # Resample daily_data_SP500 to weekly data
    weekly_data = data_daily.resample('W', offset="-1d").agg(ohlc_dict)

    # Remove any missing values
    weekly_data = weekly_data.dropna()

    # Compute the Parkinson's volatility estimator using high and low prices
    high = weekly_data['high']
    low = weekly_data['low']

    # Calculate the Parkinson volatility using the extracted 'High' and 'Low' values
    parkinson_volatility = 1 / (4 * np.log(2)) * np.sqrt((np.log(high / low) ** 2)) * np.sqrt(52)

    # Calculate weekly log returns
    weekly_returns = np.log(weekly_data['close'] / weekly_data['close'].shift(1)).dropna()

    # Define the initial parameter values and bounds for optimization
    initial_parameters = [0.1, 0.1, 0.1]  # [alpha, beta, gamma]

    # Bounds for alpha, beta, and gamma
    parameter_bounds = [(0, 1), (0, 1), (0, 1)]

    # Minimize the negative log-likelihood to estimate the GARCH(1,1) parameters
    result = minimize(garch_likelihood, initial_parameters, args=(weekly_returns, parkinson_volatility), bounds=parameter_bounds, method='SLSQP')
    
    # Extract the estimated parameters
    estimated_parameters = result.x

    # Using the estimated GARCH(1,1) parameters and returns array from the previous code
    # Square of the last observed return
    last_observed_volatility = weekly_returns[-1]**2  

    # Forecast volatility for the subsequent month
    context.forecasted_volatility = forecast_volatility(estimated_parameters, weekly_returns, parkinson_volatility)

    context.atm_strike = (round(weekly_data['close'] / context.strike_difference) * context.strike_difference)[-1]

# Function to enter the trade
def enter(context, data):
    forecast = context.forecasted_volatility
    context.atm_call = get_contract(context, context.atm_strike, 'C')
    context.atm_put = get_contract(context, context.atm_strike, 'P')

    # Current ATM call IV
    call_atm_iv = get_option_info(context.atm_call, "impliedVol")

    # Current ATM put IV
    put_atm_iv = get_option_info(context.atm_put, "impliedVol")

    # Condition for trading long straddle
    if (forecast > call_atm_iv) and (forecast > put_atm_iv):
        print(f"{get_datetime()} Entering long straddle")
        close_out(context, data)

        # Place order
        order_target(context.atm_call, 50)
        order_target(context.atm_put, 50) 

    # Condition for trading short straddle
    elif (forecast < call_atm_iv) and (forecast < put_atm_iv):
        print(f"{get_datetime()} Entering short straddle")
        close_out(context, data)

        # Place order
        order_target(context.atm_call, -50)
        order_target(context.atm_put, -50)