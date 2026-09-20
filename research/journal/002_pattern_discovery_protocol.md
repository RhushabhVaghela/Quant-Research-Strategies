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
## Pattern-characterization stage

The first exploratory summary surfaced two broad descriptive features that warrant characterization rather than immediate strategy selection:

1. short-lag signed-return autocorrelation is slightly negative at lag 1 and becomes mildly positive at longer lags;
2. absolute-return autocorrelation is consistently positive, indicating volatility clustering in the descriptive sample.

The conditional forward-return tables also show differences after prior positive versus prior negative returns. These observations are **not yet a hypothesis** and are not sufficient to call a tradeable reversal or volatility strategy.

The next controlled analysis therefore measures:

- breadth across instruments rather than the cross-sectional median alone;
- sign-conditioned behavior crossed with return-magnitude quartiles;
- stability across chronological subperiods inside the exploratory sample;
- whether the apparent short-horizon reversal survives after separating return sign from return magnitude;
- whether the pattern is broad enough to justify an economic interpretation;
- whether the mechanism is plausibly distinct from Strategy 001's continuation mechanism.

This characterization remains restricted to **2025-09-18 through 2026-06-09**. No validation or holdout observation is read.

A pattern will not advance merely because its average return is positive or negative. Advancement requires breadth, stability, an economically coherent mechanism, and a plausible path to surviving execution costs.

## Characterization execution control

The characterization stage uses the same structural universe-audit gate as the initial discovery pass. The audit report is therefore an explicit input to the characterization command; instruments with unresolved unexpected intervals or zero-volume rows are excluded rather than silently included.

Local execution:

    python scripts/characterize_strategy_002_patterns.py data/raw/strategy_002_universe --audit-report data/reports/strategy_002_universe_audit.csv --output-dir data/reports/strategy_002_pattern_characterization

The characterization loader accepts the full downloaded history as input, then slices it to the locked exploratory window. It must not reject a file merely because the file physically contains observations before the exploratory start date; only observations inside the locked window are decision-relevant.


## Characterization finding and next gate

The committed characterization now shows a broad **1–2 bar signed-return reversal pattern** across the 19 eligible instruments. At the next-bar horizon, 84.2% of instruments have a positive mean after a negative prior return, while only 5.3% have a positive mean after a positive prior return. The effect becomes less uniform at longer horizons.

This is strong enough to justify a mechanism investigation, but it is **not** yet sufficient to define a trading hypothesis. In particular, the current OHLCV data cannot distinguish economic short-horizon reversal from bid/ask bounce, price discretization, or bar-boundary effects.

The formal next step is documented in:
- `research/journal/002_pattern_characterization_findings.md`
- `research/journal/002_reversal_mechanism_protocol.md`

The mechanism characterization will remain inside the exploratory window and will decompose the next bar into close-to-close, close-to-open, and open-to-close components before any threshold, holding period, strategy rule, or validation-period evaluation is introduced.


## Reversal mechanism decision

The subsequent decomposition found that the broad raw-return reversal is concentrated in the prior-close to next-open component, while next-open to next-close does not preserve the same directional effect. The project therefore does not promote the raw reversal observation into a strategy. See research/journal/002_reversal_mechanism_findings.md. The next exploratory investigation is cross-sectional residual behavior, documented in research/journal/002_cross_sectional_residual_protocol.md.


## Cross-sectional residual finding and control

The first residual investigation found a broad next-bar residual reversal: after negative residuals, the median instrument mean next-bar residual was +3.7147 bps with 94.7% of instruments positive; after positive residuals, the median was -4.2457 bps with 0% positive. The effect weakened materially beyond the first bar and did not produce a monotonic magnitude relationship.

These results remain descriptive. The implementation subtracts the contemporaneous equal-weight cross-sectional mean including the instrument itself, so the residual specification is not yet sufficiently strict for hypothesis formation. In addition, the earlier raw-return decomposition showed a close-to-open boundary concentration. The project therefore does not promote the residual result into a trading rule.

The next controlled investigation uses a **leave-one-out cross-sectional residual** and separately decomposes close-to-close, close-to-open, and open-to-close components. It is documented in:

- `research/journal/002_cross_sectional_residual_findings.md`
- `research/journal/002_cross_sectional_residual_mechanism_protocol.md`

Execution:

    python scripts/run_strategy_002_leave_one_out_residual.py data/raw/strategy_002_universe --audit-report data/reports/strategy_002_universe_audit.csv --output-dir data/reports/strategy_002_leave_one_out_residual

This remains exploratory only. Validation and holdout data stay locked, and no strategy P&L or optimization is introduced.

## Leave-one-out mechanism result and next gate

The leave-one-out analysis strengthens the residual-reversal observation:

- prior negative residual → next-bar residual: median **+3.92 bps**, positive in **94.7%** of instruments;
- prior positive residual → next-bar residual: median **−4.48 bps**, positive in **0%** of instruments;
- the effect is weaker by two bars and inconsistent at longer horizons;
- for prior negative residuals, both close-to-open (**+2.13 bps**) and open-to-close (**+2.17 bps**) components contribute materially;
- for prior positive residuals, close-to-open (**−2.45 bps**) and open-to-close (**−0.95 bps**) components both point in the reversal direction.

Thus the effect survives leave-one-out construction and is not primarily a close-to-open boundary artifact.

However, the existing temporal-stability output measures residual autocorrelation rather than the conditional reversal itself, and lag-1 residual autocorrelation becomes materially more mixed in the fourth chronological quartile. The temporal stability gate therefore remains unresolved.

Findings are recorded in `research/journal/002_leave_one_out_residual_findings.md`.

The next controlled analysis directly measures the sign-conditioned residual reversal separately in four chronological subperiods, including boundary components. No economic hypothesis or optimization is introduced until that gate is evaluated.
