# Candlestick Patterns — Concept Inventory
## COURSE: Candlestick Patterns
A () course on identifying Japanese candlestick patterns (bullish marubozu, hammer, hanging man, shooting star) with TA-Lib, visualising them on candlestick charts with mplfinance, and backtesting long/short strategies with stop-loss/take-profit levels. Covers trade sheets, trade-level analytics, performance metrics, data resampling, and a multi-asset capstone. Repeated concepts (strategy returns, trade analytics, performance metrics) are defined once and reused across patterns.
---
## MODULE: Bullish Marubozu Pattern
### LESSON: Visualise Bullish Marubozu
- **Candlestick chart** — visualises OHLC as candles with bodies and wicks, showing open/close/high/low. prereqs: none.
- **Bullish Marubozu** — a long-bodied candle with no (or very small) shadow, signifying extreme bullishness. prereqs: candlestick chart.
- **Bearish Marubozu** — the bearish counterpart of the bullish marubozu. prereqs: bullish marubozu.
- **`ta.CDLMARUBOZU(open, high, low, close)`** — TA-Lib returns +100 for bullish, −100 for bearish, 0 if no pattern. prereqs: talib.
- **`mplfinance` (`mpf`)** — a library for plotting candlestick charts. prereqs: none.
- **`mpf.plot(...)`** — plots a candlestick chart with `type='candle'`, style, and volume options. prereqs: mplfinance.
- **`mpf.make_addplot()`** — adds overlay markers (e.g. pattern flags) to the candlestick chart. prereqs: mplfinance.
- **Pattern marker** — place a scatter marker slightly above the high (e.g. `1.01 × High`) to flag a pattern. prereqs: addplot.
- **`np.where(pattern_signal == 100, high×1.01, np.nan)`** — builds marker positions only where the pattern occurs. prereqs: numpy.
---
## MODULE: Backtesting Bullish Marubozu
### LESSON: Backtesting Bullish Marubozu
- **Candlestick backtesting** — simulate trading on pattern signals over historical price data. prereqs: pattern identification.
- **Entry condition** — enter long at the current candle's Open if the previous candle is a bullish marubozu. prereqs: bullish marubozu.
- **Entry signal** — `np.where(pattern_signal == 100, 1, 0)`; 1 marks a long entry. prereqs: numpy.
- **Stop-loss (bullish)** — set at the minimum Low of the previous n candles. prereqs: risk/regime.
- **Take-profit (bullish)** — set at entry + (entry − SL), a risk-reward multiple of the stop. prereqs: stop-loss.
- **`exit_values()`** — helper computing stop-loss and take-profit from entry price and the last n lows/highs. prereqs: backtesting.
- **Iterative backtest loop** — walk over rows, open on entry, close when SL/TP hit, and record each trade. prereqs: loops.
- **Trade sheet** — table of Entry Date/Price, Exit Date/Price, Exit Type, PnL. prereqs: backtesting.
- **Trade signal column** — mark 1 on entry dates and 0 on exit dates, then forward-fill. prereqs: signals.
- **`isin()`** — pandas membership test used to locate entry/exit dates in the price index. prereqs: pandas.
### LESSON: Trade Level Analytics (Marubozu backtest)
- **Trade-level statistics** — metrics evaluating the strategy after each trade is executed. prereqs: trade sheet.
- **Total PnL** — the sum of gains and losses across all trades. prereqs: trade sheet.
- **Win rate/percentage** — number of winning trades / total trades × 100. prereqs: trade sheet.
- **Loss percentage** — losing trades / total trades × 100. prereqs: trade sheet.
- **Average PnL per trade** — mean profit per winning and mean loss per losing trade (absolute value). prereqs: trade sheet.
- **Average trade duration** — average holding period; capital is locked while a trade is open. prereqs: trade sheet.
- **Profit factor** — (Win% × avg win) / (Loss% × avg loss); gained dollars per lost dollar. prereqs: win rate.
- **Profit-factor interpretation** — <1 unprofitable, =1 breakeven, >1 desired. prereqs: profit factor.
### LESSON: Performance Metrics (Marubozu backtest)
- **Performance metrics** — analyse returns between a trade's entry and exit. prereqs: trade analytics.
- **Open-to-close / close-to-close returns** — `(Close/Open − 1)` and `pct_change()`. prereqs: returns.
- **Strategy returns with open-to-close handling** — apply open-to-close returns on the day a new trade enters. prereqs: strategy returns.
- **Equity curve** — plot of cumulative strategy returns; consistently positive slope implies profit. prereqs: cumulative returns.
- **Cumulative returns** — `(strategy_returns + 1).cumprod()`. prereqs: strategy returns.
- **CAGR** — compound annual growth rate; `(final^(252/days) − 1) × 100`. prereqs: cumulative returns.
- **Histogram of returns** — the distribution of the strategy returns. prereqs: strategy returns.
- **Annualised volatility** — `std(strategy_returns) × sqrt(252)` for daily data. prereqs: returns.
- **Sharpe ratio** — `(R_x − R_f)/σ_x`; excess return per unit of risk; >1 preferred. prereqs: returns, volatility.
- **Risk-free rate** — return of a risk-free asset used in the Sharpe ratio. prereqs: Sharpe ratio.
- **Maximum drawdown** — `(Peak − Trough)/Peak` of cumulative equity; the largest peak-to-trough loss. prereqs: equity curve.
- **`cummax()`** — pandas rolling maximum tracking the equity peak. prereqs: pandas.
- **Drawdown series** — `(Cumulative − Peak)/Peak`. prereqs: maximum drawdown.
---
## MODULE: Hammer Candlestick Pattern
### LESSON: Backtesting and Analysing Hammer Patterns
- **Hammer candlestick** — formed during a downtrend; signals a possible reversal of the existing downtrend (bullish). prereqs: candlestick.
- **`ta.CDLHAMMER(open, high, low, close)`** — TA-Lib returns `100` for a hammer, otherwise `0`. prereqs: talib.
- **Downtrend check** — confirm the three prior close prices are in ascending order before entering. prereqs: close series.
- **Hammer entry** — enter a long at the next candle's Open after a hammer forms, given a downtrend. prereqs: hammer pattern.
- **Hammer stop-loss** — set at the Low of the hammer candle. prereqs: risk exits.
- **Hammer take-profit** — set at entry + (rr × (entry − SL)) using a reward-to-risk ratio. prereqs: hammer stop-loss.
- **Reward-to-risk ratio (rr)** — scales take-profit relative to risk; often rr=3 for hammers. prereqs: take-profit.
- **`backtesting(data, direction, rr)`** — packaged backtest helper producing trades and signals. prereqs: backtesting.
- **`trade_level_analytics(trades)`** — packaged helper computing trade-level statistics. prereqs: trade analytics.
- **`performance_metrics(data, direction)`** — packaged helper computing strategy metrics. prereqs: performance metrics.
---
## MODULE: Hanging Man Candlestick Pattern
### LESSON: Hanging Man Notebook
- **Hanging man candlestick** — formed during an uptrend; signals a possible reversal of the existing uptrend (bearish). prereqs: candlestick.
- **`ta.CDLHANGINGMAN(open, high, low, close)`** — TA-Lib returns `−100` for a hanging man, otherwise `0`. prereqs: talib.
- **Short entry** — enter a short at the next candle's Open if the previous candle is a hanging man and an uptrend exists. prereqs: hanging man pattern.
- **Uptrend condition** — confirm the prior three close prices are in descending order. prereqs: close series.
- **Hanging man stop-loss** — set at the High of the hanging man candle. prereqs: risk exits.
- **Hanging man take-profit** — set at entry − (SL − entry), the short-side risk/reward target. prereqs: hanging man stop-loss.
- **`backtesting(data, 'short', rr=1)`** — backtest the hanging man short strategy. prereqs: backtesting.
---
## MODULE: Shooting Star Candlestick Pattern
### LESSON: Resample Data (Shooting Star preparation)
- **High-to-low resampling** — resampling is only valid from higher frequency to lower frequency. prereqs: none.
- **Price mapping** — dict mapping open→first, high→max, low→min, close→last. prereqs: resampling.
- **`resample(interval).agg(mapping)`** — converts 1-minute candles to a coarser frequency (e.g. 5min). prereqs: pandas.
- **Resample interval values** — minute `m`, hour `H`, daily `D`, weekly `W`, monthly `M`. prereqs: resampling.
- **`dropna()` on resampled data** — removes off-market (weekend/holiday) NaNs. prereqs: resampling.
- **`closed` parameter** — which side (left/right) of an interval is included in aggregation. prereqs: resample.
- **`label` parameter** — how the output bucket is labeled (left vs right edge). prereqs: resample.
### LESSON: Shooting Star Notebook
- **Shooting star candlestick** — formed during an uptrend; signals a possible reversal to bearish. prereqs: candlestick.
- **`ta.CDLSHOOTINGSTAR(open, high, low, close)`** — TA-Lib returns `−100` for a shooting star, otherwise `0`. prereqs: talib.
- **Short entry for shooting star** — enter short on the next candle when the previous candle is a shooting star and an uptrend exists. prereqs: shooting star pattern.
- **Shooting star stop-loss** — set at the High of the shooting star candle. prereqs: risk exits.
- **Shooting star take-profit** — target at entry − (SL − entry), the rr-scaled short target. prereqs: shooting star stop-loss.
- **`backtesting(data, 'short', rr=1)`** — backtest the shooting star short strategy. prereqs: backtesting.
---
## MODULE: Capstone Project
### LESSON: Capstone Project Model Solution
- **Candlestick capstone** — build and backtest a candlestick-pattern strategy on multiple assets. prereqs: all modules.
- **Multi-asset price data** — daily OHLC data for two tickers (AAPL, TSLA) read from CSV. prereqs: read_csv.
- **Pattern identification** — detect marubozu and shooting star patterns with TA-Lib in one function. prereqs: talib.
- **Entry type conversion** — map 'Buy'/'Sell' labels to numeric +1/−1 positions for signal computation. prereqs: signals.
- **Strategy returns** — `trade_signal.shift(1) × Close.pct_change()`, cumulative-plotted. prereqs: strategy returns.
- **Portfolio returns** — combine each asset's strategy returns; equal-weight average; plot cumulative. prereqs: cumulative returns.