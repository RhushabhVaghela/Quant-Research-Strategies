# Strategy 003 — Predictive Signal Characterization Protocol

**Status:** 🟡 Characterization only — frozen discovery model; no strategy candidate.

## Purpose

The first Strategy 003 discovery run established a stable-looking next-5-minute predictive relationship in the exploratory/development sample. This phase characterizes that relationship without changing the frozen discovery model, searching parameters, using protected validation, or touching the final holdout.

The characterization follows the project's lifecycle:

DATA → PREDICTIVE INFORMATION DISCOVERY → CHARACTERIZATION → ECONOMIC INTERPRETATION → HYPOTHESIS → STRATEGY

## Frozen discovery inputs

- Universe: the existing 15 eligible Indian equities.
- Market proxy: NIFTYBEES.
- Target: next 5-minute cross-sectional excess return.
- Decision resolution: 5 minutes.
- Discovery model ladder: zero baseline → OLS → Ridge with fixed α=1.
- Feature families: activity, volatility/state, bar shape/intraday state, market context.
- Protected project validation starts: 2026-06-10.
- Final holdout starts: 2026-08-20.
- Holdout remains untouched.

The characterization is descriptive. It must not select a new feature subset, parameter, universe or model because it looks better.

## Characterization dimensions

### 1. Spread distribution

For the frozen OLS and Ridge predictions, summarize the development-test top-minus-bottom quintile spread using:

- mean;
- median;
- standard deviation;
- 10th/25th/75th/90th percentiles;
- positive-timestamp fraction;
- winsorized mean/median;
- sensitivity to the largest absolute observations.

The objective is to distinguish a broad effect from a small number of extreme observations.

### 2. Monotonicity

The diagnostic output must preserve the original quintile information so a later review can check whether predicted-score ordering maps monotonically into realized next-bar excess returns.

A positive top-minus-bottom spread alone is insufficient if intermediate quintiles are non-monotonic.

### 3. Time-of-day stability

Partition the development-test sample into fixed clock buckets:

- 09:15–09:59;
- 10:00–11:59;
- 12:00–13:59;
- 14:00–15:30.

These are descriptive buckets selected before reviewing the characterization results. The objective is to determine whether the signal is present broadly or concentrated in one session segment.

### 4. Cross-sectional stability

Measure prediction/target relationship by individual stock across the development-test sample.

The objective is to distinguish:

- broad cross-sectional information;
- a small number of stock-specific effects;
- a market-model artifact.

This analysis must not remove poor stocks or retain strong stocks for a new backtest.

### 5. Feature-family decomposition

Run the same frozen OLS/Ridge fitting procedure on each registered family independently:

- activity;
- volatility;
- bar shape/intraday state;
- market context.

This is an **ablation/interpretation diagnostic**, not a feature-selection search.

The families were registered before the discovery results and are not being expanded or tuned here.

### 6. Coefficient decomposition

Record standardized OLS and Ridge coefficients from the frozen full feature set.

Coefficients are descriptive because the registered feature set contains correlated transformations of the same base features. A large coefficient is not automatically a causal or independent alpha estimate.

### 7. OLS/Ridge agreement

Measure the cross-sectional correlation between the OLS and fixed-Ridge predictions.

If the predictions are nearly identical, the evidence does not currently justify increasing regularization/model complexity.

## Interpretation rules

A characterization can support an economic hypothesis only if the evidence is:

- directionally coherent;
- reasonably broad across stocks/time;
- not dependent on a handful of tails;
- not confined to one arbitrary session bucket;
- economically interpretable from information available at the decision time.

The current strongest univariate feature is the current 5-minute close location within its bar, followed by intraday position relative to the trailing 60-bar mean. These observations are **candidate mechanisms**, not conclusions.

Potential interpretation to test:

> Current within-bar price location and recent intraday state may contain short-horizon information about subsequent cross-sectional returns.

This statement remains provisional until the characterization and later protected validation support it.

## Explicit non-goals

This phase does not:

- evaluate 2026-06-10 through 2026-08-19;
- evaluate 2026-08-20 onward;
- calculate trading-strategy P&L;
- introduce nonlinear models;
- search thresholds;
- search holding periods;
- select a new universe;
- choose a winning feature subset;
- optimize costs or execution assumptions.

## Exit criteria

### Advance to economic-hypothesis formulation only if

The frozen model's predictive separation is reasonably broad, stable and interpretable.

### Hold at characterization if

The relationship is real-looking but concentrated, tail-dependent, time-localized or economically unclear.

### Close the research line if

The apparent predictive relationship disappears under basic descriptive stress tests or is explained by a previously closed mechanism.

Any future new search requires an explicit new registration and a record of the additional research degrees of freedom.
