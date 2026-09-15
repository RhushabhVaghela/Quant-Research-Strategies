# Strategy 001C — Frozen Continuation Hypothesis Specification

**Status:** 🟡 Research specification frozen — validation pending

## Purpose

001C converts the 001B research lead into a precise, testable hypothesis before we expand to the predefined research universe or optimize anything.

The original Strategy 001 symmetric mean-reversion hypothesis remains **rejected**. The surviving lead is directional: unusually large positive deviations that occur while the recent short-term trend is already positive appear to be followed by continued positive returns.

This document is the contract for the next validation stage. Parameters defined here are fixed for the baseline experiment. They must not be changed after seeing instrument-level performance.

## Frozen hypothesis

> **When a 5-minute bar closes at least 2.0 standard deviations above the mean of the previous 30 completed 5-minute closes, and the prior six-bar return is positive, the subsequent return over a fixed 30-minute horizon will be positive and stronger than the historical point-in-time return of comparable non-event observations.**

This is a research hypothesis. It is not yet an approved trading rule.

## Frozen event definition

For bar `t`:

1. Compute the mean of the previous **30 completed closes**, excluding bar `t`.
2. Compute the sample standard deviation of those same 30 closes.
3. Compute the current deviation z-score:

   `z_t = (close_t - mean(previous_30_closes)) / std(previous_30_closes)`

4. A continuation event requires `z_t >= +2.0`.
5. The event also requires the prior six-bar return to be positive.
6. All event inputs must be known at the event-bar close.
7. The event is evaluated independently within each trading session; no overnight bars are used to form the 30-bar deviation lookback or six-bar trend.

The event is therefore deliberately **one-sided**. Negative deviations are not part of the baseline continuation rule because 001B did not support a symmetric counterpart.

## Frozen trend definition

The trend feature is the existing Strategy 001A definition:

`prior_return_6bar = close[t-1] / close[t-7] - 1`

- `up`: prior return > 0
- `flat`: prior return = 0
- `down`: prior return < 0

001C requires `up`.

No trend threshold is introduced and no threshold search is permitted in this stage.

## Frozen holding horizon

**30 minutes = 6 five-minute bars.**

The 30-minute horizon is selected as the baseline because it is a middle horizon in the already-defined 5/15/30/60-minute diagnostic grid and provides a practical balance between very short execution noise and longer exposure. It is **not** selected because it produced the highest observed historical return.

The other horizons remain diagnostic sensitivity checks, not optimization targets.

## Frozen execution convention for the first trading baseline

The event is observed at the close of bar `t`.

- Signal decision: after bar `t` closes.
- Earliest entry: **next bar open (`t+1`)**.
- Baseline holding period: exit at the close of bar `t+6`.
- No same-bar entry is permitted.
- If the next bar is unavailable or the six-bar future path crosses a session boundary, the observation is invalid for this baseline.

This convention is intentionally conservative relative to the event-study measurement, which used close-to-close forward returns.

## Overlap policy

The primary trading baseline uses a fixed **12-bar event cooldown** within each session, inherited from 001A. After one selected event, subsequent events inside the next 12 bars are ignored.

The cooldown is a dependence-control convention, not a tuned trading parameter.

## Point-in-time benchmark

The event's historical benchmark must be constructed using only information that would have been available when the trade decision was made.

For an event at timestamp `t`, an eligible benchmark observation must satisfy all of the following:

- it was a non-event observation;
- it belongs to the same predefined time-of-day bucket;
- it belongs to the same prior-trend bucket;
- its six-bar forward outcome has **fully completed strictly before `t`**;
- its forward return is observed and valid.

The benchmark is therefore not allowed to use future observations merely because their starting timestamps precede `t`. Their outcomes must already be known.

The implementation lives in `src/research/point_in_time_baseline.py`.

A minimum of **30 completed historical benchmark observations** is required before a point-in-time benchmark is considered available. This is a fixed data-sufficiency rule, not a performance-selection rule.

## What is frozen versus what is not

### Frozen now

- 5-minute bar frequency
- 30-bar deviation lookback
- sample standard deviation
- positive z-score threshold = 2.0
- prior trend = six-bar return > 0
- 30-minute primary holding horizon
- next-bar-open entry convention
- close-of-sixth-future-bar exit convention
- 12-bar session cooldown
- predefined time-of-day buckets from 001A
- point-in-time matched benchmark
- minimum 30 completed benchmark observations

### Not yet optimized or approved

- z-score threshold alternatives
- lookback alternatives
- trend thresholds
- holding-period selection
- stop-loss / take-profit rules
- position sizing
- leverage
- transaction-cost assumptions
- slippage assumptions
- order type
- instrument selection
- machine-learning filters

Those questions belong to later, explicitly identified experiments.

## Primary validation questions

1. Does the frozen event occur often enough across the predefined universe to be economically testable?
2. Is the event's point-in-time incremental return positive?
3. Is the relationship consistent across instruments rather than concentrated in GOLDBEES?
4. Does it survive realistic costs and execution assumptions?
5. Does it survive chronological out-of-sample / walk-forward testing?
6. Does the effect remain after controlling for ordinary market drift and trend?

## Decision gates

- **REJECTED:** the frozen relationship is absent, reverses, or fails basic robustness checks.
- **INCONCLUSIVE:** evidence is too sparse or unstable to distinguish signal from noise.
- **PROMISING:** the relationship is directionally consistent and survives the first point-in-time and cross-instrument checks, but costs/OOS are still pending.
- **ROBUST:** survives predefined robustness and chronological OOS tests.
- **PAPER READY:** robust and executable under realistic cost/slippage assumptions.
- **LIVE CANDIDATE:** only after paper/shadow validation and explicit risk controls.

## Research discipline

The most important rule for 001C is **no post-hoc parameter tuning on the same evidence used to discover the hypothesis**.

If the frozen hypothesis fails, the failure is recorded as a valid research result. A changed hypothesis must receive a new experiment identifier rather than silently modifying 001C.

## Next step

Run the point-in-time benchmark on GOLDBEES first as an implementation and leakage audit, then apply the exact frozen specification across the predefined multi-instrument universe. Do not rank instruments by the discovery sample and then select only winners.
