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


## 003H mechanism decomposition result

The preregistered 003H test was completed using only the development framework. The three-feature mechanism model retained a positive next-bar cross-sectional relationship:

- development-test mean IC: **+0.0585**
- development-test mean rank IC: **+0.0727**
- development-test Q1-to-Q5 spread: **+1.78 bps**
- frozen full-model development-test spread: **+2.22 bps**

The mechanism quintiles were Q1 **−0.6272**, Q2 **−0.6268**, Q3 **−0.2214**, Q4 **+0.3182**, Q5 **+1.1572** bps. This is broad directional ordering with a non-monotonic middle, not strict monotonicity.

The result supports the view that the locked intrabar/intraday-state variables contain a meaningful component of the discovery relationship, but they do not account for all of it. The residual contribution is unresolved; it is not assigned retrospectively to activity, volatility or market context.

The explicit lineage audit found no direct 001 signed-return or 002 peer-residual encoding in the three locked variables. This is a feature-definition distinction, not proof of complete economic independence.

Both 003H mechanism and full-model scoring have zero observations before 14:00 because the frozen 60-bar features require a long warm-up. Therefore all-day stability remains untested and the late-session result must not be interpreted as an intrinsic afternoon effect.

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


## Residual decomposition — 2026-09-23

The preregistered one-family decomposition was completed on the development-only sample.

Development-test diagnostics:

| Model | Mean IC | Mean rank IC | Q1–Q5 spread |
|---|---:|---:|---:|
| 003H mechanism | +0.05849 | +0.07272 | +1.784 bps |
| + activity | +0.05580 | +0.07166 | +1.630 bps |
| + volatility | +0.05036 | +0.06587 | +1.524 bps |
| + market context | +0.06685 | +0.08006 | +1.872 bps |

The apparent increments relative to the mechanism were −0.155 bps for activity, −0.261 bps for volatility, and +0.087 bps for market context in Q1–Q5 spread.

However, the mechanism/activity models have 540 usable timestamps while volatility/market-context models have 504. Therefore these differences are not yet clean nested comparisons. The current result supports no conclusion that market context adds genuine incremental predictive information. A common-support nested comparison is required before interpreting the residual component.

No protected validation or final holdout data were used.


## 10. Common-support residual-family control — result and closure (2026-09-23)

The common-support nested comparison was completed on identical complete-case observations within each feature-family block. The development-test incremental results were: activity **−0.00270 mean IC**, **−0.00106 rank IC**, **−0.155 bps Q1–Q5 spread**; volatility **−0.01602 mean IC**, **−0.01294 rank IC**, **−0.349 bps**; market context **+0.00047 mean IC**, **+0.00125 rank IC**, **−0.001 bps**. The earlier apparent market-context increment therefore does not survive common-support control.

**Decision:** close these three residual-family branches under the current specification. Strategy 003 remains active because the locked 003H mechanism itself retains positive development-test ordering. The next experiment is restricted to component attribution within the three 003H raw variables, with no new features, transforms, or performance-based subset selection.


## 11. 003H component attribution — result and closure (2026-09-23)

The preregistered seven-specification component attribution experiment was completed on the development-only sample. The test compared the three locked 003H variables individually, in all pairwise combinations, and together as the fixed all-three reference. No protected validation or final holdout observations were used.

### Development-test attribution

| Specification | Mean IC | Mean rank IC | Q1–Q5 spread |
|---|---:|---:|---:|
| `close_location_1bar` | +0.04107 | +0.04799 | +0.930 bps |
| `intraday_position_60bar` | +0.00265 | +0.02668 | +0.184 bps |
| `bars_since_session_open` | not scored | not scored | not scored |
| close location + intraday position | +0.05849 | +0.07274 | +1.787 bps |
| close location + session clock | +0.04107 | +0.04799 | +0.930 bps |
| intraday position + session clock | +0.00265 | +0.02668 | +0.184 bps |
| all three | +0.05849 | +0.07272 | +1.784 bps |

The central attribution result is that the **close-location + intraday-position pair reproduces the all-three 003H reference essentially exactly** on the 540-timestamp common support used by the pair/all-three specifications. Relative to the all-three reference, the pair differs by about −0.0000035 mean IC, +0.0000198 rank IC and +0.003 bps in Q1–Q5 spread.

The `close_location_1bar` singleton already carries a substantial part of the development-test ordering (+0.930 bps spread). `intraday_position_60bar` alone is much weaker (+0.184 bps spread). Adding the session-clock variable produces no measurable incremental change in either pair containing it. The session-clock singleton itself has zero scored timestamps because the frozen within-session 60-bar availability constraints leave no usable variation/support for that specification; this must not be interpreted as evidence that time-of-day is economically irrelevant in general.

### Interpretation

The attribution experiment therefore simplifies the provisional 003H economic interpretation: the observed development-test predictive structure is primarily concentrated in the combination of **current-bar close location** and **recent 60-bar intraday position**. The registered session-clock feature is not needed to reproduce the frozen 003H diagnostic on the tested support.

This is an explanatory attribution result, **not feature-selection evidence**. The pair is not promoted simply because it matches the all-three development result. The result does not establish causality, tradability, transaction-cost resilience, or protected out-of-sample persistence.

### Decision

**Decision: keep Strategy 003 active; close the session-clock branch under the current frozen specification; treat the two-variable close-location/intraday-position pair as the provisional explanatory core of 003H.**

The project should not yet:

- select the pair as a final trading model;
- use the protected validation period;
- use the final holdout;
- optimize thresholds or holding periods;
- run nonlinear model escalation;
- optimize transaction costs or execution;
- construct a portfolio.

The next controlled question should be **mechanism falsification and lineage separation of the two-variable core**: determine whether its predictive information is economically distinct from the previously closed Strategy 001 continuation and Strategy 002 residual-reversal mechanisms, without reopening an unrestricted feature search. The development-only evidence boundary remains unchanged.



## 12. 003H lineage separation — preregistered next experiment (2026-09-23)

The component attribution result narrowed the provisional 003H explanatory core to `close_location_1bar + intraday_position_60bar`. The next experiment therefore tests whether this core is economically distinct from the already-closed Strategy 001 continuation and Strategy 002 residual-reversal mechanisms.

This is a **lineage falsification experiment**, not a new feature search. Exactly five fixed specifications are registered:

1. 003H core;
2. Strategy 001 frozen event proxy;
3. Strategy 002 leave-one-out prior residual;
4. both old-mechanism proxies together;
5. 003H core plus both old-mechanism proxies.

The Strategy 001 proxy uses its frozen event definition (`z_score >= 2.0` and `prior_return_6bar > 0`). The Strategy 002 proxy uses the prior-bar leave-one-out close-to-close residual across the eligible universe. All variables are point-in-time.

The experiment will use the same development-only sample, target, one-bar purge and 003H common-support principle. It must not access the protected validation period or final holdout, and it must not search thresholds, holding periods, new features, costs, nonlinear models or portfolio rules.

The key decision is whether the 003H core retains predictive information conditional on the old mechanisms. If it does, the evidence supports keeping 003H as a distinct information-source hypothesis; if the old mechanisms explain most of the signal, 003H should be treated as overlapping lineage rather than new alpha. Either outcome remains pre-strategy evidence and does not authorize protected validation automatically.

Registered implementation: `scripts/run_strategy_003h_lineage_separation.py`.


## 13. 003H lineage separation — result and decision (2026-09-23)

The preregistered lineage-separation experiment was completed on the development-only sample using exactly five fixed specifications. The user reran the repository locally after pulling the implementation: **155 tests passed**, the runner completed for **15 eligible equities**, and the outputs were uploaded to the repository.

### Development-test result

| Model | Mean IC | Rank IC | Q1–Q5 spread |
|---|---:|---:|---:|
| 003H core | **+0.05849** | **+0.07274** | **+1.787 bps** |
| 001 lineage | **+0.00991** | **+0.01842** | **+0.013 bps** |
| 002 lineage | **+0.02801** | **+0.04038** | **+0.644 bps** |
| 001 + 002 lineage | **+0.02815** | **+0.04059** | **+0.638 bps** |
| 003H + 001 + 002 | **+0.05577** | **+0.06774** | **+1.848 bps** |

Both the standalone 003H core and the combined model use the same **540 development-test timestamps / 8,100 observations**. Adding both old mechanisms changes mean IC only from **+0.05849 to +0.05577**, while the Q1–Q5 spread remains positive (**+1.787 vs +1.848 bps**).

The lineage-only models have different, broader support and are therefore context diagnostics rather than identical-support nested comparators.

### Internal validation diagnostic

The internal chronological validation split gives mean IC **+0.07059** for 003H and **+0.05852** for the combined model, with combined Q1–Q5 spread **+1.871 bps**. This is not the project-level protected validation beginning 2026-06-10.

### Decision

The lineage test provides evidence against **direct representational duplication** of the frozen 001 and 002 mechanisms. The old registered mechanisms do not explain away the 003H relationship.

Accordingly, the 001/002 overlap branch is closed under the frozen definitions; Strategy 003 remains active as a distinct but unvalidated intraday prediction hypothesis; Strategies 001 and 002 remain closed; and no strategy candidate is frozen.

This result does not establish causal independence, profitability, cost resilience, alternative-universe robustness, or protected out-of-sample persistence.

### Next controlled question

Move to **economic-form decomposition of the 003H two-variable core** using a finite preregistered representation set and common-support control. Do not reopen 001/002 or perform unrestricted feature, threshold, holding-period, cost, nonlinear, portfolio, validation, or holdout search.
## 14. 003H economic-form decomposition — result and final exploratory closure (2026-09-23)

The final preregistered development-stage decomposition was completed on common support using exactly four fixed specifications. The interaction branch did not produce a materially different predictive structure from the additive core.

| Specification | Dev-test Mean IC | Dev-test Rank IC | Dev-test Q1–Q5 spread |
|---|---:|---:|---:|
| close-location only | **+0.08419** | **+0.09205** | **+2.358 bps** |
| intraday-position only | **+0.00309** | **+0.02768** | **+0.219 bps** |
| additive core | **+0.05928** | **+0.07355** | **+1.780 bps** |
| joint interaction | **+0.06070** | **+0.07258** | **+1.871 bps** |

The fixed interaction changes the additive development-test result by only +0.00142 mean IC and +0.090 bps Q1–Q5 spread, while rank IC slightly decreases by 0.00097. The interaction coefficient on standardized inputs is approximately +1.96e-05. Validation shows the same qualitative pattern, so there is no compelling evidence for a distinct joint interaction mechanism under the registered form.

The strongest descriptive relationship in this decomposition is the current-bar close-location variable by itself. That finding is retained as explanatory evidence only; it is **not** a post-hoc feature-selection result and does not authorize replacing the frozen 003H core and treating the replacement as if it had been validated.

### Final development-stage decision

**Strategy 003 has completed its authorized exploratory decomposition.** The joint-interaction branch is closed. The remaining evidence is most consistent with a simple close-location-dominant/additive interpretation, but the gross magnitude remains small and no final trading model has been selected.

Protected validation beginning 2026-06-10 and final holdout beginning 2026-08-20 remain untouched. No further feature-family, transform, interaction, threshold, holding-period, cost, nonlinear, portfolio, or lineage search is authorized under this research line.

### Next gate

The next step is a hard promotion/closure decision: either freeze a narrowly specified explanatory form and register a protected-validation experiment, or close Strategy 003 as insufficient for further work. This decision must be made before reading or using the protected validation period.

Protocol: `research/journal/003h_economic_form_decomposition_protocol.md`.

## 15. Current gate after exploratory closure — 23 September 2026

The development-stage exploratory sequence is complete. The next experiment is now **protected validation of the frozen additive 003H form**, not another decomposition.

Frozen form: close_location_1bar + intraday_position_60bar, additive OLS, training-only standardization, same 15-stock universe, next 5-minute cross-sectional excess return.

Protected validation window: 2026-06-10 through 2026-08-19. Final holdout: 2026-08-20 onward, untouched.

If prediction survives, proceed to the preregistered economic execution viability protocol. If prediction fails, close Strategy 003 without rescue tuning.

The historical 5-bps sensitivity is no longer described as a universal realistic cost. Current published NSE/broker fees can already exceed 5 bps at ordinary retail notionals before spread, slippage and market impact. See `003_execution_cost_basis_research_20260923.md`.

## 16. Protected validation — result and promotion to economic testing (2026-09-23)

The frozen additive 003H candidate was executed once on the protected period **2026-06-10 through 2026-08-19**.

| Metric | Development reference | Protected validation |
|---|---:|---:|
| Mean IC | +0.0696 | **+0.08136** |
| Mean rank IC | +0.0826 | **+0.10082** |
| Q1–Q5 spread | +2.2168 bps | **+1.6870 bps** |
| Positive IC fraction | — | **60.76%** |
| Timestamps | — | **711** |
| Observations | — | **10,665** |

Protected Q1–Q5 returns were Q1 **−0.8952**, Q2 **−0.3388**, Q3 **−0.1837**, Q4 **+0.6259**, Q5 **+0.7918 bps**.

The protected spread retains about **76%** of the development-test magnitude and direction is preserved. Mean IC and rank IC are also above their development references. Under the preregistered decision rule, this advances the research from predictive validation to economic execution testing.

A major limitation remains: all protected scored timestamps are late-session, approximately **14:10–15:20 IST**, because of the frozen 60-bar warm-up. This is not interpreted as an intrinsic afternoon effect and is not used to select a narrower trading window.

**Current decision: Strategy 003 passes the protected prediction gate. The next authorized stage is the frozen economic execution viability test.**

No final-holdout data were used.

## 14. Economic execution implementation correction — 24 September 2026

Before economic results are accepted, the execution runner was corrected after code audit. The superseded prototype used normalized unit notionals for brokerage and hard-coded fully refreshed 2× turnover, and it did not operationally flag the late-session closing-auction regime.

The corrected runner now uses an explicit rupee portfolio notional (default ₹1,00,000), per-executed-order brokerage with the ₹20 cap, actual position-change turnover plus explicit final closure, and late-session / potential Closing Auction Session flags. The frozen Q5-long/Q1-short portfolio construction, one-bar horizon, protected-validation-only evidence boundary, and pre-registered cost scenarios are unchanged.

**Status:** no economic decision may use the superseded outputs; rerun the corrected implementation first.

## 15. Economic execution run invalidated — 24 September 2026

The first attempted economic execution run is **not valid evidence**. It reported ₹53,091.53 of fees and 1,060.333× cumulative turnover for a ₹1,00,000 portfolio notional, reflecting an implementation/accounting problem rather than a Strategy 003 economic result.

The implementation was corrected to separate cumulative portfolio return from cumulative executed turnover, compound the one-bar portfolio returns, and apply brokerage/statutory/execution costs to actual order-level rupee turnover. Late-session/CAS flags remain diagnostic and the protected-validation boundary is unchanged.

**Decision:** discard the superseded economic outputs for interpretation. Rerun the corrected economic implementation before making the Strategy 003 economic viability decision.
