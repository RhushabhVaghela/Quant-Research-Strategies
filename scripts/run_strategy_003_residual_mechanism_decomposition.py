"""Run Strategy 003 residual mechanism decomposition.

Development-only explanatory decomposition. Keeps the 003H mechanism
locked and adds one registered raw feature family at a time.
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
    VALIDATION_START,
    build_panel,
    fit_linear,
    fit_transform,
    load_audit,
    load_candidates,
    load_intraday,
    locked_exploratory_slice,
    purged_chronological_splits,
    score_predictions,
)

BASE_FEATURES = [
    "close_location_1bar",
    "intraday_position_60bar",
    "bars_since_session_open",
]

FAMILY_BLOCKS = {
    "activity": [
        "log_volume",
        "volume_change_1bar",
        "volume_z_12bar",
        "volume_z_60bar",
    ],
    "volatility": [
        "realized_vol_12bar",
        "realized_vol_60bar",
        "range_1bar",
        "range_z_60bar",
    ],
    "market_context": [
        "market_return_1bar",
        "market_vol_60bar",
    ],
}

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory", type=Path, nargs="?",
                        default=Path("data/raw/strategy_002_universe"))
    parser.add_argument("--output-dir", type=Path,
                        default=Path("data/reports/strategy_003_residual_mechanism_decomposition"))
    parser.add_argument("--audit-report", type=Path,
                        default=Path("data/reports/strategy_002_universe_audit.csv"))
    parser.add_argument("--universe", type=Path,
                        default=Path("research/universe_candidates.csv"))
    return parser.parse_args()

def fit_score(panel: pd.DataFrame, features: list[str], model_name: str) -> tuple[pd.DataFrame, pd.DataFrame]:
    target = "target_excess_1bar"
    base = panel[["timestamp", "symbol", target] + features].dropna(subset=[target]).copy()
    splits = purged_chronological_splits(base["timestamp"])

    train = base[(base["timestamp"] >= splits["train_start"]) & (base["timestamp"] <= splits["train_end"])].copy()
    validation = base[(base["timestamp"] >= splits["validation_start"]) & (base["timestamp"] <= splits["validation_end"])].copy()
    test = base[(base["timestamp"] >= splits["test_start"]) & (base["timestamp"] <= splits["test_end"])].copy()

    usable = [f for f in features if train[f].notna().any()]
    train = train.dropna(subset=usable)
    validation = validation.dropna(subset=usable)
    test = test.dropna(subset=usable)

    train_x, valid_x, kept = fit_transform(train, validation, usable)
    _, test_x, _ = fit_transform(train, test, kept)
    beta = fit_linear(train_x, train[target].to_numpy())

    rows = []
    scored = []
    for split_name, frame, x in (
        ("validation", validation, valid_x),
        ("development_test", test, test_x),
    ):
        pred = pd.Series(
            np.column_stack([np.ones(len(x)), x]) @ beta,
            index=frame.index,
        )
        metrics = score_predictions(frame, pred, target)
        rows.append({
            "model": model_name,
            "split": split_name,
            "feature_count": len(kept),
            "features": ";".join(kept),
            "purged": True,
            "horizon_bars": HORIZON_BARS,
            "horizon_minutes": HORIZON_BARS * BAR_MINUTES,
            **metrics,
        })
        if split_name == "development_test":
            out = frame[["timestamp", "symbol", target]].copy()
            out["prediction"] = pred.to_numpy()
            scored.append(out)

    return pd.DataFrame(rows), pd.concat(scored, ignore_index=True)

def quintile_table(scored: pd.DataFrame) -> pd.DataFrame:
    work = scored.copy()
    work["quintile"] = work.groupby("timestamp")["prediction"].rank(
        method="first", pct=True
    ).map(lambda x: min(5, int(np.ceil(x * 5))))
    return (
        work.groupby("quintile", as_index=False)
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
            "mean_target_excess_bps": part["target_excess_1bar"].mean() * 1e4 if not part.empty else np.nan,
        })
    return pd.DataFrame(rows)

def build_universe(args: argparse.Namespace) -> tuple[dict[str, pd.DataFrame], pd.DataFrame]:
    candidates = load_candidates(args.universe)
    audit = load_audit(args.audit_report)
    eligible = set(audit.loc[
        (audit["unexpected_interval_count"] == 0) & (audit["zero_volume_rows"] == 0), "symbol"
    ].astype(str))
    equity_categories = {"large_cap_equity", "liquid_auto"}
    symbols = set(candidates.loc[candidates["category"].isin(equity_categories), "symbol"].astype(str)) & eligible

    if "NIFTYBEES" not in eligible:
        raise SystemExit("NIFTYBEES is required as the market reference")

    frames = {}
    for symbol in sorted(symbols):
        path = args.directory / f"NSE_{symbol}_5minute.csv"
        if not path.exists():
            raise SystemExit(f"Missing required equity data file: {path}")
        frames[symbol] = load_intraday(path)

    market = load_intraday(args.directory / "NSE_NIFTYBEES_5minute.csv")
    return frames, market

def main() -> None:
    args = parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)
    frames, market = build_universe(args)
    panel = locked_exploratory_slice(build_panel(frames, market))

    model_rows = []
    for name, extra in [("mechanism", []), *[(k, v) for k, v in FAMILY_BLOCKS.items()]]:
        metrics, scored = fit_score(panel, BASE_FEATURES + extra, name)
        model_rows.append(metrics)
        metrics.to_csv(args.output_dir / f"{name}_metrics.csv", index=False)
        quintile_table(scored).to_csv(args.output_dir / f"{name}_quintiles.csv", index=False)
        stock_stability(scored).to_csv(args.output_dir / f"{name}_stock_stability.csv", index=False)
        time_of_day(scored).to_csv(args.output_dir / f"{name}_time_of_day.csv", index=False)

    comparison = pd.concat(model_rows, ignore_index=True)
    base_dev = comparison[(comparison["model"] == "mechanism") & (comparison["split"] == "development_test")].iloc[0]
    inc_rows = []
    for _, row in comparison[comparison["split"] == "development_test"].iterrows():
        inc_rows.append({
            "model": row["model"],
            "incremental_mean_ic_vs_mechanism": row["mean_ic"] - base_dev["mean_ic"],
            "incremental_mean_rank_ic_vs_mechanism": row["mean_rank_ic"] - base_dev["mean_rank_ic"],
            "incremental_spread_bps_vs_mechanism": row["mean_top_bottom_spread_bps"] - base_dev["mean_top_bottom_spread_bps"],
        })
    pd.DataFrame(inc_rows).to_csv(args.output_dir / "incremental_vs_mechanism.csv", index=False)

    lineage = []
    for feature in BASE_FEATURES + [f for values in FAMILY_BLOCKS.values() for f in values]:
        lineage.append({
            "strategy": "003",
            "feature": feature,
            "directly_encodes_001_signed_return": False,
            "directly_encodes_002_peer_residual_return": False,
        })
    pd.DataFrame(lineage).to_csv(args.output_dir / "lineage_audit.csv", index=False)

    splits = purged_chronological_splits(panel["timestamp"])
    manifest = {
        "strategy_id": "003",
        "experiment": "003_residual_mechanism_decomposition",
        "status": "hypothesis_test_only",
        "base_features": BASE_FEATURES,
        "family_blocks": FAMILY_BLOCKS,
        "raw_features_only": True,
        "models": ["zero_baseline", "mechanism", "activity", "volatility", "market_context"],
        "exploratory_start": str(EXPLORATORY_START.date()),
        "exploratory_end": str(EXPLORATORY_END.date()),
        "project_validation_start": str(VALIDATION_START.date()),
        "final_holdout_start": str(HOLDOUT_START.date()),
        "horizon_bars": HORIZON_BARS,
        "horizon_minutes": HORIZON_BARS * BAR_MINUTES,
        "holdout_used": False,
        "parameter_search": False,
        "feature_family_selection": False,
        "holding_period_search": False,
        "cost_optimization": False,
        "internal_split": {k: str(v) if isinstance(v, pd.Timestamp) else v for k, v in splits.items()},
    }
    (args.output_dir / "run_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")

    print("Strategy 003 residual mechanism decomposition complete")
    print(f"Eligible equity symbols: {len(frames)}")
    print(f"Locked base features: {BASE_FEATURES}")
    print(f"Family blocks: {list(FAMILY_BLOCKS)}")

if __name__ == "__main__":
    main()
