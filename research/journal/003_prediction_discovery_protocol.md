# Strategy 003 — Prediction-Driven Alpha Discovery Protocol

**Status:** 🟡 Research program — discovery only; no trading hypothesis or candidate frozen.

## 1. Research question

Strategies 001 and 002 were useful, but both centered on narrow short-horizon price patterns. Strategy 003 deliberately changes the research question:

> Can observable, point-in-time market information predict cross-sectional differences in future returns strongly and consistently enough that the information could eventually be converted into a cost-resilient portfolio?

This is a prediction problem first, not a trading-rule search. Momentum, reversal, volume, volatility and market-relative state are feature families, not assumed strategies.

If the model merely rediscovers Strategy 002's residual-reversal mechanism, that is evidence about an existing closed research line and is not automatically a new Strategy 003 alpha.

## 2. Governing methodology

Follow the project's pattern-first methodology and the supplied large-hedge-fund quant-research reference:

DATA → PREDICTIVE INFORMATION DISCOVERY → CHARACTERIZATION → ECONOMIC INTERPRETATION → FALSIFIABLE HYPOTHESIS → SIMPLE BASELINE → CONTROLLED MODEL DEVELOPMENT → PORTFOLIO CONSTRUCTION → COST/EXECUTION TEST → CHRONOLOGICAL HOLDOUT → PROSPECTIVE PAPER/SHADOW → CONTROLLED LIVE

The central discipline is: Pattern ≠ predictive information ≠ hypothesis ≠ strategy ≠ validated alpha.

ML is an extraction tool, not the hypothesis.

## 3. Locked universe and data

- Reuse the existing Strategy 002 Indian-equity data acquisition.
- Universe manifest: research/universe_candidates.csv.
- Structural-quality gate: data/reports/strategy_002_universe_audit.csv.
- Use equity candidates only for the first experiment.
- Exclude instruments that fail the existing structural-quality audit.
- NIFTYBEES is used only as a market reference/proxy, not as an equity prediction observation.
- Do not add/remove/rank securities using future outcomes.

The primary experiment stays at the existing 5-minute decision frequency. A multi-day target is not part of the primary intraday program.

The current broker-native universe has a known survivorship/PIT limitation. It is acceptable for discovery only and must be disclosed; it is not automatically eligible for final promotion.

## 4. Locked temporal boundary

- Exploratory/development: 2025-09-18 through 2026-06-09.
- Validation: 2026-06-10 through 2026-08-19 — unavailable to this discovery script.
- Final holdout: 2026-08-20 through 2026-09-17 — unavailable to this discovery program.

The holdout remains protected even if development results are disappointing.

## 5. Prediction target

The superseded first draft used 1-day and 5-day close-to-close targets. A 5-trading-day target means predicting the close-to-close return five trading days later, which is a multi-day holding-period outcome rather than an intraday target.

The primary Strategy 003 target is now the next 5-minute bar return:

`Close(t+1 bar) / Close(t) - 1`

The target is converted to cross-sectional excess return by subtracting the equal-weight mean next-bar return across the eligible contemporaneous cross-section. The final bar of each session has no target because the next observation would be the following session.


## 6. Initial feature families

The first pass explicitly excludes raw signed-return direction, prior signed-return threshold/event rules, explicit abnormal-move continuation rules, peer-relative lagged-return reversal rules, Strategy 001-style z-score event definitions, and Strategy 002-style residual-reversal signal rules.

The initial feature families are:

1. Liquidity/activity: current 5-minute log volume, one-bar volume change, 12-bar volume z-score, 78-bar volume z-score.
2. Volatility/state: 12-bar realized volatility, 78-bar realized volatility, current bar range, 78-bar range z-score.
3. Bar shape/intraday state: close location within the current bar, close relative to trailing 78-bar mean, bars since session open.
4. Market context: NIFTYBEES current 5-minute return and trailing 78-bar market volatility.
5. Cross-sectional transforms: percentile ranks and z-scores of the registered features.

All features must use only information available at the decision bar close. If a later model is dominated by signed-return information, that result must be classified against Strategy 001/002 rather than promoted as a new Strategy 003 mechanism.

## 7. Evidence layers

### Layer 1 — Univariate predictive information

For each feature and horizon, record daily Pearson IC, daily Spearman rank IC, mean IC, IC standard deviation, IC information ratio, fraction of positive-IC dates and usable dates.

The key question is stability across time, not the largest historical point estimate.

### Layer 2 — Simple multivariate models

Fixed model ladder for the first pass:

1. zero/mean baseline
2. ordinary least squares
3. Ridge regression with one fixed penalty

No large hyperparameter grid is permitted in the discovery pass.

### Layer 3 — Diagnostic portfolio translation

Predictions are converted only for diagnostics into a simple cross-sectional top-minus-bottom quintile spread. This is not yet a trading strategy. It tests whether predictive information produces economically visible separation before costs.

## 8. Chronological development split

Inside the locked exploratory period:

- first 60% of 5-minute decision timestamps: training
- next 20%: model-development validation
- final 20%: development test

No random shuffling. Because the target is the next 5-minute bar, the final training timestamp and final validation timestamp whose labels could cross the following segment are removed. This is a one-decision-timestamp purge. Future longer intraday horizons must purge by their registered horizon in decision bars.

The project validation and final holdout remain untouched.

## 9. Model escalation

Planned ladder:

baseline → linear regression → regularized linear model → tree ensemble → more complex nonlinear model → neural network only if justified

Complexity increases only when the simpler model establishes evidence worth explaining. A complex model must demonstrate incremental out-of-sample predictive information relative to a simpler baseline.

## 10. Multiple-testing controls

- Feature families are registered before the first run.
- Horizons are fixed before model comparison.
- The model ladder is fixed before results.
- No arbitrary feature-combination search.
- No large hyperparameter sweep in discovery.
- Every tested configuration is recorded.
- Negative results are retained.
- Development-test results cannot be used to invent new features.
- Final holdout cannot be used for feature/model selection.
- Material changes require a new registered experiment and an explicit record of the added search burden.

Nominal statistical significance is not sufficient. Economic magnitude, stability and execution feasibility remain necessary.

## 11. Economic interpretation gate

A predictive feature/model does not become a hypothesis until we can state what information it captures, why it might persist, what conditions should strengthen or weaken it, and why its expected magnitude could plausibly survive costs.

If a model predicts returns but no credible mechanism can be articulated, it remains an empirical pattern.

## 12. Portfolio and execution gates

Only after predictive information survives discovery may we test ranking, factor/market neutralization, volatility scaling, position limits, turnover, breadth, concentration and portfolio risk.

Only after the portfolio stage may we model spread, slippage, brokerage/taxes, market impact, liquidity, order timing, fill assumptions and capacity.

Portfolio construction can improve extraction of a real edge; it cannot manufacture expected return from a dead predictor.

## 13. Repository resources to reuse

The repository already contains substantial research resources. Before inventing equivalent analysis or code, inspect and reuse/adapt relevant material.

Relevant starting points include:

- research/journal/research_methodology.md
- research/journal/repository_resource_policy.md
- research/journal/001J_cross_sectional_equity_spec.md
- research/journal/002_pattern_discovery_protocol.md
- trading_resources/Concepts/Data-and-Feature-Engineering-for-Trading.md
- trading_resources/Concepts/Trading-with-Machine-Learning-Regression.md
- trading_resources/Concepts/Trading-with-ML-Classification-and-SVM.md
- trading_resources/Concepts/Unsupervised-Learning-in-Trading.md
- trading_resources/WQU_resources/Financial Economics/Module 2/Lesson 3 - Penalized Regression.ipynb
- trading_resources/WQU_resources/Machine Learning in Finance/Module 4/Lesson 1 - Ensemble Learning.ipynb
- trading_resources/WQU_resources/Machine Learning in Finance/Module 8/Lesson 2 - Linear Models in TensorFlow Timing Factors and Smart-Beta Strategies.ipynb
- existing Strategy 002 universe/data validation utilities.

These are references and building blocks, not validated alpha.

## 14. Promotion and closure

Promotion requires stable predictive information, an interpretable economic mechanism, simple-baseline evidence, incremental model value when applicable, chronological validation, realistic costs, execution feasibility, explicit risk controls, untouched-holdout evidence and prospective paper/shadow evidence.

A failed predictive experiment is a valid result.

## 15. First local run

After syncing:

    python scripts/run_strategy_003_prediction_discovery.py data/raw/strategy_002_universe

Outputs are written to data/reports/strategy_003_prediction_discovery/:

- feature_ic.csv
- model_metrics.csv
- quintile_diagnostics.csv
- feature_metadata.csv
- run_manifest.json

The first run is discovery evidence only. It does not freeze a trading strategy.

## 16. Decision tree

If predictive information is weak or unstable: do not add complexity; record the failure and choose a genuinely different mechanism.

If predictive information is stable: explain the mechanism, then test whether a simple model is sufficient before escalating to controlled nonlinear models.

If the only stable information is the already-closed Strategy 002 reversal mechanism, do not use Strategy 003 to disguise a reopening of Strategy 002. Record it as evidence about the existing phenomenon instead.

## Research principle

> We are not searching directly for profitable trading rules. We are searching for stable, economically interpretable predictive information, and only then asking whether that information can be converted into a profitable portfolio after risk, execution and transaction costs.