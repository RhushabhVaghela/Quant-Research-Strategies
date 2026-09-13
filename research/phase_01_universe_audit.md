# Phase 1 — Multi-Instrument Research-Universe Audit

**Status:** Tooling and candidate manifest implemented; local broker-data execution is the next step.

## Objective

Move beyond the single NIFTYBEES pipeline checkpoint and test whether the research process can be applied consistently across a predefined set of NSE cash equities and ETFs.

The purpose of this phase is **data and research eligibility**, not strategy selection.

## Candidate manifest

The initial candidate list is stored in `research/universe_candidates.csv`.

It deliberately contains multiple categories:

- broad-market ETF;
- sector ETFs;
- liquid large-cap equities across banking, technology, telecom, industrials, consumer, metals, automotive and pharmaceuticals.

The list is a reproducible starting universe, not a claim that every candidate is currently eligible for live trading. Instrument resolution and current market characteristics must be checked from the broker/exchange data before research use.

## Reproducible resolution

The script `scripts/build_research_universe.py` resolves each candidate against the cached NSE instrument master.

Run after the instrument master has been refreshed locally:

```powershell
python scripts/build_research_universe.py
```

The output records:

- symbol;
- category and rationale;
- current instrument token from the broker master;
- instrument type and segment;
- current `last_price` reported by the instrument master;
- number of whole units theoretically affordable from ₹30,000 at that reported price;
- resolution status.

The ₹30,000 calculation is a **screening diagnostic only**. It does not account for margin rules, transaction costs, slippage, broker RMS, or whether one unit provides economically meaningful exposure.

## Historical data collection

For each resolved candidate, download a common 5-minute historical window using the existing `scripts/download_historical.py` pipeline.

The first goal is a sufficiently long common sample for event studies and time-ordered out-of-sample analysis. The August 2026 NIFTYBEES sample of 21 sessions remains only a pipeline checkpoint and is not sufficient for final conclusions.

Do not optimize a strategy while selecting the universe.

## Audit

After data collection:

```powershell
python scripts/audit_universe.py data/raw --output data/reports/universe_audit.csv
```

The same structural checks must be applied across all candidate datasets.

Current minimum structural filter:

- at least 20 trading sessions;
- at least 1,000 rows;
- zero duplicate timestamps;
- zero unexpected intraday intervals;
- zero zero-volume rows.

These thresholds are **minimum data-quality gates**, not evidence that an instrument is liquid enough for live trading.

## Liquidity and capital checks still required

The current universe audit must be extended/combined with diagnostics for:

- price distribution;
- volume distribution;
- approximate traded value/turnover;
- time-of-day liquidity;
- spread/execution assumptions where data permits;
- position size under the ₹30,000 account constraint;
- transaction costs and slippage stress.

No candidate should be promoted to strategy research solely because its OHLCV file passes structural checks.

## Universe-bias control

The candidate list is defined before comparing strategy performance. Instruments must not be added, removed, or ranked because an early strategy backtest looks attractive.

If an instrument fails data-quality or execution-feasibility requirements, record the reason explicitly rather than silently deleting it.

## Next checkpoint

The user should run the following locally after pulling the latest repository:

```powershell
git pull
pytest
python scripts/build_research_universe.py
```

If the universe-resolution command succeeds, download the common historical sample for the resolved candidates. We will then inspect the actual audit output before designing the next event-study experiments.

**No live trade is required or recommended at this phase.**
