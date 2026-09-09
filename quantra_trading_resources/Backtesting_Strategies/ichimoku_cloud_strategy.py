"""
    Title: Sample Ichimoku Cloud Strategy
    Description: This is a long only strategy based on the Ichimoku cloud.
    The Ichimoku Cloud, also known as Ichimoku Kino Hyo is a technical indicator, 
    which consists of five plots and a cloud. 
    Style tags: Systematic
    Asset class: Cryptocurrencies
    Data requirement: Data subscription is required for crytp data feed.

    ############################# DISCLAIMER #############################
    This is a strategy template only and should not be
    used for live trading without appropriate backtesting and tweaking of
    the strategy parameters.
    ######################################################################
"""

def initialize(context):

    # Define symbol
    context.security = symbol('BTC')
    context.position = 0

    schedule_function(
            rebalance,
            date_rule=date_rules.every_day(),
            time_rule=time_rules.market_close()
        )


def rebalance(context, data):

    data = data.history(
        context.security, ['open', 'high', 'low', 'close'], 120, '1d')

    # Conversion line
    high_20 = data.high.rolling(20).max()
    low_20 = data.low.rolling(20).min()
    data['conversion_line'] = (high_20 + low_20) / 2

    # Base line
    high_60 = data.high.rolling(60).max()
    low_60 = data.low.rolling(60).min()
    data['base_line'] = (high_60 + low_60) / 2

    # Leading span A
    data['leading_span_A'] = (
        (data.conversion_line + data.base_line) / 2).shift(30)

    # Leading span B
    high_120 = data.high.rolling(120).max()
    low_120 = data.low.rolling(120).min()
    data['leading_span_B'] = ((high_120 + low_120) / 2).shift(30)

    # Lagging span
    data['lagging_span'] = data.close.shift(-30)

    # Prices are above the cloud
    condition_1 = (data.close[-1] > data.leading_span_A[-1]
                   ) and (data.close[-1] > data.leading_span_B[-1])

    # Leading Span A (senkou_span_A) is rising above the leading span B (senkou_span_B)
    condition_2 = (data.leading_span_A[-1] > data.leading_span_B[-1])

    # Conversion Line (tenkan_sen) moves above Base Line (kijun_sen)
    condition_3 = (data.conversion_line[-1] > data.base_line[-1])

    # Long entry
    long_entry = condition_1 and condition_2 and condition_3

    # Prices are below the cloud
    condition_4 = (data.close[-1] < data.leading_span_A[-1]
                   ) and (data.close[-1] < data.leading_span_B[-1])

    # Leading Span A (senkou_span_A) is falling below the leading span B (senkou_span_B)
    condition_5 = (data.leading_span_A[-1] < data.leading_span_B[-1])

    # Conversion Line (tenkan_sen) moves below Base Line (kijun_sen)
    condition_6 = (data.conversion_line[-1] < data.base_line[-1])

    # Long exit
    long_exit = condition_4 and condition_5 and condition_6

    # Place the order
    if long_entry and context.position == 0:
        order_target_percent(context.security, 1)
        context.position = 1

    elif long_exit and context.position == 1:
        order_target_percent(context.security, 0)
        context.position = 0
