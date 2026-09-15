# Strategy 001D — Formal Trading Strategy Specification

**Status:** 🟡 Candidate strategy — implementation and realistic backtest pending

## Purpose

001D converts the frozen 001C continuation hypothesis into an executable trading rule. The specification is frozen before the first full strategy backtest so that entry, exit, overlap, and data-use conventions cannot be changed after seeing strategy performance.

The original symmetric mean-reversion hypothesis remains rejected. The candidate strategy is the one-sided continuation rule identified through 001A–001C.

## Strategy hypothesis

When GOLDBEES closes at least 2.0 standard deviations above the mean of the previous 30 completed intraday closes, while the prior six-bar return is positive, the next approximately 30 minutes should have positive continuation relative to an appropriate historical benchmark.

001C provided a promising point-in-time attribution result. It did **not** establish that the relationship is profitable after execution costs, robust out of sample, or suitable for live trading.

## Frozen signal definition

For bar `t`:

1. Use only the previous 30 completed closes from the same trading session.
2. Calculate the sample standard deviation over those 30 closes.
3. Calculate `z_t = (close_t - mean(previous_30_closes)) / std(previous_30_closes)`.
4. Require `z_t >= +2.0`.
5. Require `prior_return_6bar = close[t-1] / close[t-7] - 1 > 0`.
6. All signal inputs must be available at the close of bar `t`.
7. No overnight bars may enter feature construction.

No alternative thresholds are part of the baseline strategy.

## Frozen execution rule

- Signal timestamp: close of bar `t`.
- Entry: **open of bar `t+1`**.
- Direction: long only.
- Exit: **close of bar `t+6`**.
- Intended holding period: six 5-minute bars / approximately 30 minutes.
- Same-bar entry is prohibited.
- If the required next-bar open or exit close is unavailable, no trade is generated.
- A trade may not cross a trading-session boundary.

The realized gross trade return is:

`gross_return = exit_price / entry_price - 1`

## Overlap and signal handling

- Use a **12-bar cooldown** after a selected entry event.
- Signals inside the cooldown are ignored.
- Only one Strategy 001 position may be open at a time.
- The cooldown is inherited from the research dependence control in 001A/001C and is not a parameter to optimize in this stage.

## Position sizing

The first backtest reports normalized per-trade returns and a constant-notional portfolio representation. No leverage, pyramiding, volatility targeting, Kelly sizing, or ML-based sizing is permitted in the baseline.

Account-level sizing for the eventual ₹30,000 validation account is a later feasibility exercise and must not be used to improve historical performance.

## Cost and slippage treatment

The engine must report:

- gross return;
- explicit transaction-cost deduction;
- explicit entry/exit slippage deduction;
- net return;
- cost sensitivity.

Because exact realized spread/slippage is not available from OHLCV alone, the initial backtest will use transparent scenario assumptions rather than pretend that historical OHLCV identifies the true execution cost. Baseline and stress scenarios must be reported separately and never hidden inside the gross result.

The cost model is deliberately isolated in the backtesting layer so assumptions can be audited and changed only in a later, explicitly recorded experiment.

## Portfolio accounting

For the normalized baseline:

- starting equity = 1.0;
- each completed trade changes equity by its net trade return;
- no compounding through leverage is assumed;
- no simultaneous positions;
- cash is otherwise idle.

The report must also provide a trade-level table so that portfolio metrics can be reproduced from individual trades.

## Required outputs

### Trade-level

- signal timestamp
- entry timestamp / price
- exit timestamp / price
- z-score
- prior six-bar return
- gross return
- transaction cost
- slippage
- net return
- cumulative equity
- drawdown

### Portfolio-level

- number of trades
- total net return
- annualized return where meaningful
- annualized volatility
- Sharpe ratio
- maximum drawdown
- win rate
- average win / average loss
- profit factor
- turnover proxy
- average holding time
- exposure

Annualized statistics must clearly state the convention used and should not be presented when the sample is too short for a meaningful interpretation.

## Data integrity rules

- Chronological data only.
- Features must use completed information available at signal time.
- Entry must occur no earlier than the next bar open.
- Exit must use a price that was not known at signal time.
- No future observations may affect signal construction, trade eligibility, position sizing, or costs.
- Session boundaries must be respected.
- Duplicate or non-monotonic timestamps invalidate the dataset.

## What is deliberately excluded

The baseline will not include:

- parameter optimization;
- stop-loss optimization;
- take-profit optimization;
- leverage optimization;
- instrument selection based on performance;
- machine-learning filtering;
- look-ahead data;
- same-bar execution;
- overnight positions;
- portfolio optimization;
- selection of the best cost scenario after seeing results.

These may become separate experiments only after the baseline has been recorded.

## Validation sequence after implementation

1. Verify trade construction with unit tests and hand-checkable examples.
2. Run the GOLDBEES baseline backtest.
3. Reconcile trade counts against the frozen event definition.
4. Inspect gross return distribution.
5. Apply transparent cost/slippage scenarios.
6. Analyze drawdown and turnover.
7. Run predefined robustness checks.
8. Perform chronological out-of-sample / walk-forward validation.
9. Only if the strategy remains robust, begin paper/shadow trading.
10. Live deployment requires a separate execution and risk approval gate.

## Promotion gates

- **CANDIDATE:** executable rule implemented; evidence still pending.
- **PROMISING:** positive and economically meaningful net performance with acceptable diagnostics, but OOS/paper validation remains.
- **ROBUST:** survives predefined robustness and chronological OOS tests.
- **PAPER READY:** robust and executable under realistic cost/slippage assumptions.
- **LIVE CANDIDATE:** paper/shadow evidence supports controlled deployment with explicit risk limits.

No performance threshold alone can promote the strategy. The decision must consider statistical evidence, execution realism, drawdown, turnover, stability, and data integrity.

## Research discipline

This document is frozen before the full trading backtest. If the strategy rule changes after observing results, the change receives a new experiment identifier and the original result remains in the journal.

## Next step

Implement and test the baseline backtester. Do not optimize the strategy before the first reproducible gross and net backtest has been recorded.
