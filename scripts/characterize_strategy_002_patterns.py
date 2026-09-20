"""Characterize candidate Strategy 002 patterns inside the locked exploratory sample.

This is still exploratory. It measures breadth and temporal stability of already
observed descriptive patterns; it does not define a trading rule or use
validation/holdout data.
"""
from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import pandas as pd

START = pd.Timestamp("2025-09-18", tz="Asia/Kolkata")
END = pd.Timestamp("2026-06-09 23:59:59", tz="Asia/Kolkata")
VALIDATION_START = pd.Timestamp("2026-06-10", tz="Asia/Kolkata")


def args() -> argparse.Namespace:
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
        default=Path("data/reports/strategy_002_pattern_characterization"),
    )
    return p.parse_args()


def load(path: Path) -> pd.DataFrame:
    df = pd.read_csv(path, parse_dates=["timestamp"])
    required = {"timestamp", "open", "high", "low", "close", "volume"}
    missing = required.difference(df.columns)
    if missing:
        raise ValueError(f"{path}: missing columns {sorted(missing)}")

    ts = pd.DatetimeIndex(df["timestamp"])
    if ts.tz is None:
        raise ValueError(f"{path}: timestamps must be timezone-aware")
    df["timestamp"] = ts.tz_convert("Asia/Kolkata")
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
    mask = (df["timestamp"] >= START) & (df["timestamp"] <= END)
    out = df.loc[mask].copy()
    if out.empty:
        raise ValueError("No observations in the locked exploratory window")

    # This is a hard research-control check, not merely a filter.
    if out["timestamp"].max() >= VALIDATION_START:
        raise AssertionError("Exploratory data crossed into validation")
    return out


def conditional_table(df: pd.DataFrame, symbol: str) -> pd.DataFrame:
    r = df["close"].pct_change(fill_method=None)
    r6 = df["close"].pct_change(6, fill_method=None)
    rows = []
    states = {
        "prior_return_negative": r < 0,
        "prior_return_positive": r > 0,
        "prior_6_return_negative": r6 < 0,
        "prior_6_return_positive": r6 > 0,
    }
    for name, mask in states.items():
        for h in (1, 2, 3, 6, 12):
            fwd = df["close"].shift(-h) / df["close"] - 1
            s = fwd.loc[mask].dropna()
            rows.append(
                {
                    "symbol": symbol,
                    "state": name,
                    "horizon": h,
                    "observations": len(s),
                    "mean": s.mean(),
                    "median": s.median(),
                    "positive_fraction": (s > 0).mean() if len(s) else np.nan,
                }
            )

    mag = r.abs().rank(method="first")
    q = pd.qcut(mag, 4, labels=["Q1", "Q2", "Q3", "Q4"], duplicates="drop")
    sign = pd.Series(
        np.where(r > 0, "positive", np.where(r < 0, "negative", "zero")),
        index=df.index,
    )
    for sq in ["positive", "negative"]:
        for bucket in ["Q1", "Q2", "Q3", "Q4"]:
            mask = (sign == sq) & (q == bucket)
            for h in (1, 2, 3, 6):
                fwd = df["close"].shift(-h) / df["close"] - 1
                s = fwd.loc[mask].dropna()
                rows.append(
                    {
                        "symbol": symbol,
                        "state": f"sign_x_abs_quartile_{sq}",
                        "horizon": h,
                        "bucket": bucket,
                        "observations": len(s),
                        "mean": s.mean(),
                        "median": s.median(),
                        "positive_fraction": (s > 0).mean()
                        if len(s)
                        else np.nan,
                    }
                )
    return pd.DataFrame(rows)


def stability(df: pd.DataFrame, symbol: str) -> pd.DataFrame:
    work = df.copy()
    work["return"] = work["close"].pct_change(fill_method=None)
    work["period"] = pd.qcut(
        work["timestamp"].astype("int64"),
        4,
        labels=["Q1_time", "Q2_time", "Q3_time", "Q4_time"],
        duplicates="drop",
    )
    rows = []
    for period, group in work.groupby("period", observed=True):
        r = group["return"]
        for lag in (1, 2, 3, 6, 12, 24):
            rows.append(
                {
                    "symbol": symbol,
                    "period": str(period),
                    "lag": lag,
                    "return_autocorr": r.autocorr(lag=lag),
                    "abs_return_autocorr": r.abs().autocorr(lag=lag),
                }
            )
    return pd.DataFrame(rows)


def main() -> None:
    a = args()
    a.output_dir.mkdir(parents=True, exist_ok=True)
    paths = sorted(a.directory.glob("*_5minute.csv"))
    if not paths:
        raise SystemExit("No Strategy 002 5-minute files found")

    if not a.audit_report.exists():
        raise SystemExit(f"Audit report not found: {a.audit_report}")

    audit = pd.read_csv(a.audit_report)
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

    conditional = []
    stable = []
    excluded = []

    for path in paths:
        symbol = path.name.removeprefix("NSE_").removesuffix("_5minute.csv")
        if symbol not in structurally_eligible:
            excluded.append(
                {"symbol": symbol, "reason": "failed structural universe audit"}
            )
            continue
        try:
            df = exploratory_slice(load(path))
        except (ValueError, AssertionError) as exc:
            excluded.append({"symbol": symbol, "reason": str(exc)})
            continue

        conditional.append(conditional_table(df, symbol))
        stable.append(stability(df, symbol))

    if not conditional or not stable:
        raise SystemExit("No valid instruments remain for exploratory characterization")

    cond = pd.concat(conditional, ignore_index=True)
    stab = pd.concat(stable, ignore_index=True)

    breadth = (
        cond.groupby(["state", "horizon"], as_index=False)
        .agg(
            instruments=("symbol", "nunique"),
            median_instrument_mean=("mean", "median"),
            q25_instrument_mean=("mean", lambda x: x.quantile(0.25)),
            q75_instrument_mean=("mean", lambda x: x.quantile(0.75)),
            positive_instrument_fraction=("mean", lambda x: (x > 0).mean()),
        )
    )

    stability_summary = (
        stab.groupby(["period", "lag"], as_index=False)
        .agg(
            instruments=("symbol", "nunique"),
            median_return_autocorr=("return_autocorr", "median"),
            median_abs_return_autocorr=("abs_return_autocorr", "median"),
            positive_return_autocorr_fraction=(
                "return_autocorr",
                lambda x: (x > 0).mean(),
            ),
        )
    )

    cond.to_csv(a.output_dir / "per_instrument_conditional_patterns.csv", index=False)
    breadth.to_csv(a.output_dir / "pattern_breadth_by_horizon.csv", index=False)
    stab.to_csv(a.output_dir / "temporal_stability_by_instrument.csv", index=False)
    stability_summary.to_csv(
        a.output_dir / "temporal_stability_summary.csv", index=False
    )
    pd.DataFrame(excluded).to_csv(
        a.output_dir / "excluded_instruments.csv", index=False
    )

    print(f"Included files: {len(cond['symbol'].unique())}")
    print(f"Excluded files: {len(excluded)}")
    print(f"Outputs: {a.output_dir}")


if __name__ == "__main__":
    main()
