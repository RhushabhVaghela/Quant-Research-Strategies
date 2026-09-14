# Strategy 001 — GOLDBEES Intraday Mean Reversion

**Status:** 🔴 Rejected as a symmetric mean-reversion signal; continuation diagnostics in progress

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

The next experiment is deliberately a **diagnostic stage, not parameter optimization**. Its purpose is to determine whether the continuation-like behavior is robust to basic dependence controls and whether it is concentrated in identifiable conditions.

The predefined diagnostics are:

1. **Event clustering / non-overlap:** retain the first event and suppress subsequent events for a fixed **12-bar cooldown**, equal to the longest tested horizon.
2. **Time of day:** compare predefined intraday periods.
3. **Recent trend:** classify the six-bar return before the event as down, flat, or up.
4. **Volatility regime:** compare the prior 30-bar realized-volatility regime against a trailing intraday reference.
5. **Volume regime:** compare event-bar volume with its prior 30-bar median.
6. **Event severity:** inspect the predefined `2.0–2.5`, `2.5–3.0`, and `3.0+` absolute-z-score bands.
7. **Directional continuation:** test whether positive-deviation continuation survives after removing overlapping event episodes.

The 12-bar cooldown is a **dependence diagnostic, not a tuned trading parameter**. No thresholds will be selected because they produce the best return.

Implementation is in:

```text
src/research/mean_reversion_diagnostics.py
scripts/run_mean_reversion_diagnostics.py
research/journal/001A_diagnostics_plan.md
```

Run locally:

```powershell
python scripts/run_mean_reversion_diagnostics.py data/raw/NSE_GOLDBEES_5minute.csv
```

The output directory is:

```text
data/reports/goldbees_mean_reversion_diagnostics/
```

## Current limitations

- The baseline event study is exploratory and not a complete trading backtest.
- Event clustering means the raw event count overstates the amount of independent evidence.
- Forward horizons overlap.
- The simple price-mean definition may mix trend and deviation effects.
- No transaction costs, spread, slippage, or order-execution model has been applied yet.
- No out-of-sample or walk-forward test has been performed.
- No live or paper deployment is justified at this stage.

## Promotion path

Only if Experiment 001A identifies a stable, economically interpretable continuation relationship will we create a **separate continuation hypothesis**. That hypothesis would then receive its own event study, baseline trading rule, cost model, out-of-sample test, and paper/shadow validation.

The original mean-reversion hypothesis remains permanently recorded as rejected rather than being rewritten after seeing the data.
