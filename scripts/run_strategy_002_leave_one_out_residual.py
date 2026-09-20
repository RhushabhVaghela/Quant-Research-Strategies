"""Characterize Strategy 002 residuals with leave-one-out market returns and bar-boundary decomposition."""
from __future__ import annotations
import argparse
from pathlib import Path
import numpy as np
import pandas as pd

START = pd.Timestamp("2025-09-18", tz="Asia/Kolkata")
END = pd.Timestamp("2026-06-09 23:59:59", tz="Asia/Kolkata")
VALIDATION_START = pd.Timestamp("2026-06-10", tz="Asia/Kolkata")
HORIZONS = (1, 2, 3, 6, 12)
STABILITY_LAGS = (1, 2, 3, 6, 12, 24)

def parse_args():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("directory", type=Path)
    p.add_argument("--audit-report", type=Path, default=Path("data/reports/strategy_002_universe_audit.csv"))
    p.add_argument("--output-dir", type=Path, default=Path("data/reports/strategy_002_leave_one_out_residual"))
    return p.parse_args()

def load(path: Path) -> pd.DataFrame:
    df = pd.read_csv(path, parse_dates=["timestamp"])
    required = {"timestamp", "open", "high", "low", "close", "volume"}
    if not required.issubset(df.columns):
        raise ValueError(f"{path}: missing columns")
    ts = pd.DatetimeIndex(df["timestamp"])
    if ts.tz is None:
        raise ValueError(f"{path}: timestamps must be timezone-aware")
    df["timestamp"] = ts.tz_convert("Asia/Kolkata")
    df = df.sort_values("timestamp")
    if df["timestamp"].duplicated().any() or not df["timestamp"].is_monotonic_increasing:
        raise ValueError(f"{path}: invalid timestamps")
    for c in ["open", "high", "low", "close", "volume"]:
        df[c] = pd.to_numeric(df[c], errors="coerce")
    if df[["open", "high", "low", "close"]].isna().any().any() or (df[["open", "high", "low", "close"]] <= 0).any().any():
        raise ValueError(f"{path}: invalid OHLC")
    if df["volume"].isna().any() or (df["volume"] < 0).any():
        raise ValueError(f"{path}: invalid volume")
    out = df.loc[(df.timestamp >= START) & (df.timestamp <= END), ["timestamp", "open", "close"]].copy()
    if out.empty:
        raise ValueError(f"{path}: no exploratory observations")
    if out.timestamp.max() >= VALIDATION_START:
        raise AssertionError(f"{path}: crossed validation boundary")
    out["close_to_close"] = out["close"].pct_change(fill_method=None)
    out["close_to_open"] = out["open"] / out["close"].shift(1) - 1.0
    out["open_to_close"] = out["close"] / out["open"] - 1.0
    return out.set_index("timestamp")[["close_to_close", "close_to_open", "open_to_close"]]

def leave_one_out(panel: pd.DataFrame, minimum_others: int = 3) -> pd.DataFrame:
    counts = panel.notna().sum(axis=1)
    sums = panel.sum(axis=1, skipna=True)
    out = pd.DataFrame(index=panel.index, columns=panel.columns, dtype=float)
    for symbol in panel.columns:
        others = counts - panel[symbol].notna().astype(int)
        loo = (sums - panel[symbol]) / others.where(others >= minimum_others)
        out[symbol] = panel[symbol] - loo
    return out

def breadth(detail: pd.DataFrame) -> pd.DataFrame:
    return detail.groupby(["condition", "component", "horizon_bars"], as_index=False).agg(
        instruments=("symbol", "nunique"),
        median_instrument_mean=("mean", "median"),
        q25_instrument_mean=("mean", lambda x: x.quantile(.25)),
        q75_instrument_mean=("mean", lambda x: x.quantile(.75)),
        positive_instrument_fraction=("mean", lambda x: (x > 0).mean()),
    )

def main():
    a = parse_args()
    a.output_dir.mkdir(parents=True, exist_ok=True)
    audit = pd.read_csv(a.audit_report)
    eligible = set(audit.loc[
        (audit.unexpected_interval_count == 0) & (audit.zero_volume_rows == 0), "symbol"
    ].astype(str))
    series = {}
    excluded = []
    for path in sorted(a.directory.glob("*_5minute.csv")):
        symbol = path.name.removeprefix("NSE_").removesuffix("_5minute.csv")
        if symbol not in eligible:
            excluded.append({"symbol": symbol, "reason": "failed structural universe audit"})
            continue
        try:
            series[symbol] = load(path)
        except (ValueError, AssertionError) as exc:
            excluded.append({"symbol": symbol, "reason": str(exc)})
    if len(series) < 4:
        raise SystemExit("Need at least four eligible instruments")
    components = ["close_to_close", "close_to_open", "open_to_close"]
    panels = {c: pd.DataFrame({s: d[c] for s, d in series.items()}).sort_index() for c in components}
    residuals = {c: leave_one_out(panels[c]) for c in components}

    rows = []
    prior = residuals["close_to_close"]
    for h in HORIZONS:
        future = residuals["close_to_close"].shift(-h)
        for condition, mask in {"prior_negative": prior < 0, "prior_positive": prior > 0}.items():
            vals = future.where(mask)
            for symbol in prior.columns:
                z = vals[symbol].dropna()
                rows.append({"symbol": symbol, "condition": condition, "component": "close_to_close",
                             "horizon_bars": h, "observations": len(z), "mean": z.mean(),
                             "median": z.median(), "positive_fraction": (z > 0).mean() if len(z) else np.nan})
        q = pd.DataFrame({
            c: pd.qcut(prior[c].abs().dropna(), 4, labels=["Q1", "Q2", "Q3", "Q4"], duplicates="drop").reindex(prior.index)
            for c in prior.columns
        })
        for sign, signmask in {"negative": prior < 0, "positive": prior > 0}.items():
            for quart in ["Q1", "Q2", "Q3", "Q4"]:
                vals = future.where(signmask & (q == quart))
                for symbol in prior.columns:
                    z = vals[symbol].dropna()
                    rows.append({"symbol": symbol, "condition": f"prior_{sign}_abs_{quart}",
                                 "component": "close_to_close", "horizon_bars": h,
                                 "observations": len(z), "mean": z.mean(), "median": z.median(),
                                 "positive_fraction": (z > 0).mean() if len(z) else np.nan})

    for component in ["close_to_open", "open_to_close"]:
        future = residuals[component].shift(-1)
        for condition, mask in {"prior_negative": prior < 0, "prior_positive": prior > 0}.items():
            vals = future.where(mask)
            for symbol in prior.columns:
                z = vals[symbol].dropna()
                rows.append({"symbol": symbol, "condition": condition, "component": component,
                             "horizon_bars": 1, "observations": len(z), "mean": z.mean(),
                             "median": z.median(), "positive_fraction": (z > 0).mean() if len(z) else np.nan})

    detail = pd.DataFrame(rows)
    stab = []
    time_index = pd.Series(prior.index.astype("int64"), index=prior.index)
    periods = pd.qcut(time_index, 4, labels=["Q1_time", "Q2_time", "Q3_time", "Q4_time"], duplicates="drop")
    for period in periods.cat.categories:
        sub = prior.loc[periods == period]
        for lag in STABILITY_LAGS:
            for symbol in prior.columns:
                x = sub[symbol].dropna()
                stab.append({"period": str(period), "symbol": symbol, "lag": lag,
                             "residual_return_acf": x.autocorr(lag=lag) if len(x) > lag else np.nan})

    detail.to_csv(a.output_dir / "per_instrument_leave_one_out_residuals.csv", index=False)
    breadth(detail).to_csv(a.output_dir / "leave_one_out_residual_breadth.csv", index=False)
    pd.DataFrame(stab).to_csv(a.output_dir / "leave_one_out_residual_temporal_stability.csv", index=False)
    pd.DataFrame(excluded).to_csv(a.output_dir / "excluded_instruments.csv", index=False)
    pd.Series({
        "exploratory_start": str(START), "exploratory_end": str(END),
        "validation_start": str(VALIDATION_START), "minimum_leave_one_out_others": 3,
        "included_instruments": sorted(series), "excluded_instruments": excluded,
        "holdout_used": False, "strategy_pnl_calculated": False
    }, dtype="object").to_json(a.output_dir / "run_manifest.json", indent=2)
    print(f"Included instruments: {len(series)}")
    print(f"Excluded instruments: {len(excluded)}")
    print(f"Outputs: {a.output_dir}")

if __name__ == "__main__":
    main()
