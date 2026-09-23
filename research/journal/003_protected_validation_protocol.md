# Strategy 003 — Protected Validation Protocol

**Status:** Drafted for decision gate only — not yet an executed validation.

## 1. Purpose

Strategy 003 has completed its authorized development-stage discovery, characterization, mechanism decomposition, common-support control, component attribution, lineage separation, and economic-form decomposition.

The remaining evidence question is whether a frozen explanatory form survives the project's protected chronological validation period without any retuning.

## 2. What is frozen before validation

If the project proceeds, the candidate must be frozen **before reading validation results**. The candidate specification registered for this protocol is:

- universe: the same 15 eligible equities used in the development research;
- horizon: next 5-minute cross-sectional excess return;
- signal information: `close_location_1bar` and `intraday_position_60bar` only;
- model: additive OLS with the training-only standardization already used in development;
- no interaction term;
- no thresholds;
- no holding-period search;
- no nonlinear model;
- no cost-based parameter changes;
- no universe changes.

Close-location-only is retained as an explanatory finding, but it is **not** substituted into this protected-validation protocol after seeing development results.

## 3. Protected boundary

- development evidence ends 2026-06-09;
- protected validation begins 2026-06-10;
- final holdout begins 2026-08-20;
- final holdout remains untouched even during protected validation.

Validation results must not be used to alter the feature set, model, universe, threshold, horizon, or execution specification.

## 4. Evaluation

Report:

- mean IC;
- rank IC;
- timestamp-level IC distribution;
- Q1–Q5 realized next-bar excess returns;
- Q1–Q5 spread;
- stock breadth;
- time coverage actually available under the frozen 60-bar feature definition;
- comparison with the frozen development reference;
- dependence/overlap diagnostics appropriate to intraday timestamps.

Do not treat descriptive IC IR as an independent-observation significance statistic. Adjacent intraday observations can be dependent.

## 5. Decision gate

Protected validation is not a promise of promotion.

If the frozen model preserves the direction and economically meaningful magnitude of the development relationship without requiring rescue rules, the project may proceed to a separately registered **economic execution/cost test**.

If the protected validation substantially weakens or reverses the relationship, Strategy 003 is closed for the current research line and the holdout remains untouched.

If the result is ambiguous, the correct action is to record the ambiguity and avoid rescue tuning.

## 6. Prohibited rescue actions

After validation results are visible, do not:

- change the feature set;
- replace additive OLS with the interaction form;
- switch to close-location-only;
- alter the universe;
- alter the horizon or holding period;
- tune thresholds;
- change the cost model to improve the result;
- inspect the final holdout to explain the validation result;
- reopen Strategies 001 or 002.

## 7. Evidence boundary

This file defines the next controlled gate. It does not claim that protected validation has been run. The final holdout remains completely untouched.