# Strategy 001A — Event Structure & Conditioning Diagnostics

**Status:** ✅ Complete — produced a continuation lead; no trading rule approved

This experiment followed the rejected symmetric mean-reversion baseline. It did not optimize parameters or create a trading rule. It tested whether the observed event behavior survived dependence controls and whether it was concentrated in predefined market conditions.

## Fixed diagnostics

1. Event clustering and a fixed 12-bar non-overlap filter.
2. Time of day.
3. Six-bar prior trend.
4. Prior 30-bar volatility regime.
5. Current volume relative to prior 30-bar median.
6. Absolute z-score severity.
7. Positive vs negative deviation continuation after non-overlapping events.

The fixed 12-bar cooldown equals the longest tested forward horizon and is a dependence diagnostic, not a tuned trading parameter.

## Result

The event stream was highly clustered: most raw events occurred within 12 bars of another event. The non-overlap filter materially reduced the number of observations while preserving the main directional pattern.

Positive-deviation events continued to show positive forward returns after the non-overlap filter. The effect was strongest when the prior six-bar trend was upward. Negative-deviation events were weaker and inconsistent.

The volatility and volume diagnostics did not provide a simple explanation for the effect. Late-session observations and larger deviations were interesting exploratory concentrations, but they were not promoted into optimized parameters.

## Interpretation

001A does **not** prove momentum. It provides a narrower hypothesis:

> A large positive deviation during an existing short-term uptrend may contain continuation information.

However, some of that return could be ordinary intraday drift or simply the continuation of the prior trend. Therefore 001A is not sufficient to build a trading strategy.

## Decision

**Mean reversion remains rejected. Continuation is a promising exploratory lead, not an approved strategy.**

The next experiment is **001B — Continuation Attribution**, which compares event outcomes with matched non-event behavior to determine whether the continuation adds information beyond ordinary intraday drift and recent trend.
