# Strategy 001J — U1 Data Acquisition Gate

**Status:** Broker-native acquisition path ready; PIT Nifty 100 is deferred rather than fabricated.

## Decision

The original U1 design required point-in-time Nifty 100 membership. That remains the clean research target, but obtaining defensible historical membership is currently slower than the September 2026 research sprint permits.

The active tactical path therefore uses the existing Zerodha Kite Connect infrastructure already present in the repository:

- current NSE EQ instrument dump for token mapping;
- Kite historical-data API for 5-minute OHLCV;
- a pre-strategy liquidity formation window to create U1;
- no Strategy 001J performance information in universe formation.

This path is explicitly marked as having current-instrument/survivorship bias and is not silently presented as PIT Nifty 100.

## Kite data capabilities relevant to 001J

Kite Connect provides an instrument master containing current tradable instruments and instrument tokens. Its historical candle API supports 5-minute candles. Current published Kite guidance indicates that a 5-minute request is limited to roughly 90 calendar days per request, but complete available history can be retrieved through multiple requests within the API rate limits. The repository downloader therefore chunks requests conservatively.

The repository already contains `src/data/kite_client.py` and `src/data/historical.py`; the CLI wrapper is `scripts/fetch_strategy_001j_kite_data.py`.

## Tactical research-window design

Use approximately **one year of 5-minute history** for the selected U1 symbols if Kite returns adequate coverage. This is materially preferable to restricting the experiment to only the most recent 90 days; 90 days is a per-request constraint, not a reason to throw away older available history.

For the September 2026 sprint, the intended structure is:

1. **Formation window:** first ~20 trading days — liquidity only.
2. **Development window:** the long middle portion of the one-year sample.
3. **Chronological holdout:** a substantial final portion, preferably ~3 months when the actual data coverage permits.
4. **Prospective phase:** begins only after candidate freeze and holdout review.

The exact calendar dates must be frozen from the actual downloaded coverage before inspecting Strategy 001J results.

## Step 1 — Fetch broker-native formation data

Fetch current NSE EQ candidates into:

`data/raw/strategy_001j_candidates/`

Example:

```powershell
python scripts/fetch_strategy_001j_kite_data.py `
  --start <FORMATION_START> `
  --end <FORMATION_END> `
  --all-nse-eq `
  --output-dir data/raw/strategy_001j_candidates
```

For a small smoke test, `--max-symbols 10` can be used. Do not use that reduced set for research.

The script uses the existing local Zerodha authentication layer. No credentials or access tokens belong in Git.

## Step 2 — Form U1 before strategy outcomes

Build the tactical U1 from the formation data:

```powershell
python scripts/build_strategy_001j_broker_liquid_universe.py `
  --input-dir data/raw/strategy_001j_candidates `
  --formation-start <FORMATION_START> `
  --formation-end <FORMATION_END> `
  --research-end <RESEARCH_END> `
  --top-n 50 `
  --min-days 15
```

Outputs:

- `data/reports/strategy_001j_broker_universe_ranking.csv`
- `data/universe/strategy_001j_u1_membership.csv`
- `data/universe/strategy_001j_u1_membership_metadata.json`

The ranking must be preserved as research evidence. No symbol may be removed because it later performs poorly, and no symbol may be added because it later performs well.

## Step 3 — Fetch full research-window data for selected U1

After U1 is generated, fetch the full research period for exactly those symbols. The downloader automatically splits long ranges into Kite-compatible chunks:

```powershell
python scripts/fetch_strategy_001j_kite_data.py `
  --start <FORMATION_START> `
  --end <RESEARCH_END> `
  --symbols-file data/universe/strategy_001j_u1_membership.csv `
  --output-dir data/raw/strategy_001j_u1
```

The downloader maps the membership CSV's `symbol` column to current Kite NSE EQ instruments.

## Step 4 — Validate membership and data

```powershell
python scripts/validate_strategy_001j_u1_membership.py
python scripts/audit_strategy_001j_u1_data.py
python scripts/validate_strategy_001j_data_gate.py `
  --start <RESEARCH_START> `
  --end <RESEARCH_END>
```

Do not run the baseline if any gate fails.

## Step 5 — Similarity diagnostics

Once the selected symbols and full bars exist, run the outcome-independent GOLDBEES comparison:

```powershell
python scripts/analyze_strategy_001j_universe_similarity.py `
  --reference <path-to-goldbees-5m.csv> `
  --universe-dir data/raw/strategy_001j_u1 `
  --end <FROZEN_DIAGNOSTIC_END>
```

The similarity report is descriptive only. It cannot change U1 after seeing Strategy 001J outcomes.

## Step 6 — Frozen 001D transfer baseline

Only after all data gates pass:

```powershell
python scripts/run_strategy_001j_baseline.py
```

This baseline uses the exact frozen 001D parameters and is recorded before the 162-configuration development grid.

## PIT Nifty 100 remains deferred

The original Nifty 100 acquisition path is not deleted. If historical constituent data becomes available later, it should be loaded as a separate clean-universe experiment under Strategy 001, with its own data provenance. The tactical Kite-native result must not be rewritten as PIT evidence.

## Stop conditions

Do not fabricate historical membership, use Strategy 001J returns to construct U1, or silently substitute current constituents for historical index membership. If the Kite data itself lacks sufficient coverage or instrument mapping for the frozen research window, stop and record the failure rather than weakening the methodology.
