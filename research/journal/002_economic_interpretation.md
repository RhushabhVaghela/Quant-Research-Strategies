# Strategy 002 — Economic Interpretation

**Status:** Candidate economic interpretation established; no validation result yet.

## Evidence being interpreted

The locked exploratory research found:

- broad 1-bar signed-return reversal in the 19 structurally eligible instruments;
- the effect survived a leave-one-out cross-sectional residual construction;
- after a negative prior residual, the median instrument mean next-bar residual return was **+3.9211 bps**, with **94.7%** of instruments positive;
- after a positive prior residual, the median was **−4.4816 bps**, with **0%** of instruments positive;
- the effect decays rapidly beyond the first bar;
- for negative prior residuals, both the next close-to-open component (**+2.1336 bps**) and next open-to-close component (**+2.1737 bps**) were positive across the cross-sectional median, so the effect is not confined to the previously identified close-to-open boundary artifact;
- for positive prior residuals, the corresponding components were negative (**−2.4452 bps** and **−0.9523 bps**);
- chronological residual autocorrelation was strongly negative at lag 1 in the first three exploratory quarters for many instruments, while the fourth quarter was more mixed.

The leave-one-out construction also removes the mechanical self-inclusion present in the earlier residual study.

## Candidate economic interpretation

The most coherent interpretation is **short-horizon idiosyncratic overreaction / temporary liquidity pressure relative to peers**.

In simple terms:

> when an instrument moves unusually down relative to the rest of the eligible universe, some of that relative move may be temporary rather than permanent, and the instrument subsequently moves back toward its peer-relative level; the reverse applies after an unusually positive relative move.

This is an economic interpretation, not a demonstrated causal mechanism.

The evidence does **not** establish whether the temporary component is caused by bid/ask bounce, inventory effects, transient liquidity imbalance, uninformed order flow, behavioral overreaction, or another microstructure mechanism. The use of 5-minute OHLCV data cannot identify those causes directly.

## External literature context

The interpretation is consistent with established short-horizon reversal literature, which has linked very short-term reversals to temporary liquidity imbalances and bid/ask bounce. Heston, Korajczyk and Sadka (2010) specifically discuss short-term cross-sectional reversal and temporary liquidity imbalances lasting less than an hour. Jegadeesh and Titman discuss short-horizon negative serial covariance as consistent with inventory-related microstructure effects.

These papers are contextual support, not evidence that the Strategy 002 effect has the same cause.

References:

- Heston, Korajczyk & Sadka (2010), Intraday Patterns in the Cross-Section of Stock Returns, Journal of Finance. https://doi.org/10.1111/j.1540-6261.2010.01573.x
- Jegadeesh & Titman, Short-Horizon Return Reversals and the Bid-Ask Spread, Journal of Financial Intermediation. https://doi.org/10.1006/jfin.1995.1006
- Miwa (2019), Short-Term Return Reversals and Intraday Transactions. https://doi.org/10.1142/S2010139219500022

## What the evidence does and does not justify

It now justifies writing a **formal, falsifiable economic hypothesis**.

It does not yet justify:

- claiming a causal liquidity mechanism;
- selecting a residual threshold;
- selecting a volatility/magnitude threshold;
- optimizing a holding period;
- selecting securities;
- estimating live profitability;
- opening the final holdout;
- deploying capital.

The next stage is therefore to preregister one simple hypothesis and one simple baseline implementation before using the validation period.
