# Strategy 002 — Pattern Discovery Protocol

**Status:** Active research. No trading hypothesis selected.

## Purpose

Characterize the behavior present in the predefined Strategy 002 research universe before selecting an economic mechanism or trading rule.

This is an exploratory research phase. A discovered pattern is **not** an alpha claim, strategy, or deployment candidate.

## Locked data boundary

All decision-relevant pattern discovery in this phase is restricted to:

- exploratory development: **2025-09-18 through 2026-06-09**, inclusive.

The following periods are not available for pattern discovery:

- development validation: **2026-06-10 through 2026-08-19**;
- final holdout/OOS: **2026-08-20 through 2026-09-17**.

The downloaded CSVs may physically contain later observations. The analysis code must filter them out before calculating any decision-relevant statistic.

## Research-universe rule

Use the predefined `research/universe_candidates.csv` universe and the current structural-quality audit. Do not add/remove/rank instruments because of a pattern result.

HINDUNILVR currently has a structural-quality issue in the downloaded audit (one unexpected interval and five zero-volume rows). Until the underlying rows are inspected and the issue is resolved or explicitly excluded, it must not silently enter pattern comparisons as though it were clean.

## Existing repository resources reused

The discovery plan deliberately reuses concepts and prior work already present in the repository:

- `research/journal/research_methodology.md`
- `research/journal/repository_resource_policy.md`
- `research/journal/001J_universe_discovery_protocol.md`
- `research/journal/001J_cross_sectional_equity_spec.md`
- `trading_resources/Concepts/Financial-Time-Series-Analysis.md`
- `trading_resources/Concepts/Unsupervised-Learning-in-Trading.md`
- `trading_resources/Concepts/CORE_CONCEPTS_LIBRARY.md`
- existing data validation and historical-data utilities.

These resources are methodological building blocks, not validated Strategy 002 evidence.

## Predefined descriptive families

The first pass is intentionally broad but finite.

### 1. Return dynamics

For 5-minute close-to-close returns:

- lag autocorrelation for a small fixed set of lags;
- signed-return persistence versus reversal;
- absolute-return autocorrelation as a volatility-clustering diagnostic;
- return quantiles and tail frequency;
- cross-sectional comparison of these quantities.

The initial lag set is fixed at **1, 2, 3, 6, 12, and 24 bars**. It is a diagnostic set, not a parameter grid.

### 2. Forward-horizon behavior

For a fixed set of horizons:

- 1, 2, 3, 6, and 12 five-minute bars.

Measure unconditional forward returns and conditional forward returns after broad prior-return states:

- prior return sign;
- prior return magnitude bucket;
- recent multi-bar return sign.

The purpose is to distinguish whether the universe exhibits short-horizon continuation, reversal, or little directional predictability.

No trading thresholds or optimized entry/exit rules are selected here.

### 3. Intraday structure

For each bar position in the regular session:

- mean return;
- median return;
- mean absolute return;
- return dispersion;
- mean volume;
- median volume.

This identifies time-of-day structure without converting a time bucket into a trading filter.

### 4. Cross-sectional dependence

Using aligned 5-minute returns:

- pairwise correlation;
- daily-return correlation;
- covariance structure;
- cross-sectional average correlation;
- dispersion of same-time returns.

The analysis should distinguish common market movement from idiosyncratic movement.

### 5. Common-factor structure

On the aligned return panel:

- standardized return covariance/correlation;
- PCA explained variance ratios;
- cumulative variance of the first few components.

PCA is descriptive here. It must not be used to select securities or create a trading portfolio during this phase.

### 6. Lead-lag diagnostics

For a small fixed set of lags, calculate directional lead-lag correlations between instruments where timestamp coverage permits.

Because the universe mixes ETFs and equities, results must be interpreted as descriptive dependence, not automatically as arbitrage.

## Multiple-testing control

This pass contains multiple descriptive statistics by design. Therefore:

- results are exploratory;
- no single p-value or strongest statistic is treated as confirmation;
- no threshold is selected because it maximizes a result;
- no strategy is created from one attractive instrument/horizon;
- repeated follow-up searches must be recorded as additional research degrees of freedom;
- negative and inconclusive findings must be preserved.

If a pattern appears interesting, the next step is **pattern characterization and economic interpretation**, not immediate optimization.

## Data-quality handling

The pattern script must fail closed for:

- missing OHLCV columns;
- invalid/non-positive prices;
- invalid/negative volume;
- non-monotonic timestamps;
- duplicate timestamps.

Unexpected intervals and zero-volume observations are reported. A dataset with unresolved structural failures must not be silently presented as a clean cross-sectional observation set.

## Outputs

The first implementation should produce:

1. per-instrument return-dynamics diagnostics;
2. per-instrument forward-horizon diagnostics;
3. time-of-day diagnostics;
4. cross-sectional correlation/dispersion diagnostics;
5. PCA diagnostics;
6. a machine-readable run manifest identifying the input directory, allowed date range, instruments included/excluded, methodology version, and analysis timestamp.

No P&L, strategy parameter grid, or holdout statistic is produced by this workflow.

## Decision gate

After this pass, Strategy 002 remains hypothesis-free until the evidence is characterized across instruments, horizons, and market states.

Only a pattern that is:

- economically interpretable;
- not confined to one accidental observation;
- sufficiently repeatable within development data;
- compatible with execution/cost realities;
- and distinguishable from already-closed Strategy 001 mechanisms

should proceed to formal hypothesis definition.
\n## Execution status\n\nThe first locked exploratory pass has now been executed locally with 19 structurally eligible instruments and produced the prescribed diagnostic files. The next step is controlled characterization of those outputs. No hypothesis, strategy P&L, optimization grid, validation-period statistic, or holdout statistic has been introduced.\n