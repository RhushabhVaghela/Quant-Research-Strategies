# Strategy 001I — Prospective OOS / Paper-Shadow Results

## Status

**🔵 Closed for capital-pursuit priority — insufficient frequency; not statistically rejected.**

Strategy 001I observed the frozen 001D GOLDBEES strategy prospectively without changing its parameters. The collector operated on 2026-09-17 and recorded two genuine prospective trades after the immutable activation boundary.

The experiment is closed as the primary capital-deployment track because the frozen single-instrument implementation generated only two selected trades in the observed session. This frequency is incompatible with the September 2026 accelerated research/deployment objective.

Closing the track does **not** mean that two trades statistically disprove the 001D hypothesis. The sample is far too small for that conclusion.

The frozen 001D rule must not be changed using these outcomes. The same economic hypothesis is now being tested as **Strategy 001J**, a new experiment under the same Strategy 001 research family, using a predefined point-in-time equity universe and a separately registered parameter-selection process.

## OOS qualification

Historical data through August 2026 had already been examined during Strategy 001 research. The 2026-09-17 observations below were captured prospectively after activation and therefore form genuine prospective observations for the frozen 001D rule.

## Frozen strategy observed

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

## 2026-09-17 prospective observations

| Signal | z-score | Paper entry | Paper exit | Gross/net return | MFE | MAE |
|---|---:|---:|---:|---:|---:|---:|
| 12:00 | 2.2675 | 124.31 | 124.21 | -8.04 bps | +0.80 bps | -16.89 bps |
| 13:05 | 2.5350 | 124.87 | 124.71 | -12.81 bps | +5.61 bps | -22.42 bps |

Simple sum of the two trade returns was approximately -20.86 bps; compounded return was approximately -20.85 bps. No statistical inference is made from this sample.

The signal ledger recorded quoted signal spreads of approximately 2.41 bps and 0.80 bps respectively. The paper outcomes do not contain realized broker execution costs; estimated slippage and brokerage fields were zero in the captured paper records. These are therefore raw paper outcomes rather than evidence of executable net profitability.

## Operational integrity

The run was validated with:

```powershell
python scripts/validate_strategy_001i_run.py data/prospective/strategy_001i
```

Validation result:

`Strategy 001I validation PASSED: no prospective-ledger integrity errors found.`

The collector remained paper/shadow only and placed no orders.

## Research interpretation

### What the evidence supports

1. The frozen strategy can operate prospectively with the implemented collector.
2. The prospective ledger and timing controls passed validation for this run.
3. The observed single-instrument frequency is low: two selected trades in the captured session.
4. The first two prospective paper outcomes were negative.
5. Actual execution economics remain unresolved.

### What the evidence does not support

1. It does not statistically reject the underlying continuation hypothesis.
2. It does not establish that the strategy will remain profitable or unprofitable in the future.
3. It does not justify changing 001D parameters.
4. It does not justify live deployment of 001D.

## Final status of Strategy 001

**001I is closed as a capital-pursuit experiment because its frozen GOLDBEES implementation is too low-frequency for the current project deadline.**

The broader continuation hypothesis remains active as Strategy 001 research. It is being investigated in **001J** rather than by modifying 001D or restarting 001I.

## Next research track

See:

- `research/journal/001J_cross_sectional_equity_spec.md`
- `research/journal/001J_universe_u1_spec.md`
- `research/journal/strategy_registry.md`

No 001D parameter changes are permitted.
