# Strategy 001G — Point-in-Time Feature & Forward-Path Replay — Results

## Status

**Implementation added; empirical run pending local execution.**

This journal entry is intentionally separated from the specification. No 001G numerical result is recorded until the replay is run against the validated GOLDBEES dataset and reconciled against the frozen 001D trade export.

## Implementation delivered

001G now provides:

- raw GOLDBEES OHLCV loading with Asia/Kolkata timestamp normalization;
- exact reuse of the frozen 001D signal/execution implementation;
- signal-time feature retention for prior 30-bar mean/std, z-score, prior six-bar return, volume baseline/ratio, and time-of-day;
- session-local, shifted rolling features to prevent overnight and look-ahead leakage;
- forward close returns at 5/10/15/20/25/30/45/60 minutes from the signal timestamp, always measured from the executable next-bar-open entry price;
- MFE/MAE from next-open entry through the frozen exit;
- reconciliation against `trades_gross.csv` using signal timestamps and gross returns;
- reproducible summary CSVs and diagnostic chart generation.

## Important horizon convention

The frozen 001D signal occurs at the close of bar `t`, entry occurs at the open of `t+1`, and the frozen exit is the close of `t+6`.

Therefore:

- the frozen **30-minute signal horizon** is measured from the signal timestamp to `t+6`;
- the actual elapsed time from executable entry (`t+1` open) to the frozen exit (`t+6` close) is approximately **25 minutes** on regular 5-minute data.

This distinction is recorded explicitly so that forward-path analysis does not accidentally reinterpret the frozen strategy as a 30-minute holding period after entry.

## Run command

```powershell
python scripts/run_strategy_001g_replay.py data/raw/NSE_GOLDBEES_5minute.csv
python scripts/plot_strategy_001g_results.py data/reports/goldbees_strategy_001g_replay
```

The runner writes:

```text
data/reports/goldbees_strategy_001g_replay/
├── replayed_trades.csv
├── forward_path.csv
├── forward_path_summary.csv
├── mfe_mae.csv
└── reconciliation.csv
```

The plotting script additionally writes:

```text
forward_path_returns.png
mfe_mae_distribution.png
```

## Acceptance checks

The local run should explicitly report:

1. replayed trade count;
2. reference 001D trade count;
3. number of exact reconciliations within the documented tolerance;
4. number of discrepancies.

The known 001D baseline contains approximately **310 trades**. A mismatch is a research finding requiring investigation; it must not be repaired by silently changing the frozen strategy.

## What will be analyzed after execution

### A. Replay integrity

- signal timestamps;
- entry timestamps/prices;
- exit timestamps/prices;
- gross returns;
- missing/extra trades;
- floating-point differences.

### B. Forward-path shape

For each fixed signal-relative horizon:

- observations;
- mean return;
- median return;
- win rate;
- p10/p90 return.

The key question is whether the gross edge appears broadly after entry or only very late in the frozen holding window.

### C. Excursion behavior

Measure:

- MFE distribution;
- MAE distribution;
- time from entry to MFE/MAE;
- relationship between MFE/MAE and final gross return.

MFE/MAE are OHLC-range diagnostics. They do not prove that an intrabar order could have captured the exact high or low because OHLCV does not reveal intrabar sequencing.

### D. Feature slices

The replay retains the point-in-time variables needed for descriptive slices. These can be examined without turning them into new trading rules. Any proposed filter or parameter change must receive a new experiment identifier and an untouched evaluation period.

## Decision rule

Until the local run is completed and reviewed, 001G remains **execution pending**.

Even if the replay is clean and the forward path is attractive, the next gate remains predefined robustness and chronological out-of-sample/walk-forward validation. 001G does not authorize paper or live trading.
