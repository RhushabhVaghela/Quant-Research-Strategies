"""
    Title: Gap up gap down strategy
    Description: This strategy uses past returns to go long or short
    Style tags: Momentum
    Asset class: Equities
    Dataset: US Equities
    Start date: You can start after a year from when the data is available
"""
from blueshift.finance import commission, slippage
from blueshift.api import(symbol,
                        order_target_percent,
                        order,
                        schedule_function,
                        date_rules,
                        time_rules,
                        get_datetime,
                        set_commission,
                        set_slippage,
                        )

def initialize(context):

    # Define symbol
    context.security = symbol('AMZN')

    # Define standard deviation threshold
    context.std_dev_threshold = 0.25

    # Schedule strategy logic
    schedule_function(enter_position,
                      date_rule=date_rules.every_day(),
                      time_rule=time_rules.market_open(minutes=5))

    schedule_function(square_off,
                      date_rule=date_rules.every_day(),
                      time_rule=time_rules.market_close(minutes=5))


def enter_position(context, data):

    # Fetch 1 day data for the above security
    try:
        price = data.history(context.security, ['open', 'close'], 90, '1d')
        current_open = data.current(context.security,'open')
    except IndexError:
        return

    # Calculate today's open to previous day's close
    returns = (price['open'] - price['close'].shift(1)) / \
        price['close'].shift(1)

    # Calculate standard deviation
    std_dev = returns.std()
    last_close = price['close'][-1]
    current_ret = current_open/last_close - 1
    # Long entry condition
    long_entry = current_ret > context.std_dev_threshold * std_dev

    # Short entry condition
    short_entry = current_ret < -context.std_dev_threshold * std_dev

    # Placing orders
    if long_entry:
        order_target_percent(context.security, 1)

    elif short_entry:
        order_target_percent(context.security, -1)

def square_off(context, data):

    # Exit position
    order_target_percent(context.security, 0)
