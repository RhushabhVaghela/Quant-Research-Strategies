"""
    Title: Sample Divergence Strategy
    Description: This is a long short strategy based on the RSI divergence.
                 In this strategy, you will calculate AroonUp and AroonDown values 
                 for the RSI values using the Aroon indicator. Then you compare these 
                 values to observe how the market's highs and lows 
                 have behaved compared with the highs and lows of the RSI.
    Data requirement: Data subscription is required for cryptocurrencies data feed

    ############################# DISCLAIMER #############################
    This is a strategy template only and should not be
    used for live trading without appropriate backtesting and tweaking of
    the strategy parameters.
    ######################################################################
"""

# Import talib 
import talib as ta

def initialize(context):

    # Define symbol
    context.security = symbol('ETHBTC')
    
    # Define lookback time period for indicators 
    context.timeperiod = 14

    # Define threshold value for the spread
    context.threshold = 75

    # Schedule strategy logic every day at the market open
    schedule_function(
            rebalance,
            date_rule=date_rules.every_day(),
            time_rule=time_rules.market_open(minutes=1))

def rebalance(context, data):

    # Fetch data
    price = data.history(
        context.security, ['open', 'high', 'low', 'close'], 60, '1d')

    # Calculate RSI indicator
    price['RSI'] = ta.RSI(price.close.values,  timeperiod=context.timeperiod)

    # Calculate Arron indicator
    price['AroonDown'], price['AroonUp'] = ta.AROON(
        price.high.values, price.low.values, timeperiod=context.timeperiod)

    # Calculate Aroon values for RSI
    price['AroonDownRSI'], price['AroonUpRSI'] = ta.AROON(
        price.RSI.values, price.RSI.values, timeperiod=context.timeperiod)

    # Calculate the Spread of AroonUp values for the price series and the RSI
    price['UpSpread'] = price.AroonUp - price.AroonUpRSI

    # Calculate the Spread of AroonDown values for the price series and the RSI
    price['DownSpread'] = price.AroonDown - price.AroonDownRSI

    # Buy signal
    if price['UpSpread'][-1] > context.threshold:
        order_target_percent(context.security, 1)

    # Sell signal
    elif price['DownSpread'][-1] > context.threshold:
        order_target_percent(context.security, -1)

    else:
        order_target_percent(context.security, 0)