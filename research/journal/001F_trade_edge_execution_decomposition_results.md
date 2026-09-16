# Strategy 001F — Results

**Status: 🟡 Complete — diagnostic evidence supports further validation; no deployment**

## Input

`data/reports/goldbees_strategy_001d_backtest/trades_gross.csv`

The experiment decomposed the **310 frozen Strategy 001D trades** without changing the signal rule.

## 1. Winner concentration

| Exclusion | Excluded winners | Remaining trades | Mean gross return | Median | Win rate | Profit factor |
|---|---:|---:|---:|---:|---:|---:|
| None | 0 | 310 | +4.77 bps | +2.41 bps | 55.81% | 2.269 |
| Top 1% | 2 | 308 | +3.80 bps | +2.40 bps | 55.52% | 2.005 |
| Top 5% | 9 | 301 | +2.48 bps | +1.97 bps | 54.49% | 1.641 |
| Top 10% | 18 | 292 | +1.41 bps | +1.32 bps | 53.08% | 1.354 |

### Interpretation

The gross result is **not solely dependent on a small number of extreme winners**. Removing the largest 10% of winning trades reduces the mean and profit factor materially, but the remaining sample is still positive with a 53.1% win rate and 1.35 profit factor.

This does not prove robustness. Tail contribution remains economically important and the exercise is an in-sample diagnostic, not an out-of-sample stress test.

## 2. Time-of-day decomposition

| Signal-time bucket | Trades | Mean gross return | Median | Win rate |
|---|---:|---:|---:|---:|
| 09–10 | 0 | — | — | — |
| 10–11 | 0 | — | — | — |
| 11–12 | 61 | +2.82 bps | -0.82 bps | 47.54% |
| 12–13 | 70 | +0.56 bps | +1.06 bps | 51.43% |
| 13–14 | 86 | +6.09 bps | +2.41 bps | 59.30% |
| 14–15 | 93 | +7.98 bps | +3.72 bps | 61.29% |
| 15–16 | 0 | — | — | — |

The later-session buckets show stronger descriptive performance in this sample. The empty morning buckets are a warm-up/data-availability consequence of the 30-bar lookback and are not evidence that morning trading is inferior.

**Important:** 001F does not promote a time-of-day filter. Selecting 13–14 or 14–15 based on this table would constitute same-sample optimization.

## 3. Signal-strength decomposition

| z-score bucket | Trades | Mean gross return | Median | Win rate |
|---|---:|---:|---:|---:|
| 2.00–2.25 | 123 | +5.46 bps | +2.46 bps | 56.91% |
| 2.25–2.50 | 77 | +2.13 bps | +1.28 bps | 53.25% |
| 2.50–3.00 | 63 | +5.58 bps | +1.23 bps | 50.79% |
| 3.00+ | 47 | +6.18 bps | +3.64 bps | 63.83% |

There is **no clean monotonic relationship** between z-score severity and subsequent trade return. The 3.00+ bucket is descriptively interesting but contains only 47 trades and cannot justify changing the frozen threshold.

## 4. Holding-period limitation

All 310 exported trades have a 25-minute entry-to-exit timestamp difference because the compact trade export records only the frozen next-bar-open entry and t+6 close exit.

Therefore 001F could not reconstruct the intermediate 5/10/15/20/30/45/60-minute forward path or MFE/MAE from the trade file alone.

This is a **measurement limitation, not evidence against the strategy**.

## 5. Overall diagnosis

001F provides three useful findings:

1. The gross edge is broader than the extreme-winner tail, although large winners remain important.
2. Performance is descriptively stronger in later-session signal buckets, but this must be treated as a future hypothesis rather than a selected filter.
3. The z-score relationship is not monotonic, so the current evidence does not support a simple "more extreme = better" explanation.

The central unresolved issue remains **execution economics**. 001E showed that the roughly +4.77 bps mean gross trade return is vulnerable to modest assumed friction. 001F does not overturn that finding.

## 6. Decision

**Decision: 🟡 PROMISING FOR FURTHER RESEARCH — NOT PAPER/LIVE READY.**

The frozen gross edge remains sufficiently structured to justify improving the measurement dataset and then conducting predefined robustness/OOS tests. No parameter, time-of-day filter, holding period, or execution rule is selected from 001F.

## 7. Next experiment

Proceed to **001G — Point-in-Time Feature & Forward-Path Replay**.

001G will reconstruct the frozen trades directly from the validated GOLDBEES OHLCV data, retain signal-time features without look-ahead, reconcile against the 001D trade export, and measure the forward path at fixed horizons plus MFE/MAE where supported.

Only after that measurement gate should predefined robustness and chronological out-of-sample testing begin.
