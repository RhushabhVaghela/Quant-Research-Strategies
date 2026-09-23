# Strategy 003H — Economic-Form Decomposition Protocol

**Status:** 🟡 Preregistered development-only experiment — final controlled research gate before a protected-validation decision.

## 1. Research question

The lineage-separation experiment found that the provisional 003H core — `close_location_1bar + intraday_position_60bar` — retains predictive information after explicitly representing the frozen Strategy 001 continuation event and Strategy 002 leave-one-out residual.

The remaining question is narrower:

> **What interpretable economic form does the 003H two-variable relationship take?**

This experiment is designed to distinguish whether the observed relationship is primarily:

1. a **current-bar location effect**;
2. a **recent intraday-position/state effect**; or
3. a **joint location × state relationship** that is not well represented by either variable alone.

This is an explanatory decomposition, not a new feature search and not a trading-rule optimization.

## 2. Fixed representations

Use only the two already-locked 003H raw variables:

- `close_location_1bar`
- `intraday_position_60bar`

Evaluate exactly these four fixed specifications:

1. **Close-location only**
2. **Intraday-position only**
3. **Additive two-variable OLS core**
4. **Pre-registered joint form:** additive OLS plus one fixed product interaction, `close_location_1bar × intraday_position_60bar`

The interaction is registered as a single economic-form test because the research question explicitly asks whether the effect is joint rather than merely additive. No other transforms, powers, splines, bins, thresholds, regimes, ranks, cross-sectional transforms, or feature-selection steps are permitted.

The additive two-variable core remains the reference model from the completed attribution experiment. The interaction specification is a decomposition of the same two variables, not a new feature family.

## 3. Economic interpretation being tested

The fixed representations correspond to three mutually informative interpretations:

- **Location-only:** where the current bar closes inside its own range contains the dominant short-horizon information.
- **State-only:** the stock's current position relative to its recent 60-bar intraday state contains the dominant information.
- **Joint state:** the predictive relationship depends on how current-bar location interacts with recent intraday position.

These are competing descriptive interpretations. The experiment must not declare a mechanism causal merely because one specification has a larger historical metric.

## 4. Data and target

Keep exactly the existing Strategy 003 framework:

- same 15 eligible equities;
- same 5-minute data;
- same next-5-minute cross-sectional excess-return target;
- same exploratory/development window ending 2026-06-09;
- same chronological train / validation / development-test split;
- same one-decision-timestamp purge;
- same complete-case support across the two locked variables.

Protected validation beginning 2026-06-10 and final holdout beginning 2026-08-20 remain untouched.

## 5. Evaluation

For every specification report:

- mean IC;
- mean rank IC;
- descriptive IC IR;
- positive IC fraction;
- Q1–Q5 realized next-bar excess returns;
- Q1–Q5 spread;
- usable timestamps and observations;
- stock breadth;
- internal chronological validation versus development-test results.

For the interaction specification additionally report:

- the fitted interaction coefficient;
- the sign of the interaction coefficient;
- whether the interaction changes the cross-sectional score ordering materially relative to the additive model.

Coefficient magnitude must not be interpreted as causal effect size because all features are standardized in the model-fitting pipeline.

## 6. Common-support requirement

All four specifications must be evaluated on the same complete-case support for `close_location_1bar` and `intraday_position_60bar`.

This prevents apparent differences from being caused by feature availability rather than economic form.

## 7. Decision framework

The purpose is not to choose the specification with the largest development metric.

### Result A — additive interpretation remains sufficient

If the interaction adds negligible predictive ordering relative to the additive two-variable reference, record the simpler additive interpretation and close the interaction branch.

### Result B — stable joint-form evidence

If the interaction produces a materially different and internally consistent ordering on the preregistered development diagnostics, treat the joint form as an **economic-form hypothesis** requiring a final robustness gate. This still does not authorize protected validation automatically.

### Result C — unstable/inconclusive

If the interaction is unstable across the internal chronological validation and development-test periods, or the result depends strongly on a small subset of observations, retain 003H as unresolved and close the research line rather than adding further transforms.

## 8. Final-gate discipline

This is the last authorized exploratory/development decomposition under the current 003H lineage.

After this experiment:

- do not add new feature families;
- do not search alternative transforms;
- do not search thresholds;
- do not search holding periods;
- do not optimize costs;
- do not escalate to nonlinear models;
- do not construct a portfolio;
- do not reopen Strategies 001 or 002;
- do not use the protected validation or final holdout to choose among forms.

The only permitted next decision is:

**close Strategy 003 as unresolved/insufficient, or freeze one clearly defined explanatory form and move to a separately controlled protected-validation experiment.**

## 9. Implementation contract

The runner must use the existing Strategy 003 panel construction and point-in-time target code rather than rebuilding equivalent data logic.

Expected files:

- runner: `scripts/run_strategy_003h_economic_form_decomposition.py`
- tests: `tests/test_strategy_003h_economic_form_decomposition.py`
- report directory: `data/reports/strategy_003h_economic_form_decomposition/`

The run manifest must state:

- development-only boundary;
- protected validation untouched;
- final holdout untouched;
- four fixed specifications;
- common-support requirement;
- no parameter search;
- no feature selection;
- no nonlinear model search;
- no cost/holding-period/portfolio work.

## 10. Repository-learning context

This experiment also serves as an explicit learning module in the project's educational record: a model specification is only meaningful when the research question, information set, support, chronology, and decision boundary are fixed first.

It therefore reinforces the project's recurring lessons:

**simple model → interpretable mechanism → controlled comparison → common support → chronological evidence → hard decision gate.**
