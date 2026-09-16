# Strategy 001F — Results

**Status: pending local execution**

The 001F diagnostic implementation has been added, but results are intentionally not written until the analysis is executed against the repository's frozen Strategy 001D trade file.

## Required input

`data/reports/goldbees_strategy_001d_backtest/trades_gross.csv`

## Required outputs

- `winner_exclusion.csv`
- `time_of_day.csv`
- `holding_period.csv`
- feature-slice outputs when the frozen trade file contains the corresponding point-in-time feature columns

## Decision discipline

No parameter, threshold, holding period, feature filter, or execution rule will be selected from these same-sample diagnostics. The purpose is to understand the existing frozen strategy before the next robustness/OOS stage.

Results, interpretation, charts, and the promotion/rejection decision will be added after the user runs the experiment and the outputs are reviewed.
