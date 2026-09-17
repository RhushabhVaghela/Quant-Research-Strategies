# Strategy 001J — Data Source Playbook

**Status:** Locked acquisition plan; no historical membership or raw market data is embedded here.

## 1. PIT Nifty 100 membership

### Preferred route — official historical data

Use NSE/NSE Indices historical constituent/reconstitution records when available. The official Nifty 100 page provides the current constituent list and index methodology, while the reconstitution calendar documents the regular March/September schedule and notes possible additional reviews.

Official references:

- NSE Nifty 100: https://www.nseindia.com/static/products-services/indices-nifty100-index
- NSE Indices reconstitution calendar: https://www.niftyindices.com/resources/index-rebalancing-schedule
- NSE Indices equity-index methodology: https://www.niftyindices.com/Methodology/Method_NIFTY_Equity_Indices.pdf

### Licensed route

NSE Indices states that historical index constituent data is available through its data products/subscription service and lists quantitative research among the intended uses. A licensed provider may therefore be used if it supplies explicit historical effective dates and symbol identifiers.

Record the provider/product, license/usage restrictions, coverage, retrieval date, and transformation steps in `strategy_001j_u1_membership_metadata.json`.

### Secondary reconstruction

Use only if the preferred routes cannot provide the required historical coverage. Reconstruct each interval from dated reconstitution evidence and retain a source ledger for every change. Secondary evidence may include dated index/fund portfolio documents, but it must be labeled secondary and cross-checked where possible.

Do **not** construct history by taking the current Nifty 100 list and assuming it was always the membership set.

## 2. Required coverage window

Before acquiring large volumes of 5-minute data, freeze the intended 001J development and holdout dates from the verified source coverage. Do not choose dates after inspecting strategy performance.

The minimum research period must provide enough history for:

- the 30-bar feature warm-up;
- development analysis;
- chronological holdout;
- any separately planned prospective activation period.

Exact dates belong in the experiment record after source coverage is verified.

## 3. 5-minute equity data

The required dataset is NSE equity 5-minute OHLCV with timestamps that can be normalized to `Asia/Kolkata` and a documented raw-vs-adjusted price convention.

Potential acquisition routes include:

1. an existing licensed historical NSE intraday dataset;
2. an exchange/broker data service that explicitly permits the required historical depth and research use;
3. another documented source only after verifying timestamps, corporate actions, symbol history, and completeness.

The repository should not contain credentials or private API keys. Raw licensed data should not be committed unless its license permits redistribution.

## 4. Required local ingestion contract

Membership:

`data/universe/strategy_001j_u1_membership.csv`

Metadata:

`data/universe/strategy_001j_u1_membership_metadata.json`

Raw bars:

`data/raw/strategy_001j_u1/<SYMBOL>.csv`

Schema:

```text
timestamp,open,high,low,close,volume
```

## 5. Validation sequence

After loading membership:

```powershell
python scripts/validate_strategy_001j_u1_membership.py
```

After loading raw bars:

```powershell
python scripts/audit_strategy_001j_u1_data.py
```

After the research window is frozen:

```powershell
python scripts/validate_strategy_001j_data_gate.py `
  --start <YYYY-MM-DDTHH:MM:SS+05:30> `
  --end <YYYY-MM-DDTHH:MM:SS+05:30>
```

Only after all three gates pass should the GOLDBEES similarity report and Strategy 001J baseline be run.

## 6. Source ledger requirements

For every membership reconstruction or mapping change, preserve:

- symbol as supplied by the source;
- canonical repository symbol;
- effective-from date/time;
- effective-to date/time;
- source document/URL/product;
- source publication date;
- retrieval date;
- transformation applied;
- confidence/cross-check note.

For raw bars, preserve:

- provider/source;
- extraction date;
- requested date range;
- timezone convention;
- adjusted/unadjusted status;
- corporate-action treatment;
- any missing sessions or symbols;
- symbol renames/mergers/delistings affecting the sample.

## 7. No-data stop condition

If the required historical PIT membership or 5-minute data cannot be obtained with defensible provenance, Strategy 001J remains blocked. Do not manufacture data, substitute today's universe for historical membership, or proceed directly to backtesting.
