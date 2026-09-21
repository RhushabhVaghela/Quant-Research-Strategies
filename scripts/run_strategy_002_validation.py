"""Run the frozen Strategy 002 baseline on the chronological validation period."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd

VALIDATION_START = pd.Timestamp("2026-06-10", tz="Asia/Kolkata")
HOLDOUT_START = pd.Timestamp("2026-08-20", tz="Asia/Kolkata")
COST_SCENARIOS_BPS = (0.0, 5.0, 10.0, 15.0)


def parse_args():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("directory", type=Path)
    p.add_argument(
        "--audit-report",
        type=Path,
        default=Path("data/reports/strategy_002_universe_audit.csv"),
    )
    p.add_argument(
        "--output-dir",
        type=Path,
        default=Path("data/reports/strategy_002_validation"),
    )
    return p.parse_args()


def load_validation(path: Path) -> pd.DataFrame:
    df = pd.read_csv(path, parse_dates=["timestamp"])
    required = {"timestamp", "open", "close", "volume"}
    if not required.issubset(df.columns):
        raise ValueError(f"{path}: missing required columns")
    ts = pd.DatetimeIndex(df["timestamp"])
    if ts.tz is None:
        raise ValueError(f"{path}: timestamps must be timezone-aware")
    df["timestamp"] = ts.tz_convert("Asia/Kolkata")
    df = df.sort_values("timestamp")
    if df["timestamp"].duplicated().any() or not df["timestamp"].is_monotonic_increasing:
        raise ValueError(f"{path}: invalid timestamps")
    for c in ["open", "close", "volume"]:
        df[c] = pd.to_numeric(df[c], errors="coerce")
    if df[["open", "close"]].isna().any().any() or (df[["open", "close"]] <= 0).any().any():
        raise ValueError(f"{path}: invalid prices")
    if df["volume"].isna().any() or (df["volume"] < 0).any():
        raise ValueError(f"{path}: invalid volume")

    out = df.loc[
        (df.timestamp >= VALIDATION_START) & (df.timestamp < HOLDOUT_START),
        ["timestamp", "open", "close"],
    ].copy()
    if out.empty:
        raise ValueError(f"{path}: no validation observations")
    if out.timestamp.min() < VALIDATION_START or out.timestamp.max() >= HOLDOUT_START:
        raise AssertionError(f"{path}: crossed validation boundaries")
    out["return"] = out["close"].pct_change(fill_method=None)
    return out.set_index("timestamp")


def load_universe(directory: Path, audit_report: Path):
    audit = pd.read_csv(audit_report)
    eligible = set(
        audit.loc[
            (audit.unexpected_interval_count == 0)
            & (audit.zero_volume_rows == 0),
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
            series[symbol] = load_validation(path)
        except (ValueError, AssertionError) as exc:
            excluded.append({"symbol": symbol, "reason": str(exc)})
    if len(series) < 4:
        raise SystemExit("Need at least four eligible instruments")
    return series, excluded


def build_signals(series: dict[str, pd.DataFrame]) -> pd.DataFrame:
    closes = pd.DataFrame({s: d["close"] for s, d in series.items()}).sort_index()
    opens = pd.DataFrame({s: d["open"] for s, d in series.items()}).sort_index()
    returns = closes.pct_change(fill_method=None)

    records = []
    for ts in returns.index:
        row = returns.loc[ts]
        valid = row.dropna()
        if len(valid) < 4:
            continue

        # Leave-one-out residual at the completed signal bar.
        cross_sum = valid.sum()
        n = len(valid)
        residual = valid - (cross_sum - valid) / (n - 1)

        next_ts = pd.Timestamp(ts) + pd.Timedelta(minutes=5)
        if next_ts not in opens.index or next_ts not in closes.index:
            continue
        # Never carry a position overnight.
        if next_ts.date() != ts.date():
            continue

        long_symbols = residual[residual < 0].index.tolist()
        short_symbols = residual[residual > 0].index.tolist()
        if not long_symbols or not short_symbols:
            continue

        long_returns = (closes.loc[next_ts, long_symbols] / opens.loc[next_ts, long_symbols]) - 1.0
        short_returns = -((closes.loc[next_ts, short_symbols] / opens.loc[next_ts, short_symbols]) - 1.0)

        long_mean = float(long_returns.mean())
        short_mean = float(short_returns.mean())
        portfolio_gross = 0.5 * long_mean + 0.5 * short_mean

        # Diagnostic only: next-bar residual close-to-close outcome.
        next_row = returns.loc[next_ts].dropna()
        common = [s for s in residual.index if s in next_row.index]
        if common:
            next_sum = next_row[common].sum()
            next_n = len(common)
            next_residual = next_row[common] - (next_sum - next_row[common]) / (next_n - 1)
            predictive_long = float(next_residual[long_symbols].mean()) if set(long_symbols).issubset(next_residual.index) else np.nan
            predictive_short = float(-next_residual[short_symbols].mean()) if set(short_symbols).issubset(next_residual.index) else np.nan
            predictive_portfolio = (
                0.5 * predictive_long + 0.5 * predictive_short
                if np.isfinite(predictive_long) and np.isfinite(predictive_short)
                else np.nan
            )
        else:
            predictive_portfolio = np.nan

        records.append(
            {
                "signal_timestamp": ts,
                "entry_timestamp": next_ts,
                "exit_timestamp": next_ts,
                "long_count": len(long_symbols),
                "short_count": len(short_symbols),
                "long_mean_open_to_close": long_mean,
                "short_mean_open_to_close": short_mean,
                "gross_portfolio_return": portfolio_gross,
                "predictive_next_bar_residual_return": predictive_portfolio,
            }
        )

    return pd.DataFrame(records)


def metrics(returns: pd.Series) -> dict:
    r = returns.dropna()
    if r.empty:
        return {
            "observations": 0,
            "mean_signal_return_bps": np.nan,
            "median_signal_return_bps": np.nan,
            "positive_signal_fraction": np.nan,
            "compounded_return_pct": np.nan,
            "daily_sharpe": np.nan,
            "max_drawdown_pct": np.nan,
        }
    equity = (1.0 + r).cumprod()
    daily = equity.groupby(equity.index.date).last().pct_change().dropna()
    sharpe = np.nan
    if len(daily) > 1 and daily.std(ddof=1) > 0:
        sharpe = np.sqrt(252.0) * daily.mean() / daily.std(ddof=1)
    drawdown = equity / equity.cummax() - 1.0
    return {
        "observations": int(len(r)),
        "mean_signal_return_bps": float(r.mean() * 1e4),
        "median_signal_return_bps": float(r.median() * 1e4),
        "positive_signal_fraction": float((r > 0).mean()),
        "compounded_return_pct": float((equity.iloc[-1] - 1.0) * 100.0),
        "daily_sharpe": float(sharpe),
        "max_drawdown_pct": float(drawdown.min() * 100.0),
    }


def main():
    args = parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)
    series, excluded = load_universe(args.directory, args.audit_report)
    signals = build_signals(series)
    if signals.empty:
        raise SystemExit("No validation portfolio observations were generated")

    signals["signal_timestamp"] = pd.to_datetime(signals["signal_timestamp"])
    signals = signals.set_index("signal_timestamp").sort_index()

    summary_rows = []
    daily_rows = []
    for cost_bps in COST_SCENARIOS_BPS:
        net = signals["gross_portfolio_return"] - cost_bps / 1e4
        m = metrics(net)
        m.update(
            {
                "cost_round_trip_bps": cost_bps,
                "validation_start": str(VALIDATION_START),
                "validation_end_exclusive": str(HOLDOUT_START),
            }
        )
        summary_rows.append(m)

        tmp = pd.DataFrame({"return": net})
        daily = tmp.groupby(tmp.index.date)["return"].apply(lambda x: (1.0 + x).prod() - 1.0)
        for date, value in daily.items():
            daily_rows.append(
                {
                    "date": str(date),
                    "cost_round_trip_bps": cost_bps,
                    "daily_return": float(value),
                }
            )

    signals.to_csv(args.output_dir / "validation_signal_returns.csv")
    pd.DataFrame(summary_rows).to_csv(args.output_dir / "validation_summary.csv", index=False)
    pd.DataFrame(daily_rows).to_csv(args.output_dir / "validation_daily_returns.csv", index=False)

    manifest = {
        "analysis": "strategy_002_fixed_baseline_validation",
        "validation_start": str(VALIDATION_START),
        "holdout_start": str(HOLDOUT_START),
        "included_instruments": sorted(series),
        "excluded_instruments": excluded,
        "cost_scenarios_round_trip_bps": list(COST_SCENARIOS_BPS),
        "signal_definition": "leave-one-out residual sign at completed 5-minute close",
        "execution_definition": "next 5-minute bar open to next 5-minute bar close",
        "overnight_positions": False,
        "optimization_performed": False,
        "holdout_used": False,
        "live_orders_placed": False,
    }
    (args.output_dir / "run_manifest.json").write_text(
        json.dumps(manifest, indent=2),
        encoding="utf-8",
    )
    print(f"Included instruments: {len(series)}")
    print(f"Excluded instruments: {len(excluded)}")
    print(f"Validation portfolios: {len(signals)}")
    print(f"Outputs: {args.output_dir}")


if __name__ == "__main__":
    main()
