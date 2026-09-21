# Strategy 002 — Candidate Baseline Specification

**Status:** Candidate baseline prepared; temporal-stability gate must pass before chronological validation opens.

## Purpose

Provide one simple, pre-specified executable baseline for testing the Strategy 002 hypothesis. This is not an optimized strategy.

## Universe

Use the existing Strategy 002 research universe after the structural-quality gate:

- 19 eligible instruments;
- HINDUNILVR excluded for the documented audit failure.

Do not add or remove instruments based on validation performance.

## Signal

At the close of each completed 5-minute bar:

1. calculate each eligible instrument's 5-minute close-to-close return;
2. calculate the equal-weight mean return of all **other** eligible instruments;
3. calculate the leave-one-out residual;
4. classify residuals:
   - negative residual -> long signal;
   - positive residual -> short signal.

No z-score, residual threshold, lookback optimization, volatility filter, sector filter, or additional feature is permitted.

## Portfolio construction

When both long and short signals exist at a timestamp:

- allocate equal notional to all long signals within the long sleeve;
- allocate equal notional to all short signals within the short sleeve;
- make the two sleeves equal gross notional;
- maintain zero net notional at signal construction;
- do not use leverage beyond the equal-gross baseline;
- do not rank securities by residual magnitude.

If one side is empty, do not open a portfolio for that timestamp.

This is a market-neutral baseline intended to isolate the cross-sectional mechanism rather than market direction.

## Execution timing

- signal: completed bar close;
- entry: next 5-minute bar open;
- exit: next 5-minute bar close;
- holding period: exactly one 5-minute bar;
- no overnight positions;
- no overlapping restriction beyond the portfolio being reconstituted at each signal timestamp.

The baseline is deliberately simple. Execution feasibility and costs must be evaluated before any live consideration.

## Development and validation

The baseline definition is fixed, but chronological validation must not begin until the preceding temporal-stability gate is reviewed and documented.

- Exploratory development: 2025-09-18 through 2026-06-09.
- Chronological validation: 2026-06-10 through 2026-08-19.
- Final holdout/OOS: 2026-08-20 through 2026-09-17.

The validation period may now be used to evaluate this fixed baseline.

The final holdout remains locked until:

1. validation evaluation is complete;
2. any permitted development decisions are documented;
3. a candidate is frozen;
4. the holdout evaluation procedure is frozen in advance.

## Cost policy

Initial evaluation must report:

- gross return;
- explicit transaction-cost sensitivity;
- execution assumptions;
- long/short leg turnover;
- distribution of trade-level outcomes;
- capacity/liquidity diagnostics where available.

No cost assumption may be tuned to make the strategy pass.

## Promotion gate

A positive validation result alone is insufficient. Promotion requires:

- reproducible implementation;
- correct timing;
- stable validation behavior;
- realistic costs/slippage;
- adequate liquidity and capacity;
- risk controls;
- prospective/paper evidence.

No live capital is authorized by this document.
