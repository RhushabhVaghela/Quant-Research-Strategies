"""Run the locked first-pass Strategy 003 prediction-discovery experiment.

This is a discovery/prediction diagnostic, not a trading-strategy backtest.
It uses only the Strategy 003 exploratory window and cannot read the protected
validation or final holdout periods.

The first model ladder is zero-baseline -> OLS -> fixed-penalty Ridge, with no
hyperparameter search.
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

HORIZONS = (1, 5)
RIDGE_ALPHA = 1.0
QUINTILES = 5


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


def daily_ohlcv(df: pd.DataFrame) -> pd.DataFrame:
    work = df.copy()
    work["date"] = work["timestamp"].dt.tz_convert("Asia/Kolkata").dt.normalize()
    return (
        work.groupby("date", sort=True)
        .agg(
            open=("open", "first"),
            high=("high", "max"),
            low=("low", "min"),
            close=("close", "last"),
            volume=("volume", "sum"),
            bars=("close", "count"),
        )
        .reset_index()
    )


def trailing_features(daily: pd.DataFrame, market: pd.DataFrame) -> pd.DataFrame:
    out = daily.copy()
    close = out["close"]
    ret1 = close.pct_change()
    ret5 = close.pct_change(5)
    ret20 = close.pct_change(20)

    out["ret_1d"] = ret1
    out["ret_5d"] = ret5
    out["ret_20d"] = ret20
    out["ma_gap_5d"] = close / close.rolling(5).mean() - 1.0
    out["ma_gap_20d"] = close / close.rolling(20).mean() - 1.0
    out["vol_5d"] = ret1.rolling(5).std(ddof=1) * np.sqrt(252.0)
    out["vol_20d"] = ret1.rolling(20).std(ddof=1) * np.sqrt(252.0)
    out["range_1d"] = (out["high"] - out["low"]) / close

    log_volume = np.log1p(out["volume"])
    out["log_volume"] = log_volume
    out["volume_mean_5d"] = log_volume.rolling(5).mean()
    volume_mean_20 = log_volume.rolling(20).mean()
    volume_std_20 = log_volume.rolling(20).std(ddof=1)
    out["volume_z_20d"] = (
        (log_volume - volume_mean_20) / volume_std_20.replace(0, np.nan)
    )

    market_close = market.set_index("date")["close"].reindex(out["date"]).ffill()
    market_ret1 = market_close.pct_change()
    market_ret5 = market_close.pct_change(5)
    market_ret20 = market_close.pct_change(20)

    out["market_rel_1d"] = ret1.to_numpy() - market_ret1.to_numpy()
    out["market_rel_5d"] = ret5.to_numpy() - market_ret5.to_numpy()
    out["market_rel_20d"] = ret20.to_numpy() - market_ret20.to_numpy()

    # Align the market-return series explicitly to the stock's daily index.
    # Mixing a Series indexed by stock dates with a market Series carrying its
    # own index can make pandas align by label and produce a longer result than
    # the stock frame. The beta feature must have exactly one value per stock date.
    market_ret1_aligned = market_ret1.reindex(out["date"]).set_axis(out.index)
    cov20 = ret1.rolling(20).cov(market_ret1_aligned)
    var20 = market_ret1_aligned.rolling(20).var()
    out["market_beta_20d"] = (
        cov20 / var20.replace(0, np.nan)
    ).to_numpy()

    return out


def build_panel(
    frames: dict[str, pd.DataFrame],
    market: pd.DataFrame,
) -> pd.DataFrame:
    parts = []
    for symbol, frame in frames.items():
        enriched = trailing_features(daily_ohlcv(frame), market)
        enriched["symbol"] = symbol
        parts.append(enriched)

    panel = pd.concat(parts, ignore_index=True).sort_values(["date", "symbol"])

    base_features = [
        "ret_1d",
        "ret_5d",
        "ret_20d",
        "ma_gap_5d",
        "ma_gap_20d",
        "vol_5d",
        "vol_20d",
        "range_1d",
        "log_volume",
        "volume_mean_5d",
        "volume_z_20d",
        "market_rel_1d",
        "market_rel_5d",
        "market_rel_20d",
        "market_beta_20d",
    ]

    for col in base_features:
        grouped = panel.groupby("date")[col]
        panel[f"{col}_rank"] = grouped.rank(pct=True, method="average")
        mean = grouped.transform("mean")
        std = grouped.transform("std")
        panel[f"{col}_cs_z"] = (panel[col] - mean) / std.replace(0, np.nan)

    market_daily = market.set_index("date")
    market_ret = market_daily["close"].pct_change()
    market_vol = market_ret.rolling(20).std(ddof=1) * np.sqrt(252.0)
    panel["market_return_1d"] = panel["date"].map(market_ret)
    panel["market_vol_20d"] = panel["date"].map(market_vol)

    return panel


def add_targets(panel: pd.DataFrame) -> pd.DataFrame:
    parts = []
    for _, group in panel.groupby("symbol", sort=False):
        g = group.sort_values("date").copy()
        for horizon in HORIZONS:
            g[f"future_return_{horizon}d"] = (
                g["close"].shift(-horizon) / g["close"] - 1.0
            )
        parts.append(g)

    out = pd.concat(parts, ignore_index=True)

    for horizon in HORIZONS:
        target = f"future_return_{horizon}d"
        future_mean = out.groupby("date")[target].transform("mean")
        out[f"target_excess_{horizon}d"] = out[target] - future_mean

    return out.sort_values(["date", "symbol"]).reset_index(drop=True)


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
    base = [
        "ret_1d",
        "ret_5d",
        "ret_20d",
        "ma_gap_5d",
        "ma_gap_20d",
        "vol_5d",
        "vol_20d",
        "range_1d",
        "log_volume",
        "volume_mean_5d",
        "volume_z_20d",
        "market_rel_1d",
        "market_rel_5d",
        "market_rel_20d",
        "market_beta_20d",
    ]
    derived = [
        col for col in panel.columns
        if col.endswith("_rank") or col.endswith("_cs_z")
    ]
    return list(dict.fromkeys(base + derived))


def univariate_ic(panel: pd.DataFrame, features: list[str]) -> pd.DataFrame:
    rows = []
    for horizon in HORIZONS:
        target = f"target_excess_{horizon}d"
        for feature in features:
            daily_pearson = []
            daily_rank = []

            work = panel[["date", feature, target]].dropna()
            for _, group in work.groupby("date"):
                if len(group) < 5:
                    continue
                daily_pearson.append(group[feature].corr(group[target]))
                daily_rank.append(group[feature].corr(group[target], method="spearman"))

            if not daily_pearson:
                continue

            pearson = np.asarray(daily_pearson, dtype=float)
            rank = np.asarray(daily_rank, dtype=float)
            std = np.nanstd(pearson, ddof=1) if len(pearson) > 1 else np.nan

            rows.append(
                {
                    "horizon_days": horizon,
                    "feature": feature,
                    "usable_dates": int(len(pearson)),
                    "mean_ic": float(np.nanmean(pearson)),
                    "ic_std": float(std),
                    "ic_ir": float(np.nanmean(pearson) / std * np.sqrt(len(pearson)))
                    if np.isfinite(std) and std > 0
                    else np.nan,
                    "positive_ic_date_fraction": float(np.nanmean(pearson > 0)),
                    "mean_rank_ic": float(np.nanmean(rank)),
                    "rank_ic_std": float(np.nanstd(rank, ddof=1))
                    if len(rank) > 1
                    else np.nan,
                }
            )

    return pd.DataFrame(rows).sort_values(
        ["horizon_days", "mean_rank_ic"], ascending=[True, False]
    )


def chronological_splits(dates: pd.Series | pd.DatetimeIndex) -> dict[str, pd.Timestamp]:
    unique = pd.DatetimeIndex(sorted(pd.DatetimeIndex(dates).unique()))
    if len(unique) < 30:
        raise ValueError("Too few decision dates for the fixed internal split")

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
    work = frame[["date", target_col]].copy()
    work["prediction"] = prediction.to_numpy()

    daily_ic = []
    daily_rank_ic = []
    spreads = []

    for _, group in work.dropna().groupby("date"):
        if len(group) < 10:
            continue

        daily_ic.append(group["prediction"].corr(group[target_col]))
        daily_rank_ic.append(
            group["prediction"].corr(group[target_col], method="spearman")
        )

        rank = group["prediction"].rank(method="first", pct=True)
        high = group.loc[rank > 0.8, target_col].mean()
        low = group.loc[rank <= 0.2, target_col].mean()
        spreads.append(high - low)

    if not daily_ic:
        return {
            "usable_dates": 0,
            "mean_ic": np.nan,
            "mean_rank_ic": np.nan,
            "ic_ir": np.nan,
            "positive_ic_fraction": np.nan,
            "mean_top_bottom_spread_bps": np.nan,
        }

    ic = np.asarray(daily_ic, dtype=float)
    rank_ic = np.asarray(daily_rank_ic, dtype=float)
    spread = np.asarray(spreads, dtype=float)
    ic_std = np.nanstd(ic, ddof=1) if len(ic) > 1 else np.nan

    return {
        "usable_dates": int(len(ic)),
        "mean_ic": float(np.nanmean(ic)),
        "mean_rank_ic": float(np.nanmean(rank_ic)),
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

    for horizon in HORIZONS:
        target = f"target_excess_{horizon}d"
        base = panel[["date", "symbol", target] + features].dropna().copy()
        splits = chronological_splits(base["date"])

        train = base[
            (base["date"] >= splits["train_start"])
            & (base["date"] <= splits["train_end"])
        ].copy()
        validation = base[
            (base["date"] >= splits["validation_start"])
            & (base["date"] <= splits["validation_end"])
        ].copy()
        test = base[
            (base["date"] >= splits["test_start"])
            & (base["date"] <= splits["test_end"])
        ].copy()

        train_x, valid_x, kept = fit_transform(train, validation, features)
        _, test_x, _ = fit_transform(train, test, kept)

        y_train = train[target].to_numpy()

        model_specs = [
            ("ols", None),
            ("ridge_fixed_alpha", RIDGE_ALPHA),
        ]

        for split_name, frame in (("validation", validation), ("development_test", test)):
            zero = pd.Series(0.0, index=frame.index)
            model_rows.append(
                {
                    "horizon_days": horizon,
                    "model": "zero_baseline",
                    "split": split_name,
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
                        "horizon_days": horizon,
                        "model": model_name,
                        "split": split_name,
                        **score_predictions(frame, prediction, target),
                    }
                )

                if split_name == "development_test":
                    diagnostic = frame[["date", "symbol", target]].copy()
                    diagnostic["prediction"] = prediction.to_numpy()
                    diagnostic["prediction_pct_rank"] = diagnostic.groupby("date")[
                        "prediction"
                    ].rank(method="first", pct=True)
                    q = (
                        diagnostic.groupby("date")
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
                    q["horizon_days"] = horizon
                    q["model"] = model_name
                    quintile_rows.extend(q.to_dict("records"))

    return pd.DataFrame(model_rows), pd.DataFrame(quintile_rows)


def feature_metadata(features: list[str]) -> pd.DataFrame:
    descriptions = {
        "ret_1d": "Prior 1-day close-to-close return",
        "ret_5d": "Prior 5-day close-to-close return",
        "ret_20d": "Prior 20-day close-to-close return",
        "ma_gap_5d": "Close relative to trailing 5-day moving average",
        "ma_gap_20d": "Close relative to trailing 20-day moving average",
        "vol_5d": "Annualized trailing 5-day realized volatility",
        "vol_20d": "Annualized trailing 20-day realized volatility",
        "range_1d": "Daily high-low range divided by close",
        "log_volume": "Log(1 + daily volume)",
        "volume_mean_5d": "Trailing 5-day mean log volume",
        "volume_z_20d": "Trailing 20-day z-score of log volume",
        "market_rel_1d": "1-day return relative to NIFTYBEES",
        "market_rel_5d": "5-day return relative to NIFTYBEES",
        "market_rel_20d": "20-day return relative to NIFTYBEES",
        "market_beta_20d": "Trailing 20-day beta to NIFTYBEES",
    }
    rows = []
    for feature in features:
        base = feature
        transform = "raw trailing feature"
        if feature.endswith("_rank"):
            base = feature[:-5]
            transform = "cross-sectional percentile rank"
        elif feature.endswith("_cs_z"):
            base = feature[:-5]
            transform = "cross-sectional z-score"

        rows.append(
            {
                "feature": feature,
                "base_feature": base,
                "transform": transform,
                "description": descriptions.get(
                    base, "Derived cross-sectional feature"
                ),
            }
        )
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

    market = daily_ohlcv(load_intraday(market_path))
    # Lock the decision/outcome panel before creating forward targets so the
    # 5-day target cannot cross into the protected validation period.
    panel = locked_exploratory_slice(build_panel(frames, market))
    panel = add_targets(panel)
    features = feature_columns(panel)

    ic = univariate_ic(panel, features)
    models, quintiles = model_diagnostics(panel, features)
    metadata = feature_metadata(features)

    ic.to_csv(args.output_dir / "feature_ic.csv", index=False)
    models.to_csv(args.output_dir / "model_metrics.csv", index=False)
    quintiles.to_csv(args.output_dir / "quintile_diagnostics.csv", index=False)
    metadata.to_csv(args.output_dir / "feature_metadata.csv", index=False)

    splits = chronological_splits(panel["date"])
    manifest = {
        "strategy_id": "003",
        "analysis": "prediction_discovery",
        "status": "discovery_only",
        "exploratory_start": str(EXPLORATORY_START.date()),
        "exploratory_end": str(EXPLORATORY_END.date()),
        "validation_start": str(VALIDATION_START.date()),
        "holdout_start": str(HOLDOUT_START.date()),
        "prediction_horizons_days": list(HORIZONS),
        "equity_symbols": sorted(frames),
        "market_proxy": "NIFTYBEES",
        "feature_count": len(features),
        "models": ["zero_baseline", "ols", "ridge_fixed_alpha"],
        "ridge_alpha": RIDGE_ALPHA,
        "quintiles": QUINTILES,
        "internal_split": {k: str(v.date()) for k, v in splits.items()},
        "holdout_used": False,
        "strategy_pnl_calculated": False,
        "parameter_search": False,
    }
    (args.output_dir / "run_manifest.json").write_text(
        json.dumps(manifest, indent=2), encoding="utf-8"
    )

    print("Strategy 003 discovery complete")
    print(f"Eligible equity symbols: {len(frames)}")
    print(f"Feature count: {len(features)}")
    print(f"Exploratory window: {EXPLORATORY_START.date()} -> {EXPLORATORY_END.date()}")
    print(f"Protected validation starts: {VALIDATION_START.date()}")
    print(f"Protected holdout starts: {HOLDOUT_START.date()}")
    print(f"Outputs: {args.output_dir}")


if __name__ == "__main__":
    main()
