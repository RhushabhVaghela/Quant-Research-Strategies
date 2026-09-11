from __future__ import annotations
import argparse
from datetime import date
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.data.historical import fetch_historical, save_candles
from src.data.instruments import download_instruments, load_instruments, resolve_instrument
from src.data.kite_client import KiteClient
from src.data.validation import assert_valid

def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument("--exchange", default="NSE")
    p.add_argument("--symbol", required=True)
    p.add_argument("--start", required=True, type=date.fromisoformat)
    p.add_argument("--end", required=True, type=date.fromisoformat)
    p.add_argument("--interval", default="5minute")
    p.add_argument("--chunk-days", type=int, default=30)
    return p.parse_args()

def main():
    args = parse_args()
    client = KiteClient()

    instrument_path = ROOT / "data" / "raw" / f"instruments_{args.exchange.lower()}.csv"
    download_instruments(client, instrument_path, args.exchange)
    instruments = load_instruments(instrument_path)
    instrument = resolve_instrument(instruments, args.exchange, args.symbol)

    print(f"Resolved {args.exchange}:{args.symbol} -> {instrument['instrument_token']}")

    candles = fetch_historical(
        client, int(instrument["instrument_token"]), args.start, args.end,
        args.interval, args.chunk_days
    )
    if candles.empty:
        raise RuntimeError("No historical candles returned.")

    report = assert_valid(candles)
    print(f"Validation passed: {report}")

    output = ROOT / "data" / "raw" / f"{args.exchange}_{args.symbol}_{args.interval}.csv"
    save_candles(candles, output)
    print(f"Saved {len(candles):,} rows to {output}")

if __name__ == "__main__":
    main()
