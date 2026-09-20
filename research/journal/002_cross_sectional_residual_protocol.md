# Strategy 002 — Cross-Sectional Residual Pattern Protocol

**Status:** Exploratory pattern investigation. No trading hypothesis selected.

## Motivation

The first Strategy 002 pattern investigation found a broad signed-return reversal in raw 5-minute close-to-close returns. Mechanism decomposition showed that much of the effect occurs from the prior close to the next open rather than during the next bar itself. That observation is not being promoted to a strategy.

The next question is narrower:

> After removing common market movement, does a stock-specific short-horizon deviation show a repeatable reversal that remains observable long enough to be acted upon?

This is a new descriptive investigation, not a predefined trading hypothesis.

## Locked sample

Use only exploratory development: **2025-09-18 through 2026-06-09**, across the 19 structurally eligible instruments.

Do not use validation (2026-06-10 through 2026-08-19) or final holdout/OOS (2026-08-20 through 2026-09-17).

## Construction

At each 5-minute timestamp with sufficient cross-sectional coverage:

1. Compute each instrument's close-to-close return.
2. Compute the equal-weight cross-sectional market return from the eligible universe.
3. Define each instrument's residual return as stock return minus cross-sectional market return.
4. Examine residual-return autocorrelation; next-bar residual return conditional on prior residual sign; sign × residual-magnitude quartile; 1, 2, 3, 6 and 12 bar horizons; cross-instrument breadth; and chronological stability.
5. Compare the residual result with the raw-return result.

## Controls

This stage does not choose z-score thresholds, lookbacks, holding periods, stop levels, instrument subsets, portfolio weights, or transaction-cost assumptions for optimization.

The cross-sectional market return is defined mechanically from the eligible universe and is not selected for performance.

## Decision gate

Advance toward an economic hypothesis only if the residual effect is broad rather than concentrated, survives chronological inspection, is not merely the same market-wide bar-boundary effect already identified, and is defined using information available before the prospective return interval.

If these conditions are not met, preserve the negative finding and continue pattern discovery.

## Reuse

This stage reuses the repository's existing time-series analysis, cross-sectional universe/audit infrastructure, PCA/common-factor analysis, and prior Strategy 001 cross-sectional research conventions.
