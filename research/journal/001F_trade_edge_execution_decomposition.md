# Strategy 001F — Trade-Level Edge & Execution Decomposition

## Purpose

001F is a diagnostic experiment following the frozen Strategy 001D backtest and the 001E trade-distribution/execution audit.

The 001D strategy produced a positive gross result, but the average gross trade return is small relative to plausible execution friction and the top 10% of trades contribute a large share of positive profit. 001F therefore studies **where the gross edge comes from and how quickly it is realized**, without searching for profitable parameters.

## Research questions

1. Is gross performance dependent on a small number of extreme winners?
2. How does performance change after removing the largest 1%, 5%, and 10% winning trades?
3. Does signal strength contain descriptive information about subsequent return?
4. How does trade performance vary by time of day, prior trend, volatility, and volume regime using only information available at signal time?
5. How does return accumulate across the intended 5m, 15m, 30m, and 60m horizons where available?
6. How sensitive is performance to entry timing, using execution definitions that do not introduce look-ahead?
7. Is the observed edge broad enough to justify further robustness/OOS testing?

## Frozen baseline

001F does not change the 001D strategy definition:

- GOLDBEES 5-minute bars
- 30 completed-bar lookback
- z-score threshold `>= +2.0`
- prior six-bar return `> 0`
- 30-minute primary holding horizon
- signal decided at event-bar close
- entry at next-bar open
- exit at close of bar `t+6`
- 12-bar session cooldown
- no overnight feature construction
- no parameter optimization

## Planned diagnostics

### A. Winner concentration

Report gross performance after excluding the largest positive trades by rank:

- no exclusion
- top 1% winners removed
- top 5% winners removed
- top 10% winners removed

The purpose is diagnostic only. These exclusions must not be used to select a better strategy.

### B. Signal-strength buckets

Describe outcomes by the frozen event z-score severity using bins defined before inspecting results. Do not search for an optimal threshold.

### C. Conditional feature slices

Use only point-in-time features already available to the frozen signal:

- time of day
- prior six-bar return/trend
- prior 30-bar volatility
- volume ratio where available
- event z-score/severity

Use fixed, predeclared buckets. Results are descriptive and are not parameter-selection evidence.

### D. Holding-period decomposition

Where the trade dataset contains or can safely reconstruct intermediate forward returns, report return at 5m, 15m, 30m, and 60m. The 30m result remains the frozen primary horizon.

### E. Entry-timing sensitivity

Compare the frozen next-bar-open execution with clearly defined delayed alternatives only if they can be computed without look-ahead. Do not introduce a price that would not have been observable/executable at the stated decision time.

### F. Tail dependence

Report contribution of the largest positive and negative trades, return skewness, and distribution quantiles. Distinguish positive skew from strategy robustness.

## Decision rule

001F does not promote the strategy to paper trading.

A positive result means only that the current gross edge has a sufficiently understandable structure to justify the next robustness/OOS experiment. A negative result can justify rejecting the current architecture or redesigning the hypothesis.

No threshold, holding period, feature filter, or execution rule may be selected from 001F results and then evaluated on the same sample as if it were out-of-sample evidence.

## Relationship to prior experiments

- 001A rejected the original mean-reversion interpretation and identified directional continuation.
- 001B found a descriptive incremental continuation effect versus matched non-event observations.
- 001C strengthened that result using a point-in-time benchmark.
- 001D converted the frozen hypothesis into actual trades and found positive gross performance but strong cost sensitivity.
- 001E showed positive median gross returns, a 4.77 bps mean gross trade return, and 53.7% of positive profit contributed by the top 10% of trades.
- 001F investigates that concentration and the execution/timing structure before any optimization or OOS promotion.
