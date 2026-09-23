"""Run Strategy 003H — controlled economic-mechanism decomposition.

This is an explanatory hypothesis test, not a trading-strategy backtest.
It compares the frozen full discovery model with a preregistered simple
bar-shape/intraday-state specification using only development data.
Protected validation and final holdout periods are never read.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd

from scripts.run_strategy_003_prediction_discovery import (
    BAR_MINUTES,
    EXPLORATORY_END,
    EXPLORATORY_START,
    HORIZON_BARS,
    HOLDOUT_START,
    RIDGE_ALPHA,
    VALIDATION_START,
    build_panel,
    feature_columns,
    fit_linear,
    fit_transform,
    load_audit,
    load_candidates,
    load_intraday,
    locked_exploratory_slice,
    purged_chronological_splits,
    score_predictions,
)

MECHANISM_FEATURES = [
    "close_location_1bar",
    "intraday_position_60bar",
    "bars_since_session_open",
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
        default=Path("data/reports/strategy_003_hypothesis_003h"),
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


def fit_score(
    panel: pd.DataFrame,
    features: list[str],
) -> tuple[pd.DataFrame, pd.DataFrame]:
    target = "target_excess_1bar"
    base = panel[["timestamp", "symbol", target] + features].dropna(subset=[target]).copy()
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

    usable = [f for f in features if train[f].notna().any()]
    train = train.dropna(subset=usable)
    validation = validation.dropna(subset=usable)
    test = test.dropna(subset=usable)

    train_x, valid_x, kept = fit_transform(train, validation, usable)
    _, test_x, _ = fit_transform(train, test, kept)

    beta = fit_linear(train_x, train[target].to_numpy())
    valid_pred = pd.Series(
        np.column_stack([np.ones(len(valid_x)), valid_x]) @ beta,
        index=validation.index,
    )
    test_pred = pd.Series(
        np.column_stack([np.ones(len(test_x)), test_x]) @ beta,
        index=test.index,
    )

    rows = []
    scored = []
    for split_name, frame, prediction in (
        ("validation", validation, valid_pred),
        ("development_test", test, test_pred),
    ):
        metrics = score_predictions(frame, prediction, target)
        rows.append({
            "model": "mechanism_ols",
            "split": split_name,
            "feature_count": len(kept),
            "features": ";".join(kept),
            "purged": True,
            "horizon_bars": HORIZON_BARS,
            "horizon_minutes": HORIZON_BARS * BAR_MINUTES,
            **metrics,
        })
        if split_name == "development_test":
            scored_frame = frame[["timestamp", "symbol", target]].copy()
            scored_frame["prediction"] = prediction.to_numpy()
            scored.append(scored_frame)

    return pd.DataFrame(rows), pd.concat(scored, ignore_index=True)


def quintile_table(scored: pd.DataFrame) -> pd.DataFrame:
    work = scored.copy()
    work["quintile"] = work.groupby("timestamp")["prediction"].rank(
        method="first", pct=True
    ).map(lambda x: min(5, int(np.ceil(x * 5))))
    return (
        work.groupby(["quintile"], as_index=False)
        .agg(
            timestamps=("timestamp", "nunique"),
            observations=("target_excess_1bar", "size"),
            mean_return_bps=("target_excess_1bar", lambda s: s.mean() * 1e4),
            median_return_bps=("target_excess_1bar", lambda s: s.median() * 1e4),
            positive_fraction=("target_excess_1bar", lambda s: (s > 0).mean()),
        )
        .sort_values("quintile")
    )


def stock_stability(scored: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for symbol, group in scored.groupby("symbol"):
        corr = group["prediction"].corr(group["target_excess_1bar"])
        rows.append({
            "symbol": symbol,
            "n": len(group),
            "prediction_target_corr": float(corr) if np.isfinite(corr) else np.nan,
            "mean_target_excess_bps": float(group["target_excess_1bar"].mean() * 1e4),
        })
    return pd.DataFrame(rows).sort_values("symbol")


def time_bucket(ts: pd.Series) -> pd.Series:
    local = pd.DatetimeIndex(ts).tz_convert("Asia/Kolkata")
    minutes = local.hour * 60 + local.minute
    return pd.cut(
        minutes,
        bins=[-1, 10 * 60 - 1, 12 * 60 - 1, 14 * 60 - 1, 15 * 60 + 30],
        labels=["09:15-09:59", "10:00-11:59", "12:00-13:59", "14:00-15:30"],
    )


def time_of_day(scored: pd.DataFrame) -> pd.DataFrame:
    work = scored.copy()
    work["time_bucket"] = time_bucket(work["timestamp"])
    rows = []
    for bucket in work["time_bucket"].cat.categories:
        part = work[work["time_bucket"] == bucket]
        rows.append({
            "time_bucket": str(bucket),
            "scored_rows": len(part),
            "timestamps": part["timestamp"].nunique(),
            "mean_target_excess_bps": (
                part["target_excess_1bar"].mean() * 1e4 if not part.empty else np.nan
            ),
        })
    return pd.DataFrame(rows)


def lineage_audit() -> pd.DataFrame:
    return pd.DataFrame([
        {
            "strategy": "003H",
            "feature": "close_location_1bar",
            "directly_encodes_001_signed_return": False,
            "directly_encodes_002_peer_residual_return": False,
            "interpretation": "Current close position within current bar; no explicit lagged return sign or peer residual.",
        },
        {
            "strategy": "003H",
            "feature": "intraday_position_60bar",
            "directly_encodes_001_signed_return": False,
            "directly_encodes_002_peer_residual_return": False,
            "interpretation": "Current close relative to trailing 60-bar session mean; state variable rather than explicit signed-return event.",
        },
        {
            "strategy": "003H",
            "feature": "bars_since_session_open",
            "directly_encodes_001_signed_return": False,
            "directly_encodes_002_peer_residual_return": False,
            "interpretation": "Session-clock state; no return or peer-residual information.",
        },
    ])


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
    symbols = set(
        candidates.loc[candidates["category"].isin(equity_categories), "symbol"].astype(str)
    ) & eligible

    if "NIFTYBEES" not in eligible:
        raise SystemExit("NIFTYBEES is required as the market reference")

    frames = {}
    for symbol in sorted(symbols):
        path = args.directory / f"NSE_{symbol}_5minute.csv"
        if not path.exists():
            raise SystemExit(f"Missing required equity data file: {path}")
        frames[symbol] = load_intraday(path)

    market_path = args.directory / "NSE_NIFTYBEES_5minute.csv"
    market = load_intraday(market_path)

    panel = locked_exploratory_slice(build_panel(frames, market))

    mechanism_metrics, mechanism_scored = fit_score(panel, MECHANISM_FEATURES)
    full_metrics, full_scored = fit_score(panel, feature_columns(panel))

    mechanism_q = quintile_table(mechanism_scored)
    full_q = quintile_table(full_scored)
    mechanism_stock = stock_stability(mechanism_scored)
    full_stock = stock_stability(full_scored)
    mechanism_tod = time_of_day(mechanism_scored)
    full_tod = time_of_day(full_scored)

    mechanism_metrics.to_csv(args.output_dir / "mechanism_model_metrics.csv", index=False)
    full_metrics.to_csv(args.output_dir / "full_model_metrics.csv", index=False)
    mechanism_q.to_csv(args.output_dir / "mechanism_quintile_summary.csv", index=False)
    full_q.to_csv(args.output_dir / "full_model_quintile_summary.csv", index=False)
    mechanism_stock.to_csv(args.output_dir / "mechanism_stock_stability.csv", index=False)
    full_stock.to_csv(args.output_dir / "full_model_stock_stability.csv", index=False)
    mechanism_tod.to_csv(args.output_dir / "mechanism_time_of_day.csv", index=False)
    full_tod.to_csv(args.output_dir / "full_model_time_of_day.csv", index=False)
    lineage_audit().to_csv(args.output_dir / "lineage_audit.csv", index=False)

    comparison = pd.DataFrame([
        {
            "model": "mechanism_ols",
            **mechanism_metrics.loc[
                mechanism_metrics["split"] == "development_test"
            ].iloc[0].to_dict(),
        },
        {
            "model": "full_ols",
            **full_metrics.loc[
                full_metrics["split"] == "development_test"
            ].iloc[0].to_dict(),
        },
    ])
    comparison.to_csv(args.output_dir / "model_comparison.csv", index=False)

    splits = purged_chronological_splits(panel["timestamp"])
    manifest = {
        "strategy_id": "003",
        "experiment": "003H_mechanism_decomposition",
        "status": "hypothesis_test_only",
        "locked_features": MECHANISM_FEATURES,
        "models": ["zero_baseline", "mechanism_ols", "full_ols"],
        "exploratory_start": str(EXPLORATORY_START.date()),
        "exploratory_end": str(EXPLORATORY_END.date()),
        "project_validation_start": str(VALIDATION_START.date()),
        "final_holdout_start": str(HOLDOUT_START.date()),
        "horizon_bars": HORIZON_BARS,
        "horizon_minutes": HORIZON_BARS * BAR_MINUTES,
        "holdout_used": False,
        "strategy_pnl_calculated": False,
        "parameter_search": False,
        "new_feature_search": False,
        "holding_period_search": False,
        "cost_optimization": False,
        "internal_split": {
            k: str(v) if isinstance(v, pd.Timestamp) else v
            for k, v in splits.items()
        },
        "note": "Explanatory decomposition only. The mechanism feature set was preregistered before this run and is not selected by historical performance.",
    }
    (args.output_dir / "run_manifest.json").write_text(
        json.dumps(manifest, indent=2, default=str), encoding="utf-8"
    )

    print("Strategy 003H mechanism decomposition complete")
    print(f"Eligible equity symbols: {len(frames)}")
    print(f"Locked mechanism features: {MECHANISM_FEATURES}")
    print(f"Outputs: {args.output_dir}")


if __name__ == "__main__":
    main()
