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

## Result and decision — 2026-09-23

The preregistered attribution run completed successfully with 151 repository tests passing before execution. The seven specifications were evaluated on the development-only sample; protected validation and final holdout remained untouched.

### Development-test results

| Specification | Mean IC | Mean rank IC | Q1–Q5 spread |
|---|---:|---:|---:|
| close_location_1bar | +0.04107 | +0.04799 | +0.930 bps |
| intraday_position_60bar | +0.00265 | +0.02668 | +0.184 bps |
| bars_since_session_open | not scored | not scored | not scored |
| close_location_1bar + intraday_position_60bar | +0.05849 | +0.07274 | +1.787 bps |
| close_location_1bar + bars_since_session_open | +0.04107 | +0.04799 | +0.930 bps |
| intraday_position_60bar + bars_since_session_open | +0.00265 | +0.02668 | +0.184 bps |
| all three | +0.05849 | +0.07272 | +1.784 bps |

The close-location + intraday-position pair reproduces the all-three reference essentially exactly on the pair's/all-three's 540-timestamp support. The development-test differences versus all-three are approximately −0.0000035 mean IC, +0.0000198 rank IC and +0.003 bps Q1–Q5 spread.

The close-location singleton carries a substantial standalone component, while intraday position alone is weak. Adding the session-clock variable does not change the scored pair results. The session-clock singleton has zero scored timestamps under the frozen availability design, so the experiment does not test a general time-of-day hypothesis.

### Decision

The attribution question is sufficiently answered to simplify the provisional 003H interpretation: the predictive structure is concentrated in the combination of current-bar close location and 60-bar intraday position. The session-clock variable is closed under the current specification.

This remains attribution, not feature selection. The two-variable pair is therefore **not** promoted to a trading strategy, and no protected validation, holdout, threshold search, holding-period search, nonlinear escalation, cost optimization, or portfolio construction is authorized by this result.

The next registered work should test whether this two-variable explanatory core is economically distinct from the previously closed Strategy 001 and Strategy 002 mechanisms. That follow-up must be preregistered and remain development-only unless a later gate explicitly authorizes protected validation.


## Current status correction — 2026-09-23

The historical next-step language in this attribution record is superseded by the completed lineage-separation and economic-form decomposition experiments. Attribution remains a historical explanatory result. The current Strategy 003 decision gate is documented in `003_protected_validation_protocol.md`; protected validation has not been executed.