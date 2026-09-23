"""Run the frozen Strategy 003 protected chronological validation.

Prediction-only. Trains the frozen additive 003H model on all development
observations through 2026-06-09 and evaluates only 2026-06-10 through
2026-08-19. It must not inspect the final holdout beginning 2026-08-20.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd

from scripts.run_strategy_003_prediction_discovery import (
    BAR_MINUTES,
    EXPLORATORY_START,
    build_panel,
    fit_linear,
    load_audit,
    load_candidates,
    load_intraday,
    locked_exploratory_slice,
    score_predictions,
)

FEATURES = ["close_location_1bar", "intraday_position_60bar"]
DEVELOPMENT_END = pd.Timestamp("2026-06-09 23:59:59+05:30")
VALIDATION_START = pd.Timestamp("2026-06-10 00:00:00+05:30")
VALIDATION_END = pd.Timestamp("2026-08-19 23:59:59+05:30")
HOLDOUT_START = pd.Timestamp("2026-08-20 00:00:00+05:30")
HORIZON_BARS = 1


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("directory", type=Path, nargs="?", default=Path("data/raw/strategy_002_universe"))
    p.add_argument("--output-dir", type=Path, default=Path("data/reports/strategy_003_protected_validation"))
    p.add_argument("--audit-report", type=Path, default=Path("data/reports/strategy_002_universe_audit.csv"))
    p.add_argument("--universe", type=Path, default=Path("research/universe_candidates.csv"))
    return p.parse_args()


def fit_standardized(train: pd.DataFrame, other: pd.DataFrame):
    means = train[FEATURES].mean()
    stds = train[FEATURES].std(ddof=1)
    if ((stds <= 0) | stds.isna()).any():
        bad = stds.index[((stds <= 0) | stds.isna())].tolist()
        raise ValueError(f"Frozen feature became constant/unusable: {bad}")
    return (
        ((train[FEATURES] - means) / stds).to_numpy(),
        ((other[FEATURES] - means) / stds).to_numpy(),
    )


def quintiles(scored: pd.DataFrame) -> pd.DataFrame:
    work = scored.copy()
    work["quintile"] = work.groupby("timestamp").prediction.rank(
        method="first", pct=True
    ).map(lambda x: min(5, int(np.ceil(x * 5))))
    return work.groupby("quintile", as_index=False).agg(
        timestamps=("timestamp", "nunique"),
        observations=("target_excess_1bar", "size"),
        mean_return_bps=("target_excess_1bar", lambda s: s.mean() * 1e4),
        median_return_bps=("target_excess_1bar", lambda s: s.median() * 1e4),
        positive_fraction=("target_excess_1bar", lambda s: (s > 0).mean()),
    )


def main() -> None:
    args = parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)

    candidates = load_candidates(args.universe)
    audit = load_audit(args.audit_report)
    eligible = set(audit.loc[
        (audit.unexpected_interval_count == 0) & (audit.zero_volume_rows == 0), "symbol"
    ].astype(str))
    symbols = set(candidates.loc[
        candidates.category.isin({"large_cap_equity", "liquid_auto"}), "symbol"
    ].astype(str)) & eligible

    if "NIFTYBEES" not in eligible:
        raise SystemExit("NIFTYBEES is required as the market reference")

    frames = {}
    for symbol in sorted(symbols):
        frame = load_intraday(args.directory / f"NSE_{symbol}_5minute.csv")
        frames[symbol] = frame.loc[frame.index < HOLDOUT_START].copy()
    market = load_intraday(args.directory / "NSE_NIFTYBEES_5minute.csv")
    market = market.loc[market.index < HOLDOUT_START].copy()
    # Hard stop: raw inputs are truncated before the final holdout is passed to build_panel.
    panel = locked_exploratory_slice(build_panel(frames, market))
    panel = panel.dropna(subset=FEATURES + ["target_excess_1bar"]).copy()

    train = panel.loc[
        (panel.timestamp >= EXPLORATORY_START) & (panel.timestamp <= DEVELOPMENT_END)
    ].copy()
    validation = panel.loc[
        (panel.timestamp >= VALIDATION_START) & (panel.timestamp <= VALIDATION_END)
    ].copy()
    if train.empty or validation.empty:
        raise ValueError("Frozen development/validation window is empty")

    train_x, validation_x = fit_standardized(train, validation)
    beta = fit_linear(train_x, train["target_excess_1bar"].to_numpy())
    prediction = pd.Series(
        np.column_stack([np.ones(len(validation_x)), validation_x]) @ beta,
        index=validation.index,
        name="prediction",
    )
    scored = validation[["timestamp", "symbol", "target_excess_1bar"]].copy()
    scored["prediction"] = prediction.to_numpy()

    metrics = score_predictions(validation, prediction, "target_excess_1bar")
    row = {
        "split": "protected_validation",
        "mean_ic": metrics["mean_ic"],
        "mean_rank_ic": metrics["mean_rank_ic"],
        "descriptive_ic_ir": metrics.get("descriptive_ic_ir", np.nan),
        "mean_top_bottom_spread_bps": metrics["mean_top_bottom_spread_bps"],
        "positive_ic_fraction": metrics.get("positive_ic_fraction", np.nan),
        "timestamps": int(validation.timestamp.nunique()),
        "observations": int(len(validation)),
        "symbols": int(validation.symbol.nunique()),
        "validation_start": str(VALIDATION_START),
        "validation_end": str(VALIDATION_END),
    }

    pd.DataFrame([row]).to_csv(args.output_dir / "protected_validation_metrics.csv", index=False)
    development_reference = pd.DataFrame([{
        "metric": "mean_ic", "development_test_reference": 0.0696,
    }, {
        "metric": "mean_rank_ic", "development_test_reference": 0.0826,
    }, {
        "metric": "mean_top_bottom_spread_bps", "development_test_reference": 2.2168,
    }])
    development_reference.to_csv(
        args.output_dir / "development_reference_comparison.csv", index=False
    )
    quintiles(scored).to_csv(args.output_dir / "protected_validation_quintiles.csv", index=False)
    scored.to_csv(args.output_dir / "protected_validation_scored_observations.csv", index=False)

    timestamp_diag = scored.groupby("timestamp").apply(
        lambda g: pd.Series({
            "ic": g["prediction"].corr(g["target_excess_1bar"]),
            "rank_ic": g["prediction"].rank().corr(g["target_excess_1bar"].rank()),
            "observations": len(g),
        }),
        include_groups=False,
    ).reset_index()
    timestamp_diag.to_csv(
        args.output_dir / "protected_validation_timestamp_diagnostics.csv", index=False
    )

    manifest = {
        "experiment": "003_protected_validation",
        "status": "executed_prediction_only",
        "frozen_features": FEATURES,
        "model": "additive_OLS_training_only_standardization",
        "development_start": str(EXPLORATORY_START),
        "development_end": str(DEVELOPMENT_END),
        "validation_start": str(VALIDATION_START),
        "validation_end": str(VALIDATION_END),
        "final_holdout_start": str(HOLDOUT_START),
        "horizon_bars": HORIZON_BARS,
        "horizon_minutes": BAR_MINUTES * HORIZON_BARS,
        "protected_validation_used": True,
        "final_holdout_used": False,
        "feature_search": False,
        "model_search": False,
        "threshold_search": False,
        "holding_period_search": False,
        "cost_optimization": False,
        "portfolio_construction": False,
        "rescue_tuning": False,
        "raw_inputs_truncated_before_holdout": True,
    }
    (args.output_dir / "run_manifest.json").write_text(
        json.dumps(manifest, indent=2), encoding="utf-8"
    )

    print("Strategy 003 protected validation complete")
    print(f"Eligible equity symbols: {len(frames)}")
    print(f"Validation timestamps: {validation.timestamp.nunique()}")
    print(f"Validation observations: {len(validation)}")
    print(f"Outputs: {args.output_dir}")


if __name__ == "__main__":
    main()
