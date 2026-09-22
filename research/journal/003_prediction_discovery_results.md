# Strategy 003 — Prediction Discovery Results and Characterization Entry

**Run:** current intraday discovery run  
**Date recorded:** 2026-09-22  
**Status:** 🟡 Discovery evidence; characterization initiated  
**Protected holdout:** untouched

## Discovery result

The completed Strategy 003 discovery run used:

- 15 eligible Indian equities;
- 39 registered model features including raw, rank and cross-sectional-z transforms;
- next-5-minute cross-sectional excess return;
- exploratory/development data through 2026-06-09;
- one-decision-timestamp chronological purging;
- zero baseline, OLS and fixed Ridge α=1.

The repository test suite passed with **135 tests** before this characterization stage.

## Main discovery observations

### Univariate information

The strongest positive base-feature relationships were concentrated in activity/volatility features, including one-bar volume change and trailing volume/range state.

The strongest negative base-feature relationship was `close_location_1bar`, with exploratory mean IC approximately **−0.0525** and mean rank IC approximately **−0.0599**.

`intraday_position_60bar` was also materially negative, with exploratory mean IC approximately **−0.0299** and mean rank IC approximately **−0.0345**.

These are descriptive exploratory results. Because 5-minute timestamps are serially dependent and transformed variants are not independent discoveries, the reported timestamp/date-level IC IR values are not interpreted as ordinary independent-sample significance measures.

### Frozen multivariate model

The OLS model produced:

| Split | Mean IC | Mean rank IC | Descriptive IC IR | Mean top-bottom spread |
|---|---:|---:|---:|---:|
| Validation within development | +0.0718 | +0.0660 | 5.53 | +2.01 bps |
| Development test | +0.0696 | +0.0826 | 4.87 | +2.22 bps |

Fixed Ridge α=1 was essentially identical:

| Split | Mean IC | Mean rank IC | Mean top-bottom spread |
|---|---:|---:|---:|
| Validation within development | +0.0718 | +0.0661 | +2.03 bps |
| Development test | +0.0696 | +0.0826 | +2.20 bps |

The similarity between OLS and Ridge means the first-pass result is not currently sensitive to the fixed regularization choice.

## Current interpretation

The development evidence is stronger than the earlier daily Strategy 003 experiment in one important respect: the model's predictive rank relationship did not collapse between the internal validation and development-test segments.

However, the evidence is **not a validated alpha result**.

The roughly 2.0–2.2 bps top-bottom diagnostic spread is before all real execution frictions and is not a strategy P&L measure. At a 5-minute decision frequency, turnover and implementation costs may dominate such an effect.

The current result therefore supports moving from predictive-information discovery into **descriptive characterization**, not into strategy construction or model escalation.

## Research lineage guardrail

The current feature set deliberately excludes the signed-return mechanisms owned by Strategies 001 and 002. Any later result that depends primarily on those mechanisms must be treated as evidence about the existing closed research lines rather than a new Strategy 003 mechanism.

## Next controlled stage

The next registered characterization investigates:

1. spread distribution and tail sensitivity;
2. quintile monotonicity;
3. time-of-day stability;
4. stock-level stability;
5. base feature-family ablations;
6. standardized coefficient decomposition;
7. OLS-vs-Ridge prediction agreement.

The final project validation and final holdout remain protected.

See `research/journal/003_prediction_discovery_characterization_protocol.md`.


## Controlled second characterization pass — implementation update

The first characterization production run showed that two requested diagnostics were not yet sufficiently observable:

1. the output contained only Q5-minus-Q1 spreads, so intermediate Q2–Q4 monotonicity could not be evaluated directly;
2. only the late-session time bucket appeared in the scored output, but the frozen 60-bar feature windows can remove early-session observations through complete-case requirements.

The characterization runner has therefore been extended without changing the frozen discovery model or protected data boundaries.

New outputs:

- `data/reports/strategy_003_prediction_characterization/quintile_returns.csv` — timestamp/model/Q1–Q5 realized next-bar excess returns;
- `data/reports/strategy_003_prediction_characterization/quintile_summary.csv` — aggregate return distribution by quintile;
- `data/reports/strategy_003_prediction_characterization/time_of_day_coverage.csv` — raw target rows versus frozen-model scored rows for all four registered time buckets;
- `time_of_day_stability.csv` now emits all four buckets, including explicit zero-observation/status rows.

The time-of-day coverage diagnostic is intentionally based on the full development-test target sample. It does not change the frozen 60-bar feature set or impute missing early-session features. Therefore any early-session scoring gap will be recorded as a feature-availability limitation rather than silently interpreted as absence of the predictive relationship.

### Evidence status

This implementation change does **not** establish quintile monotonicity or time-of-day stability by itself. Those conclusions require the regenerated outputs from the controlled characterization run.

No economic hypothesis, nonlinear model escalation, strategy construction, protected validation, or final holdout evaluation is authorized from this pass until the new outputs have been reviewed.
