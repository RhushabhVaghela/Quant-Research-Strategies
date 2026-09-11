# Phase 1 — Market Data Specification

## Objective
Build a reliable 5-minute OHLCV data layer before researching an intraday strategy.

## Initial hypothesis
A sufficiently large intraday directional move may have different continuation
or reversal behavior depending on volatility, volume, time of day, recent trend,
and broader market state.

## Event-study inputs
- recent return
- return z-score
- range expansion
- realized volatility
- relative volume
- distance from VWAP/reference
- trend strength
- market/index return
- time of day

## Forward outcomes
+5, +10, +15, +30, +60 minutes.

## Data-quality rules
1. Unique, sorted timestamps.
2. Timestamps represented in Asia/Kolkata.
3. Positive OHLC prices.
4. High >= open and close.
5. Low <= open and close.
6. Non-negative volume.
7. Investigate missing/invalid observations rather than silently filling them.
8. Resolve instrument tokens dynamically from the current instrument master.

Research sequence:
hypothesis -> data -> event study -> statistical test -> baseline ->
conditional features -> ML if justified -> walk-forward/OOS -> costs ->
paper/shadow -> controlled live validation.
