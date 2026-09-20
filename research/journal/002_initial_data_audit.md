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

## Current audit result

The first local run produced:

- repository tests: 100 passed;
- 20/20 candidate instruments resolved against the current NSE instrument master;
- current last_price was reported as 0.0 for all 20 resolved rows;
- only two historical OHLCV datasets were present under the audited raw-data path:
  - GOLDBEES: 30,912 rows, 413 trading sessions, median 75 bars/session;
  - NIFTYBEES: 1,575 rows, 21 trading sessions, median 75 bars/session;
- both existing datasets passed the current structural-quality filter.

The zero-valued last_price field is not being treated as evidence that the instruments have zero market value. The universe builder reads last_price from the broker instrument-master record. That field is not a suitable basis for the current liquidity/capital screen until its provenance and population are verified. A Sunday market closure may prevent a fresh live quote, but it does not explain the absence of historical OHLCV files and is not sufficient reason to alter the data workflow.

## Historical data acquisition step

The next data-layer step is to acquire a common historical 5-minute OHLCV window for the predefined 20-instrument manifest before any pattern discovery.

A new generic utility reuses the repository's existing Kite authentication and historical-data functions:

- scripts/fetch_research_universe_kite_data.py
- src/data/kite_client.py
- src/data/historical.py
- src/data/validation.py

The new utility is deliberately data-layer only. It does not define a return hypothesis, signal, parameter grid, optimization rule, or strategy.

The output naming convention is compatible with scripts/audit_universe.py:

- NSE_<SYMBOL>_5minute.csv

The default local output directory is data/raw/strategy_002_universe/.

The downloader also writes a manifest and JSON metadata report under data/reports/. Raw market data remains local and is not expected to be committed to Git.

### Common window

For the accelerated September 2026 research sprint, use:

- start: 2025-09-18
- end: 2026-09-17

This is a data-availability window, not a strategy-training/holdout definition. The later pattern-discovery phase must establish its own development/holdout discipline without using the eventual holdout for exploratory selection.

### Local acquisition command

Run from the repository root:

```cmd
git pull origin main
pytest -q
python scripts/fetch_research_universe_kite_data.py --start 2025-09-18 --end 2026-09-17 --symbols-file research/universe_candidates.csv --output-dir data/raw/strategy_002_universe --manifest data/reports/research_universe_kite_download_manifest.csv
```

If a symbol download fails, the script records the failure and continues with the remaining symbols. Do not silently delete failed symbols from the predefined manifest.

After acquisition, audit the new directory:

```cmd
python scripts/audit_universe.py data/raw/strategy_002_universe --output data/reports/strategy_002_universe_audit.csv
```

The next research decision should be made from that audit. In particular, compare common coverage, session completeness, intraday gaps, zero-volume observations, return behavior, and liquidity proxies across the candidate set.

No instrument should be promoted because its historical returns look attractive. The purpose of this step is to establish a clean, comparable descriptive dataset for pattern discovery.
