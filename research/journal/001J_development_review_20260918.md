# Strategy 001J — Development Review

**Review date:** 2026-09-18  
**Phase:** Development diagnostics complete; holdout remains unopened  
**Universe:** U1 — locked Kite-native liquid NSE EQ top 50  
**Development window:** 2026-06-10 through 2026-08-19  
**Holdout window:** 2026-08-20 through 2026-09-17  

## 1. Scope

This review covers the preregistered 162-configuration development grid and the subsequent chronological stability and cost-sensitivity diagnostics. No holdout result is used in this review.

The development stability report is a screening aid only. It does not automatically select a production candidate.

## 2. Development stability result

The stability screen identifies four configurations with positive mean return and profit factor above 1.0 in all three fixed chronological development subperiods:

| Config | Lookback | Z | Trend | Hold | Cooldown | Trades | Mean | Median | PF | Worst-period mean | Worst-period PF |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 156 | 40 | 2.5 | 6 | 9 | 12 | 524 | 2.35 bps | -3.05 bps | 1.141 | 0.147 bps | 1.009 |
| 162 | 40 | 2.5 | 9 | 9 | 12 | 522 | 2.64 bps | -2.53 bps | 1.159 | 0.656 bps | 1.042 |
| 150 | 40 | 2.5 | 3 | 9 | 12 | 516 | 2.40 bps | -3.05 bps | 1.143 | 0.273 bps | 1.018 |
| 132 | 40 | 2.0 | 3 | 9 | 12 | 810 | 2.66 bps | -2.89 bps | 1.170 | 0.263 bps | 1.017 |

These results are not sufficient by themselves to freeze a candidate. In particular, the median trade return is negative for all four configurations, and the positive development mean is only a few basis points per trade.

The broader development screen also shows nearby configurations with materially different results, so the final decision must consider parameter-neighborhood behavior rather than treating the top row as a unique optimum.

## 3. Cost sensitivity result

The cost-sensitivity diagnostic applies a flat round-trip haircut of 0, 5, 10, 15, 20, 25, and 30 bps. This is a diagnostic assumption, not a claim about the exact Zerodha bill for any particular order size.

The key observation is that the configurations above do not retain positive mean return at a 5 bps round-trip haircut. For example:

- Config 156: 2.35 bps gross mean → -2.65 bps at 5 bps cost.
- Config 162: 2.64 bps gross mean → -2.36 bps at 5 bps cost.
- Config 150: 2.40 bps gross mean → -2.60 bps at 5 bps cost.
- Config 132: 2.66 bps gross mean → -2.34 bps at 5 bps cost.
- Config 161, the strongest aggregate-PF configuration in the development grid, has 3.47 bps gross mean and becomes -1.53 bps at 5 bps cost.

The cost diagnostic therefore materially changes the interpretation of the development results: the apparent gross edge is too small to regard the current 001J implementation as execution-ready.

## 4. Broker-cost context

Current Zerodha published charges for NSE equity intraday include brokerage of 0.03% or ₹20 per executed order, whichever is lower; equity intraday STT of 0.025% on the sell side; NSE equity transaction charges of 0.00307%; GST on applicable brokerage/SEBI/transaction charges; SEBI charges; and buy-side stamp duty.

Therefore, a 5 bps round-trip sensitivity case should not be interpreted as an aggressive upper bound. Actual all-in cost depends on trade notional, brokerage cap, statutory charges, spread, slippage, and execution quality. For this reason, the development result should not be promoted based on gross returns alone.

## 5. Decision

**No 001J candidate is frozen from this development run.**

The reason is methodological rather than a statistical claim that the continuation hypothesis is false. The 162-config development exercise produced a small gross effect, but the effect is not sufficiently cost-resilient for a live-capital promotion decision.

The holdout remains **unopened for candidate selection purposes**. We will not inspect the holdout and then choose a configuration because the development result is inconvenient.

## 6. Warning remediation

The development stability script previously emitted a NumPy deprecation warning from generic timedelta arithmetic when constructing the inclusive metadata end date. The implementation has been changed to use an explicit frozen `DEVELOPMENT_END` date (`2026-08-19`) alongside the exclusive boundary (`2026-08-20`). This removes the unnecessary timedelta conversion from metadata generation without changing the development windows, trade filtering, ranking logic, or numerical methodology.

A regression test was also added to pin the three development boundary dates and ensure the inclusive/exclusive relationship remains explicit.

## 7. Next experiment under Strategy 001

The next step is a new, explicitly preregistered development experiment under the same Strategy 001 economic hypothesis. It must be designed around the observed bottleneck — low per-trade expectancy relative to execution costs — without changing rules after inspecting holdout results.

The follow-up experiment must:

1. Preserve the locked U1 universe unless a separately documented universe experiment is registered.
2. Use only development data for parameter/design decisions.
3. Define the candidate family and all tested configurations before running the new development experiment.
4. Add explicit cost-aware evaluation rather than relying on gross mean return.
5. Prefer economically meaningful expectancy and cost resilience over raw trade count.
6. Continue to report median return, breadth, tail behavior, drawdown, concurrency, concentration, and chronological stability.
7. Keep the holdout untouched until a candidate passes the development freeze record.
8. If no candidate survives conservative costs, reject this implementation and move to a different Strategy 001 experiment rather than forcing a holdout result.

## 8. Reproducibility record

The user's local run reported **95 tests passing**. The stability analysis completed and explicitly reported that no holdout data was loaded. The cost-sensitivity analysis also completed without loading holdout data. The remaining stability-script warning has now been addressed in the repository.

The warning fix is a code-quality change only: it does not alter the frozen 001D strategy, U1 membership, development dates, candidate grid, stability calculations, or cost-sensitivity methodology. After pulling the latest commits, rerun the test suite and both development diagnostics locally and confirm that the warning is absent and the generated numerical outputs are unchanged.
