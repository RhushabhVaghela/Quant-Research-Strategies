# Strategy 001B — Continuation Attribution

**Status:** 🔬 Research experiment — implementation complete; empirical result pending

## Why this experiment exists

Strategy 001 began with a symmetric mean-reversion hypothesis: unusually large deviations from a recent intraday mean should be followed by movement back toward that mean.

Experiment 001 rejected that hypothesis. Large positive deviations were followed by positive returns rather than negative returns. Experiment 001A then showed that this continuation-like behavior survived a fixed non-overlap filter and was especially visible when the prior six-bar trend was upward.

That is a useful clue, but it is **not yet evidence of a tradable momentum strategy**. A price that continues upward after an event may simply be experiencing normal intraday drift or may already be trending before the event. 001B is designed to separate those explanations.

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

The benchmark uses all available non-event observations matched on the same predefined time-of-day and prior-trend buckets.

This is a **descriptive attribution benchmark**, not a prospective trading signal. Because the benchmark is calculated over the full research sample, it must not be used directly to construct a live signal. If the attribution result is promising, a separate point-in-time baseline and trading experiment will be required.

## What would count as evidence?

### Reject

Reject the continuation lead if positive-deviation events do not show a stable directional effect, or if their apparent return advantage disappears relative to matched non-event observations.

### Inconclusive

Use this label if the direction is interesting but sample sizes, consistency across horizons/conditions, or baseline comparisons are insufficient to support a clear conclusion.

### Promising

Use this label only if the continuation effect:

- remains visible after the 12-bar non-overlap filter;
- is directionally coherent across sensible horizons;
- is not explained by the ordinary matched non-event baseline;
- remains interpretable after conditioning on prior trend and time of day; and
- is strong enough to justify a separate baseline trading strategy and out-of-sample test.

Even a **Promising** result does not mean Paper Ready.

## Outputs

The runner writes:

```text
data/reports/goldbees_continuation_attribution/
├── direction_trend_summary.csv
├── event_vs_non_event_summary.csv
└── metadata.csv
```

Run with:

```powershell
python scripts/run_continuation_attribution.py data/raw/NSE_GOLDBEES_5minute.csv
```

## Research interpretation rule

We will not select a time window, z-score threshold, trend threshold, or other parameter because it produces the best result in this experiment. Any parameter optimization belongs to a later, explicitly controlled model-development stage with time-ordered out-of-sample validation.

## Promotion path

If 001B is promising, the next stage is **not immediately live trading**. We will create a separate continuation strategy specification, define a simple baseline trading rule, model costs/slippage, test across the predefined multi-instrument universe, and then perform chronological out-of-sample/walk-forward validation.

If 001B is rejected, the failure will remain in the journal and we will formulate a new economic hypothesis rather than rewriting Strategy 001.
