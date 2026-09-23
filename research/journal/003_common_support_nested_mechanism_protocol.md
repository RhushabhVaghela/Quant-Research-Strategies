# Strategy 003 — Common-Support Nested Mechanism Comparison

**Status:** ✅ Completed explanatory control — development-only; no strategy candidate.

## Purpose
The residual-family decomposition showed different usable timestamp counts across blocks. This experiment removed that comparability problem by evaluating the locked 003H mechanism and each one-family extension on identical complete-case observations.

## Results — development test

| Added block | Incremental mean IC | Incremental rank IC | Incremental Q1–Q5 spread |
|---|---:|---:|---:|
| Activity | **−0.00270** | **−0.00106** | **−0.155 bps** |
| Volatility | **−0.01602** | **−0.01294** | **−0.349 bps** |
| Market context | **+0.00047** | **+0.00125** | **−0.001 bps** |

The earlier apparent market-context improvement does not survive common-support control. The previous +0.00836 mean-IC increment was obtained on different observation support; on identical support the increment is effectively zero.

## Decision
- Activity: no demonstrated incremental predictive information beyond 003H.
- Volatility: no demonstrated incremental predictive information; the nested comparison is negative.
- Market context: prior apparent improvement is treated as a support-composition artifact.

These findings close these specific preregistered family extensions under the current Strategy 003 specification. They do not make universal claims about those feature families.

## Evidence boundary
Only the exploratory/development framework through **2026-06-09** was used. Protected validation begins **2026-06-10** and final holdout begins **2026-08-20**.

## Next experiment
The next controlled question is narrower than another family search: which of the three locked 003H variables accounts for the interpretable predictive structure, and does the relationship require their combination?

The next experiment will compare the three singletons, the three pairwise combinations, and the all-three 003H reference solely for attribution. It is not a performance-based feature-selection exercise. No new transforms, lookbacks, thresholds, interactions, holding periods, costs, nonlinear models, protected validation, or holdout usage are authorized.