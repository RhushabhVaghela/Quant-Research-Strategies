# Strategy 001J — Secondary Development Experiment: Cost-Efficiency Search

**Registration date:** 2026-09-18  
**Phase:** Secondary/exploratory development; holdout remains unopened  
**Parent strategy:** 001 — intraday continuation  
**Universe:** U1 — locked Kite-native liquid NSE EQ top 50  
**Frequency:** 5-minute OHLCV

## 1. Motivation

The first preregistered 162-configuration development grid established that several configurations showed small positive gross mean returns across chronological development subperiods, but the effect was only a few basis points per trade and did not survive the predefined 5 bps round-trip sensitivity.

This secondary experiment therefore tests a narrower economic question:

> Can the registered intraday continuation effect be expressed with stronger signals and/or shorter holding periods so that per-trade expectancy is less vulnerable to execution costs?

This is a **new exploratory development stage**, not a reopening of the first grid and not a modification of frozen 001D. Because it uses the same development sample after the first development review, the risk of development overfitting is higher and must be acknowledged in the eventual freeze record.

## 2. Data boundary

Only the frozen development window is permitted:

- 2026-06-10 through 2026-08-19 inclusive.
- U1 membership remains unchanged.
- No holdout file, timestamp, result, or statistic may be read.

The chronological holdout remains:

- 2026-08-20 through 2026-09-17 inclusive.

The holdout is not part of this experiment.

## 3. Registered candidate family

The exact grid is fixed before execution:

| Parameter | Values |
|---|---|
| lookback_bars | 20, 30, 40 |
| z_threshold | 2.5, 3.0, 3.5 |
| trend_bars | 3, 6, 9 |
| holding_bars | 3, 6 |
| cooldown_bars | 12, 24 |

Total configurations: **108**.

This family deliberately removes the lower z-threshold values from the first grid and adds stronger thresholds, while testing shorter holding periods and a longer cooldown. The change is motivated by the measured cost bottleneck, not by any holdout observation.

## 4. Evaluation

Each configuration is evaluated independently. No automatic winner is selected.

Required outputs include:

- number of trades;
- distinct symbols;
- mean and median gross trade return;
- win rate;
- profit factor;
- maximum individual loss/gain;
- chronological subperiod behavior;
- positive-symbol breadth;
- maximum concurrent entries;
- net mean return under 5, 10, 15 and 20 bps round-trip haircuts;
- trade-count reduction versus the first 162-grid where comparable configurations exist.

The principal economic screen is **cost resilience of per-trade expectancy**, not cumulative return.

A configuration that produces fewer trades is not automatically preferable. Reduced frequency is useful only if the remaining trades exhibit stronger and sufficiently stable expectancy.

## 5. Selection discipline

The experiment is exploratory and must not be treated as an independent confirmation of the same development sample.

Before any holdout access:

1. Review the complete 108-row grid.
2. Review chronological stability.
3. Review parameter-neighborhood behavior.
4. Review breadth and concentration.
5. Review cost-adjusted expectancy.
6. Record one candidate or explicitly record that none is sufficiently supported.
7. Record the sequential-development limitation in the freeze record.

No candidate may be chosen using holdout results.

## 6. Promotion discipline

Even if a candidate survives this secondary development stage, it is **not** considered validated.

A frozen candidate must subsequently be evaluated once on the untouched chronological holdout. If the holdout is acceptable, the candidate still requires prospective paper/shadow validation, execution/capacity review, and risk controls before any live capital.

If no candidate survives conservative cost assumptions, Strategy 001J should not be forced into live deployment.

## 7. Reproducibility

The implementation is a separate script with frozen constants and an explicit assertion that the grid contains exactly 108 configurations. It reads only the locked U1 data and development dates.

Generated reports should be stored under:

`data/reports/strategy_001j_secondary_development/`

No generated report from this experiment may be used to alter U1 membership retrospectively.
