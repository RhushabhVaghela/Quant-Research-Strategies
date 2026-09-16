"""Run Strategy 001G point-in-time feature and forward-path replay."""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd

from src.research.strategy_001g_replay import (
    load_ohlcv,
    run_replay,
    summarize_forward_path,
)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("data_csv", type=Path)
    parser.add_argument(
        "reference_trades_csv",
        type=Path,
        nargs="?",
        default=Path("data/reports/goldbees_strategy_001d_backtest/trades_gross.csv"),
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("data/reports/goldbees_strategy_001g_replay"),
    )
    args = parser.parse_args()

    data = load_ohlcv(args.data_csv)
    reference = pd.read_csv(args.reference_trades_csv)
    results = run_replay(data, reference)
    args.output_dir.mkdir(parents=True, exist_ok=True)

    results["trades"].to_csv(args.output_dir / "replayed_trades.csv", index=False)
    results["forward_path"].to_csv(args.output_dir / "forward_path.csv", index=False)
    summarize_forward_path(results["forward_path"]).to_csv(
        args.output_dir / "forward_path_summary.csv", index=False
    )
    results["excursions"].to_csv(args.output_dir / "mfe_mae.csv", index=False)
    results["reconciliation"].to_csv(args.output_dir / "reconciliation.csv", index=False)

    recon = results["reconciliation"]
    matches = int(recon["match"].fillna(False).sum())
    total_ref = len(reference)
    total_replay = len(results["trades"])
    discrepancies = len(recon) - matches
    print(f"Replayed frozen 001D trades: {total_replay}")
    print(f"Reference 001D trades: {total_ref}")
    print(f"Exact reconciliations within tolerance: {matches}")
    print(f"Reconciliation discrepancies: {discrepancies}")
    print(f"Wrote Strategy 001G outputs to {args.output_dir}")


if __name__ == "__main__":
    main()
