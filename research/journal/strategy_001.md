# Strategy 001 — Intraday Price Behaviour

## What I tested

I started by testing whether unusually large intraday moves would tend to reverse.

The data did not support a strong and consistent mean-reversion relationship, so I investigated the opposite behaviour: whether some large moves were more likely to continue.

## What I found

The continuation pattern was more interesting than the original reversal idea. I then built a more formal backtest and checked the result across different time periods.

The gross backtest was positive, but the edge was small enough that trading costs became a major issue.

I also tested the research using point-in-time data and a prospective paper/shadow process. The prospective sample was too small to make a strong statistical conclusion about the underlying phenomenon.

I later tested the same general idea across a broader equity universe, but that did not produce a candidate that I was comfortable promoting.

## Why I closed it

I closed the tested implementation because the evidence was not strong enough after considering:

- transaction costs
- turnover
- limited trade frequency
- execution sensitivity
- robustness across research stages

I did not want to keep changing the rules simply to make the historical numbers look better.

## What I learned

This project taught me that a **gross edge** is not the same thing as a **tradable edge**.

I also learned the importance of:

- point-in-time data
- forward-return analysis
- drawdown and trade distributions
- realistic costs
- out-of-sample thinking
- keeping a clear research trail

## Key terms

**Mean reversion:** the idea that an unusually high or low value tends to move back toward a longer-term level.

**Momentum / continuation:** the idea that an existing move may continue for some period.

**Z-score:** a measure of how far an observation is from its recent mean in units of standard deviation.

**MFE / MAE:** maximum favourable excursion and maximum adverse excursion. They describe the best and worst movement experienced during a trade.

**Point-in-time analysis:** calculating a signal using only information that was available when the signal was generated.

## Status

**Closed — no promoted trading implementation.**
