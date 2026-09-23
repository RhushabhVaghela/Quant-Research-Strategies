# Strategy 003 — Residual Mechanism Decomposition Protocol

**Status:** 🟡 Preregistered explanatory decomposition — no strategy candidate, no protected validation, no holdout.

## 1. Purpose

003H showed that the locked bar-shape/intraday-state mechanism retains a positive next-bar cross-sectional relationship, but does not explain the full frozen discovery-model relationship.

The next question is narrowly defined:

> Which existing, economically distinct feature-family blocks contain incremental predictive information beyond the locked 003H mechanism, without reopening unrestricted feature search?

This is an explanatory decomposition, not a hunt for the highest-performing feature subset.

## 2. Locked base mechanism

Every comparison includes exactly these three raw mechanism features:

- `close_location_1bar`
- `intraday_position_60bar`
- `bars_since_session_open`

These features are frozen from 003H.

## 3. One-at-a-time residual blocks

Add exactly one registered family at a time:

### Activity
- `log_volume`
- `volume_change_1bar`
- `volume_z_12bar`
- `volume_z_60bar`

### Volatility
- `realized_vol_12bar`
- `realized_vol_60bar`
- `range_1bar`
- `range_z_60bar`

### Market context
- `market_return_1bar`
- `market_vol_60bar`

The market-context block is deliberately kept separate from the full discovery feature set. It remains an explanatory block, not a basis for an optimized model.

## 4. Transform policy

Use the existing raw representations only.

Do not add rank transforms, cross-sectional z-score transforms, new lookback lengths, interactions, thresholds, regime filters, feature selection, or nonlinear terms.

## 5. Model comparison

Evaluate:

1. zero baseline;
2. 003H mechanism OLS;
3. mechanism + activity;
4. mechanism + volatility;
5. mechanism + market context.

All model fits use the same chronological training/validation/development-test split and one decision-timestamp purge.

No model is selected as a final specification from the development-test results.

## 6. Required diagnostics

For every model report mean IC, mean rank IC, descriptive IC IR, positive IC fraction, mean top-minus-bottom spread, Q1–Q5 realized excess-return table, stock-level prediction/target correlations, time-of-day coverage, usable timestamps/observations, and incremental development-test metrics relative to the locked mechanism.

The incremental metrics are descriptive. No statistical threshold or family winner is declared in advance.

## 7. Evidence boundary

Use only the same exploratory/development framework through **2026-06-09**. Do not read protected validation beginning **2026-06-10** or final holdout beginning **2026-08-20**.

No portfolio P&L, turnover optimization, execution simulation, or cost grid is permitted.

## 8. Decision discipline

Possible outcomes:

- no material incremental contribution: keep 003 as an unresolved mechanism hypothesis;
- incremental contribution in one or more blocks: record the evidence and economic interpretation, but do not immediately combine, optimize, or trade the blocks;
- inconsistent decomposition: preserve the negative/inconclusive result and reconsider whether the original full-model relationship is sufficiently interpretable.

No family is selected because it has the largest observed development-test metric.

## 9. Lineage and implementation controls

The experiment remains distinct from Strategy 001 signed-return continuation and Strategy 002 peer-residual reversal.

The implementation must preserve the existing data audit, universe, target, split, purge, and transformations already used by Strategy 003.

Outputs must include a manifest documenting that holdout, parameter search, family selection, holding-period search, and cost optimization were not used.


## 10. Decomposition result — 2026-09-23

The one-family decomposition was completed successfully.

### Development-test results

| Model | Mean IC | Mean rank IC | Q1–Q5 spread |
|---|---:|---:|---:|
| 003H mechanism | +0.05849 | +0.07272 | +1.784 bps |
| Mechanism + activity | +0.05580 | +0.07166 | +1.630 bps |
| Mechanism + volatility | +0.05036 | +0.06587 | +1.524 bps |
| Mechanism + market context | +0.06685 | +0.08006 | +1.872 bps |

On the reported samples, activity and volatility reduced the development-test diagnostic relative to 003H, while market context increased it slightly. The reported incremental differences were:

- activity: mean IC **−0.00270**, rank IC **−0.00106**, spread **−0.155 bps**;
- volatility: mean IC **−0.00813**, rank IC **−0.00685**, spread **−0.261 bps**;
- market context: mean IC **+0.00836**, rank IC **+0.00734**, spread **+0.087 bps**.

### Critical comparability limitation

These model rows do **not** use identical observation support:

- mechanism/activity: **540** usable timestamps;
- volatility/market context: **504** usable timestamps.

The difference comes from the longer warm-up requirements of some added features. Therefore the raw incremental differences above cannot yet be interpreted as pure incremental information from the added family. A portion may arise from evaluating the models on different timestamps.

This is especially important for market context: its apparent improvement is small (**+0.087 bps spread**) and must not be treated as evidence that market context adds a real residual alpha component until a common-support comparison is completed.

### Interpretation

The decomposition does not reveal a large obvious residual feature family. The locked 003H mechanism remains positive, while adding activity or volatility does not improve the reported development-test diagnostics. Market context is the only block with a positive reported increment, but the support mismatch prevents a clean attribution.

The appropriate next experiment is therefore **not** another feature search. It is a common-support nested comparison that evaluates the locked mechanism and each one-family extension on exactly the same observations. This will separate genuine incremental information from sample-composition effects.

Protected validation and final holdout remain untouched.
