# Strategy 002 — Cross-Sectional Residual Findings

**Status:** Exploratory finding. No trading hypothesis selected.

## Scope

The first cross-sectional residual investigation used only the locked exploratory window **2025-09-18 through 2026-06-09** and the 19 structurally eligible instruments. Validation and final holdout/OOS observations were not used.

The residual was defined as each instrument's 5-minute close-to-close return minus the equal-weight cross-sectional mean return.

## Observed pattern

The residual analysis shows a broad next-bar reversal pattern:

- After a negative residual, the median instrument mean next-bar residual return was **+3.7147 bps**, with **94.7%** of instruments positive.
- After a positive residual, the median instrument mean next-bar residual return was **−4.2457 bps**, with **0%** of instruments positive.
- At two bars, the effects weakened materially: +0.8035 bps after negative residuals and −0.1345 bps after positive residuals.
- At 3, 6 and 12 bars the median effects were small and changed sign for the negative-residual state.

The magnitude-conditioned results do not produce a simple monotonic relationship. The largest negative-residual quartile has a stronger next-bar reversal, but the effect does not persist uniformly across subsequent horizons. Positive-residual magnitude buckets likewise do not establish a clean threshold or duration rule.

## Temporal stability

The residual lag-1 autocorrelation is negative for many instruments in the first three chronological quarters, but the fourth quarter is materially more mixed. Longer-lag signs also vary substantially by period and instrument.

Therefore the current evidence supports **existence of a descriptive short-horizon residual reversal pattern**, but not yet a stable economic mechanism.

## Important methodological limitation

The current residual definition subtracts the contemporaneous cross-sectional mean that includes the instrument's own return. This is a mechanically convenient descriptive residual, but it is not the final factor-adjusted residual specification that should support a trading hypothesis.

The current result also uses close-to-close returns. The earlier raw-return mechanism study showed that raw reversal was concentrated around the prior-close/next-open boundary. Therefore the residual result could still reflect the same boundary phenomenon rather than an independently tradeable stock-specific mechanism.

## Decision

Do **not** create a Strategy 002 trading hypothesis, parameter grid, or execution engine from these results.

The next controlled investigation is a **leave-one-out residual mechanism decomposition**:

1. remove each instrument's own return from the cross-sectional market estimate;
2. construct residuals separately for close-to-close, prior-close-to-next-open, and next-open-to-next-close returns;
3. test the same sign-conditioned next-bar behavior and breadth;
4. inspect chronological stability;
5. determine whether residual reversal remains after removing self-contamination and whether it is still concentrated at the bar boundary.

Only if that investigation produces a broad, stable, economically interpretable and information-timely effect should a formal hypothesis be written.

## Research-control statement

No validation-period or final holdout/OOS observations are used in this finding. No trading P&L, threshold optimization, holding-period optimization, or instrument selection was performed.


## Follow-up status

The stricter leave-one-out residual mechanism analysis has now been executed locally. Its purpose is to test whether the earlier descriptive residual reversal survives removal of self-contamination and whether it remains outside the previously identified close-to-open boundary effect.

No conclusion from this follow-up is recorded here until its generated outputs are committed and reviewed. The current state is therefore **result pending**, not hypothesis confirmed or rejected.
