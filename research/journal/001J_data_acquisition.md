# Strategy 001J — U1 Data Acquisition Gate

**Status:** Broker-native acquisition path ready; 90-session experiment window frozen; PIT Nifty 100 is deferred rather than fabricated.

## Decision

The original U1 design required point-in-time Nifty 100 membership. That remains the clean research target, but obtaining defensible historical membership is currently slower than the September 2026 research sprint permits.

The active tactical path therefore uses the existing Zerodha Kite Connect infrastructure already present in the repository:

- current NSE EQ instrument dump for token mapping;
- Kite historical-data API for 5-minute OHLCV;
- a pre-strategy liquidity formation window to create U1;
- no Strategy 001J performance information in universe formation.

This path is explicitly marked as having current-instrument/survivorship bias and is not silently presented as PIT Nifty 100.

## Frozen experiment window

The research window is now immutable for this sprint:

- **formation:** 2026-05-12 through 2026-06-09 — 20 sessions;
- **development:** 2026-06-10 through 2026-08-19 — 50 sessions;
- **holdout:** 2026-08-20 through 2026-09-17 — 20 sessions.

See `research/journal/001J_experiment_window.md` for the full lock. The window is 90 market sessions rather than 90 calendar days because the preregistered split is session-based. Kite's request-size limitation is handled by chunking and does not redefine the research window.

## Kite data capabilities relevant to 001J

Kite Connect provides an instrument master containing current tradable instruments and instrument tokens. Its historical candle API supports 5-minute candles. The repository downloader chunks requests conservatively.

The repository already contains `src/data/kite_client.py` and `src/data/historical.py`; the CLI wrapper is `scripts/fetch_strategy_001j_kite_data.py`.

## Step 1 — U1 formation data

The U1 liquidity formation window that produced the locked membership file is separate from the experiment formation phase above. U1 selection remains based only on median daily traded value and minimum formation-day coverage.

## Step 2 — Validate membership

```cmd
python scripts/validate_strategy_001j_u1_membership.py
```

## Step 3 — Validate the frozen experiment data window

The gate is now session-aware and should be run against the frozen window:

```cmd
python scripts/audit_strategy_001j_u1_data.py --input-dir data/raw/strategy_001j_u1
python scripts/validate_strategy_001j_data_gate.py --start 2026-05-12 --end 2026-09-17
```

The gate checks each selected symbol for:

- data in the frozen window;
- 09:15 IST first bar on each observed session;
- exact 5-minute increments with no interior gaps;
- positive OHLC and non-negative volume;
- at least 37 bars per session for one complete frozen-baseline trade path;
- no missing observed sessions across the locked U1;
- no timestamps beyond the normal 15:25 final 5-minute bar.

A terminal session ending at 15:10 is allowed if it is contiguous. A 72-bar session is therefore not automatically rejected merely because it does not contain the 15:15, 15:20, and 15:25 bars. An interior gap is rejected.

## Step 4 — Frozen 001D transfer baseline

Only after all data gates pass:

```cmd
python scripts/run_strategy_001j_baseline.py --start 2026-05-12 --end 2026-09-17
```

The runner now requires/uses the frozen experiment window rather than silently consuming all available U1 history. It uses the exact frozen 001D parameters and is recorded before the 162-configuration development grid.

## Step 5 — Development grid

After the transfer baseline is recorded, the preregistered 162-configuration grid may be evaluated on **development only** (2026-06-10 through 2026-08-19). The candidate is frozen before holdout.

## Step 6 — Holdout

Holdout covers 2026-08-20 through 2026-09-17. No holdout result may be used to retune the candidate.

## Step 7 — Similarity diagnostics

The outcome-independent GOLDBEES comparison remains descriptive only. It cannot change U1 after seeing Strategy 001J outcomes.

## PIT Nifty 100 remains deferred

The original Nifty 100 acquisition path is not deleted. If historical constituent data becomes available later, it should be loaded as a separate clean-universe experiment under Strategy 001, with its own data provenance. The tactical Kite-native result must not be rewritten as PIT evidence.

## Stop conditions

Do not fabricate historical membership, use Strategy 001J returns to construct U1, weaken the frozen experiment window after inspecting results, or silently substitute current constituents for historical index membership. If the Kite data lacks sufficient session-level coverage or integrity for the frozen research window, stop and record the failure rather than weakening the methodology.
