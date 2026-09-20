# Strategy 002 — Initial Data Audit

**Status:** Active research. No trading hypothesis has been selected.

## Objective

Establish what the available market data can support before choosing a return mechanism. This phase is descriptive and eligibility-focused; it does not optimize a strategy or select instruments using historical strategy P&L.

## Existing repository resources reused

The repository already contains a general research-universe workflow:

- `research/phase_00_research_universe_spec.md`
- `research/phase_01_universe_audit.md`
- `research/universe_candidates.csv`
- `scripts/build_research_universe.py`
- `scripts/audit_universe.py`
- `scripts/audit_historical.py`
- `src/data/audit.py`
- `src/research/universe.py`

These are being used as the starting data layer rather than creating a duplicate Strategy 002 data pipeline.

## Initial candidate universe

The existing reproducible manifest contains 20 NSE candidates across:

- broad-market ETF;
- sector ETFs;
- a commodity ETF;
- liquid large-cap equities across banking, technology, telecom, industrials, consumer, metals, automotive, and pharmaceuticals.

The manifest is a research starting point only. It is not selected on the basis of Strategy 002 performance.

The existing resolved report contains broker instrument mappings for these candidates, but its `last_price` fields are zero-valued in the committed report, so current price/liquidity conclusions must not be inferred from that artifact. A fresh local instrument-master resolution is required.

## Audit gates

Before pattern discovery, the local dataset should be checked for:

1. instrument resolution against a refreshed NSE instrument master;
2. common historical coverage;
3. duplicate timestamps;
4. non-monotonic timestamps;
5. unexpected intraday gaps;
6. session/bar-count consistency;
7. zero-volume observations;
8. return distribution;
9. volume distribution;
10. time-of-day behavior;
11. approximate traded value/liquidity;
12. obvious data-quality or corporate-action anomalies.

The existing minimum structural screen is 20 trading sessions and 1,000 rows, with zero duplicate timestamps, zero unexpected intraday intervals, and zero zero-volume rows. These are data-quality gates, not profitability or live-trading gates.

## Commands for the actual local audit

After pulling main and refreshing the broker instrument master:

```cmd
git pull origin main
pytest -q
python scripts/build_research_universe.py
python scripts/audit_universe.py data/raw --output data/reports/strategy_002_universe_audit.csv
```

The common historical window should be established from the actual available data after resolution rather than inventing a new strategy-specific window before the data is inspected.

## Pattern-discovery boundary

No holdout observations should be used to choose a pattern, feature, hypothesis, threshold, model, or strategy definition.

No trading engine or parameter grid is justified yet.

## Current conclusion

The repository already has enough generic infrastructure to begin the first real Strategy 002 phase. The next evidence required is the **actual refreshed instrument resolution and local OHLCV audit output**. Only after those results are inspected should we decide what descriptive analyses and pattern-discovery tests are warranted.

A pattern may be weak, unstable, or absent. That is a valid outcome; the audit must not be shaped to manufacture a strategy.
