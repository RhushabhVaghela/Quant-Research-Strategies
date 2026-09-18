# Strategy 001J — Secondary Development Review

**Review date:** 2026-09-18  
**Phase:** Secondary development complete; no candidate frozen; holdout remains unopened  
**Universe:** U1 — locked Kite-native liquid NSE EQ top 50  
**Development window:** 2026-06-10 through 2026-08-19  
**Holdout window:** 2026-08-20 through 2026-09-17

## 1. Scope

This review covers the preregistered 108-configuration secondary development experiment registered in `001J_secondary_development_spec.md`.

The experiment was motivated by the first 162-configuration development result: gross expectancy was only a few basis points per trade and did not survive the predefined 5 bps sensitivity. The secondary grid therefore tested stronger z-score thresholds, shorter holding periods, and longer cooldowns.

No holdout data was loaded or used.

## 2. Execution integrity

The user's local run reported:

- **100 tests passed**.
- The secondary development runner completed all **108 configurations**.
- The runner explicitly reported that **no holdout data was loaded**.
- The experiment used the locked U1 universe and the fixed development window.

The uploaded run output records the 100-test result and successful 108-configuration execution. fileciteturn273file0L2-L8

## 3. Secondary-grid result

The strongest gross-mean configurations are concentrated in the high-threshold / longer-lookback part of the registered grid. Examples include:

| Config | Lookback | Z | Trend | Hold | Cooldown | Trades | Mean gross | Median gross | PF | Mean after 5 bps |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 100 | 40 | 3.5 | 3 | 6 | 24 | 224 | 3.63 bps | -2.54 bps | 1.208 | -1.37 bps |
| 99 | 40 | 3.5 | 3 | 6 | 12 | 227 | 3.40 bps | -2.56 bps | 1.195 | -1.60 bps |
| 104 | 40 | 3.5 | 6 | 6 | 24 | 227 | 2.35 bps | -1.84 bps | 1.130 | -2.65 bps |
| 108 | 40 | 3.5 | 9 | 6 | 24 | 230 | 2.31 bps | -2.31 bps | 1.130 | -2.69 bps |

The important pattern is not the exact ordering. Across the strongest secondary configurations, median trade returns remain negative and the mean edge remains below 5 bps.

The uploaded result rows show, for example, Config 100 at 3.63 bps gross mean and -1.37 bps under the 5 bps haircut, while Config 104 is 2.35 bps gross and -2.65 bps at 5 bps. fileciteturn273file0L101-L104

## 4. Chronological behavior

The strongest configurations do show a recurring positive late-development subperiod, but this is not sufficient evidence of a stable production edge.

For example, Config 100 has approximately:

- early mean: 6.08 bps;
- middle mean: 0.70 bps;
- late mean: 4.47 bps.

The middle-period weakening is material, and the full-sample median remains negative.

This means the secondary experiment did not convert the original effect into a uniformly strong chronological edge.

## 5. Breadth and frequency

The stronger configurations generally involve roughly 224–230 trades across 49 symbols, compared with hundreds more trades for lower-threshold configurations.

The reduction in frequency is real, but it did not produce enough per-trade expectancy to overcome a conservative 5 bps friction assumption.

The correct interpretation is therefore **lower frequency without sufficient economic improvement**, rather than “fewer trades is better.”

## 6. Cost resilience

The predefined secondary cost grid is decisive for the current promotion question.

The best gross mean observed in the secondary grid is approximately **3.63 bps per trade**. A flat 5 bps haircut therefore makes even that configuration negative on mean return.

This is before separately modeling spread, slippage, adverse selection, and order-size-dependent execution.

Accordingly, no secondary configuration is economically strong enough to freeze for the untouched holdout.

## 7. Methodological decision

**No 001J candidate is frozen.**

This is not a statistical rejection of the underlying Strategy 001 continuation hypothesis. It is a decision that the current 001J implementation does not demonstrate enough cost-resilient expectancy to justify consuming the untouched holdout or allocating live capital.

The holdout remains protected. We will not inspect it merely to find a configuration that looks better.

The sequential-development limitation must also be recorded: this second search reused the same development sample after the first development review, so it cannot be treated as independent confirmation.

## 8. 001J status

The September 2026 001J cross-sectional continuation sprint is **closed for candidate selection**.

- U1 remains immutable.
- Frozen 001D remains immutable.
- 001I remains closed for capital-pursuit priority and is not statistically rejected.
- No 001J candidate is promoted to holdout.
- No holdout result is used to select or rescue 001J.

A future continuation experiment under Strategy 001 remains possible, but it must be registered as a new experiment with a genuinely different design rather than repeatedly searching the same development sample.

## 9. Next portfolio step

Because the project deadline requires progress across multiple independent strategies, the research program now moves to a materially different economic mechanism rather than continuing to optimize 001J.

The next registered strategy is **Strategy 002 — intraday statistical arbitrage / pairs mean reversion in liquid Indian equities**.

Its purpose is diversification of economic mechanism: unlike 001's directional continuation signal, 002 will trade a relative-value spread between two related securities and will be evaluated on spread normalization, pair stability, turnover, costs, and simultaneous long/short execution feasibility.

The new strategy specification must be frozen before data-driven parameter selection begins.

## 10. Reproducibility record

The user's local run reported 100 tests passing and successful completion of the 108-configuration secondary development with no holdout data loaded. fileciteturn273file0L2-L8

This review is a decision record only; it does not claim that the assistant executed the user's local commands.
