"""Run the pre-registered Strategy 001J parameter grid on development data only.

This script intentionally does not choose a winner. It writes one row per
configuration so selection can be reviewed as a research artifact.
"""

from __future__ import annotations

import argparse
import itertools
from pathlib import Path

import pandas as pd

from src.research.strategy_001j_cross_sectional import Strategy001JConfig, run_universe

LOOKBACKS = (20, 30, 40)
Z_THRESHOLDS = (1.5, 2.0, 2.5)
TREND_BARS = (3, 6, 9)
HOLDING_BARS = (3, 6, 9)
COOLDOWN_BARS = (6, 12)


def load_symbol_csv(path: Path, source_timezone: str | None) -> pd.DataFrame:
    frame = pd.read_csv(path)
    required = {"timestamp", "open", "high", "low", "close", "volume"}
    missing = required - set(frame.columns)
    if missing:
        raise ValueError(f"{path}: missing columns {sorted(missing)}")
    ts = pd.to_datetime(frame["timestamp"], errors="raise")
    if ts.dt.tz is None:
        if not source_timezone:
            raise ValueError(f"{path}: naive timestamps require --source-timezone")
        ts = ts.dt.tz_localize(source_timezone)
    frame["timestamp"] = ts.dt.tz_convert("Asia/Kolkata")
    return frame.set_index("timestamp").sort_index()


def summarize(trades: pd.DataFrame, config: Strategy001JConfig) -> dict:
    returns = trades["gross_return"].astype(float) if not trades.empty else pd.Series(dtype=float)
    positive = returns[returns > 0].sum()
    negative = -returns[returns < 0].sum()
    return {
        "lookback_bars": config.lookback_bars,
        "z_threshold": config.z_threshold,
        "trend_bars": config.trend_bars,
        "holding_bars": config.holding_bars,
        "cooldown_bars": config.cooldown_bars,
        "trades": int(len(trades)),
        "symbols": int(trades["symbol"].nunique()) if not trades.empty else 0,
        "mean_gross_return": float(returns.mean()) if not trades.empty else float("nan"),
        "median_gross_return": float(returns.median()) if not trades.empty else float("nan"),
        "win_rate": float((returns > 0).mean()) if not trades.empty else float("nan"),
        "profit_factor": float(positive / negative) if negative > 0 else float("inf"),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input-dir", default="data/raw/strategy_001j_u1")
    parser.add_argument("--output", default="data/reports/strategy_001j_parameter_grid.csv")
    parser.add_argument("--source-timezone", default=None)
    args = parser.parse_args()

    frames = {
        path.stem.upper(): load_symbol_csv(path, args.source_timezone)
        for path in sorted(Path(args.input_dir).glob("*.csv"))
    }
    if not frames:
        raise SystemExit(f"No CSV files found in {args.input_dir}")

    rows = []
    for values in itertools.product(
        LOOKBACKS, Z_THRESHOLDS, TREND_BARS, HOLDING_BARS, COOLDOWN_BARS
    ):
        config = Strategy001JConfig(*values)
        trades = run_universe(frames, config=config)
        rows.append(summarize(trades, config))

    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(rows).to_csv(output, index=False)
    print(f"Wrote {len(rows)} configurations to {output}")


if __name__ == "__main__":
    main()
