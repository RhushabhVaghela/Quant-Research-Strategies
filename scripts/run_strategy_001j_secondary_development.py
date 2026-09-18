"""Run the preregistered secondary 001J cost-efficiency development experiment.

This is an exploratory second-stage development search motivated by the first
development run's small per-trade expectancy relative to costs. It is
deliberately incapable of reading the chronological holdout.
"""

from __future__ import annotations

import argparse
from datetime import timedelta
from pathlib import Path

import numpy as np
import pandas as pd

from src.research.strategy_001j_cross_sectional import Strategy001JConfig, run_universe
from scripts.run_strategy_001j_baseline import (
    apply_point_in_time_membership,
    load_membership,
    load_symbol_csv,
)

DEVELOPMENT_START = "2026-06-10"
DEVELOPMENT_END = "2026-08-19"
COST_BPS = (0, 5, 10, 15, 20)
GRID = {
    "lookback_bars": (20, 30, 40),
    "z_threshold": (2.5, 3.0, 3.5),
    "trend_bars": (3, 6, 9),
    "holding_bars": (3, 6),
    "cooldown_bars": (12, 24),
}


def _window_timestamp(value: str, end_of_day: bool = False) -> pd.Timestamp:
    ts = pd.Timestamp(value).tz_localize("Asia/Kolkata")
    if end_of_day:
        ts += timedelta(days=1)
    return ts


def _configs() -> list[Strategy001JConfig]:
    configs: list[Strategy001JConfig] = []
    for lookback in GRID["lookback_bars"]:
        for z in GRID["z_threshold"]:
            for trend in GRID["trend_bars"]:
                for holding in GRID["holding_bars"]:
                    for cooldown in GRID["cooldown_bars"]:
                        configs.append(
                            Strategy001JConfig(lookback, z, trend, holding, cooldown)
                        )
    assert len(configs) == 108
    return configs


def _load_frames(membership_path: Path, input_dir: Path) -> dict[str, pd.DataFrame]:
    membership = load_membership(membership_path)
    start = _window_timestamp(DEVELOPMENT_START)
    end = _window_timestamp(DEVELOPMENT_END, end_of_day=True)
    frames: dict[str, pd.DataFrame] = {}
    for symbol in sorted(membership["symbol"].unique()):
        path = input_dir / f"{symbol}.csv"
        if not path.exists():
            raise SystemExit(f"Missing U1 data for {symbol}: {path}")
        raw = load_symbol_csv(path, None, start, end)
        frames[symbol] = apply_point_in_time_membership(symbol, raw, membership)
    return frames


def _metrics(trades: pd.DataFrame) -> dict[str, float | int]:
    if trades.empty:
        return {
            "trades": 0,
            "symbols": 0,
            "mean_gross": np.nan,
            "median_gross": np.nan,
            "win_rate": np.nan,
            "profit_factor": np.nan,
            "max_loss": np.nan,
            "max_gain": np.nan,
            "max_concurrent_entries": 0,
        }

    r = trades["gross_return"].astype(float)
    wins = r[r > 0].sum()
    losses = -r[r < 0].sum()
    return {
        "trades": int(len(r)),
        "symbols": int(trades["symbol"].nunique()),
        "mean_gross": float(r.mean()),
        "median_gross": float(r.median()),
        "win_rate": float((r > 0).mean()),
        "profit_factor": float(wins / losses) if losses > 0 else np.inf,
        "max_loss": float(r.min()),
        "max_gain": float(r.max()),
        "max_concurrent_entries": int(
            trades.groupby("signal_timestamp").size().max()
        ),
    }


def _cost_metrics(trades: pd.DataFrame) -> dict[str, float]:
    r = trades["gross_return"].astype(float)
    out: dict[str, float] = {}
    for bps in COST_BPS:
        net = r - (bps / 10_000.0)
        out[f"mean_net_{bps}bps"] = float(net.mean())
    return out


def _period_metrics(trades: pd.DataFrame) -> dict[str, float | int]:
    ts = pd.to_datetime(trades["signal_timestamp"], utc=True).dt.tz_convert("Asia/Kolkata")
    periods = {
        "early": ("2026-06-10", "2026-07-07"),
        "middle": ("2026-07-07", "2026-08-01"),
        "late": ("2026-08-01", "2026-08-20"),
    }
    out: dict[str, float | int] = {}
    for name, (start, end) in periods.items():
        mask = (ts >= pd.Timestamp(start, tz="Asia/Kolkata")) & (
            ts < pd.Timestamp(end, tz="Asia/Kolkata")
        )
        r = trades.loc[mask, "gross_return"].astype(float)
        out[f"{name}_trades"] = int(len(r))
        out[f"{name}_mean_gross"] = float(r.mean()) if len(r) else np.nan
        out[f"{name}_win_rate"] = float((r > 0).mean()) if len(r) else np.nan
    return out


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--membership", default="data/universe/strategy_001j_u1_membership.csv")
    parser.add_argument("--input-dir", default="data/raw/strategy_001j_u1")
    parser.add_argument(
        "--output-dir",
        default="data/reports/strategy_001j_secondary_development",
    )
    args = parser.parse_args()

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    frames = _load_frames(Path(args.membership), Path(args.input_dir))

    rows: list[dict] = []
    all_trades: list[pd.DataFrame] = []
    for config_id, config in enumerate(_configs(), start=1):
        trades = run_universe(frames, config=config)
        row = {
            "config_id": config_id,
            "lookback_bars": config.lookback_bars,
            "z_threshold": config.z_threshold,
            "trend_bars": config.trend_bars,
            "holding_bars": config.holding_bars,
            "cooldown_bars": config.cooldown_bars,
        }
        row.update(_metrics(trades))
        row.update(_cost_metrics(trades))
        row.update(_period_metrics(trades))
        rows.append(row)
        if not trades.empty:
            t = trades.copy()
            t["config_id"] = config_id
            all_trades.append(t)

    grid = pd.DataFrame(rows)
    grid.to_csv(output_dir / "secondary_development_grid.csv", index=False)
    if all_trades:
        pd.concat(all_trades, ignore_index=True).to_csv(
            output_dir / "secondary_development_trades.csv", index=False
        )
    else:
        pd.DataFrame().to_csv(
            output_dir / "secondary_development_trades.csv", index=False
        )

    pd.DataFrame(
        [
            {
                "phase": "secondary_development",
                "start": DEVELOPMENT_START,
                "end": DEVELOPMENT_END,
                "configurations": len(rows),
                "universe_symbols": len(frames),
                "cost_grid_bps": ",".join(map(str, COST_BPS)),
                "selection_rule": "manual review only; no automatic candidate selection",
                "holdout_access": "none",
                "sequential_development_warning": "same development sample was used after first development review",
            }
        ]
    ).to_csv(output_dir / "run_metadata.csv", index=False)

    print(
        f"001J secondary development complete: {len(rows)} configurations, "
        f"development only ({DEVELOPMENT_START} through {DEVELOPMENT_END})."
    )
    print(f"Results: {output_dir / 'secondary_development_grid.csv'}")
    print("No holdout data was loaded.")


if __name__ == "__main__":
    main()
