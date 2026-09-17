# Strategy 002 — Universe U1 Specification

**Status:** 🟡 Defined — point-in-time constituent data acquisition pending.

## Purpose

U1 is the first broad equity universe for the accelerated Strategy 002 research track. The universe is deliberately defined before strategy performance is examined so that symbol selection is not optimized from backtest results.

## Primary universe

**Nifty 100 constituents, using point-in-time effective membership.**

Nifty 100 is a broad large-cap universe representing 100 companies from the Nifty 500 and combining Nifty 50 and Nifty Next 50. NSE Indices states that Nifty 100 represents about 64.95% of NSE free-float market capitalization and about 40.93% of traded value based on the six months ending March 2026. The index is reconstituted semi-annually in March and September.

Reference: NSE Indices Nifty 100 documentation and index reconstitution calendar.

## Critical anti-survivorship rule

The current September 2026 constituent list must **not** simply be applied to the entire historical sample.

For historical research, membership must be represented as:

```text
symbol | effective_from | effective_to
```

A symbol is eligible for a historical bar only when it was a member of U1 on that date.

If point-in-time membership cannot be reconstructed for a historical period, that period may be used only as an explicitly labeled exploratory/survivorship-biased analysis and must not be presented as the final OOS evidence.

## Liquidity eligibility

Membership alone is not enough for execution research. At each historical decision point, the implementation should additionally verify:

1. sufficient 5-minute OHLCV coverage;
2. no material missing-bar problem;
3. positive and plausible prices/volume;
4. adequate recent trading activity;
5. no unresolved corporate-action/data adjustment problem;
6. instrument is actually tradable through the intended execution venue;
7. the symbol has enough history to construct the required intraday features.

The exact liquidity thresholds will be frozen before the final Strategy 002 backtest. They must not be selected because they maximize historical P&L.

## Exclusions for the first sprint

The first U1 experiment excludes:

- illiquid small-cap names outside the defined universe;
- newly listed securities without sufficient history;
- symbols with unresolved data integrity issues;
- securities that cannot be reliably mapped to the broker instrument master;
- options/futures;
- leveraged or inverse products;
- ETFs such as GOLDBEES for the primary equity-universe experiment.

GOLDBEES remains the historical Strategy 001 instrument and is not mixed into U1.

## Data frequency

Primary research frequency:

**5-minute OHLCV.**

The architecture should retain the symbol and timestamp dimensions so the same signal engine can process multiple instruments without mixing observations across symbols.

## Portfolio-level controls

The research engine must eventually support:

- maximum simultaneous positions;
- per-symbol position limits;
- sector exposure limits;
- daily turnover;
- signal clustering controls;
- one-signal-per-symbol cooldown;
- cross-sectional concentration reporting.

These controls are not to be optimized from the final holdout.

## Universe expansion

U1 is intentionally conservative for the first sprint. After the pipeline is validated, expansion candidates are:

1. Nifty 200 / broader large-mid-cap universe;
2. liquid mid-cap subset;
3. separately defined sector universes;
4. other asset classes.

Each expansion receives a new universe identifier and is recorded before its performance is evaluated.

## Acceptance criteria

U1 is considered ready for historical Strategy 002 research only when:

- point-in-time membership is available for the research period;
- symbol identifiers map consistently to raw data;
- coverage diagnostics are reproducible;
- no future constituent information leaks into historical eligibility;
- the final universe rules are committed before candidate performance selection.
