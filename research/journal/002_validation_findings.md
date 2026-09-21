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

The baseline reconstitutes the market-neutral portfolio at essentially every eligible 5-minute signal timestamp. The validation produced 3,699 portfolio observations, of which 3,698 had a prior target portfolio for target-turnover comparison.

The completed turnover decomposition reports:

- mean one-way target-weight turnover: **57.98%** of normalized gross exposure per rebalance;
- median one-way target-weight turnover: **58.33%**;
- 95th percentile one-way target-weight turnover: **78.41%**;
- mean executed round-trip turnover: **200%** of normalized gross exposure per completed one-bar trade;
- mean holding time: **5 minutes**;
- mean daily executed round-trip turnover: **147.96 normalized round trips**.

The 200% figure is intentional: the frozen baseline enters 100% gross exposure at the next-bar open and exits 100% gross exposure at the next-bar close. It is distinct from target-weight turnover and should not be added to target turnover as if they were separate trading costs.

The diagnostic confirms that the baseline is structurally high-turnover. It also confirms that exact live costs cannot be inferred from these normalized figures alone; spread, slippage, brokerage, taxes, market impact, and actual order mechanics would still need to be measured.

## Gate decision

**Current fixed baseline: not promotable.**

The candidate should not advance to the final holdout or live/shadow trading in its current form. The subsequent pre-registered H2/H3/H6 development experiment was evaluated only on the development period and produced no candidate that survived the 2 bps low-cost sensitivity. Strategy 002 is therefore closed for the current capital-pursuit/candidate-selection program.

This is not a statistical rejection of every possible residual-reversal phenomenon. It is closure of the tested executable research line because neither the one-bar baseline nor the registered lower-frequency holding variants established adequate cost-resilient economics.

## Research-preserving closure

The one-bar baseline remains frozen historical evidence. The H2/H3/H6 development search is closed, and no additional holding lengths, thresholds, filters, or execution variants should be added after observing those results under this Strategy 002 line.

The final holdout (**2026-08-20 through 2026-09-17**) remains untouched by the H2/H3/H6 selection process. The next research effort should use a genuinely different economic mechanism and/or asset class under a new strategy ID.
