"""
    Title: Sample Buy and Hold Strategy
    Description: This is a long only strategy that rebalances the 
        portfolio weights at the start of every month.
    Style tags: Systematic
    Asset class: Equities
    Dataset: US Equities
"""
# blueshift
from blueshift.api import(symbol,
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

    # universe selection
    context.long_portfolio = [
        symbol('AMZN'),
        symbol('AAPL'),
        symbol('WMT'),
        symbol('MU'),
        symbol('BAC'),
        symbol('KO'),
        symbol('BA'),
        symbol('AXP')
    ]

    """ 
    	Call rebalance function on the first trading day of each month
        after 2.5 hours from market open
    """
       
    schedule_function(rebalance,
                      date_rules.month_start(days_offset=0),
                      time_rules.market_open(hours=2, minutes=30))

def rebalance(context, data):
    """
        A function to rebalance the portfolio is passed on to the call
        of schedule_function above.
    """

    # Position 50% of portfolio to be long in each security
    for security in context.long_portfolio:
        print("{} Going long on {}".format(get_datetime(), context.long_portfolio))
        order_target_percent(security, 1.0/10)