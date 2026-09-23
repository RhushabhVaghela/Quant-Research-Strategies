# Strategy 003 — Common-Support Nested Mechanism Comparison

**Status:** 🟡 Preregistered explanatory control — development-only.

## Purpose

The residual-family decomposition found different usable timestamp counts across models. This experiment removes that comparability problem.

For each comparison, the locked 003H mechanism and exactly one registered family extension are evaluated on the **same complete-case observations**. No family is selected, optimized, or promoted.

## Models

For each block:

1. mechanism: close_location_1bar, intraday_position_60bar, bars_since_session_open
2. mechanism + activity
3. mechanism + volatility
4. mechanism + market context

Each model is fit separately on the same common-support train/validation/development-test observations for that block. The one-bar chronological purge remains unchanged.

## Evaluation

Report:

- mean IC;
- mean rank IC;
- descriptive IC IR;
- positive IC fraction;
- Q1–Q5 realized excess returns;
- Q1–Q5 spread;
- incremental IC/rank IC/spread versus the mechanism on the identical support;
- usable timestamps and observations;
- time-of-day coverage.

The comparison is descriptive. It does not authorize selecting the best block.

## Decision discipline

A positive increment is evidence only that the added block contains information beyond the mechanism **on common support**. It is not evidence of tradability, cost resilience, causal mechanism, or validated alpha.

If market context remains incrementally positive, it may motivate a separately preregistered economic interpretation. If the increment disappears, the earlier apparent improvement is treated as a support-composition artifact.

No portfolio construction, threshold search, holding-period search, nonlinear model escalation, cost optimization, protected validation, or final holdout is allowed.

## Evidence boundary

Only the exploratory/development framework through **2026-06-09** may be used. Protected validation begins **2026-06-10** and final holdout begins **2026-08-20**.
