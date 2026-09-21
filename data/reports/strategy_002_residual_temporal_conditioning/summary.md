# Strategy 002 — Residual Temporal Conditioning Summary

**Purpose:** Review the preregistered chronological-stability gate before opening validation.

## Research controls

- Exploratory period: 2025-09-18 00:00:00+05:30 through 2026-06-09 23:59:59+05:30
- Included instruments: 19
- Validation used: false
- Holdout used: false
- Strategy P&L calculated: false
- Optimization performed: false

## One-bar conditional residual reversal by period

| Period | Condition | Median instrument mean (bps) | Positive-instrument fraction |
|---|---|---:|---:|
| Q1_time | prior_negative | 0.3241 | 89.5% |
| Q1_time | prior_positive | -0.4339 | 26.3% |
| Q2_time | prior_negative | 0.3277 | 84.2% |
| Q2_time | prior_positive | -0.3852 | 15.8% |
| Q3_time | prior_negative | 0.4808 | 89.5% |
| Q3_time | prior_positive | -0.5233 | 5.3% |
| Q4_time | prior_negative | 0.4334 | 84.2% |
| Q4_time | prior_positive | -0.3271 | 10.5% |

## Gate interpretation

The primary temporal-stability gate is not a profitability test. Review whether the negative-residual condition remains positive and the positive-residual condition remains negative across chronological periods, without selecting a favorable period.

This summary does not authorize validation or live trading. A mixed/sign-changing result should remain unresolved rather than being repaired through parameter changes.

## Next step

If the chronological pattern is directionally coherent and broad, document the finding and proceed to the fixed-baseline validation runner. If it is materially unstable, record the result and do not open validation for this candidate.
