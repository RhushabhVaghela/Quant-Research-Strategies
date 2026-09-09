# Intraday Strategy Ideation — Phase 0

**Status:** Research only. No strategy has been approved for trading.

## Objective

Identify a small set of hypothesis-driven intraday strategy families that can be researched rigorously, compared against simple baselines, extended with ML/DL only when justified, and eventually connected to paper/live execution.

## Candidate A — Regime-Conditioned Intraday Momentum

**Hypothesis:** Intraday directional moves may persist more reliably in specific combinations of trend, volatility, volume, and market-regime conditions than across all observations.

**Research:** Define objective momentum/continuation events; perform an event study; test whether conditioning on volatility, volume, time-of-day, and broader-market state changes forward-return distributions.

**ML role:** Estimate continuation probability or expected trade outcome and filter candidate events.

**Quantra building blocks:** intraday momentum, time-series momentum, random forest/classification/regression, k-means/regime ideas, volatility targeting, strategy analytics.

**Main risks:** leakage, overfitting thresholds, ignoring execution costs, confusing correlation with causation.

## Candidate B — Intraday Mean-Reversion Regime Filter

**Hypothesis:** Short-horizon deviations from an intraday reference price may mean-revert under range-bound/low-trend regimes, but may fail during strong directional regimes.

**Research:** Measure conditional reversion after standardized price deviations; identify when reversion is more/less likely.

**ML role:** Regime classification or trade-quality filtering rather than unconditional prediction.

**Quantra building blocks:** mean reversion, Bollinger-style features, k-means, ML classifiers, volatility/risk modules.

**Main risks:** trading against strong trends, spread/slippage, unstable mean definition.

## Candidate C — Intraday Relative-Value / Pairs

**Hypothesis:** Closely related instruments can temporarily diverge from a stable relationship, creating short-horizon relative-value opportunities when the relationship and market regime remain supportive.

**Research:** Test stationarity/cointegration, spread dynamics, half-life, conditional convergence, and regime dependence.

**ML role:** Predict convergence probability or filter spread-entry events.

**Quantra building blocks:** pairs trading, OLS hedge ratio, ADF/cointegration, z-scores, ML classification/regression, volatility targeting.

**Main risks:** relationship breakdown, hedge-ratio instability, synchronized execution, short availability, transaction costs.

## Candidate D — Intraday Volume/Price Regime Strategy

**Hypothesis:** Abnormal volume combined with price/range behavior may contain information about whether a move is likely to continue or reverse.

**Research:** Normalize volume by time-of-day expectations; study forward returns conditional on volume shock, range expansion, and direction.

**ML role:** Learn nonlinear interactions between volume, price, volatility, and time-of-day.

**Quantra building blocks:** volume reversal, intraday momentum, order-flow research, classification models, strategy analytics.

**Main risks:** bar-level volume is not order-book data; execution costs; news-driven outliers.

## Candidate E — Intraday Volatility-Regime Strategy

**Hypothesis:** The behavior and reliability of directional/reversion signals changes materially across volatility regimes.

**Research:** Forecast/estimate short-horizon volatility and condition signal selection/position sizing on the forecast.

**ML role:** Volatility classification/forecasting or trade-quality filtering.

**Quantra building blocks:** GARCH, volatility targeting, ML regression, intraday momentum/mean reversion.

**Main risks:** forecast instability, parameter sensitivity, confusing volatility prediction with return prediction.

## Candidate F — Hybrid Signal Ensemble

**Hypothesis:** Distinct weak signals may contain complementary information, and a model may improve signal selection by learning when each signal tends to work.

**Research:** Build independent, interpretable baseline signals; test incremental information and correlation among signals before combining them.

**ML role:** Meta-model that predicts signal quality rather than raw price.

**Quantra building blocks:** momentum, mean reversion, volatility, ML classifiers, portfolio/risk methods.

**Main risks:** excessive feature stacking and multiple testing; must prove incremental value out of sample.

## Candidate G — Intraday Options/Volatility Research

**Hypothesis:** Differences between forecast/realized volatility and option-implied volatility may create conditional opportunities, subject to liquidity and transaction costs.

**Research:** First establish whether the forecast/implied relationship is measurable and tradable at the intended horizon.

**ML role:** Forecast realized volatility or classify attractive relative-volatility conditions.

**Quantra building blocks:** GARCH, implied/forward volatility, volatility smile/skew, options strategies.

**Main risks:** data quality, option liquidity, bid-ask spreads, Greeks, execution complexity.

## Initial ranking framework

| Candidate | Research depth | Intraday fit | ML fit | Data/implementation | Live feasibility | Main concern |
|---|---|---|---|---|---|---|
| A Momentum + regime | High | High | High | High | High | overfitting |
| B Mean reversion + regime | High | High | High | High | High | trend losses |
| C Relative value/pairs | High | Medium-High | High | Medium | Medium | relationship breakdown |
| D Volume/price | High | High | High | Medium-High | High | data limitations |
| E Volatility regime | High | High | High | Medium | High | forecast instability |
| F Signal ensemble | High | High | High | High | High | multiple testing |
| G Options/volatility | Very High | High | High | Medium-Low | Medium-Low | complexity/liquidity |

## Decision rule

Do not choose the winner based on expected return. The next phase should evaluate the hypotheses against actual data availability, event-study evidence, statistical validity, realistic costs, and execution constraints.

A strategy can be rejected. Rejection is a valid research outcome.
