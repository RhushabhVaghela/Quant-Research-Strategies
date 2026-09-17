"""Evaluate the preregistered Strategy 001J parameter grid on development only.

This script is intentionally incapable of evaluating the chronological holdout:
the phase dates are frozen constants from the registered experiment window.
It produces one row per configuration plus the underlying trade ledger for
reproducibility. It does not select or freeze a production candidate.
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
GRID = {
    "lookback_bars": (20, 30, 40),
    "z_threshold": (1.5, 2.0, 2.5),
    "trend_bars": (3, 6, 9),
    "holding_bars": (3, 6, 9),
    "cooldown_bars": (6, 12),
}


def _window_timestamp(value: str, end_of_day: bool = False) -> pd.Timestamp:
    ts = pd.Timestamp(value).tz_localize("Asia/Kolkata")
    if end_of_day:
        ts += timedelta(days=1)
    return ts


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


def _max_drawdown_from_returns(returns: pd.Series) -> float:
    if returns.empty:
        return np.nan
    equity = (1.0 + returns).cumprod()
    drawdown = equity / equity.cummax() - 1.0
    return float(drawdown.min())


def _metrics(trades: pd.DataFrame) -> dict[str, float | int]:
    if trades.empty:
        return {
            "trades": 0, "symbols": 0, "mean_trade_return": np.nan,
            "median_trade_return": np.nan, "win_rate": np.nan,
            "profit_factor": np.nan, "trade_return_sum": 0.0,
            "max_trade_loss": np.nan, "max_trade_gain": np.nan,
            "max_daily_equal_weight_drawdown": np.nan,
            "max_concurrent_entries": 0,
        }

    r = trades["gross_return"].astype(float)
    wins = r[r > 0].sum()
    losses = -r[r < 0].sum()
    daily = (
        trades.assign(session=pd.to_datetime(trades["exit_timestamp"]).dt.date)
        .groupby("session")["gross_return"]
        .mean()
    )
    return {
        "trades": int(len(trades)),
        "symbols": int(trades["symbol"].nunique()),
        "mean_trade_return": float(r.mean()),
        "median_trade_return": float(r.median()),
        "win_rate": float((r > 0).mean()),
        "profit_factor": float(wins / losses) if losses > 0 else np.inf,
        "trade_return_sum": float(r.sum()),
        "max_trade_loss": float(r.min()),
        "max_trade_gain": float(r.max()),
        "max_daily_equal_weight_drawdown": _max_drawdown_from_returns(daily),
        "max_concurrent_entries": int(trades.groupby("signal_timestamp").size().max()),
    }


def _configs() -> list[Strategy001JConfig]:
    configs: list[Strategy001JConfig] = []
    for lookback in GRID["lookback_bars"]:
        for z in GRID["z_threshold"]:
            for trend in GRID["trend_bars"]:
                for holding in GRID["holding_bars"]:
                    for cooldown in GRID["cooldown_bars"]:
                        configs.append(Strategy001JConfig(lookback, z, trend, holding, cooldown))
    assert len(configs) == 162
    return configs


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--membership", default="data/universe/strategy_001j_u1_membership.csv")
    parser.add_argument("--input-dir", default="data/raw/strategy_001j_u1")
    parser.add_argument("--output-dir", default="data/reports/strategy_001j_development_grid")
    args = parser.parse_args()

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    frames = _load_frames(Path(args.membership), Path(args.input_dir))

    rows: list[dict] = []
    all_trades: list[pd.DataFrame] = []
    for config_id, config in enumerate(_configs(), start=1):
        trades = run_universe(frames, config=config)
        metrics = _metrics(trades)
        row = {
            "config_id": config_id,
            "lookback_bars": config.lookback_bars,
            "z_threshold": config.z_threshold,
            "trend_bars": config.trend_bars,
            "holding_bars": config.holding_bars,
            "cooldown_bars": config.cooldown_bars,
            **metrics,
        }
        rows.append(row)
        if not trades.empty:
            t = trades.copy()
            t["config_id"] = config_id
            all_trades.append(t)

    pd.DataFrame(rows).to_csv(output_dir / "development_grid.csv", index=False)
    if all_trades:
        pd.concat(all_trades, ignore_index=True).to_csv(output_dir / "development_trades.csv", index=False)
    else:
        pd.DataFrame().to_csv(output_dir / "development_trades.csv", index=False)

    metadata = pd.DataFrame([{
        "phase": "development",
        "start": DEVELOPMENT_START,
        "end": DEVELOPMENT_END,
        "configurations": len(rows),
        "universe_symbols": len(frames),
        "selection_rule": "No automatic candidate selection; review breadth, central tendency, tails, costs, concentration, and subperiod stability before freezing one configuration.",
        "holdout_access": "none",
    }])
    metadata.to_csv(output_dir / "run_metadata.csv", index=False)
    print(f"001J development grid complete: {len(rows)} configurations, development only ({DEVELOPMENT_START} through {DEVELOPMENT_END}).")
    print(f"Results: {output_dir / 'development_grid.csv'}")


if __name__ == "__main__":
    main()
