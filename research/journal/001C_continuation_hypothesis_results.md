# Strategy 001C — Point-in-Time Validation Results

**Status:** 🟡 Promising research lead — proceed to formal strategy backtest

## Purpose

001C tested the frozen continuation hypothesis using a point-in-time benchmark. The purpose was to determine whether the continuation effect remained positive when the benchmark was restricted to historical observations whose forward outcomes would already have been known at the event time.

## Frozen hypothesis tested

A 5-minute bar qualifies when:

- its close is at least 2.0 standard deviations above the previous 30 completed same-session closes; and
- its prior six-bar return is positive.

The primary outcome is the subsequent 30-minute return. The frozen execution convention for the later trading baseline is next-bar-open entry and close-of-`t+6` exit.

## Point-in-time benchmark result

The GOLDBEES implementation produced **1,668 frozen events** and **401 selected non-overlapping events** under the fixed 12-bar cooldown.

For the positive/uptrend continuation condition, the point-in-time benchmark produced the following aggregate results:

| Horizon | Event return | Point-in-time baseline | Incremental return | Positive incremental rate |
|---|---:|---:|---:|---:|
| 5 min | +0.0148% | +0.0032% | **+0.0115%** | 51.2% |
| 15 min | +0.0205% | +0.0099% | **+0.0106%** | 47.8% |
| 30 min | +0.0443% | +0.0194% | **+0.0249%** | 51.0% |
| 60 min | +0.0527% | +0.0279% | **+0.0247%** | 49.0% |

The pre-specified 30-minute primary horizon therefore showed approximately **+2.49 basis points of incremental gross return** relative to the point-in-time matched benchmark.

## Interpretation

The continuation lead **survives the point-in-time benchmark restriction**. This is stronger evidence than the full-sample descriptive attribution used in 001B.

However, this result does not yet establish a tradable alpha. The positive incremental rate is close to 50%, so the positive mean may be driven by return magnitude rather than a large increase in hit rate. The effect must therefore be evaluated at the trade level, including distribution, drawdown, turnover, costs, and execution assumptions.

The 001C result also does not establish cross-instrument generalization or chronological out-of-sample stability.

## Decision

**PROMISING — promote the continuation hypothesis to the formal Strategy 001D candidate backtest.**

The original symmetric mean-reversion hypothesis remains permanently **REJECTED**.

We will not optimize the 001D rule using the same GOLDBEES discovery evidence. The frozen rule becomes the baseline for the first realistic trading backtest.

## What 001C establishes

- The continuation effect is not eliminated by requiring a strictly point-in-time benchmark.
- The positive/uptrend condition remains directionally positive at all tested horizons.
- The 30-minute primary horizon shows approximately +2.49 bp incremental gross return.
- The fixed non-overlap selection provides a less dependent event sample.

## What 001C does not establish

- statistical significance sufficient for production use;
- profitability after costs and slippage;
- realistic execution feasibility;
- cross-instrument generalization;
- out-of-sample or walk-forward robustness;
- appropriate account-level position sizing;
- suitability for paper or live trading.

## Next experiment: 001D

Implement the frozen trading rule:

1. signal after event-bar close;
2. enter at next-bar open;
3. exit at close of `t+6`;
4. long-only;
5. fixed 12-bar cooldown;
6. no overnight trades;
7. constant-notional normalized accounting;
8. gross, cost-sensitivity, and slippage-sensitivity reporting;
9. no parameter optimization.

Implementation files:

- `research/journal/001D_formal_strategy_spec.md`
- `src/research/continuation_backtest.py`
- `tests/test_continuation_backtest.py`
- `scripts/run_strategy_001_backtest.py`

The first 001D run is an implementation and economic-feasibility test, not a license to deploy capital.
