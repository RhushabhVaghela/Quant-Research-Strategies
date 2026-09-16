# Strategy 001H — Predefined Robustness & Chronological Holdout Validation — Results

## Status

**🟡 Complete — historical robustness encouraging; execution economics unresolved.**

001H is a validation experiment on the frozen 001D strategy. It does not optimize parameters, select filters, or reinterpret the 2026 period as pristine untouched out-of-sample evidence.

The implementation reuses the frozen 001D signal/execution logic and evaluates four fixed chronological periods, a fixed 2025-vs-2026 sample designation, and a pre-registered round-trip friction ladder.

## 1. Execution controls

Frozen 001D rules remain unchanged:

- GOLDBEES 5-minute OHLCV;
- previous 30 completed same-session closes;
- sample standard deviation;
- z-score ≥ +2.0;
- prior six-bar return > 0;
- long-only;
- signal at event-bar close;
- next-bar-open entry;
- close of `t+6` exit;
- 12-bar cooldown;
- no overnight feature construction;
- one position at a time;
- no leverage or optimized sizing.

The cost ladder is expressed as **round-trip friction** of 0, 2, 4, 6, 8, 10, and 14 bps. These are research scenarios, not observed live spread, impact, brokerage, or tax measurements.

## 2. Historical/OOS qualification

The complete January 2025–August 2026 sample has already been examined during Strategy 001 research. Therefore:

- 2025 is labeled **development/reference**;
- 2026 is labeled **chronological holdout / OOS-style**;
- neither period is described as pristine untouched OOS;
- future paper/shadow execution will be the first genuinely prospective OOS period.

The 2026 H2 period contains the currently available portion of 2026 H2 in the dataset and should not be interpreted as a full half-year observation.

## 3. Chronological performance

The local empirical run produced 310 frozen trades across the four periods.

| Period | Trades | Mean gross | Median gross | Win rate | PF | Cumulative gross | MDD | Daily Sharpe |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 2025 H1 | 100 | +3.32 bps | +1.25 bps | 51.00% | 1.947 | +3.36% | -0.84% | 2.639 |
| 2025 H2 | 97 | +5.79 bps | +3.30 bps | 64.95% | 2.971 | +5.76% | -0.32% | 4.174 |
| 2026 H1 | 76 | +6.63 bps | +2.03 bps | 52.63% | 2.260 | +5.13% | -0.90% | 2.223 |
| 2026 H2* | 37 | +2.19 bps | +0.79 bps | 51.35% | 1.627 | +0.81% | -0.45% | 2.298 |

\* Available portion of 2026 H2 in the historical dataset.

The frozen gross edge remains positive in all four chronological periods. The later period is weaker in magnitude than 2025 H2 and 2026 H1, but it does not show a collapse to negative gross performance.

## 4. Development vs chronological holdout

| Sample designation | Trades | Mean gross | Median gross | Win rate | PF | Cumulative gross | MDD | Daily Sharpe |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 2025 development/reference | 197 | +4.53 bps | +2.89 bps | 57.87% | 2.406 | +9.31% | -0.84% | 3.429 |
| 2026 chronological holdout | 113 | +5.18 bps | +1.64 bps | 52.21% | 2.105 | +5.98% | -0.90% | 2.163 |

The 2026 chronological holdout remains positive and has a similar mean gross return to 2025, although its median and win rate are lower. The result supports temporal persistence of the observed gross relationship within the examined historical sample.

This is a chronological robustness result, **not clean OOS evidence**, because the full January 2025–August 2026 sample was available to the research process.

## 5. Cost sensitivity

| Round-trip friction | Mean net | Median net | Win rate | PF | Cumulative net | MDD | Daily Sharpe |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 0 bps | +4.77 bps | +2.41 bps | 55.81% | 2.269 | +15.85% | -0.90% | 2.710 |
| 2 bps | +2.77 bps | +0.41 bps | 51.29% | 1.593 | +8.89% | -1.39% | 1.603 |
| 4 bps | +0.77 bps | -1.59 bps | 43.87% | 1.134 | +2.34% | -2.61% | 0.448 |
| 6 bps | -1.23 bps | -3.59 bps | 37.74% | 0.821 | -3.81% | -4.50% | -0.721 |
| 8 bps | -3.23 bps | -5.59 bps | 31.94% | 0.606 | -9.60% | -9.69% | -1.868 |
| 10 bps | -5.23 bps | -7.59 bps | 26.45% | 0.456 | -15.03% | -15.08% | -2.959 |
| 14 bps | -9.23 bps | -11.59 bps | 19.03% | 0.274 | -24.95% | -24.93% | -4.883 |

The central economic finding is unchanged: the historical gross edge is small relative to plausible execution friction. Under the simple linear scenario model, performance crosses from positive to negative between 4 and 6 bps round-trip.

This is **not** an estimate of actual executable friction. The model does not yet contain observed bid/ask spreads, market impact, brokerage/taxes, order-book conditions, or realized fill quality.

## 6. Trading activity

| Period | Trades | Active days | Sessions | % sessions with trade | Trades / active day | Median signal gap | P10 signal gap | Median holding |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 2025 H1 | 100 | 76 | 123 | 61.79% | 1.316 | 1,440.0 min | 65.0 min | 25 min |
| 2025 H2 | 97 | 73 | 126 | 57.94% | 1.329 | 1,477.5 min | 95.0 min | 25 min |
| 2026 H1 | 76 | 59 | 120 | 49.17% | 1.288 | 2,735.0 min | 70.0 min | 25 min |
| 2026 H2* | 37 | 31 | 44 | 70.45% | 1.194 | 1,502.5 min | 132.5 min | 25 min |

\* Available portion of 2026 H2.

Signal frequency is sparse and broadly similar in trades per active day. The 2026 H1 median signal gap is longer, but there is no evidence here that a frequency regime change invalidates the strategy. The fixed 25-minute entry-to-exit holding duration remains unchanged.

## 7. Distribution stability

Selected distribution diagnostics:

| Period | P10 | P25 | P75 | P90 | Largest winner | Largest loser | Top-10% profit share |
|---|---:|---:|---:|---:|---:|---:|---:|
| 2025 H1 | -11.99 bps | -4.06 bps | +9.58 bps | +18.75 bps | +67.61 bps | -28.42 bps | 52.36% |
| 2025 H2 | -10.78 bps | -2.73 bps | +11.01 bps | +27.09 bps | +67.10 bps | -25.65 bps | 47.86% |
| 2026 H1 | -14.55 bps | -7.52 bps | +12.63 bps | +29.20 bps | +192.63 bps | -85.66 bps | 63.37% |
| 2026 H2* | -11.80 bps | -7.11 bps | +9.57 bps | +17.89 bps | +24.56 bps | -16.84 bps | 41.13% |

The edge is not identical across periods. In particular, 2026 H1 has greater tail dependence because of a very large winner, while 2026 H2 shows a lower top-10% profit share. The positive result therefore should not be described as a uniform per-trade effect.

## 8. Charts

The plotting script generated:

```text
chronological_performance.png
development_vs_holdout.png
cost_sensitivity.png
trade_return_distributions.png
trading_activity.png
daily_equity.png
daily_drawdown.png
```

The charts are descriptive diagnostics and should be read alongside the numerical CSV outputs.

## 9. Interpretation

001H provides three useful pieces of evidence:

1. **Temporal persistence:** the frozen gross relationship remains positive in every examined chronological period.
2. **Historical holdout stability:** 2026 remains positive relative to the 2025 development/reference period, without being treated as pristine OOS.
3. **Execution sensitivity:** the economic margin is narrow. The simple cost grid becomes negative between 4 and 6 bps round-trip.

The result is therefore not a rejection of the signal, but it is also not evidence for live deployment. The remaining uncertainty is concentrated in genuine prospective behavior and observed execution economics.

## 10. What 001H establishes

- The frozen 001D rules can be reproduced across the full historical sample.
- Gross performance is positive across four chronological periods.
- The 2026 historical holdout does not show a gross-performance collapse.
- Signal frequency is relatively sparse but broadly stable.
- The gross edge is small enough that execution friction is a first-order determinant of economic viability.

## 11. What 001H cannot establish

001H cannot establish:

- live bid/ask spread or market impact;
- actual Zerodha execution quality;
- pristine historical OOS discovery;
- superiority of any new parameter set;
- that MFE/MAE can be captured in live trading;
- that the strategy is ready for live capital.

## 12. Decision

**🟡 Proceed to prospective paper/shadow validation.**

The evidence is sufficient to justify a controlled prospective test of the **unchanged frozen 001D strategy**, primarily to measure whether the signal persists when outcomes are unknown at decision time and whether real execution conditions are compatible with the small historical gross edge.

No threshold, holding period, time-of-day filter, stop, target, sizing rule, or ML filter is being introduced as part of 001H.

The next gate is 001I: prospective OOS / paper-shadow validation. No Strategy 002 work begins before Strategy 001 receives a final decision.
