"""Run one frozen Strategy 001J candidate on the chronological holdout.

The holdout dates are immutable constants from the registered experiment
window. The candidate parameters must be supplied explicitly, so this script
cannot silently optimize or search the holdout.
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

HOLDOUT_START = "2026-08-20"
HOLDOUT_END = "2026-09-17"


def _window_timestamp(value: str, end_of_day: bool = False) -> pd.Timestamp:
    ts = pd.Timestamp(value).tz_localize("Asia/Kolkata")
    if end_of_day:
        ts += timedelta(days=1)
    return ts


def _load_frames(membership_path: Path, input_dir: Path) -> dict[str, pd.DataFrame]:
    membership = load_membership(membership_path)
    start = _window_timestamp(HOLDOUT_START)
    end = _window_timestamp(HOLDOUT_END, end_of_day=True)
    frames: dict[str, pd.DataFrame] = {}
    for symbol in sorted(membership["symbol"].unique()):
        path = input_dir / f"{symbol}.csv"
        if not path.exists():
            raise SystemExit(f"Missing U1 data for {symbol}: {path}")
        raw = load_symbol_csv(path, None, start, end)
        frames[symbol] = apply_point_in_time_membership(symbol, raw, membership)
    return frames


def _max_drawdown(returns: pd.Series) -> float:
    if returns.empty:
        return np.nan
    equity = (1.0 + returns).cumprod()
    return float((equity / equity.cummax() - 1.0).min())


def _summary(trades: pd.DataFrame) -> pd.DataFrame:
    if trades.empty:
        return pd.DataFrame([{
            "trades": 0, "symbols": 0, "mean_trade_return": np.nan,
            "median_trade_return": np.nan, "win_rate": np.nan,
            "profit_factor": np.nan, "trade_return_sum": 0.0,
            "max_trade_loss": np.nan, "max_trade_gain": np.nan,
            "max_daily_equal_weight_drawdown": np.nan,
            "max_concurrent_entries": 0,
        }])
    r = trades["gross_return"].astype(float)
    wins = r[r > 0].sum()
    losses = -r[r < 0].sum()
    daily = (
        trades.assign(session=pd.to_datetime(trades["exit_timestamp"]).dt.date)
        .groupby("session")["gross_return"]
        .mean()
    )
    return pd.DataFrame([{
        "trades": int(len(trades)),
        "symbols": int(trades["symbol"].nunique()),
        "mean_trade_return": float(r.mean()),
        "median_trade_return": float(r.median()),
        "win_rate": float((r > 0).mean()),
        "profit_factor": float(wins / losses) if losses > 0 else np.inf,
        "trade_return_sum": float(r.sum()),
        "max_trade_loss": float(r.min()),
        "max_trade_gain": float(r.max()),
        "max_daily_equal_weight_drawdown": _max_drawdown(daily),
        "max_concurrent_entries": int(trades.groupby("signal_timestamp").size().max()),
    }])


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--lookback", type=int, required=True)
    parser.add_argument("--z", type=float, required=True)
    parser.add_argument("--trend", type=int, required=True)
    parser.add_argument("--holding", type=int, required=True)
    parser.add_argument("--cooldown", type=int, required=True)
    parser.add_argument("--membership", default="data/universe/strategy_001j_u1_membership.csv")
    parser.add_argument("--input-dir", default="data/raw/strategy_001j_u1")
    parser.add_argument("--output-dir", default="data/reports/strategy_001j_holdout")
    args = parser.parse_args()

    config = Strategy001JConfig(
        lookback_bars=args.lookback,
        z_threshold=args.z,
        trend_bars=args.trend,
        holding_bars=args.holding,
        cooldown_bars=args.cooldown,
    )
    frames = _load_frames(Path(args.membership), Path(args.input_dir))
    trades = run_universe(frames, config=config)
    summary = _summary(trades)

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    trades.to_csv(output_dir / "holdout_trades.csv", index=False)
    summary.to_csv(output_dir / "holdout_summary.csv", index=False)
    pd.DataFrame([{
        "phase": "holdout",
        "start": HOLDOUT_START,
        "end": HOLDOUT_END,
        "lookback_bars": config.lookback_bars,
        "z_threshold": config.z_threshold,
        "trend_bars": config.trend_bars,
        "holding_bars": config.holding_bars,
        "cooldown_bars": config.cooldown_bars,
        "candidate_status": "parameters supplied externally and treated as frozen; no optimization performed",
    }]).to_csv(output_dir / "holdout_metadata.csv", index=False)

    print(f"001J holdout complete: frozen candidate evaluated on {HOLDOUT_START} through {HOLDOUT_END}.")
    print(summary.to_string(index=False))


if __name__ == "__main__":
    main()
