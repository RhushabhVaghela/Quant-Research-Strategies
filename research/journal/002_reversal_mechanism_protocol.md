# Strategy 002 — Reversal Mechanism Characterization Protocol

**Status:** Active exploratory research. No trading hypothesis or strategy selected.

## Purpose

The committed pattern-characterization results show a broad short-horizon signed-return reversal pattern in the locked exploratory sample. This stage does **not** convert that observation into a strategy.

The next question is narrower:

> Does the apparent 5-minute reversal look like an economically meaningful short-horizon price-reaction effect, or is it largely a bar-construction / microstructure artifact?

The analysis therefore decomposes the next-bar move into components that can be measured from the existing OHLCV data, without requiring a bid/ask feed.

## Evidence motivating this stage

Across the 19 structurally eligible instruments, the exploratory characterization reports:

- after a negative prior 5-minute return, the median instrument mean next-bar return is positive and 84.2% of instruments have a positive mean;
- after a positive prior 5-minute return, the median instrument mean next-bar return is negative and only 5.3% of instruments have a positive mean;
- the effect weakens and changes sign at longer horizons;
- signed-return autocorrelation is generally negative at lag 1 but is not stable in sign across all later lags and chronological subperiods;
- absolute-return autocorrelation is positive across the sample, consistent with volatility clustering rather than directional predictability.

These are descriptive findings from the exploratory period only. They do not establish profitability, tradability, causality, or a hypothesis.

## Locked data boundary

This stage is restricted to the exploratory development window:

- **2025-09-18 through 2026-06-09**, inclusive.

Validation:

- **2026-06-10 through 2026-08-19**

Final holdout/OOS:

- **2026-08-20 through 2026-09-17**

Validation and holdout remain untouched.

## Decomposition tests

For each structurally eligible instrument:

1. Compute the prior 5-minute close-to-close return.
2. Condition on prior return sign.
3. Measure the next-bar:
   - close-to-close return;
   - close-to-open return;
   - open-to-close return.
4. Repeat for prior-return magnitude quartiles crossed with sign.
5. Report cross-instrument breadth and medians rather than selecting individual securities.
6. Compare the sign-conditioned components across chronological subperiods.

### Interpretation

This decomposition is diagnostic:

- If the reversal is concentrated in close-to-open while open-to-close does not show the same direction, the apparent signal may be strongly related to the transition between bars.
- If the reversal persists inside the next bar from open to close, that is more consistent with a directional intrabar response and less consistent with a simple close-to-close artifact.
- Neither result by itself proves economic alpha. Without bid/ask quotes, spread, trade-direction, and order-book data, microstructure effects cannot be completely ruled out.

## Additional controls

The analysis will also inspect:

- zero-return frequency;
- price discretization / repeated closes;
- conditional observation counts;
- sign × magnitude behavior;
- cross-instrument breadth;
- chronological stability.

No threshold, holding period, instrument subset, or trading rule is optimized in this stage.

## Decision gate

Advance to formal economic-hypothesis definition only if the reversal remains sufficiently broad and interpretable after decomposition and is not adequately explained by an obvious measurement artifact.

If the decomposition points primarily to microstructure or bar-boundary effects, preserve the finding as a descriptive result and investigate a different pattern family instead.

## Reproducibility

The analysis must use the existing downloaded Strategy 002 OHLCV files and the structural universe audit. It must not acquire or use validation/holdout observations.

Planned execution:

    python scripts/characterize_strategy_002_reversal_mechanism.py data/raw/strategy_002_universe --audit-report data/reports/strategy_002_universe_audit.csv --output-dir data/reports/strategy_002_reversal_mechanism

