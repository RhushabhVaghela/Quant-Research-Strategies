# Strategy 002 — Accelerated Multi-Asset Research Roadmap

**Status:** 🟡 Research initiated — historical universe construction is the next gate.

## Why Strategy 001 is closed for capital pursuit

Strategy 001 established a real, historically positive GOLDBEES intraday continuation effect and a reproducible frozen implementation. The 001D rule was subsequently subjected to execution-cost, decomposition, replay, and chronological robustness work.

The 001I prospective collector then produced the first genuinely prospective observations on 2026-09-17. Only two selected trades were generated during the session. Both were negative:

| Signal | Paper entry | Paper exit | Gross return |
|---|---:|---:|---:|
| 12:00 | 124.31 | 124.21 | -8.04 bps |
| 13:05 | 124.87 | 124.71 | -12.81 bps |

The sample is far too small to statistically reject the continuation hypothesis. The operational conclusion is different: **the frozen GOLDBEES implementation is too low-frequency to be the primary capital-deployment candidate for the September 2026 project deadline.**

The 001D parameters therefore remain frozen and are not optimized using the two prospective observations. 001I is closed as a capital-pursuit experiment rather than kept active for weeks merely to accumulate a checkpoint sample.

This is a **research-priority decision, not a claim that Strategy 001 is statistically disproven**.

## New objective

Build a reusable multi-asset research framework capable of testing systematic intraday hypotheses across a predefined, liquid Indian equity universe.

The first Strategy 002 hypothesis will deliberately reuse the economic structure discovered in Strategy 001 — short-horizon intraday continuation after an unusually strong move — but it will be tested across a broader equity universe and will have a separately registered parameter-selection process.

If that hypothesis does not survive the broader universe, we will stop it and move to a different hypothesis or asset class. We do not force Strategy 002 to succeed merely because it is derived from Strategy 001.

## Research sequence

```text
U1 point-in-time universe
        ↓
Data coverage / corporate-action / liquidity audit
        ↓
Strategy 002 baseline using 001D parameters
        ↓
Cross-sectional historical event study
        ↓
Pre-registered parameter-selection experiment on development period only
        ↓
Frozen 002 candidate
        ↓
Chronological holdout
        ↓
One-session prospective paper/shadow validation
        ↓
Execution-cost audit
        ↓
Separate controlled-live validation
```

## Frequency objective

Trade frequency is an engineering constraint, not a performance target.

The accelerated research track should seek enough observations to make rapid research decisions, with an initial design target of roughly **20–50 candidate/selected opportunities per session across the universe**. If the economics require excessive turnover or the signal is too sparse, the hypothesis is rejected or redesigned as a new experiment.

We will **not** lower thresholds or otherwise alter rules solely to manufacture 100+ trades/day.

## Parameter discipline

The first baseline uses the exact frozen 001D parameters:

- lookback = 30 bars;
- z threshold = +2.0;
- prior trend = 6 bars;
- holding period = 6 bars;
- cooldown = 12 bars;
- long-only;
- next-bar-open entry;
- exit at t+6 close.

Only after the baseline is recorded may a separate parameter experiment be run. The parameter search must be narrow, pre-registered, and evaluated on a development period only. The selected configuration is then frozen before chronological holdout and prospective testing.

## Pre-registered parameter experiment

The initial grid is intentionally small:

- lookback: 20, 30, 40 bars;
- z threshold: 1.5, 2.0, 2.5;
- prior-trend window: 3, 6, 9 bars;
- holding period: 3, 6, 9 bars;
- cooldown: 6, 12 bars.

This is a research grid, not permission to select the best-looking combination after inspecting the holdout. The number of tested configurations and all results must be retained.

## Evaluation

Every candidate must report:

- number of signals and selected trades;
- trade return distribution;
- mean and median gross return;
- explicit cost scenarios;
- net return under each scenario;
- win rate and profit factor;
- maximum drawdown;
- turnover;
- exposure;
- symbol concentration;
- sector concentration;
- time-of-day concentration;
- cross-sectional and market-regime dependence;
- number of distinct symbols contributing observations;
- performance before and after the selection/freeze boundary.

A large trade count is not sufficient. Correlated signals generated simultaneously by the same market move must not be treated as fully independent evidence.

## Deadline plan — September 2026

### 17–18 September

1. Freeze the U1 universe definition.
2. Obtain/validate point-in-time membership data.
3. Audit available 5-minute OHLCV coverage.
4. Generalize the existing continuation engine from one symbol to symbol × timestamp.
5. Run the 001D-parameter baseline across U1.

### 19–21 September

1. Complete the cross-sectional baseline event study.
2. Run the pre-registered parameter experiment on the development sample.
3. Freeze the candidate configuration.
4. Run chronological holdout and cost sensitivity.

### 22–24 September

1. Build live multi-symbol paper/shadow capture.
2. Validate signal timestamps, next-bar execution, duplicate handling, and broker data.
3. Run at least one full-session prospective paper test.

### 25–27 September

1. Audit paper outcomes against the historical model.
2. Measure actual quoted spreads and observable execution friction.
3. Run the controlled-live readiness review.

### 28–30 September

If — and only if — the predefined gates pass, perform a **small controlled live validation** with explicit capital and risk limits. Otherwise preserve the candidate as a paper-tested research result rather than forcing deployment to satisfy the calendar.

## Portfolio architecture

Strategy 002 is intentionally being built as a reusable multi-symbol strategy rather than another one-off ticker script. Future strategies should consume the same universe, data, signal, execution, cost, and validation layers.

This is the infrastructure step that allows several strategies to be researched in parallel instead of waiting for one instrument to generate enough trades.
