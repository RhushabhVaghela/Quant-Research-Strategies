"""Run Strategy 003 common-support nested mechanism comparisons."""

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

BASE = ["close_location_1bar", "intraday_position_60bar", "bars_since_session_open"]
BLOCKS = {
    "activity": ["log_volume", "volume_change_1bar", "volume_z_12bar", "volume_z_60bar"],
    "volatility": ["realized_vol_12bar", "realized_vol_60bar", "range_1bar", "range_z_60bar"],
    "market_context": ["market_return_1bar", "market_vol_60bar"],
}

def args() -> argparse.Namespace:
    p = argparse.ArgumentParser()
    p.add_argument("directory", type=Path, nargs="?", default=Path("data/raw/strategy_002_universe"))
    p.add_argument("--output-dir", type=Path, default=Path("data/reports/strategy_003_common_support"))
    p.add_argument("--audit-report", type=Path, default=Path("data/reports/strategy_002_universe_audit.csv"))
    p.add_argument("--universe", type=Path, default=Path("research/universe_candidates.csv"))
    return p.parse_args()

def fit_model(base: pd.DataFrame, features: list[str], name: str, splits: dict[str, pd.Timestamp]) -> tuple[pd.DataFrame, pd.DataFrame]:
    train = base[(base.timestamp >= splits["train_start"]) & (base.timestamp <= splits["train_end"])].copy()
    valid = base[(base.timestamp >= splits["validation_start"]) & (base.timestamp <= splits["validation_end"])].copy()
    test = base[(base.timestamp >= splits["test_start"]) & (base.timestamp <= splits["test_end"])].copy()
    train_x, valid_x, kept = fit_transform(train, valid, features)
    _, test_x, _ = fit_transform(train, test, kept)
    beta = fit_linear(train_x, train.target_excess_1bar.to_numpy())
    rows, scored = [], []
    for split, frame, x in [("validation", valid, valid_x), ("development_test", test, test_x)]:
        pred = pd.Series(np.column_stack([np.ones(len(x)), x]) @ beta, index=frame.index)
        m = score_predictions(frame, pred, "target_excess_1bar")
        rows.append({"model": name, "split": split, "feature_count": len(kept), "features": ";".join(kept), **m})
        if split == "development_test":
            out = frame[["timestamp", "symbol", "target_excess_1bar"]].copy()
            out["prediction"] = pred.to_numpy()
            scored.append(out)
    return pd.DataFrame(rows), pd.concat(scored, ignore_index=True)

def quintiles(scored: pd.DataFrame) -> pd.DataFrame:
    w = scored.copy()
    w["quintile"] = w.groupby("timestamp").prediction.rank(method="first", pct=True).map(lambda x: min(5, int(np.ceil(x * 5))))
    return w.groupby("quintile", as_index=False).agg(
        timestamps=("timestamp","nunique"),
        observations=("target_excess_1bar","size"),
        mean_return_bps=("target_excess_1bar",lambda s:s.mean()*1e4),
        median_return_bps=("target_excess_1bar",lambda s:s.median()*1e4),
        positive_fraction=("target_excess_1bar",lambda s:(s>0).mean()),
    )

def common_base(panel: pd.DataFrame, features: list[str]) -> pd.DataFrame:
    cols = ["timestamp","symbol","target_excess_1bar"] + features
    return panel[cols].dropna().copy()

def main() -> None:
    a = args()
    a.output_dir.mkdir(parents=True, exist_ok=True)
    candidates = load_candidates(a.universe)
    audit = load_audit(a.audit_report)
    eligible = set(audit.loc[(audit.unexpected_interval_count == 0) & (audit.zero_volume_rows == 0), "symbol"].astype(str))
    symbols = set(candidates.loc[candidates.category.isin({"large_cap_equity","liquid_auto"}), "symbol"].astype(str)) & eligible
    frames = {}
    for symbol in sorted(symbols):
        frames[symbol] = load_intraday(a.directory / f"NSE_{symbol}_5minute.csv")
    market = load_intraday(a.directory / "NSE_NIFTYBEES_5minute.csv")
    panel = locked_exploratory_slice(build_panel(frames, market))
    splits = purged_chronological_splits(panel.timestamp)

    all_rows = []
    for name, extra in BLOCKS.items():
        features = BASE + extra
        common = common_base(panel, features)
        metrics, scored = fit_model(common, BASE, "mechanism", splits)
        ext_metrics, ext_scored = fit_model(common, features, name, splits)
        all_rows.extend([metrics, ext_metrics])
        q = quintiles(scored).merge(quintiles(ext_scored), on="quintile", suffixes=("_mechanism","_extended"))
        q.to_csv(a.output_dir / f"{name}_quintiles_common_support.csv", index=False)
        pair = ext_metrics[ext_metrics.split == "development_test"].iloc[0]
        base_row = metrics[metrics.split == "development_test"].iloc[0]
        pd.DataFrame([{
            "block": name,
            "common_support_timestamps": int(common.timestamp.nunique()),
            "mechanism_mean_ic": base_row.mean_ic,
            "extended_mean_ic": pair.mean_ic,
            "incremental_mean_ic": pair.mean_ic - base_row.mean_ic,
            "mechanism_mean_rank_ic": base_row.mean_rank_ic,
            "extended_mean_rank_ic": pair.mean_rank_ic,
            "incremental_mean_rank_ic": pair.mean_rank_ic - base_row.mean_rank_ic,
            "mechanism_spread_bps": base_row.mean_top_bottom_spread_bps,
            "extended_spread_bps": pair.mean_top_bottom_spread_bps,
            "incremental_spread_bps": pair.mean_top_bottom_spread_bps - base_row.mean_top_bottom_spread_bps,
        }]).to_csv(a.output_dir / f"{name}_incremental_common_support.csv", index=False)

    pd.concat(all_rows, ignore_index=True).to_csv(a.output_dir / "metrics_common_support.csv", index=False)
    manifest = {
        "experiment": "003_common_support_nested_mechanism",
        "base_features": BASE,
        "blocks": BLOCKS,
        "common_support_per_block": True,
        "holdout_used": False,
        "parameter_search": False,
        "feature_selection": False,
        "holding_period_search": False,
        "cost_optimization": False,
        "exploratory_end": str(EXPLORATORY_END.date()),
        "project_validation_start": str(VALIDATION_START.date()),
        "final_holdout_start": str(HOLDOUT_START.date()),
        "horizon_bars": HORIZON_BARS,
        "horizon_minutes": HORIZON_BARS * BAR_MINUTES,
        "splits": {k: str(v) if isinstance(v, pd.Timestamp) else v for k,v in splits.items()},
    }
    (a.output_dir / "run_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    print("Strategy 003 common-support nested mechanism comparison complete")

if __name__ == "__main__":
    main()
