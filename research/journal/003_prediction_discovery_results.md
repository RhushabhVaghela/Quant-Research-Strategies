# Strategy 003 — Prediction Discovery Results and Characterization Entry

**Run:** current intraday discovery run  
**Date recorded:** 2026-09-23  
**Status:** 🟡 Provisional economic hypothesis; mechanism test next  
**Protected validation:** untouched  
**Final holdout:** untouched

## Discovery result

The completed Strategy 003 discovery run used:

- 15 eligible Indian equities;
- 39 registered model features including raw, rank and cross-sectional-z transforms;
- next-5-minute cross-sectional excess return;
- exploratory/development data through 2026-06-09;
- one-decision-timestamp chronological purging;
- zero baseline, OLS and fixed Ridge α=1.

The active work remains within the exploratory/development sample.

## Discovery evidence

The frozen OLS model produced a development-test mean IC of **+0.0696**, mean rank IC of **+0.0826**, and mean top-minus-bottom quintile spread of approximately **+2.22 bps**. Fixed Ridge α=1 was essentially identical.

The strongest negative univariate relationships were `close_location_1bar` and `intraday_position_60bar`, while positive univariate relationships were concentrated in activity/volatility state variables. These are exploratory relationships, not independent significance claims.

## Characterization evidence

### Q1–Q5 ordering

The regenerated quintile summary shows a coherent endpoint ordering:

| Prediction quintile | OLS mean next-bar excess return |
|---|---:|
| Q1 | **−1.1230 bps** |
| Q2 | **−0.1004 bps** |
| Q3 | **−0.1497 bps** |
| Q4 | **+0.2794 bps** |
| Q5 | **+1.0937 bps** |

Q1-to-Q5 is therefore about **+2.217 bps**. The intermediate buckets are not perfectly monotonic because Q3 is slightly below Q2, but the endpoints and direction are coherent: low predictions are associated with negative average next-bar excess returns and high predictions with positive average next-bar excess returns.

This should be described as **broad directional ordering with a small non-monotonic middle**, not strict monotonicity.

The same structure appears for fixed Ridge.

### Tail sensitivity

For OLS:

- raw mean spread: **+2.2168 bps**;
- median spread: **+2.6083 bps**;
- raw standard deviation: **10.8615 bps**;
- winsorized mean: **+2.2947 bps**;
- positive-spread fraction: **61.31%**;
- top 5% absolute-observation contribution: about **1.53 bps per timestamp**.

The winsorized mean is very close to the raw mean, so the average separation does not appear to be created by a tiny set of extreme timestamps. The distribution is nevertheless noisy: the standard deviation is several times larger than the mean.

### Feature-family decomposition

Development-test mean top-minus-bottom spreads:

| Feature family | OLS mean spread |
|---|---:|
| Activity | **+0.2125 bps** |
| Volatility | **+0.9845 bps** |
| Bar shape / intraday state | **+1.7537 bps** |
| Market context | **−0.0952 bps** |

The largest descriptive contribution comes from bar-shape/intraday-state variables, followed by volatility. Market context alone is approximately zero/negative in this diagnostic.

This is an ablation finding, not authorization to choose the bar-shape family as the final model.

### Stock breadth

Prediction/target correlations are small and mixed across the 15 equities. The largest positive stock-level correlation is about **+0.127** for SUNPHARMA; several stocks are near zero or negative. This argues against a single-stock explanation but does not yet demonstrate strong stock-by-stock stability.

The appropriate interpretation is **broadly distributed but individually weak cross-sectional evidence**.

### Time-of-day coverage

The registered four session buckets are present in the coverage audit. However, the frozen 60-bar rolling features remove the early-session observations from the scored model sample. The current `time_of_day_stability.csv` therefore cannot be used to claim that the effect is stable across all four session segments.

This is a feature-availability limitation of the frozen discovery design, not evidence that the signal is absent early in the session. The 60-bar feature set must not be changed merely to manufacture early-session coverage.

### OLS versus Ridge

Prediction correlation is approximately **0.9999999**. The two models therefore provide essentially the same score ordering under the fixed α=1 regularization.

There is no current evidence that model complexity or stronger regularization is needed.

## Interpretation

The characterization now supports a provisional economic interpretation:

> **Intrabar price location and recent intraday state may contain short-horizon cross-sectional information because the current bar may encode temporary imbalance in price discovery/positioning that persists into the next bar rather than being fully resolved at the decision close.**

This remains a hypothesis, not a claim of causality.

The current registered feature set does not explicitly reproduce the signed-return event mechanisms owned by Strategies 001 and 002. The mechanism still has to be tested against those lineage boundaries.

## Current decision

**🟡 Advance from characterization to a controlled economic-mechanism test.**

Do not yet:

- use protected validation;
- use the final holdout;
- build a trading strategy;
- optimize thresholds;
- search holding periods;
- run a transaction-cost grid;
- add XGBoost or neural networks;
- select a final feature subset;
- treat +2.2 bps as strategy P&L.

The gross effect remains small enough that later execution economics could still eliminate it.

## Next registered experiment

See `research/journal/003_prediction_hypothesis_protocol.md`.

The next test is **003H — Mechanism decomposition**:

1. compare the frozen full model with a simple preregistered bar-shape/intraday-state specification;
2. test whether the predictive ordering survives in that interpretable representation;
3. check that the mechanism is distinct from the closed 001 continuation and 002 residual-reversal lines;
4. use the same development-only predictive diagnostics;
5. do not change the protected validation or holdout boundaries.

Only if that mechanism remains coherent should the program consider strategy definition and later controlled validation.
