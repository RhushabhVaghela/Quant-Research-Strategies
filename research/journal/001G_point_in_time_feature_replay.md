# Strategy 001G — Point-in-Time Feature & Forward-Path Replay

## Purpose

001G reconstructs the frozen Strategy 001D trades directly from the validated GOLDBEES OHLCV dataset rather than relying only on the compact trade export.

The objective is to recover the complete point-in-time research state at each signal and the forward price path after entry. This addresses the main limitation identified in 001F: the frozen trade CSV does not contain all signal-time features or intermediate forward returns.

001G is a **replay and measurement experiment**. It does not change Strategy 001D and does not select a new threshold, holding period, filter, or execution rule.

## Research questions

1. Can every frozen 001D trade be reproduced from raw OHLCV using the same signal and execution rules?
2. What signal-time features were available without look-ahead?
3. How does return evolve after entry at fixed forward horizons?
4. How quickly does favorable movement occur, and how large is adverse movement before the intended exit?
5. Does the forward path provide evidence about execution sensitivity without changing the frozen strategy?
6. Can the missing 001F conditional slices be measured from the original point-in-time feature set?

## Frozen Strategy 001D rule

- 5-minute GOLDBEES bars
- previous 30 completed same-session closes
- sample standard deviation
- z-score >= +2.0
- prior six-bar return > 0
- long-only
- signal at event-bar close
- entry at next-bar open
- exit at close of bar t+6
- 12-bar cooldown
- no overnight feature construction
- one position at a time
- no leverage or optimized sizing

## Point-in-time feature set

At signal time, retain only information that was observable by the event-bar close:

- signal timestamp
- session date
- signal close
- prior 30-bar mean
- prior 30-bar standard deviation
- z-score
- prior six-bar return
- volume and prior-volume baseline / volume ratio where safely defined
- time-of-day bucket

All rolling features must be shifted before rolling and grouped by session where required. No future bar may enter a signal-time feature.

## Forward-path measurements

For each frozen trade, reconstruct returns from the executable next-bar-open entry price to available same-session closes at fixed horizons where bars exist:

- +5 minutes
- +10 minutes
- +15 minutes
- +20 minutes
- +25 minutes
- +30 minutes (primary frozen horizon)
- +45 minutes
- +60 minutes

Also calculate maximum favorable excursion (MFE), maximum adverse excursion (MAE), and the timestamp/elapsed minutes of each extreme when the data support it.

These are descriptive measurements. They must not be used to choose a new holding period from the same sample.

## Reconciliation requirement

The replay must compare its reconstructed frozen trades with the existing 001D `trades_gross.csv` using stable identifiers/timestamps and report discrepancies rather than silently altering the baseline.

Expected baseline properties include approximately 310 trades and the existing 001D entry/exit logic. Small floating-point differences may be tolerated; missing or extra trades require investigation.

## Execution interpretation

001G may compare the path after the frozen next-bar-open entry with delayed-entry prices only when the alternative is mechanically observable and pre-defined. No intrabar fill assumption should be presented as historical fact when OHLCV does not provide the required execution information.

The main purpose is to establish how much of the gross edge is already present shortly after entry and therefore how exposed the strategy is to spread, slippage, and latency.

## Decision discipline

001G is not an optimization stage. No result may be converted into a new production rule without assigning a new experiment identifier and reserving an untouched evaluation period.

The experiment can:

- validate the 001D replay and improve measurement quality;
- reveal that the gross edge is broad and develops before the intended exit;
- reveal that the edge is delayed or concentrated near exit;
- reveal adverse excursions that matter for execution/risk;
- identify data or implementation discrepancies requiring a research stop.

## Resources used

The broader repository research library informs this experiment: Quantra trade analytics and backtesting material for trade/path/MFE/MAE measurement; WQU Financial Data, Financial Markets, Statistics, Stochastic Modeling and later ML material for point-in-time feature design and statistical validation; Zerodha/KiteConnect resources for eventual execution realism; and the project's signal-discovery framework for hypothesis-first and leakage-control discipline.

Reference resources are methodological guidance, not copied or automatically validated alpha.

## Promotion boundary

001G does not authorize paper or live trading. After replay reconciliation and interpretation, the next gate remains predefined robustness and chronological out-of-sample/walk-forward validation.
