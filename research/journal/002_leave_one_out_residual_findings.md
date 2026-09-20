# Strategy 002 — Leave-One-Out Residual Findings

**Status:** Exploratory finding; no trading hypothesis selected.

## Scope and controls

The leave-one-out residual mechanism analysis was executed on the locked exploratory sample only:

- exploratory window: **2025-09-18 through 2026-06-09**;
- eligible instruments: **19**;
- excluded: **HINDUNILVR**, because it failed the structural universe audit;
- minimum leave-one-out cross-sectional coverage: **3 other eligible instruments**;
- validation and final holdout were not used;
- strategy P&L was not calculated;
- no optimization was performed.

## Main result

The short-horizon residual reversal survives the stricter leave-one-out construction.

At the next five-minute bar:

| Prior leave-one-out residual | Median instrument mean next residual | Instruments with positive mean |
|---|---:|---:|
| Negative | **+3.92 bps** | **94.7% (18/19)** |
| Positive | **−4.48 bps** | **0.0% (0/19)** |

At two bars, the effect is materially weaker:

- prior negative: **+0.85 bps**, positive in **68.4%** of instruments;
- prior positive: **−0.14 bps**, positive in **42.1%** of instruments.

At three, six, and twelve bars, the cross-instrument effect becomes small and inconsistent.

This establishes that the earlier equal-weight residual observation was not caused by including the instrument itself in its market benchmark.

## Boundary decomposition

The next-bar effect is not confined to the prior-close/next-open boundary.

For a prior negative residual:

- close-to-open component: **+2.13 bps**, positive in **84.2%** of instruments;
- open-to-close component: **+2.17 bps**, positive in **84.2%**.

For a prior positive residual:

- close-to-open component: **−2.45 bps**, positive in **10.5%**;
- open-to-close component: **−0.95 bps**, positive in **31.6%**.

Therefore the leave-one-out residual reversal survives the same boundary decomposition that previously caused the raw single-instrument reversal to be rejected as a potential bar-boundary artifact.

The result is still not proof of an economically exploitable effect. Execution timing, bid/ask effects, price discreteness, and the construction of the cross-sectional benchmark remain relevant.

## Magnitude conditioning

The descriptive magnitude relationship is stronger for negative residual shocks:

| Prior residual state | Median next-bar residual |
|---|---:|
| Negative, Q1 magnitude | +0.20 bps |
| Negative, Q2 | +3.59 bps |
| Negative, Q3 | +4.27 bps |
| Negative, Q4 | **+8.01 bps** |
| Positive, Q1 magnitude | −1.34 bps |
| Positive, Q2 | −2.49 bps |
| Positive, Q3 | −6.05 bps |
| Positive, Q4 | −5.03 bps |

The negative-residual side is approximately monotonic across magnitude quartiles in this exploratory sample. The positive-residual side becomes more negative through Q3 but is not monotonic from Q3 to Q4.

These are descriptive subgroup results, not a threshold-selection exercise. No residual z-score or magnitude cutoff is justified by them.

## Temporal stability

The existing temporal-stability output measures residual-return autocorrelation rather than the conditional reversal effect itself.

The lag-1 residual ACF is strongly negative for many instruments in Q1-Q3, but becomes materially more mixed in Q4. For example, several broad-market instruments that showed strongly negative lag-1 residual autocorrelation earlier in the sample move toward less negative or positive values in Q4.

Therefore the temporal-stability gate is **not yet satisfied**. We cannot treat the broad next-bar reversal as temporally stable solely from the current outputs.

The next controlled analysis must directly measure the conditional reversal effect separately inside the four chronological subperiods, rather than using ACF as a proxy.

## Current research decision

The leave-one-out result clears two important descriptive gates:

1. the reversal survives removal of self-contamination from the cross-sectional benchmark;
2. the effect is not primarily a close-to-open boundary artifact.

However, the temporal stability gate remains unresolved.

**Decision: do not formulate the formal Strategy 002 economic hypothesis yet.**

The next investigation will calculate the same sign-conditioned residual reversal separately across chronological subperiods, including the close-to-open and open-to-close components. This is a characterization test, not optimization.

If the conditional effect remains broad and directionally coherent across subperiods, the project can proceed to explicit economic interpretation and hypothesis definition. If it is concentrated in only part of the exploratory period, the result will remain an unresolved descriptive pattern and the project will continue pattern discovery.

## Reproducibility

Source outputs:

- `data/reports/strategy_002_leave_one_out_residual/leave_one_out_residual_breadth.csv`
- `data/reports/strategy_002_leave_one_out_residual/per_instrument_leave_one_out_residuals.csv`
- `data/reports/strategy_002_leave_one_out_residual/leave_one_out_residual_temporal_stability.csv`
- `data/reports/strategy_002_leave_one_out_residual/run_manifest.json`

No validation or holdout statistic is included in these findings.
