# Phase 1 — Intraday Dataset Audit

This phase sits between data ingestion and strategy research.

## Why this exists

A successful API download does not automatically mean the dataset is suitable
for research. We need to understand session structure, timestamp spacing,
missing intraday intervals, volume behavior, return distributions, and time-of-
day effects before defining a trading event.

## First command

After downloading a local dataset:

```bash
python scripts/audit_historical.py data/raw/NSE_NIFTYBEES_5minute.csv
```

The audit:

- re-runs the existing OHLCV validation;
- counts trading sessions and bars per session;
- checks for unexpected gaps *within* a trading session;
- reports zero-volume observations;
- summarizes 5-minute return behavior without crossing overnight boundaries;
- produces a time-of-day profile for returns and volume.

## Important interpretation rule

An overnight/weekend/holiday gap is not automatically a missing 5-minute bar.
The audit therefore checks interval continuity only when two consecutive bars
belong to the same session date.

## What comes next

We will use the output to decide whether the dataset is ready for an event
study. We will not optimize a strategy from this diagnostic output.

The eventual research question remains:

> Are unusually large intraday directional moves associated with different
> continuation/reversal behavior under different volatility, volume, time-of-
> day, trend, and market-state conditions?

The first event-study implementation should be built only after the session
and data-quality assumptions have been inspected on actual downloaded data.
