# Quant Research Strategies

This is my personal quantitative research repository. I use Python to study systematic trading ideas, test them with historical data, and learn what does and does not hold up in real-world conditions.

My focus is on building strategies that are **research-driven and tradable**, rather than simply producing a good-looking backtest.

## What I am working on

I am currently working across:

- Intraday equity research
- Derivatives and options
- Financial time-series models
- Statistical analysis
- Machine learning for financial prediction
- Risk and portfolio analysis
- Market-data and API-based workflows

I am also strengthening the theory behind the work, including **AR, MA, ARMA, ARIMA, GARCH, stationarity, autocorrelation, regression, volatility, and option pricing**.

## Research approach

For each idea, I try to follow a simple process:

**Data → observation → hypothesis → model → backtest → cost check → out-of-sample test → paper/shadow testing**

I keep failed experiments as part of the record. A strategy is not considered successful just because it makes money in a historical backtest.

## Current research

| Strategy | Area | Current status |
|---|---|---|
| Strategy 001 | Intraday price behaviour | Closed after the tested implementation did not show enough cost-resilient performance |
| Strategy 002 | Cross-sectional statistical research | Closed after the tested version was too small relative to trading costs |
| Strategy 003 | Short-horizon return prediction | Predictive relationship found, but the tested trading implementation did not remain viable after costs |

More detail is available in:

- [Strategy 001](research/journal/strategy_001.md)
- [Strategy 002](research/journal/strategy_002.md)
- [Strategy 003](research/journal/strategy_003.md)
- [Research methodology](research/methodology.md)

## Quant concepts I am using

**Return:** the percentage change in an asset's value.

**Volatility:** a measure of how much returns vary. I use it as both a risk measure and a possible market-state variable.

**Sharpe ratio:** risk-adjusted performance, comparing excess return with return volatility.

**Maximum drawdown:** the largest fall from a previous portfolio peak.

**Correlation:** how two variables move together. I use it for diversification, market relationships, and feature analysis.

**Stationarity:** a time series is stationary when its statistical behaviour is reasonably stable over time. This matters for models such as ARIMA and for spread-based research.

**AR / MA / ARMA / ARIMA:** time-series models used to describe and forecast relationships in past observations. ARIMA also handles differencing when a series is not stationary.

**GARCH:** a volatility model that captures changing variance over time.

**OLS:** ordinary least squares regression. I use it as a simple and interpretable statistical baseline.

**Regularization:** a way of limiting model complexity. For example, Ridge regression adds an L2 penalty to reduce unstable coefficients.

**IC (Information Coefficient):** the correlation between a model score and the later return it is trying to predict.

**Cross-sectional analysis:** comparing several assets at the same point in time rather than analysing one asset in isolation.

**Walk-forward validation:** repeatedly training on earlier data and testing on later data to better reflect how a model would be used in practice.

**Out-of-sample testing:** testing a frozen idea on data that was not used to choose the model or rules.

**Transaction costs:** brokerage, taxes, exchange fees and other trading charges.

**Slippage:** the difference between the price I expect and the price at which a trade is actually executed.

## Why the repository is structured this way

I want the Git history to show how my research developed. New hypotheses, tests, fixes, failed ideas and improvements are recorded as I work rather than added only after a project is finished.

The goal is to show the research process clearly and honestly.
