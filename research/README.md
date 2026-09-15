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

**Decision: 🟡 Candidate — executable baseline implemented; historical result pending.**

The frozen implementation uses:

- 5-minute bars;
- previous 30 completed same-session closes;
- sample standard deviation;
- z-score ≥ +2.0;
- prior six-bar return > 0;
- long-only;
- signal after event-bar close;
- next-bar-open entry;
- close-of-t+6 exit;
- fixed 12-bar cooldown;
- no overnight trades;
- one position at a time;
- constant-notional normalized accounting;
- no leverage or optimized sizing;
- no parameter optimization.

The engine separately reports gross performance and explicit cost/slippage sensitivity.

Implementation:

```text
research/journal/001D_formal_strategy_spec.md
src/research/continuation_backtest.py
tests/test_continuation_backtest.py
scripts/run_strategy_001_backtest.py
```

## Strategy 001 promotion path

```text
001C point-in-time validation              🟡 promising
        ↓
001D formal baseline backtest              ← CURRENT
        ↓
Gross + cost/slippage analysis
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
