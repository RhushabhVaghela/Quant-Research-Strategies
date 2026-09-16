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

The frozen implementation uses 5-minute bars, previous 30 completed same-session closes, sample standard deviation, z-score ≥ +2.0, prior six-bar return > 0, long-only, signal after event-bar close, next-bar-open entry, close-of-t+6 exit, fixed 12-bar cooldown, no overnight trades, one position at a time, constant-notional normalized accounting, no leverage/optimized sizing, and no parameter optimization.

The completed baseline contains 310 trades. Gross performance was +15.85% cumulative with a +4.77 bps mean trade return, 55.81% win rate, and 2.269 profit factor. The predefined cost grid showed that modest friction can eliminate the gross edge, so this is not paper/live ready.

### 001E — trade distribution & execution audit

**Decision: 🟡 Complete — gross edge remains interesting, execution economics unresolved.**

001E found a +2.41 bps median and +4.77 bps mean gross trade return; the top 10% of winners contributed about 53.7% of positive profit; gross performance remained positive in each chronological period examined; mean trades per active day were about 1.30; median holding duration was 25 minutes; and the predefined friction grid rapidly consumed the small per-trade edge.

Detailed results are in `journal/001E_trade_distribution_execution_audit_results.md`.

### 001F — trade-level edge & execution decomposition

**Decision: 🟡 Promising for further research — not paper/live ready.**

After removing the top 10% of winning trades, the remaining 292 trades still had a +1.41 bps mean gross return, +1.32 bps median, 53.08% win rate, and 1.354 profit factor. Tail winners remain important, but the gross result is not solely produced by a few extremes. Later-session buckets were descriptively stronger, while z-score buckets showed no clean monotonic relationship. These are not selected filters.

The compact 001D trade export lacked the complete signal-time feature set and intermediate forward prices, motivating 001G.

Detailed results: `journal/001F_trade_edge_execution_decomposition_results.md`.

### 001G — point-in-time feature & forward-path replay

**Decision: 🟡 Implementation complete — empirical run pending.**

001G reconstructs the frozen 001D trades directly from validated GOLDBEES OHLCV, retains signal-time features without look-ahead, reconciles the replay against the 001D trade export, and measures forward returns plus MFE/MAE. The implementation deliberately reuses the frozen 001D signal/execution logic rather than introducing a new rule.

Implementation:

```text
src/research/strategy_001g_replay.py
scripts/run_strategy_001g_replay.py
scripts/plot_strategy_001g_results.py
tests/test_strategy_001g_replay.py
research/journal/001G_point_in_time_feature_replay.md
research/journal/001G_point_in_time_feature_replay_results.md
```

Run locally against the validated dataset and frozen 001D trade export. Do not interpret 001G as a promotion gate until reconciliation and diagnostics are reviewed.

## Strategy 001 promotion path

```text
001C point-in-time validation              🟡 promising
        ↓
001D formal baseline backtest              🟡 gross positive / costs unresolved
        ↓
001E distribution + execution audit        🟡 complete
        ↓
001F trade decomposition                   🟡 complete
        ↓
001G PIT feature + forward-path replay     ← CURRENT
        ↓
Predefined robustness tests
        ↓
Chronological OOS / walk-forward
        ↓
Paper / shadow validation
        ↓
Execution validation
        ↓
Controlled live validation
        ↓
Strategy 001 final decision
        ↓
Only then: Strategy 002
```

A failure at any gate is recorded rather than repaired by post-hoc parameter tuning.

**No strategy is approved for deployment yet.**
