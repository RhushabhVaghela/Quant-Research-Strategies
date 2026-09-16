# Strategy 001E — Trade Distribution & Execution Audit

**Status:** 🟡 In progress

## Purpose

001E audits the first frozen Strategy 001D trading backtest **without changing the strategy rule**.

The objective is to determine whether the +15.85% gross result is broad and stable enough to justify further research, and how much execution friction the frozen signal can economically tolerate.

This is a diagnostic experiment, not an optimization experiment.

## Questions

### 1. Where does the gross edge come from?

Inspect the 310 completed trades using mean, median, quartiles, P10/P90, tails, minimum/maximum, winning/losing distributions, and concentration of cumulative profits in the largest trades.

### 2. What execution friction can the frozen rule tolerate?

Run a **predefined cost grid** rather than selecting a favorable scenario after seeing results. Vary transaction cost and slippage independently and jointly. Report mean net return, compounded net return, win rate, profit factor, maximum drawdown, and the approximate break-even friction region.

This is an economic diagnostic, not a claim about actual historical execution costs.

### 3. Is the result stable through time?

Use chronological, non-overlapping periods. At minimum inspect 2025 H1, 2025 H2, 2026 H1, and the remaining available 2026 sample. Report trade count, gross return, mean return, win rate, profit factor, and drawdown where meaningful.

### 4. How frequently does the strategy trade?

Measure trades per trading day, holding duration, days with trades, maximum trades per day, time-of-day distribution, and time between selected signals.

### 5. Are the portfolio metrics correctly defined?

The existing 001D engine reports a trade-level Sharpe-like statistic. That value must not be treated as the final annualized strategy Sharpe. 001E adds a time-indexed equity/return view and documents the annualization convention. If the observations do not support a meaningful annualized statistic, the report should say so rather than manufacture one.

## Frozen inputs

001E does **not** alter the 001D rule:

- 30-bar lookback;
- z-score threshold +2.0;
- positive prior six-bar return;
- six-bar holding period;
- next-bar-open entry;
- close-of-t+6 exit;
- 12-bar cooldown;
- long-only direction;
- session boundaries.

No stop-loss, take-profit, threshold search, holding-period search, sizing optimization, ML filter, or performance-based instrument selection is allowed.

## Resource integration

The audit deliberately uses the broader project library rather than a single course. Quantra backtesting and strategy material informs trade-level analytics, equity curves, drawdowns, Sharpe, transaction-cost and slippage analysis. Quantra strategy material provides later building blocks for intraday momentum, volume, order flow, volatility, and trade analytics. WQU Financial Data, Financial Economics, Financial Markets, Derivatives, Stochastic Modeling, Machine Learning, and Deep Learning material can inform later statistical validation, feature engineering, regime analysis, and model experiments where justified. Zerodha/KiteConnect resources inform eventual execution validation. The project's signal-discovery framework supplies the hypothesis-first, point-in-time, OOS, and research-discipline controls.

Reference material is used as methodology and building blocks. It is not treated as automatically validated alpha.

## Decision gates

**REJECTED:** the gross effect is unstable, economically trivial, or fails integrity checks.

**INCONCLUSIVE:** evidence is insufficient to determine whether the gross effect is genuine or economically usable.

**PROMISING:** the frozen rule remains economically/statistically interesting and stable enough to justify predefined robustness and OOS validation, while not yet being paper/live ready.

A positive gross result alone is insufficient for promotion.

## Next stage

If the frozen rule remains interesting after 001E, proceed to predefined robustness and chronological OOS/walk-forward validation. If it does not, record the failure. Any genuinely new strategy hypothesis receives a new experiment identifier; the original 001D result remains preserved.
