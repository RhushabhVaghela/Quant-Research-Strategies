# Strategy 001 — GOLDBEES Intraday Mean Reversion

**Status:** 🔴 Original mean-reversion hypothesis rejected; continuation lead promoted to frozen validation

## Research question

Does an unusually large short-term deviation of GOLDBEES from its recent intraday equilibrium tend to be followed by a statistically meaningful move back toward that equilibrium?

## Why GOLDBEES?

GOLDBEES is the first instrument selected for this strategy research because it is accessible for eventual small-account validation and allows us to study an intraday hypothesis without starting with derivatives. Its lower nominal unit price is useful for later capital-feasibility analysis, but **price alone is not evidence of profitability**. The strategy must first demonstrate an edge after realistic costs and execution assumptions.

## Research discipline

This experiment was deliberately an **event study before a trading backtest**. We did not optimize a trading rule until we had evidence about the underlying relationship.

The sequence is:

1. Define the hypothesis before examining the result.
2. Measure the deviation using only information available at the event bar.
3. Measure future returns only after the event.
4. Keep forward returns within the same trading session.
5. Separate positive and negative deviations.
6. Report sample size and distribution, not only average return.
7. Record negative and inconclusive results rather than deleting them.
8. Only promote a hypothesis after statistical and economic evidence justifies doing so.

## Experiment 001 — Baseline deviation event study

### Hypothesis

When GOLDBEES closes unusually far from its recent intraday mean, the subsequent return should tend to have the opposite sign if a short-term mean-reversion effect exists.

The initial implementation used a configurable default lookback of **30 five-minute bars** and an absolute z-score threshold of **2.0**. These were research defaults, not optimized parameters.

### Prediction target

For each event, calculate same-session forward close-to-close returns over 1, 3, 6, and 12 bars (5, 15, 30, and 60 minutes). For mean reversion, positive deviation should be followed by negative return and negative deviation by positive return.

### Result

The GOLDBEES dataset contained **30,912 five-minute bars** from January 2025 through August 2026. The baseline event study produced **2,953 combined directional event observations**.

The symmetric mean-reversion hypothesis was **rejected**. Reversion-aligned mean returns were negative at every tested horizon:

| Horizon | Mean reversion-aligned return |
|---|---:|
| 5 min | -0.00365% |
| 15 min | -0.00901% |
| 30 min | -0.01703% |
| 60 min | -0.02105% |

Positive deviations instead showed positive average forward returns, increasing from approximately **+0.00764% at 5 minutes** to **+0.05577% at 60 minutes**. Negative deviations were weaker and inconsistent.

### Decision

**REJECTED as a symmetric mean-reversion signal.**

We did not convert this into a trading rule merely because another parameterization might produce a better backtest.

## Experiment 001A — Event Structure & Conditioning Diagnostics

001A tested whether the continuation-like behavior survived dependence controls and whether it was concentrated in predefined conditions. It retained the fixed 30-bar / 2.0-z-score baseline and used a fixed 12-bar non-overlap diagnostic.

### Main findings

- Raw events were highly clustered; the fixed 12-bar non-overlap filter reduced this dependence.
- Positive-deviation continuation remained visible after non-overlap filtering.
- The clearest concentration was positive deviation combined with an existing **upward six-bar prior trend**.
- Negative-deviation behavior was weaker and inconsistent.
- Volume and volatility did not provide a simple primary explanation.
- Late-session and severity concentrations were treated as exploratory only; no parameters were optimized around them.

### Decision

**Symmetric mean reversion remained rejected. Continuation became a promising exploratory lead.**

The unresolved question was whether continuation contained information beyond ordinary intraday drift and the trend already present before the event.

## Experiment 001B — Continuation Attribution

001B asked:

> **Does the continuation-like return after a large deviation contain information beyond ordinary intraday drift and the recent six-bar trend?**

It compared positive and negative deviations, prior-trend regimes, predefined time-of-day buckets, and fixed non-overlapping events against matched non-event observations.

### Result

The strongest subgroup was **positive deviation + prior uptrend**. Event returns exceeded the matched non-event baseline at every tested horizon:

| Horizon | Events | Event mean | Matched baseline | Incremental return |
|---|---:|---:|---:|---:|
| 5 min | 363 | +0.0156% | +0.0025% | **+0.0128%** |
| 15 min | 343 | +0.0202% | +0.0084% | **+0.0113%** |
| 30 min | 299 | +0.0443% | +0.0177% | **+0.0255%** |
| 60 min | 246 | +0.0532% | +0.0270% | **+0.0243%** |

Positive deviations also remained above the matched baseline when trend regimes were pooled. Negative deviations did not show the symmetric reversal pattern expected under mean reversion.

### Decision

**PROMISING RESEARCH LEAD.**

The evidence is sufficient to stop investigating whether the original symmetric mean-reversion relationship should become a strategy. It should not.

The evidence is also sufficient to formalize a continuation hypothesis for broader validation. However, 001B is not a validated trading strategy because the non-event comparison is a full-sample descriptive attribution benchmark and we have not yet tested costs, execution, or chronological out-of-sample stability.

Detailed results are recorded in `research/journal/001B_continuation_attribution_results.md`.

## Experiment 001C — Frozen Continuation Hypothesis

001C is the lock between discovery and broader validation. The continuation hypothesis is frozen before instrument selection, parameter search, or ML filtering.

### Frozen hypothesis

> **When a 5-minute bar closes at least 2.0 standard deviations above the previous 30 completed closes and the prior six-bar return is positive, the subsequent 30-minute return should be positive and stronger than the historical point-in-time return of comparable non-event observations.**

### Frozen trading baseline

- deviation lookback: 30 completed five-minute bars;
- z-score: ≥ +2.0;
- trend: prior six-bar return > 0;
- primary horizon: 6 bars / 30 minutes;
- decision: after event-bar close;
- entry: next-bar open;
- exit: close of bar `t+6`;
- overlap control: fixed 12-bar session cooldown;
- no overnight feature construction;
- minimum point-in-time benchmark history: 30 completed comparable observations.

The 30-minute horizon is a fixed middle-horizon baseline, not a post-hoc selection of the best-performing horizon.

### Point-in-time benchmark

For an event at timestamp `t`, a historical non-event observation is eligible only if:

- it belongs to the same predefined time-of-day bucket;
- it belongs to the same prior-trend bucket;
- its own six-bar forward outcome has fully completed **strictly before `t`**;
- its outcome is valid and observed.

This prevents the subtle leakage where an observation starts before the event but its future outcome would not yet have been known at the event decision time.

The implementation is in `src/research/point_in_time_baseline.py`, with tests in `tests/test_point_in_time_baseline.py` and a reproducible runner in `scripts/run_point_in_time_baseline.py`.

### Decision

**Specification frozen — validation pending.**

No instrument will be selected because of its GOLDBEES discovery performance. The exact hypothesis will first be audited for leakage and then applied unchanged across the predefined research universe.

## What changed in our research direction?

We are no longer asking:

> "Can we make mean reversion work on GOLDBEES?"

We are now asking:

> "Does an unusually large positive move, when combined with an already-positive short-term trend, provide repeatable continuation information across a predefined universe?"

This is a new hypothesis and is treated independently from the rejected mean-reversion hypothesis.

## Next phase

1. Run the 001C point-in-time benchmark on GOLDBEES as an implementation/leakage audit.
2. Verify the frozen event and execution conventions on synthetic tests and historical data.
3. Apply the unchanged hypothesis across the predefined multi-instrument universe.
4. Evaluate cross-instrument consistency rather than cherry-picking winners.
5. Add realistic transaction costs, spread, slippage, and execution constraints.
6. Perform chronological out-of-sample / walk-forward validation.
7. Only then consider paper/shadow trading.

## Current limitations

- No complete cost-aware trading backtest has been approved.
- No out-of-sample or walk-forward test has been performed.
- The point-in-time benchmark has been implemented but its historical GOLDBEES result has not yet been run and reviewed in this repository state.
- No live or paper deployment is justified by these experiments alone.
- The original mean-reversion hypothesis remains permanently rejected and will not be rewritten based on later results.
