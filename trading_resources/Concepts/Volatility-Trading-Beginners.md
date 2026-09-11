# Volatility Trading for Beginners — Exhaustive Concept Inventory
## COURSE: Volatility Trading for Beginners
## MODULE: Calculating Beta
### LESSON: Calculate Beta With Python (`Calculate Beta With Python.ipynb`)
- **CONCEPT:** Beta — a measure of a stock's volatility relative to the benchmark (e.g. S&P 500); beta > 1 means the stock overperforms/moves more than the benchmark, beta < 1 less. prereqs: none
- **CONCEPT:** Benchmark return — the reference index (S&P 500) return series against which a stock's returns are regressed to estimate beta. prereqs: index returns
- **CONCEPT:** Daily returns — computing each asset's day-to-day percentage change (`pct_change()`), the raw input to beta regression. prereqs: percentage change
- **CONCEPT:** Ordinary Least Squares (OLS) regression — linear regression via statsmodels `sm.OLS(y, x).fit()`; the slope of regressing stock returns on index returns is beta. prereqs: linear regression, slope
- **CONCEPT:** Independent vs dependent variable — index returns (x, independent) and stock returns (y, dependent) in the regression; beta is the coefficient of x. prereqs: regression roles
- **CONCEPT:** Constant/intercept term — `sm.add_constant` adds the intercept; omitting it forces the intercept to zero and estimates only the slope, avoiding overfitting. prereqs: intercept, model specification
- **CONCEPT:** y-intercept and slope from `.params` — reading the fitted intercept (`params[0]`) and beta/slope (`params[1]`) from the fitted model. prereqs: fitted parameters
- **CONCEPT:** Regression equation `y = a + bx` — using the intercept and beta in the line equation to reconstruct estimated stock returns from index returns. prereqs: linear equation
- **CONCEPT:** Scatter plot of returns — plotting index returns vs stock returns and overlaying the fitted regression line to visualise the slope and relationship. prereqs: scatter plot, matplotlib
- **CONCEPT:** Beta and the CAPM link — interpreting beta (estimated here) for use later in the Capital Asset Pricing Model (CAPM) expected-return framework. prereqs: beta, CAPM
## MODULE: Research on BAB (Betting Against Beta)
### LESSON: Research on the BAB Strategy — I (`Research on BAB - I.ipynb`)
- **CONCEPT:** Betting-Against-Beta (BAB) — Frazzini & Pedersen's (2014) strategy that argues against holding high-beta stocks; instead going long low-beta and short high-beta stocks to obtain positive risk-adjusted returns. prereqs: CAPM, beta
- **CONCEPT:** CAPM high-beta appeal — under the Capital Asset Pricing Model, high-beta stocks are expected to give higher expected returns, which attracts investors to them. prereqs: CAPM, expected return
- **CONCEPT:** Frazzini–Pedersen hypothesis — the empirical claim that betting against beta (long low beta, short high beta) produces superior risk-adjusted performance. prereqs: BAB idea, risk-adjusted return
- **CONCEPT:** Train/test split of data — dividing the price sample into a train year (to estimate betas) and a test year (to evaluate performance), so results are out-of-sample. prereqs: overfitting avoidance, train/test
- **CONCEPT:** `calc_beta` via OLS — function that regresses a stock's returns on market returns and returns the slope (beta). prereqs: OLS, beta
- **CONCEPT:** Computing stock returns (`pct_change`) — train-sample daily returns used to regress betas. prereqs: percentage change
- **CONCEPT:** Beta for all stocks via `apply` — applying `calc_beta` across every stock column (axis=0) to get a beta value per stock. prereqs: pandas apply, beta
- **CONCEPT:** Beta quantile buckets — using `pd.qcut(beta, q=20)` to split the ~487 stocks into 20 beta buckets, each with ~25 stocks, from lowest (bucket 1) to highest (bucket 20) beta. prereqs: quantiles, sorting
- **CONCEPT:** Bucket return performance — computing each stock's test-period return and averaging by beta bucket to examine the low-to-high beta return pattern. prereqs: grouping, means
- **CONCEPT:** Downward slope of returns vs beta — observing that returns decline from low-beta to high-beta buckets, supporting the hypothesis that shorting high beta would be profitable. prereqs: bucket returns, trend
### LESSON: Research on the BAB Strategy — II (`Research on BAB - II.ipynb`)
- **CONCEPT:** Multi-year validation — extending the BAB backtest from a 2-year window (2021–2022) to a longer 7-year span (2015–2022) to check whether the hypothesis holds more reliably. prereqs: BAB research design
- **CONCEPT:** Iterated yearly train/test loop — a `for` loop over years that treats each year as training data and the next year as test data, recomputing beta buckets and bucket-return plots each iteration. prereqs: loops, train/test split
- **CONCEPT:** `get_performance` helper — a function encapsulating beta calculation, quantile bucketing, and per-bucket return averaging/plotting for one train/test pair. prereqs: functions, beta buckets
- **CONCEPT:** try-except end-of-data guard — using a try-except block so that when the loop requests a nonexistent next-year test set (e.g. training on 2022 requiring 2023), execution stops gracefully. prereqs: error handling
- **CONCEPT:** Slope direction across years — summarising whether each year's bucket-return curve slopes upward or downward (only 2 of 7 years downward), used to test the generality of the BAB claim. prereqs: trend interpretation
- **CONCEPT:** Hypothesis not confirmed on recent data — concluding that betting against beta was not consistently profitable in the more recent sample, motivating a pivot to long-only high-beta backtests. prereqs: BAB hypothesis, empirical results
## MODULE: Backtesting BAB
### LESSON: Backtesting the BAB Strategy — I (`BAB Backtesting - I.ipynb`)
- **CONCEPT:** Long-only high-beta backtest — following the research conclusion that over most years going long high-beta stocks makes sense, backtesting a long-only portfolio of the highest-beta S&P 500 stocks for 2016. prereqs: high-beta stocks, research on BAB
- **CONCEPT:** Beta estimation on a training year — calculating betas on the prior year's (2015) returns using the calc_beta/OLS function, then applying them to trade the test year (2016). prereqs: beta, train/test
- **CONCEPT:** Rolling-year change detection — detecting a new calendar year via `data.index[i].year != data.index[i-1].year` to isolate train-year data. prereqs: looping, datetime year
- **CONCEPT:** Beta for a whole panel — `apply(calc_beta, args=(S&P500 returns,), axis=0)` computes each stock's beta against the S&P 500 for the train year. prereqs: pandas apply, OLS
- **CONCEPT:** Descending beta ranking — `beta_df.rank(ascending=False, axis=1)` ranks stocks from highest to lowest beta across each row (axis=1). prereqs: ranking, axis semantics
- **CONCEPT:** Top-bucket stock selection — selecting the first 20 ranked (high-beta) stocks as the long universe; assigning 1 to those chosen and 0 otherwise via `applymap`. prereqs: ranking, threshold selection
- **CONCEPT:** Equally-weighted portfolio returns — averaging the selected stocks' daily returns (`mean(axis=1)`) to compute an equal-weight portfolio backtest. prereqs: mean, pct_change
- **CONCEPT:** Strategy analytics (`qa.strategy_stats`) — a helper module reporting the top 5 largest drawdowns and summary metrics (Sharpe ratio, CAGR, MDD) for a returns series. prereqs: analytics module
- **CONCEPT:** Result interpretation — decent CAGR (e.g. 18.04%) but low risk-adjusted Sharpe (0.70) for the single-year backtest, motivating a longer validation. prereqs: Sharpe, CAGR, MDD
### LESSON: Backtesting the BAB Strategy — II (`BAB Backtesting - II.ipynb`)
- **CONCEPT:** Multi-year long-only BAB backtest — rebalancing the high-beta portfolio annually from 2015 to 2022 to validate the strategy over a longer window. prereqs: BAB backtesting I, annual rebalancing
- **CONCEPT:** Annual beta estimation loop — for each new year, estimating betas on the prior year and storing them, producing a beta_df indexed by each test year's start. prereqs: loops, beta
- **CONCEPT:** Signals spanning the whole period — creating a `signals` dataframe covering all trading days by concatenating yearly long-asset flags with the remaining data index, sorting, and forward-filling. prereqs: concat, ffill, index alignment
- **CONCEPT:** Position persistence via forward fill — filling the signals NaN gaps with the previous yearly selection (`fillna(method='ffill')`) so positions persist between rebalances. prereqs: ffill, rebalancing
- **CONCEPT:** Equally-weighted daily strategy returns — `(signals * data.pct_change()).mean(axis=1)`, combining stock returns with active-position flags into one strategy series. prereqs: signals, returns, mean
- **CONCEPT:** Strategy statistics over the broad sample — Sharpe 0.86, CAGR 25.1%, max drawdown 43.7% (2020 crash) using `qa.strategy_stats`. prereqs: Sharpe, CAGR, MDD
- **CONCEPT:** Survivorship caveat — noting the backtest ignores that some stocks entered and left the S&P 500 list between 2016–2022, a known limitation (adds survivorship bias). prereqs: survivorship bias, index constituents
## MODULE: Bollinger Bands
### LESSON: Oversold Trading Strategy (`Oversold Trading Strategy.ipynb`)
- **CONCEPT:** Bollinger Bands — a volatility envelope: middle band is a moving average, upper band = MA + (mult × moving std), lower band = MA − (mult × moving std); computed here with TA-Lib `ta.BBANDS`. prereqs: moving average, standard deviation
- **CONCEPT:** Moving average (middle band) — the rolling mean of the close over the look-back period (e.g. 20). prereqs: mean, rolling window
- **CONCEPT:** Upper/lower band multiples — `nbdevup`/`nbdevdn` multiples of the moving standard deviation added/subtracted from the moving average to form the bands. prereqs: standard deviation, bands
- **CONCEPT:** Oversold signal — a long entry when the close crosses below the lower band for the first time (today's Close < lowerband AND yesterday's Close > yesterday's lowerband). prereqs: bands, crossover detection
- **CONCEPT:** Crossover detection with `np.where` — flagging a signal when current close is below the lower band and the previous close was above it. prereqs: boolean conditions, shift
- **CONCEPT:** Average True Range (ATR) — a volatility indicator used to set dynamic stop-loss and take-profit multiples from the entry price. prereqs: true range, volatility indicator
- **CONCEPT:** Dynamic SL/TP targets — stop_loss = entry − ATR × stop_loss_multiple; take_profit = entry + ATR × take_profit_multiple; dynamically follow volatility while in a trade. prereqs: ATR, entry price
- **CONCEPT:** Event-driven backtesting loop — iterating each day, entering a long on the oversold signal and closing when the close breaches stop-loss or take-profit. prereqs: backtest loop, signals
- **CONCEPT:** Trade book / trading dataframe — a record of Position, Entry Time, Entry Price, Exit Time, Exit Price, and PnL for each trade. prereqs: dataframes, trade recording
- **CONCEPT:** PnL net of trading cost — subtracting a per-trade transaction cost (close × 0.0002 × 2 for entry+exit) from gross PnL. prereqs: transaction cost, PnL
- **CONCEPT:** Plotting positions — marking buy (green up-triangle) and sell (red down-triangle) points on the close-price chart to visualise trade timing. prereqs: scatter plotting
- **CONCEPT:** Strategy analytics & conclusion — computing Sharpe, CAGR, MDD; noting that an oversold (mean-reversion) band strategy works well for mean-reverting stocks but not for trend-following ones. prereqs: performance metrics, style fit
### LESSON: Breakout Strategy Implementation (`Breakout Strategy Implementation.ipynb`)
- **CONCEPT:** Breakout / trend-following strategy — a Bollinger-band-based trend strategy that buys when price transitions out of a squeeze into an expansion phase, for trending (non-mean-reverting) stocks. prereqs: Bollinger bands, trend following
- **CONCEPT:** Bandwidth — (upper − lower) / middle, a normalised measure of the band width that rises when volatility expands out of a squeeze. prereqs: bands, ratio
- **CONCEPT:** Rolling bandwidth — the rolling mean (e.g. 21-period) of bandwidth used as a reference to detect expansion. prereqs: rolling mean, bandwidth
- **CONCEPT:** Expansion-condition signal — entering a long when today's bandwidth > rolling bandwidth (transition to expansion) AND today's High rises above the upperband. prereqs: conditional logic, bands
- **CONCEPT:** Signal termination (0) and forward-fill — setting signal to 0 when Low falls back below the middle band (squeeze return), then forward-filling so position persists between those events. prereqs: ffill, exit condition
- **CONCEPT:** ATR-based dynamic exits — stop-loss and take-profit as multiples of ATR from the entry price (e.g. 2× and 3× for breakout strategy). prereqs: ATR, SL/TP
- **CONCEPT:** Event-driven backtesting loop & trade book — long entry on breakout signal, exit on SL/TP breach; PnL net of trading cost recorded in a trades frame. prereqs: backtest loop, PnL, trading cost
- **CONCEPT:** Strategy analytics & comparison — high Sharpe (1.29) and CAGR (85.94%) with large drawdown (51.41%), characteristic of a momentum/breakout profile; tuning suggestions include trying other stocks and a short variant. prereqs: Sharpe, CAGR, MDD
## MODULE: Entry Signals
### LESSON: Determine the Entry Points (`Determine the Entry Points.ipynb`)
- **CONCEPT:** Moving-average crossover strategy — a trend-detection method using a short and a long simple moving average; a long entry occurs when the short MA crosses above the long MA (bullish crossover). prereqs: moving averages, crossover
- **CONCEPT:** Bullish crossover — when the short-term SMA (e.g. 15-day) rises above the long-term SMA (e.g. 35-day), indicating bullishness and triggering a buy. prereqs: SMAs, comparison
- **CONCEPT:** Bearish crossover — when the short-term SMA falls below the long-term SMA, signalling bearishness (exit signal). prereqs: SMAs, comparison
- **CONCEPT:** Simple moving average (SMA) via TA-Lib — `ta.SMA(series, timeperiod)` computes a rolling average of close prices for a given span. prereqs: TA-Lib, rolling average
- **CONCEPT:** Crossover detection with two reference points — the signal fires when yesterday's SMA_15 below SMA_35 AND today's SMA_15 above SMA_35, found by shifting yesterday's values with `shift(1)`. prereqs: shift, boolean AND
- **CONCEPT:** `np.where` signal generation — conditionally assigning 1 when the crossover condition holds, else 0. prereqs: numpy where
- **CONCEPT:** Plotting entry signals — overlaying green triangles where the long-signal fires on the close-price chart. prereqs: scatter plotting
- **CONCEPT:** Saving signals to CSV (`to_csv`) — persisting the enriched dataframe (with SMA and signal columns) to `visa_signals.csv` for reuse by the exit-strategy notebooks. prereqs: pandas I/O
## MODULE: Fixed SL & TP
### LESSON: Exit Using Fixed Stop-Loss and Take Profit (`Exit Using Fixed Stop-Loss and Take Profit.ipynb`)
- **CONCEPT:** Fixed stop-loss and take-profit — pre-set percentage-based exit levels (e.g. stop 1%, take 3%) decided once at entry and unchanged regardless of market volatility. prereqs: exit rules, percentages
- **CONCEPT:** Stop-loss price — entry_price × (1 − stop_loss_percentage); a level at which a losing trade is closed. prereqs: entry price, percentages
- **CONCEPT:** Take-profit price — entry_price × (1 + take_profit_percentage); the level at which a profitable trade is banked. prereqs: entry price, percentages
- **CONCEPT:** Trade book — a tracking dataframe of Position, Entry Time, Entry Price, Exit Time, Exit Price, and PnL for all historical trades. prereqs: trade recording, dataframes
- **CONCEPT:** Position-state tracking — a binary flag (0 = flat, 1 = long) to track whether a long position is open during the backtest loop. prereqs: state machine, backtest loop
- **CONCEPT:** Backtest entry/exit loop — on a buy signal enter a long (record entry, set SL/TP levels), and while long exit whenever close breaches SL or TP, recording the closed trade. prereqs: signals, backtest loop
- **CONCEPT:** PnL net of transaction cost — exit close − entry price − (close × 0.0002 × 2) to reflect entry-plus-exit costs. prereqs: PnL, transaction costs
- **CONCEPT:** Limitation of fixed exits — fixed thresholds stay constant even in volatile conditions, causing early or inappropriate exits and losses (visible in 2019–2022 returns). prereqs: fixed levels, volatility sensitivity
## MODULE: SL & TP using ATR
### LESSON: Exit Using ATR (`Exit Using ATR.ipynb`)
- **CONCEPT:** Average True Range (ATR) — a volatility indicator measured as the average of the True Range over n periods (e.g. 14); indicates how much an asset moves on average. prereqs: true range, volatility
- **CONCEPT:** True Range (TR) — max of (High − Low), |High − prev Close|, |Low − prev Close|; the widest gap of a candle against the prior close. prereqs: OHLC, absolute values
- **CONCEPT:** ATR formula & TA-Lib computation — TR averaged over the window, computed here via `ta.ATR(high, low, close, timeperiod=14)`. prereqs: ATR formula, TA-Lib
- **CONCEPT:** Dynamic stop-loss / take-profit — SL = entry − ATR × stop_loss_multiple; TP = entry + ATR × take_profit_multiple; levels scale with current volatility instead of staying fixed. prereqs: ATR, exit levels
- **CONCEPT:** Volatility-adaptive exits motivation — fixed levels ignore volatility and exit too early or too late; ATR-based levels adjust to the asset's live volatility. prereqs: fixed-vs-dynamic contrast
- **CONCEPT:** Backtest loop and trade book — same event-driven long entry/exit loop as the fixed approach, but with ATR-computed SL/TP; higher PnL than fixed (e.g. ~$50 vs ~$35). prereqs: backtest loop, trade book
- **CONCEPT:** Comparison preview — noting returns are higher with dynamic exits, motivating a head-to-head comparison notebook. prereqs: metrics comparison
### LESSON: Comparison Between Fixed and Dynamic Approaches (`Comparison Between Fixed and Dynamic Approaches.ipynb`)
- **CONCEPT:** Trade analytics (`get_analytics`) — a summary of trading statistics for a trade book: number of longs, net profit, winners/losers counts, win/loss percentages, and average profit/loss per trade. prereqs: trade book, statistics
- **CONCEPT:** Win/loss percentage — percentage of profitable vs loss-making trades out of all long trades; dynamic approach shows a higher win percentage (e.g. 65.85% vs 62.79%). prereqs: winners/losers counts
- **CONCEPT:** Net profit comparison — dynamic ATR-based exits produced substantially higher net profit (e.g. $72.3 vs $17.1) than fixed exits. prereqs: PnL summing
- **CONCEPT:** Profit/loss per trade — average gain on winning trades and average loss on losing trades; dynamic exits may set wider stops (larger ATR) leading to larger per-trade losses but overall higher profit. prereqs: means, PnL distribution
- **CONCEPT:** Position column via `ffill` — adding a long-position indicator (1 at entry, 0 at exit) and forward-filling for the full history, to later compute strategy returns. prereqs: ffill, position tracking
- **CONCEPT:** Cumulative strategy returns — weighted daily returns (`pct_change() × shifted long_position`) compounded; the dynamic strategy's equity curve sits higher. prereqs: pct_change, cumprod, shift
- **CONCEPT:** Drawdown comparison — computing max drawdown of both equity curves; the dynamic approach's drawdown is higher (e.g. −13.52% vs −8.16%) because high-volatility ATR can set wide stops. prereqs: running maximum, drawdown
- **CONCEPT:** Sharpe ratio — (mean return / std return) × √252; a risk-adjusted performance measure where higher is better; the dynamic approach has a higher Sharpe (e.g. 0.75 vs 0.56). prereqs: mean, std, annualisation
- **CONCEPT:** Overall conclusion of the comparison — the dynamic approach performs better on net profit, win percentage, cumulative returns, and Sharpe despite occasionally larger drawdowns from volatility-scaled stops. prereqs: metric integration, trade-offs
## MODULE: Hedging Using VIX
### LESSON: Portfolio Hedging Using VIX (`Portfolio Hedging Using VIX.ipynb`)
- **CONCEPT:** Negative SPY–VIX correlation — SPY (S&P 500) and VIX (volatility) generally move inversely: portfolio falls and VIX rises during market panic; the basis for hedging. prereqs: correlation, VIX behaviour
- **CONCEPT:** VIXY as a short-term VIX ETF — an ETF tracking short-term VIX futures, used as the hedge leg versus the SPY long. prereqs: VIX, VIXY instrument
- **CONCEPT:** Hedge ratio — the quantity of VIXY per unit of SPY (e.g. 0.5); capital is allocated between legs in this ratio. prereqs: position sizing
- **CONCEPT:** Hedged daily returns — SPY daily return plus 0.5 × VIXY daily return (scaled by hedge ratio). prereqs: returns, weighting
- **CONCEPT:** Portfolio weighted return — dividing the summed returns by (1 + hedge_ratio) so the combined position normalises to one unit of capital. prereqs: weighting, normalisation
- **CONCEPT:** Cumulative portfolio return — compounding the hedged portfolio returns and comparing its equity curve to SPY alone to check hedging benefit. prereqs: cumprod, equity curve
- **CONCEPT:** VIXY monthly-return heatmap — a seaborn heatmap of VIXY returns by (year, month) showing that VIXY is negative most months—revealing that always-long hedging drags portfolio profitability. prereqs: resampling, heatmap
- **CONCEPT:** Selectivity motivation — because VIX only spikes rarely, going selectively long on VIXY (only when fear rises) improves the hedge strategy; addressed in the next section. prereqs: VIX regime behaviour
## MODULE: Selective Long on VIX
### LESSON: Going Selectively Long on VIX (`Going Selectively Long on VIX.ipynb`)
- **CONCEPT:** Selectively long VIX — holding VIXY (the hedge) only when volatility is rising, since VIX rises only during infrequent panic episodes; improves return vs always-long hedging. prereqs: VIX hedging, fear regime
- **CONCEPT:** Entry trigger with Bollinger upper band — going long VIXY when the 5-period SMA of VIXY close crosses above the upper Bollinger band (timeperiod 60, nbdevup 1.5). prereqs: SMA, Bollinger bands
- **CONCEPT:** Exit trigger on reversion — exiting the VIXY long when the 5-SMA falls back below the upper band. prereqs: bands, SMA crossover
- **CONCEPT:** Multi-period indicators — a short 5-period SMA versus a longer 60-period upper band set the hedge-timing regime. prereqs: indicator periods
- **CONCEPT:** Signal & capital margin — when no VIXY position is held, that allocated capital sits as cash; only the SPY long accrues returns. prereqs: positions, cash margin
- **CONCEPT:** Strategy returns — signal-gated VIXY returns (× hedge ratio) plus SPY returns, normalised by (1 + hedge ratio), then compounded. prereqs: hedging, weighted returns, cumprod
- **CONCEPT:** Conclusion — selectively-long VIXY outperforms always-long VIXY because VIX gains are rare; suggestions include futures data, dynamic hedge ratio, and shorting SPY when long VIXY. prereqs: comparison, enhancement ideas
## MODULE: VIX Spread
### LESSON: VIX Spread Strategy (`VIX Spread Strategy.ipynb`)
- **CONCEPT:** VIXM — an ETF tracking medium-term VIX futures, used as the long leg to hedge the short leg. prereqs: VIX futures ETFs
- **CONCEPT:** VIXY short bias — instead of always long VIX (which loses money), going short VIXY is more prudent, but a short exposes the portfolio to rising-VIX panic losses. prereqs: short positions, VIX behaviour
- **CONCEPT:** Long-short VIX spread — hedging the short VIXY exposure with a long VIXM position, forming a market-neutral-style VIX spread. prereqs: long/short, hedging
- **CONCEPT:** Hedge ratio for the spread — 3 contracts of VIXM per 1 contract of short VIXY (hedge_ratio = 3). prereqs: relative sizing, hedging
- **CONCEPT:** Leg returns — VIXM daily returns scaled by the hedge ratio and VIXY returns negated (−1 for the short leg). prereqs: returns, sign flipping
- **CONCEPT:** Portfolio weighted return — summed leg returns divided by (1 + hedge ratio) to normalise the combined spread position. prereqs: normalisation, weighting
- **CONCEPT:** Cumulative spread return — compounding the long-short portfolio returns and plotting to evaluate the VIX-spread strategy's performance vs VIXY alone. prereqs: cumprod, equity curve
## MODULE: Capstone Project
### LESSON: Capstone Project (`Capstone_Project_Model_Solution.ipynb`)
- **CONCEPT:** Capstone study — a full-cross-section backtest applying the Bollinger breakout strategy to the entire S&P 500 stock universe to identify the best performers. prereqs: breakout strategy, backtesting
- **CONCEPT:** Multi-stock panel data — reading S&P 500 constituent prices over 2010–2022 with a multi-level (ticker, field) column header via `header=[0, 1]`. prereqs: multiindex columns
- **CONCEPT:** `str_perf` strategy function — a reusable function that, for one stock, builds Bollinger bands, computes bandwidth + rolling width, generates the breakout signal and an ATR/exits-free long-only run with middle-band take-profit, then returns the Sharpe, CAGR, and MDD via the `qa` helper. prereqs: breakout signal, band take-profit
- **CONCEPT:** Band-width break-out entry — entering a long when bandwidth exceeds its rolling mean AND High breaches the upper band, consistent with the breakout strategy. prereqs: bandwidth, breakout
- **CONCEPT:** Middle-band take-profit exit — exiting the long when Close exceeds the middle band (a tighter mean-reversion-style objective for the capstone variant). prereqs: Bollinger middle band, exit rules
- **CONCEPT:** Trading-cost-adjusted PnL — per-trade PnL minus trading cost (close × 0.0002 × 2). prereqs: PnL, transaction costs
- **CONCEPT:** Cross-sectional backtest loop — iterating every ticker, running `str_perf`, and storing each stock's Sharpe/CAGR/MDD in a results dataframe; a try-except skips stocks that fail to generate trades. prereqs: loops, error handling, results collection
- **CONCEPT:** Selecting the best five stocks — ranking stocks by Sharpe ratio and choosing the top five performers for the portfolio recommendation. prereqs: sorting, ranking, Sharpe