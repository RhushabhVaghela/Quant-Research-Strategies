# Strategy 003 — Short-Horizon Return Prediction

## What I tested

For this research line, I changed the question.

Instead of starting with one predefined trading rule, I tested whether short-horizon returns could be predicted from information describing the current market state.

I looked at feature groups covering areas such as:

- liquidity and activity
- volatility
- intraday price structure
- market context

I started with simple statistical models before considering more complex machine-learning approaches.

## What I found

The prediction work produced a measurable relationship between the model score and later cross-sectional returns.

The relationship also survived the protected prediction test, which was important because that period had not been used to choose the model.

However, the next step exposed a different problem: converting the prediction into an executable portfolio created too much trading and too much cost.

## Why I closed it

The predictive result by itself was not enough.

The tested implementation became uneconomic after trading costs, so I closed the current executable version.

This was an important result for me because it showed that:

**prediction quality ≠ trading profitability**

A model can have useful predictive information and still fail as a trading strategy.

## What I learned

I learned more about:

- cross-sectional prediction
- feature engineering
- OLS regression
- Ridge regression
- regularization
- Information Coefficient (IC)
- rank IC
- chronological validation
- protected out-of-sample testing
- transaction-cost analysis

## Key terms

**OLS:** ordinary least squares regression, used here as an interpretable baseline.

**Ridge regression:** a regression model with an L2 penalty that helps control unstable coefficients.

**IC:** the correlation between predicted scores and later returns.

**Rank IC:** the same idea using the rank order of predictions and returns.

**Feature engineering:** turning raw market data into variables that may contain useful information for a model.

**Protected validation:** a test period kept separate from the research decisions used to build the candidate.

## Status

**Closed — the tested trading implementation did not clear the economic viability check.**
