"""Fetch Strategy 001J 5-minute NSE equity data through the existing Kite client.

This script uses the repository's existing Zerodha authentication layer. It never
stores credentials. The current Kite instrument dump is used only to map live NSE
EQ instruments to instrument tokens; historical candles are fetched with Kite's
historical-data API and saved locally for research.

Use a symbols file for the pre-selected universe. Without one, --all-nse-eq
fetches every currently tradable NSE EQ instrument and is intentionally expensive.

For repairing an existing dataset, use --merge. This fetches only the requested
range and merges it with the existing CSV instead of replacing the full history.
"""

from __future__ import annotations

import argparse
import json
from datetime import date
from pathlib import Path

import pandas as pd

from src.data.historical import fetch_historical, save_candles
from src.data.kite_client import KiteClient


def _load_symbols(path: Path) -> list[str]:
    frame = pd.read_csv(path)
    column = "symbol" if "symbol" in frame.columns else frame.columns[0]
    return sorted({str(x).strip().upper() for x in frame[column].dropna() if str(x).strip()})


def _nse_equity_instruments(kite: KiteClient) -> dict[str, dict]:
    rows = kite.instruments("NSE")
    return {
        str(row["tradingsymbol"]).upper(): row
        for row in rows
        if row.get("instrument_type") == "EQ" and row.get("segment") == "NSE"
    }


def _merge_with_existing(output: Path, fetched: pd.DataFrame) -> pd.DataFrame:
    """Merge fetched candles into an existing CSV without losing history."""
    incoming = fetched.reset_index()[["timestamp", "open", "high", "low", "close", "volume"]]
    incoming["timestamp"] = pd.to_datetime(incoming["timestamp"], errors="raise")

    if output.exists():
        existing = pd.read_csv(output)
        required = {"timestamp", "open", "high", "low", "close", "volume"}
        missing = required - set(existing.columns)
        if missing:
            raise ValueError(f"{output}: existing file missing columns {sorted(missing)}")
        existing = existing[["timestamp", "open", "high", "low", "close", "volume"]].copy()
        existing["timestamp"] = pd.to_datetime(existing["timestamp"], errors="raise")
        merged = pd.concat([existing, incoming], ignore_index=True)
    else:
        merged = incoming

    merged = merged.sort_values("timestamp").drop_duplicates("timestamp", keep="last").reset_index(drop=True)
    return merged


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--start", required=True, help="YYYY-MM-DD")
    parser.add_argument("--end", required=True, help="YYYY-MM-DD")
    parser.add_argument("--symbols-file", type=Path, default=None)
    parser.add_argument("--all-nse-eq", action="store_true")
    parser.add_argument("--output-dir", type=Path, default=Path("data/raw/strategy_001j_u1"))
    parser.add_argument("--chunk-days", type=int, default=80)
    parser.add_argument("--pause-seconds", type=float, default=0.35)
    parser.add_argument("--max-symbols", type=int, default=None)
    parser.add_argument("--overwrite", action="store_true", help="Replace existing symbol files with the fetched range")
    parser.add_argument("--merge", action="store_true", help="Merge the fetched range into existing symbol files")
    parser.add_argument("--manifest", type=Path, default=Path("data/reports/strategy_001j_kite_download_manifest.csv"))
    args = parser.parse_args()

    if args.overwrite and args.merge:
        raise SystemExit("Use at most one of --overwrite or --merge")

    start = date.fromisoformat(args.start)
    end = date.fromisoformat(args.end)
    if start > end:
        raise SystemExit("--start must be <= --end")
    if bool(args.symbols_file) == bool(args.all_nse_eq):
        raise SystemExit("Provide exactly one of --symbols-file or --all-nse-eq")

    client = KiteClient()
    instruments = _nse_equity_instruments(client)
    symbols = list(instruments)
    if args.symbols_file:
        symbols = _load_symbols(args.symbols_file)
    symbols = sorted(symbols)
    if args.max_symbols is not None:
        symbols = symbols[: args.max_symbols]

    args.output_dir.mkdir(parents=True, exist_ok=True)
    manifest: list[dict] = []
    for i, symbol in enumerate(symbols, start=1):
        row = instruments.get(symbol)
        if row is None:
            manifest.append({"symbol": symbol, "status": "missing_current_kite_instrument"})
            continue
        output = args.output_dir / f"{symbol}.csv"
        if output.exists() and not args.overwrite and not args.merge:
            manifest.append({"symbol": symbol, "status": "exists_skipped", "path": str(output)})
            continue
        try:
            frame = fetch_historical(
                client,
                int(row["instrument_token"]),
                start,
                end,
                interval="5minute",
                chunk_days=args.chunk_days,
                pause_seconds=args.pause_seconds,
            )
            if frame.empty:
                manifest.append({"symbol": symbol, "status": "empty", "rows": 0})
                continue

            if args.merge:
                out = _merge_with_existing(output, frame)
            else:
                out = frame.reset_index()[["timestamp", "open", "high", "low", "close", "volume"]]

            save_candles(out.set_index("timestamp"), output)
            manifest.append({
                "symbol": symbol,
                "status": "merged" if args.merge else "downloaded",
                "rows": len(out),
                "first_timestamp": str(out["timestamp"].min()),
                "last_timestamp": str(out["timestamp"].max()),
                "instrument_token": int(row["instrument_token"]),
                "path": str(output),
            })
            action = "merged" if args.merge else "downloaded"
            print(f"[{i}/{len(symbols)}] {symbol}: {action}, {len(out)} rows")
        except Exception as exc:
            manifest.append({"symbol": symbol, "status": f"error: {exc}"})
            print(f"[{i}/{len(symbols)}] {symbol}: ERROR: {exc}")

    manifest_path = args.manifest
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(manifest).to_csv(manifest_path, index=False)
    metadata = manifest_path.with_suffix(".json")
    metadata.write_text(json.dumps({
        "source": "Zerodha Kite Connect historical_data API",
        "exchange": "NSE",
        "instrument_type": "EQ",
        "interval": "5minute",
        "requested_start": args.start,
        "requested_end": args.end,
        "symbol_count_requested": len(symbols),
        "mode": "merge" if args.merge else "overwrite" if args.overwrite else "skip-existing",
        "note": "Current Kite instrument dump is used for token mapping. It does not provide historical index membership.",
    }, indent=2), encoding="utf-8")
    print(f"Wrote download manifest: {manifest_path}")


if __name__ == "__main__":
    main()
