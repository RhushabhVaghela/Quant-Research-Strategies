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

The gate is session-aware and should be run against the frozen window:

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

The gate now uses Python's explicit `datetime.timedelta` values for fixed session offsets, avoiding the NumPy generic-timedelta deprecation warnings seen during the first repaired run. This is a code-quality fix only; the validation contract is unchanged.

### Repairing an incomplete final session

The original full-history download may end before the final frozen session for some symbols. Do **not** use `--overwrite` to repair this: `--overwrite` intentionally replaces a symbol file with only the requested range.

Use the downloader's safe `--merge` mode instead. It preserves the existing history, adds the requested repair range, sorts by timestamp, and replaces overlapping timestamps with the newly fetched observations:

```cmd
python scripts/fetch_strategy_001j_kite_data.py --start 2026-09-17 --end 2026-09-17 --symbols-file data/universe/strategy_001j_u1_membership.csv --output-dir data/raw/strategy_001j_u1 --merge --manifest data/reports/strategy_001j_kite_repair_20260917.csv
```

After the repair, rerun both checks:

```cmd
python scripts/audit_strategy_001j_u1_data.py --input-dir data/raw/strategy_001j_u1
python scripts/validate_strategy_001j_data_gate.py --start 2026-05-12 --end 2026-09-17
```

A data-gate failure must be repaired at the data layer. Do not relax the gate merely to obtain a green result.

## Step 4 — Frozen 001D transfer baseline

Only after all data gates pass:

```cmd
python scripts/run_strategy_001j_baseline.py --start 2026-05-12 --end 2026-09-17
```

The runner uses the exact frozen 001D parameters and is recorded before the 162-configuration development grid. It is a transferability baseline, not an optimizer.

## Step 5 — Development grid

The preregistered grid is exactly 162 configurations:

- lookback: 20, 30, 40 bars;
- z threshold: 1.5, 2.0, 2.5;
- trend: 3, 6, 9 bars;
- holding: 3, 6, 9 bars;
- cooldown: 6, 12 bars.

The development runner is deliberately hard-coded to **2026-06-10 through 2026-08-19** and cannot evaluate the chronological holdout. Run:

```cmd
python scripts/run_strategy_001j_development_grid.py
```

Outputs are written under `data/reports/strategy_001j_development_grid/`:

- `development_grid.csv` — one row per configuration;
- `development_trades.csv` — reproducible trade ledger for development;
- `run_metadata.csv` — frozen phase and selection-discipline metadata.

The grid runner does **not** automatically declare the highest-returning configuration the winner. Candidate review must consider breadth, central tendency, tails, costs, drawdown, concentration, chronological subperiod stability, and neighboring-parameter stability. Record the chosen configuration in `research/journal/001J_candidate_freeze_template.md` before opening the holdout.

## Step 6 — Holdout

Holdout covers **2026-08-20 through 2026-09-17**. Only one already-frozen candidate may be evaluated. The holdout runner requires the five parameter values explicitly and contains no grid search:

```cmd
python scripts/run_strategy_001j_holdout.py --lookback <FROZEN_LOOKBACK> --z <FROZEN_Z> --trend <FROZEN_TREND> --holding <FROZEN_HOLDING> --cooldown <FROZEN_COOLDOWN>
```

Outputs are written under `data/reports/strategy_001j_holdout/`.

Do not modify the candidate after seeing holdout results. If the holdout is weak or unstable, record that outcome rather than retuning against it.

## Step 7 — Similarity diagnostics

The outcome-independent GOLDBEES comparison remains descriptive only. It cannot change U1 after seeing Strategy 001J outcomes.

## Step 8 — Prospective paper/shadow

After holdout review and candidate freeze, a surviving configuration can enter a prospective broker-data paper/shadow phase. The live collector must use only signal-time information, next-bar execution assumptions, forward path/MFE/MAE capture, and explicit gross-versus-executable cost accounting. No live orders are implied by this phase.

## PIT Nifty 100 remains deferred

The original Nifty 100 acquisition path is not deleted. If historical constituent data becomes available later, it should be loaded as a separate clean-universe experiment under Strategy 001, with its own data provenance. The tactical Kite-native result must not be rewritten as PIT evidence.

## Stop conditions

Do not fabricate historical membership, use Strategy 001J returns to construct U1, weaken the frozen experiment window after inspecting results, or silently substitute current constituents for historical index membership. If the Kite data lacks sufficient session-level coverage or integrity for the frozen research window, stop and record the failure rather than weakening the methodology.
