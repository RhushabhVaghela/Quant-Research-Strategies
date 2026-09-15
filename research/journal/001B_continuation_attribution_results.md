# Strategy 001B — Continuation Attribution Results

**Status:** 🟡 Promising research lead — not paper-ready and not a trading rule

## Experiment objective

001B asked whether the continuation-like behavior observed after large positive deviations was more than ordinary intraday drift and the prior six-bar trend.

The fixed research setup was inherited from Strategy 001 / 001A:

- GOLDBEES 5-minute bars;
- 30 completed bars for the deviation calculation;
- absolute z-score threshold = 2.0;
- same-session forward returns;
- horizons = 1, 3, 6, and 12 bars;
- fixed 12-bar non-overlap event set;
- predefined six-bar trend regimes and time-of-day buckets.

No parameter was optimized using these results.

## Decision summary

| Hypothesis | Result | Interpretation |
|---|---|---|
| H1 — continuation lead | **PROMISING** | Positive deviations, especially in prior uptrends, are followed by positive returns after non-overlap filtering. |
| H2 — incremental information | **PROMISING, exploratory** | Positive-event returns exceed the matched non-event baseline, especially in the uptrend regime. However, the current benchmark is descriptive full-sample attribution, not a point-in-time test. |
| H3 — directional asymmetry | **PROMISING** | Positive and negative deviations behave differently; there is no symmetric mean-reversion/continuation pattern. |

The correct promotion is therefore **PROMISING RESEARCH LEAD**, not "validated strategy".

## Main aggregate result

The strongest and most interpretable subgroup is **positive deviation + prior uptrend**.

| Horizon | Events | Event mean | Matched non-event mean | Incremental return | Event win rate | Baseline win rate |
|---|---:|---:|---:|---:|---:|---:|
| 5 min | 363 | +0.0156% | +0.0025% | **+0.0128%** | 49.6% | 46.4% |
| 15 min | 343 | +0.0202% | +0.0084% | **+0.0113%** | 50.7% | 50.4% |
| 30 min | 299 | +0.0443% | +0.0177% | **+0.0255%** | 56.2% | 51.8% |
| 60 min | 246 | +0.0532% | +0.0270% | **+0.0243%** | 57.3% | 52.4% |

The event return is therefore higher than the matched non-event return at every tested horizon in this subgroup. The incremental relationship is largest at 30 and 60 minutes.

## Positive deviations overall

When all prior-trend regimes are pooled, positive deviations still show an incremental relationship versus the matched non-event observations:

| Horizon | Events | Event mean | Baseline mean | Incremental return |
|---|---:|---:|---:|---:|
| 5 min | 385 | +0.0141% | +0.0017% | **+0.0124%** |
| 15 min | 360 | +0.0214% | +0.0053% | **+0.0161%** |
| 30 min | 315 | +0.0459% | +0.0105% | **+0.0354%** |
| 60 min | 259 | +0.0519% | +0.0170% | **+0.0349%** |

This is useful because the continuation effect is not confined to one tiny time-of-day bucket or one trend bucket. The prior-uptrend subgroup is nevertheless the cleanest and largest concentration.

## Negative deviations provide an important control

Negative deviations do not show the mirror image that a symmetric mean-reversion hypothesis would predict.

Across all trend regimes:

| Horizon | Negative event mean | Matched baseline mean | Incremental return |
|---|---:|---:|---:|
| 5 min | -0.0067% | +0.0017% | **-0.0085%** |
| 15 min | +0.0072% | +0.0053% | +0.0019% |
| 30 min | -0.0029% | +0.0105% | **-0.0133%** |
| 60 min | -0.0038% | +0.0176% | **-0.0214%** |

This asymmetry is consistent with the earlier rejection of symmetric mean reversion. It also argues against simply replacing the original strategy with a symmetric "trade every extreme move" rule.

## What this means in simple words

The evidence now says:

> When GOLDBEES is already moving upward, and it makes an unusually large positive move, the next 15–60 minutes have historically been stronger than what we normally saw during comparable non-event periods.

The important word is **historically**. We have not yet established that this survives a prospective point-in-time benchmark, transaction costs, slippage, or out-of-sample testing.

A useful mental model is:

```text
Existing uptrend
      +
Unusually large positive deviation
      ↓
Historically stronger subsequent returns
      ↓
PROMISING continuation lead
```

This is no longer a mean-reversion hypothesis.

## Why the result is not yet a validated strategy

There are several reasons to stop before trading:

1. **The event-vs-non-event benchmark is descriptive and full-sample.** It was intentionally used for attribution, but it is not a prospective point-in-time trading benchmark.
2. **No statistical significance framework has yet been finalized for this hypothesis.** The current result is descriptive and exploratory.
3. **No trading costs or execution effects have been modeled.** An average incremental return of a few basis points can be materially affected by spread, brokerage, taxes, slippage, and market impact.
4. **No chronological out-of-sample or walk-forward validation has been performed.**
5. **GOLDBEES is a discovery instrument, not the final universe selection.**
6. **No parameter optimization has been performed, and none should be inferred from the strongest subgroup.**

## Important methodological boundary

The matched baseline uses the full research sample. That is acceptable for the narrow question "what does this historical event look like relative to normal observations?" but it would create look-ahead/data-leakage risk if directly converted into a live signal.

Therefore, before paper trading, the next implementation must construct the benchmark and any signal features strictly from information available before each decision point.

## Final 001B decision

### **PROMISING — proceed to hypothesis specification and multi-instrument validation**

We now have enough evidence to stop investigating whether the original mean-reversion strategy works. It does not.

We also have enough evidence to formalize a **new continuation hypothesis** and test that same hypothesis across the predefined research universe.

This is not permission to optimize the hypothesis around GOLDBEES. The next experiment must use a locked specification so that instruments are evaluated consistently rather than selected because they perform well after inspection.

## Next research phase

1. Write and freeze a continuation-strategy specification.
2. Define the trend feature, deviation event, entry timing, holding period, and exit logic without using future information.
3. Build a point-in-time baseline for the incremental comparison.
4. Apply the locked hypothesis across the predefined multi-instrument universe.
5. Evaluate cross-instrument consistency rather than selecting only the best performers.
6. Add realistic transaction costs, spread, slippage, and execution constraints.
7. Perform chronological out-of-sample / walk-forward validation.
8. Only after those gates consider paper/shadow trading.

**No live trade is justified by 001B alone.**
