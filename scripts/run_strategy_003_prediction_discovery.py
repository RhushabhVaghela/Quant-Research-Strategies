"""Run Strategy 003 intraday prediction discovery.

This is a discovery/prediction diagnostic, not a trading-strategy backtest.
The primary target is the next 5-minute cross-sectional excess return.
The first feature set deliberately excludes signed-return mechanisms owned by
Strategies 001 and 002. Protected validation/holdout periods are not read.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd

EXPLORATORY_START = pd.Timestamp("2025-09-18")
EXPLORATORY_END = pd.Timestamp("2026-06-09 23:59:59")
VALIDATION_START = pd.Timestamp("2026-06-10")
HOLDOUT_START = pd.Timestamp("2026-08-20")

HORIZON_BARS = 1
BAR_MINUTES = 5
RIDGE_ALPHA = 1.0
QUINTILES = 5
LONG_WINDOW_BARS = 60

BASE_FEATURES = [
    "log_volume",
    "volume_change_1bar",
    "volume_z_12bar",
    "volume_z_60bar",
    "realized_vol_12bar",
    "realized_vol_60bar",
    "range_1bar",
    "range_z_60bar",
    "close_location_1bar",
    "intraday_position_60bar",
    "bars_since_session_open",
]

CONTEXT_FEATURES = [
    "market_return_1bar",
    "market_vol_60bar",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "directory",
        type=Path,
        nargs="?",
        default=Path("data/raw/strategy_002_universe"),
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("data/reports/strategy_003_prediction_discovery"),
    )
    parser.add_argument(
        "--audit-report",
        type=Path,
        default=Path("data/reports/strategy_002_universe_audit.csv"),
    )
    parser.add_argument(
        "--universe",
        type=Path,
        default=Path("research/universe_candidates.csv"),
    )
    return parser.parse_args()


def load_candidates(path: Path) -> pd.DataFrame:
    frame = pd.read_csv(path)
    required = {"symbol", "category"}
    missing = required.difference(frame.columns)
    if missing:
        raise ValueError(f"{path}: missing columns {sorted(missing)}")
    return frame


def load_audit(path: Path) -> pd.DataFrame:
    frame = pd.read_csv(path)
    required = {"symbol", "unexpected_interval_count", "zero_volume_rows"}
    missing = required.difference(frame.columns)
    if missing:
        raise ValueError(f"{path}: missing columns {sorted(missing)}")
    return frame


def load_intraday(path: Path) -> pd.DataFrame:
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

    for col in ("open", "high", "low", "close", "volume"):
        df[col] = pd.to_numeric(df[col], errors="coerce")

    if df[["open", "high", "low", "close"]].isna().any().any():
        raise ValueError(f"{path}: missing OHLC values")
    if (df[["open", "high", "low", "close"]] <= 0).any().any():
        raise ValueError(f"{path}: non-positive OHLC values")
    if df["volume"].isna().any() or (df["volume"] < 0).any():
        raise ValueError(f"{path}: invalid volume")

    return df


def session_bar_features(intraday: pd.DataFrame) -> pd.DataFrame:
    work = intraday.copy()
    work["date"] = (
        work["timestamp"].dt.tz_convert("Asia/Kolkata").dt.normalize().dt.tz_localize(None)
    )
    work["bar_in_session"] = work.groupby("date").cumcount()
    work["bars_since_session_open"] = work["bar_in_session"].astype(float)

    close = work["close"]
    volume = work["volume"].astype(float)
    log_volume = np.log1p(volume)
    ret1 = work.groupby("date")["close"].pct_change()

    work["log_volume"] = log_volume
    work["volume_change_1bar"] = work.groupby("date")["volume"].pct_change()
    work["volume_z_12bar"] = work.groupby("date")["log_volume"].transform(
        lambda s: (s - s.rolling(12).mean()) / s.rolling(12).std(ddof=1).replace(0, np.nan)
    )
    work["volume_z_60bar"] = work.groupby("date")["log_volume"].transform(
        lambda s: (s - s.rolling(LONG_WINDOW_BARS).mean()) / s.rolling(LONG_WINDOW_BARS).std(ddof=1).replace(0, np.nan)
    )
    work["realized_vol_12bar"] = ret1.groupby(work["date"]).transform(
        lambda s: s.rolling(12).std(ddof=1)
    )
    work["realized_vol_60bar"] = ret1.groupby(work["date"]).transform(
        lambda s: s.rolling(LONG_WINDOW_BARS).std(ddof=1)
    )
    work["range_1bar"] = (work["high"] - work["low"]) / close
    range_mean = work.groupby("date")["range_1bar"].transform(
        lambda s: s.rolling(LONG_WINDOW_BARS).mean()
    )
    range_std = work.groupby("date")["range_1bar"].transform(
        lambda s: s.rolling(LONG_WINDOW_BARS).std(ddof=1)
    )
    work["range_z_60bar"] = (
        (work["range_1bar"] - range_mean) / range_std.replace(0, np.nan)
    )
    work["close_location_1bar"] = (
        (close - work["low"]) / (work["high"] - work["low"]).replace(0, np.nan)
    )
    work["intraday_position_60bar"] = (
        close / work.groupby("date")["close"].transform(lambda s: s.rolling(LONG_WINDOW_BARS).mean()) - 1.0
    )
    return work


def add_market_context(stock: pd.DataFrame, market: pd.DataFrame) -> pd.DataFrame:
    market_work = session_bar_features(market)
    market_work["market_return_1bar"] = market_work.groupby("date")["close"].pct_change()
    market_work["market_vol_60bar"] = market_work.groupby("date")["market_return_1bar"].transform(
        lambda s: s.rolling(LONG_WINDOW_BARS).std(ddof=1)
    )
    context = market_work[["timestamp", "market_return_1bar", "market_vol_60bar"]].drop_duplicates("timestamp")
    return stock.merge(context, on="timestamp", how="left", validate="one_to_one")


def build_symbol_panel(frame: pd.DataFrame, market: pd.DataFrame) -> pd.DataFrame:
    out = session_bar_features(frame)
    out = add_market_context(out, market)
    out["future_return_1bar"] = (
        out.groupby("date")["close"].shift(-HORIZON_BARS) / out["close"] - 1.0
    )
    return out


def build_panel(frames: dict[str, pd.DataFrame], market: pd.DataFrame) -> pd.DataFrame:
    parts = []
    for symbol, frame in frames.items():
        enriched = build_symbol_panel(frame, market)
        enriched["symbol"] = symbol
        parts.append(enriched)
    panel = pd.concat(parts, ignore_index=True).sort_values(["timestamp", "symbol"])
    future_mean = panel.groupby("timestamp")["future_return_1bar"].transform("mean")
    panel["target_excess_1bar"] = panel["future_return_1bar"] - future_mean

    for col in BASE_FEATURES + CONTEXT_FEATURES:
        grouped = panel.groupby("timestamp")[col]
        panel[f"{col}_rank"] = grouped.rank(pct=True, method="average")
        mean = grouped.transform("mean")
        std = grouped.transform("std")
        panel[f"{col}_cs_z"] = (panel[col] - mean) / std.replace(0, np.nan)
    return panel.sort_values(["timestamp", "symbol"]).reset_index(drop=True)


def locked_exploratory_slice(panel: pd.DataFrame) -> pd.DataFrame:
    out = panel[
        (panel["date"] >= EXPLORATORY_START)
        & (panel["date"] <= EXPLORATORY_END)
    ].copy()
    if out.empty:
        raise ValueError("No observations remain in the locked exploratory window")
    if out["date"].max() >= VALIDATION_START:
        raise AssertionError("Exploratory panel crossed into validation")
    if out["date"].max() >= HOLDOUT_START:
        raise AssertionError("Exploratory panel crossed into holdout")
    return out


def feature_columns(panel: pd.DataFrame) -> list[str]:
    derived = [
        col for col in panel.columns
        if col.endswith("_rank") or col.endswith("_cs_z")
    ]
    return list(dict.fromkeys(BASE_FEATURES + CONTEXT_FEATURES + derived))


def univariate_ic(panel: pd.DataFrame, features: list[str]) -> pd.DataFrame:
    rows = []
    target = "target_excess_1bar"
    work_all = panel[["timestamp", "date", target] + features].dropna()

    for feature in features:
        daily_pearson = []
        daily_rank = []
        for _, day in work_all.groupby("date"):
            timestamp_ics = []
            timestamp_rank_ics = []
            for _, group in day.groupby("timestamp"):
                if len(group) < 5:
                    continue
                timestamp_ics.append(group[feature].corr(group[target]))
                timestamp_rank_ics.append(
                    group[feature].rank(method="average").corr(
                        group[target].rank(method="average")
                    )
                )
            if timestamp_ics:
                daily_pearson.append(np.nanmean(timestamp_ics))
                daily_rank.append(np.nanmean(timestamp_rank_ics))
        if not daily_pearson:
            continue
        pearson = np.asarray(daily_pearson, dtype=float)
        rank = np.asarray(daily_rank, dtype=float)
        std = np.nanstd(pearson, ddof=1) if len(pearson) > 1 else np.nan
        rows.append({
            "feature": feature,
            "usable_dates": int(len(pearson)),
            "mean_ic": float(np.nanmean(pearson)),
            "ic_std": float(std),
            "ic_ir": float(np.nanmean(pearson) / std * np.sqrt(len(pearson)))
            if np.isfinite(std) and std > 0 else np.nan,
            "positive_ic_date_fraction": float(np.nanmean(pearson > 0)),
            "mean_rank_ic": float(np.nanmean(rank)),
            "rank_ic_std": float(np.nanstd(rank, ddof=1)) if len(rank) > 1 else np.nan,
        })
    if not rows:
        raise ValueError(
            "No usable univariate IC observations remain. "
            "Check feature warm-up windows and session length."
        )
    return pd.DataFrame(rows).sort_values(
        ["mean_rank_ic", "mean_ic"], ascending=[False, False]
    )


def chronological_splits(timestamps: pd.Series | pd.DatetimeIndex) -> dict[str, pd.Timestamp]:
    unique = pd.DatetimeIndex(sorted(pd.DatetimeIndex(timestamps).unique()))
    if len(unique) < 300:
        raise ValueError("Too few intraday decision timestamps for the fixed internal split")
    train_end_i = int(len(unique) * 0.60) - 1
    valid_end_i = int(len(unique) * 0.80) - 1
    return {
        "train_start": unique[0],
        "train_end": unique[train_end_i],
        "validation_start": unique[train_end_i + 1],
        "validation_end": unique[valid_end_i],
        "test_start": unique[valid_end_i + 1],
        "test_end": unique[-1],
    }


def purged_chronological_splits(
    timestamps: pd.Series | pd.DatetimeIndex,
    horizon_bars: int = HORIZON_BARS,
) -> dict[str, pd.Timestamp]:
    unique = pd.DatetimeIndex(sorted(pd.DatetimeIndex(timestamps).unique()))
    splits = chronological_splits(unique)
    train_end_idx = unique.get_loc(splits["train_end"])
    valid_end_idx = unique.get_loc(splits["validation_end"])
    if train_end_idx - horizon_bars < 0:
        raise ValueError("Not enough timestamps for horizon-aware train purge")
    if valid_end_idx - horizon_bars < unique.get_loc(splits["validation_start"]):
        raise ValueError("Not enough timestamps for horizon-aware validation purge")
    splits["train_end_unpurged"] = splits["train_end"]
    splits["validation_end_unpurged"] = splits["validation_end"]
    splits["train_end"] = unique[train_end_idx - horizon_bars]
    splits["validation_end"] = unique[valid_end_idx - horizon_bars]
    splits["train_purge_count"] = horizon_bars
    splits["validation_purge_count"] = horizon_bars
    splits["purge_unit"] = "decision_timestamp"
    splits["horizon_bars"] = horizon_bars
    return splits


def fit_linear(
    x: np.ndarray,
    y: np.ndarray,
    ridge_alpha: float | None = None,
) -> np.ndarray:
    x_aug = np.column_stack([np.ones(len(x)), x])
    if ridge_alpha is None:
        beta, *_ = np.linalg.lstsq(x_aug, y, rcond=None)
        return beta

    penalty = np.eye(x_aug.shape[1])
    penalty[0, 0] = 0.0
    lhs = x_aug.T @ x_aug + ridge_alpha * penalty
    rhs = x_aug.T @ y
    return np.linalg.solve(lhs, rhs)


def fit_transform(
    train: pd.DataFrame,
    other: pd.DataFrame,
    features: list[str],
) -> tuple[np.ndarray, np.ndarray, list[str]]:
    means = train[features].mean()
    stds = train[features].std(ddof=1)
    keep = stds[(stds > 0) & stds.notna()].index.tolist()

    if len(keep) < 3:
        raise ValueError("Too few non-constant features after training fit")

    train_x = ((train[keep] - means[keep]) / stds[keep]).fillna(0.0).to_numpy()
    other_x = ((other[keep] - means[keep]) / stds[keep]).fillna(0.0).to_numpy()
    return train_x, other_x, keep


def score_predictions(
    frame: pd.DataFrame,
    prediction: pd.Series,
    target_col: str,
) -> dict[str, float]:
    work = frame[["timestamp", target_col]].copy()
    work["prediction"] = prediction.to_numpy()

    timestamp_ic = []
    timestamp_rank_ic = []
    spreads = []

    for _, group in work.dropna().groupby("timestamp"):
        if len(group) < 10:
            continue

        prediction = group["prediction"]
        target = group[target_col]

        # Pearson correlation is undefined for a constant prediction (as in
        # the zero baseline). Check variance explicitly so the baseline does
        # not emit NumPy warnings or depend on scipy through pandas.corr().
        if prediction.nunique(dropna=True) > 1 and target.nunique(dropna=True) > 1:
            ic_value = prediction.corr(target)
            prediction_rank = prediction.rank(method="average")
            target_rank = target.rank(method="average")
            rank_ic_value = prediction_rank.corr(target_rank)

            if np.isfinite(ic_value):
                timestamp_ic.append(ic_value)
            if np.isfinite(rank_ic_value):
                timestamp_rank_ic.append(rank_ic_value)

        rank = prediction.rank(method="first", pct=True)
        high = group.loc[rank > 0.8, target_col].mean()
        low = group.loc[rank <= 0.2, target_col].mean()
        spreads.append(high - low)

    if not timestamp_ic:
        return {
            "usable_timestamps": 0,
            "mean_ic": np.nan,
            "mean_rank_ic": np.nan,
            "ic_ir": np.nan,
            "positive_ic_fraction": np.nan,
            "mean_top_bottom_spread_bps": np.nan,
        }

    ic = np.asarray(timestamp_ic, dtype=float)
    rank_ic = np.asarray(timestamp_rank_ic, dtype=float)
    spread = np.asarray(spreads, dtype=float)
    ic_std = np.nanstd(ic, ddof=1) if len(ic) > 1 else np.nan

    return {
        "usable_timestamps": int(len(ic)),
        "mean_ic": float(np.nanmean(ic)),
        "mean_rank_ic": float(np.nanmean(rank_ic)),
        # Descriptive only: adjacent 5-minute timestamps are dependent.
        "ic_ir": float(np.nanmean(ic) / ic_std * np.sqrt(len(ic)))
        if np.isfinite(ic_std) and ic_std > 0
        else np.nan,
        "positive_ic_fraction": float(np.nanmean(ic > 0)),
        "mean_top_bottom_spread_bps": float(np.nanmean(spread) * 1e4),
    }


def model_diagnostics(
    panel: pd.DataFrame,
    features: list[str],
) -> tuple[pd.DataFrame, pd.DataFrame]:
    model_rows = []
    quintile_rows = []
    target = "target_excess_1bar"

    base = panel[["timestamp", "symbol", target] + features].dropna().copy()
    splits = purged_chronological_splits(base["timestamp"])

    train = base[
        (base["timestamp"] >= splits["train_start"])
        & (base["timestamp"] <= splits["train_end"])
    ].copy()
    validation = base[
        (base["timestamp"] >= splits["validation_start"])
        & (base["timestamp"] <= splits["validation_end"])
    ].copy()
    test = base[
        (base["timestamp"] >= splits["test_start"])
        & (base["timestamp"] <= splits["test_end"])
    ].copy()

    train_x, valid_x, kept = fit_transform(train, validation, features)
    _, test_x, _ = fit_transform(train, test, kept)
    y_train = train[target].to_numpy()

    model_specs = [("ols", None), ("ridge_fixed_alpha", RIDGE_ALPHA)]

    for split_name, frame in (("validation", validation), ("development_test", test)):
        zero = pd.Series(0.0, index=frame.index)
        model_rows.append(
            {
                "horizon_bars": HORIZON_BARS,
                "horizon_minutes": HORIZON_BARS * BAR_MINUTES,
                "model": "zero_baseline",
                "split": split_name,
                "purged": True,
                **score_predictions(frame, zero, target),
            }
        )

    for model_name, alpha in model_specs:
        beta = fit_linear(train_x, y_train, ridge_alpha=alpha)
        valid_pred = pd.Series(
            np.column_stack([np.ones(len(valid_x)), valid_x]) @ beta,
            index=validation.index,
        )
        test_pred = pd.Series(
            np.column_stack([np.ones(len(test_x)), test_x]) @ beta,
            index=test.index,
        )

        for split_name, frame, prediction in (
            ("validation", validation, valid_pred),
            ("development_test", test, test_pred),
        ):
            model_rows.append(
                {
                    "horizon_bars": HORIZON_BARS,
                    "horizon_minutes": HORIZON_BARS * BAR_MINUTES,
                    "model": model_name,
                    "split": split_name,
                    "purged": True,
                    **score_predictions(frame, prediction, target),
                }
            )

            if split_name == "development_test":
                diagnostic = frame[["timestamp", "symbol", target]].copy()
                diagnostic["prediction"] = prediction.to_numpy()
                diagnostic["prediction_pct_rank"] = diagnostic.groupby(
                    "timestamp"
                )["prediction"].rank(method="first", pct=True)
                q = (
                    diagnostic.groupby("timestamp")
                    .apply(
                        lambda g: pd.Series(
                            {
                                "high_q_bps": g.loc[
                                    g["prediction_pct_rank"] > 0.8, target
                                ].mean()
                                * 1e4,
                                "low_q_bps": g.loc[
                                    g["prediction_pct_rank"] <= 0.2, target
                                ].mean()
                                * 1e4,
                            }
                        ),
                        include_groups=False,
                    )
                    .reset_index()
                )
                q["spread_bps"] = q["high_q_bps"] - q["low_q_bps"]
                q["horizon_bars"] = HORIZON_BARS
                q["horizon_minutes"] = HORIZON_BARS * BAR_MINUTES
                q["model"] = model_name
                quintile_rows.extend(q.to_dict("records"))

    return pd.DataFrame(model_rows), pd.DataFrame(quintile_rows)


def feature_metadata(features: list[str]) -> pd.DataFrame:
    descriptions = {
        "log_volume": "Log(1 + current 5-minute volume)",
        "volume_change_1bar": "Current 5-minute volume change versus previous bar",
        "volume_z_12bar": "Trailing 12-bar z-score of log volume within session",
        "volume_z_60bar": "Trailing 60-bar z-score of log volume within session",
        "realized_vol_12bar": "Trailing 12-bar realized volatility within session",
        "realized_vol_60bar": "Trailing 60-bar realized volatility within session",
        "range_1bar": "Current 5-minute high-low range divided by close",
        "range_z_60bar": "Current range relative to trailing 60-bar range distribution",
        "close_location_1bar": "Current close location inside the current 5-minute bar",
        "intraday_position_60bar": "Current close relative to trailing 60-bar mean close",
        "bars_since_session_open": "Bars elapsed since session open",
        "market_return_1bar": "NIFTYBEES return over the current 5-minute interval",
        "market_vol_60bar": "Trailing 60-bar realized volatility of NIFTYBEES",
    }
    rows = []
    for feature in features:
        base = feature
        transform = "raw intraday feature"
        if feature.endswith("_rank"):
            base = feature[:-5]
            transform = "cross-sectional percentile rank"
        elif feature.endswith("_cs_z"):
            base = feature[:-5]
            transform = "cross-sectional z-score"
        rows.append({
            "feature": feature,
            "base_feature": base,
            "transform": transform,
            "description": descriptions.get(base, "Derived cross-sectional feature"),
        })
    return pd.DataFrame(rows)


def main() -> None:
    args = parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)

    candidates = load_candidates(args.universe)
    audit = load_audit(args.audit_report)

    eligible = set(
        audit.loc[
            (audit["unexpected_interval_count"] == 0)
            & (audit["zero_volume_rows"] == 0),
            "symbol",
        ].astype(str)
    )

    equity_categories = {"large_cap_equity", "liquid_auto"}
    equity_symbols = set(
        candidates.loc[
            candidates["category"].isin(equity_categories), "symbol"
        ].astype(str)
    ) & eligible

    if "NIFTYBEES" not in eligible:
        raise SystemExit(
            "NIFTYBEES is required as the market reference but is not structurally eligible"
        )

    frames = {}
    for symbol in sorted(equity_symbols):
        path = args.directory / f"NSE_{symbol}_5minute.csv"
        if not path.exists():
            raise SystemExit(f"Missing required equity data file: {path}")
        frames[symbol] = load_intraday(path)

    market_path = args.directory / "NSE_NIFTYBEES_5minute.csv"
    if not market_path.exists():
        raise SystemExit(f"Missing required market proxy data file: {market_path}")
    market = load_intraday(market_path)

    panel = locked_exploratory_slice(build_panel(frames, market))
    features = feature_columns(panel)

    ic = univariate_ic(panel, features)
    models, quintiles = model_diagnostics(panel, features)
    metadata = feature_metadata(features)

    ic.to_csv(args.output_dir / "feature_ic.csv", index=False)
    models.to_csv(args.output_dir / "model_metrics.csv", index=False)
    quintiles.to_csv(args.output_dir / "quintile_diagnostics.csv", index=False)
    metadata.to_csv(args.output_dir / "feature_metadata.csv", index=False)

    splits = purged_chronological_splits(panel["timestamp"])
    manifest = {
        "strategy_id": "003",
        "analysis": "intraday_prediction_discovery",
        "status": "discovery_only",
        "research_scope": "intraday_only",
        "decision_bar_minutes": BAR_MINUTES,
        "horizon_bars": HORIZON_BARS,
        "horizon_minutes": HORIZON_BARS * BAR_MINUTES,
        "exploratory_start": str(EXPLORATORY_START.date()),
        "exploratory_end": str(EXPLORATORY_END.date()),
        "validation_start": str(VALIDATION_START.date()),
        "holdout_start": str(HOLDOUT_START.date()),
        "equity_symbols": sorted(frames),
        "market_proxy": "NIFTYBEES",
        "feature_count": len(features),
        "features_include_signed_return_direction": False,
        "excluded_mechanisms": [
            "Strategy 001 short-horizon continuation",
            "Strategy 002 short-horizon cross-sectional residual reversal",
        ],
        "models": ["zero_baseline", "ols", "ridge_fixed_alpha"],
        "ridge_alpha": RIDGE_ALPHA,
        "quintiles": QUINTILES,
        "internal_split": {
            k: str(v) if isinstance(v, pd.Timestamp) else v
            for k, v in splits.items()
        },
        "holdout_used": False,
        "strategy_pnl_calculated": False,
        "parameter_search": False,
        "dependency_warning": (
            "5-minute observations are serially dependent; timestamp-level IC IR "
            "is descriptive only."
        ),
    }
    (args.output_dir / "run_manifest.json").write_text(
        json.dumps(manifest, indent=2, default=str), encoding="utf-8"
    )

    print("Strategy 003 intraday prediction discovery complete")
    print(f"Eligible equity symbols: {len(frames)}")
    print(f"Feature count: {len(features)}")
    print(f"Horizon: {HORIZON_BARS} bar ({HORIZON_BARS * BAR_MINUTES} minutes)")
    print(
        f"Exploratory window: {EXPLORATORY_START.date()} -> "
        f"{EXPLORATORY_END.date()}"
    )
    print(f"Protected validation starts: {VALIDATION_START.date()}")
    print(f"Protected holdout starts: {HOLDOUT_START.date()}")
    print(f"Outputs: {args.output_dir}")


if __name__ == "__main__":
    main()
