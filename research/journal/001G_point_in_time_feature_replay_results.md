# Strategy 001G — Point-in-Time Feature & Forward-Path Replay — Results

## Status

**🟡 Complete — replay reconciled; forward-path diagnostics are informative; strategy remains not paper/live ready.**

The frozen 001D strategy was reconstructed directly from the validated GOLDBEES OHLCV data and compared against the frozen 001D gross trade export. The replay matched all reference trades within the documented floating-point tolerance.

## 1. Replay integrity

| Check | Result |
|---|---:|
| Replayed frozen 001D trades | 310 |
| Reference 001D trades | 310 |
| Exact reconciliations within tolerance | 310 |
| Reconciliation discrepancies | 0 |

The uploaded `reconciliation.csv` contains 310 matched rows. Gross-return absolute differences were floating-point scale only; no trade-level mismatch was observed.

This is an important implementation gate: 001G did not alter the frozen 001D signal or execution logic while recovering additional diagnostic information.

## 2. Forward-path results

Forward returns are measured from the executable next-bar-open entry price to the close at each signal-relative horizon. Therefore the frozen 30-minute signal horizon corresponds to approximately 25 minutes of entry-to-exit elapsed time on regular 5-minute bars.

| Signal-relative horizon | Observations | Mean | Median | Win rate | P10 | P90 |
|---:|---:|---:|---:|---:|---:|---:|
| 5 min | 310 | +1.36 bps | 0.00 bps | 47.10% | -4.88 bps | +7.62 bps |
| 10 min | 310 | +2.44 bps | +0.99 bps | 52.26% | -7.23 bps | +12.54 bps |
| 15 min | 310 | +2.22 bps | +0.86 bps | 51.61% | -8.01 bps | +15.77 bps |
| 20 min | 310 | +3.40 bps | +1.75 bps | 56.45% | -9.53 bps | +17.98 bps |
| 25 min | 310 | +4.51 bps | +2.47 bps | 57.42% | -12.42 bps | +19.85 bps |
| 30 min | 310 | +4.77 bps | +2.41 bps | 55.81% | -12.99 bps | +22.16 bps |
| 45 min | 284 | +5.83 bps | +3.49 bps | 58.45% | -13.88 bps | +29.37 bps |
| 60 min | 255 | +5.43 bps | +3.79 bps | 56.86% | -19.03 bps | +27.94 bps |

### Interpretation

The forward path does **not** show the gross effect appearing only at the final frozen exit. The mean and median are already positive by 10 minutes and the mean rises substantially between 15 and 25 minutes. The 25–30 minute region is therefore consistent with the original frozen holding horizon rather than looking like an isolated terminal observation.

However, the path is noisy and positively skewed. At 5 minutes the median is exactly 0 bps and the win rate is below 50%, while the positive mean is partly driven by larger winners. The 30-minute distribution has a standard deviation of approximately 20.47 bps and skewness of approximately 3.22. This is evidence of a noisy, tail-sensitive gross effect, not proof of a stable executable alpha.

The 45- and 60-minute observations are fewer because forward paths cannot cross the session boundary under the current same-session convention. They should not be treated as directly equivalent samples to the 5–30 minute results.

## 3. MFE / MAE diagnostics

MFE and MAE are measured from the next-open entry through the frozen exit window. They are OHLC-range diagnostics and do **not** prove that an intrabar order could have captured the exact high or low because the data does not reveal intrabar sequencing.

| Statistic | MFE | MAE |
|---|---:|---:|
| Mean | +15.35 bps | -9.63 bps |
| Median | +9.48 bps | -6.88 bps |
| P10 | +1.50 bps | -19.89 bps |
| P25 | +4.80 bps | -12.77 bps |
| P75 | +17.96 bps | -3.57 bps |
| P90 | +35.82 bps | -1.52 bps |
| Minimum | 0.00 bps | -93.59 bps |
| Maximum | +192.63 bps | 0.00 bps |

MFE was positive for approximately 93.23% of trades; MAE was negative for approximately 97.10% of trades.

MFE reached its maximum at a median of 15 minutes from entry. MAE reached its maximum adverse excursion at a median of 5 minutes from entry. The timing is descriptive only and is not a basis for changing the exit or adding a stop.

Among the 173 gross-winning trades, final gross return captured a median of approximately 66.7% of that trade's MFE. This indicates that many winners gave back part of their favorable path before the frozen exit, but the statistic should not be converted into an optimized exit rule without a separate, pre-specified experiment and untouched evaluation period.

The MFE/MAE chart is stored as `data/reports/goldbees_strategy_001g_replay/mfe_mae_distribution.png` after local execution.

## 4. Signal-time feature diagnostics

The replay also recovered the point-in-time variables that were unavailable in the compact 001D export.

### Time of day

| Signal bucket | Trades | Mean gross | Median gross |
|---|---:|---:|---:|
| 11–12 | 61 | +2.82 bps | -0.82 bps |
| 12–13 | 70 | +0.56 bps | +1.06 bps |
| 13–14 | 86 | +6.09 bps | +2.41 bps |
| 14–15 | 93 | +7.98 bps | +3.72 bps |

Later-session buckets are descriptively stronger in this same historical sample. This is **not** being promoted to an afternoon-only filter; selecting it from the same sample would introduce another research degree of freedom.

### Z-score

| Z-score bucket | Trades | Mean gross | Median gross |
|---|---:|---:|---:|
| 2.00–2.25 | 123 | +5.46 bps | +2.46 bps |
| 2.25–2.50 | 77 | +2.13 bps | +1.28 bps |
| 2.50–3.00 | 63 | +5.58 bps | +1.23 bps |
| 3.00+ | 47 | +6.18 bps | +3.64 bps |

There is no clean monotonic relationship between z-score magnitude and gross outcome.

### Other signal-time relationships

Simple correlations with gross trade return were small for z-score (approximately +0.02), prior six-bar return (+0.05), and volume ratio (-0.04). Prior 30-bar standard deviation had a larger positive correlation (+0.18), but this is a descriptive scale relationship and should not be interpreted as evidence that volatility itself is an independent alpha feature.

Volume-ratio distribution: median approximately 1.09× the prior 30-bar average, P25 approximately 0.67×, P75 approximately 1.71×, and P90 approximately 3.04×.

## 5. What 001G establishes

001G establishes four useful facts:

1. **The frozen 001D implementation is reproducible.** All 310 trades reconcile exactly within tolerance.
2. **The gross effect has a measurable forward path.** The effect is already visible before the frozen exit and strengthens through the 20–30 minute region.
3. **The trade path contains substantial excursion relative to the final return.** Median MFE is about 9.48 bps versus a 2.41 bps median final gross return, while median MAE is about -6.88 bps.
4. **The descriptive feature slices do not yet justify a new filter.** Later-session strength is visible, but z-score, prior trend, and volume relationships do not provide a sufficiently clean basis for rule changes from this same sample.

## 6. What 001G does NOT establish

001G does not establish:

- that the strategy survives realistic bid/ask spread and market impact;
- that the 001D gross edge is statistically stable out of sample;
- that a particular stop, profit target, or alternative holding period is superior;
- that MFE can actually be captured in live execution;
- that the signal remains predictive after accounting for costs;
- that the strategy is ready for paper or live trading.

The existing 001E cost grid remains a central unresolved issue: the gross mean trade return is only about +4.77 bps, so execution friction can consume a large fraction of the observed edge.

## 7. Decision

**🟡 001G complete — proceed to predefined robustness and chronological validation.**

The replay passed its integrity gate and provides enough evidence to move forward, but it does not authorize parameter changes or deployment.

The next experiment is **001H — Predefined Robustness & Chronological Holdout Validation**. It will test temporal stability, cost sensitivity, and explicitly separated historical development/holdout periods without selecting new parameters from the full sample.

A genuinely untouched prospective OOS period is not available for this historical dataset because the 2025–2026 sample has already been examined during Strategy 001 research. Therefore the historical holdout will be labeled an **OOS-style chronological holdout**, while future paper/shadow trading will provide the clean prospective out-of-sample evidence.
