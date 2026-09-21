# Strategy 002 — Chronological Validation Findings

**Status:** Fixed baseline failed the initial validation promotion gate because the observed gross edge is too small relative to even the first stated transaction-cost sensitivity.

## Scope

- Validation: **2026-06-10 through 2026-08-19**
- Instruments: 19 structurally eligible instruments
- Observations: 3,695 usable portfolio timestamps
- Final holdout: **2026-08-20 through 2026-09-17**, not used
- Signal: leave-one-out residual sign at completed 5-minute close
- Execution: next 5-minute bar open → next 5-minute bar close
- No parameter optimization was performed.

## Results

| Round-trip cost assumption | Mean return per portfolio | Median | Positive fraction | Compounded return | Daily Sharpe | Max drawdown |
|---:|---:|---:|---:|---:|---:|---:|
| 0 bps | +0.0896 bps | +0.1751 bps | 53.48% | +3.35% | 4.52 | -1.35% |
| 5 bps | -4.9104 bps | -4.8249 bps | 3.52% | -83.72% | -234.12 | -83.70% |
| 10 bps | -9.9104 bps | -9.8249 bps | 0.51% | -97.44% | -486.19 | -97.43% |
| 15 bps | -14.9104 bps | -14.8249 bps | 0.11% | -99.60% | -750.11 | -99.60% |

## Interpretation

The zero-cost result shows a small positive gross validation effect. However, its mean magnitude is only **0.0896 bps per five-minute portfolio rebalance**.

The first explicit cost sensitivity of 5 bps overwhelms the gross edge by a very large margin. The baseline therefore does **not** demonstrate cost resilience.

The 5/10/15 bps rows should not be interpreted as forecasts of actual realized costs. They are sensitivity scenarios. The result instead establishes that the current implementation has a very small gross edge relative to plausible execution-cost scales.

## Important turnover observation

The baseline reconstitutes the market-neutral portfolio at essentially every eligible 5-minute signal timestamp. The validation produced 3,695 portfolio observations over the validation period. Consequently, this is a **high-turnover implementation**.

The current validation report does not yet decompose actual notional turnover by long and short leg. That is a reporting gap and must be measured before any claim about exact live transaction costs or capacity.

This gap does not rescue the candidate: the gross edge is only 0.0896 bps per rebalance, so detailed turnover measurement is necessary to quantify execution economics, but the current evidence does not support promotion.

## Gate decision

**Current fixed baseline: not promotable.**

The candidate should not advance to the final holdout or live/shadow trading in its current form.

The exploratory residual mechanism itself should not be described as statistically disproven. The validation result shows that this particular fully rebalanced, one-bar executable baseline does not produce sufficient gross edge to survive the tested cost sensitivities.

## Research-preserving next step

Before any new candidate is created, record the failure and preserve the frozen baseline unchanged.

If further Strategy 002 work is justified, it must be treated as a **new development experiment** using only the exploratory/development data. Any change intended to reduce turnover or improve execution economics—such as signal persistence, entry filtering, portfolio rebalancing frequency, or alternative execution timing—would be a new candidate and must not use the final holdout for selection.

The final holdout remains locked.


## Follow-up diagnostic

The fixed baseline remains frozen and is not being retuned. The turnover/execution decomposition is restricted to the validation period.

A critical accounting distinction is now explicit. The diagnostic reports both:

1. **target-weight turnover** — the mathematical change between consecutive hypothetical target portfolios; and
2. **executed round-trip turnover** — the actual trading lifecycle of the frozen baseline.

The frozen baseline does not carry a position from one signal timestamp into the following signal timestamp. It enters the selected portfolio at the next bar's open and closes that portfolio at the next bar's close. With normalized gross exposure of 1.0, that is 1.0 unit of entry notional plus 1.0 unit of exit notional, or **2.0 units of executed round-trip turnover per portfolio observation**.

This distinction matters because target-weight turnover alone would understate the execution activity and could incorrectly suggest that the baseline is less expensive to trade than its implementation actually is.

The diagnostic is defined in `research/journal/002_turnover_execution_decomposition_protocol.md` and implemented in `scripts/run_strategy_002_turnover_decomposition.py`. It does not authorize use of the final holdout.

No lower-turnover candidate has been selected from this diagnostic. If a specific economically motivated modification is justified, it must be registered as a new development experiment and evaluated without using the final holdout.

