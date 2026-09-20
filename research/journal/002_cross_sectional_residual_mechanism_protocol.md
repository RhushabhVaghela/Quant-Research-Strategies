# Strategy 002 — Leave-One-Out Residual Mechanism Protocol

**Status:** Exploratory pattern investigation. No trading hypothesis selected.

## Objective

Determine whether the observed short-horizon cross-sectional residual reversal survives a stricter residual construction and whether it is an actionable stock-specific effect rather than a bar-boundary artifact.

This is a characterization step, not strategy development.

## Locked sample

Use only:

- exploratory development: **2025-09-18 through 2026-06-09**;
- the same 19 structurally eligible instruments.

Do not read validation (**2026-06-10 through 2026-08-19**) or final holdout/OOS (**2026-08-20 through 2026-09-17**) for decision-relevant statistics.

## Method

For each timestamp and instrument:

1. Compute the instrument's return component.
2. Compute the equal-weight cross-sectional return using **all other eligible instruments only**.
3. Define the instrument residual as its return minus this leave-one-out cross-sectional return.

Perform the calculation separately for:

- close-to-close: prior close → current close;
- close-to-open: prior close → current open;
- open-to-close: current open → current close.

For the close-to-close residual, evaluate next-bar residual returns conditional on prior residual sign at horizons 1, 2, 3, 6 and 12 bars.

For the boundary decomposition, evaluate the next bar's close-to-open and open-to-close residual components conditional on the prior close-to-close residual sign.

Report:

- per-instrument observations;
- mean, median and positive fraction;
- cross-instrument breadth;
- sign × residual-magnitude quartiles;
- chronological stability;
- comparison of close-to-close versus boundary components.

## Controls

No z-score, lookback, entry threshold, exit threshold, holding-period optimization, stop, portfolio weighting, instrument selection, transaction-cost assumption, or P&L calculation is permitted.

The leave-one-out construction is fixed in advance. It must not be changed after inspecting which specification produces the most attractive result.

A minimum cross-sectional coverage rule must be explicit in the implementation: a timestamp is usable for an instrument only when the leave-one-out market contains at least **3 other eligible instruments**.

## Interpretation gates

Advance toward economic hypothesis definition only if:

1. the effect survives leave-one-out construction;
2. it is broad across instruments rather than dependent on a small subset;
3. it is present across chronological subperiods;
4. it is not explained primarily by close-to-open boundary adjustment;
5. the signal information is available before the return interval being evaluated;
6. the magnitude relationship is descriptive and not being reverse-engineered into a threshold.

If the effect disappears or remains primarily a boundary artifact, preserve that finding and continue pattern discovery.

## Reuse

This investigation reuses the repository's existing:

- time-series analysis conventions;
- cross-sectional universe and audit infrastructure;
- Strategy 001 cross-sectional research conventions;
- reversal mechanism decomposition methodology.

## Reproducible execution

Run:

    python scripts/run_strategy_002_leave_one_out_residual.py data/raw/strategy_002_universe --audit-report data/reports/strategy_002_universe_audit.csv --output-dir data/reports/strategy_002_leave_one_out_residual

No validation or holdout statistic may be introduced by this workflow.


## Execution status

The leave-one-out residual mechanism analysis has now been executed locally.

- Included instruments: **19**
- Excluded instruments: **1**
- Decision-relevant window: **2025-09-18 through 2026-06-09**
- Validation/holdout observations: not used
- Strategy P&L: not calculated
- Optimization: not performed

The generated CSV/JSON outputs must be committed and reviewed before interpreting the mechanism. This execution status records only that the predefined analysis ran successfully; it does not imply that the residual effect survived the stricter test.
