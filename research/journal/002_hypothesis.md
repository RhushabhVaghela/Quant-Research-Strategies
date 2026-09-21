# Strategy 002 — Economic Hypothesis

**Status:** Preregistered hypothesis; temporal-stability gate passed descriptively. Chronological validation not yet evaluated.

## Hypothesis

**Short-horizon idiosyncratic residual reversal hypothesis**

For an eligible Indian equity/ETF, when its 5-minute close-to-close return is negative relative to the contemporaneous returns of the other eligible instruments, the instrument's subsequent 5-minute residual return will tend to be positive. Conversely, a positive residual will tend to be followed by a negative residual.

The mechanism proposed is temporary stock-specific price pressure / liquidity imbalance causing part of a short-horizon relative move to mean-revert.

This is a falsifiable hypothesis, not a claim that the mechanism has been proven.

## Formal definition

For instrument i at completed 5-minute bar t:

r(i,t) = close(i,t) / close(i,t-1) - 1

m(-i,t) = mean(r(j,t)) for all eligible j != i

residual(i,t) = r(i,t) - m(-i,t)

Prediction:

- residual(i,t) < 0 -> expected residual(i,t+1) > 0
- residual(i,t) > 0 -> expected residual(i,t+1) < 0

The leave-one-out construction is fixed and must not be changed after validation results are observed.

## Timing

The signal is known at the close of bar t.

A baseline implementation therefore enters at the next bar open and evaluates the next-bar close-to-close residual outcome. No information from the future bar may enter the signal.

## Primary prediction

The primary confirmatory prediction is the **next 5-minute bar**.

The exploratory evidence showed materially weaker effects at 2 bars and beyond. The 1-bar horizon is therefore fixed for the initial validation rather than selected after seeing validation results.

## Null hypothesis

There is no systematic relationship between the sign of the completed-bar leave-one-out residual and the sign of the next-bar leave-one-out residual.

## Disconfirming evidence

The hypothesis should not advance if validation shows one or more of the following:

- the sign relationship disappears materially;
- the cross-sectional breadth collapses;
- the effect is unstable across chronological validation subperiods;
- the effect is smaller than plausible execution/friction;
- the relationship requires a threshold or subset chosen from validation data;
- the result depends on a data-quality exception;
- the effect cannot be implemented using information available at the signal time.

## Exploratory evidence already observed

Within the locked exploratory period:

- negative residual -> median next-bar residual **+3.9211 bps**; **94.7%** positive instruments;
- positive residual -> median next-bar residual **−4.4816 bps**; **0%** positive instruments;
- negative residual -> next close-to-open **+2.1336 bps** and next open-to-close **+2.1737 bps**;
- positive residual -> next close-to-open **−2.4452 bps** and next open-to-close **−0.9523 bps**.

These numbers are development evidence only. They must not be treated as validation or holdout evidence.

## Scope

The hypothesis applies only to the predefined Strategy 002 research universe and its existing structural-quality gate.

HINDUNILVR remains excluded because of its unresolved structural data-quality failure.

No universe expansion, threshold search, parameter grid, or ML model is part of this hypothesis test.
