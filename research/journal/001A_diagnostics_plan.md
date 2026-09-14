# Strategy 001A — Event Structure & Conditioning Diagnostics

This experiment follows the rejected symmetric mean-reversion baseline. It does not optimize parameters or create a trading rule. It tests whether the observed event behavior survives dependence controls and whether it is concentrated in predefined market conditions.

Planned diagnostics:

1. Event clustering and a fixed 12-bar non-overlap filter.
2. Time of day.
3. Six-bar prior trend.
4. Prior 30-bar volatility regime.
5. Current volume relative to prior 30-bar median.
6. Absolute z-score severity.
7. Positive vs negative deviation continuation after non-overlapping events.

The fixed 12-bar cooldown equals the longest tested forward horizon and is a dependence diagnostic, not a tuned trading parameter.
