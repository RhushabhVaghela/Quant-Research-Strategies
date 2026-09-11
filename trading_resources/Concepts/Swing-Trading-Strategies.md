# Swing Trading Strategies — Concept Inventory
## COURSE: Swing Trading Strategies
A () course on building and backtesting swing trading strategies in Python. Covers Python fundamentals, financial data handling, MACD and Williams Fractal indicators, stock screening, trade-book construction, and performance analysis.
---
## MODULE: Introduction to Python
### LESSON: My First Jupyter Notebook
- **Programming** — telling a machine what to do by writing code. prereqs: none.
- **Jupyter notebook** — an interactive document of code cells and markdown cells run with Shift+Enter. prereqs: none.
- **Code comments** — non-executable notes using `#` (single line) or triple quotes `"""..."""` (multi-line). prereqs: none.
- **Print statement** — `print("...")` outputs text/values to the console. prereqs: none.
- **Variables** — named storage for values, assigned with `=` (read as "is set to"). prereqs: none.
- **Integer** — a whole number data type (positive or negative). prereqs: variables.
- **Float** — a real/decimal number data type, e.g. `5.0` or `float(5)`. prereqs: variables.
- **String** — text data enclosed in single or double quotes. prereqs: variables.
- **Case sensitivity** — Python treats `gold_price` and `Gold_Price` as different variables. prereqs: variables.
- **Indentation** — Python requires consistent leading spaces within a code block; wrong indentation raises an error. prereqs: variables.
- **Simple returns** — percentage change in price: `(Final/Initial - 1) * 100`. prereqs: variables, arithmetic.
- **Log returns** — natural log of the price ratio: `math.log(price_2 / price_1)`. prereqs: simple returns, math module.
- **`type()` function** — returns the data type of a variable. prereqs: variables.
- **`math` module** — Python standard library for math functions; imported with `import math`. prereqs: none.
### LESSON: Operations and Functions in Python
- **Exponentiation operator** — `**` raises a number to a power, e.g. `3**2`. prereqs: arithmetic.
- **Modulo operator** — `%` returns the remainder of a division, e.g. `15 % 4`. prereqs: arithmetic.
- **Built-in math functions** — `abs()`, `round()`, `max()`, `min()`, `sum()`. prereqs: none.
- **`import` keyword** — loads a library so its functions become available. prereqs: none.
- **Comparison operators** — `==`, `!=`, `<`, `>`, `<=`, `>=`; return booleans. prereqs: none.
- **Boolean values** — `True` / `False` results of logical operations. prereqs: comparison operators.
- **Logical operators** — `not`, `or`, `and` combine boolean statements per a truth table. prereqs: booleans.
- **Functions** — reusable blocks of code defined with `def name(params):`. prereqs: none.
- **Function parameters** — inputs passed into a function, separated by commas. prereqs: functions.
- **Variable scope** — a variable defined inside a function is not accessible outside it. prereqs: functions.
- **`return` statement** — sends a value out of a function so it can be stored/used outside. prereqs: functions, scope.
### LESSON: DataFrame and Basic Functionality
- **DataFrame** — pandas' tabular data structure of rows and columns (spreadsheet-like). prereqs: none.
- **`pd.DataFrame()` constructor** — creates a dataframe from a dict of lists. prereqs: pandas import.
- **Index** — the row labels of a dataframe; can be set with `set_index()`. prereqs: DataFrame.
- **`set_index()`** — sets a column as the row index. prereqs: DataFrame.
- **`pd.read_csv()`** — reads a CSV file into a dataframe; `index_col` sets the index column. prereqs: pandas.
- **`head()` / `tail()`** — display the first/last n rows (default 5). prereqs: DataFrame.
- **`loc`** — label-based row/column access; end index is inclusive. prereqs: DataFrame.
- **`iloc`** — position-based row/column access; end index is exclusive. prereqs: DataFrame.
- **Boolean indexing** — filtering rows with a boolean condition, e.g. `df[df.col > 5000]`. prereqs: DataFrame, booleans.
- **Accessing columns** — select a column by name with `df[["col"]]`. prereqs: DataFrame.
- **`drop()`** — removes rows or columns; `axis=1` drops columns. prereqs: DataFrame.
- **Adding columns** — assign a new column, e.g. `df['SMA'] = df['Close'].rolling(10).mean()`. prereqs: DataFrame.
- **`rolling().mean()`** — computes a rolling (moving) average over a window. prereqs: DataFrame.
---
## MODULE: Financial Market Data and Visualisation
### LESSON: Importing Time Series Data
- **Time series data** — data indexed by time (e.g. daily OHLCV prices). prereqs: none.
- **`yfinance` package** — downloads financial data from Yahoo Finance; installed via `!pip install yfinance`. prereqs: none.
- **`yf.download()`** — fetches OHLCV data for a ticker between start/end dates. prereqs: yfinance.
- **Adjusted price** — price adjusted for corporate actions; `auto_adjust=True` in `yf.download`. prereqs: yfinance.
- **CSV file** — comma-separated values plain-text tabular file. prereqs: none.
- **`pd.to_datetime()`** — converts an index/column to datetime format for time-series operations. prereqs: pandas.
### LESSON: Data Visualisation
- **Data visualisation** — graphical representation of data to draw insights. prereqs: none.
- **`matplotlib` library** — Python plotting library; `import matplotlib.pyplot as plt`. prereqs: none.
- **`%matplotlib inline`** — magic command to render plots inside the notebook. prereqs: matplotlib.
- **`plt.style.use()`** — sets the plot style; `plt.style.available` lists options. prereqs: matplotlib.
- **Line graph** — `df['col'].plot()` plots a column over its index. prereqs: matplotlib, DataFrame.
- **`plt.title()` / `plt.xlabel()` / `plt.ylabel()`** — set plot title and axis labels. prereqs: matplotlib.
- **Scatter plot** — `plt.scatter(col1, col2)` shows the relationship between two variables. prereqs: matplotlib.
- **Histogram** — `df['col'].plot(kind='hist')` shows the frequency distribution of a column. prereqs: matplotlib.
- **`plt.show()`** — displays the current figure. prereqs: matplotlib.
---
## MODULE: MACD
### LESSON: MACD Entry Rules
- **MACD (Moving Average Convergence Divergence)** — momentum indicator from the difference of two EMAs. prereqs: EMA.
- **MACD line** — fast-period EMA minus slow-period EMA (default 12 and 26). prereqs: EMA.
- **Signal line** — EMA of the MACD line (default 9-period). prereqs: MACD line.
- **MACD histogram** — MACD line minus signal line. prereqs: MACD line, signal line.
- **TA-Lib (`talib`)** — technical analysis library; `ta.MACD(close)` returns line, signal, histogram. prereqs: none.
- **`pd.read_pickle()`** — reads a compressed pickle file (`.bz2`) into a dataframe. prereqs: pandas.
- **`dropna()`** — removes rows with missing (NaN) values. prereqs: DataFrame.
- **`np.where(condition, if_true, if_false)`** — vectorized conditional to build a signal column. prereqs: numpy.
- **Long entry signal** — buy when MACD line crosses above the signal line (`MACD line > Signal line`). prereqs: MACD components.
### LESSON: Minute Price Data Resampling Techniques
- **Minute data** — intraday data at 1-minute frequency. prereqs: none.
- **`yf.download(period=, interval=)`** — downloads data at a chosen frequency (e.g. `1m`). prereqs: yfinance.
- **Resampling** — converting high-frequency data to a lower frequency (not the reverse). prereqs: time series.
- **`DataFrame.resample(interval).agg(dict)`** — aggregates data to a new frequency. prereqs: pandas.
- **OHLCV aggregation dict** — maps Open→first, High→max, Low→min, Close→last, Volume→sum. prereqs: resampling.
- **Resample intervals** — `15T` (15 min), `1H` (1 hour), `4H` (4 hours). prereqs: resampling.
### LESSON: Working With Pickle File
- **Pickle file** — Python serialization format that retains column/index data types. prereqs: none.
- **`bz2` compression** — compressed pickle format for smaller file size. prereqs: pickle.
- **`to_pickle()`** — saves a dataframe to a pickle file. prereqs: pandas.
- **`read_pickle()`** — reads a pickle file back into a dataframe. prereqs: pandas.
- **DatetimeIndex** — index of datetime objects, preserved through pickle. prereqs: pickle, datetime.
- **Pickle version compatibility** — pickle files are Python-version-specific and backward compatible. prereqs: pickle.
- **Common pickle errors** — `AttributeError` (pandas version mismatch) and `ValueError: unsupported pickle protocol`. prereqs: pickle.
---
## MODULE: Stock Screener
### LESSON: Fetch Data for Multiple Stocks
- **Data vendor** — a service (e.g. Yahoo Finance) providing OHLCV data. prereqs: none.
- **Ticker** — the symbol identifying a stock. prereqs: none.
- **Loop over tickers** — `for t in tickers: stock_data[t] = yf.download(t, ...)` fetches data for many stocks. prereqs: yfinance, loops.
- **Dictionary of dataframes** — storing each stock's dataframe keyed by ticker. prereqs: dict, DataFrame.
- **`pickle.dump()` / `pickle.load()`** — write/read a Python object to/from a pickle file. prereqs: pickle.
- **Adjusted prices** — prices adjusted for stock splits, dividends, and rights offerings. prereqs: none.
### LESSON: Stock Screener
- **Stock screener** — filters a stock universe by criteria to find tradable assets. prereqs: none.
- **Penny stock filter** — exclude stocks with average price below a threshold (e.g. $5). prereqs: screener.
- **Liquidity filter** — require average dollar-volume above a threshold (e.g. $100M). prereqs: screener.
- **Dollar-volume** — price × volume, a liquidity measure. prereqs: liquidity.
- **Market capitalisation filter** — require market cap above a threshold (e.g. $200B). prereqs: screener.
- **Market capitalisation** — outstanding shares × average price. prereqs: none.
- **ADX filter** — require ADX > 25 to confirm a strong trend. prereqs: ADX indicator.
- **Hurst exponent** — measures trend persistence; `compute_Hc()` from the `hurst` package. prereqs: none.
- **Hurst filter** — require Hurst exponent > 0.5 to validate the trend. prereqs: Hurst exponent.
- **Distance from 52-week high** — `(52-week high - Close) / 52-week high`; small distance indicates an uptrend. prereqs: screener.
- **Uptrend filter** — select stocks within 10% of their 52-week high. prereqs: distance from high.
- **Forward bias avoidance** — in backtesting, split data so filters use past data only. prereqs: backtesting.
---
## MODULE: Williams Fractals
### LESSON: Williams Fractal
- **Williams Fractal** — a 5-candle reversal pattern indicator. prereqs: candlesticks.
- **Bullish fractal** — the middle of the latest 5 candles has the lowest low. prereqs: Williams Fractal.
- **Bearish fractal** — the middle of the latest 5 candles has the highest high. prereqs: Williams Fractal.
- **`rolling(5).apply(func)`** — applies a function over a rolling 5-bar window. prereqs: pandas.
- **`shift(1)`** — lags a signal by one bar to avoid forward bias (fractal confirmed only after candles form). prereqs: pandas.
- **Fractal signal** — combined bullish (+1) and bearish (−1) fractal signals, shifted. prereqs: bullish/bearish fractal.
- **Trade book** — a table of entry/exit times and prices from a strategy. prereqs: none.
- **`get_trade_book()`** — helper that builds a trade book from a signal column, take-profit, and stop-loss. prereqs: trade book.
- **Take-profit / stop-loss** — exit levels set as percentages of entry price (e.g. 4% / 2%). prereqs: trade book.
- **`analyse_performance()`** — helper that computes strategy performance metrics. prereqs: performance measures.
---
## MODULE: Swing Strategy Backtesting
### LESSON: MACD Swing Strategy
- **Entry signal** — buy when MACD line > signal line. prereqs: MACD.
- **Exit via technical indicator** — close a long when the MACD line crosses below the signal line. prereqs: MACD.
- **Stop-loss / profit-target exit** — close when stop-loss or profit target is hit. prereqs: risk management.
- **Risk-reward ratio** — e.g. 1:2 means 2% stop-loss and 4% profit target. prereqs: none.
- **Time exit** — close a position automatically after a holding period (e.g. one month). prereqs: none.
- **PnL calculation** — exit price minus entry price, minus trading costs. prereqs: none.
- **Transaction cost** — broker fee per trade (e.g. 0.0002). prereqs: PnL.
- **Slippage** — difference between expected and actual fill price (e.g. 0.0005). prereqs: PnL.
- **`timedelta`** — `datetime` object for date/time arithmetic (e.g. holding-period checks). prereqs: datetime.
---
## MODULE: Different Performance Measures
### LESSON: Performance Measures
- **Backtesting details** — number of trades, start/end dates, duration, holding time. prereqs: trade book.
- **Holding time** — duration of a trade (exit time − entry time); average/median/min/max. prereqs: trade book.
- **Annualised returns** — average annual return of a strategy, annualised from cumulative returns. prereqs: returns.
- **Profit factor** — sum of profits divided by sum of losses. prereqs: returns.
- **Win rate** — proportion of winning trades. prereqs: returns.
- **Heatmap of month vs year returns** — visualises returns by month and year. prereqs: returns.
- **Equity curve** — cumulative strategy returns over time. prereqs: returns.
- **Annualised volatility** — `sqrt(Var(returns)) * sqrt(252*6.5)` for hourly data. prereqs: returns.
- **Maximum drawdown** — `(Trough - Peak) / Peak`; the largest peak-to-trough loss. prereqs: equity curve.
- **Rolling volatility** — volatility over a rolling window (e.g. 60 days). prereqs: volatility.
- **Sharpe ratio** — `(R_p - R_f) / sigma_p`; excess return per unit of risk. prereqs: returns, volatility.
- **Sortino ratio** — risk-adjusted return using only downside volatility. prereqs: Sharpe ratio.
- **Calmar ratio** — annualised return divided by maximum drawdown. prereqs: returns, max drawdown.
- **Risk-adjusted return metrics** — returns adjusted for the risk taken, for comparing portfolios. prereqs: returns, risk metrics.
- **`analyse_performance()`** — combines backtesting details, return, risk, and risk-adjusted metrics. prereqs: all metrics.
---
## MODULE: Composite Swing Trading Strategy
### LESSON: Composite Swing Trading Strategy
- **Composite strategy** — combining two indicators (MACD + Williams Fractal) for entry signals. prereqs: MACD, Williams Fractal.
- **Composite entry signal** — buy when both MACD and Williams Fractal signal an entry. prereqs: MACD, fractal.
- **Signal quality** — combining indicators can improve signal quality and performance. prereqs: composite strategy.
- **Performance comparison** — composite strategy vs individual strategies (Sharpe, volatility). prereqs: performance measures.
---
## MODULE: Capstone Project
### LESSON: Capstone Project Model Solution
- **Capstone project** — build a swing trading strategy with a stock screener on multiple assets. prereqs: all modules.
- **Read price data** — load a pickle dict of minute data for multiple tickers. prereqs: pickle, dict.
- **Resample to hourly** — convert minute data to hourly candles with an OHLCV aggregation dict. prereqs: resampling.
- **Data sanity check** — check for missing data/outliers (e.g. 7 hourly points per day). prereqs: resampling.
- **Data split for backtesting** — use the first part for screening filters, the second for trading (avoid forward bias). prereqs: screener.
- **Williams Alligator** — 3 EMA lines (Jaw 13-shift8, Teeth 8-shift5, Lips 5-shift3) for momentum swings. prereqs: EMA.
- **Alligator bullish signal** — Lips above Teeth above Jaw. prereqs: Williams Alligator.
- **Combined buy signal** — buy when Williams Fractal is bullish AND Williams Alligator is bullish. prereqs: fractal, alligator.
- **Trade book per asset** — build a trade book for each filtered asset with take-profit/stop-loss. prereqs: trade book.
- **Portfolio returns** — combine per-asset strategy returns with equal weights. prereqs: returns.
- **`pyfolio` package** — generates performance tear sheets for a portfolio. prereqs: performance measures.
- **`create_simple_tear_sheet()`** — pyfolio function producing a full performance report. prereqs: pyfolio.
### LESSON: Capstone Project Solution Template
- **Solution template** — a scaffold notebook with placeholders to build the capstone solution. prereqs: capstone.
- **`sys.path.append()`** — adds a directory to the Python import path for custom modules. prereqs: python.
- **`compute_Hc()`** — computes the Hurst exponent for trend validation. prereqs: hurst package.
---
## Swing-Trading-Strategies — Section-based course structure
# Concept Inventory — Swing Trading Strategies
## COURSE: Swing Trading Strategies
### Section: Section 1 - Introduction
- **Course introduction & structure:** scope — Python/data, technical analysis, MACD strategy, backtesting, capstone. prereqs: none.
- **Course structure flow diagram (PNG):** overview of the learning path. prereqs: none.
### Section: Section 2 - Swing Trading Overview
- **What is swing trading:** holding positions for days-to-weeks to capture medium-term price swings. prereqs: trading basics.
- **Properties of swing trading:** timeframe, frequency, goals, distinctions from day trading / investing. prereqs: swing trading.
### Section: Section 3 - Swing Trading Style
- **Swing trading style:** risk/reward profile and the technical approach used throughout. prereqs: swing trading.
### Section: Section 5 - Financial Market Data and Visualisation
- **Importing data:** loading price data via yfinance/CSV (DataFrame). prereqs: pandas, finance.
- **Additional reading for financial market data:** data sources, data quality and cleaning. prereqs: data import.
- **FAQs on data:** common questions on OHLCV and frequency. prereqs: price data.
### Section: Section 6 - Strategic Plan
- **Strategic plan:** the step-by-step method for building and validating a swing strategy. prereqs: swing trading.
### Section: Section 7 - Technical Analysis in Trading
- **Technical analysis in trading:** using historical price/volume patterns for decisions. prereqs: none.
- **Types of technical indicators:** trend, momentum, volatility, volume indicator categories. prereqs: technical analysis.
### Section: Section 8 - Moving Average Primer
- **Moving average & EMA (PDF):** SMA vs EMA definitions and weighting. prereqs: price series.
- **Moving average crossovers:** golden/death cross signals and their interpretation. prereqs: moving averages.
### Section: Section 9 - MACD
- **MACD entry points:** using MACD for long/short entries. prereqs: MACD indicator.
- **MACD line & signal line:** MACD line (12-26 EMA diff) vs signal line (9 EMA), crossovers. prereqs: EMA.
- **MACD histogram:** difference between MACD and signal line, momentum representation. prereqs: MACD.
### Section: Section 10 - Exit Strategy
- **Need of exit rules:** why exits matter for locking profit and cutting losses. prereqs: risk management.
- **Exit rules:** predefined rules for closing positions (targets, stops, signal reversal). prereqs: entry signals.
- **Additional reading for exit rules:** exit strategy research. prereqs: exit rules.
### Section: Section 11 - Introduction to Backtesting
- **What is backtesting:** simulating strategy on historical data. prereqs: none.
- **How to do backtesting:** signal generation, position sizing, equity curve. prereqs: backtesting.
- **Additional reading for backtesting:** backtest methodology and pitfalls. prereqs: backtesting.
### Section: Section 13 - Different Performance Measures
- **Different performance measures:** CAGR, Sharpe, Sortino, Calmar, max drawdown, win rate. prereqs: returns.
- **Measuring risk:** drawdown, volatility as risk measures. prereqs: performance measures.
- **Additional reading for performance measures:** metric definitions and interpretation. prereqs: performance measures.
### Section: Section 16 - Optimum Number of Indicators
- **Optimum number of indicators:** how many indicators to combine for robust signals vs overfitting. prereqs: technical indicators.
### Section: Section 17 - Williams Fractals
- **Williams fractals:** Bill Williams' 5-bar fractal pattern marking swing highs/lows. prereqs: price action.
### Section: Section 19 - Stock Screener
- **Stock screener:** filtering stocks by criteria (liquidity, volatility, trend). prereqs: technical analysis.
- **Identify trending stocks:** ranking stocks by trend strength. prereqs: screener, trend.
- **Identifying direction of trend:** technical trend direction confirmation. prereqs: trend.
### Section: Section 20 - Risk Management
- **Risk management:** risk-reward, stop-loss, position risk. prereqs: none.
- **Position sizing:** fraction-of-capital sized by risk and stop distance. prereqs: risk management.
- **Additional reading for risk management:** risk control strategies. prereqs: risk management.
### Section: Section 21 - Automate Trading Strategy Using IBridgePy
- **IBridgePy automation (zip MACDSwingStrategy):** automating strategy execution via Interactive Brokers bridge. prereqs: IB API, strategy.
### Section: Section 23 - Capstone Project
- **Problem statement (PDF):** build a full swing-trading strategy. prereqs: all previous.
- **Solution template & model solution (zips):** provided code and data for capstone evaluation. prereqs: capstone.
### Section: Section 24 - Course Summary
- **Ten simple rules for swing trading (PDF):** good-practice checklist. prereqs: swing trading.
- **Ten deadly sins of swing trading (PDF):** common mistakes to avoid. prereqs: swing trading.
- **Course summary:** recap and downloadable ZIP. prereqs: all.
## Course Prerequisite Map
Before this course a learner needed: Python + pandas for data import/manipulation; financial data (OHLCV) and plotting with matplotlib; basic technical analysis (moving averages, trend); understanding of returns and compounding; and foundational backtesting + performance-metric concepts (Sharpe, Sortino, drawdown).