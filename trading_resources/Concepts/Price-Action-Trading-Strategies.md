# Price Action Trading Strategies Using Python — Concept Inventory
Course goal: detect and backtest price-action chart patterns (head and shoulders, inverse head and shoulders, double/triple tops & bottoms, support/resistance), pivot-point systems (traditional, Woodie's, Camarilla) and Fibonacci retracements — with entry/exit risk management, backtesting, trade-level analytics, performance metrics, and transaction-cost/slippage accounting.
## Enumerated Notebooks (24) + Module (1)
| # | Module folder | Notebook |
|---|---|---|
| 1 | Detecting Head and Shoulders Pattern | Identify Local Minima and Maxima |
| 2 | Detecting Head and Shoulders Pattern | Detecting Head and Shoulders |
| 3 | Backtesting Head and Shoulders Pattern | Head and Shoulders: Entry and Exits |
| 4 | Backtesting Head and Shoulders Pattern | Backtesting Head and Shoulders Pattern |
| 5 | Inverse Head and Shoulders Pattern | Detect the Inverse Head and Shoulders Pattern |
| 6 | Inverse Head and Shoulders Pattern | Backtest the Inverse Head and Shoulders Pattern |
| 7 | Double Top Pattern | Detect the Double Top Pattern |
| 8 | Double-Bottom Pattern | Detect the Double Bottom Pattern |
| 9 | Triple and n-Top Patterns | Detect the Triple Top Pattern |
| 10 | Triple-Bottom Pattern | Detect the Triple Bottom Pattern |
| 11 | Strategy Using Support and Resistance | Detecting Support and Resistance Levels |
| 12 | Strategy Using Support and Resistance | Backtesting Support Level |
| 13 | Pivot Points | Compute and Visualise Pivot Points |
| 14 | Types of Pivot Points | Visualise Woodie's Pivots |
| 15 | Types of Pivot Points | Visualise Camarilla Pivots |
| 16 | Woodie's Trend Trading | Woodie's Trend Based Strategy |
| 17 | Woodie's Range Trading | Woodie's Range Trading Strategy |
| 18 | Camarilla Trend Trading | Camarilla Trend Based Strategy |
| 19 | Fibonacci Ratios | Calculation of Fibonacci Ratios |
| 20 | Fibonacci Retracement Strategy | Fibonacci Retracement Strategy |
| 21 | Performance Analysis | Trade Level Analytics |
| 22 | Performance Analysis | Performance Metrics |
| 23 | Transaction Costs and Slippage | Implementation of Transaction Cost and Slippage |
| 24 | Capstone Project | Capstone Project Solution |
Recurring module functions (used across most strategy notebooks)
- **`get_min_max(data, argrel_window)`** — local minima/maxima detection (via scipy `argrelextrema`).
- **`backtester(data)` / `intraday_backtester(data, intraday_exit)`** — produce a `round_trips_details` trade log (entry/exit dates & prices, position, `exit_type`, PnL).
- **`trade_level_analytics(trades)`** — win%, avg PnL, holding period, profit factor.
- **`get_performance_metrics(data, col_names)`** — CAGR, Sharpe, annualised vol, max drawdown, equity curve.
---
## 1. Identify Local Minima and Maxima
**Concepts:**
- Detecting local minima/maxima is the foundational first step for any chart-pattern detection.
- **scipy `argrelextrema`** to find swing lows/highs: pass the `Low` series with `np.less` comparator, or the `High` series with `np.greater`; `order=argrel_window` sets the comparison window.
- Mapping integer indices back to dates/prices.
- Candlestick visualisation with `mplfinance` (`plot`, `style` param).
- Build reusable `get_min_max()` function in the shared module.
**Prereqs:** pandas; numpy; min/max reasoning on a series; plotting.
## 2. Detecting Head and Shoulders
**Concepts:**
- A **head and shoulders (HS)** pattern = 5 sequential local extremes: shoulders A, E (maxima), head C (maxima above both), neckline points B, D (minima).
- Define pattern-detection conditions: A, C, E ∈ maxima; B, D ∈ minima; C above A & E; A & E above B & D; shoulders within 1.5% of their mean (tolerance).
- Build an **HS scanner** over consecutive sequences of 5 min/max points; reports indices of valid patterns.
- **Store pattern details** (dates/prices of head, shoulders, neckline) for later analysis.
- Visualise detected patterns with `mplfinance`.
**Prereqs:** notebook 1; structural reasoning about chart shapes.
## 3. Head and Shoulders: Entry and Exits
**Concepts:**
- HS pattern is completed only after the right shoulder breaks **below the neckline** — the confirmation event.
- Filter patterns to avoid look-ahead bias: `time_for_confirmation > 5 bars` (pattern fully formed) **and** within 30 bars (not overextended).
- Visualise the breakdown candle with `mplfinance`.
- **Risk management / exit levels** for short entry: stop-loss just above the second shoulder; target at a multiple of (head − neck2) below entry.
- Plot confirmation point, stop-loss (red) and target (green) levels.
**Prereqs:** notebook 2; understanding of look-ahead bias; risk-level thinking.
## 4. Backtesting Head and Shoulders
**Concepts:**
- Merge price data (`spy_daily_1993_2018.csv`) with stored pattern details into one strategy DataFrame.
- **Backtester** logic: initial settings (capital, position sizing, entry/exit flags); positions check; entry-position update when `entry_flag=True`; exit-position update when `exit_flag=True`.
- Record trade log (`round_trips_details`) with entry/exit dates & prices, position, exit-type (stop/target/time), and PnL.
- Interpreting a **trade log** print.
**Prereqs:** notebooks 2–3; event-driven loop reasoning; merges.
## 5. Detect the Inverse Head and Shoulders (IHS)
**Concepts:**
- IHS is the mirror of HS: 5 sequential points with A, C, E ∈ minima (troughs), B, D ∈ maxima (neckline), head C below the neckline, shoulders above it, shoulders within 1.5% of their mean.
- **IHS scanner** analogous to the HS scanner with mirrored conditions.
- Store pattern details; find the long-entry confirmation date.
- Filter for validity (confirmation > 5 bars, within 30 bars).
- **Risk management** for long entry: stop-loss 1% below the right shoulder; target at `head_length` above entry.
**Prereqs:** notebook 2 (HS detection pattern); notebook 3 (risk levels).
## 6. Backtest the Inverse Head and Shoulders
**Concepts:**
- Merge `apple_daily_1980_2022.csv` with `ihs_pattern_details.csv`; generate a `signal` column.
- Generate a trade sheet with `backtester()`.
- **Trade-level analytics** via `trade_level_analytics()` (win count, **profit factor ≈ 2.7** = excellent).
- **Strategy performance** via `get_performance_metrics()` (CAGR, Sharpe, max drawdown); forward-fill `signal` across entry→exit range.
**Prereqs:** notebooks 4–5; backtesting & analytics functions.
## 7. Detect the Double Top Pattern
**Concepts:**
- **Double top** = 3 sequential points: A, C ∈ maxima (two tops), B ∈ minima (neckline); A & C above B; tops within 1.5% tolerance.
- **Double top scanner** (similar pattern to HS/IHS scanners with the stated conditions).
- Store pattern details; find short-entry confirmation date; filter validity (5-bar look-ahead guard, within 30 bars).
- **Trade**: confirmation of breakdown below neckline → short the second top.
- **Risk management**: stop-loss 1% above the second top; target at `top_length` below short entry.
**Prereqs:** notebook 1; notebook 3 (risk) and 5 (scanner pattern-conditions).
## 8. Detect the Double Bottom Pattern
**Concepts:**
- **Double bottom** mirror of double top: A, C ∈ minima (two bottoms), B ∈ maxima (neckline); A & C below B; bottoms within 1.5% tolerance.
- **Double bottom scanner** with conditions inverted from double top.
- Store details; find long-entry confirmation date; validity filters.
- **Risk management**: stop-loss 1% below the second bottom; target at `bottom_length` above long entry.
**Prereqs:** notebooks 1 and 7 (mirror logic).
## 9. Detect the Triple Top Pattern
**Concepts:**
- **Triple top** = 5 sequential points: A, C, E ∈ maxima (three tops) above neckline points B, D ∈ minima; first two tops within 1.5% tolerance (rule from Advanced Trading Rules).
- **Triple top scanner** (analogous to other scanners).
- Store pattern details; short entry confirmation; validity filters.
- **Risk management**: stop-loss 1% above the third top; target at `top_length` below short entry.
**Prereqs:** notebook 7 (double top); scanner-condition pattern logic.
## 10. Detect the Triple Bottom Pattern
**Concepts:**
- **Triple bottom** mirror of triple top: A, C, E ∈ minima below B, D ∈ maxima (neckline); first two bottoms within 1.5% tolerance.
- **Triple bottom scanner**; store details; long entry confirmation; validity filters.
- **Risk management**: stop-loss 1% below the third bottom; target at `bottom_length` above long entry.
**Prereqs:** notebook 9 (mirror, like double-bottom from double-top).
## 11. Detecting Support and Resistance Levels
**Concepts:**
- Support = level from which price has bounced at least once; resistance = level capped by price.
- Resample minute data to daily (`resample`), use a `90-day` lookback window.
- Identify levels via `get_min_max()` from the shared module (minima= support, maxima = resistance).
- **Nearest support/resistance**: a level is support if `ltp` > support and vice versa; pick the most recent for higher re-test probability.
- Build `get_support(price_data, argrel_window=15)` and `get_resistance(...)` helpers.
**Prereqs:** notebooks 1 (min/max) and 4 (resampling); level-trading intuition.
## 12. Backtesting Support Level
**Concepts:**
- Multi-timeframe strategy: find daily support, trade on 15-minute closes.
- Map daily support into the 15-min merged DataFrame; merge daily + 15-min frames.
- **Entry**: go long at current Close when previous Close dropped below the support level with no open position.
- **Exit**: stop-loss 10% below and take-profit 15% above entry Close.
- Backtest (long at next candle close), then apply `trade_level_analytics()` and `get_performance_metrics()`.
**Prereqs:** notebooks 11 and 4; multi-timeframe merge; risk levels.
## 13. Compute and Visualise Pivot Points
**Concepts:**
- **Pivot point (P)** = (High + Low + Close)/3 of the preceding day; better reference than prior close (captures range).
- Support/resistance formula set for traditional pivots (R1..R3, S1..S3 from P and (High−Low) range).
- `shift(1)` to compute on preceding candle's OHLC.
- Resample minute→daily to compute daily pivots, visualise over a recent minute window as horizontal lines.
**Prereqs:** OHLCV candle semantics; resampling; plotting.
## 14. Visualise Woodie's Pivots
**Concepts:**
- **Woodie's pivots** suit longer (positional) timeframes; computed on weekly data.
- **W-Pivot WP = (High + Low + 2×Close)/4** (weekly).
- Support/resistance formulas (R1..R3, S1..S3) based on WP and weekly range.
- Resample minute→daily + weekly; visualise levels over daily close series.
**Prereqs:** notebook 13 (pivot formula concept); resampling.
## 15. Visualise Camarilla Pivots
**Concepts:**
- **Camarilla pivots** yield 6 support + 6 resistance levels, closer together (especially S1–S3 / H1–H3); best on shorter timeframes.
- Pivot P = (High+Low+Close)/3 computed on daily data.
- Resistance H1..H6 & support L1..L6 formulas driven by `Range = High − Low` (e.g., H1 = Close + Range×(1.1/12), H3, H4; H5=Close×(High/Low), H6 derived; matching L-side levels).
- Visualise levels over minute closes.
**Prereqs:** notebook 13 (traditional pivots); understanding of ranges.
## 16. Woodie's Trend Based Strategy
**Concepts:**
- **Trend (breakout)** regime signal on weekly Woodie's: `Day's Open > Week's R2` and `Day's Open < Week's R3`.
- **Entry** on 15-min close above **R3**; final signal = trend_signal AND entry_signal.
- Multi-frequency workflow: resample minute→weekly/daily/15-min, compute weekly Woodie's, freeze levels for the week, merge.
- **Risk management**: stop-loss at R2; target set at a distance relative to (R3−R2) above R3 (tuned to avoid negative PnL).
- Backtest with `backtester()`; analytics + performance metrics (CAGR, Sharpe, max drawdown); parameter sensitivity (target distance change flips PnL).
**Prereqs:** notebooks 14; 4 (backtest) and 21 (analytics).
## 17. Woodie's Range Trading Strategy
**Concepts:**
- **Range** regime signal on weekly Woodie's: `Day's Open < Week's R2` and `Day's Open > Week's S2`.
- **Entry** on 15-min close **below S2**; final signal = range_signal AND entry_signal.
- Multi-frequency merge (weekly pivots → daily/15-min), freeze weekly pivot levels for the week.
- **Risk management**: stop-loss at average of S2 & S3; target = W-Pivot level.
- Backtest; trade-level analytics; strategy performance.
**Prereqs:** notebook 16 (workflow mirror, inverted regime) + 14.
## 18. Camarilla Trend Based Strategy
**Concepts:**
- **Camarilla trend (breakout)** conditions from daily Camarilla levels: `Day's Open < H3` and `Day's Open > H4`.
- **Entry** on 5-min close **above H4**; final = trend_signal AND entry_signal.
- Higher trade frequency than Woodie's (frequent, closely-spaced Camarilla levels → more trades).
- **Risk management** (long): stop-loss at H3, target at H6.
- Backtest with `intraday_backtester()`; forward-fill for equity curve; `trade_level_analytics()` + `get_performance_metrics()` (e.g., 394 trades, profit factor 1.58; CAGR 3.95%, Sharpe 0.31, MDD −14.98%).
**Prereqs:** notebooks 15 and 16/17 (regime+entry pattern), 4/21 (backtest/analytics).
## 19. Calculation of Fibonacci Ratios
**Concepts:**
- Fibonacci retracement ratios: 23.6%, 38.2%, 50%, 61.8%, 78.6% of the price range (Max − Min).
- Identify max/min price from the `High`/`Low` (candlestick) or `Close` (line) series.
- Plot the price series with the Fibonacci ratio lines; observe price reacting near levels (e.g., reversal at 50%).
**Prereqs:** price-range arithmetic; plotting.
## 20. Fibonacci Retracement Strategy
**Concepts:**
- Two-timeframe design: monthly (or daily) to compute Fibonacci levels; 30-min (intraday) for entry timing.
- Preconditions for a tradable segment: price in **uptrend** and max price > min price + 25% (strong trend).
- Compute per-year Fibonacci ratios (rolling min/max).
- **Buy zone** = Close between 38.6% and 50% level; **SMA signal** = 21-period SMA above the 50% level; buy when both hold.
- **Exit/sell** when conditions break; **stop-loss** at 61.8% level; **take-profit** at 23% level.
- Drop unused OHLC columns, rename `Close` to distinguish monthly vs 30-min, merge dataframes.
- Filter to valid uptrend periods; backtest with `backtester()`; `trade_level_analytics()` + `get_performance_metrics()` (win% > loss%, positive profit factor; CAGR, Sharpe, max drawdown).
**Prereqs:** notebook 19; multi-timeframe resample/merge; backtest & analytics functions.
## 21. Trade Level Analytics
**Concepts:**
- Metrics evaluating a strategy **per trade** (beyond aggregate PnL).
- **Profit & Loss** (sum of trade gains/losses).
- **Win Percentage / Win Rate** = winning trades / total × 100 (a <50% win rate can still be profitable if winners >> losers).
- **Average PnL per trade** (average profit per winning trade vs average loss per losing trade).
- **Average Trade Duration / holding period** (exit − entry) and its capital/turnover implications.
- **Profit Factor** = win% × avg-win / (lose% × avg-loss); grading scale (<1 unprofitable, ~1 breakeven, 1.1–1.4 average, 1.4–2 decent, ≥2 excellent).
- Wrap into reusable `trade_level_analytics()`.
**Prereqs:** trading results data; ratio arithmetic.
## 22. Performance Metrics
**Concepts:**
- Metrics evaluating strategy performance **within trades** (entry→exit).
- **Equity curve** (cumulative strategy returns) for profit trajectory & visibility of drawdowns.
- **CAGR** (Compound Annual Growth Rate) = ((EV/BV)^(1/n) − 1)×100.
- **Annualised Volatility** = std(strategy_returns) × √(252 × candles/day).
- **Sharpe Ratio** = (mean return − risk-free) / volatility; higher preferred (Sharpe > 1 preferable).
- **Maximum Drawdown** = (peak − trough)/peak; lower magnitude preferred.
- Histogram of returns (distribution).
- Wrap into reusable `get_performance_metrics()`.
**Prereqs:** cumulative-returns; standard deviation; CAGR formula.
## 23. Implementation of Transaction Cost and Slippage
**Concepts:**
- Account for **brokerage/commission + taxes** before going live (e.g., 0.03% + 0.02% of traded value; broker-dependent).
- **Slippage modelling** = difference between expected and executed price; estimate from minute data using last-5-minute candles per day (`groupby("date")`, high end-of-day liquidity).
- Buy slippage = worst execution price (High) − last traded (Close); sell slippage = last traded (Close) − worst execution (Low); express as % of close; use a conservative max.
- Adjust strategy returns: detect position change (`signal.diff`) and deduct `change × total cost` from daily returns.
- Compare gross vs net (post-cost) cumulative returns (e.g., 1.126× → 1.004×), and total PnL vs total cost to judge viability.
**Prereqs:** notebooks 21–22; position change/turnover reasoning.
## 24. Capstone Project Solution
**Concepts:**
- End-to-end integration of the pattern-detection and analytics toolkit on `spy_daily_1993_2018.csv`.
- Sections: Min–Max (locate extremes) → Head and Shoulders → Inverse Head and Shoulders → **Box Plot** (visualising trade/return distributions).
- Consolidates `get_min_max`, scanners, backtester, and analytics into a single analysis.
**Prereqs:** every preceding notebook, particularly 1–2, 5, 21–22.
---
## Price-Action-Trading-Strategies — Section-based course structure (full lesson-by-lesson view)
# Concept Inventory — Price Action Trading Strategies Using Python
## COURSE: Price Action Trading Strategies Using Python
### Section: Section 1 - Introduction
- **Introduction:** course overview. prereqs: none.
- **Course structure:** pattern identification (reversal/continuation) → support/resistance → pivots → Fibonacci → backtesting. prereqs: none.
### Section: Section 2 - Basics of Price Action Trading
- **Price action trading:** studying basic price behaviour across time to make trading decisions without relying solely on lagging indicators. prereqs: none.
- **Benefits & drawbacks of price action trading:** clean signals, widespread timeframe applicability; but noise on short timeframes. prereqs: price action.
- **Asset & dataset applicability (FAQs):** concepts apply to any listed stock; minute-level data resampled to 15-min/hourly/daily. prereqs: price action.
### Section: Section 3 - Supply and Demand Analysis
- **Supply and demand analysis:** supply zone (sellers dominant) and demand zone (buyers dominant); price reverses after entering the zone. prereqs: price action.
- **Supply/demand zones & patterns:** zones defined by price patterns (Rally-Base-Rally, Drop-Base-Drop); Wykoff market phases. prereqs: supply & demand analysis.
### Section: Section 4 - Head and Shoulders Pattern
- **Head and shoulders pattern:** bearish reversal pattern (two shoulders + higher head + neckline); forms at the end of an uptrend. prereqs: price action basics.
- **Trading head and shoulders pattern:** entry on neckline break; targets and stop placement. prereqs: head & shoulders.
### Section: Section 5 - FAQs on Head and Shoulders Pattern
- **Variations in shoulders:** asymmetric/unequal shoulder variants tolerated. prereqs: head & shoulders.
- **Timeframe reliability:** patterns more reliable on longer timeframes; noise increases false signals short-term. prereqs: head & shoulders.
### Section: Section 6 - Detecting Head and Shoulders Pattern
- **Local minima and maxima:** programmatic detection of extremes within a window (shoulders/head at maxima, neck at minima); used to find swing points. prereqs: head & shoulders; Python.
### Section: Section 8 - Performance Analysis
- **Performance analysis:** backtested pattern trades with trade metrics (profit factor, win rate). prereqs: backtesting basics.
- **APPT & 17 trading metrics:** deeper per-trade analytics beyond P/L ratio. prereqs: performance analysis.
### Section: Section 9 - Transaction Costs and Slippage
- **Transaction costs & slippage:** costs eroding pattern-strategy returns; slippage splits into spread, market impact, volatility costs; minimising slippage. prereqs: performance analysis.
### Section: Section 10 - Inverse Head and Shoulders Pattern
- **Inverse head and shoulders pattern:** bullish reversal mirror of head & shoulders (forms at end of downtrend). prereqs: head & shoulders.
### Section: Section 11 - Double Top Pattern
- **Double top pattern:** bearish reversal forming two near-equal tops ("M") at end of an uptrend. prereqs: price action.
### Section: Section 12 - Double-Bottom Pattern
- **Double-bottom pattern:** bullish reversal, two lows near a support level ("W"); neckline between the two lows; confirms support. prereqs: double top.
### Section: Section 13 - Triple and n-Top Pattern
- **Triple and n-Top pattern:** bearish reversal after three (or n) near-equal tops; failure to make a higher high due to buyer/seller imbalance. prereqs: double top.
- **Reversal patterns additional reading:** harmonic patterns, triple-top trading, candlestick reversals. prereqs: reversal patterns.
### Section: Section 14 - Triple-Bottom Pattern
- **Triple-bottom pattern:** bullish reversal, three lows at a strong support zone, seller exhaustion; neckline at the highest interim point. prereqs: double-bottom; triple-top.
### Section: Section 15 - Continuation Patterns
- **Continuation patterns:** patterns that suggest the existing trend will resume (triangles, rectangles, flags, pennants). prereqs: price action.
- **Cup and handle (continuation):** bullish continuation pattern with buy targets. prereqs: continuation patterns.
### Section: Section 16 - Triangle Pattern
- **Triangle pattern:** consolidation/pennant-like continuation pattern formed by converging trendlines. prereqs: continuation patterns.
### Section: Section 17 - Flag Pattern
- **Flag pattern:** short-term consolidation after a sharp move, flagpole + flag; continuation signal. prereqs: continuation patterns.
### Section: Section 18 - Pennant Pattern
- **Pennant pattern:** small symmetrical triangle at the end of a flagpole; continuation signal. prereqs: continuation patterns.
### Section: Section 19 - Support and Resistance
- **Support and resistance:** price levels where buying (support) or selling (resistance) pressure reverses the move. prereqs: price action.
### Section: Section 20 - Strategy Using Support and Resistance
- **Strategy using support and resistance in action:** backtested support/resistance break-and-retest strategy logic. prereqs: support & resistance; backtesting.
### Section: Section 23 - Pivot Points
- **Pivot points:** derived levels from prior-period high/low/close used as intraday support/resistance references. prereqs: support & resistance.
- **Effectiveness of pivot-point strategies:** tested accuracy vs traditional & modified criteria. prereqs: pivot points.
### Section: Section 24 - Types of Pivot Points
- **Types of pivot points:** Standard, Fibonacci, Camarilla and Woodie's pivots (different formulas). prereqs: pivot points.
### Section: Section 25 - Woodie's Range Trading
- **Range trading using Woodie's pivots:** buying at Woodie support, selling at resistance s (mean-reversion around pivot). prereqs: Woodie pivots; range trading.
### Section: Section 26 - Woodie's Trend Trading
- **Woodie's trend trading:** trend-following uses of Woodie's pivots (breakout of pivot levels). prereqs: Woodie pivots; trend following.
### Section: Section 27 - Camarilla Trend Trading
- **Trend-based strategy using Camarilla pivots:** intraday support/resistance around Camarilla levels for trend entries. prereqs: Camarilla pivots; trend.
### Section: Section 28 - Fibonacci Ratios
- **Fibonacci ratios:** 23.6%, 38.2%, 50%, 61.8% retracement/extension levels. prereqs: none.
- **Fibonacci retracement & extension applications; limitations.** prereqs: Fibonacci ratios.
### Section: Section 29 - Fibonacci in Action
- **Fibonacci in action:** plotting retracement/extension levels on price data and their use. prereqs: Fibonacci ratios.
### Section: Section 30 - Fibonacci Retracement Strategy
- **Fibonacci retracement strategy:** entry at retracement support within an uptrend. prereqs: Fibonacci ratios.
- **FAQs on Fibonacci strategy:** placement, targets, validity. prereqs: Fibonacci strategy.
### Section: Section 31 - Short-Selling with Fibonacci Retracements
- **Short selling with Fibonacci:** short entry at a retracement resistance in a downtrend. prereqs: Fibonacci strategy; short selling basics.
### Section: Section 32 - Capstone Project
- **Capstone project:** backtest head & shoulders and inverse head & shoulders on SPY daily (2010–2022); pattern recognition functions; returns box plot. prereqs: all sections.
### Section: Section 34 - Summary
- **Summary of the course:** recap of supply/demand zones, reversal & continuation patterns, support/resistance, pivots, Fibonacci; next steps. prereqs: all sections.
## Course Prerequisite Map
- Foundations: *Price Action Basics → Supply & Demand.*
- Reversal patterns: *Supply/Demand + Support → Head & Shoulders → Inverse H&S; Double Top → Double Bottom → Triple/n-Top → Triple Bottom.* (Each pattern builds on prior reversal concepts.)
- Reversal-pattern detection: *Local Minima/Maxima (Python) → programmatic pattern detection.*
- Continuation patterns: *Continuation concepts → Triangle → Flag → Pennant.*
- Levels tools: *Support/Resistance → Strategy; → Pivot Points → Types (Woodie, Camarilla) → Range/Trend strategies; → Fibonacci Ratios → Retracement Strategy → Short-selling variant.*
- Backtesting/analytics: *Backtesting + Transaction Costs → Performance Analysis.* (Applies to all strategies.)
- Course flow: **Intro → Price Action Basics → Supply/Demand → H&S (+FAQs, Detection) → Inverse H&S → Double/Triple patterns → Continuation (Triangle/Flag/Pennant) → Support/Resistance → Strategy → Pivots (Types/Woodie/Camarilla) → Fibonacci (Ratios/Action/Retracement/Short) → Capstone → Summary.**
- FunPath basics feeding this course: Python for trading, pandas, local extrema (scipy argrelmax), basic backtesting and trade metrics.