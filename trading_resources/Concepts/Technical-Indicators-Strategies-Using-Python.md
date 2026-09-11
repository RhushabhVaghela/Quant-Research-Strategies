# Technical Indicators Strategies in Python — Concept Inventory
## COURSE: Technical Indicators Strategies in Python
A () course on building and backtesting technical-indicator trading strategies in Python. Covers moving averages (SMA/EMA/WMA), MACD, RSI, ROC, volume indicators (Chaikin), TRIN, market-breadth analysis, screeners, trade sheets, transaction costs/slippage, risk management, and performance metrics. Repetitive concepts (data import, signal→return computation) are defined once in their introducing lesson and cross-referenced.
---
## MODULE: Moving Average
### LESSON: Simple Moving Average
- **Moving average (rolling average)** — the mean of a data field over a set of consecutive periods; a trend-following indicator. prereqs: none.
- **Simple Moving Average (SMA)** — moving average that weighs all data points equally. prereqs: moving average.
- **`rolling(window).mean()`** — pandas method computing a rolling average over a lookback window. prereqs: pandas.
- **Bullish crossover** — SMA crosses above the close price (candle 1 SMA below close, candle 2 SMA above close); signals an uptrend. prereqs: SMA.
- **Bearish crossover** — SMA crosses below the close price; signals a downtrend. prereqs: SMA.
- **Crossover detection with `np.where`** — identifies crossovers using conditions on current and shifted values. prereqs: numpy, shift.
### LESSON: SMA and Price Crossover
- **SMA and Price Crossover Strategy** — a long-only strategy buying when close > SMA. prereqs: SMA.
- **Entry condition** — enter long when the SMA crosses the price line from above (go long when close > SMA). prereqs: crossover.
- **Exit condition** — exit when the SMA crosses the price line from below. prereqs: crossover.
- **Signal column** — `np.where(close > SMA, 1, 0)` stores 1 for buy, 0 otherwise. prereqs: numpy.
- **`pct_change()`** — computes percentage change (returns) of a price series. prereqs: pandas.
- **Strategy returns** — `returns * signal.shift(1)`; `shift(1)` avoids look-ahead bias by using the previous signal. prereqs: returns, shift.
- **`shift(1)`** — lags a series by one period so positions are known before returns accrue. prereqs: pandas.
- **Cumulative strategy returns** — `(strategy_returns + 1).cumprod()` visualises long-term performance. prereqs: strategy returns.
### LESSON: Exercise Notebook (Precomputed SMA Signals)
- **Precomputed signal data** — reading a CSV that already contains close, SMA, and signal columns. prereqs: read_csv.
- **Trade signals dataframe** — a prices/signals dataset used to build trade sheets and metrics. prereqs: signals.
---
## MODULE: Exponential Moving Average
### LESSON: Exponential Moving Average
- **Exponential Moving Average (EMA)** — moving average assigning exponentially increasing weights to more recent data. prereqs: WMA.
- **EMA vs WMA weighting** — WMA weights rise linearly; EMA weights rise exponentially. prereqs: EMA, WMA.
- **`ewm(span=).mean()`** — pandas method computing the EMA with a lookback span. prereqs: pandas.
- **EMA price-crossing strategy** — buy when close > EMA (signal 1), exit on bearish crossover. prereqs: EMA.
- **`get_strategy_returns()`** — utility function plotting signals, returns, cumulative returns, and drawdowns. prereqs: strategy returns.
---
## MODULE: Weighted Moving Average
### LESSON: Weighted Moving Average
- **Weighted Moving Average (WMA)** — a moving average that assigns higher weight to the most recent data point. prereqs: SMA.
- **WMA rationale** — responds faster than SMA without discarding older data. prereqs: SMA.
- **`ta.WMA(data, timeperiod)`** — TA-Lib function computing the weighted moving average. prereqs: talib.
- **WMA crossover** — buy when close price > WMA; exit on bearish crossover. prereqs: WMA, crossover.
- **Moving average choice** — SMA/WMA/EMA selection depends on holding period and response speed. prereqs: SMA, WMA, EMA.
---
## MODULE: Multiple Moving Averages
### LESSON: Moving Average Crossovers
- **Moving average crossover** — the point where one moving average cuts through another moving average. prereqs: moving average.
- **Short and long EMA** — two EMAs with different lookback periods (e.g. 100 and 500). prereqs: EMA.
- **Bullish MA crossover** — short EMA crosses above the long EMA; suggests an uptrend / long entry. prereqs: short/long EMA.
- **Bearish MA crossover** — short EMA crosses below the long EMA; suggests a downtrend / exit. prereqs: short/long EMA.
- **Crossover entry** — go long when the short EMA > long EMA. prereqs: crossover strategy.
- **Exponential Moving Average Crossover Strategy** — use two EMAs to generate buy/sell signals. prereqs: EMA, crossover.
### LESSON: Triple Crossover Strategy
- **Triple Crossover Strategy** — adds a medium EMA to the double crossover (short, medium, long EMAs). prereqs: double crossover.
- **Triple entry condition** — enter long when the short EMA crosses both the long and medium EMAs from below. prereqs: crossover.
- **Signal for triple crossover** — buy when short EMA > long EMA AND short EMA > medium EMA. prereqs: numpy.
- **Signal reduction** — more moving averages reduce false signals but can miss profitable opportunities. prereqs: triple crossover.
---
## MODULE: MACD
### LESSON: MACD
- **MACD (Moving Average Convergence Divergence)** — momentum indicator from two EMAs. prereqs: EMA.
- **MACD line** — fast-period EMA minus slow-period EMA (default 12 and 26). prereqs: EMA.
- **Signal line** — EMA of the MACD line (default 9-period). prereqs: MACD line.
- **MACD histogram** — MACD line minus signal line. prereqs: MACD line, signal line.
- **`ta.MACD(close)`** — TA-Lib returns MACD line, signal line, and histogram. prereqs: talib.
- **Buy signal** — buy when the MACD line crosses above the signal line (`MACD line > Signal line`). prereqs: MACD components.
- **Exit signal** — exit when the MACD line crosses below the signal line. prereqs: MACD components.
- **`np.where` for signals** — vectorized conditional to build a 1/0 signal column. prereqs: numpy.
---
## MODULE: Multiple Timeframes
### LESSON: Data Resampling
- **Multiple timeframe analysis** — studying price charts across more than one timeframe. prereqs: none.
- **Data resampling** — converting minute data into longer candles (e.g. 15min, 240min) with `resample()`. prereqs: pandas.
- **OHLCV resample dict** — open→first, high→max, low→min, close→last, volume→sum. prereqs: resampling.
- **`resample(freq, label, closed).agg(dict)`** — aggregates minute data to a chosen frequency. prereqs: pandas.
- **Short and long SMA per timeframe** — compute `sma_short`/`sma_long` (e.g. rolling 50 and 200) in both timeframes. prereqs: SMA, resampling.
- **`pd.merge`** — merges two dataframes on their datetime index with suffixes per timeframe. prereqs: pandas.
- **`fillna(method='ffill')`** — forward-fills missing values after merging frequencies. prereqs: merge.
- **Column selection** — filter the merged dataframe to the columns needed for the strategy. prereqs: dataframe.
### LESSON: Multiple Timeframe Strategy
- **Higher/lower timeframe** — e.g. 240min (higher, trend direction) and 15min (lower, entry/exit timing). prereqs: data resampling.
- **Timeframe selection** — higher timeframe under 1 day (240min); lower from a factor of 4 (240 / 4 / 4 = 15min). prereqs: resampling.
- **Crossover per timeframe** — bullish crossovers identified in both `crossover_15min` and `crossover_240min` columns. prereqs: crossover.
- **Multiple-timeframe entry** — enter long only when bullish crossover is confirmed in BOTH higher and lower timeframes. prereqs: multi-timeframe.
- **Multi-timeframe signal** — `np.where(crossover_240min, 1, 0) * crossover_15min`. prereqs: numpy.
- **Trend confirmation** — higher timeframe sets trend direction; lower timeframe confirms timing. prereqs: multi-timeframe.
- **Three-timeframe extension** — higher (major), medium (minor), and lower (signals) timeframes. prereqs: multiple timeframe.
---
## MODULE: ROC
### LESSON: Rate of Change
- **ROC (Rate of Change)** — percentage change in prices between current and price N periods ago. prereqs: none.
- **`pct_change(period)`** — pandas method computing ROC over a gap (default 1). prereqs: pandas.
- **Positive/negative momentum** — positive ROC implies rising prices; negative ROC implies falling prices. prereqs: ROC.
- **ROC semi-annual** — `pct_change(125)` compares price to ~6 months ago. prereqs: ROC.
- **ROC long-only strategy** — signal 1 when ROC_125 > 0 (buy), else 0 (no position). prereqs: ROC, signals.
---
## MODULE: Chaikin Oscillator
### LESSON: Volume Indicators
- **Volume indicators** — evaluate a security's buying vs selling pressure and which side controls price action. prereqs: none.
- **Chaikin A/D** — cumulative volume line built from price changes; measures buying/selling pressure. prereqs: volume indicators.
- **`ta.AD(high, low, close, volume)`** — computes the Chaikin accumulation/distribution line. prereqs: talib.
- **Chaikin Oscillator** — momentum of the Chaikin A/D line; the difference of slow and fast EMA of Chaikin AD. prereqs: Chaikin A/D.
- **`ta.ADOSC(high, low, close, volume, fastperiod, slowperiod)`** — computes the Chaikin oscillator. prereqs: talib.
- **Interpreting the oscillator** — >0 means buying pressure has momentum; ≤0 means selling pressure has momentum. prereqs: Chaikin oscillator.
### LESSON: Trading Hypothesis
- **Trading hypothesis** — a stated rule linking indicator behaviour to entry/exit decisions before implementation. prereqs: none.
---
## MODULE: Chaikin Oscillator Strategy
### LESSON: Chaikin Oscillator Strategy
- **Chaikin long-only strategy** — buy when Chaikin Oscillator > 0, hold while above 0. prereqs: Chaikin oscillator.
- **Entry condition** — open long when `chaikin_osc > 0`. prereqs: Chaikin oscillator.
- **Exit condition** — close long when Chaikin ≤ 0. prereqs: Chaikin oscillator.
- **Chaikin signal** — `np.where(chaikin_osc > 0, 1, 0)`. prereqs: numpy.
### LESSON: Chaikin Oscillator and Bollinger Bands Strategy
- **Bollinger Bands** — the bands of an SMA plus/minus a multiple of a moving standard deviation. prereqs: SMA.
- **`ta.BBANDS(series, period, nbdevup, nbdevdn)`** — returns upper, middle, and lower bands. prereqs: talib.
- **Upper/middle/lower band** — moving average middle band; upper/lower set by moving std ± dev. prereqs: Bollinger band.
- **Composite entry** — long entry when Chaikin crosses below the lower band (likely reversal up). prereqs: Bollinger band, oscillator.
- **Long exit** — exit when Chaikin crosses above the middle band. prereqs: oscillator, bands.
- **Short entry** — go short when Chaikin crosses above the upper band. prereqs: oscillator, bands.
- **Short exit** — exit short when Chaikin crosses below the middle band. prereqs: oscillator, bands.
- **Long/short signal combination** — sum long (+1) and short (−1) signals into one column. prereqs: signals.
---
## MODULE: Transaction Costs and Slippage
### LESSON: Implementation of Transaction Cost and Slippage
- **Transaction costs** — commissions, individual taxes, and exchange-mandated fees on executed trades. prereqs: none.
- **Brokerage cost** — a broker commission as % of traded value (e.g. 0.03%) plus taxes (e.g. 0.02%). prereqs: none.
- **Slippage** — the difference between the expected and actual execution price. prereqs: none.
- **Slippage modelling** — estimate from the last five-minute candles of each trading day using groupby. prereqs: groupby.
- **Buy-order slippage** — worst/buy execution at the high: `(high − close)/close`. prereqs: slippage.
- **Sell-order slippage** — worst/sell execution at the low: `(close − low)/close`. prereqs: slippage.
- **Total charges** — transaction cost + slippage + brokerage, applied on net position changes. prereqs: all costs.
- **Net strategy returns** — deduct trading cost (total charges × |signal − signal.shift(1)|) from gross returns. prereqs: strategy returns, costs.
- **Cost impact** — transaction costs can convert a profitable backtest (5x) into a marginal result (0.2x). prereqs: net returns.
---
## MODULE: Relative Strength Index
### LESSON: Relative Strength Index
- **RSI (Relative Strength Index)** — oscillator measuring trend strength, ranging 0–100, identifying overbought/oversold regions. prereqs: none.
- **`ta.RSI(close, timeperiod)`** — TA-Lib computes RSI with a lookback period (default 14). prereqs: talib.
- **Oversold region** — RSI < 30 implies the stock may reverse up, a possible buy. prereqs: RSI.
- **Overbought region** — RSI > 70 implies overbought, a possible sell/exit. prereqs: RSI.
- **RSI long-only strategy** — long entry when RSI < 30; exit when RSI > 70. prereqs: RSI.
- **Forward-filling signals** — `fillna(method='ffill')` keeps a position until an exit triggers. prereqs: signal.
---
## MODULE: Calculation of TRIN Indicator
### LESSON: Calculation of TRIN Indicator
- **TRIN indicator** — a market breadth tool using price and volume of an index's constituents. prereqs: none.
- **Market breadth** — a measure of how many market stocks are moving in a given direction. prereqs: none.
- **Advancing/declining stocks** — count of index constituents whose price rose vs. fell versus yesterday. prereqs: market breadth.
- **AD ratio** — number of advancing stocks divided by the number of declining stocks. prereqs: market breadth.
- **`AU` volume ratio** — traded volume of advancing stocks divided by volume of declining stocks. prereqs: market breadth.
- **TRIN formula** — TRIN = AD ratio / AD volume ratio. prereqs: AD ratio, AD volume ratio.
- **TRIN = 1 (neutral)** — a balanced market when advancing equals declining counts and volumes. prereqs: TRIN.
- **TRIN < 1 (bullish)** — more volume in advancing stocks, interpreted as an uptrend. prereqs: TRIN.
- **TRIN > 1 (bearish)** — more volume in declining stocks. prereqs: TRIN.
- **`diff()`** — pandas method computing the change from the previous row. prereqs: pandas.
---
## MODULE: TRIN Indicator Based Strategy
### LESSON: Implementation of TRIN Strategy
- **TRIN limitation** — TRIN fails in extreme scenarios, so decompose it into AUD and AUD-volume ratios. prereqs: TRIN.
- **Trinity This smoothing** — calculate a 9-day SMA of the AD ratio and AD volume ratio to reduce false signals. prereqs: SMA.
- **TRIN buy signal** — buy when both AD ratio and AD volume ratio are below their respective SMAs. prereqs: TRIN components.
- **TRIN exit signal** — exit when either the AD ratio or AD volume ratio rises above its SMA. prereqs: TRIN components.
- **Strategy vs index returns** — compare the strategy's cumulative returns against the S&P500 buy-and-hold. prereqs: cumulative returns.
---
## MODULE: Creation of a Screener Using Technical Indicators
### LESSON: Implementation of Screener Using Three Indicators
- **Technical-indicator screener** — filters stocks by conditions using indicator values. prereqs: indicators.
- **Screener indicators** — ADX (trend), Chaikin ROC oscillator, and SMA; plus volatility (order/rule step). prereqs: ADX, ROC, SMA.
- **Positive vs negative ADX** — drop stocks where the positive-direction ADX is below the negative-direction ADX. prereqs: screener.
- **Ranking indicator values** — use `rank()` on each indicator column when comparing stocks. prereqs: pandas.
- **Low-volatility filter** — sift out top N low-volatility stocks to reduce risk. prereqs: ranking.
- **Score and sort** — take the equal-weight average of indicator ranks, sort descending, keep the top 20. prereqs: ranking.
- **`pd.read_html`** (in capstone) — read tables directly from a Wikipedia page via pandas. prereqs: pandas.
### LESSON: Technical Analysis Dashboard
- **Technical Analysis Dashboard** — input a ticker and get indicator values plus trading signals. prereqs: none.
- **Dashboard data load** — `yf.download(stock, date, auto_adjust=True)` fetches the asset data. prereqs: yfinance.
- **Moving-average signals** — buy signal if the last price > the MA value over several periods, otherwise sell. prereqs: moving average.
- **Oscillator values** — record the last day's ADX (14), Money Flow Index, and modern. prereqs: talib.
- **Volume indicator section** — compute the Chaikin A/D oscillator (`ta.ADOSC`). prereqs: Chaikin.
- **Market breadth** — the percentage of S&P500 stocks above short/long SMAs; >60% implies an uptrend. prereqs: SMA, market breadth.
---
## MODULE: Putting It All Together
### LESSON: Multiple Indicator Strategy
- **Multiple indicator strategy** — combine indicators of different categories (trend + volume). prereqs: none.
- **Price ROC** — `close.pct_change(500)` for a long-horizon trend measurement. prereqs: ROC.
- **Chaikin Oscillator ROC** — `chaikin_osc.pct_change(500)` measures volume momentum. prereqs: Chaikin oscillator.
- **Entry condition** — enter when oscillator ROC > 0 AND price ROC > 0.05. prereqs: ROC.
- **Exit condition** — exit when oscillator ROC < 0 OR price ROC < 0. prereqs: ROC.
- **Signal reduction** — combining indicators reduces false signals and can miss opportunities. prereqs: multiple-indicator strategy.
---
## MODULE: Risk Management
### LESSON: ATR-Based Stop-Loss and Take-Profit
- **Fixed stop-loss/taking-profit limitation** — fixed levels ignore market volatility, causing early/late exits. prereqs: none.
- **ATR (Average True Range)** — a volatility gauge of how much an asset moves on average over a period. prereqs: none.
- **True range** — `max(High−Low, |High−Prev Close|, |Low−Prev Close|)`. prereqs: ATR.
- **ATR calculation** — the average of true range over n periods. prereqs: true range.
- **`ta.ATR(high, low, close, timeperiod)`** — computes the ATR. prereqs: talib.
- **ATR-based stop-loss** — the stop level set at a multiple of ATR away from entry price. prereqs: ATR.
- **ATR-based take-profit** — the take-profit at a multiple of ATR away from entry price. prereqs: ATR.
- **Trade book with ATR exits** — a trade sheet capturing entry/exit when the stop-loss or target hits. prereqs: trade book.
- **Volatility-aware improvement** — ATR-adjusted exits raised cumulative return and Sharpe ratio (crucial example). prereqs: ATR exits.
---
## MODULE: Trade Sheet
### LESSON: Generate Trade Sheet
- **Trade sheet** — records all trades with Position, Entry Date/Price, Exit Date/Price, PnL. prereqs: none.
- **Long crossover confirmation** — `close < SMA` on the previous candle and `close ≥ SMA` now. prereqs: crossover.
- **Exit crossover confirmation** — `close > SMA` on the previous and `close ≤ SMA` now. prereqs: crossover.
- **Iterative trade recording** — loop over dates, treat on entry confirmation and close on exit confirmation. prereqs: loops, signals.
- **Trade PnL** — `(Exit Price − Entry Price) × Position`. prereqs: trade sheet.
---
## MODULE: Performance Analysis
### LESSON: Trade Level Analytics
- **Trade-level analytics** — metrics evaluating a strategy after each trade executes. prereqs: trade sheet.
- **TradeTotal PnL** — the sum of gains and losses across all trades. prereqs: trade sheet.
- **Win rate/percentage** — winning trades / total trades × 100. prereqs: trade sheet.
- **Loss percentage** — losing trades / total trades × 100. prereqs: trade sheet.
- **Per-trade PnL winners/losers** — mean profit per winning and mean loss per losing trade (absolute value). prereqs: trade analytics.
- **Average trade duration** — average holding period; locked capital reduces simultaneous trades. prereqs: trade dates.
- **Profit given Factor** — (Win% × avg win) / (Loss% × avg loss); money made vs lost. prereqs: trade analytics.
- **Profit-factor interpretation** — <1 unprofitable, =1 breakeven, >1 desired. prereqs: profit factor.
- **Low win rate with profits** — a strategy can profit even below a 50% win rate if gains outsize losses. prereqs: win rate.
### LESSON: Performance Metrics
- **Performance metrics** — analyze returns between a trade's entry and exit. prereqs: trade-level analytics.
- **Equity curve** — plot of cumulative strategy returns; consistent positive slope implies profit. prereqs: strategy returns.
- **Cumulative return** — `(strategy_return + 1).cumprod()`. prereqs: strategy returns.
- **CAGR** — the compound annual growth rate of the strategy. prereqs: cumulative returns.
- **Histogram of returns** — distribution of the strategy returns. prereqs: strategy returns.
- **Annualised volatility** — `std(strategy_returns) × sqrt(252 × n)` for candles per day. prereqs: returns.
- **Sharpe ratio** — `(R_x − R_f)/σ_x`; mean excess return per unit of risk; >1 preferred. prereqs: returns, volatility.
- **Risk-free rate** — the return of a risk-free asset used in the Sharpe ratio. prereqs: Sharpe.
- **Maximum drawdown** — `(Peak − Trough)/Peak` of cumulative equity; the largest peak-to-trough loss. prereqs: equity curve.
- **`cummax()`** — pandas rolling maximum to track the peak for drawdown. prereqs: pandas.
- **Drawdown series** — `(Cumulative − Peak)/Peak`. prereqs: maximum drawdown.
- **`get_strategy_returns()`** — reusable helper computing and plotting returns + performance metrics. prereqs: all metrics.
---
## MODULE: Capstone Project
### LESSON: Capstone Project (Solution + Template)
- **Capstone project** — build and backtest a strategy combining market breadth, SMA, and Supertrend. prereqs: all modules.
- **Market breadth analysis** — the percentage of S&P500 stocks above their 50-SMA. prereqs: market breadth, SMA.
- **Long-term trend signal** — Apple's daily close > 50-period SMA. prereqs: SMA.
- **Multiple-frequency merge** — merge 15-min signals with the daily SMA using `pd.merge` + ffill. prereqs: merge, resample.
- **Supertrend indicator** — ATR-based bands indicating an uptrend. prereqs: ATR.
- **Supertrend parameters** — `atr_period = 27×14`, `atr_multiplier = 3`. prereqs: ATR.
- **`ta.ATR` in Supertrend** — uses `ta.ATR(high, low, close, timeperiod)` for the volatility bands. prereqs: ATR.
- **Combine strategy signals** — returns only when market breadth > condition, SMA crossover, and Supertrend all agree. prereqs: strategy signal.
- **Strategy returns** — `supertrend.shift(1) × close.pct_change() × sma_crossover.shift(1) × (breadth>50).shift(1)`. prereqs: multi-indicator.
- **Portfolio performance** — apply the strategy to multiple tickers and average the returns; plot cumulative. prereqs: portfolio, cumulative returns.
- **Model template vs solution** — a scaffold notebook with placeholders to build the capstone. prereqs: capstone.
---
## Technical-Indicators-Strategies-Using-Python — Section-based course structure (full lesson-by-lesson view)
# Concept Inventory — Technical Indicators Strategies in Python
## COURSE: Technical Indicators Strategies in Python
### Section: Section 1 - Introduction
- **Introduction to the course:** scope — indicators, strategies, backtesting, screener. prereqs: none.
- **Course structure (PDF, image):** learning path outline. prereqs: none.
- **FAQs (PDF):** common course questions. prereqs: none.
### Section: Section 2 - Principles of Technical Analysis
- **Principles of technical analysis:** price discounting, trends, history repeats; assumptions. prereqs: none.
- **Why technical analysis gets a bad reputation:** subjectivity and misuse critiques. prereqs: technical analysis.
- **Additional reading (PDF):** fundamental principles reading. prereqs: technical analysis.
### Section: Section 3 - Trend is your Friend
- **Trend is your friend:** trend analysis principle; trade with the prevailing trend. prereqs: technical analysis.
### Section: Section 4 - Moving Average
- **Simple Moving Average (SMA):** mean of last N prices via rolling window. prereqs: price series.
- **Classification of moving averages:** SMA/WMA/EMA families and applications. prereqs: moving average.
- **Strategy flow diagram (PDF):** building a SMA-based signal. prereqs: SMA.
- **Additional reading for data source (PDF):** fetching price data. prereqs: pandas, data.
### Section: Section 6 - Performance Analysis
- **Additional reading on performance metrics (PDF):** Sharpe, drawdown, CAGR evaluation. prereqs: returns.
- **Additional reading on trade level analytics (PDF):** per-trade win/loss analysis. prereqs: trade sheet.
### Section: Section 7 - Transaction Costs and Slippage
- **Transaction costs and slippage:** brokerage, spread, market impact; impact on net returns. prereqs: backtesting.
- **Additional reading (PDF):** cost modeling detail. prereqs: transaction costs.
### Section: Section 10 - Weighted Moving Average
- **Weighted Moving Average (WMA):** average with linearly increasing weights on recent prices. prereqs: moving average.
- **Anatomy of a candle (PDF):** OHLC anatomy. prereqs: price data.
- **Strategy flow diagram (PDF):** WMA-based signal. prereqs: WMA.
### Section: Section 11 - Exponential Moving Average
- **Exponential Moving Average (EMA):** weighted average with exponential decay favoring recent prices. prereqs: moving average.
- **EMA calculation (PDF):** recursive formula, smoothing factor. prereqs: EMA.
- **Types of moving averages (PDF):** SMA vs EMA vs WMA comparison. prereqs: moving average.
- **5 FAQs about moving averages (PDF):** lag, sensitivity. prereqs: moving average.
- **Strategy flow diagram (PDF):** EMA-based signals. prereqs: EMA.
### Section: Section 12 - Multiple Moving Averages
- **Moving average crossovers:** double and triple crossover strategies (e.g. MACD-like). prereqs: moving averages.
- **Strategy flow diagrams (PDF):** multi-MA signal pipelines. prereqs: crossovers.
- **Additional reading on moving average strategies (PDF):** applications. prereqs: crossovers.
### Section: Section 13 - MACD
- **MACD entry points:** MACD-based long/short entries. prereqs: MACD.
- **MACD line & signal line:** 12-26 EMA diff and 9 EMA signal, crossovers. prereqs: EMA.
- **MACD histogram:** (MACD line − signal line), momentum strength. prereqs: MACD.
- **Strategy flow diagram (PDF):** MACD strategy. prereqs: MACD.
### Section: Section 14 - ROC
- **ROC (Rate of Change):** momentum indicator = (P_t/P_{t-n} − 1). prereqs: price series.
- **ROC strategy logic (PDF):** trading on ROC sign/magnitude. prereqs: ROC.
### Section: Section 15 - Intuition and Interpretation of RSI
- **Intuition of RSI indicator:** measures speed/magnitude of price change, 0-100 oscillator. prereqs: momentum.
- **Interpret values of RSI:** overbought (>70) / oversold (<30) zones. prereqs: RSI.
### Section: Section 16 - Properties and Practical Application of RSI
- **Properties of RSI indicator:** bounded range, mean-reverting behavior. prereqs: RSI.
- **RSI in action:** divergences and practical signal use. prereqs: RSI.
- **RSI strategy logic (PDF):** RSI-based entry/exit. prereqs: RSI.
- **Additional reading on RSI (PDF):** detailed RSI reference. prereqs: RSI.
### Section: Section 17 - Volume
- **Spikes in volume:** identifying unusual volume surges as signals. prereqs: volume.
- **On-Balance Volume (OBV):** cumulative volume adding/subtracting by price direction. prereqs: volume, price.
### Section: Section 18 - Chaikin AD
- **Chaikin Accumulation/Distribution:** money-flow indicator from close location value vs HL range, times volume. prereqs: volume, price range.
- **Additional reading on Chaikin AD (PDF):** reference. prereqs: Chaikin AD.
### Section: Section 19 - Limitations of Chaikin AD and OBV
- **Limitations of OBV and Chaikin AD:** divergence does not always work; lag and noise. prereqs: Chaikin AD, OBV.
### Section: Section 20 - Chaikin Oscillator
- **Chaikin oscillator (PDF):** EMA(spread) of the Chaikin AD measures momentum of buying/selling pressure. prereqs: Chaikin AD, EMA.
### Section: Section 21 - Chaikin Oscillator Strategy
- **Chaikin oscillator strategy logic (PDF, image):** signal rules on oscillator. prereqs: Chaikin oscillator.
- **Bollinger Bands (PDF):** price bands at ±kσ around SMA. prereqs: SMA, std.
- **Chaikin oscillator + Bollinger strategy logic (PDF, image):** composite strategy. prereqs: Chaikin oscillator, Bollinger.
### Section: Section 22 - Putting It All Together
- **Combining indicators:** using multiple indicators for stronger confirmations. prereqs: indicators.
- **Chaikin oscillator with ROC:** composite momentum strategy. prereqs: Chaikin oscillator, ROC.
- **Strategy flow diagram (PDF):** integrated pipeline. prereqs: combining indicators.
### Section: Section 23 - Multiple Timeframes
- **Multiple timeframes:** combining e.g. 15-min + 240-min signals for context and entries. prereqs: time series.
### Section: Section 24 - ATR
- **ATR (Average True Range):** volatility measure from true range (max of high-low, high-prevClose, low-prevClose). prereqs: OHLC.
- **Additional reading for ATR (PDF):** reference and use. prereqs: ATR.
### Section: Section 25 - Risk Management
- **ATR-based SL & TP:** setting stop-loss/take-profit as multiples of ATR. prereqs: ATR.
- **Additional reading for SL & TP using ATR (PDF):** adaptive stops research. prereqs: ATR, SL/TP.
### Section: Section 26 - Market Breadth Analysis
- **Need of market breadth analysis:** assessing broad market participation beyond single index. prereqs: equity indices, technical analysis.
### Section: Section 27 - McClellan Indicator
- **McClellan indicator:** breadth indicator from exponentially smoothed advance/decline net change (AD line). prereqs: market breadth.
- **Additional reading (PDF):** reference. prereqs: McClellan.
### Section: Section 28 - Application of McClellan Indicator
- **Application of McClellan indicator:** overbought/oversold breadth signals. prereqs: McClellan.
- **Can McClellan predict a market crash:** historical crashes vs extreme breadth readings. prereqs: McClellan.
- **Additional reading (PDF):** application reference. prereqs: McClellan.
### Section: Section 29 - Calculation of TRIN Indicator
- **TRIN (Arms Index):** (advancing/declining ratio) / (adv/del volume ratio); volume-weighted breadth. prereqs: market breadth, volume.
### Section: Section 30 - TRIN Indicator Based Strategy
- **TRIN strategy:** trading on TRIN extremes (fear/greed breadth). prereqs: TRIN.
- **Flow chart of TRIN strategy (PDF, image):** signal logic. prereqs: TRIN.
- **Alternative methods for market breadth (PDF):** other breadth approaches. prereqs: market breadth.
- **Additional reading for TRIN (PDF):** reference. prereqs: TRIN.
### Section: Section 31 - Creation of a Screener Using Technical Indicators
- **Creation of a screener using technical indicators:** ranking stocks by indicator values and selecting top N. prereqs: indicators, ranking.
- **Alternative method for creating screener (PDF):** level-based vs rank-based screening. prereqs: screener.
### Section: Section 32 - Five Secrets of Successful Traders
- **Five secrets:** discipline, risk control, system, consistency, review. prereqs: none.
- **Technical analysis checklist (PDF):** pre-trade checklist. prereqs: technical analysis.
### Section: Section 33 - Capstone Project
- **Problem statement (PDF):** build an indicator-based strategy with backtesting. prereqs: all previous.
- **Code template & solution (zips):** provided code and data. prereqs: capstone.
### Section: Section 35 - Summary
- **Summary of the course:** recap and downloadable resources. prereqs: all.
- **Next steps (PDF):** what to do after the course. prereqs: all.
## Course Prerequisite Map
Before this course a learner needed: Python + pandas + NumPy for data handling and indicator math; financial OHLCV data and matplotlib plotting; moving averages and trend concepts; an understanding of returns, compounding, and basic statistics (mean, standard deviation); and foundational backtesting and performance-metric concepts (Sharpe, drawdown, transaction costs, slippage, trade-level analytics).