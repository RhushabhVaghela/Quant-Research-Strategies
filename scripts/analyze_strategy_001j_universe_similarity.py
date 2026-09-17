"""Descriptive behavior similarity analysis for Strategy 001J.

This tool compares U1 securities with GOLDBEES using pre-registered,
strategy-outcome-independent descriptors. It never selects a trading universe.
An explicit --end boundary is required so the observation window can be frozen
before performance results are inspected.
"""

from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import pandas as pd

UTC = "UTC"

FEATURE_COLUMNS = [
    "corr_5m",
    "corr_daily",
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
    df = df.loc[~df.index.duplicated(keep="first")]
    df = df.loc[df.index <= end]
    df["close"] = pd.to_numeric(df["close"], errors="coerce")
    return df.loc[df["close"].gt(0)]


def _daily_returns(df: pd.DataFrame) -> pd.Series:
    daily = df["close"].groupby(df.index.floor("D")).last()
    return daily.pct_change().dropna()


def _five_minute_returns(df: pd.DataFrame) -> pd.Series:
    return df["close"].pct_change().replace([np.inf, -np.inf], np.nan).dropna()


def _aligned_corr(left: pd.Series, right: pd.Series) -> float:
    joined = pd.concat([left.rename("left"), right.rename("right")], axis=1, join="inner").dropna()
    if len(joined) < 3 or joined["left"].std(ddof=1) == 0 or joined["right"].std(ddof=1) == 0:
        return np.nan
    return float(joined["left"].corr(joined["right"]))


def _descriptors(reference: pd.DataFrame, candidate: pd.DataFrame) -> dict[str, float]:
    ref_5m = _five_minute_returns(reference)
    cand_5m = _five_minute_returns(candidate)
    ref_daily = _daily_returns(reference)
    cand_daily = _daily_returns(candidate)

    # Use the reference distribution only to define a fixed descriptive tail threshold.
    # This is not a strategy threshold and is not fitted to candidate performance.
    tail_threshold = float(ref_5m.quantile(0.95)) if len(ref_5m) >= 20 else np.nan
    upper_tail = (
        float((cand_5m > tail_threshold).mean())
        if np.isfinite(tail_threshold) and len(cand_5m)
        else np.nan
    )

    return {
        "corr_5m": _aligned_corr(ref_5m, cand_5m),
        "corr_daily": _aligned_corr(ref_daily, cand_daily),
        "daily_vol_annualized": float(cand_daily.std(ddof=1) * np.sqrt(252)) if len(cand_daily) >= 2 else np.nan,
        "autocorr_5m_lag1": float(cand_5m.autocorr(lag=1)) if len(cand_5m) >= 3 else np.nan,
        "mean_abs_5m_return": float(cand_5m.abs().mean()) if len(cand_5m) else np.nan,
        "positive_fraction_5m": float((cand_5m > 0).mean()) if len(cand_5m) else np.nan,
        "upper_tail_frequency_5m": upper_tail,
        "observations_5m": int(len(cand_5m)),
        "observations_daily": int(len(cand_daily)),
        "overlap_5m": int(pd.concat([ref_5m.rename("r"), cand_5m.rename("c")], axis=1, join="inner").dropna().shape[0]),
        "overlap_daily": int(pd.concat([ref_daily.rename("r"), cand_daily.rename("c")], axis=1, join="inner").dropna().shape[0]),
    }


def _distance_and_rank(report: pd.DataFrame) -> pd.DataFrame:
    """Create a descriptive standardized distance; never creates a selection flag."""
    available = [c for c in FEATURE_COLUMNS if c in report.columns]
    z = pd.DataFrame(index=report.index)
    for col in available:
        x = pd.to_numeric(report[col], errors="coerce")
        median = x.median()
        mad = (x - median).abs().median()
        scale = 1.4826 * mad if np.isfinite(mad) and mad > 0 else x.std(ddof=1)
        z[col] = (x - median) / scale if np.isfinite(scale) and scale > 0 else 0.0

    # Correlations are converted to distance from the reference behavior (1 = identical).
    if "corr_5m" in z:
        z["corr_5m"] = 1.0 - report["corr_5m"]
    if "corr_daily" in z:
        z["corr_daily"] = 1.0 - report["corr_daily"]

    report = report.copy()
    report["descriptive_distance"] = np.sqrt(z.pow(2).mean(axis=1, skipna=True))
    report["descriptive_rank"] = report["descriptive_distance"].rank(method="min", ascending=True).astype("Int64")
    return report


def analyze(reference_path: Path, universe_dir: Path, end: str) -> pd.DataFrame:
    end_ts = pd.Timestamp(end)
    if end_ts.tzinfo is None:
        end_ts = end_ts.tz_localize(UTC)
    else:
        end_ts = end_ts.tz_convert(UTC)

    reference = _load_bars(reference_path, end_ts)
    if reference.empty:
        raise ValueError("Reference GOLDBEES data is empty before the --end boundary")

    rows: list[dict] = []
    for path in sorted(universe_dir.glob("*.csv")):
        if path.name.lower() == reference_path.name.lower():
            continue
        try:
            candidate = _load_bars(path, end_ts)
            if candidate.empty:
                continue
            row = {"symbol": path.stem, **_descriptors(reference, candidate)}
            rows.append(row)
        except (ValueError, pd.errors.ParserError) as exc:
            raise ValueError(f"Failed to analyze {path}: {exc}") from exc

    report = pd.DataFrame(rows)
    if report.empty:
        return report
    return _distance_and_rank(report.sort_values("symbol").reset_index(drop=True))


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
