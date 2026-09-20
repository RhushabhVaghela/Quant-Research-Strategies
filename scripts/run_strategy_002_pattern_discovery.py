"""Run Strategy 002 hypothesis-free exploratory pattern diagnostics.

The analysis is locked to the exploratory-development period. It does not
calculate strategy P&L and cannot read validation/holdout observations.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd

EXPLORATORY_START = pd.Timestamp("2025-09-18", tz="Asia/Kolkata")
EXPLORATORY_END = pd.Timestamp("2026-06-09 23:59:59", tz="Asia/Kolkata")
VALIDATION_START = pd.Timestamp("2026-06-10", tz="Asia/Kolkata")
HOLDOUT_START = pd.Timestamp("2026-08-20", tz="Asia/Kolkata")
LAGS = (1, 2, 3, 6, 12, 24)
HORIZONS = (1, 2, 3, 6, 12)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory", type=Path)
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("data/reports/strategy_002_pattern_discovery"),
    )
    parser.add_argument(
        "--audit-report",
        type=Path,
        default=Path("data/reports/strategy_002_universe_audit.csv"),
    )
    return parser.parse_args()


def load_symbol(path: Path) -> pd.DataFrame:
    df = pd.read_csv(path, parse_dates=["timestamp"])
    required = {"timestamp", "open", "high", "low", "close", "volume"}
    missing = required.difference(df.columns)
    if missing:
        raise ValueError(f"{path}: missing columns {sorted(missing)}")

    timestamps = pd.DatetimeIndex(df["timestamp"])
    if timestamps.tz is None:
        raise ValueError(f"{path}: timestamps must be timezone-aware")
    df["timestamp"] = timestamps.tz_convert("Asia/Kolkata")
    df = df.sort_values("timestamp")

    if df["timestamp"].duplicated().any():
        raise ValueError(f"{path}: duplicate timestamps")
    if not df["timestamp"].is_monotonic_increasing:
        raise ValueError(f"{path}: non-monotonic timestamps")

    numeric = ["open", "high", "low", "close", "volume"]
    for column in numeric:
        df[column] = pd.to_numeric(df[column], errors="coerce")

    if df[["open", "high", "low", "close"]].isna().any().any():
        raise ValueError(f"{path}: missing OHLC values")
    if (df[["open", "high", "low", "close"]] <= 0).any().any():
        raise ValueError(f"{path}: non-positive OHLC values")
    if df["volume"].isna().any() or (df["volume"] < 0).any():
        raise ValueError(f"{path}: invalid volume")

    return df


def exploratory_slice(df: pd.DataFrame) -> pd.DataFrame:
    mask = (df["timestamp"] >= EXPLORATORY_START) & (
        df["timestamp"] <= EXPLORATORY_END
    )
    out = df.loc[mask].copy()
    if out.empty:
        raise ValueError("No observations in the locked exploratory window")

    # This is a hard research-control check, not merely a filter.
    if out["timestamp"].max() >= VALIDATION_START:
        raise AssertionError("Exploratory data crossed into validation")
    if out["timestamp"].max() >= HOLDOUT_START:
        raise AssertionError("Exploratory data crossed into holdout")
    return out


def return_dynamics(df: pd.DataFrame, symbol: str) -> pd.DataFrame:
    returns = df["close"].pct_change()
    absolute_returns = returns.abs()
    rows = []

    for lag in LAGS:
        rows.append(
            {
                "symbol": symbol,
                "lag_bars": lag,
                "return_autocorr": returns.autocorr(lag=lag),
                "absolute_return_autocorr": absolute_returns.autocorr(lag=lag),
                "observations": int(returns.notna().sum()),
            }
        )

    return pd.DataFrame(rows)


def forward_diagnostics(df: pd.DataFrame, symbol: str) -> pd.DataFrame:
    returns = df["close"].pct_change()
    prior_6 = df["close"].pct_change(6)
    magnitude_rank = returns.abs().rank(method="first")
    magnitude_bucket = pd.qcut(
        magnitude_rank,
        q=4,
        labels=["Q1", "Q2", "Q3", "Q4"],
        duplicates="drop",
    )

    states = {
        "all": pd.Series(True, index=df.index),
        "prior_return_positive": returns > 0,
        "prior_return_negative": returns < 0,
        "prior_6_return_positive": prior_6 > 0,
        "prior_6_return_negative": prior_6 < 0,
    }

    rows = []
    for horizon in HORIZONS:
        forward = df["close"].shift(-horizon) / df["close"] - 1.0
        for state_name, state_mask in states.items():
            sample = forward.loc[state_mask].dropna()
            rows.append(
                {
                    "symbol": symbol,
                    "horizon_bars": horizon,
                    "state": state_name,
                    "bucket": "ALL",
                    "observations": int(sample.size),
                    "mean_forward_return": sample.mean(),
                    "median_forward_return": sample.median(),
                }
            )

        for bucket in magnitude_bucket.dropna().unique():
            bucket_mask = magnitude_bucket == bucket
            sample = forward.loc[bucket_mask].dropna()
            rows.append(
                {
                    "symbol": symbol,
                    "horizon_bars": horizon,
                    "state": "prior_abs_return_quartile",
                    "bucket": str(bucket),
                    "observations": int(sample.size),
                    "mean_forward_return": sample.mean(),
                    "median_forward_return": sample.median(),
                }
            )

    return pd.DataFrame(rows)


def intraday_diagnostics(df: pd.DataFrame, symbol: str) -> pd.DataFrame:
    work = df.copy()
    work["return"] = work["close"].pct_change()
    work["bar_number"] = work.groupby(work["timestamp"].dt.date).cumcount() + 1

    out = (
        work.groupby("bar_number", observed=True)
        .agg(
            mean_return=("return", "mean"),
            median_return=("return", "median"),
            mean_abs_return=("return", lambda x: x.abs().mean()),
            return_std=("return", "std"),
            mean_volume=("volume", "mean"),
            median_volume=("volume", "median"),
            observations=("return", "count"),
        )
        .reset_index()
    )
    out.insert(0, "symbol", symbol)
    return out


def daily_correlation_diagnostics(
    frames: dict[str, pd.DataFrame],
) -> pd.DataFrame:
    daily = []
    for symbol, frame in frames.items():
        work = frame.set_index("timestamp")
        close = work["close"].resample("1D").last()
        daily.append(close.pct_change(fill_method=None).rename(symbol))
    panel = pd.concat(daily, axis=1)
    corr = panel.corr()
    upper = np.triu(np.ones(corr.shape, dtype=bool), k=1)
    return (
        corr.where(upper)
        .stack()
        .rename("correlation")
        .reset_index()
        .rename(columns={"level_0": "symbol_a", "level_1": "symbol_b"})
    )


def lead_lag_diagnostics(
    frames: dict[str, pd.DataFrame],
) -> pd.DataFrame:
    series = {
        symbol: frame.set_index("timestamp")["close"].pct_change()
        for symbol, frame in frames.items()
    }
    rows = []
    symbols = sorted(series)
    for i, symbol_a in enumerate(symbols):
        for symbol_b in symbols[i + 1 :]:
            pair = pd.concat([series[symbol_a], series[symbol_b]], axis=1).dropna()
            if len(pair) < max(LAGS) + 10:
                continue
            for lag in LAGS:
                rows.append(
                    {
                        "symbol_leader": symbol_a,
                        "symbol_follower": symbol_b,
                        "lag_bars": lag,
                        "correlation": pair.iloc[:, 0].corr(pair.iloc[:, 1].shift(-lag)),
                        "observations": int(pair.iloc[:, [0, 1]].dropna().shape[0]),
                    }
                )
                rows.append(
                    {
                        "symbol_leader": symbol_b,
                        "symbol_follower": symbol_a,
                        "lag_bars": lag,
                        "correlation": pair.iloc[:, 1].corr(pair.iloc[:, 0].shift(-lag)),
                        "observations": int(pair.iloc[:, [0, 1]].dropna().shape[0]),
                    }
                )
    return pd.DataFrame(rows)



def cross_sectional_diagnostics(
    frames: dict[str, pd.DataFrame],
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    series = []
    for symbol, frame in frames.items():
        series.append(
            frame.set_index("timestamp")["close"].pct_change().rename(symbol)
        )

    panel = pd.concat(series, axis=1).sort_index()
    correlation = panel.corr()

    upper = np.triu(np.ones(correlation.shape, dtype=bool), k=1)
    correlation_long = (
        correlation.where(upper)
        .stack()
        .rename("correlation")
        .reset_index()
        .rename(columns={"level_0": "symbol_a", "level_1": "symbol_b"})
    )

    dispersion = pd.DataFrame(
        {
            "timestamp": panel.index,
            "cross_sectional_mean_return": panel.mean(axis=1),
            "cross_sectional_std_return": panel.std(axis=1),
            "cross_sectional_median_return": panel.median(axis=1),
            "active_instruments": panel.notna().sum(axis=1),
        }
    )

    # PCA requires rows with complete observations across the retained symbols.
    # Retain symbols with usable coverage first, then remove incomplete rows.
    complete = panel.dropna(axis=1, how="all").dropna(how="any")
    if complete.shape[0] < 2 or complete.shape[1] < 2:
        pca = pd.DataFrame(
            [
                {
                    "component": 1,
                    "explained_variance_ratio": np.nan,
                    "cumulative_explained_variance": np.nan,
                    "note": "insufficient complete aligned panel",
                }
            ]
        )
    else:
        standardized = (complete - complete.mean()) / complete.std(ddof=1)
        singular_values = np.linalg.svd(
            standardized.to_numpy(), full_matrices=False, compute_uv=False
        )
        eigenvalues = singular_values**2 / max(len(standardized) - 1, 1)
        ratios = eigenvalues / eigenvalues.sum()
        pca = pd.DataFrame(
            {
                "component": np.arange(1, len(ratios) + 1),
                "explained_variance_ratio": ratios,
            }
        )
        pca["cumulative_explained_variance"] = (
            pca["explained_variance_ratio"].cumsum()
        )
        pca["note"] = ""

    return correlation_long, dispersion, pca


def main() -> None:
    args = parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)

    paths = sorted(args.directory.glob("*_5minute.csv"))
    if not paths:
        raise SystemExit(f"No *_5minute.csv files found in {args.directory}")

    if not args.audit_report.exists():
        raise SystemExit(f"Audit report not found: {args.audit_report}")
    audit = pd.read_csv(args.audit_report)
    required_audit = {"symbol", "unexpected_interval_count", "zero_volume_rows"}
    missing_audit = required_audit.difference(audit.columns)
    if missing_audit:
        raise SystemExit(
            f"Audit report missing required columns: {sorted(missing_audit)}"
        )
    structurally_eligible = set(
        audit.loc[
            (audit["unexpected_interval_count"] == 0)
            & (audit["zero_volume_rows"] == 0),
            "symbol",
        ].astype(str)
    )

    frames: dict[str, pd.DataFrame] = {}
    excluded: list[dict[str, str]] = []

    for path in paths:
        symbol = path.name.removeprefix("NSE_").removesuffix("_5minute.csv")
        if symbol not in structurally_eligible:
            excluded.append(
                {"symbol": symbol, "reason": "failed structural universe audit"}
            )
            continue
        try:
            frames[symbol] = exploratory_slice(load_symbol(path))
        except (ValueError, AssertionError) as exc:
            excluded.append({"symbol": symbol, "reason": str(exc)})

    if not frames:
        raise SystemExit("No valid instruments remain for exploratory analysis")

    dynamics = pd.concat(
        [return_dynamics(frame, symbol) for symbol, frame in frames.items()],
        ignore_index=True,
    )
    forward = pd.concat(
        [forward_diagnostics(frame, symbol) for symbol, frame in frames.items()],
        ignore_index=True,
    )
    intraday = pd.concat(
        [intraday_diagnostics(frame, symbol) for symbol, frame in frames.items()],
        ignore_index=True,
    )
    correlation, dispersion, pca = cross_sectional_diagnostics(frames)
    daily_correlation = daily_correlation_diagnostics(frames)
    lead_lag = lead_lag_diagnostics(frames)

    dynamics.to_csv(args.output_dir / "return_dynamics.csv", index=False)
    forward.to_csv(args.output_dir / "forward_horizon_diagnostics.csv", index=False)
    intraday.to_csv(args.output_dir / "intraday_diagnostics.csv", index=False)
    correlation.to_csv(
        args.output_dir / "cross_sectional_correlation.csv", index=False
    )
    daily_correlation.to_csv(
        args.output_dir / "daily_correlation.csv", index=False
    )
    lead_lag.to_csv(args.output_dir / "lead_lag_diagnostics.csv", index=False)
    dispersion.to_csv(
        args.output_dir / "cross_sectional_dispersion.csv", index=False
    )
    pca.to_csv(args.output_dir / "pca_explained_variance.csv", index=False)

    manifest = {
        "analysis": "strategy_002_pattern_discovery",
        "methodology_version": "v1",
        "exploratory_start": str(EXPLORATORY_START),
        "exploratory_end": str(EXPLORATORY_END),
        "validation_start": str(VALIDATION_START),
        "holdout_start": str(HOLDOUT_START),
        "lags": list(LAGS),
        "horizons": list(HORIZONS),
        "included_symbols": sorted(frames),
        "excluded_symbols": excluded,
        "holdout_used": False,
        "strategy_pnl_calculated": False,
    }
    (args.output_dir / "run_manifest.json").write_text(
        json.dumps(manifest, indent=2), encoding="utf-8"
    )

    print(f"Included instruments: {len(frames)}")
    print(f"Excluded instruments: {len(excluded)}")
    print(f"Exploratory window: {EXPLORATORY_START} -> {EXPLORATORY_END}")
    print(f"Outputs: {args.output_dir}")


if __name__ == "__main__":
    main()
