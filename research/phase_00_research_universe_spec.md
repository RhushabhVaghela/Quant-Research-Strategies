# Phase 0 — Research Universe Specification

**Status:** Initial universe-design specification.

## 1. Objective

Move from a single validation instrument (NIFTYBEES) to a research universe that can test whether a candidate intraday effect is:

- economically feasible;
- statistically repeatable;
- portable across instruments;
- robust to market regimes;
- executable with the project's capital constraint.

## 2. Initial universe scope

The first universe should focus on **NSE-listed cash equities and ETFs** with reliable historical OHLCV data through the intended broker/data source.

We intentionally defer futures and options until the cash-market research process is stable.

## 3. Inclusion criteria

A candidate instrument should satisfy most or all of the following:

1. NSE-listed cash equity or ETF.
2. Reliable instrument-master resolution through the data layer.
3. Sufficient 5-minute historical data for event-study and out-of-sample analysis.
4. No persistent data-quality failures.
5. Sufficient liquidity for the intended position size.
6. Reasonable price level for a small account.
7. Sufficient trading activity to avoid a strategy being driven by stale/zero-volume bars.
8. Execution assumptions that can be stress-tested.
9. No obvious corporate-action/data-adjustment problem in the research sample.
10. Suitable for the intended long/short or long-only strategy design.

## 4. Important selection rule

**Do not select instruments because they produced the best historical strategy performance.**

Universe selection must be determined independently of the strategy outcome where possible. Otherwise the project risks survivorship/data-mining bias.

## 5. Candidate categories

We will eventually compare:

### A. Broad-market ETFs

Examples may include NIFTYBEES and other liquid index ETFs, subject to current liquidity/data checks.

Purpose:

- market-level behavior;
- clean first prototype;
- lower single-company event risk.

### B. Highly liquid large-cap equities

A diversified set of liquid NSE large-cap names can test whether an effect survives beyond an index ETF.

Purpose:

- cross-sectional validation;
- stock-specific intraday behavior;
- larger sample of independent-looking events.

### C. Sector ETFs / sector-linked instruments

Potentially useful for testing whether a phenomenon is market-wide or sector-specific.

### D. Other instruments

Futures/options/other products are deferred until their contract, margin, expiry, settlement and execution constraints are separately specified.

## 6. Data requirements

For every instrument, retain:

- symbol;
- exchange;
- instrument token;
- instrument type;
- trading dates;
- 5-minute OHLCV;
- timezone-normalized timestamps;
- data source;
- retrieval date;
- validation report;
- audit report.

Where possible, preserve raw data separately from cleaned/derived datasets.

## 7. Required universe-level diagnostics

Before strategy testing, generate:

- number of trading sessions;
- bars/session distribution;
- missing/duplicate timestamps;
- zero-volume bars;
- return distribution;
- volume distribution;
- time-of-day activity;
- median/percentile price;
- approximate turnover/liquidity measures;
- data coverage period.

The diagnostic output should make it obvious which instruments are unsuitable before strategy optimization begins.

## 8. Avoiding universe bias

The final universe should not be constructed by looking at which securities made the strategy look good.

Prefer a predefined or reproducible eligibility rule such as:

```text
liquid + data-complete + supported product type
```

and then run the same research process across the resulting universe.

## 9. NIFTYBEES checkpoint

NIFTYBEES is currently the first completed data checkpoint:

- 21 trading sessions in the August 2026 sample;
- 75 five-minute bars per session;
- 1,575 rows;
- no duplicate timestamps;
- no unexpected intraday gaps;
- no zero-volume rows.

These facts establish that the data pipeline works for this instrument. They do **not** establish that NIFTYBEES is the best trading instrument or that the tested event contains a tradable edge.

## 10. Next research task

Build an instrument-universe discovery/audit workflow before extending the current event study to ML.

The workflow should:

1. download/resolve a predefined candidate list;
2. fetch a common historical window where practical;
3. run validation and audit;
4. calculate basic liquidity/return diagnostics;
5. produce a comparable universe report;
6. identify instruments that pass the minimum research criteria;
7. only then continue with directional event studies.
