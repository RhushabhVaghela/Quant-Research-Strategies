"""Descriptive GOLDBEES-vs-U1 behavior diagnostics for Strategy 001J.

This tool never selects or filters the Strategy 001J universe. An explicit
observation end boundary is required to make the comparison auditable.
"""

from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import pandas as pd

UTC = "UTC"
DISTANCE_FEATURES = [
    "daily_vol_annualized",
    "autocorr_5m_lag1",
    "mean_abs_5m_return",
    "positive_fraction_5m",
    "upper_tail_frequency_5m",
]


def _load_bars(path: Path, end: pd.Timestamp) -> pd.DataFrame:
    df = pd.read_csv(path)
    required = {"timestamp", "open", "high", "low", "close", "volume"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"{path}: missing columns {sorted(missing)}")
    ts = pd.to_datetime(df["timestamp"], errors="raise", utc=True)
    df = df.assign(timestamp=ts).set_index("timestamp").sort_index()
    if df.index.has_duplicates:
        raise ValueError(f"{path}: duplicate timestamps")
    df = df.loc[df.index <= end]
    df["close"] = pd.to_numeric(df["close"], errors="coerce")
    return df.loc[df["close"].gt(0)]


def _daily_returns(df: pd.DataFrame) -> pd.Series:
    daily = df["close"].groupby(df.index.floor("D")).last()
    return daily.pct_change().dropna()


def _five_minute_returns(df: pd.DataFrame) -> pd.Series:
    return df["close"].pct_change().replace([np.inf, -np.inf], np.nan).dropna()


def _aligned_corr(left: pd.Series, right: pd.Series) -> tuple[float, int]:
    joined = pd.concat([left.rename("left"), right.rename("right")], axis=1, join="inner").dropna()
    if len(joined) < 3 or joined["left"].std(ddof=1) == 0 or joined["right"].std(ddof=1) == 0:
        return np.nan, int(len(joined))
    return float(joined["left"].corr(joined["right"])), int(len(joined))


def _descriptors(reference: pd.DataFrame, candidate: pd.DataFrame) -> dict[str, float]:
    ref_5m = _five_minute_returns(reference)
    cand_5m = _five_minute_returns(candidate)
    ref_daily = _daily_returns(reference)
    cand_daily = _daily_returns(candidate)
    corr_5m, overlap_5m = _aligned_corr(ref_5m, cand_5m)
    corr_daily, overlap_daily = _aligned_corr(ref_daily, cand_daily)
    tail_threshold = float(ref_5m.quantile(0.95)) if len(ref_5m) >= 20 else np.nan
    return {
        "corr_5m": corr_5m,
        "corr_daily": corr_daily,
        "daily_vol_annualized": float(cand_daily.std(ddof=1) * np.sqrt(252)) if len(cand_daily) >= 2 else np.nan,
        "autocorr_5m_lag1": float(cand_5m.autocorr(lag=1)) if len(cand_5m) >= 3 else np.nan,
        "mean_abs_5m_return": float(cand_5m.abs().mean()) if len(cand_5m) else np.nan,
        "positive_fraction_5m": float((cand_5m > 0).mean()) if len(cand_5m) else np.nan,
        "upper_tail_frequency_5m": float((cand_5m > tail_threshold).mean()) if np.isfinite(tail_threshold) and len(cand_5m) else np.nan,
        "observations_5m": int(len(cand_5m)),
        "observations_daily": int(len(cand_daily)),
        "overlap_5m": overlap_5m,
        "overlap_daily": overlap_daily,
    }


def _distance_and_rank(report: pd.DataFrame) -> pd.DataFrame:
    z = pd.DataFrame(index=report.index)
    for col in DISTANCE_FEATURES:
        x = pd.to_numeric(report[col], errors="coerce")
        median = x.median()
        mad = (x - median).abs().median()
        scale = 1.4826 * mad if np.isfinite(mad) and mad > 0 else x.std(ddof=1)
        z[col] = (x - median) / scale if np.isfinite(scale) and scale > 0 else 0.0
    # Correlation is a direct similarity measure; convert it to distance from 1.
    for col in ("corr_5m", "corr_daily"):
        if col in report.columns:
            z[col] = 1.0 - pd.to_numeric(report[col], errors="coerce")
    report = report.copy()
    # Avoid numpy's "Mean of empty slice" warning when a diagnostic has no
    # finite features (e.g. deliberately tiny unit-test fixtures). Such a
    # symbol remains unrated rather than being assigned an artificial distance.
    finite_counts = z.notna().sum(axis=1)
    squared = z.pow(2).where(z.notna())
    mean_squared = squared.sum(axis=1, min_count=1) / finite_counts.replace(0, np.nan)
    report["descriptive_distance"] = np.sqrt(mean_squared)
    report["descriptive_rank"] = report["descriptive_distance"].rank(method="min", ascending=True).astype("Int64")
    return report


def analyze(reference_path: Path, universe_dir: Path, end: str) -> pd.DataFrame:
    end_ts = pd.Timestamp(end)
    end_ts = end_ts.tz_localize(UTC) if end_ts.tzinfo is None else end_ts.tz_convert(UTC)
    reference = _load_bars(reference_path, end_ts)
    if reference.empty:
        raise ValueError("Reference GOLDBEES data is empty before the --end boundary")
    rows: list[dict] = []
    for path in sorted(universe_dir.glob("*.csv")):
        if path.name.lower() == reference_path.name.lower():
            continue
        candidate = _load_bars(path, end_ts)
        if candidate.empty:
            continue
        rows.append({"symbol": path.stem.upper(), **_descriptors(reference, candidate)})
    report = pd.DataFrame(rows)
    return _distance_and_rank(report.sort_values("symbol").reset_index(drop=True)) if not report.empty else report


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--reference", type=Path, required=True, help="GOLDBEES 5-minute OHLCV CSV")
    parser.add_argument("--universe-dir", type=Path, required=True, help="Directory containing U1 symbol CSV files")
    parser.add_argument("--end", required=True, help="Frozen observation boundary, e.g. 2026-01-31T15:30:00+05:30")
    parser.add_argument("--output", type=Path, default=Path("data/reports/strategy_001j_universe_similarity/similarity.csv"))
    args = parser.parse_args()
    report = analyze(args.reference, args.universe_dir, args.end)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    report.to_csv(args.output, index=False)
    print(f"Wrote {len(report)} symbol diagnostics to {args.output}")


if __name__ == "__main__":
    main()
