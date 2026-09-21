# Strategy 002 — Turnover-Reduction Development Experiment

**Status:** Registered development experiment; no results evaluated yet.

## Why this experiment exists

The frozen one-bar baseline failed the cost-resilience gate because its gross effect is only +0.0896 bps per portfolio observation while the implementation executes a full entry and exit every signal.

The turnover diagnostic shows that the problem is partly structural: the baseline is deliberately a one-bar round trip. A natural economic question is therefore whether the residual-reversal signal contains enough persistence to justify holding the selected portfolio for more than one bar.

This is a new development experiment under Strategy 002. It does not modify the frozen baseline.

## Data permission

Only the exploratory/development period may be used for selection:

**2025-09-18 through 2026-06-09**

The chronological validation period (**2026-06-10 through 2026-08-19**) and final holdout (**2026-08-20 through 2026-09-17**) are protected from this experiment.

## Pre-registered mechanism

At a completed 5-minute signal bar:

1. calculate the leave-one-out cross-sectional residual exactly as in the frozen baseline;
2. negative residual instruments form the long sleeve;
3. positive residual instruments form the short sleeve;
4. equal-weight each sleeve at 50% gross exposure;
5. enter the selected portfolio at the next bar open;
6. hold the same selected portfolio for a fixed number of bars;
7. exit at the close of the final holding bar;
8. do not overlap portfolios;
9. do not carry positions overnight;
10. do not rebalance while a portfolio is active.

The only experimental dimension is the fixed holding length.

## Pre-registered holding variants

| Variant | Holding length |
|---|---:|
| H2 | 2 bars / 10 minutes |
| H3 | 3 bars / 15 minutes |
| H6 | 6 bars / 30 minutes |

No additional holding lengths may be added after seeing results without registering a new search.

## Economic rationale

The original characterization showed that the residual-reversal effect was strongest at the next bar and weakened at longer horizons. That makes this a deliberately conservative turnover experiment: test only a small set of nearby holding lengths rather than searching broadly for the historical optimum.

The experiment asks whether reducing turnover can preserve enough of the reversal effect to improve net economics. It is not permitted to assume that longer holding is beneficial.

## Evaluation

For each holding variant report:

- number of trades/portfolio episodes;
- mean and median gross return;
- gross win rate;
- compounded gross return;
- maximum drawdown;
- average holding time;
- executed round-trip turnover;
- gross return per unit of executed turnover;
- sensitivity to explicit round-trip cost assumptions of 2, 5, and 10 bps;
- chronological subperiod results within the exploratory/development window;
- trade overlap and overnight violations.

The primary economic question is **cost-resilient gross return relative to turnover**, not raw gross return alone.

## Selection discipline

No variant is selected merely because it has the highest return.

A candidate must show:

- mechanically correct execution;
- no overnight leakage;
- materially lower turnover than H1;
- positive gross economics;
- improvement under at least the low-cost sensitivity;
- stability across chronological development subperiods;
- no dependence on a small number of extreme observations.

If no variant satisfies these conditions, Strategy 002 should be closed rather than repeatedly searched.

## Validation rule

A successful development variant must be frozen before the existing chronological validation period is reopened.

The existing 2026-06-10 through 2026-08-19 validation result must not be used to choose among H2/H3/H6. If a development variant survives, the validation period can later be evaluated once, with the final holdout remaining untouched.

