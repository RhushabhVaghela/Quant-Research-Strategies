# Strategy 001I — Prospective OOS / Paper-Shadow Results

## Status

**🟡 Protocol hardened — prospective data collection not yet completed.**

This file is intentionally a results template. No prospective performance numbers are populated until the frozen Strategy 001D process has generated and recorded observations after the 001I activation boundary.

## OOS qualification

Historical data through August 2026 has already been examined during Strategy 001 research. Therefore:

- 2025 = development/reference;
- 2026 through the examined historical period = chronological holdout / OOS-style;
- September observations inspected before 001I activation = historical/research data;
- first signals captured prospectively after activation = genuine prospective OOS observations.

The activation timestamp must be recorded in `data/prospective/strategy_001i/run_manifest.json`. Restarting the same run does not move that boundary.

## Frozen strategy

The 001D rules are unchanged:

- GOLDBEES 5-minute OHLCV;
- previous 30 completed same-session closes;
- sample standard deviation;
- z-score ≥ +2.0;
- prior six-bar return > 0;
- long-only;
- signal at event-bar close;
- next-bar-open entry;
- close of `t+6` exit;
- 12-bar cooldown;
- no overnight feature construction;
- one position at a time;
- no leverage or optimized sizing.

## Prospective review checkpoints

These are review checkpoints, not success thresholds:

| Checkpoint | Purpose | Result |
|---|---|---|
| 20 completed trades | Operational/data-quality review | Pending |
| 50 completed trades | First statistical review | Pending |
| 100 completed trades | Stronger stability review | Pending |
| ~3 months | Time/regime review | Pending |

## Signal/trade summary

| Metric | Prospective result | Historical reference |
|---|---:|---:|
| Signals/trades | Pending | 310 frozen trades |
| Mean gross return | Pending | +4.77 bps |
| Median gross return | Pending | +2.41 bps |
| Win rate | Pending | 55.81% |
| Profit factor | Pending | 2.269 |
| Cumulative gross return | Pending | +15.85% |
| Max drawdown | Pending | -0.90% |
| Daily Sharpe diagnostic | Pending | 2.710 |

Historical reference values are provided only for comparison; they are not prospective targets.

## Execution economics

| Metric | Prospective result |
|---|---:|
| Mean observed spread | Pending |
| Median observed spread | Pending |
| Mean slippage | Pending |
| Brokerage/statutory costs | Pending |
| Mean net return | Pending |
| Median net return | Pending |
| Net cumulative return | Pending |
| Net max drawdown | Pending |

Observed execution costs must be measured separately where possible rather than inferred from the historical cost grid.

## Distribution comparison

To be populated only after prospective observations exist:

- P10/P25/P50/P75/P90;
- largest winner/loser;
- top-10%-winner profit share;
- MFE/MAE;
- forward path at 5/10/15/20/25/30/45/60 minutes where session data permit.

## Operational integrity

Before interpreting performance, run:

```powershell
python scripts/validate_strategy_001i_run.py data/prospective/strategy_001i
```

Record:

- number of expected vs captured bars;
- missing/delayed data;
- signal logging failures;
- duplicate records;
- outcome finalization failures;
- any manual intervention;
- any deviation from the frozen strategy.

A capture-system failure must not be misclassified as a strategy failure.

## Decision

**Pending prospective evidence.**

The eventual decision will be one of:

- **🟢 Proceed to separate controlled-live validation protocol**;
- **🟡 Extend paper/shadow validation**;
- **🔴 Reject/freeze Strategy 001**.

No strategy parameters will be changed to improve this prospective cohort after outcomes are observed.
