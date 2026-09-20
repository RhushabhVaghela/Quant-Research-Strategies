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

### Common data window and validation reserve

The acquisition window is:

- start: 2025-09-18
- end: 2026-09-17

The full downloaded window must **not** be treated as one pool for pattern discovery, optimization, and final validation. The chronological research split is locked before pattern discovery:

| Phase | Dates | Allowed use |
|---|---|---|
| Exploratory development | 2025-09-18 through 2026-06-09 | Pattern discovery, descriptive analysis, hypothesis formation, controlled development |
| Development validation | 2026-06-10 through 2026-08-19 | Candidate comparison/robustness checks after a pattern/hypothesis is specified; no final holdout claims |
| Untouched chronological holdout/OOS | 2026-08-20 through 2026-09-17 | Final evaluation of one frozen candidate only; no pattern discovery, feature selection, threshold tuning, or strategy changes |

The holdout is therefore **already present in the downloaded files, but remains logically inaccessible to exploratory research**. All research code and analysis must filter by timestamp before calculating statistics that can influence decisions. A result computed over the entire 2025-09-18 through 2026-09-17 window must be treated as descriptive-only and must not be used to select a pattern, feature, hypothesis, parameter, or candidate.

The development-validation split also protects against repeatedly searching the earliest sample and then calling the same observations OOS. The final holdout is the strongest chronological protection and may only be opened after a candidate is frozen.

These dates are a research-control decision, not a claim that the eventual strategy must trade on every session or that all instruments have identical usable coverage.

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


## Acquisition result

The local common-window acquisition was completed for all 20 predefined candidates.

- 20/20 downloads completed successfully.
- 19/20 currently pass the structural minimum filter.
- HINDUNILVR is the only current structural exception, with one unexpected interval and five zero-volume rows.
- The other 19 candidates have zero duplicate timestamps, zero unexpected intervals, and zero zero-volume rows.
- The acquired files contain 247 trading sessions over the requested common window, with a median of 75 five-minute bars per session for the audited candidates.

The structural audit is an eligibility/data-quality result only. Return diagnostics from this audit are descriptive and must not be used to rank instruments or select a strategy.

HINDUNILVR is therefore excluded from the first clean cross-sectional pattern pass until the underlying quality issue is inspected. This is a data-quality decision, not a performance decision.

## Next phase — controlled pattern discovery

The first pattern-discovery workflow is now registered in:

- `research/journal/002_pattern_discovery_protocol.md`
- `scripts/run_strategy_002_pattern_discovery.py`
- `tests/test_strategy_002_pattern_discovery.py`

The runner is hard-bounded to the exploratory-development period:

`2025-09-18 through 2026-06-09`.

It performs only descriptive diagnostics:

- return autocorrelation and absolute-return autocorrelation;
- fixed forward-horizon conditional return diagnostics;
- intraday/time-of-day structure;
- aligned cross-sectional correlation and dispersion;
- descriptive PCA/common-factor diagnostics.

It produces no strategy P&L, no parameter optimization grid, and no holdout statistics.

The development-validation period and final holdout remain logically inaccessible to this workflow. The final holdout cannot be opened until a specific economic hypothesis and executable candidate have been defined, developed, validated, and frozen.

## Current research decision

Proceed with the hypothesis-free exploratory pattern pass using the 19 currently structurally eligible instruments. Preserve HINDUNILVR as a documented data-quality exception rather than silently dropping it from the research universe.

No Strategy 002 economic hypothesis has been selected.
