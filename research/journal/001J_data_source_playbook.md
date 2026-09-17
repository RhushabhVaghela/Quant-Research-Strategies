# Strategy 001J — Data Source Playbook

**Status:** Active broker-native acquisition path; PIT Nifty 100 deferred.

## 1. Primary tactical source — Zerodha Kite Connect

The active September 2026 path uses the project's existing Zerodha Kite Connect authentication/client layer.

Relevant repository components:

- `src/data/kite_auth.py`
- `src/data/kite_client.py`
- `src/data/historical.py`
- `scripts/fetch_strategy_001j_kite_data.py`
- `scripts/build_strategy_001j_broker_liquid_universe.py`

Kite's instrument dump supplies current tradable instruments and instrument tokens. The historical candle API supplies archived candles, including 5-minute OHLCV. Current instrument availability is not a historical membership database, so this tactical universe carries a documented survivorship/current-instrument limitation.

Official Kite references:

- https://kite.trade/docs/connect/v3/market-data-and-instruments/
- https://kite.trade/docs/connect/v3/historical/

## 2. Broker-native U1 formation

U1 is formed before any Strategy 001J performance is examined.

Fixed rule:

- universe source: current Kite NSE EQ instrument dump;
- formation data: 5-minute OHLCV;
- minimum formation days: 15;
- liquidity metric: daily `sum(close * volume)`;
- ranking statistic: median daily traded value across formation days;
- selected count: top 50;
- activation: immediately after formation window;
- no strategy P&L, holdout results, or similarity results used for selection.

This is outcome-independent but not PIT-clean.

## 3. Acquisition commands

Formation candidates:

```powershell
python scripts/fetch_strategy_001j_kite_data.py `
  --start <FORMATION_START> `
  --end <FORMATION_END> `
  --all-nse-eq `
  --output-dir data/raw/strategy_001j_candidates
```

Build U1:

```powershell
python scripts/build_strategy_001j_broker_liquid_universe.py `
  --input-dir data/raw/strategy_001j_candidates `
  --formation-start <FORMATION_START> `
  --formation-end <FORMATION_END> `
  --research-end <RESEARCH_END> `
  --top-n 50 `
  --min-days 15
```

Selected-symbol research data:

```powershell
python scripts/fetch_strategy_001j_kite_data.py `
  --start <FORMATION_START> `
  --end <RESEARCH_END> `
  --symbols-file data/universe/strategy_001j_u1_membership.csv `
  --output-dir data/raw/strategy_001j_u1
```

## 4. Data contract

Each raw file must contain:

```text
timestamp,open,high,low,close,volume
```

Normalize timestamps to `Asia/Kolkata`, reject duplicate timestamps, preserve chronological order, and retain the downloader manifest.

Do not commit `.env`, API keys, access tokens, or other credentials.

## 5. Validation sequence

```powershell
python scripts/validate_strategy_001j_u1_membership.py
python scripts/audit_strategy_001j_u1_data.py
python scripts/validate_strategy_001j_data_gate.py `
  --start <RESEARCH_START> `
  --end <RESEARCH_END>
```

Only after these pass should the similarity diagnostics and frozen 001D baseline run.

## 6. Similarity diagnostics

Run the locked GOLDBEES behavior comparison only after U1 and its research-window data are fixed. It remains descriptive and cannot modify U1 after seeing strategy outcomes.

## 7. Deferred PIT Nifty 100 route

The original PIT Nifty 100 research remains valid and should be resumed if historical constituent data becomes available with defensible provenance. It must be recorded separately rather than silently replacing the tactical Kite-native result.

## 8. No-data stop condition

Do not fabricate historical membership, infer historical index membership from today's list, or use strategy returns to manufacture a more attractive universe. If Kite lacks the required data for a symbol/window, record the failure and apply only the pre-registered data eligibility rules.
