"""Fetch Strategy 001J 5-minute NSE equity data through the existing Kite client.

This script uses the repository's existing Zerodha authentication layer. It never
stores credentials. The current Kite instrument dump is used only to map live NSE
EQ instruments to instrument tokens; historical candles are fetched with Kite's
historical-data API and saved locally for research.

Use a symbols file for the pre-selected universe. Without one, --all-nse-eq
fetches every currently tradable NSE EQ instrument and is intentionally expensive.
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
    parser.add_argument("--overwrite", action="store_true")
    parser.add_argument("--manifest", type=Path, default=Path("data/reports/strategy_001j_kite_download_manifest.csv"))
    args = parser.parse_args()

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
        if output.exists() and not args.overwrite:
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
            out = frame.reset_index()[["timestamp", "open", "high", "low", "close", "volume"]]
            save_candles(out.set_index("timestamp"), output)
            manifest.append({
                "symbol": symbol,
                "status": "downloaded",
                "rows": len(out),
                "first_timestamp": str(out["timestamp"].min()),
                "last_timestamp": str(out["timestamp"].max()),
                "instrument_token": int(row["instrument_token"]),
                "path": str(output),
            })
            print(f"[{i}/{len(symbols)}] {symbol}: {len(out)} rows")
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
        "note": "Current Kite instrument dump is used for token mapping. It does not provide historical index membership.",
    }, indent=2), encoding="utf-8")
    print(f"Wrote download manifest: {manifest_path}")


if __name__ == "__main__":
    main()
