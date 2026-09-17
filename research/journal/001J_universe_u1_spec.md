# Strategy 001J — Universe U1 Specification

**Status:** Tactical broker-native U1 locked for the September 2026 sprint; PIT Nifty 100 remains a deferred clean-universe path.

## Primary universe — U1

U1 is a **Kite-native liquid NSE equity universe** formed before any Strategy 001J outcome is evaluated.

The current Kite instrument dump provides the live tradable NSE EQ instrument set and instrument tokens. Kite's historical API then supplies 5-minute OHLCV for those instruments. The repository's existing authentication and historical-data layers are used; credentials remain local.

The U1 formation rule is fixed:

1. download current NSE EQ instruments from Kite;
2. fetch 5-minute OHLCV over a pre-declared formation window;
3. calculate daily traded value as `sum(close * volume)` across 5-minute bars;
4. require at least 15 formation days;
5. rank by median daily traded value;
6. select the top 50 symbols;
7. activate membership only after the formation window;
8. never use Strategy 001J P&L, win rate, drawdown, holdout results, or similarity rank to choose the universe.

The selection is therefore outcome-independent, but it is **not fully point-in-time clean** because Kite's current instrument dump does not reconstruct historical delistings or historical index membership. This limitation must remain visible in every 001J report and prevents treating this tactical universe as equivalent to PIT Nifty 100.

## Deferred clean universe

The original PIT Nifty 100 U1 remains a valid research path when historical constituent data is obtained. It is not being manufactured from today's list. This tactical U1 exists solely to make the same Strategy 001 hypothesis testable with the broker data already available to the project.

## Membership contract

The generated membership file remains:

```text
symbol,effective_from,effective_to
```

Intervals are half-open: `[effective_from, effective_to)`.

For the tactical U1, each selected symbol receives one membership interval beginning immediately after the formation window and ending at the frozen research-window boundary.

## Bar data

Primary research data:

- NSE equity;
- 5-minute OHLCV from Zerodha Kite Connect;
- exchange-local timestamps normalized to `Asia/Kolkata`;
- duplicate timestamps rejected;
- chronological order verified;
- missing-bar diagnostics retained;
- positive OHLC prices;
- non-negative volume.

Kite's historical API supports 5-minute candles and current instrument-token mapping. Historical intraday request limits require date-range chunking; the acquisition script uses conservative chunks and the API rate limit rather than assuming one request can cover an arbitrary period.

## Liquidity/data eligibility

The liquidity rule is frozen before Strategy 001J performance evaluation. The formation window determines the U1 membership. The backtest must not alter U1 because a symbol produces more attractive strategy results.

## Exclusions

U1 excludes:

- ETFs, including GOLDBEES;
- futures and options;
- leveraged/inverse products;
- non-NSE-EQ instruments;
- instruments without sufficient formation-window data;
- instruments with unresolved data-integrity problems.

GOLDBEES remains the frozen 001D reference and is not eligible for U1.

## Promotion caveat

Because U1 is based on the current broker instrument universe, the experiment has a survivorship/current-instrument limitation. A positive result can support further research and prospective testing, but it cannot by itself establish the same level of historical-universe validity as a true PIT constituent study.
