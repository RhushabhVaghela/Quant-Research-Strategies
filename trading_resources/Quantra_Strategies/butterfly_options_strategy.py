import talib as ta
from datetime import datetime
import warnings
import numpy as np
import pandas as pd
from scipy.stats import rv_histogram

warnings.simplefilter('ignore')

config = {
    'stop_loss_percentage': 0.3,
    'take_profit_percentage': 0.3,
}


def initialize(context):
    # Define lookback
    context.lookback = 100

    # Intialize exit flag
    context.exit_flag = False

    # Define the position
    context.position = 0

    # Define the number of lots to purchase
    context.quantity = 50

    # Set strike difference
    context.strike_difference = 50

    # Define the symbol
    context.symbol = 'NIFTY50'

    # Initialize no. of trades
    context.trade_num = 0

    # Expiry dates are in YYYYMMDD format
    context.expiry = "20220825"
    context.expiry_date_pytz = datetime.strptime(context.expiry, '%Y%m%d')

    context.date = datetime.today()

    # Future for the same underlying
    context.future_sym = superSymbol(
        secType='FUT',
        symbol=context.symbol,
        exchange='NSE',
        currency='INR',
        expiry=context.expiry,
        includeExpired=True)


def get_pop_empirical(futures_data, current_price, days_to_expiry, price_range):
    # Calculate empirical POP
    trading_days_to_expiry = round(days_to_expiry * (5 / 7))
    futures_data['percent_change_in_price'] = futures_data.futures_close.pct_change(trading_days_to_expiry)
    forecasted_prices = (1 + futures_data['percent_change_in_price']) * current_price
    histogram = np.histogram(forecasted_prices.dropna(), bins=30)
    hist_dist = rv_histogram(histogram)

    payoff = pd.DataFrame(index=price_range)
    payoff['probability_empirical'] = hist_dist.cdf(x=price_range)
    payoff['probability_empirical'] = payoff['probability_empirical'].diff()
    return payoff


# Long call payoff
def long_call_payoff(spot_price, strike_price, premium_spent):
    return np.where(spot_price < strike_price, 0, spot_price - strike_price) - premium_spent


# Long put payoff
def long_put_payoff(spot_price, strike_price, premium_spent):
    return np.where(spot_price < strike_price, strike_price - spot_price, 0) - premium_spent


# Short call payoff
def short_call_payoff(spot_price, strike_price, premium_collected):
    breakeven = strike_price + premium_collected
    return float(
        np.where(spot_price > breakeven, breakeven - spot_price, min(premium_collected, breakeven - spot_price)))


# Short put payoff
def short_put_payoff(spot_price, strike_price, premium_collected):
    breakeven = strike_price - premium_collected
    return float(
        np.where(spot_price > breakeven, min(premium_collected, spot_price - breakeven), spot_price - breakeven))


def get_payoff(spot_price_expiry, options_strategy):
    options_strategy['payoff'] = np.nan
    for i in options_strategy.index:
        if options_strategy.loc[i, 'Option Type'] == 'CE':
            if options_strategy.loc[i, 'position'] == 1:
                # long call payoff at expiry
                options_strategy.loc[i, 'payoff'] = long_call_payoff(spot_price_expiry,
                                                                     options_strategy.loc[i, 'Strike Price'],
                                                                     options_strategy.loc[i, 'premium'])

            elif options_strategy.loc[i, 'position'] == -1:
                # Short call payoff at expiry
                options_strategy.loc[i, 'payoff'] = short_call_payoff(spot_price_expiry,
                                                                      options_strategy.loc[i, 'Strike Price'],
                                                                      options_strategy.loc[i, 'premium'])

        elif options_strategy.loc[i, 'Option Type'] == 'PE':
            if options_strategy.loc[i, 'position'] == 1:
                # long put payoff at expiry
                options_strategy.loc[i, 'payoff'] = long_put_payoff(spot_price_expiry,
                                                                    options_strategy.loc[i, 'Strike Price'],
                                                                    options_strategy.loc[i, 'premium'])

            elif options_strategy.loc[i, 'position'] == -1:
                # Short put payoff at expiry
                options_strategy.loc[i, 'payoff'] = short_put_payoff(spot_price_expiry,
                                                                     options_strategy.loc[i, 'Strike Price'],
                                                                     options_strategy.loc[i, 'premium'])

    return options_strategy['payoff'].sum()


def get_expected_profit_empirical(futures_data, options_strategy, days_to_expiry, price_range):
    # Payoff
    payoff = pd.DataFrame()
    payoff['price_range'] = price_range
    payoff['pnl'] = payoff.apply(lambda r: get_payoff(r.price_range, options_strategy), axis=1)
    payoff.set_index('price_range', inplace=True)

    futures_price = futures_data.futures_close[-1]

    # POP Empirical
    payoff['probability_empirical'] = get_pop_empirical(futures_data, futures_price, days_to_expiry, payoff.index)

    # Expected Profit
    payoff['expected_pnl'] = payoff.probability_empirical * payoff.pnl
    exp_profit = payoff['expected_pnl'].sum()
    return exp_profit


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


# Get premium for strikes
def get_premium(context, data, options_strategy):
    for i in options_strategy.index:
        options_strategy.loc[i, 'premium'] = \
            data.history(options_strategy.loc[i, 'symbol'], ['close'], 100, '1m').close[-1]
    return options_strategy


# Setup butterfly
def setup_butterfly(ATM_strike_price, context, data):
    ATM_CE = get_contract(context, ATM_strike_price, 'C')
    ATM_PE = get_contract(context, ATM_strike_price, 'P')

    context.butterfly = pd.DataFrame(columns=['Option Type', 'Strike Price', 'position', 'premium', 'symbol'])

    context.butterfly.loc['0'] = ['CE', ATM_strike_price, 1, np.nan, ATM_CE]
    context.butterfly.loc['1'] = ['PE', ATM_strike_price, 1, np.nan, ATM_PE]

    context.butterfly = get_premium(context, data, context.butterfly)

    net_premium = context.butterfly.premium.sum()

    OTM_CE = get_contract(context, ATM_strike_price + round(net_premium / 50) * 50, 'C')
    OTM_PE = get_contract(context, ATM_strike_price - round(net_premium / 50) * 50, 'P')

    context.butterfly.loc['2'] = ['CE', ATM_strike_price + round(net_premium / 50) * 50, -1, np.nan, OTM_CE]
    context.butterfly.loc['3'] = ['PE', ATM_strike_price - round(net_premium / 50) * 50, -1, np.nan, OTM_PE]

    context.butterfly = get_premium(context, data, context.butterfly)

    return context.butterfly


def handle_data(context, data):
    future_data = data.history(context.future_sym,
                               ['high', 'low', 'close'], context.lookback, '1d')
    adx = ta.ADX(future_data.high, future_data.low, future_data.close, timeperiod=14)[-1]
    future_data.dropna(inplace=True)
    future_data = future_data.rename(columns={'close': 'futures_close'})

    days_to_expiry = (context.expiry_date_pytz - datetime.today()).days

    if (context.position == 0) & (adx <= 30) & (days_to_expiry > 0):

        # ATM Strike Price
        ATM_strike_price = \
            (round(future_data['futures_close'] / context.strike_difference) * context.strike_difference)[-1]

        # Setup butterfly
        context.butterfly = setup_butterfly(ATM_strike_price, context, data)
        print(f"We have setup the context.butterfly{context.butterfly}")

        # Range for payoff
        range = np.arange(ATM_strike_price - 2000, ATM_strike_price + 2000, 50)

        # Historical days
        historical_days = 30

        # Calculate expected profit
        exp_profit = get_expected_profit_empirical(future_data.iloc[-historical_days:],
                                                   context.butterfly.copy(), days_to_expiry, range)

        if exp_profit < 0:
            context.entry_premium = (context.butterfly.premium * context.butterfly.position).sum()

            # Compute SL and TP for the trade
            context.sl = context.entry_premium * (1 - config['stop_loss_percentage'] / 100)
            context.tp = context.entry_premium * (1 + config['take_profit_percentage'] / 100)

            # Update current position to 1
            context.position = 1
            place_order(context, context.butterfly, 1)

            # Increase number of trades by 1
            context.trade_num += 1
            print("-" * 30)

            # Print trade details
            print(
                f"Trade No: {context.trade_num} | Entry | Date: {datetime.today()} | Premium: {context.entry_premium}")

    elif context.position == 1:

        # Update net premium
        context.butterfly = get_premium(context, data, context.butterfly)
        net_premium = (context.butterfly.position * context.butterfly.premium).sum()

        # Exit the trade if any of the exit condition is met
        if days_to_expiry == 0:
            context.exit_flag = True

        elif net_premium < context.sl:
            context.exit_flag = True

        elif net_premium > context.tp:
            context.exit_flag = True

        if context.exit_flag:
            # Update current position to 0
            context.position = 0
            place_order(context, context.butterfly, 0)

            # Set exit flag to false
            context.exit_flag = False


# Place order
def place_order(context, options_strategy, action):
    for i in options_strategy.index:
        symbol = options_strategy.loc[i, 'symbol']
        position = options_strategy.loc[i, 'position']
        order_target(symbol, context.quantity * position * action)
