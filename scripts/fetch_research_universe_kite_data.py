"""Fetch a common 5-minute NSE EQ history for the predefined research universe.

This is a generic data-layer utility. It does not contain a trading hypothesis,
signal, optimization grid, or strategy-selection logic.

The current NSE instrument dump is used only for token mapping. Historical
candles come from the Kite historical-data API. Raw research data is written
locally and is expected to remain outside Git version control.
"""

from __future__ import annotations

import argparse
import json
from datetime import date
from pathlib import Path

import pandas as pd

from src.data.historical import fetch_historical, save_candles
from src.data.kite_client import KiteClient
from src.data.validation import assert_valid


ROOT = Path(__file__).resolve().parents[1]


def _load_symbols(path: Path) -> list[str]:
    frame = pd.read_csv(path)
    if "symbol" not in frame.columns:
        raise ValueError(f"{path}: expected a 'symbol' column")
    symbols = sorted(
        {
            str(value).strip().upper()
            for value in frame["symbol"].dropna()
            if str(value).strip()
        }
    )
    if not symbols:
        raise ValueError(f"{path}: no symbols found")
    return symbols


def _nse_equity_instruments(client: KiteClient) -> dict[str, dict]:
    rows = client.instruments("NSE")
    return {
        str(row["tradingsymbol"]).upper(): row
        for row in rows
        if row.get("instrument_type") == "EQ" and row.get("segment") == "NSE"
    }


def _output_path(output_dir: Path, symbol: str) -> Path:
    return output_dir / f"NSE_{symbol}_5minute.csv"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--start", required=True, help="YYYY-MM-DD")
    parser.add_argument("--end", required=True, help="YYYY-MM-DD")
    parser.add_argument(
        "--symbols-file",
        type=Path,
        default=ROOT / "research" / "universe_candidates.csv",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=ROOT / "data" / "raw" / "strategy_002_universe",
    )
    parser.add_argument("--chunk-days", type=int, default=30)
    parser.add_argument("--pause-seconds", type=float, default=0.35)
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Replace existing symbol files with the requested range.",
    )
    parser.add_argument(
        "--max-symbols",
        type=int,
        default=None,
        help="Optional deterministic cap for a smoke test.",
    )
    parser.add_argument(
        "--manifest",
        type=Path,
        default=ROOT / "data" / "reports" / "research_universe_kite_download_manifest.csv",
    )
    args = parser.parse_args()

    start = date.fromisoformat(args.start)
    end = date.fromisoformat(args.end)
    if start > end:
        raise SystemExit("--start must be <= --end")
    if args.chunk_days < 1:
        raise SystemExit("--chunk-days must be >= 1")
    if args.pause_seconds < 0:
        raise SystemExit("--pause-seconds must be >= 0")

    symbols = _load_symbols(args.symbols_file)
    if args.max_symbols is not None:
        if args.max_symbols < 1:
            raise SystemExit("--max-symbols must be >= 1")
        symbols = symbols[: args.max_symbols]

    client = KiteClient()
    instruments = _nse_equity_instruments(client)

    args.output_dir.mkdir(parents=True, exist_ok=True)
    manifest: list[dict] = []

    for index, symbol in enumerate(symbols, start=1):
        output = _output_path(args.output_dir, symbol)
        row = instruments.get(symbol)

        if row is None:
            manifest.append(
                {
                    "symbol": symbol,
                    "status": "missing_current_kite_instrument",
                    "path": str(output),
                }
            )
            print(f"[{index}/{len(symbols)}] {symbol}: missing current NSE EQ instrument")
            continue

        if output.exists() and not args.overwrite:
            manifest.append(
                {
                    "symbol": symbol,
                    "status": "exists_skipped",
                    "instrument_token": int(row["instrument_token"]),
                    "path": str(output),
                }
            )
            print(f"[{index}/{len(symbols)}] {symbol}: exists, skipped")
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
                manifest.append(
                    {
                        "symbol": symbol,
                        "status": "empty",
                        "rows": 0,
                        "instrument_token": int(row["instrument_token"]),
                        "path": str(output),
                    }
                )
                print(f"[{index}/{len(symbols)}] {symbol}: empty response")
                continue

            report = assert_valid(frame)
            save_candles(frame, output)

            manifest.append(
                {
                    "symbol": symbol,
                    "status": "downloaded",
                    "rows": len(frame),
                    "first_timestamp": str(frame.index.min()),
                    "last_timestamp": str(frame.index.max()),
                    "instrument_token": int(row["instrument_token"]),
                    "path": str(output),
                    "validation": str(report),
                }
            )
            print(
                f"[{index}/{len(symbols)}] {symbol}: "
                f"downloaded {len(frame):,} rows; validation passed"
            )
        except Exception as exc:
            manifest.append(
                {
                    "symbol": symbol,
                    "status": f"error: {exc}",
                    "instrument_token": int(row["instrument_token"]),
                    "path": str(output),
                }
            )
            print(f"[{index}/{len(symbols)}] {symbol}: ERROR: {exc}")

    manifest_path = args.manifest
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(manifest).to_csv(manifest_path, index=False)

    metadata_path = manifest_path.with_suffix(".json")
    metadata_path.write_text(
        json.dumps(
            {
                "source": "Zerodha Kite Connect historical_data API",
                "exchange": "NSE",
                "instrument_type": "EQ",
                "interval": "5minute",
                "requested_start": args.start,
                "requested_end": args.end,
                "symbol_count_requested": len(symbols),
                "chunk_days": args.chunk_days,
                "pause_seconds": args.pause_seconds,
                "overwrite": args.overwrite,
                "universe_manifest": str(args.symbols_file),
                "note": (
                    "Current Kite instrument mapping is used only for token "
                    "resolution. Historical index membership is not inferred."
                ),
            },
            indent=2,
        ),
        encoding="utf-8",
    )

    print(f"Wrote download manifest: {manifest_path}")
    print(f"Wrote download metadata: {metadata_path}")


if __name__ == "__main__":
    main()
