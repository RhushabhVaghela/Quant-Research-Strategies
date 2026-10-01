# Strategy 001 — Intraday Price Behaviour

## 1. The starting question

I started with a simple intraday question: **when price moves unusually far from its recent level, does it usually come back?**

This led me to test a **mean-reversion** idea. Mean reversion means that an unusually high or low price is expected to move back toward its recent average.

## 2. Why I chose this dataset

I used five-minute **GOLDBEES OHLCV** data.

I chose five-minute data because the project is focused on intraday behaviour, so a daily dataset would hide the short-term movement I was trying to study. GOLDBEES gave me a single, liquid instrument with enough intraday observations to study repeated events.

## 3. First test: does the move reverse?

I measured how far price had moved from its recent intraday mean and looked at the returns that followed large deviations.

The important result was that the data did **not** show the reversal pattern I expected. Large positive deviations were more often followed by positive returns.

That changed the research question.

Instead of asking, “does a large move reverse?”, I asked:

> **Could some large moves actually be followed by continuation?**

## 4. Second step: identify when continuation is stronger

The next step was to see whether the continuation behaviour was the same in every situation.

I separated events by recent direction and other simple conditions. The clearest pattern was stronger continuation after a positive prior move.

This was useful because it turned a broad observation into a more specific hypothesis:

**large positive deviation + prior positive direction may contain short-horizon continuation information.**

## 5. Why I moved to a formal point-in-time test

The pattern itself was not enough. It was measured after looking through historical data, so I needed to check whether the relationship still existed when the signal was defined using only information that would have been available at the time.

That is what **point-in-time (PIT)** analysis means: no future information is allowed into the signal.

The point-in-time comparison kept the continuation result visible at several short horizons, with the 30-minute horizon showing the clearest incremental result in the tested setup.

That justified moving from an event study to an actual trading rule.

## 6. Turning the hypothesis into a strategy

I froze a simple implementation rather than continuously changing it.

The trading rule used:

- five-minute data;
- a recent intraday mean and standard deviation;
- a **z-score** threshold for unusually large positive deviations;
- positive prior six-bar return;
- entry on the next bar;
- a fixed holding period;
- a session cooldown;
- no leverage or optimised position sizing.

A **z-score** expresses how far an observation is from its mean in standard-deviation units.

The backtest produced positive gross returns. At this stage, the obvious next question was not “how can I make the return higher?” It was **“does the edge survive trading costs?”**

## 7. Execution and robustness checks

I then looked at the trade distribution, holding periods, forward-return path, and different chronological periods.

I also used **MFE** and **MAE**:

- MFE (maximum favourable excursion) measures the best movement in the trade's favour.
- MAE (maximum adverse excursion) measures the worst movement against the trade.

These checks helped me understand whether the result was broad or mainly driven by a few trades, and whether the entry-to-exit path supported the original holding period.

The gross result remained interesting, but the edge was small enough that transaction costs and execution assumptions mattered a lot.

## 8. Why I tested a prospective period

Historical research had already been inspected, so I needed a period that could not be changed after seeing the outcome.

I therefore used a **prospective paper/shadow** process. Signals were recorded before their outcomes were known, and the rules were kept fixed.

Only two selected observations were produced in that initial prospective run. That was not enough to reject the underlying continuation observation, but it was also not enough to establish strong evidence for a live strategy.

## 9. Why I tested a broader universe

The next question was whether the behaviour was specific to GOLDBEES or could be used across more liquid NSE equities.

I therefore tested the same economic idea across a broader universe.

The broader search did not produce a candidate that was strong enough after considering costs and stability. At that point, continuing to search the same historical sample would have increased the risk of overfitting.

## 10. Conclusion

I closed the tested implementation.

The main lesson was that a **gross statistical edge** and a **tradable edge** are different things. The continuation behaviour was interesting enough to study, but the tested implementations did not establish sufficiently strong economics after execution costs and the constraints of the research process.

### Key terms

**Mean reversion:** tendency for an unusually high or low value to move back toward a recent level.

**Continuation / momentum:** tendency for an existing move to continue for some period.

**Z-score:** distance from the mean measured in standard deviations.

**Point-in-time:** only information available at the decision time is used.

**MFE / MAE:** best and worst movement experienced while a trade is open.

**Transaction cost:** the direct cost of entering and exiting a trade.

**Overfitting:** fitting historical noise so closely that the result does not generalise.

## Status

**Closed — no promoted trading implementation.**
