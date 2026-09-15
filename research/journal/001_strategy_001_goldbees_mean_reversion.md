# Strategy 001 — GOLDBEES Intraday Mean Reversion

**Status:** 🔴 Rejected as a symmetric mean-reversion signal; continuation attribution in progress

## Research question

Does an unusually large short-term deviation of GOLDBEES from its recent intraday equilibrium tend to be followed by a statistically meaningful move back toward that equilibrium?

## Why GOLDBEES?

GOLDBEES is the first instrument selected for this strategy research because it is accessible for eventual small-account validation and allows us to study an intraday mean-reversion hypothesis without starting with derivatives. Its lower nominal unit price is useful for later capital-feasibility analysis, but **price alone is not evidence of profitability**. The strategy must first demonstrate an edge after realistic costs and execution assumptions.

## Research discipline

This experiment is deliberately an **event study before a trading backtest**. We will not optimize a trading rule until we establish whether the underlying relationship exists.

The sequence is:

1. Define the hypothesis before examining the result.
2. Measure the deviation using only information available at the event bar.
3. Measure future returns only after the event.
4. Keep forward returns within the same trading session.
5. Separate positive and negative deviations.
6. Report sample size and distribution, not only average return.
7. Record negative and inconclusive results rather than deleting them.
8. Only promote a hypothesis to a strategy after statistical and economic evidence justifies doing so.

## Experiment 001 — Baseline deviation event study

### Hypothesis

When GOLDBEES closes unusually far from its recent intraday mean, the subsequent return should tend to have the opposite sign if a short-term mean-reversion effect exists.

Formally, using a rolling lookback of `L` bars:

- equilibrium = rolling mean of close using the previous `L` completed bars;
- dispersion = rolling standard deviation of close using the previous `L` completed bars;
- deviation z-score = `(current_close - prior_mean) / prior_std`;
- positive deviation events are large positive z-scores;
- negative deviation events are large negative z-scores.

The initial implementation uses a configurable default lookback of **30 five-minute bars** and a configurable default absolute z-score threshold of **2.0**. These are research defaults, not optimized parameters and not a claim that they are optimal.

### Prediction target

For each event, calculate same-session forward close-to-close returns over:

- 1 bar = 5 minutes
- 3 bars = 15 minutes
- 6 bars = 30 minutes
- 12 bars = 60 minutes

For mean reversion, the important directional question is whether:

- positive deviation → negative subsequent return;
- negative deviation → positive subsequent return.

We therefore report both raw forward returns and **reversion-aligned returns**.

## Experiment 001 result

The GOLDBEES dataset contained **30,912 five-minute bars** from January 2025 through August 2026. The baseline event study produced **2,953 combined directional event observations** at the 2.0 z-score threshold.

The symmetric mean-reversion hypothesis was **not supported**. Reversion-aligned returns for all events were negative at every tested horizon:

| Horizon | Mean reversion-aligned return |
|---|---:|
| 5 min | -0.00365% |
| 15 min | -0.00901% |
| 30 min | -0.01703% |
| 60 min | -0.02105% |

The positive-deviation side was particularly notable: mean raw forward returns increased from approximately **+0.00764% at 5 minutes** to **+0.05577% at 60 minutes**. That is continuation, not reversion. Negative deviations were much weaker and inconsistent.

The raw all-event forward returns were also positive and increased with horizon, but this alone is **not evidence of a tradable momentum edge**. Events can cluster, forward horizons overlap, and GOLDBEES can exhibit persistent drift. The simple rolling mean of raw price may also be an imperfect equilibrium definition for a trending asset.

Exploratory t-statistics were calculated, but they must not be interpreted as definitive significance tests because event observations are not necessarily independent.

### Decision

**REJECTED as a symmetric mean-reversion signal.**

This is a research result, not a trading loss: the hypothesis was falsified enough that we should not turn it into a trading rule merely because another parameterization might look profitable.

## Experiment 001A — Event structure & conditioning diagnostics

001A tested whether the continuation-like behavior survived basic dependence controls and whether it was concentrated in predefined conditions. It used the same fixed 30-bar / 2.0-z-score baseline and a fixed 12-bar non-overlap diagnostic.

### Main findings

- Raw events were highly clustered; the fixed 12-bar non-overlap filter removed most of the clustering.
- Positive-deviation continuation remained visible after non-overlap filtering.
- The strongest concentration was positive deviation combined with an existing **upward six-bar prior trend**.
- Negative-deviation behavior was weaker and inconsistent.
- Volatility and volume did not provide a simple primary explanation.
- Late-session behavior and larger deviations were interesting exploratory concentrations, but no parameters were optimized from them.

### Decision

**Symmetric mean reversion remains rejected. Continuation is a promising exploratory lead, not an approved strategy.**

The key unresolved question is whether continuation contains information beyond ordinary intraday drift and the recent trend that was already present before the event.

## Experiment 001B — Continuation Attribution

001B is the next falsifiable experiment. It asks:

> **Does the continuation-like return after a large deviation contain information beyond ordinary intraday drift and the recent six-bar trend?**

It compares positive and negative deviations, prior-trend regimes, and predefined time-of-day buckets. The primary event set remains the fixed 12-bar non-overlapping events.

A descriptive non-event benchmark matches observations on predefined **time-of-day + prior-trend** buckets. This benchmark is used only to attribute the observed return; it is explicitly **not** a prospective trading signal because it is calculated over the full research sample.

Implementation:

```text
src/research/continuation_attribution.py
scripts/run_continuation_attribution.py
tests/test_continuation_attribution.py
research/journal/001B_continuation_attribution.md
```

Run locally:

```powershell
python scripts/run_continuation_attribution.py data/raw/NSE_GOLDBEES_5minute.csv
```

### Promotion rule

- **REJECTED:** continuation disappears relative to matched normal behavior or is not stable enough to justify further work.
- **INCONCLUSIVE:** evidence is interesting but insufficient.
- **PROMISING:** continuation survives the non-overlap check, remains coherent after trend/time conditioning, and shows an incremental relationship versus the matched non-event benchmark.

Even a **PROMISING** result does not make the strategy paper-ready. It would then require a separate trading specification, realistic costs/slippage, multi-instrument testing, and chronological out-of-sample/walk-forward validation.

## Current limitations

- No complete trading backtest has been approved.
- No transaction costs, spread, slippage, or order-execution model has yet been applied to a continuation strategy.
- No out-of-sample or walk-forward test has been performed.
- No live or paper deployment is justified at this stage.
- The original mean-reversion hypothesis remains rejected and will not be rewritten based on later results.
