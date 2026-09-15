# Strategy 001B — Continuation Attribution

**Status:** 🟡 Promising research lead — not paper-ready and not a trading rule

## Why this experiment exists

Strategy 001 began with a symmetric mean-reversion hypothesis: unusually large deviations from a recent intraday mean should be followed by movement back toward that mean.

Experiment 001 rejected that hypothesis. Large positive deviations were followed by positive returns rather than negative returns. Experiment 001A then showed that this continuation-like behavior survived a fixed non-overlap filter and was especially visible when the prior six-bar trend was upward.

001B asks whether this continuation contains information beyond ordinary intraday drift and the trend that was already present before the event.

## Research question

> Does the continuation-like return after a large deviation contain information beyond ordinary intraday drift and the recent six-bar trend?

## Hypotheses

### H1 — Continuation lead

A large positive deviation, especially during a prior uptrend, is followed by positive returns.

### H2 — Incremental information

The event return is larger than the return normally observed in comparable non-event observations after matching on predefined time-of-day and prior-trend buckets.

### H3 — Directional asymmetry

Positive and negative deviations may behave differently. We therefore do not assume that a positive continuation effect must have a symmetric negative counterpart.

These are research hypotheses, not trading rules.

## Fixed methodology

The experiment inherits the Strategy 001 defaults without optimization:

- 5-minute bars;
- 30 completed bars for the deviation lookback;
- absolute z-score threshold of 2.0;
- same-session forward returns;
- horizons of 1, 3, 6, and 12 bars;
- fixed 12-bar non-overlap filter for the primary event set.

### Attribution dimensions

1. **Deviation direction:** positive versus negative.
2. **Prior trend:** down, flat, or up using the six-bar return already calculated before the event.
3. **Time of day:** the predefined bins used in 001A.
4. **Event versus non-event:** compare event observations with observations that did not meet the event condition.

### Non-event benchmark

The benchmark uses available non-event observations matched on the same predefined time-of-day and prior-trend buckets.

This is a **descriptive attribution benchmark**, not a prospective trading signal. It is calculated over the full research sample to answer the narrow attribution question. It must not be used directly to construct a live signal. A separate point-in-time benchmark is required before trading.

## 001B empirical result

The strongest and most interpretable subgroup was **positive deviation + prior uptrend**. After the fixed 12-bar non-overlap filter, it contained hundreds of observations and showed positive event returns above the matched non-event baseline at every tested horizon:

| Horizon | Events | Event mean | Matched baseline | Incremental return | Event win rate | Baseline win rate |
|---|---:|---:|---:|---:|---:|---:|
| 5 min | 363 | +0.0156% | +0.0025% | **+0.0128%** | 49.6% | 46.4% |
| 15 min | 343 | +0.0202% | +0.0084% | **+0.0113%** | 50.7% | 50.4% |
| 30 min | 299 | +0.0443% | +0.0177% | **+0.0255%** | 56.2% | 51.8% |
| 60 min | 246 | +0.0532% | +0.0270% | **+0.0243%** | 57.3% | 52.4% |

Positive deviations pooled across all trend regimes also remained above the matched baseline at all four horizons. The incremental differences were approximately +0.0124%, +0.0161%, +0.0354%, and +0.0349% for 5, 15, 30, and 60 minutes respectively.

Negative deviations did not show a symmetric reversal pattern. Pooled incremental returns were approximately -0.0085%, +0.0019%, -0.0133%, and -0.0214% across the same horizons.

The detailed result table and methodology are recorded in `research/journal/001B_continuation_attribution_results.md`.

## Interpretation

In simple terms:

> When GOLDBEES was already in an upward short-term trend and then made an unusually large positive move, the next 15–60 minutes were historically stronger than comparable non-event periods.

This supports the continuation lead and provides exploratory evidence that the event contains information beyond the matched trend/time-of-day baseline.

It does **not** prove a tradable edge. The benchmark is descriptive and full-sample, and costs, execution, and out-of-sample stability have not yet been tested.

## Decision gates

### H1 — Continuation lead: **PROMISING**

The positive-deviation continuation survived the non-overlap filter and remained coherent across the tested horizons, particularly in the prior-uptrend regime.

### H2 — Incremental information: **PROMISING, exploratory**

Event returns exceeded the matched non-event baseline across the strongest positive/uptrend subgroup and positive deviations overall. Because the current baseline is full-sample descriptive attribution, this result must be confirmed using a strictly point-in-time benchmark before it can support a trading rule.

### H3 — Directional asymmetry: **PROMISING**

Positive and negative deviations behave differently. The data does not support a symmetric reversal rule.

## Final 001B decision

### **PROMISING RESEARCH LEAD**

We have enough evidence to stop trying to rescue the original symmetric mean-reversion strategy and to formalize a continuation hypothesis for broader validation.

We will **not** optimize the hypothesis around GOLDBEES based on these results. The next stage should lock the hypothesis first and then apply it consistently across the predefined multi-instrument universe.

## Important limitations

- The event-vs-non-event benchmark is descriptive and full-sample, not point-in-time.
- No complete trading backtest has been approved.
- No transaction costs, spread, slippage, or market-impact model has yet been applied.
- No chronological out-of-sample or walk-forward validation has been performed.
- No statistical significance framework has yet been finalized for the eventual trading signal.
- GOLDBEES is a discovery/prototype instrument, not evidence that it is the best instrument to trade.
- No parameter optimization should be inferred from the strongest subgroup.

## Next phase

1. Freeze a continuation strategy specification.
2. Define the event, trend feature, entry timing, holding period, and exit logic using only information available before the decision.
3. Build a point-in-time baseline.
4. Apply the locked hypothesis across the predefined research universe.
5. Evaluate cross-instrument consistency rather than cherry-picking winners.
6. Add realistic transaction costs, spread, slippage, and execution constraints.
7. Perform chronological out-of-sample / walk-forward validation.
8. Only then consider paper/shadow trading.

**001B alone does not justify live trading.**
