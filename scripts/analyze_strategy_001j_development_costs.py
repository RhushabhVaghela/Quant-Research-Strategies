"""Apply a preregistered round-trip cost sensitivity to 001J development trades.

Costs are expressed in basis points per completed round trip. This is a
sensitivity analysis, not a broker fee quote and not a candidate selector.
No holdout data is read.
"""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd

COST_BPS = (0, 5, 10, 15, 20, 25, 30)
DEVELOPMENT_START = pd.Timestamp("2026-06-10", tz="Asia/Kolkata")
DEVELOPMENT_END_EXCLUSIVE = pd.Timestamp("2026-08-20", tz="Asia/Kolkata")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--trades", default="data/reports/strategy_001j_development_grid/development_trades.csv")
    parser.add_argument("--output-dir", default="data/reports/strategy_001j_development_stability")
    args = parser.parse_args()

    trades = pd.read_csv(args.trades)
    required = {"config_id", "gross_return", "signal_timestamp"}
    missing = required - set(trades.columns)
    if missing:
        raise ValueError(f"development_trades.csv missing columns: {sorted(missing)}")
    trades["signal_timestamp"] = pd.to_datetime(trades["signal_timestamp"], utc=True).dt.tz_convert("Asia/Kolkata")
    trades["gross_return"] = pd.to_numeric(trades["gross_return"], errors="raise")
    if trades["signal_timestamp"].min() < DEVELOPMENT_START or trades["signal_timestamp"].max() >= DEVELOPMENT_END_EXCLUSIVE:
        raise ValueError("Development trade ledger contains timestamps outside the frozen development window.")

    rows: list[dict] = []
    for config_id, g in trades.groupby("config_id"):
        gross = g["gross_return"]
        for cost_bps in COST_BPS:
            cost = cost_bps / 10_000.0
            net = gross - cost
            wins = net[net > 0].sum()
            losses = -net[net < 0].sum()
            rows.append({
                "config_id": int(config_id),
                "round_trip_cost_bps": cost_bps,
                "trades": int(len(net)),
                "mean_net_return": float(net.mean()),
                "median_net_return": float(net.median()),
                "win_rate": float((net > 0).mean()),
                "profit_factor": float(wins / losses) if losses > 0 else float("inf"),
                "net_return_sum": float(net.sum()),
                "profitable_after_cost": bool(net.mean() > 0 and wins > losses),
            })

    out = Path(args.output_dir)
    out.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(rows).to_csv(out / "development_cost_sensitivity.csv", index=False)
    pd.DataFrame([{
        "cost_grid_bps": ",".join(map(str, COST_BPS)),
        "interpretation": "round-trip gross-return haircut; excludes symbol-specific fees, taxes, spread and market impact",
        "candidate_selection": "diagnostic only; no automatic selection",
        "holdout_access": "none",
    }]).to_csv(out / "cost_analysis_metadata.csv", index=False)
    print("001J development cost sensitivity complete. No holdout data was loaded.")


if __name__ == "__main__":
    main()
