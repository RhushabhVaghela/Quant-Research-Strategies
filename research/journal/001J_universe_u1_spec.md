# Strategy 001J — Universe U1 Specification

**Status:** Definition locked; point-in-time membership acquisition is the next data gate.

## Primary universe

U1 is the **point-in-time Nifty 100 constituent universe** for the Strategy 001J cross-sectional equity experiment.

NSE describes Nifty 100 as a diversified 100-stock large-cap index representing major sectors and tracking the combined portfolio of Nifty 50 and Nifty Next 50. NSE Indices' reconstitution calendar lists Nifty 100 as semi-annually reconstituted on the last working day of March and September.

Sources:
- NSE Nifty 100: https://www.nseindia.com/static/products-services/indices-nifty100-index
- NSE Indices reconstitution calendar: https://www.niftyindices.com/resources/index-rebalancing-schedule

## Point-in-time membership

The canonical membership table is:

```text
symbol,effective_from,effective_to
```

A security is eligible only when its observation date falls inside its membership interval. Historical research must not apply the September 2026 constituent list to earlier dates.

Additional index changes caused by corporate actions, suspension, delisting, or other ad-hoc events must be represented when applicable. The methodology documentation notes that additional index review can occur for such events.

## Data-source policy

The preferred source for index composition is NSE/NSE Indices or a licensed historical constituent dataset that preserves effective dates. The repository should store a compact normalized membership table plus a metadata record containing:

- source name;
- source URL or document identifier;
- retrieval date;
- source publication/effective date where available;
- transformation steps;
- symbol-mapping notes.

Do not silently substitute an unofficial current constituent list for historical membership.

## Bar data

Primary research data:

- NSE equity;
- 5-minute OHLCV;
- exchange-local timestamps normalized to `Asia/Kolkata`;
- symbol-local session boundaries;
- duplicate timestamps rejected;
- missing-bar diagnostics retained.

Corporate-action adjustments and raw-vs-adjusted price conventions must be documented before the final backtest.

## Liquidity/data eligibility

The final eligibility rules must be frozen before candidate selection. Required checks include:

1. sufficient feature history;
2. sufficient 5-minute coverage;
3. no material missing-bar problem;
4. valid positive OHLC prices;
5. plausible volume;
6. broker/instrument mapping where execution is contemplated;
7. no unresolved corporate-action or symbol-mapping issue.

Liquidity thresholds are not to be selected by maximizing backtest performance.

## Exclusions

The first experiment excludes:

- ETFs, including GOLDBEES;
- futures and options;
- leveraged/inverse products;
- securities outside U1;
- securities whose historical identity cannot be mapped reliably;
- securities lacking adequate data for the relevant feature window.

GOLDBEES remains the frozen 001D instrument and is kept separate from U1.

## Similarity analysis is diagnostic, not universe selection

The experiment includes a separate GOLDBEES behavior-similarity report. It may use return correlation, volatility, autocorrelation, return-distribution descriptors, and overlap diagnostics to understand transferability.

This report does **not** replace U1. In particular, a symbol is not admitted to or removed from U1 because it has a favorable correlation, descriptive distance, or later Strategy 001J return. Any similarity-selected universe used for a future trading experiment must be registered as a separate experiment/version with its selection rule frozen before performance evaluation.

See `research/journal/001J_universe_discovery_protocol.md` and `scripts/analyze_strategy_001j_universe_similarity.py`.

## Expansion policy

If U1 produces insufficient observations after the pipeline is validated, a broader universe such as Nifty 200 may be evaluated as a **new universe experiment under Strategy 001**, with its own identifier and pre-registered rules. The universe must never be broadened retrospectively only because a preferred parameter configuration needs more trades.
