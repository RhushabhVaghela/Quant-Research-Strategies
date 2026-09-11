# Phase 1 Data Layer

## Install
```bash
pip install -r requirements.txt
```

Copy `.env.example` to `.env` and fill in your own Kite credentials.
Never commit `.env`.

## First download
```bash
python scripts/download_historical.py --symbol NIFTYBEES --start 2026-08-01 --end 2026-08-31
```

The script downloads the current NSE instrument master, resolves the symbol,
retrieves 5-minute candles in chunks, normalizes timestamps to Asia/Kolkata,
deduplicates, validates OHLCV, and saves local CSV data.

## Tests
```bash
pytest
```

Kite candle timestamps represent the start of the candle; the pipeline preserves
that convention. Do not treat an in-progress live candle as final.

This phase does not place orders, generate signals, backtest, train ML models,
or claim profitability.
