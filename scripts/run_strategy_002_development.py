"""Run the preregistered Strategy 002 development grid.

Only the fixed development window is loaded. Formation pairs and hedge betas
are read from the formation output and are never re-selected here.
"""

from __future__ import annotations

import argparse
from datetime import timedelta
from pathlib import Path
from itertools import product

import numpy as np
import pandas as pd

from scripts.run_strategy_001j_baseline import (
    apply_point_in_time_membership,
    load_membership,
    load_symbol_csv,
)
from src.research.strategy_002_pairs import Strategy002Config, run_pairs

DEV_START = "2026-06-10"
DEV_END = "2026-08-19"
DEV_END_EXCLUSIVE = "2026-08-20"
LOOKBACKS = (60, 120, 240)
ENTRY_ZS = (2.0, 2.5, 3.0)
EXIT_ZS = (0.5, 1.0)
HOLDINGS = (3, 6, 12)
COOLDOWNS = (6, 12)
COST_BPS = (0, 5, 10, 15, 20)
PAIR_COST_LEG_MULTIPLIER = 2


def _window(value: str) -> pd.Timestamp:
    ts = pd.Timestamp(value).tz_localize("Asia/Kolkata")
    return ts


def _load_frames(membership_path: Path, input_dir: Path, pairs_path: Path) -> dict[str, pd.DataFrame]:
    membership = load_membership(membership_path)
    start = _window(DEV_START)
    end = _window(DEV_END_EXCLUSIVE)
    symbols = set(pd.read_csv(pairs_path)[["symbol_a", "symbol_b"]].to_numpy().ravel())
    frames = {}
    for symbol in sorted(symbols):
        raw = load_symbol_csv(input_dir / f"{symbol}.csv", None, start, end)
        frames[symbol] = apply_point_in_time_membership(symbol, raw, membership)
    return frames


def _metrics(trades: pd.DataFrame) -> dict:
    if trades.empty:
        return {"trades": 0, "pairs": 0, "symbols": 0, "mean_gross": np.nan,
                "median_gross": np.nan, "win_rate": np.nan, "profit_factor": np.nan}
    r = trades["gross_return"].astype(float)
    wins = r[r > 0].sum()
    losses = -r[r < 0].sum()
    return {
        "trades": int(len(trades)),
        "pairs": int(trades["pair_id"].nunique()),
        "symbols": int(set(trades["symbol_a"]).union(trades["symbol_b"]).__len__()),
        "mean_gross": float(r.mean()),
        "median_gross": float(r.median()),
        "win_rate": float((r > 0).mean()),
        "profit_factor": float(wins / losses) if losses > 0 else np.inf,
        "max_loss": float(r.min()),
        "max_gain": float(r.max()),
        "max_concurrent": int(trades.groupby("signal_timestamp").size().max()),
    }


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--membership", default="data/universe/strategy_001j_u1_membership.csv")
    p.add_argument("--input-dir", default="data/raw/strategy_001j_u1")
    p.add_argument("--pairs", default="data/universe/strategy_002_pairs/formation_pairs.csv")
    p.add_argument("--output-dir", default="data/reports/strategy_002_development")
    args = p.parse_args()

    pairs = pd.read_csv(args.pairs)
    if pairs.empty:
        raise SystemExit("Formation pair file is empty; do not run development.")
    frames = _load_frames(Path(args.membership), Path(args.input_dir), Path(args.pairs))
    output = Path(args.output_dir)
    output.mkdir(parents=True, exist_ok=True)

    # COST_BPS is defined as round-trip cost per leg. A two-leg equal-dollar\n    # pair therefore receives a 2x haircut at each cost scenario.\n    configs = list(product(LOOKBACKS, ENTRY_ZS, EXIT_ZS, HOLDINGS, COOLDOWNS))
    assert len(configs) == 108

    rows, trade_tables = [], []
    for i, (lb, ez, xz, hold, cooldown) in enumerate(configs, 1):
        cfg = Strategy002Config(lb, ez, xz, hold, cooldown, 4.0)
        trades = run_pairs(pairs, frames, cfg)
        m = _metrics(trades)
        m.update({"config_id": i, "lookback_bars": lb, "entry_z": ez,
                  "exit_z": xz, "max_holding_bars": hold, "cooldown_bars": cooldown})
        for bps in COST_BPS:
            m[f"mean_after_{bps}bps_per_leg_roundtrip"] = m["mean_gross"] - (PAIR_COST_LEG_MULTIPLIER * bps) / 10000 if np.isfinite(m["mean_gross"]) else np.nan
        rows.append(m)
        if not trades.empty:
            t = trades.copy()
            t["config_id"] = i
            trade_tables.append(t)

    pd.DataFrame(rows).to_csv(output / "development_grid.csv", index=False)
    if trade_tables:
        pd.concat(trade_tables, ignore_index=True).to_csv(output / "development_trades.csv", index=False)
    else:
        pd.DataFrame().to_csv(output / "development_trades.csv", index=False)
    pd.DataFrame([{
        "development_start": DEV_START,
        "development_end": DEV_END,
        "configurations": len(configs),
        "pairs_frozen": len(pairs),
        "holdout_start": "2026-08-20",
        "holdout_end": "2026-09-17",
        "holdout_access": "none",
        "pair_selection_access": "formation only",
    }]).to_csv(output / "run_metadata.csv", index=False)
    print("Strategy 002 development grid complete.")
    print(f"Configurations: {len(configs)}; frozen pairs: {len(pairs)}")
    print("No holdout data was loaded.")


if __name__ == "__main__":
    main()
