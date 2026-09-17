# Strategy 001J — Universe Similarity & Behavior Discovery Protocol

**Status:** Protocol locked before Strategy 001J candidate results

## Purpose

Strategy 001J keeps U1 — the point-in-time Nifty 100 — as its **predefined primary universe**. This protocol adds a separate descriptive research layer to answer:

> Which U1 securities exhibit behavior that is descriptively similar to the frozen GOLDBEES reference instrument?

The analysis improves understanding of transferability and can prioritize future research. It is **not** a strategy-performance filter and must not be used to cherry-pick a subset of U1 after observing Strategy 001J returns.

## Why correlation alone is insufficient

Return correlation identifies co-movement, but correlation alone does not establish that two instruments share the same short-horizon continuation mechanism. The discovery layer therefore records correlation alongside predefined behavioral descriptors.

Initial descriptors:

1. aligned 5-minute close-to-close return correlation;
2. aligned daily close-to-close return correlation;
3. annualized daily-return volatility;
4. lag-1 autocorrelation of 5-minute returns;
5. mean absolute 5-minute return;
6. positive-return fraction of 5-minute observations;
7. upper-tail frequency using a fixed GOLDBEES reference threshold;
8. observation and overlap counts.

These are descriptive properties, not signals.

## Reference instrument

GOLDBEES is the behavioral reference because 001D is the frozen Strategy 001 implementation. The 001D rules remain immutable. The similarity analysis does not modify 001D or use 001I outcomes.

## Point-in-time discipline

The similarity report requires an explicit observation end boundary. Data after that boundary is excluded. If the report will be used to prioritize later research, the boundary must be recorded before Strategy 001J performance results are inspected.

Historical U1 eligibility remains governed by the PIT membership file. A current constituent list must never be substituted for historical membership.

## Interpretation rules

- High 5-minute correlation means synchronized short-horizon returns, not identical economics.
- High daily correlation can coexist with different intraday behavior.
- Similar volatility does not imply similar return dynamics.
- Autocorrelation can be unstable for short samples.
- Tail frequency depends on the chosen reference threshold and is therefore descriptive, not a standalone selection rule.
- Missing observations and different trading calendars can affect correlations materially.
- ETF-vs-equity microstructure differences are expected and must be documented rather than silently normalized away.

## Prohibited uses

For 001J, do not:

- select symbols because they produced the highest Strategy 001J return;
- choose a correlation cutoff after seeing Strategy 001J P&L;
- select a subset because it creates a preferred trade count;
- remove symbols after inspecting their Strategy 001J outcomes;
- use holdout or prospective returns to alter U1.

U1 remains the primary transfer test because it is defined independently of Strategy 001J performance.

## Future use

The report may:

- identify behavioral similarities for interpretation;
- diagnose cross-sectional transfer differences;
- prioritize a separately registered future universe experiment;
- inform a genuinely different statistical-arbitrage research program where correlation/PCA/clustering is part of the hypothesis.

Any future similarity-selected trading universe must have its selection rule pre-registered as a new experiment/version before its performance is evaluated.

## Output

`scripts/analyze_strategy_001j_universe_similarity.py` writes:

`data/reports/strategy_001j_universe_similarity/similarity.csv`

The output has a descriptive distance/rank but no automatic `selected=true` field and does not filter the trading universe.

## Stop condition

The similarity report is not profitability evidence. Strategy 001J still requires PIT membership validation, data audit, baseline transfer test, frozen development/holdout design, robustness, costs, and prospective validation.
