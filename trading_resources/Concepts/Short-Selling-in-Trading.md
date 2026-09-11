## COURSE: Short Selling in Trading
Course folder: `Short-Selling-in-Trading/Short Selling in Trading`
Notebooks: 12
---
## MODULE: Returns
- Notebook: `Stock Return Calculation/Return Calculation.ipynb`
### LESSON: Return Calculation
- **Return** — profit or loss from trading, investing, or saving. − prereqs: PnL
- **Arithmetic returns** — percentage change: (current − previous)/previous. − prereqs: prices, percentage change
- **Logarithmic returns** — natural log of (current price / previous price). − prereqs: returns, logarithms
- **Cumulative arithmetic returns** — cumulative sum of daily arithmetic returns. − prereqs: returns, cumsum
- **Cumulative log returns** — cumulative sum of daily log returns. − prereqs: log returns, cumsum
- **Time-additivity of log returns** — multi-period log return = sum of period log returns. − prereqs: log returns
- **Return histogram** — plotting the returns distribution. − prereqs: plotting, returns
## MODULE: Relative Series
- Notebook: `Relative Series/Compute the Relative Series.ipynb`
### LESSON: Compute the Relative Series
- **Relative series** — a stock restated relative to a benchmark and currency. − prereqs: returns
- **Adjustment factor** — benchmark close × exchange rate. − prereqs: multiplication
- **Relative series formula** — OHLC price divided by the adjustment factor. − prereqs: division, adjustment factor
- **Rebased series** — relative series rebased to the first stock price. − prereqs: relative series
- **Currency / benchmark effect** — separating stock moves from market and FX moves. − prereqs: exchange rate, benchmark
- **Relative-series function** — a reusable Python function (`relative`). − prereqs: functions, series
## MODULE: Stock Classification (Screener)
- Notebook: `Stock Classification/Classification of Stocks.ipynb`
### LESSON: Classification of Stocks (screener)
- **Stock screener** — a screening tool to scan a universe of stocks. − prereqs: universe, screening
- **Relative series computation** — the screener builds a relative series first. − prereqs: relative series
- **Swing detection** — 20-period local highs and lows (`argrelextrema`). − prereqs: swings, extremum
- **Regime detection** — identifying the trading phase from swings and price moves. − prereqs: swings, regime
- **Regime change date** — extracting the most recent regime shift date. − prereqs: regime detection
- **Absolute vs relative cumulative returns** — unadjusted vs benchmark-adjusted returns. − prereqs: cumulative returns, relative series
- **Loop over multiple stocks** — screening all tickers in a universe. − prereqs: loops, screening
## MODULE: Regime Detection
- Notebooks: `Regime Change Detection/Regime Change- Breakout_Breakdown Model.ipynb`, `Regime Change Detection/Regime Change- Crossover Model.ipynb`, `Regime Methods/Compare the Regimes.ipynb`
### LESSON: Moving Average Crossover (Crossover Model)
- **Moving average crossover** — short-term MA crossing above/below long-term MA defines regime. − prereqs: moving averages, trend
- **Golden / death cross** — 50/200 crossover (bullish golden, bearish death). − prereqs: SMA, crossover
- **Simple moving average (SMA)** — equal-weight windowed average of prices. − prereqs: moving averages
- **Exponential moving average (EMA)** — weighted average favouring recent price data. − prereqs: SMA, weighting
- **Regime signal** — +1 when short MA >= long MA (bullish), -1 bearish. − prereqs: crossover
- **Whipsaw problem** — MA crossover fails in sideways markets. − prereqs: crossover, sideways market
### LESSON: Breakout / Breakdown Model
- **Breakout** — price printing a new high over a 252-day (52-week) window. − prereqs: highs, rolling window
- **Breakdown** — price printing a new low over the lookback window. − prereqs: lows, breakout
- **Regime breakout signal** — go long when rebased high >= rolling high. − prereqs: breakout
- **Regime breakdown signal** — go short when rebased low <= rolling low. − prereqs: breakdown
- **Breakout-breakdown model** — combined long/short regime from new highs/lows. − prereqs: breakout, breakdown
- **Lag drawback** — unavoidable 252-day lag gives back gains to the market. − prereqs: breakout, lag
- **Low win rate** — shortening the horizon produces false positives. − prereqs: win rate, horizon
### LESSON: Compare the Regime Methods
- **Regime change comparison** — comparing crossover, breakout, and floor/ceiling regimes. − prereqs: regime, detection
- **Hindsight bias in floor/ceiling** — swings are retroactively assigned, so a lag is needed. − prereqs: floorceiling, lag
- **Cumulative return comparison** — comparing compounded returns across methods. − prereqs: cumulative returns
- **Drawdown comparison** — comparing maximum drawdowns across methods. − prereqs: drawdown
- **Golden cross advantage** — captures regime change best but with high volatility. − prereqs: crossover, drawdown
- **Method blending** — combining methods to reduce drawdown. − prereqs: regime methods
## MODULE: Floor & Ceiling
- Notebooks: `Floor and Ceiling/Swings.ipynb`, `Floor and Ceiling/Floor and Ceiling.ipynb`
### LESSON: Swing Calculation
- **Swing high / low** — local price peaks and troughs. − prereqs: prices, local extrema
- **`argrelextrema`** — scipy function to find peaks/troughs over a window. − prereqs: scipy, extrema
- **Alternation** — requiring swings to alternate high/low and keeping extreme values. − prereqs: swings
- **Eliminating non-alternating swings** — rule-based while-loop filtering of repeats. − prereqs: alternation, loops
- **Last swing adjustment** — aligning the final swing with the most recent extreme. − prereqs: swings, extremum
- **Join and crossover avoidance** — dropping existing columns before a join to avoid overlap. − prereqs: join, pandas
### LESSON: Floor & Ceiling Method
- **Floor & ceiling** — quantify distance from a peak/bottom to later swings. − prereqs: swings
- **Classic vs floor/ceiling bull–bear definition** — traditional HH/HL definitions have low statistical validity. − prereqs: bull/bear, regime
- **Volatility-standardised distance** — measuring distance in units of rolling standard deviation (3-month). − prereqs: volatility, distance
- **1.5-stdev threshold** — marks the start of a regime change. − prereqs: distance test, threshold
- **Floor/ceiling stability** — does not flip in sideways markets (unlike crossing). − prereqs: switching, regime
- **Breakout/breakdown handling** — positive or negative breakthrough changes the regime. − prereqs: breakout, floor/ceiling
- **Regime state (−1 bearish / +1 bullish)** — binary regime indicator. − prereqs: regime
## MODULE: Stop Loss and Position Sizing — Metrics
- Notebooks: `Stop Loss and Position Sizing/Position Sizing - I.ipynb`, `Stop Loss and Position Sizing/Position Sizing - II.ipynb`
### LESSON: Position Sizing - I
- **Gain expectancy** — win% × avg win% − loss% × abs(avg loss%). − prereqs: PnL, probability
- **Signal module** — the win/loss side of gain expectancy. − prereqs: gain expectancy
- **Money management module** — position sizing / avg win–loss amplitudes. − prereqs: gain expectancy
- **Equal-weight position sizing** — fixed percentage per position; relies on signals, ignores vol. − prereqs: sizing, portfolio
- **Constant equity at risk** — position sized vs a constant stop-loss distance; penalises volatile stocks. − prereqs: stop loss, volatility
- **Hit rate / miss rate** — rolling ratio of winning vs losing days. − prereqs: returns, statistics
- **Arithmetic & geometric gain expectancy** — win/loss-density measures. − prereqs: expectancy, returns
- **Gain-to-pain ratio (profit factor)** — sum(profits)/sum(losses). − prereqs: returns, profit/loss
- **Tail ratio** — quantile-based left/right tail measure on cumulative returns. − prereqs: quantile, returns
- **Common sense ratio** — profit factor × tail ratio. − prereqs: profit factor, tail ratio
- **Kelly criterion (K%)** — W − (1−W)/R based trade-size. − prereqs: win rate, win/loss ratio
- **Robustness metrics (grit, ulcer, T-stat, Calmar)** — drawdown/loss-driven robustness. − prereqs: drawdown, loss
- **Cumulative returns (log-exp form)** — expanding sum then exponential. − prereqs: returns, exponential
### LESSON: Position Sizing - II
- **Stock universe loop** — iterate four bank stocks and a MA parameter grid. − prereqs: loops
- **Relative series, swings & regime per stock** — chaining reusable function steps. − prereqs: relative, swings, regime
- **MA-cross signal within regime** — `signal_fcstmt` for entry when regime & cross align. − prereqs: regime, crossover
- **Stop-loss function** — `stop_loss(...)` for risk-adjusted position. − prereqs: stop loss
- **Transaction costs** — `transaction_costs` deducted from daily returns. − prereqs: returns, transaction costs
- **Scoreboard optimisation** — sorting parameter combinations by robustness score. − prereqs: robustness, optimisation
- **Round-lot sizing** — `round_lot` rounding shares to lots. − prereqs: sizing, shares
- **Equity-at-risk vs equal weight** — comparing the two sizing curves. − prereqs: position sizing
- **Equity-curve simulation** — simulating daily account value. − prereqs: equity curve
## MODULE: Trading Strategy
- Notebooks: `Strategy Creation/Strategy Creation.ipynb`, `Strategy Creation/Strategy Optimization.ipynb`
### LESSON: Strategy Creation
- **Gain expectancy formula reuse** — the linkage between signal and money module. − prereqs: expectancy
- **Strategy definition** — blending the three regime methods into a long/short strategy. − prereqs: regime, strategy
- **Stable, low-lag, sideways-resilient regime** — selects floor/ceiling as the base. − prereqs: regime selection
- **Signal generation (MA cross)** — short- and mid-term MAs produce entries/exits. − prereqs: MA, signals
- **Stop loss for short trades** — essential because MA lag causes false positives. − prereqs: stop loss, short
- **Long entry/exit** — long when regime==1 and st>=mt; exit when st<mt. − prereqs: regime, crossover
- **Short entry/exit** — short when regime==-1 and st<=mt; exit when st>mt. − prereqs: short, crossover
- **Stop-loss breach handling** — exit a trade when stop loss is breached. − prereqs: stop loss, signal
- **Transaction-cost function** — detect entry/exit and deduct costs. − prereqs: transaction costs, returns
### LESSON: Strategy Optimization
- **Strategy optimisation** — search over short/mid-term MA combinations. − prereqs: moving averages, optimisation
- **Relative and absolute returns** — rebased-close and raw-close log returns. − prereqs: returns, log returns
- **ST/MT permutation grid** — `itertools.product` over short/mid-term windows. − prereqs: itertools, permutations
- **Hurdle criterion** — strategy must beat max(passive, regime) returns. − prereqs: hurdle, returns
- **Performance ranking** — sorting combinations by cumulative performance. − prereqs: performance, ranking
- **Top-combination chart** — plot top 10 st/mt strategy curves. − prereqs: plotting, ranking
---
## Cross-cutting / Thematic Concepts
Recurring across many notebooks (trivial, convenience).
- **pandas / numpy time-series basics** — read_csv, diff, rolling, expanding, cumsum. − prereqs: none
- **SciPy signal processing** — `argrelextrema` for local-extremum detection. − prereqs: none
- **Custom `short_selling` module** — reusable functions (`relative`, `swings`, `regime_fc`, `returns`, `cumulative_returns`). − prereqs: packaging
---
## Short-Selling-in-Trading — Section-based course structure
# Concept Inventory — Short Selling in Trading
## COURSE: Short Selling in Trading
### Section: Section 1 - Introduction
- **About the author / course:** credibility and scope. prereqs: none.
- **Introduction to short selling:** definition and motivation for shorting an asset. prereqs: none.
### Section: Section 2 - Short Selling
- **Short selling:** selling an asset you do not own (borrowed) and buying it back later, profiting from a price decline. prereqs: stock market basics.
- **Long-short strategy:** combining long positions in undervalued stocks with short positions in overvalued ones to capture relative performance. prereqs: short selling, long positions.
### Section: Section 3 - Relative Series
- **Factors affecting a stock (PDF):** company fundamentals, sector, market, currency, benchmark that drive a stock's own path. prereqs: equity analysis.
- **Relative series:** the price series of a stock normalized relative to a benchmark, showing outperformance vs underperformance independent of the market. prereqs: price series, benchmark.
- **Calculating relative series:** dividing the stock price by a benchmark index price across each date. prereqs: relative series, pandas.
### Section: Section 4 - Stock Return Calculation
- **Returns (Additional Reading):** simple vs log returns and why log returns are used in quantitative analysis (time-additive, symmetric). prereqs: price series, math.
- **Stock return calculation:** computing daily percentage change of the relative series. prereqs: returns.
### Section: Section 5 - Regime Definition
- **Regime definition:** classifying the market into distinct states (bull/bear/trending/range) over time. prereqs: time series, trend.
### Section: Section 6 - Regime Change Detection
- **Breakout / breakdown model:** detecting a regime change when price breaks above (breakout) or below (breakdown) a level. prereqs: regimes, support/resistance.
- **Crossover model:** detecting regime change via moving-average crossovers (short vs long MA). prereqs: moving averages, regime.
### Section: Section 7 - Floor and Ceiling
- **Floor and ceiling:** price bands (floor = lower support, ceiling = upper resistance) defining a trading range. prereqs: support/resistance.
- **Swings:** local highs and lows used to identify structural turning points. prereqs: price action.
- **Lagless swing detection (zip):** an indicator that marks swings with minimal lag. prereqs: swings.
### Section: Section 8 - Regime Methods
- **Compare regime methods:** evaluating breakout/breakdown vs crossover for regime classification quality. prereqs: regimes, crossover model, breakout model.
### Section: Section 9 - Stock Classification
- **Classify stocks to bulls or bears:** assigning each stock a bull or bear label based on its regime. prereqs: regimes.
- **Flow diagram for classification (PDF, image):** visual pipeline: relative series → returns → regime detection → classification. prereqs: stock classification.
### Section: Section 10 - Strategy Creation
- **Overview of strategy creation:** building a short/hold strategy from the regime classification. prereqs: stock classification.
- **Strategy logic:** go short when classified bearish, long/hold when bullish. prereqs: classification, short selling.
- **Strategy flow diagram (PDF, image):** entry/exit signal generation from regime. prereqs: strategy logic.
### Section: Section 13 - Stop Loss and Position Sizing
- **Performance metrics:** evaluating strategy with returns, Sharpe, drawdown. prereqs: backtesting metrics.
- **Optimisation:** tuning strategy parameters (thresholds/indicators) for better out-of-sample performance. prereqs: performance metrics.
- **Stop loss and position sizing:** setting risk per trade and sizing positions. prereqs: risk management, position sizing.
### Section: Section 14 - World Stock Screener Notebook
- **World stock screener notebook (zip):** applying the short-selling screening logic across many global stocks. prereqs: stock classification, screener.
### Section: Section 16 - Course Summary
- **Course summary:** recap of relative series → regime → classification → strategy. prereqs: all previous.
- **Short selling in current market:** relevance and application today. prereqs: short selling.
## Course Prerequisite Map
Before this course a learner needed: basics of equities and short selling; price/return series and percentage (log) returns; support/resistance and trend concepts; moving averages for crossover regimes; pandas for relative-series and return computation; and an understanding of backtesting performance metrics (returns, Sharpe, drawdown).