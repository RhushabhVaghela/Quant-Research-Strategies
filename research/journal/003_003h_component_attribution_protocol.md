# Strategy 003H Component Attribution Protocol

**Status:** 🟡 Preregistered explanatory experiment — development-only.

## Question

The common-support residual-family control found no demonstrable incremental information in activity, volatility, or market-context blocks beyond the locked 003H mechanism. The next question is therefore attribution within the three already-locked 003H variables.

## Locked variables

- close_location_1bar
- intraday_position_60bar
- bars_since_session_open

## Fixed specifications

Evaluate exactly:

1. close_location_1bar
2. intraday_position_60bar
3. bars_since_session_open
4. close_location_1bar + intraday_position_60bar
5. close_location_1bar + bars_since_session_open
6. intraday_position_60bar + bars_since_session_open
7. all three together as the locked 003H reference

## Method

Use the existing next-5-minute cross-sectional excess-return target, same universe, same development window, same one-decision-timestamp purge, and raw feature representations already present in the repository.

Each specification is fit independently using the existing OLS procedure. Report development validation and development-test IC, rank IC, descriptive IC IR, positive IC fraction, Q1–Q5 realized excess returns, and Q1–Q5 spread.

## Interpretation rule

This is **attribution, not feature selection**. The project must not choose a singleton or pair simply because it has a larger historical spread. The all-three model remains the preregistered 003H reference.

The experiment can answer whether the predictive ordering is broadly present in one component or requires a combination. It cannot establish causality, tradability, cost resilience, or validated alpha.

## Exclusions

No new features, transforms, lookbacks, interactions, thresholds, regimes, holding-period search, transaction-cost optimization, nonlinear models, protected validation, or final holdout.

## Evidence boundary

Exploratory/development data end **2026-06-09**. Protected validation begins **2026-06-10**. Final holdout begins **2026-08-20**.
