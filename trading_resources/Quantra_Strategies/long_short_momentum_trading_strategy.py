'''
    Title: Long-short Momentum Trading Strategy Template
    Description: This strategy uses past returns to long and short currency
    pairs.
    Dataset: Forex

    ############################# DISCLAIMER #############################
    This is a strategy template only and should not be
    used for live trading without appropriate backtesting and tweaking of
    the strategy parameters.
    ######################################################################
'''


# blueshift Libraries
from blueshift.api import (
                            symbol,
                            order_target_percent,
                            schedule_function,
                            date_rules,
                            time_rules,
                            set_account_currency,
                            get_datetime
                        )

def initialize(context):

    # Set base currency to USD for PnL calculations
    set_account_currency('USD')

    # Set the lookback window
    context.lookback = 50

    # Call the strategy function
    # at the start of every week 15 minutes after market open
    schedule_function(
                        strategy,
                        date_rules.week_start(),
                        time_rules.market_open(minutes=15)
                     )

    # List of currency pairs
    context.currency_list = [
                               symbol('AUD/USD'),
                               symbol('EUR/USD'),
                               symbol('GBP/USD'),
                               symbol('NZD/USD'),
                               symbol('USD/CHF'),
                               symbol('USD/CAD'),
                               symbol('USD/JPY')
                            ]


def strategy(context, data):
    """
        A function to rebalance the portfolio. This function is called by the
        schedule_function above.
    """
    try:
        # Fetch currency pairs daily price data for the last 50 trading days
        currency_data = data.history(
                                        context.currency_list,
                                        'close',
                                        context.lookback,
                                        '1d'
                                    )
    except IndexError:
        return
    # Compute returns over the lookback period
    currency_returns = currency_data.iloc[-1]/currency_data.iloc[0] - 1

    # Sort the values as per returns
    currency_returns.sort_values(ascending=False, inplace=True)
    print("{} Currency returns {}".format(get_datetime(), currency_returns))
    # Long top 3 pairs
    for s in currency_returns.index[:3]:
        order_target_percent(s, 1.0/6)

    # Short bottom 3 pairs
    for s in currency_returns.index[-3:]:
        order_target_percent(s, -1.0/6)

    # No position in the fourth currency pair
    order_target_percent(currency_returns.index[3], 0)