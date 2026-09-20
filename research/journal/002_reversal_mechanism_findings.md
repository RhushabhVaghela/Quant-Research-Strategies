# Strategy 002 — Reversal Mechanism Findings

**Status:** Exploratory mechanism characterized; the raw short-horizon reversal observation is **not promoted to a trading hypothesis**.

## Locked evidence base

This analysis uses only the exploratory development window, 2025-09-18 through 2026-06-09, across 19 structurally eligible instruments. Validation (2026-06-10 through 2026-08-19) and final holdout/OOS (2026-08-20 through 2026-09-17) remain protected.

## Main decomposition result

The apparent next-bar close-to-close reversal is concentrated at the **close-to-open boundary**, not in the next bar's open-to-close movement.

For a negative prior 5-minute return:

| Next-bar component | Median instrument mean | Positive instruments |
|---|---:|---:|
| Close → Close | **+2.889 bps** | **84.2%** |
| Prior close → Next open | **+3.736 bps** | **94.7%** |
| Next open → Next close | **−0.600 bps** | **36.8%** |

For a positive prior 5-minute return:

| Next-bar component | Median instrument mean | Positive instruments |
|---|---:|---:|
| Close → Close | **−3.165 bps** | **5.3%** |
| Prior close → Next open | **−0.806 bps** | **42.1%** |
| Next open → Next close | **−2.619 bps** | **21.1%** |

The magnitude-conditioned results reinforce that the close-to-open component is the dominant contributor for negative prior returns. In the largest negative-return quartile, prior-close → next-open has a median instrument mean of about **+6.20 bps** and is positive in **100%** of instruments, while next-open → next-close is approximately **−0.26 bps** with only 47.4% positive instruments.

## Interpretation

This substantially changes the interpretation of the original reversal observation.

The raw close-to-close effect should **not** currently be treated as a tradable intraday reversal signal. A large part of the measured move occurs between the previous bar's close and the next bar's open. With ordinary 5-minute OHLCV data, that transition is exactly where close-print / next-open-print effects, auction mechanics, price discreteness, and bid/ask-related effects can enter.

More importantly, an executable strategy that observes the prior 5-minute close and then submits an order for the next bar cannot automatically assume it captures the measured close-to-open move. If the price adjustment has already occurred by the next open, the backtest would suffer from a serious execution-timing mismatch.

The next-open → next-close component does **not** preserve the same broad reversal magnitude. That weakens the case for an economically meaningful within-bar reversal mechanism.

## Decision gate

**Do not freeze a reversal hypothesis and do not build a reversal trading engine from this observation.**

The finding is retained as a valid exploratory result, but the current evidence does not establish a tradable alpha mechanism.

This is a research rejection of the **current raw-bar reversal interpretation**, not a rejection of all possible mean-reversion or relative-value mechanisms.

## Next investigation

The observation motivates a more careful **cross-sectional residual/relative-return investigation**:

- remove common market movement before measuring individual-stock reversals;
- examine whether idiosyncratic moves contain a short-horizon reversal component;
- distinguish market-wide moves from stock-specific deviations;
- require the signal to exist in a return component that can be entered after the information becomes observable.

This is materially different from the original Strategy 001 continuation mechanism and remains hypothesis-free at this stage.

## Research controls

No validation-period results, holdout results, strategy P&L, transaction-cost optimization, threshold selection, or instrument selection has been used.
