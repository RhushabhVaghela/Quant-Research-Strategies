"""Run the pre-registered Strategy 002 turnover-reduction development experiment.

Selection data only: 2025-09-18 through 2026-06-09.
Validation and final holdout are explicitly excluded.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd

DEVELOPMENT_START = pd.Timestamp("2025-09-18", tz="Asia/Kolkata")
VALIDATION_START = pd.Timestamp("2026-06-10", tz="Asia/Kolkata")
HOLDOUT_START = pd.Timestamp("2026-08-20", tz="Asia/Kolkata")
HOLDING_BARS = (2, 3, 6)
MIN_INSTRUMENTS = 4
COST_SCENARIOS_BPS = (0.0, 2.0, 5.0, 10.0)


def parse_args():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory", type=Path)
    parser.add_argument("--audit-report", type=Path, default=Path("data/reports/strategy_002_universe_audit.csv"))
    parser.add_argument("--output-dir", type=Path, default=Path("data/reports/strategy_002_turnover_reduction_development"))
    return parser.parse_args()


def load_development(path: Path) -> pd.DataFrame:
    df = pd.read_csv(path, parse_dates=["timestamp"])
    required = {"timestamp", "open", "close", "volume"}
    if not required.issubset(df.columns):
        raise ValueError(f"{path}: missing required columns")

    timestamps = pd.DatetimeIndex(df["timestamp"])
    if timestamps.tz is None:
        raise ValueError(f"{path}: timestamps must be timezone-aware")

    df["timestamp"] = timestamps.tz_convert("Asia/Kolkata")
    df = df.sort_values("timestamp")

    if df["timestamp"].duplicated().any() or not df["timestamp"].is_monotonic_increasing:
        raise ValueError(f"{path}: invalid timestamps")

    for column in ("open", "close", "volume"):
        df[column] = pd.to_numeric(df[column], errors="coerce")

    if df[["open", "close"]].isna().any().any() or (df[["open", "close"]] <= 0).any().any():
        raise ValueError(f"{path}: invalid prices")
    if df["volume"].isna().any() or (df["volume"] < 0).any():
        raise ValueError(f"{path}: invalid volume")

    out = df.loc[
        (df["timestamp"] >= DEVELOPMENT_START)
        & (df["timestamp"] < VALIDATION_START),
        ["timestamp", "open", "close"],
    ].copy()

    if out.empty:
        raise ValueError(f"{path}: no development observations")
    return out.set_index("timestamp")


def load_universe(directory: Path, audit_report: Path):
    audit = pd.read_csv(audit_report)
    eligible = set(
        audit.loc[
            (audit["unexpected_interval_count"] == 0)
            & (audit["zero_volume_rows"] == 0),
            "symbol",
        ].astype(str)
    )

    series = {}
    excluded = []
    for path in sorted(directory.glob("*_5minute.csv")):
        symbol = path.name.removeprefix("NSE_").removesuffix("_5minute.csv")
        if symbol not in eligible:
            excluded.append({"symbol": symbol, "reason": "failed structural universe audit"})
            continue
        try:
            series[symbol] = load_development(path)
        except (ValueError, AssertionError) as exc:
            excluded.append({"symbol": symbol, "reason": str(exc)})

    if len(series) < MIN_INSTRUMENTS:
        raise SystemExit(f"Need at least {MIN_INSTRUMENTS} eligible instruments")
    return series, excluded


def build_weights(residual: pd.Series) -> pd.Series:
    negative = residual[residual < 0].index
    positive = residual[residual > 0].index
    if len(negative) == 0 or len(positive) == 0:
        return pd.Series(dtype=float)

    weights = pd.Series(0.0, index=residual.index, dtype=float)
    weights.loc[negative] = 0.5 / len(negative)
    weights.loc[positive] = -0.5 / len(positive)
    return weights


def gross_trade_return(
    weights: pd.Series,
    opens: pd.DataFrame,
    closes: pd.DataFrame,
    entry_ts: pd.Timestamp,
    exit_ts: pd.Timestamp,
) -> float:
    common = weights.index.intersection(opens.columns).intersection(closes.columns)
    common = common[
        opens.loc[entry_ts, common].notna()
        & closes.loc[exit_ts, common].notna()
    ]
    if len(common) < MIN_INSTRUMENTS:
        return np.nan

    asset_returns = closes.loc[exit_ts, common] / opens.loc[entry_ts, common] - 1.0
    return float((weights.loc[common] * asset_returns).sum())


def run_variant(series: dict[str, pd.DataFrame], holding_bars: int) -> pd.DataFrame:
    closes = pd.DataFrame({symbol: frame["close"] for symbol, frame in series.items()}).sort_index()
    opens = pd.DataFrame({symbol: frame["open"] for symbol, frame in series.items()}).sort_index()
    returns = closes.pct_change(fill_method=None)

    timestamps = returns.index
    records = []
    next_available_index = 0

    for index, ts in enumerate(timestamps):
        if index < next_available_index:
            continue

        valid = returns.loc[ts].dropna()
        if len(valid) < MIN_INSTRUMENTS:
            continue

        cross_sum = valid.sum()
        n = len(valid)
        residual = valid - (cross_sum - valid) / (n - 1)
        weights = build_weights(residual)
        if weights.empty:
            continue

        entry_index = index + 1
        exit_index = entry_index + holding_bars - 1
        if exit_index >= len(timestamps):
            continue

        entry_ts = timestamps[entry_index]
        exit_ts = timestamps[exit_index]
        if entry_ts.date() != ts.date() or exit_ts.date() != ts.date():
            continue
        if entry_ts not in opens.index or exit_ts not in closes.index:
            continue

        gross_return = gross_trade_return(weights, opens, closes, entry_ts, exit_ts)
        if not np.isfinite(gross_return):
            continue

        next_available_index = exit_index + 1
        records.append(
            {
                "signal_timestamp": ts,
                "entry_timestamp": entry_ts,
                "exit_timestamp": exit_ts,
                "holding_bars": holding_bars,
                "holding_minutes": 5 * holding_bars,
                "long_count": int((weights > 0).sum()),
                "short_count": int((weights < 0).sum()),
                "gross_return": gross_return,
                "executed_round_trip_turnover": 2.0,
            }
        )

    return pd.DataFrame(records)


def metrics(returns: pd.Series) -> dict:
    r = returns.dropna()
    if r.empty:
        return {
            "trades": 0,
            "mean_gross_return_bps": np.nan,
            "median_gross_return_bps": np.nan,
            "gross_win_rate": np.nan,
            "compounded_return_pct": np.nan,
            "max_drawdown_pct": np.nan,
        }

    equity = (1.0 + r).cumprod()
    drawdown = equity / equity.cummax() - 1.0
    return {
        "trades": int(len(r)),
        "mean_gross_return_bps": float(r.mean() * 1e4),
        "median_gross_return_bps": float(r.median() * 1e4),
        "gross_win_rate": float((r > 0).mean()),
        "compounded_return_pct": float((equity.iloc[-1] - 1.0) * 100.0),
        "max_drawdown_pct": float(drawdown.min() * 100.0),
    }


def main():
    args = parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)
    series, excluded = load_universe(args.directory, args.audit_report)

    all_rows = []
    summary_rows = []

    for holding_bars in HOLDING_BARS:
        trades = run_variant(series, holding_bars)
        if trades.empty:
            continue

        trades["signal_timestamp"] = pd.to_datetime(trades["signal_timestamp"])
        gross = trades["gross_return"]
        base = metrics(gross)

        for cost_bps in COST_SCENARIOS_BPS:
            net = gross - cost_bps / 1e4
            m = metrics(net)
            summary_rows.append(
                {
                    "holding_variant": f"H{holding_bars}",
                    "holding_bars": holding_bars,
                    "cost_round_trip_bps": cost_bps,
                    **m,
                    "mean_executed_turnover_per_trade": 2.0,
                    "gross_return_per_turnover_bps": float(gross.mean() * 1e4 / 2.0),
                    "development_start": str(DEVELOPMENT_START),
                    "development_end_exclusive": str(VALIDATION_START),
                }
            )

        all_rows.append(trades)

    if not summary_rows:
        raise SystemExit("No development trades were generated")

    pd.concat(all_rows, ignore_index=True).to_csv(
        args.output_dir / "turnover_reduction_trades.csv",
        index=False,
    )
    pd.DataFrame(summary_rows).to_csv(
        args.output_dir / "turnover_reduction_summary.csv",
        index=False,
    )
    (args.output_dir / "run_manifest.json").write_text(
        json.dumps(
            {
                "analysis": "strategy_002_turnover_reduction_development",
                "development_start": str(DEVELOPMENT_START),
                "validation_start": str(VALIDATION_START),
                "holdout_start": str(HOLDOUT_START),
                "holding_bars": list(HOLDING_BARS),
                "cost_scenarios_round_trip_bps": list(COST_SCENARIOS_BPS),
                "holdout_used": False,
                "validation_used": False,
                "optimization_after_results": False,
                "selection_rule": "pre-registered H2/H3/H6 only",
            },
            indent=2,
        ),
        encoding="utf-8",
    )

    print(f"Included instruments: {len(series)}")
    print(f"Excluded instruments: {len(excluded)}")
    print(f"Development variants: {list(HOLDING_BARS)}")
    print(f"Outputs: {args.output_dir}")


if __name__ == "__main__":
    main()
