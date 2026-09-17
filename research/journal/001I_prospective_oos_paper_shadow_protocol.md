# Strategy 001I — Prospective OOS / Paper-Shadow Validation Protocol

## Purpose

001I was the first genuinely prospective out-of-sample gate for Strategy 001. The historical research sample had been examined through August 2026. 001I observed the already-frozen 001D strategy prospectively, with each signal recorded before its future outcome was known.

The 001I cohort is now **closed for capital-pursuit priority** because the frozen single-instrument GOLDBEES implementation is too low-frequency for the September 2026 accelerated research/deployment objective. This closure is a research-priority decision, not a statistical rejection based on the two observed trades.

## 1. OOS boundary and closure

The original prospective OOS boundary was the activation timestamp recorded in `data/prospective/strategy_001i/run_manifest.json`.

Rules for the completed cohort:

1. Data observed before activation remained historical/research data.
2. Signals were captured at the event-bar boundary before their fixed future outcomes were known.
3. The 001D parameters were not changed during the cohort.
4. The prospective outcomes were not used to retune 001D.
5. The captured 001I ledger is preserved as an immutable research record.
6. No new 001I collection is required for the current capital-pursuit sprint.
7. Reuse of the continuation hypothesis on another universe or with different parameters is registered as a new experiment under the Strategy 001 research family; it does not modify 001D or restart 001I.

## 2. Frozen strategy that was tested

001I observed Strategy 001D exactly as frozen:

- GOLDBEES 5-minute OHLCV;
- previous 30 completed same-session closes;
- sample standard deviation;
- z-score ≥ +2.0;
- prior six-bar return > 0;
- long-only;
- signal at event-bar close;
- next-bar-open entry;
- close of `t+6` exit;
- 12-bar cooldown;
- no overnight feature construction;
- one position at a time;
- no leverage or optimized sizing.

No threshold, lookback, holding period, cooldown, time-of-day filter, stop, target, or ML filter was introduced into 001I.

## 3. Paper/shadow implementation

The collector used Zerodha/KiteTicker live data, built completed 5-minute GOLDBEES bars, logged point-in-time signals, and finalized paper outcomes after the frozen exit candle completed. It never placed orders.

The captured run passed the repository's prospective-ledger integrity validator.

## 4. Why the cohort is closed

The observed 2026-09-17 session produced only two selected trades. That is too little evidence for statistical rejection, but it demonstrates that the frozen **single-instrument** implementation is not an efficient primary vehicle for the current deadline.

Therefore:

> **Do not wait for 001I to accumulate more trades. Do not optimize 001D from this prospective sample. Close the cohort and move the research effort to the broader 001J experiment.**

The underlying continuation hypothesis remains a Strategy 001 research hypothesis and is being tested in 001J using a predefined point-in-time equity universe and a separately registered parameter-selection process.

## 5. Execution-cost measurement retained

The original protocol required separate recording of quoted spread, intended/observable prices, slippage, and brokerage/statutory costs. The 2026-09-17 paper records did not contain realized broker execution costs; those fields remained zero/blank under paper assumptions. This limitation is retained in the results record and must be addressed by any future controlled-live protocol.

## 6. No-look-ahead controls retained

The following controls remain part of the research standard:

1. Future bars cannot enter signal construction.
2. Outcomes cannot be used to retune an already frozen cohort.
3. Losing observations cannot be removed manually.
4. MFE/MAE cannot be used retrospectively to create stops/targets.
5. Entry/exit prices cannot be selected after seeing the forward path.
6. A changed rule receives a new experiment identifier.

## 7. Relationship to Strategy 001J

001J is a new experiment under Strategy 001, not a continuation of the same prospective 001I cohort. It tests the same broad economic continuation hypothesis across a predefined point-in-time equity universe and may perform a separately registered parameter-selection experiment on development data.

See:

- `research/journal/001J_cross_sectional_equity_spec.md`
- `research/journal/001J_universe_u1_spec.md`
- `research/journal/strategy_registry.md`

The 001I ledger and conclusions must not be overwritten to make 001J appear to be the same OOS cohort.

## 8. Final status

**🔵 001I closed for capital-pursuit priority.**

The frozen 001D GOLDBEES strategy remains a completed research artifact with historical evidence and a small genuine prospective sample. It is not approved for live deployment.

The next active experiment is Strategy **001J**.
