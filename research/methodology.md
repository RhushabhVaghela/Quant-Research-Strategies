# Research Methodology

I use the following process when I work on a new quantitative trading idea.

## 1. Start with data

I first look at the data and understand what is actually present.

I check things such as:

- return behaviour
- volatility
- correlation
- autocorrelation
- cross-sectional differences
- market regimes

## 2. Form a hypothesis

An observation is not automatically a strategy.

I try to explain why the relationship might exist and define a test that could prove the idea wrong.

## 3. Build a simple baseline

Before using a complex machine-learning model, I build a simple statistical baseline such as OLS regression.

This gives me something to compare against and makes it easier to see whether additional model complexity is actually helping.

## 4. Control data leakage

I make sure the model only uses information that would have been available at the decision time.

This is important for avoiding:

- look-ahead bias
- data leakage
- accidental use of future information

## 5. Validate in time order

Financial data is time-dependent, so I prefer chronological splits and walk-forward validation instead of randomly shuffling observations.

## 6. Include trading costs

I check brokerage, taxes, fees, spread and slippage before deciding that a result is tradable.

A small gross edge can disappear after realistic trading costs.

## 7. Test out of sample

Once a model or strategy is fixed, I test it on later data that was not used to make the decisions.

I do not change the rules just because the new period is weak.

## 8. Keep the failures

A failed experiment is still useful when it tells me why an idea did not work.

I keep those results so I can avoid repeating the same mistake.

## Key terms

**Point-in-time:** using only information available at that moment.

**Walk-forward validation:** train on the past, test on the following period, then move the window forward.

**Out-of-sample:** data kept separate from model or strategy selection.

**Overfitting:** fitting historical noise so closely that the result does not generalise.

**Transaction costs:** direct costs of trading.

**Slippage:** execution difference between the intended and actual price.
