# Strategy 002 — Pattern Characterization Findings

**Status:** Exploratory evidence characterized; no trading hypothesis frozen.

## Locked evidence base

All findings in this document use only the locked exploratory development window:

- **2025-09-18 through 2026-06-09**
- 19 structurally eligible instruments
- HINDUNILVR excluded because the universe audit reports one unexpected interval and five zero-volume rows

Validation (**2026-06-10 through 2026-08-19**) and final holdout/OOS (**2026-08-20 through 2026-09-17**) remain untouched.

## Main observation: broad short-horizon reversal

The characterization results show a much clearer signed-return reversal pattern than the initial aggregate ACF alone suggested.

For the next 5-minute close-to-close return:

| Prior state | Median instrument mean | Positive-instrument fraction |
|---|---:|---:|
| Prior 5-minute return negative | +2.889 bps | 84.2% |
| Prior 5-minute return positive | -3.165 bps | 5.3% |

At the 2-bar horizon the corresponding medians are approximately:

- prior negative: **+2.881 bps**, positive in **84.2%** of instruments;
- prior positive: **-4.066 bps**, positive in **10.5%** of instruments.

The effect becomes less uniform at longer horizons. For example, after a negative prior return the median instrument mean becomes negative by 6 and 12 bars, while after a positive prior return the cross-sectional sign becomes less uniformly negative.

This is therefore best described as a **short-horizon reversal pattern**, not a persistent mean-reversion process.

## Magnitude conditioning

The sign × absolute-return characterization does not show a simple monotonic "larger move → stronger reversal" relationship across all instruments and horizons.

The cross-sectional medians for the prior-negative state are positive at 1–6 bars, but the quartile distributions are mixed. The corresponding prior-positive states are generally negative at 1–6 bars, also with substantial cross-sectional dispersion.

Therefore, the evidence does not justify selecting a return-magnitude threshold yet.

## Temporal stability

The signed-return autocorrelation characterization is directionally less stable than the sign-conditioned forward-return result.

Across the four chronological exploratory subperiods, the median lag-1 return autocorrelation remains negative:

- Q1: -0.0286
- Q2: -0.0115
- Q3: -0.0222
- Q4: -0.0133

However, later-lag autocorrelation changes sign across periods. This means the observation should not be generalized into a broad multi-bar mean-reversion claim.

Absolute-return autocorrelation remains positive across the four periods at short lags, supporting the separate descriptive conclusion that volatility clustering is present. Volatility clustering is not itself a directional alpha hypothesis.

## Economic interpretation status

The current evidence is strong enough to justify a **mechanism investigation**, but not strong enough to freeze a formal trading hypothesis.

The most important unresolved question is whether the 1–2 bar reversal is:

1. an economically meaningful short-horizon price-reaction effect;
2. a market microstructure / bid-ask / price-discretization effect;
3. an artifact of bar-boundary construction;
4. or a mixture of these mechanisms.

The current OHLCV data do not contain bid/ask quotes or trade-direction information, so a complete microstructure attribution is not possible from this dataset alone.

## Decision

**Do not optimize or backtest a reversal strategy yet.**

The appropriate next step is a controlled decomposition of the next bar into:

- close-to-close;
- prior-close-to-next-open;
- next-open-to-next-close.

The decomposition is designed to determine where the observed reversal is occurring before an economic hypothesis is written.

## Research-control rule

No threshold, holding period, instrument subset, validation result, or holdout result has been selected from this finding.

The next analysis remains exploratory and uses only the locked development period. If the reversal is primarily a bar-boundary/microstructure phenomenon, the finding will be retained as a descriptive result and another pattern family will be investigated rather than forcing a strategy from it.

## Reproducibility

Source characterization files:

- `data/reports/strategy_002_pattern_characterization/pattern_breadth_by_horizon.csv`
- `data/reports/strategy_002_pattern_characterization/temporal_stability_summary.csv`
- `data/reports/strategy_002_pattern_characterization/per_instrument_conditional_patterns.csv`
- `data/reports/strategy_002_pattern_characterization/temporal_stability_by_instrument.csv`

Next protocol:

- `research/journal/002_reversal_mechanism_protocol.md`
