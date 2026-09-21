# Strategy 002 — Residual Temporal Conditioning Findings

**Status:** Temporal-stability gate passed descriptively; fixed-baseline validation may now proceed.

## Scope and controls

The analysis used only the locked exploratory period **2025-09-18 through 2026-06-09** and the 19 instruments that passed the structural universe gate. Validation and final holdout observations were not used. No strategy P&L or optimization was calculated.

## One-bar conditional residual reversal by chronological period

| Period | Prior residual condition | Median instrument mean | Positive-instrument fraction |
|---|---|---:|---:|
| Q1_time | negative | +0.3241 bps | 89.5% |
| Q1_time | positive | -0.4339 bps | 26.3% |
| Q2_time | negative | +0.3277 bps | 84.2% |
| Q2_time | positive | -0.3852 bps | 15.8% |
| Q3_time | negative | +0.4808 bps | 89.5% |
| Q3_time | positive | -0.5233 bps | 5.3% |
| Q4_time | negative | +0.4334 bps | 84.2% |
| Q4_time | positive | -0.3271 bps | 10.5% |

## Interpretation

The direction of the conditional relationship is coherent across all four chronological partitions:

- negative residuals are followed by positive residual returns in every period;
- positive residuals are followed by negative residual returns in every period;
- the breadth remains high for the negative-residual condition (84.2%–89.5%);
- the positive-residual condition is directionally negative in all four periods, although its positive-instrument fraction is not zero in the first two periods.

The magnitude varies across periods, so this result should be treated as evidence of **directional temporal stability**, not proof that the effect size is constant.

The one-bar effect is the relevant horizon for the preregistered candidate. Longer horizons were not used to select a different holding period.

## Gate decision

The predefined temporal-stability gate is **satisfied descriptively**. There is no sign change across the four chronological partitions and the effect is not isolated to one favorable period.

This permits the project to proceed to the **fixed-baseline chronological validation** on **2026-06-10 through 2026-08-19**.

This does **not** establish profitability, cost resilience, capacity, or live deployability.

## Next stage

Validation must use the already-defined leave-one-out residual signal and must not introduce:

- residual thresholds;
- magnitude ranking;
- volatility filters;
- sector filters;
- instrument selection;
- parameter optimization;
- holding-period selection.

The final holdout **2026-08-20 through 2026-09-17** remains locked.

## Important execution-timing clarification

The exploratory hypothesis concerns the next-bar **close-to-close residual**. However, the executable baseline enters at the next bar **open**. Therefore, validation must separately report:

1. the predictive next-bar residual close-to-close relationship; and
2. the actual executable open-to-close portfolio return.

The executable P&L must not incorrectly use close-to-close returns after an open-time entry.
