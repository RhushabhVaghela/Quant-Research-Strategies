"""Decompose the observed short-horizon reversal pattern inside the locked exploratory sample.

This is mechanism characterization only. It does not define a trading rule and
does not read validation or holdout observations.
"""
from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import pandas as pd

START = pd.Timestamp("2025-09-18", tz="Asia/Kolkata")
END = pd.Timestamp("2026-06-09 23:59:59", tz="Asia/Kolkata")
VALIDATION_START = pd.Timestamp("2026-06-10", tz="Asia/Kolkata")


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("directory", type=Path)
    p.add_argument("--audit-report", type=Path,
                   default=Path("data/reports/strategy_002_universe_audit.csv"))
    p.add_argument("--output-dir", type=Path,
                   default=Path("data/reports/strategy_002_reversal_mechanism"))
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
    if df["timestamp"].duplicated().any() or not df["timestamp"].is_monotonic_increasing:
        raise ValueError(f"{path}: invalid timestamp ordering")
    numeric = ["open", "high", "low", "close", "volume"]
    for c in numeric:
        df[c] = pd.to_numeric(df[c], errors="coerce")
    if df[["open", "high", "low", "close"]].isna().any().any():
        raise ValueError(f"{path}: missing OHLC")
    if (df[["open", "high", "low", "close"]] <= 0).any().any():
        raise ValueError(f"{path}: non-positive OHLC")
    if df["volume"].isna().any() or (df["volume"] < 0).any():
        raise ValueError(f"{path}: invalid volume")
    out = df.loc[(df["timestamp"] >= START) & (df["timestamp"] <= END)].copy()
    if out.empty:
        raise ValueError(f"{path}: no exploratory observations")
    if out["timestamp"].max() >= VALIDATION_START:
        raise AssertionError(f"{path}: exploratory data crossed validation boundary")
    return out


def rows(df: pd.DataFrame, symbol: str) -> pd.DataFrame:
    prior = df["close"].pct_change(fill_method=None)
    next_close = df["close"].shift(-1)
    next_open = df["open"].shift(-1)

    next_cc = next_close / df["close"] - 1
    next_co = next_open / df["close"] - 1
    next_oc = next_close / next_open - 1

    magnitude = prior.abs().rank(method="first")
    quartile = pd.qcut(magnitude, 4, labels=["Q1", "Q2", "Q3", "Q4"], duplicates="drop")
    sign = pd.Series(np.where(prior > 0, "positive",
                              np.where(prior < 0, "negative", "zero")),
                     index=df.index)

    states = []
    for s in ("negative", "positive"):
        states.append((f"prior_{s}", sign == s))
        for q in ("Q1", "Q2", "Q3", "Q4"):
            states.append((f"prior_{s}_abs_{q}", (sign == s) & (quartile == q)))

    result = []
    for state, mask in states:
        for component, series in (
            ("next_close_to_close", next_cc),
            ("next_close_to_open", next_co),
            ("next_open_to_close", next_oc),
        ):
            x = series.loc[mask].dropna()
            result.append({
                "symbol": symbol,
                "state": state,
                "component": component,
                "observations": len(x),
                "mean": x.mean(),
                "median": x.median(),
                "positive_fraction": (x > 0).mean() if len(x) else np.nan,
            })
    return pd.DataFrame(result)


def main() -> None:
    a = parse_args()
    a.output_dir.mkdir(parents=True, exist_ok=True)
    if not a.audit_report.exists():
        raise SystemExit(f"Audit report not found: {a.audit_report}")
    audit = pd.read_csv(a.audit_report)
    needed = {"symbol", "unexpected_interval_count", "zero_volume_rows"}
    if not needed.issubset(audit.columns):
        raise SystemExit("Audit report lacks required structural columns")
    eligible = set(audit.loc[
        (audit["unexpected_interval_count"] == 0)
        & (audit["zero_volume_rows"] == 0), "symbol"
    ].astype(str))

    tables = []
    excluded = []
    for path in sorted(a.directory.glob("*_5minute.csv")):
        symbol = path.name.removeprefix("NSE_").removesuffix("_5minute.csv")
        if symbol not in eligible:
            excluded.append({"symbol": symbol, "reason": "failed structural universe audit"})
            continue
        try:
            tables.append(rows(load(path), symbol))
        except (ValueError, AssertionError) as exc:
            excluded.append({"symbol": symbol, "reason": str(exc)})

    if not tables:
        raise SystemExit("No eligible instruments remain")
    detail = pd.concat(tables, ignore_index=True)

    breadth = (
        detail.groupby(["state", "component"], as_index=False)
        .agg(
            instruments=("symbol", "nunique"),
            median_instrument_mean=("mean", "median"),
            q25_instrument_mean=("mean", lambda x: x.quantile(.25)),
            q75_instrument_mean=("mean", lambda x: x.quantile(.75)),
            positive_instrument_fraction=("mean", lambda x: (x > 0).mean()),
        )
    )

    stability = []
    detail["period"] = pd.qcut(
        detail["state"].astype(str), 1, labels=False
    )  # placeholder column removed below
    # Recompute temporal stability from raw files without using later periods.
    # Four chronological quarters are used only as descriptive subperiods.
    for path in sorted(a.directory.glob("*_5minute.csv")):
        symbol = path.name.removeprefix("NSE_").removesuffix("_5minute.csv")
        if symbol not in eligible:
            continue
        try:
            df = load(path)
        except (ValueError, AssertionError):
            continue
        period = pd.qcut(df["timestamp"].astype("int64"), 4,
                         labels=["Q1_time", "Q2_time", "Q3_time", "Q4_time"],
                         duplicates="drop")
        prior = df["close"].pct_change(fill_method=None)
        next_close = df["close"].shift(-1)
        next_open = df["open"].shift(-1)
        components = {
            "next_close_to_close": next_close / df["close"] - 1,
            "next_close_to_open": next_open / df["close"] - 1,
            "next_open_to_close": next_close / next_open - 1,
        }
        sign = pd.Series(np.where(prior > 0, "positive",
                                  np.where(prior < 0, "negative", "zero")),
                         index=df.index)
        for p, g in df.groupby(period, observed=True):
            idx = g.index
            for s in ("negative", "positive"):
                mask = sign.loc[idx] == s
                for name, series in components.items():
                    x = series.loc[idx].loc[mask].dropna()
                    stability.append({
                        "symbol": symbol,
                        "period": str(p),
                        "state": f"prior_{s}",
                        "component": name,
                        "observations": len(x),
                        "mean": x.mean(),
                        "positive_fraction": (x > 0).mean() if len(x) else np.nan,
                    })

    detail.to_csv(a.output_dir / "per_instrument_reversal_decomposition.csv", index=False)
    breadth.to_csv(a.output_dir / "reversal_decomposition_breadth.csv", index=False)
    pd.DataFrame(stability).to_csv(
        a.output_dir / "reversal_decomposition_temporal_stability.csv", index=False
    )
    pd.DataFrame(excluded).to_csv(a.output_dir / "excluded_instruments.csv", index=False)
    print(f"Included instruments: {detail['symbol'].nunique()}")
    print(f"Excluded instruments: {len(excluded)}")
    print(f"Outputs: {a.output_dir}")


if __name__ == "__main__":
    main()
