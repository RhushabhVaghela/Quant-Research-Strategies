# Strategy 001I — Operational Runbook

## Purpose

This runbook explains how to collect the first genuinely prospective Strategy 001 observations. It is intentionally operational rather than analytical: do not change the frozen strategy while this cohort is running.

## Before the first prospective session

1. Sync the repository.
2. Run the full test suite and require a clean pass.
3. Confirm the local `.env` contains the existing Zerodha credentials without exposing them.
4. Confirm the Zerodha access token is valid.
5. Confirm `NSE:GOLDBEES` resolves from the current instrument master.
6. Start the collector **before 09:15 IST** on the chosen prospective session.
7. Do not open or backfill later historical candles for the same session in order to create missing prospective signals.

## Test gate

```powershell
pytest -q
```

The expected count should include the 001I tests added after the 001H gate. Do not rely on a remembered test count; use the local pytest output as the source of truth.

## Start paper/shadow collection

```powershell
python scripts/run_strategy_001i_paper_shadow.py
```

The collector:

- authenticates through the existing `KiteClient`;
- resolves GOLDBEES from the live NSE instrument master;
- uses pre-activation historical candles only as a warm-up;
- subscribes to live GOLDBEES ticks in KiteTicker full mode;
- builds completed 5-minute bars from exchange-timestamped ticks;
- evaluates the frozen 001D rule at the completed event-bar boundary;
- writes signal records before the fixed exit outcome is known;
- finalizes paper outcomes only after the frozen exit candle has completed;
- never calls an order-placement endpoint.

Zerodha documents WebSocket full mode as the stream that includes market depth; the live packet includes an exchange timestamp and depth information. Historical candle timestamps represent the start of the candle, so the runbook treats the 5-minute timestamp as candle start and waits for the candle to complete before evaluating the signal. citeturn2search0turn1search1

## Local output

```text
data/prospective/strategy_001i/
├── run_manifest.json
├── bars.csv
├── signals.csv
└── outcomes.csv
```

These files are ignored by Git. Do not commit them unless a later research artifact explicitly requires a sanitized sample.

## After the market session

Check:

```powershell
Get-Content data/prospective/strategy_001i/run_manifest.json
Get-Content data/prospective/strategy_001i/signals.csv
Get-Content data/prospective/strategy_001i/outcomes.csv
```

Also check the console output for:

- `DATA_MISSING`;
- `OPERATIONAL_ERROR`;
- unexpected disconnects;
- signal count;
- outcome count.

Do not manually repair a missing prospective observation from historical data. Record the exception and preserve the original ledger.

## What not to do

- Do not run the historical 001H script on the prospective session and call it OOS.
- Do not add a time-of-day filter.
- Do not change z-score, lookback, holding period, or cooldown.
- Do not add stops or profit targets.
- Do not use observed MFE/MAE to alter exits.
- Do not place live orders from the paper-shadow collector.
- Do not delete losing trades or duplicate signals.

## Review workflow

At 20, 50, and 100 completed trades, pause for the predefined review only. The checkpoint is for data integrity and distribution/execution diagnostics, not for parameter tuning.

The results are entered into:

`research/journal/001I_prospective_oos_paper_shadow_results.md`

No Strategy 002 work begins until Strategy 001 receives a final research-gate decision.
