# Strategy 002 — Intraday Statistical Arbitrage / Pairs Mean Reversion

**Registration date:** 2026-09-18  
**Status:** Research specification registered; no development result yet  
**Asset class:** Indian equities  
**Mechanism:** Relative-value / statistical arbitrage  
**Primary data:** Zerodha/Kite 5-minute OHLCV  
**Broker:** Zerodha/Kite  
**Parent portfolio role:** Diversifying mechanism from Strategy 001 directional continuation

## 1. Research question

Can short-lived relative mispricing between sufficiently stable, liquid equity pairs be identified and traded intraday as a market-neutral spread-normalization signal after realistic execution costs?

This is deliberately different from Strategy 001. Strategy 001 asks whether an unusually strong move continues. Strategy 002 asks whether the **relative spread between two securities temporarily deviates from its historical relationship and subsequently normalizes**.

## 2. Data and feasibility

Kite's historical API provides archived candle data for tradable instruments at minute and multi-minute intervals, and the instrument master provides the tradable NSE equity universe and instrument tokens. citeturn1search0turn1search4

The first implementation will therefore use the existing broker-native U1 equity data already acquired for 001J rather than introducing a new external data dependency.

The research must explicitly test whether the selected pair legs are simultaneously tradable and sufficiently liquid. A statistical edge that cannot be executed on both legs is not a deployable arbitrage result.

## 3. Universe

The initial candidate universe is the locked U1 top-50 Kite-native liquid NSE EQ universe.

Pair selection is **formation-only** and must not use development or holdout P&L.

The formation stage will:

1. align each symbol's 5-minute returns;
2. remove pairs with inadequate overlapping observations;
3. measure pairwise dependence using predefined diagnostics;
4. estimate a spread relationship on the formation sample;
5. reject unstable or structurally broken relationships;
6. freeze the eligible pair set before development.

No pair may be selected because it performed well in development.

## 4. Economic hypothesis

Related liquid equities can temporarily diverge because of idiosyncratic order flow, temporary liquidity imbalance, or short-lived relative repricing.

If a pair has a sufficiently stable historical relationship, an unusually large standardized spread deviation may have a higher probability of normalization than continuation.

The hypothesis is explicitly **relative-value mean reversion**, not directional mean reversion in a single stock.

## 5. Signal architecture

The initial architecture will be deliberately simple and interpretable:

- estimate a hedge relationship using formation data;
- construct a signed pair spread;
- standardize the spread using only information available before the signal;
- enter when the spread z-score exceeds a preregistered absolute threshold;
- long the relatively cheap leg and short the relatively rich leg;
- exit on spread normalization, a maximum holding period, or a predefined risk stop;
- prohibit overnight carry in the first live-feasibility version;
- enforce same-session entry and exit.

## 6. Point-in-time discipline

At every signal timestamp:

- pair membership must already be frozen;
- hedge parameters must use only data available before the signal;
- the current bar cannot be used to compute a statistic that determines entry at that same bar's open;
- both legs must have valid observations;
- entry prices must reflect the next executable bar;
- both legs must be accounted for in gross and net P&L.

A missing leg invalidates the pair trade rather than silently substituting a stale price.

## 7. Development / holdout structure

Use the same frozen September 2026 research split unless a data-integrity issue requires a separately registered window:

- formation: 2026-05-12 through 2026-06-09;
- development: 2026-06-10 through 2026-08-19;
- holdout: 2026-08-20 through 2026-09-17.

The pair universe and hedge relationships must be frozen before development candidate selection.

The holdout remains inaccessible until a candidate freeze record is completed.

## 8. Registered development search

The first development search should remain small enough to avoid another uncontrolled parameter sweep.

Candidate dimensions:

- spread lookback: 60, 120, 240 completed 5-minute bars;
- entry absolute z: 2.0, 2.5, 3.0;
- exit absolute z: 0.5, 1.0;
- maximum holding: 3, 6, 12 bars;
- cooldown: 6, 12 bars.

This is a fixed 108-configuration family.

No second development grid may be opened merely because the first grid produces an inconvenient result. Any sequential search requires a new preregistration and explicit overfitting warning.

## 9. Evaluation

Required metrics:

- pair trades;
- distinct pairs;
- distinct symbols;
- mean and median pair return;
- win rate;
- profit factor;
- maximum loss/gain;
- maximum concurrent pair positions;
- gross and net return;
- 5/10/15/20 bps **per-leg-aware** cost scenarios;
- pair concentration;
- leg concentration;
- sector concentration where classification is available;
- turnover;
- holding time;
- chronological early/middle/late stability;
- spread-z distribution;
- percentage of trades reaching the normalization region;
- adverse excursion and maximum pair loss.

A pair-level result is not treated as 100 independent observations merely because the same stock participates in many pairs.

## 10. Execution and cost model

Pairs trading creates two execution streams. Costs must therefore be modeled for both legs.

The research must distinguish:

1. theoretical spread return;
2. executable two-leg gross return;
3. brokerage/statutory charges;
4. bid/ask spread;
5. slippage;
6. legging risk;
7. rejected/partial fills.

A candidate cannot be promoted on a single-leg or theoretical spread calculation.

## 11. Live-feasibility constraint

The first version is intended to be **intraday only**.

This avoids relying on overnight cash-equity short availability and reduces corporate-action and borrow complications.

Live promotion additionally requires evidence that both legs can be entered and exited with acceptable synchronization and that the strategy remains economically meaningful after two-leg costs.

## 12. Promotion gates

A Strategy 002 candidate must pass:

1. formation-only pair selection;
2. reproducible broker data;
3. point-in-time hedge estimation;
4. no lookahead;
5. chronological development stability;
6. parameter-neighborhood stability;
7. pair and leg breadth;
8. realistic two-leg costs and slippage;
9. execution synchronization feasibility;
10. untouched holdout validation;
11. prospective paper/shadow validation;
12. explicit risk and position limits.

Failure is a valid research outcome.

## 13. Portfolio role

Strategy 002 is intentionally registered as a different mechanism from Strategy 001.

001: directional intraday continuation.  
002: relative-value intraday mean reversion.

The portfolio must not promote two strategies that are economically redundant simply because their parameter values or symbols differ.
