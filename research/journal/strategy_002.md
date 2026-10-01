# Strategy 002 — Cross-Sectional Statistical Research

## 1. Why I started a second strategy

After Strategy 001, I did not want to build another version of the same single-instrument continuation idea.

I changed the question completely:

> **Can I separate broad market movement from asset-specific movement, and does that asset-specific component tend to reverse?**

This led to a **cross-sectional residual** approach.

Cross-sectional analysis compares several assets at the same point in time. A residual is the part of a return left after removing the component explained by another variable, such as the broader market.

## 2. Why I chose a cross-sectional equity dataset

I used a group of Indian equities with common five-minute observations.

The five-minute frequency kept the research intraday, while several equities allowed me to compare stocks against one another at the same timestamp. That was important because the hypothesis was about **relative behaviour**, not the direction of one individual asset.

I also used market-level information so that the residual was not simply measuring whether the whole market was rising or falling.

## 3. First step: look for cross-sectional structure

I first examined whether the individual stock returns had a common market component and whether the remaining residuals showed a repeatable pattern.

The exploratory work showed enough structure to justify a more formal test.

That led to the next question:

> **Does a simple residual-reversal portfolio actually make money after the signal is turned into a trade?**

## 4. Formal baseline

I built a fixed, one-bar executable baseline.

The idea was straightforward: rank stocks using their residual behaviour and test whether the stocks with the most unusual residuals tended to move back toward the cross-sectional centre on the next five-minute bar.

The baseline was intentionally simple because I wanted to measure the underlying effect before adding more conditions.

The chronological validation produced only a very small positive gross effect.

That result changed the focus from signal discovery to economics.

## 5. Why I tested holding periods

One possible problem was turnover.

**Turnover** measures how much of the portfolio is traded relative to its size. A strategy that makes many small trades can show a statistical relationship but still lose money after costs.

I therefore tested longer holding periods to see whether reducing trading frequency improved the result.

The tested holding-period variants did not produce enough gross return to create a viable cost-adjusted candidate.

## 6. Why I stopped

At this point, continuing to tune the same idea would have meant repeatedly searching the same historical sample for a better result.

That creates **data-snooping** and overfitting risk: the more choices I make after seeing the data, the harder it becomes to tell whether the final result is genuine.

I therefore closed the tested research line rather than trying to manufacture a stronger backtest.

## 7. Conclusion

Strategy 002 did not establish enough economic value to justify promotion.

The research was still useful because it showed me the difference between:

- finding a statistical relationship;
- building an executable portfolio;
- and finding an effect large enough to survive trading costs.

### Key terms

**Cross-sectional:** comparing multiple assets at the same time.

**Residual:** the part left after removing an estimated explanatory component.

**Residual reversal:** a hypothesis that an unusually positive residual may be followed by a negative return, and vice versa.

**Market neutral:** reducing exposure to broad market direction.

**Turnover:** trading volume relative to portfolio size.

**Data snooping:** using repeated choices based on the same historical data in a way that can make a result look stronger than it really is.

## Status

**Closed — no promoted trading implementation.**
