"""Resolve the predefined research candidates against the cached NSE instrument master."""

from __future__ import annotations

import argparse
from pathlib import Path
import sys

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.data.instruments import load_instruments, resolve_instrument


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--candidates",
        type=Path,
        default=ROOT / "research" / "universe_candidates.csv",
    )
    parser.add_argument(
        "--instruments",
        type=Path,
        default=ROOT / "data" / "raw" / "instruments_nse.csv",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=ROOT / "data" / "reports" / "research_universe.csv",
    )
    parser.add_argument("--capital", type=float, default=30_000.0)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    candidates = pd.read_csv(args.candidates)
    instruments = load_instruments(args.instruments)

    rows: list[dict] = []
    for candidate in candidates.to_dict("records"):
        symbol = str(candidate["symbol"]).upper()
        try:
            instrument = resolve_instrument(instruments, "NSE", symbol)
        except (KeyError, ValueError) as exc:
            rows.append(
                {
                    **candidate,
                    "exchange": "NSE",
                    "instrument_token": None,
                    "instrument_type": None,
                    "segment": None,
                    "last_price": None,
                    "capital_for_one_unit": None,
                    "units_at_capital": None,
                    "resolution_status": f"FAILED: {exc}",
                }
            )
            continue

        price = float(instrument["last_price"])
        units = int(args.capital // price) if price > 0 else 0
        rows.append(
            {
                **candidate,
                "exchange": instrument["exchange"],
                "instrument_token": int(instrument["instrument_token"]),
                "instrument_type": instrument["instrument_type"],
                "segment": instrument["segment"],
                "last_price": price,
                "capital_for_one_unit": price,
                "units_at_capital": units,
                "resolution_status": "RESOLVED",
            }
        )

    report = pd.DataFrame(rows)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    report.to_csv(args.output, index=False)

    display_columns = [
        "symbol",
        "category",
        "instrument_token",
        "instrument_type",
        "segment",
        "last_price",
        "units_at_capital",
        "resolution_status",
    ]
    print(report[display_columns].to_string(index=False))
    print(f"\nSaved research-universe resolution to {args.output}")


if __name__ == "__main__":
    main()
