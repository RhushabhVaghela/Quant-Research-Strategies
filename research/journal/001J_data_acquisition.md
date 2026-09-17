# Strategy 001J — U1 Data Acquisition Gate

**Status:** In progress — membership contract created; historical point-in-time membership still must be loaded before the baseline is run.

## Objective

Build a defensible point-in-time Nifty 100 membership table and corresponding 5-minute NSE equity data for the 001J experiment. The research must not apply the September 2026 constituent list to the entire historical sample.

## Verified index facts

NSE describes Nifty 100 as a diversified 100-stock index representing major sectors and tracking the combined portfolio of Nifty 50 and Nifty Next 50. The NSE page currently provides the current constituent download and methodology. NSE Indices' reconstitution calendar states that Nifty 100 is reconstituted semi-annually on the last working day of March and September, with additional reviews possible for events such as suspension, delisting, or schemes of arrangement.

Primary references:

- https://www.nseindia.com/static/products-services/indices-nifty100-index
- https://www.niftyindices.com/resources/index-rebalancing-schedule

## Historical-source policy

Preferred order:

1. Official NSE/NSE Indices historical constituent/reconstitution records.
2. A licensed historical constituent dataset with explicit effective dates.
3. A documented secondary reconstruction only when primary historical records cannot be obtained, with every interval carrying its source and reconstruction note.

A current constituent CSV by itself is **not** an acceptable historical universe.

## Repository contract

Canonical membership file:

`data/universe/strategy_001j_u1_membership.csv`

Required columns:

```text
symbol,effective_from,effective_to
```

Metadata:

`data/universe/strategy_001j_u1_membership_metadata.json`

Validation:

```powershell
python scripts/validate_strategy_001j_u1_membership.py
```

The validator intentionally fails while the membership file is empty.

## Historical reconstruction notes

The public web evidence confirms the semi-annual schedule and provides historical reconstitution announcements, but the current NSE constituent page is a current-state page. Therefore the project must not infer all historical intervals from the current list.

As a secondary cross-check, dated ETF/fund portfolio documents can help verify historical snapshots. They must not silently replace official index membership. For example, dated Nifty 100 ETF portfolio documents are available for March 2025 and September 2024. Such documents should be recorded as secondary evidence if used for reconstruction.

## Next data task

Acquire the historical membership intervals first. Then acquire 5-minute OHLCV for every symbol needed by those intervals and run the data-coverage audit before any 001J baseline result is generated.

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

The baseline runner applies membership intervals before constructing signals.

## Stop condition

Do not run the Strategy 001J baseline or parameter grid until:

- membership validation passes;
- symbol mapping is documented;
- data coverage is audited;
- timestamp/session conventions are verified;
- corporate-action handling is documented;
- the exact development and holdout boundaries are frozen.
