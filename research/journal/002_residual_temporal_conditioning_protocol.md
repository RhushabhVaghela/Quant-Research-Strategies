# Strategy 002 — Residual Conditional Temporal Stability Protocol

**Status:** Controlled exploratory characterization. No trading hypothesis selected.

## Objective

The leave-one-out residual investigation established a broad next-bar residual reversal and showed that the effect is not primarily concentrated in the next bar's close-to-open boundary.

The remaining major gate is temporal stability.

This analysis directly measures whether the conditional residual reversal persists across chronological subperiods rather than using residual autocorrelation as a proxy.

## Locked sample

Use only:

- exploratory development: **2025-09-18 through 2026-06-09**;
- the same 19 structurally eligible instruments.

Do not use:

- validation: **2026-06-10 through 2026-08-19**;
- final holdout/OOS: **2026-08-20 through 2026-09-17**.

## Predefined chronological partitions

Split the exploratory observations into four chronological quartiles:

- Q1_time
- Q2_time
- Q3_time
- Q4_time

The partitions are chronological only. They are not selected because of performance.

## Measurements

Using the already-fixed leave-one-out residual construction:

1. For each instrument and chronological period, measure next-bar residual return conditional on:
   - prior residual < 0;
   - prior residual > 0.
2. Measure horizons:
   - 1 bar;
   - 2 bars;
   - 3 bars;
   - 6 bars;
   - 12 bars.
3. For the one-bar horizon, separately measure:
   - close-to-open residual;
   - open-to-close residual.
4. Report:
   - observation count;
   - mean;
   - median;
   - positive fraction.
5. Summarize breadth by period:
   - number of instruments;
   - median instrument mean;
   - Q25/Q75;
   - fraction of instruments with positive mean.

The construction, universe, and horizons are inherited from the previous leave-one-out analysis. No new threshold or parameter is introduced.

## Interpretation gates

The result should be considered temporally supportive only if the conditional reversal:

- remains directionally coherent across chronological periods;
- is not driven by one period or a small number of instruments;
- remains observable at a horizon that is realistically actionable;
- does not require selecting a favorable period after seeing the results.

A mixed or sign-changing chronological pattern should be recorded as unresolved rather than repaired through parameter changes.

## What this analysis does not do

It does not:

- select a z-score;
- choose an entry threshold;
- choose a holding period;
- select instruments;
- optimize portfolio weights;
- calculate strategy P&L;
- use transaction-cost assumptions for candidate selection;
- read validation or holdout observations.

## Reuse

This analysis reuses the fixed leave-one-out residual construction and the repository's existing chronological stability conventions. It is intentionally a narrow follow-up to the previous mechanism decomposition.

## Reproducible execution

Run:

    python scripts/characterize_strategy_002_residual_temporal_conditioning.py data/raw/strategy_002_universe --audit-report data/reports/strategy_002_universe_audit.csv --output-dir data/reports/strategy_002_residual_temporal_conditioning


## Controlled review step

After the temporal-conditioning runner completes, create the descriptive summary with:

    python scripts/summarize_strategy_002_residual_temporal_conditioning.py data/reports/strategy_002_residual_temporal_conditioning

The summary script refuses to proceed if the manifest indicates validation/holdout use, strategy P&L, or optimization. The chronological stability result must be reviewed before the fixed-baseline validation period is opened.
