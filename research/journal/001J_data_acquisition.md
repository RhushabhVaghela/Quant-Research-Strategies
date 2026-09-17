# Strategy 001J — U1 Data Acquisition Gate

**Status:** In progress — PIT membership and 5-minute data are still external acquisition blockers.

## Objective

Build a defensible point-in-time Nifty 100 membership table and corresponding 5-minute NSE equity data for the 001J experiment. The research must not apply the September 2026 constituent list to the entire historical sample.

## Verified index facts

NSE describes Nifty 100 as a diversified 100-stock index representing major sectors and tracking the combined portfolio of Nifty 50 and Nifty Next 50. NSE/Nifty Indices documents Nifty 100 as semi-annually reconstituted in March and September, with additional reviews possible for corporate events, suspension, delisting, or schemes of arrangement.

Primary references:

- https://www.nseindia.com/static/products-services/indices-nifty100-index
- https://www.niftyindices.com/resources/index-rebalancing-schedule
- https://www.niftyindices.com/Methodology/Method_NIFTY_Equity_Indices.pdf

## Historical-source policy

Preferred order:

1. Official NSE/NSE Indices historical constituent/reconstitution records.
2. A licensed historical constituent dataset with explicit effective dates.
3. A documented secondary reconstruction only when primary historical records cannot be obtained, with every interval carrying its source and reconstruction note.

NSE Indices explicitly offers historical index constituent data by subscription and identifies quantitative research as a use case. If a licensed historical feed is used, its provider, product, coverage, retrieval date, and license constraints must be recorded in the metadata.

A current constituent CSV by itself is **not** an acceptable historical universe.

## Required membership evidence

The canonical membership table is:

`data/universe/strategy_001j_u1_membership.csv`

Required columns:

```text
symbol,effective_from,effective_to
```

Intervals are interpreted as half-open: `[effective_from, effective_to)`.

The metadata file must record at minimum:

- source name/provider;
- source URL or document/product identifier;
- retrieval date;
- coverage start/end;
- publication/effective dates where available;
- transformation/reconstruction steps;
- symbol-mapping notes;
- any known gaps or secondary cross-checks.

Validation:

```powershell
python scripts/validate_strategy_001j_u1_membership.py
```

The validator intentionally fails while the membership file is empty.

## Historical reconstruction policy

Public index pages establish the index definition and reconstitution schedule, but a current constituent page is a current-state view. We therefore must not infer all historical intervals from today's list.

Dated index/fund portfolio documents can be used as secondary cross-checks when they clearly identify an observation/effective date. They must be recorded as secondary evidence and must not silently replace official index membership.

## 5-minute equity data

Required local layout:

```text
data/
├── universe/
│   ├── strategy_001j_u1_membership.csv
│   └── strategy_001j_u1_membership_metadata.json
└── raw/
    └── strategy_001j_u1/
        ├── SYMBOL1.csv
        ├── SYMBOL2.csv
        └── ...
```

Each bar file must contain:

```text
timestamp,open,high,low,close,volume
```

Data requirements:

- NSE equity instruments only;
- 5-minute OHLCV;
- timestamps normalized to `Asia/Kolkata`;
- duplicate timestamps rejected;
- chronological order verified;
- missing-bar diagnostics retained;
- positive OHLC prices;
- non-negative volume;
- corporate-action adjustment convention documented;
- historical symbol changes/mappings documented.

Do not use a data source that silently backfills unavailable historical bars or silently mixes adjusted and unadjusted price conventions.

## Data audit

Run:

```powershell
python scripts/audit_strategy_001j_u1_data.py
```

The audit must be followed by a membership-to-data coverage check before the baseline. Having 100 CSV files is not sufficient: every PIT membership interval used by the research must have corresponding symbol data for the relevant dates.

## Similarity diagnostics

After the data audit and before candidate selection, run the locked, outcome-independent GOLDBEES behavior comparison with an explicit frozen observation boundary:

```powershell
python scripts/analyze_strategy_001j_universe_similarity.py `
  --reference <path-to-goldbees-5m.csv> `
  --universe-dir data/raw/strategy_001j_u1 `
  --end <frozen-utc-or-offset-aware-boundary>
```

Output:

`data/reports/strategy_001j_universe_similarity/similarity.csv`

This report is diagnostic only. It must not alter U1 based on Strategy 001J P&L.

## Stop conditions

Do not run the Strategy 001J baseline or parameter grid until:

- PIT membership validation passes;
- source metadata is complete;
- historical symbol mapping is documented;
- membership-to-data coverage is verified;
- 5-minute data audit passes;
- timestamp/session conventions are verified;
- corporate-action handling is documented;
- the exact development and holdout boundaries are frozen.

The current repository intentionally contains an empty membership template and no raw U1 CSVs. No historical market data should be fabricated to clear these gates.
