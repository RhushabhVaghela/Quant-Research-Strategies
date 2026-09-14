# Strategy 001 — GOLDBEES Intraday Mean Reversion

**Status:** 🔬 Research — Experiment 001 pending local execution

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

### What would count as evidence?

A promising result would require more than a positive mean. We want to see:

- a meaningful number of independent events;
- consistent direction across related horizons;
- evidence in both deviation directions or a clearly explainable asymmetry;
- a distribution that is not dominated by a few observations;
- statistical evidence that is not obviously explained by noise;
- persistence across different periods and market conditions;
- eventual improvement after realistic transaction costs and slippage.

No fixed profitability threshold is declared in advance because economic significance depends on execution costs, turnover, capital usage, and the eventual trading implementation.

### Decision rule for Experiment 001

- **REJECTED:** evidence is inconsistent with the stated hypothesis or clearly too weak to justify further testing.
- **INCONCLUSIVE:** the effect may exist, but sample size, instability, or other limitations prevent a decision.
- **PROMISING:** evidence justifies a second experiment designed to test robustness rather than optimize the signal.

A promising event study is **not** a live-trading recommendation.

## Results

**Pending local execution.**

Run:

```powershell
python scripts/run_mean_reversion_event_study.py data/raw/NSE_GOLDBEES_5minute.csv
```

The script writes machine-readable results and charts under `data/reports/goldbees_mean_reversion/`.

## What we will record after execution

The next journal update will include:

- dataset period and number of sessions;
- event count overall and by direction;
- forward-return statistics by horizon;
- reversion-aligned return statistics;
- t-statistics and confidence intervals as exploratory diagnostics;
- event distribution and cumulative event outcome charts;
- limitations and possible sources of bias;
- the explicit decision: rejected, inconclusive, or promising;
- the next experiment, if justified.

## Promotion path

If Experiment 001 is promising, we will **not** immediately optimize thresholds. The next stage will investigate whether the effect survives across time periods and whether conditioning variables such as volatility, volume, time of day, or market regime explain the signal.

If Experiment 001 is rejected, the failure remains part of the research history. A new hypothesis may be proposed, but it must be documented separately rather than silently rewriting this experiment.
