"""
    Title: Sample Value Strategy in Forex
    Description: This is a long only strategy which rebalances the 
        portfolio weights at the end of the month.
    Style tags: Systematic
    Asset class: Forex
    Dataset: Forex and REER 
"""


def initialize(context):

    # Define Symbol. You need data subscription to fetch symbols.
    context.secList = [symbol('CASH, SGD, USD'),
                       symbol('CASH, AUD, USD'),
                       symbol('CASH, CAD, USD'),
                       symbol('CASH, CHF, USD'),
                       symbol('CASH, GBP, USD'),
                       symbol('CASH, JPY, USD'),
                       symbol('CASH, NZP, USD'),
                       symbol('CASH, EUR, USD')]

    # Call rebalance function on the month end, 5 minutes before the market close
    schedule_function(rebalance,
                      date_rules.month_end(offset),
                      time_rules.market_close(hours=0, minutes=5))


def rebalance(context, data):

    # Read Forex data
    price = data.history(context.secList, 'close', 30, '1d')

    # Read the REER data from CSV file
    # The REER data can be downloaded from the Bank for International Settlements (BIS) website
    # REER data is update by BIS once a month. Once the data published,
    # you can update the CSV file.
    reer = pd.read_csv('REER_27.csv', index_col=0)
    reer.index = pd.to_datetime(reer.index)

    # Calculate the rolling mean of reer
    reer_mean = reer.rolling(6).mean()[-1]

    # Place the order
    for security in context.secList:
        if reer[security] < reer_mean:
            order_target_percent(security, 0.1)
        elif reer[security] < reer_mean:
            order_target_percent(security, 0)