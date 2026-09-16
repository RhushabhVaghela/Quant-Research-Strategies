# Quant Research Workspace

This directory records the research process behind the strategy portfolio.

## Research principles

- Start with a financial hypothesis, not a model.
- Treat Quantra/WQU notebooks as reference material and building blocks, not automatically validated strategies.
- Establish a simple baseline before adding ML/DL.
- Use time-ordered validation and walk-forward testing where appropriate.
- Prevent look-ahead bias, leakage, survivorship bias, and data snooping.
- Include explicit execution, cost, and slippage assumptions.
- Record negative and inconclusive results.
- Keep research-universe selection independent from strategy performance where possible.
- Complete Strategy 001 before starting Strategy 002.

## Reference material

The repository contains WorldQuant University learning material and code under `trading_resources/WQU_resources/`. These resources can be used for study, implementation patterns, candidate strategy ideas, feature engineering, and later ML/model development. Code from those resources is not treated as automatically validated trading logic.

## Phase 0 controls

- `phase_00_india_retail_trading_spec.md`
- `phase_00_capital_and_execution_spec.md`
- `phase_00_research_universe_spec.md`

These documents define the project's research and execution controls.

## Phase 1 universe work

- `phase_01_universe_audit.md` — candidate resolution, common historical-data collection, audit gates, liquidity/capital checks, and universe-bias controls.
- `universe_candidates.csv` — reproducible initial candidate manifest.

The candidate manifest is defined independently of strategy performance.

## Strategy 001 research path

### 001 — GOLDBEES mean reversion

**Decision: 🔴 Rejected.**

The initial hypothesis was that unusually large deviations from a recent intraday mean would reverse. The event study did not support that relationship; positive deviations were followed by positive rather than negative returns.

### 001A — event structure & conditioning

**Decision: ✅ Complete — continuation lead identified.**

A fixed 12-bar non-overlap diagnostic reduced event clustering while preserving the positive-deviation continuation pattern. Prior six-bar trend was the clearest conditioning variable. No parameters were optimized.

### 001B — continuation attribution

**Decision: 🟡 Promising research lead.**

The strongest subgroup was positive deviation during a prior uptrend. Event returns exceeded matched non-event baselines across the tested horizons. Detailed results are in `journal/001B_continuation_attribution_results.md`.

### 001C — point-in-time continuation validation

**Decision: 🟡 Promising — continuation lead survives the point-in-time benchmark.**

The implementation produced 1,668 frozen events and 401 selected non-overlapping events under the fixed 12-bar cooldown.

For positive deviation + prior uptrend:

| Horizon | Event return | PIT baseline | Incremental return |
|---|---:|---:|---:|
| 5 min | +0.0148% | +0.0032% | **+0.0115%** |
| 15 min | +0.0205% | +0.0099% | **+0.0106%** |
| 30 min | +0.0443% | +0.0194% | **+0.0249%** |
| 60 min | +0.0527% | +0.0279% | **+0.0247%** |

The 30-minute primary horizon therefore showed approximately +2.49 basis points of incremental gross return relative to the point-in-time matched benchmark. This remains a research result, not a deployment decision.

Detailed results are in `journal/001C_continuation_hypothesis_results.md`.

### 001D — formal trading backtest

**Decision: 🟡 Candidate — gross backtest positive; cost sensitivity unresolved.**

The frozen implementation uses 5-minute GOLDBEES data, previous 30 completed same-session closes, sample standard deviation, z-score ≥ +2.0, prior six-bar return > 0, long-only, next-bar-open entry, close-of-t+6 exit, fixed 12-bar cooldown, no overnight feature construction, one position at a time, and no leverage or optimized sizing.

The completed baseline contains 310 trades. Gross performance was +15.85% cumulative with a +4.77 bps mean trade return, 55.81% win rate, and 2.269 profit factor. The predefined cost grid showed that modest friction can eliminate the gross edge, so this is not paper/live ready.

### 001E — trade distribution & execution audit

**Decision: 🟡 Complete — gross edge remains interesting, execution economics unresolved.**

001E found a +2.41 bps median and +4.77 bps mean gross trade return; the top 10% of winners contributed about 53.7% of positive profit; gross performance remained positive in each chronological period examined; mean trades per active day were about 1.30; median holding duration was 25 minutes; and the predefined friction grid rapidly consumed the small per-trade edge.

Detailed results are in `journal/001E_trade_distribution_execution_audit_results.md`.

### 001F — trade-level edge & execution decomposition

**Decision: 🟡 Promising for further research — not paper/live ready.**

After removing the top 10% of winning trades, the remaining 292 trades still had a +1.41 bps mean gross return, +1.32 bps median, 53.08% win rate, and 1.354 profit factor. Tail winners remain important, but the gross result is not solely produced by a few extremes. Later-session buckets were descriptively stronger, while z-score buckets showed no clean monotonic relationship. These are not selected filters.

The compact 001D trade export lacked the complete signal-time feature set and intermediate forward returns, motivating 001G.

Detailed results: `journal/001F_trade_edge_execution_decomposition_results.md`.

### 001G — point-in-time feature & forward-path replay

**Decision: 🟡 Complete — replay reconciled; forward-path diagnostics informative; not paper/live ready.**

The frozen 001D strategy was reconstructed directly from validated GOLDBEES OHLCV. All 310 replayed trades matched the 310-trade 001D reference within tolerance, with zero discrepancies.

The forward path was already positive before the frozen exit: mean return was +1.36 bps at 5 minutes, +2.44 bps at 10 minutes, +3.40 bps at 20 minutes, +4.51 bps at 25 minutes, and +4.77 bps at 30 minutes. Median return was +2.41 bps at 30 minutes. The 45- and 60-minute samples are smaller because paths cannot cross the session boundary.

MFE averaged +15.35 bps with a +9.48 bps median, while MAE averaged -9.63 bps with a -6.88 bps median. These are path diagnostics, not proof that intrabar highs/lows could be captured in execution.

Descriptive signal-time slices showed stronger gross outcomes in the 13–15 session buckets, but this is not being converted into an afternoon-only filter. Z-score buckets showed no clean monotonic relationship, and simple correlations of gross return with z-score, prior six-bar return, and volume ratio were small.

Detailed results: `journal/001G_point_in_time_feature_replay_results.md`.

### 001H — predefined robustness & chronological holdout

**Decision: 🟡 Complete — historical robustness encouraging; execution economics still unresolved.**

The frozen 001D strategy remained positive across all four chronological periods. 2025 contained 197 trades with +4.53 bps mean gross return, 57.87% win rate, 2.406 profit factor, and +9.31% cumulative gross return. The 2026 chronological holdout contained 113 trades with +5.18 bps mean gross return, 52.21% win rate, 2.105 profit factor, and +5.98% cumulative gross return.

The historical split provides evidence of persistence rather than a collapse in the later sample. However, it is explicitly **OOS-style**, not pristine untouched OOS, because the full January 2025–August 2026 sample has already been examined during research.

The cost ladder remains the central economic concern: 4 bps round-trip leaves +0.77 bps mean net trade return and +2.34% cumulative net return, while 6 bps round-trip produces -1.23 bps mean net return and -3.81% cumulative net return. At 14 bps round-trip, mean net return is -9.23 bps and cumulative net return is -24.95%. These are scenario assumptions, not observed live costs.

The local run completed successfully with 59 tests passing before the 001H robustness analysis. The plotting script initially exposed an implementation issue because the exported trade table does not carry the derived period label; that script has now been fixed to reconstruct the period from `signal_timestamp`.

Detailed results: `journal/001H_predefined_robustness_chronological_holdout_results.md`.

### 001I — prospective OOS / paper-shadow validation

**Decision: 🟡 Protocol hardened — prospective data collection is the next gate.**

Because the historical dataset has been examined through August 2026, we will **not** relabel August 2026 or any September data inspected before the prospective start as OOS. The first genuinely prospective OOS period begins after the immutable activation timestamp, with signals recorded before their outcomes are known.

The frozen 001D strategy remains unchanged during this window. Each signal is logged point-in-time, then its outcome and execution-friction information are appended only after the fixed exit completes. No threshold, holding period, time-of-day filter, stop, target, or other strategy rule may be changed based on observed prospective outcomes.

The first phase is paper/shadow rather than live capital. The implementation now has an append-only prospective ledger, an immutable run manifest, a collector that can restart across sessions without moving the OOS boundary, and a dedicated integrity validator.

Run validator: `scripts/validate_strategy_001i_run.py`.

Protocol: `journal/001I_prospective_oos_paper_shadow_protocol.md`.

Results journal: `journal/001I_prospective_oos_paper_shadow_results.md`.

## Strategy 001 promotion path

```text
001C point-in-time validation                       🟡 promising
        ↓
001D formal baseline backtest                       🟡 gross positive / costs unresolved
        ↓
001E distribution + execution audit                 🟡 complete
        ↓
001F trade decomposition                            🟡 complete
        ↓
001G PIT feature + forward-path replay              🟡 complete
        ↓
001H predefined robustness + historical holdout     🟡 complete
        ↓
001I prospective OOS / paper-shadow                 ← CURRENT
        ↓
Execution validation
        ↓
Controlled live validation (only if justified)
        ↓
Strategy 001 final decision
        ↓
Only then: Strategy 002
```

A failure at any gate is recorded rather than repaired by post-hoc parameter tuning.

**No strategy is approved for deployment yet.**
