## COURSE: Backtesting Trading Strategies
### MODULE: Financial Data
#### NOTEBOOK: Daily Stock Price Data
- **Backtesting** — Simulating a trading strategy on historical data to evaluate its viability before going live. prereqs: none
- **yfinance** — Python package to download historical financial data from Yahoo Finance. prereqs: Python, pip
- **yf.download(ticker, start, end)** — Downloads OHLCV data for an asset across a date range into a DataFrame. prereqs: yfinance
- **OHLCV columns** — The open, high, low, close, adjusted close, and volume columns common to price data. prereqs: yfinance
- **Tickers for different geographies** — Suffixes denote exchange, e.g. HSBA.L (London), RELIANCE.NS (NSE India). prereqs: tickers
- **Plotting close price** — Using matplotlib `.plot()` to visualise a full year of price movement. prereqs: matplotlib
- **Adjusted vs unadjusted prices** — Raw closing prices vs prices adjusted for corporate actions. prereqs: price data
- **Corporate actions** — Stock splits, dividends, and rights offerings that alter historical prices. prereqs: adjusted prices
- **auto_adjust=True** — yfinance option returning all OHLCV columns already split/dividend-adjusted. prereqs: yf.download
- **warnings.filterwarnings('ignore')** — Suppresses warnings for a cleaner notebook. prereqs: Python
### MODULE: Data Pre-Processing
#### NOTEBOOK: Data Quality Checks and Data Cleaning
- **Data quality** — Ensuring input data is clean and reliable before analysis for trustworthy results. prereqs: none
- **pd.read_csv(parse_dates, index_col)** — Loading a CSV while parsing a date column and setting an index column. prereqs: pandas
- **parse_dates** — read_csv argument converting a named column to datetime (date columns default to strings). prereqs: read_csv
- **head() / tail()** — Previewing the first/last five rows of a DataFrame. prereqs: pandas
- **dataframe.info()** — Concise summary of columns, non-null counts, and dtypes. prereqs: pandas
- **isna()** — Returns a boolean Series marking missing (NA) values per element. prereqs: pandas
- **isna().sum()** — Counts missing values in each column. prereqs: isna
- **Missing / null values** — Gaps in the dataset that may skew analysis if not handled. prereqs: isna
- **dropna()** — Removes rows (axis=0/'index') or columns (axis=1/'columns') containing nulls. prereqs: pandas
- **dropna parameters (axis, how, inplace)** — `how='any'/'all'` choose when to drop; `inplace=True` mutates the DataFrame. prereqs: dropna
- **DataFrame.shape** — Tuple of (rows, columns); `shape[0]` gives the row count. prereqs: pandas
- **Duplicate values** — Repeated rows arising from human error or merging multiple sources. prereqs: data cleaning
- **duplicated().value_counts()** — Counts duplicated (True) vs unique (False) observations. prereqs: pandas
- **Proportion of duplicates** — Ratio of duplicate rows to total; small fractions may be ignored. prereqs: duplicated
- **Consecutive duplicate removal** — Using `.diff() != 0` across columns to drop only immediately repeated rows. prereqs: pandas diff
- **Outliers** — Values unusually large/small vs the rest of the data, detectable via large percentage changes. prereqs: data cleaning
- **pct_change() for outlier detection** — Plotting daily percentage change to spot extreme (anomalous) moves. prereqs: pct_change
### MODULE: Trading Rules
#### NOTEBOOK: Generate Entry and Exit Signals
- **Trading hypothesis** — The stated rule/sentiment basis driving when to enter and exit positions. prereqs: backtest concepts
- **Backtest flowchart** — A diagram of the full backtesting pipeline (import → signals → trade sheet → analytics). prereqs: none
- **Short-term & long-term lookback** — Window periods (9-day, 21-day) for the two moving averages. prereqs: moving averages
- **Short/long moving averages** — Simple moving averages of Close via `.rolling().mean()` stored as `ma_short`, `ma_long`. prereqs: pandas rolling
- **Signal definition** — `np.where(ma_short > ma_long, 1, 0)`: 1 when short MA is above long MA, else 0. prereqs: numpy
- **Entry condition** — Open a long position when the short-term MA crosses above the long-term MA from below. prereqs: signal
- **Exit condition** — Close the long position when the short-term MA crosses below the long-term MA from above. prereqs: signal
- **Holding period** — The date range during which a long position is active. prereqs: signal
- **Visualising holding periods** — Plotting price with `secondary_y` and `plt.fill_between(where=signal>0)` to shade in-position periods. prereqs: matplotlib
- **Strategy returns** — `signal.shift(1) * Close.pct_change()`; multiply prior-day signal by daily price change. prereqs: pct_change, shift
- **Lookahead avoidance (shift)** — Applying the signal a day later to prevent using same-day data for trades. prereqs: shift
- **Total cumulative strategy return** — `(strategy_returns+1).prod()-1` gives compounded return over the period. prereqs: prod, strategy returns
#### NOTEBOOK: Backtest and Generate Trade Sheet
- **Trade sheet** — A table of all backtested trades with positions, entry/exit dates, and entry/exit prices. prereqs: trading signals
- **Long crossover column** — Boolean marking entry days: previous day short<long and today short≥long. prereqs: moving averages
- **Exit/squared crossover column** — Boolean marking exit days: previous day short>long and today short≤long. prereqs: moving averages
- **np.where with shifted conditions** — Change-of-state detection using `.shift(1)` on the moving averages. prereqs: np.where
- **Trade record fields** — Position, Entry Date, Entry Price, Exit Date, Exit Price per completed trade. prereqs: trade sheet
- **current_position state variable** — Tracks '1' (holding long) or '0' (flat) during the backtest loop. prereqs: backtesting
- **Iterating over dates** — Looping `for current_date in data.index` to process each day's entry/exit logic. prereqs: pandas
- **pd.concat() to append trades** — Accumulating completed trades into a growing trade_sheet DataFrame. prereqs: pandas
- **backtest_trade_sheet() function** — A reusable wrapper producing the trade sheet from data and crossover columns. prereqs: trading rules
- **Trade PnL** — `(Exit Price - Entry Price) * Position` computes profit/loss per trade. prereqs: trade sheet
- **Total PnL** — Sum of all per-trade PnL, indicating overall strategy profit/loss. prereqs: trade PnL
### MODULE: Trade Level Analytics
#### NOTEBOOK: Trade Level Analytics
- **Trade level analytics** — Metrics describing performance across completed trades (not within them). prereqs: backtesting outputs
- **Total PnL** — `trades.PnL.sum()` gives the sum of all gains and losses across trades. prereqs: trade analytics
- **Number of trades** — Counting trades via indexing a Position/PnL subset (long trades only). prereqs: pandas filtering
- **Win rate (Win %)** — % of profitable trades: `(winners / total) * 100`; above 50% is favourable. prereqs: trade PnL
- **Loss rate** — % of losing trades: `(losers / total) * 100`. prereqs: total trades
- **Average profit per winning trade** — Sum of winner PnL divided by winner count. prereqs: win rate
- **Average loss per losing trade** — Mean absolute value of losing trades' PnL. prereqs: loss rate
- **Average trade duration (holding period)** — Mean of `(Exit Date - Entry Date)`; capital is locked during a trade. prereqs: trade sheet
- **pd.to_datetime() on entry/exit dates** — Casting to datetime so holding periods can be subtracted. prereqs: pandas
- **Profit Factor** — Ratio of (Win% × avg win PnL) to (Loss% × avg loss PnL); a graded strategy-quality metric. prereqs: win/loss rate, averages
- **Profit-factor interpretation** — Grades: <1 unprofitable, 1 breakeven, 1.1–1.4 average, 1.4–2.0 decent, ≥2 excellent. prereqs: profit factor
### MODULE: Performance Metrics
#### NOTEBOOK: Performance Metrics
- **Performance metrics** — Measures evaluating a strategy's behaviour between trade entry and exit. prereqs: trade analytics
- **Strategy returns** — `signal.shift(1) * Close.pct_change()` gives per-day strategy return. prereqs: pct_change
- **Equity curve** — Plot of cumulative strategy returns over time; positive slope indicates profitability. prereqs: returns
- **Cumulative returns** — `(returns+1).cumprod()` running product compounding daily returns. prereqs: strategy returns
- **CAGR** — Compound Annual Growth Rate: `((EV/BV)^(1/n)-1)*100` annualising growth with compounding. prereqs: equity curve, returns
- **Histogram of returns** — `Strategy_Returns.hist(bins=50)` shows the distribution of daily returns. prereqs: matplotlib
- **Annualised volatility** — `std() * sqrt(252)` converts daily volatility to a yearly figure. prereqs: std, annualisation
- **Standard deviation (volatility)** — Average dispersion/fluctuation of the strategy returns. prereqs: statistics
- **Sharpe ratio (with risk-free)** — `(mean_return - daily_risk_free)/std * sqrt(252)`; ratio of excess return to volatility. prereqs: mean, std, risk-free
- **Risk-free rate** — A baseline (e.g. 2%/year) subtracted from returns before Sharpe; converted to daily. prereqs: Sharpe ratio
- **Maximum drawdown** — Max loss from a running peak to a trough of the equity curve: `(Cum-Ret - Peak)/Peak`. prereqs: equity curve
- **Cumulative maximum (Peak)** — `Cumulative_Returns.cummax()` tracks the running peak of the curve. prereqs: pandas
- **Drawdown series** — Per-day percentage decline of returns from the running peak. prereqs: cumulative max
- **Plotting drawdowns** — `plt.plot` + `plt.fill_between(where=drawdown)` to show frequency/severity of losses. prereqs: matplotlib
### MODULE: Risk Management
#### NOTEBOOK: Backtesting With Stop-Loss and Take-Profit
- **Stop-loss** — A predefined price level that caps a trade's loss; exiting when price falls to it. prereqs: risk management
- **Take-profit** — A predefined price level that locks in profit; exiting when price rises to it. prereqs: risk management
- **Exit conditions (with stop-loss/take-profit)** — Exit on low≤stop-loss, high≥take-profit, or a crossover exit. prereqs: risk rules
- **Stop-loss / take-profit price** — `entry_price * (1 ± percentage)` for SL and TP levels at entry. prereqs: position sizing
- **Stop-loss & take-profit percentages** — Levels set as a fraction of the long entry price (e.g. 3% SL, 15% TP). prereqs: risk parameters
- **Exit Type column** — Labels each closed trade as 'Stop-Loss', 'Take-Profit', or 'Exit_crossover/Squareoff'. prereqs: trade sheet
- **backtest_trade_sheet_sl_tp()** — Function to generate trades adding SL/TP breach checks to the backtest loop. prereqs: backtest function
- **PnL with stop-loss/take-profit** — Same `(Exit - Entry)*Position` PnL; adding SL/TP can raise total PnL (e.g. +19%). prereqs: trade PnL
- **close-column breach testing** — Using the day's close/price value to decide if a stop-loss/take-profit was hit. prereqs: stop-loss
### MODULE: Transaction Costs and Slippage
#### Notebook: Implementation of Transaction Cost and Slippage
- **Transaction costs** — Commissions/fees, slippage, and taxes paid to execute trades; must be modelled pre-live. prereqs: backtesting
- **Brokerage fee** — The commission a broker charges to execute a transaction (e.g. 0.03% of traded value). prereqs: trading costs
- **Tax on trades** — Government tax imposed on financial transactions (e.g. 0.02%). prereqs: trading costs
- **Total brokerage cost** — Sum of brokerage + tax percentages (e.g. 0.05% combined). prereqs: brokerage, tax
- **Slippage** — Difference between expected trade price and actual execution price; estimated from market data. prereqs: transaction costs
- **Last 5-minute candles** — Using the final five one-minute price candles of each day to estimate end-of-day slippage. prereqs: slippage modelling
- **groupby(date).tail(5)** — Keeping the last N rows per day to isolate closing-minute bars. prereqs: groupby
- **Slippage for buy orders** — `(High - Close)/Close`: worst buy execution is at the bar high. prereqs: slippage modelling
- **Slippage for sell orders** — `(Close - Low)/Close`: worst sell execution at the bar low. prereqs: slippage modelling
- **Mean & maximum slippage** — Averaging daily slippage then taking the maximum buy/sell cost as the estimate (e.g. 0.09%). prereqs: slippage modelling
- **Transaction cost** — A fixed per-dollar cost on shares purchased/sold (e.g. 0.001). prereqs: costs
- **Total charges** — Sum of transaction cost + slippage cost + brokerage cost. prereqs: costs & slippage
- **Trading cost on position change** — `total_charges * |signal - signal.shift(1)|` applies cost only when position changes. prereqs: signal, shift
- **Net strategy returns** — Subtract the trading cost from raw strategy returns to get realistic returns. prereqs: strategy returns
- **Cumulative returns after costs** — `(net_returns+1).cumprod()` plots growth after all charges. prereqs: cumprod
- **Comparing costed vs uncosted results** — Showing how costs degrade headline strategy performance before going live. prereqs: cumulative returns
### MODULE: Capstone Project
#### NOTEBOOK: Capstone Project Solution Template
- **Multi-stock backtest** — Backtesting the moving-average crossover strategy on Apple, Facebook, Microsoft, and Tesla. prereqs: backtesting
- **Capital-reading multiple prices** — Reading a CSV with four price series and parsing the date index to datetime. prereqs: read_csv
- **Computing moving averages for many stocks** — `.rolling(window).mean()` applied across an entire multi-column DataFrame. prereqs: rolling
- **Signals for the portfolio** — Comparing short/long moving averages across all stocks at once. prereqs: moving averages
- **Equal-weighted portfolio** — Averaging strategy returns across stocks (`.mean(axis=1)`) as a simple portfolio. prereqs: equity curves
- **Equity curves per stock & portfolio** — Plotting `(returns+1).cumprod()` for each stock and the equal-weighted average. prereqs: cumulative returns
- **CAGR for a portfolio** — Annualising portfolio compounded returns via `((cumprod.iloc[-1] ** (252/days)) - 1) * 100`. prereqs: CAGR
- **Portfolio Sharpe ratio** — Applying the annualised Sharpe formula to mean portfolio returns vs a 2% risk-free rate. prereqs: Sharpe ratio
#### NOTEBOOK: Capstone Project Model Solution
- **Data ingestion & datetime index** — `pd.read_csv` + `data.index = pd.to_datetime(...)` normalises index across assets. prereqs: pandas
- **Multiple rolling means** — `data.rolling(9).mean()` / `data.rolling(21).mean()` over all stock columns. prereqs: rolling
- **Signal with boolean→int** — `ma_short > ma_long` yields a boolean DataFrame; `.astype(int)` converts to 1/0. prereqs: signals
- **Strategy returns (element-wise)** — `signal.shift(1) * data.pct_change()` lets pandas broadcast across all assets. prereqs: pct_change, shift
- **Equity curve plotting** — `plt.plot((strategy_returns+1).cumprod())` draws cumulative returns per stock. prereqs: matplotlib, cumprod
- **Plot legend & tick_params** — `plt.legend(...)` and `plt.tick_params(labelsize=15)` polish the equity plot. prereqs: matplotlib
- **Equal-weighted portfolio curve** — `(strategy_returns.mean(axis=1)+1).cumprod()` averages across the four stocks. prereqs: equity curves
- **Portfolio CAGR** — Compounding portfolio returns then annualising with the 252-day exponent. prereqs: CAGR
- **Daily risk-free rate for Sharpe** — Setting `risk_free_rate = 0.02/252` before computing the pool Sharpe. prereqs: Sharpe ratio
- **drawdown_cal() function** — A custom function returning (max drawdown, drawdown series) from a cumulative-returns series. prereqs: drawdown
- **running_max via np.maximum.accumulate()** — Cumulative running peak of the pooled portfolio returns, floored at 1. prereqs: numpy
- **Maximum drawdown of portfolio** — Deepest % peak-to-trough loss (e.g. −22.04%) via the min drawdown. prereqs: drawdown_cal
- **Plotting portfolio drawdown** — `plt.plot(drawdown)` plus `plt.fill_between(..., red)` to visualise loss periods. prereqs: matplotlib
---
## Backtesting-Trading-Strategies — Section-based course structure
# Concept Inventory — Backtesting Trading Strategies
## COURSE: Backtesting Trading Strategies
### Section: Section 1 - Introduction
- **Course structure & roadmap:** how the course is organized into backtesting steps (data → rules → analytics → metrics → risk). prereqs: none.
- **What you will learn in the course:** the end-to-end backtesting workflow. prereqs: none.
### Section: Section 2 - Backtesting
- **What is Backtesting:** evaluating a trading strategy on historical data to estimate its performance without risking capital. prereqs: none.
- **Backtesting vs Simulation:** backtesting runs on *historical* data; simulation can use synthetic/future hypothetical scenarios. prereqs: what is backtesting.
- **Backtesting Process:** the step-by-step pipeline (get data, pre-process, define rules, execute, measure). prereqs: what is backtesting; financial data.
- **Key decisions & parameters for backtesting:** period selection, dataset scope, bias avoidance. prereqs: what is backtesting.
- **Backtesting platforms:** tools used to construct and run backtests. prereqs: what is backtesting.
### Section: Section 3 - Financial Data
- **Financial data:** price (OHLCV), fundamental, sentiment and news data used as inputs to a strategy. prereqs: none.
- **Financial data storage:** organization/persistence of price & volume data for analysis. prereqs: financial data.
- **Limitations of financial data:** data is not always available, may be missing/erroneous, survivorship-ed; affects result reliability. prereqs: financial data.
- **Getting market data via APIs / Python packages:** retrieving data programmatically (pandas, yfinance-style tools). prereqs: financial data; Python basics.
- **Fundamental & sentiment data sources:** alternate data feeds beyond prices. prereqs: financial data.
### Section: Section 4 - Data Pre-Processing
- **Data pre-processing / cleaning:** handling incorrect and missing values so analysis is statistically valid. prereqs: financial data.
- **Data cleaning importance:** erroneous values produce disastrous/misleading backtest results. prereqs: data pre-processing.
- **Survivorship bias:** using only currently-listed stocks inflates performance because delisted (failed) stocks are excluded. prereqs: data pre-processing; financial data.
- **Look-ahead bias:** using information not yet available at the trade time; avoided with point-in-time databases. prereqs: survivorship bias.
### Section: Section 5 - Trading Rules
- **Developing trading rules:** encoding a strategy's entry/exit logic explicitly and consistently. prereqs: backtesting.
- **Entry and Exit rules:** the specific conditions that open and close positions. prereqs: trading rules.
### Section: Section 6 - Trade Level Analytics
- **Trade level analytics I:** per-trade measures used to inspect individual trades. prereqs: trading rules.
- **Trade level analytics II:** win ratio, average P&L of winning trade, profit factor, average trade duration. prereqs: trade level analytics I.
- **Average Profitability Per Trade (APPT):** P/L ratio alone is insufficient; APPT combines win rate and payoff. prereqs: trade level analytics.
- **17 common trading metrics:** suite of metrics to interpret a strategy's generated trades. prereqs: trade level analytics.
### Section: Section 7 - Performance Metrics
- **Equity Curve:** cumulative value/growth of a strategy over time. prereqs: cumulative returns.
- **CAGR (Compound Annual Growth Rate):** annualized return of the equity curve. prereqs: equity curve; cumulative returns.
- **Sharpe Ratio:** excess return per unit of total risk (volatility). prereqs: returns; standard deviation.
- **Sortino Ratio:** Sharpe-type measure using only downside volatility. prereqs: Sharpe ratio.
- **Maximum Drawdown:** largest peak-to-trough decline in the equity curve — a core risk measure. prereqs: equity curve.
- **Cumulative Returns (computation):** product of successive (1+r) terms; can be expressed as growth multiplier or as percentage (−1). prereqs: returns.
- **Performance/risk metrics & strategy optimisation:** metrics used not just to measure but to tune strategies. prereqs: performance metrics.
### Section: Section 8 - Risk Management
- **Stop-Loss and Take-Profit:** predefined exit levels limiting loss and locking profit. prereqs: entry/exit rules; performance metrics.
- **Guidelines for setting Stop-Loss / Take-Profit:** how to choose levels (e.g., via MAE). prereqs: stop-loss & take-profit.
- **Maximum Adverse Excursion (MAE):** worst adverse price move during a trade; used to set optimum stop-loss. prereqs: stop-loss; risk management.
- **Maximum Favorable Excursion (MFE):** best favorable move; used to size positions relative to risk. prereqs: MAE; risk management.
- **Fixed vs trailing stop-loss:** trade-off between cost and protection. prereqs: stop-loss.
- **Algorithmic trading risks & checks:** operational/compliance risks of running strategies live. prereqs: risk management.
### Section: Section 9 - Transaction Costs and Slippage
- **Transaction costs:** commissions and other fees that erode strategy returns. prereqs: performance metrics.
- **Slippage:** difference between expected and actual fill price. prereqs: transaction costs.
- **Slippage decomposition:** spread, market impact, and volatility costs. prereqs: slippage.
- **Estimating and minimising slippage:** accounting for costs so backtests reflect reality. prereqs: slippage; transaction costs.
### Section: Section 10 - Paper Trading
- **Introduction to Paper Trading:** running a strategy on live/streaming data without real capital. prereqs: backtesting.
- **Advantages/disadvantages of paper trading:** validation before risking capital; psychological and data-bookkeeping caveats. prereqs: paper trading.
- **Things to keep in mind while paper trading:** how long to paper trade, realistic fills, discipline. prereqs: paper trading; slippage.
### Section: Section 13 - Common Pitfalls in Backtesting
- **Biases to avoid:** general category of systematic errors in backtests. prereqs: data pre-processing.
- **Survivorship & look-ahead bias via point-in-time data:** using point-in-time databases to avoid biases. prereqs: survivorship bias; look-ahead bias.
- **Data Snooping:** testing many parameter combinations until one 'works' by chance (multiple-testing problem). prereqs: biases; statistics basics.
- **Common mistakes with trading volume:** assuming you can trade more than available volume/liquidity. prereqs: financial data; slippage.
- **Over-reliance on backtesting:** backtests are no guarantee of future live performance. prereqs: backtesting.
- **LTCM case study:** importance of risk management (Long Term Capital Management collapse). prereqs: risk management.
### Section: Section 14 - FAQs
- **Ideal time period for backtesting:** choosing a representative sample window. prereqs: backtesting.
- **Number of assets to backtest on:** diversification vs overfitting trade-off. prereqs: backtesting.
- **Risk metrics and Sharpe ratio questions:** interpretation of common metrics. prereqs: Sharpe ratio; risk management.
- **Paper vs live trading differences:** why live results differ from backtest. prereqs: paper trading.
### Section: Section 15 - Capstone Project
- **Capstone project — moving-average crossover backtest:** build & backtest a long-only 9/21-day MA crossover on 4 stocks; equal-weighted portfolio; compute CAGR, Sharpe, MaxDD. prereqs: all prior sections.
### Section: Section 17 - Course Summary
- **Course recap and next steps:** entire backtesting process; follow-on Python-for-trading courses. prereqs: all prior sections.
## Course Prerequisite Map
- Backtesting itself is foundational (needs only market basics): *Backtesting → Simulation, Process, Platforms, FAQs, Capstone.*
- Financial data builds on none; *Financial Data → Storage → Pre-Processing → Survivorship/Look-ahead bias.*
- Trading Rules needs backtesting; *Trading Rules → Entry/Exit → Trade Level Analytics.*
- Performance Metrics needs returns: *Returns → Cumulative Returns → Equity Curve → CAGR/Drawdown; + Sharp/Sortino.*
- Risk Management builds on Entry/Exit + Performance Metrics; *MAE/MFE → stop-loss guidelines.*
- Transaction Costs/Slippage builds on metrics; *Transaction Costs → Slippage (spread/impact/vol).*
- Paper Trading and Common Pitfalls build on backtesting + data + statistics fundamentals.
- Course flow: **Introduction → Backtesting → Financial Data → Pre-Processing → Trading Rules → Trade Analytics → Performance Metrics → Risk Mgmt → Costs/Slippage → Paper Trading → Pitfalls → FAQs → Capstone.**
- FunPath basics feeding this course (from Track ladder): Python basics for trading, returns math (simple/cumulative/log), basic statistics (mean, std, correlation).