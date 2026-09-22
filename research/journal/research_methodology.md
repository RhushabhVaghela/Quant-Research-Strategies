# Research Methodology — Pattern-First Systematic Trading

## Purpose

The project follows a pattern-first research process. We do not begin by inventing a strategy and then searching historical data until it appears profitable. We first acquire relevant data, discover and characterize statistical patterns, interpret them economically, formulate a falsifiable hypothesis, and only then define a tradable strategy. For prediction-driven research, the same discipline applies one layer earlier: first establish stable predictive information, then interpret it economically and only then convert it into a portfolio/strategy.

## Intraday target alignment

When the project's stated objective is intraday strategy research, discovery targets must live on an intraday decision horizon unless a separate multi-horizon research question has been explicitly registered.

A daily or multi-day forward-return target is not an intraday prediction target merely because it may later inform an intraday trade. A 5-trading-day target is a multi-day close-to-close outcome.

Prediction horizon and trading holding period are related but not identical. A next-bar predictive target can be evaluated first without assuming the eventual strategy must hold for exactly one bar. The eventual executable holding period is chosen after the predictive information is understood and a distinct economic mechanism is formulated.

For intraday experiments, horizon definitions must be expressed in decision bars/minutes, and chronological train/validation boundaries must be purged by the number of future decision observations used by the target.

The project's current 003 starting resolution is one 5-minute bar because the source data and existing intraday research are 5-minute. This is a discovery resolution, not a permanent five-minute holding-period assumption. If the signal survives, a pre-registered small set of adjacent horizons can be characterized later.


## Lifecycle

Data → data audit → pattern discovery → pattern characterization → economic interpretation → hypothesis → strategy definition → development → candidate freeze → untouched chronological holdout → prospective paper/shadow → controlled live validation.

A pattern is not a hypothesis. A hypothesis is not a strategy. A strategy is not validated alpha.

## 1. Data and pattern discovery

Start with relevant point-in-time data and predefined descriptive/statistical tools appropriate to the asset and question. Examples include return distributions, conditional forward returns, autocorrelation, volatility, correlation/covariance, PCA, clustering, stationarity, spread diagnostics, seasonality, liquidity, and other methods already available in the repository.

Discovery is exploratory. Results may suggest relationships, but they are not treated as validated trading edges.

Pattern discovery must not quietly use strategy P&L to define the universe or select the most attractive historical outcome. If many alternative tests, transformations, horizons, universes, or filters are examined, that research freedom must be recorded because it contributes to multiple-testing and data-snooping risk.

## 2. Pattern characterization

Before defining a strategy, characterize a promising pattern using evidence such as:

- effect size and direction;
- frequency/breadth;
- time stability;
- cross-sectional stability;
- distribution and tail behavior;
- dependence between observations;
- regime sensitivity;
- economic plausibility;
- liquidity and execution context.

The goal is to understand what is actually present, not to manufacture a trading rule.

## 3. Economic hypothesis

A pattern becomes a strategy candidate only when a plausible mechanism can be stated. The hypothesis should specify:

- the economic mechanism;
- the population/instrument universe;
- the prediction target;
- the information available at decision time;
- why the effect might persist after costs;
- conditions under which the effect should weaken or disappear.

The hypothesis should be falsifiable.

## 4. Strategy definition

Translate the hypothesis into a precise executable specification: universe, signal, entry, exit, holding period, position sizing, risk controls, costs, execution assumptions, and data timing.

Start with a simple interpretable baseline. Do not optimize parameters merely because they improve historical P&L.

## 5. Development and legitimate optimization

Optimization is appropriate **after** the pattern/hypothesis has been established and only within a pre-designated development sample.

Development may compare a preregistered parameter/model family. The objective is to identify a robust region, not a magical historical maximum.

Selection should consider more than cumulative return: mean/median, distribution, drawdown, win rate, profit factor, costs, turnover, breadth, concentration, chronological stability, neighboring-parameter stability, execution feasibility, and economic rationale.

A parameter search is not automatically valid merely because it is called a grid search. The full number of research decisions matters: universe choices, features, transformations, thresholds, exits, filters, costs, regimes, model classes, and repeated searches all create opportunities for overfitting.

## 6. Multiple testing and data snooping controls

The project uses the following controls:

1. Separate exploratory discovery from confirmatory validation.
2. Define the research universe independently of strategy outcomes where possible.
3. Predefine development dimensions before running a candidate search.
4. Preserve all tested configurations and negative results.
5. Prefer parameter neighborhoods and stability over isolated maxima.
6. Do not repeatedly reopen a development sample because an earlier search failed.
7. If a sequential search is scientifically justified, register it explicitly and record that the effective search space has increased.
8. Protect the chronological holdout from all candidate-selection decisions.
9. Never use holdout results to choose parameters, features, universes, or rescue rules.
10. Treat cross-sectional and repeated trades as dependent observations when appropriate.
11. Require prospective evidence before live promotion.

Where formal multiple-testing corrections are appropriate, they should be selected based on the research design rather than applied mechanically. Statistical significance is only one part of the evidence; economic magnitude and execution feasibility remain necessary.

## 7. Holdout

After candidate selection, freeze the complete strategy specification. The chronological holdout is then evaluated without retuning.

If the holdout fails, record the failure. Do not use the holdout to search for a new rule. A new investigation requires a new preregistration and an explicit account of the additional research degrees of freedom.

## 8. Prospective validation

Historical validation is followed, where appropriate, by paper/shadow testing with an immutable activation boundary. Signals are recorded using only information available at the decision time; outcomes are appended only after they occur.

Prospective results are not used to silently retune the frozen strategy.

## 9. Repository resources are mandatory reference material

Before implementing a new investigation, inspect the repository for relevant existing resources. The repository contains educational and research material from Quantra and WorldQuant University as well as prior project work on statistics, correlation/covariance, PCA, clustering, DBSCAN, similar-stock identification, stationarity, autocorrelation, pairs trading, portfolio construction, data acquisition, point-in-time controls, and execution.

Use relevant resources to:

- reuse working code;
- adapt existing implementations;
- combine methods from multiple sources;
- reuse mathematical/statistical understanding;
- avoid rebuilding equivalent functionality unnecessarily.

Existing resources are references and building blocks, not automatically validated alpha. Any reused method must still satisfy the current experiment's data, timing, validation, and execution requirements.

This is a standing project rule: **when making a GitHub research request, first remind ourselves to inspect the repository resources and use the relevant ones where appropriate.**

## 10. Strategy lineage

A genuinely different economic mechanism receives a new strategy ID. Parameter variants, universe variants, and implementation experiments under the same mechanism remain experiments under the parent strategy.

Historical strategy records are immutable evidence. Closure means the tested implementation was not promoted; it does not imply that every broader form of the economic phenomenon has been disproven.
