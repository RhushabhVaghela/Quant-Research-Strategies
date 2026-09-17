# Strategy 001J — Universe Similarity & Behavior Discovery Protocol

**Status:** Protocol locked before Strategy 001J candidate results

## Purpose

Strategy 001J keeps U1 — the point-in-time Nifty 100 — as its **predefined primary universe**. This protocol adds a separate descriptive research layer to answer a different question:

> Which U1 securities exhibit behavior that is descriptively similar to the frozen GOLDBEES reference instrument?

The analysis is intended to improve understanding of the transfer problem and to prioritize future research. It is **not** a strategy-performance filter and it must not be used to cherry-pick a subset of U1 after observing Strategy 001J returns.

## Why correlation alone is insufficient

A return-correlation matrix can identify instruments that tend to move together, but correlation alone does not establish that two instruments share the same short-horizon continuation mechanism. The discovery layer therefore records correlation alongside predefined behavioral descriptors.

The initial descriptor set is deliberately simple and auditable:

1. Pearson correlation of aligned 5-minute close-to-close returns;
2. Pearson correlation of daily close-to-close returns;
3. annualized daily-return volatility;
4. lag-1 autocorrelation of 5-minute returns;
5. mean absolute 5-minute return;
6. positive-return fraction of 5-minute observations;
7. upper-tail frequency using the reference instrument's positive-return threshold;
8. observation count and overlapping-session coverage.

These are descriptive properties, not signals.

## Reference instrument

GOLDBEES is the behavioral reference because 001D is the frozen Strategy 001 implementation. The 001D rules remain immutable. The similarity analysis does not modify 001D or use 001I outcomes.

## Point-in-time discipline

Similarity diagnostics must be computed from a **pre-specified observation window**. The end date/time must be recorded before Strategy 001J performance results are inspected if the diagnostics will be used to prioritize later research.

The script therefore requires an explicit `--end` boundary. Data after that boundary is excluded.

If historical membership is available, U1 eligibility is still governed by the PIT membership file. A current constituent list must never be substituted for historical membership.

## Interpretation rules

- High 5-minute correlation means synchronized short-horizon returns, not identical economics.
- High daily correlation can coexist with very different intraday behavior.
- Similar volatility does not imply similar return dynamics.
- Autocorrelation is descriptive and can be unstable for short samples.
- Tail frequency is sensitive to the chosen reference threshold and is therefore reported, not treated as a standalone selection rule.
- Missing observations and different trading calendars can materially affect correlations.
- ETF-vs-equity microstructure differences are expected and must be documented rather than silently normalized away.

## No performance-based universe selection

The following are prohibited for 001J:

- selecting symbols because they produced the highest Strategy 001J backtest return;
- selecting a correlation cutoff after seeing Strategy 001J P&L;
- selecting a subset because it creates a preferred trade count;
- removing symbols after inspecting their Strategy 001J outcomes;
- using holdout or prospective returns to alter the discovery universe.

U1 remains the primary transfer test precisely because it is defined independently of historical Strategy 001J performance.

## Future use

The output may be used to:

- understand which U1 securities resemble the GOLDBEES behavioral profile;
- diagnose why transfer performance differs across securities;
- prioritize a separately registered future universe experiment;
- inform a genuinely different statistical-arbitrage research program where correlation/PCA/clustering is part of the economic hypothesis.

If a future experiment uses a similarity-selected universe as an actual trading universe, that selection rule must be pre-registered under a new experiment/version and evaluated without using the resulting strategy performance to define the rule.

## Output contract

The analysis script writes one row per U1 symbol with the predefined descriptors and a descriptive distance/rank. The output is diagnostic; there is no `selected=true` field and no automatic strategy-universe filtering.

Expected output:

`data/reports/strategy_001j_universe_similarity/similarity.csv`

## Stop condition

Do not interpret the similarity report as evidence of profitability. Strategy 001J still requires the independent PIT-universe validation, data audit, frozen development/holdout design, baseline, parameter experiment, costs, and prospective validation specified in the main experiment specification.
