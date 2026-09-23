# Strategy 003 — Provisional Economic Hypothesis Protocol

**Status:** 🟡 Provisional hypothesis formulation — no strategy candidate, no protected validation, no holdout.

## 1. Why a hypothesis is now warranted

The controlled development-test characterization of the frozen next-5-minute OLS/Ridge model produced a coherent prediction ordering rather than an isolated Q5-minus-Q1 effect:

- OLS mean realized excess return by prediction quintile: Q1 **−1.1230 bps**, Q2 **−0.1004 bps**, Q3 **−0.1497 bps**, Q4 **+0.2794 bps**, Q5 **+1.0937 bps**.
- Q1→Q5 therefore spans about **2.217 bps**, matching the previously reported top-minus-bottom diagnostic.
- The distribution is not obviously driven by a handful of extreme observations: raw mean spread **+2.2168 bps** versus winsorized mean **+2.2947 bps**.
- OLS and fixed Ridge predictions are effectively identical (correlation approximately **0.9999999**).
- Stock-level prediction/target correlations are small and mixed, with positive relationships in some names and negative/near-zero relationships in others; the evidence does not identify a single-stock driver.
- Base-family ablation attributes the largest descriptive spread to the registered **bar-shape/intraday-state** family (**+1.7537 bps**), followed by volatility (**+0.9845 bps**), while activity is small (**+0.2125 bps**) and market context is approximately zero/negative (**−0.0952 bps**).

These results support formulating a falsifiable economic interpretation, but they do **not** establish a validated alpha or a tradable strategy.

## 2. Provisional mechanism

The leading candidate mechanism is:

> **Intrabar price location and recent intraday state may contain short-horizon cross-sectional information because the current bar may encode temporary imbalance in price discovery/positioning that persists into the next bar rather than being fully resolved at the decision close.**

This is intentionally broader than a directional trading rule. It describes an information mechanism to be tested, not a conclusion that a specific reversal or continuation trade exists.

The hypothesis remains subject to the Strategy 001/002 lineage guardrail. The current registered features do not include explicit signed-return event rules or residual-reversal rules. If later work shows that the effect is actually driven by a previously closed signed-return mechanism, it should be reassigned to that lineage rather than promoted as new Strategy 003 alpha.

## 3. Falsifiable predictions

The hypothesis makes the following predictions for the frozen 5-minute cross-sectional setting:

1. **Cross-sectional ordering:** higher model-implied scores should continue to correspond to higher next-bar excess returns, while lower scores correspond to lower next-bar excess returns.
2. **Mechanism relevance:** the relationship should remain materially present when the interpretation-relevant bar-shape/intraday-state variables are examined without requiring signed-return event rules.
3. **Breadth:** the effect should not require a single stock or tiny stock subset.
4. **Time behavior:** the effect should not be entirely explained by an arbitrary late-session artifact. Because the current frozen 60-bar features have strong warm-up requirements, early-session coverage must be treated as an information limitation rather than patched by changing the feature set.
5. **Economic magnitude:** the gross cross-sectional separation must be large enough to survive a later, separately registered portfolio/execution test. A few basis points of diagnostic spread are not sufficient evidence by themselves.

## 4. What is not yet claimed

This protocol does **not** claim:

- that the effect is profitable after transaction costs;
- that one-bar holding is the final holding period;
- that the bar-shape family is the final feature set;
- that a threshold can be selected from the current quintile results;
- that nonlinear ML will improve the signal;
- that the protected validation period or final holdout will confirm the relationship.

No threshold, horizon, model, feature subset, universe or cost assumption is being optimized from this document.

## 5. Next controlled experiment

The next experiment should test the economic interpretation rather than immediately escalate model complexity.

### Experiment 003H — Mechanism decomposition

**Question:** Is the frozen predictive relationship consistent with the provisional intrabar-state mechanism, or does it disappear once the relevant information is represented in a simpler interpretable specification?

Use only the existing exploratory/development-test framework first. Do **not** use the protected validation or final holdout.

The experiment should compare, without parameter optimization:

1. the frozen full-model diagnostic;
2. a preregistered simple bar-shape/intraday-state model containing the already-registered base features from that family;
3. the existing zero baseline.

The purpose is explanatory decomposition. It is not a search for the best feature subset.

The experiment should report the same predictive diagnostics used previously: cross-sectional IC/rank IC, Q1–Q5 ordering, top-minus-bottom spread, stock breadth, and time coverage. It should also explicitly test whether the simplified mechanism remains distinguishable from the previously closed 001/002 mechanisms.

### Boundary condition

No portfolio construction, turnover optimization, transaction-cost grid, holding-period search, threshold search, tree model or neural network is authorized until this mechanism test is completed and judged interpretable.

## 6. Evidence boundary

All evidence in this protocol is from the exploratory/development-test sample ending **2026-06-09**. The project validation period beginning **2026-06-10** and final holdout beginning **2026-08-20** remain protected.
