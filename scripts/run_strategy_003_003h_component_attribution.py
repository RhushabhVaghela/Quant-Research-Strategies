"""Run Strategy 003H component attribution.

Development-only explanatory experiment. Compares singleton, pairwise,
and all-three combinations of the locked 003H raw features. No feature
selection, parameter search, protected validation, or holdout use.
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

BASE = [
    "close_location_1bar",
    "intraday_position_60bar",
    "bars_since_session_open",
]

COMPONENTS = {
    "close_location": ["close_location_1bar"],
    "intraday_position": ["intraday_position_60bar"],
    "session_clock": ["bars_since_session_open"],
    "close_location__intraday_position": ["close_location_1bar", "intraday_position_60bar"],
    "close_location__session_clock": ["close_location_1bar", "bars_since_session_open"],
    "intraday_position__session_clock": ["intraday_position_60bar", "bars_since_session_open"],
    "all_three": BASE,
}

def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("directory", type=Path, nargs="?", default=Path("data/raw/strategy_002_universe"))
    p.add_argument("--output-dir", type=Path, default=Path("data/reports/strategy_003_003h_component_attribution"))
    p.add_argument("--audit-report", type=Path, default=Path("data/reports/strategy_002_universe_audit.csv"))
    p.add_argument("--universe", type=Path, default=Path("research/universe_candidates.csv"))
    return p.parse_args()


def fit_component_transform(
    train: pd.DataFrame,
    other: pd.DataFrame,
    features: list[str],
) -> tuple[np.ndarray, np.ndarray, list[str]]:
    """Standardize a singleton/pair/component block without the discovery
    runner's >=3-feature guard.

    The discovery guard is appropriate for the full model, but this
    attribution experiment intentionally evaluates one- and two-feature
    blocks. We therefore retain only non-constant training features while
    requiring at least one usable feature.
    """
    means = train[features].mean()
    stds = train[features].std(ddof=1)
    keep = stds[(stds > 0) & stds.notna()].index.tolist()
    if not keep:
        raise ValueError("No non-constant features after training fit")
    train_x = ((train[keep] - means[keep]) / stds[keep]).fillna(0.0).to_numpy()
    other_x = ((other[keep] - means[keep]) / stds[keep]).fillna(0.0).to_numpy()
    return train_x, other_x, keep

def fit_score(panel: pd.DataFrame, features: list[str], model_name: str, splits: dict[str, pd.Timestamp]):
    target = "target_excess_1bar"
    base = panel[["timestamp", "symbol", target] + features].dropna(subset=[target]).copy()
    train = base[(base.timestamp >= splits["train_start"]) & (base.timestamp <= splits["train_end"])].copy()
    valid = base[(base.timestamp >= splits["validation_start"]) & (base.timestamp <= splits["validation_end"])].copy()
    test = base[(base.timestamp >= splits["test_start"]) & (base.timestamp <= splits["test_end"])].copy()
    train = train.dropna(subset=features)
    valid = valid.dropna(subset=features)
    test = test.dropna(subset=features)
    train_x, valid_x, kept = fit_component_transform(train, valid, features)
    _, test_x, _ = fit_component_transform(train, test, kept)
    beta = fit_linear(train_x, train[target].to_numpy())
    rows = []
    scored = None
    for split_name, frame, x in [("validation", valid, valid_x), ("development_test", test, test_x)]:
        pred = pd.Series(np.column_stack([np.ones(len(x)), x]) @ beta, index=frame.index)
        rows.append({
            "model": model_name,
            "split": split_name,
            "feature_count": len(kept),
            "features": ";".join(kept),
            "usable_timestamps": int(frame.timestamp.nunique()),
            "purged": True,
            "horizon_bars": HORIZON_BARS,
            "horizon_minutes": HORIZON_BARS * BAR_MINUTES,
            **score_predictions(frame, pred, target),
        })
        if split_name == "development_test":
            scored = frame[["timestamp", "symbol", target]].copy()
            scored["prediction"] = pred.to_numpy()
    return pd.DataFrame(rows), scored

def quintiles(scored: pd.DataFrame, model_name: str) -> pd.DataFrame:
    w = scored.copy()
    w["quintile"] = w.groupby("timestamp").prediction.rank(method="first", pct=True).map(lambda x: min(5, int(np.ceil(x * 5))))
    return w.groupby("quintile", as_index=False).agg(
        timestamps=("timestamp", "nunique"),
        observations=("target_excess_1bar", "size"),
        mean_return_bps=("target_excess_1bar", lambda s: s.mean() * 1e4),
        median_return_bps=("target_excess_1bar", lambda s: s.median() * 1e4),
        positive_fraction=("target_excess_1bar", lambda s: (s > 0).mean()),
    ).assign(model=model_name)

def main() -> None:
    a = parse_args()
    a.output_dir.mkdir(parents=True, exist_ok=True)
    candidates = load_candidates(a.universe)
    audit = load_audit(a.audit_report)
    eligible = set(audit.loc[(audit.unexpected_interval_count == 0) & (audit.zero_volume_rows == 0), "symbol"].astype(str))
    symbols = set(candidates.loc[candidates.category.isin({"large_cap_equity", "liquid_auto"}), "symbol"].astype(str)) & eligible
    if "NIFTYBEES" not in eligible:
        raise SystemExit("NIFTYBEES is required as the market reference")
    frames = {s: load_intraday(a.directory / f"NSE_{s}_5minute.csv") for s in sorted(symbols)}
    market = load_intraday(a.directory / "NSE_NIFTYBEES_5minute.csv")
    panel = locked_exploratory_slice(build_panel(frames, market))
    splits = purged_chronological_splits(panel.timestamp)

    metrics = []
    quintile_frames = []
    for name, features in COMPONENTS.items():
        m, scored = fit_score(panel, features, name, splits)
        metrics.append(m)
        quintile_frames.append(quintiles(scored, name))
    metrics_df = pd.concat(metrics, ignore_index=True)
    q_df = pd.concat(quintile_frames, ignore_index=True)
    metrics_df.to_csv(a.output_dir / "component_metrics.csv", index=False)
    q_df.to_csv(a.output_dir / "component_quintiles.csv", index=False)

    ref = metrics_df[(metrics_df.model == "all_three") & (metrics_df.split == "development_test")].iloc[0]
    rows = []
    for name in COMPONENTS:
        row = metrics_df[(metrics_df.model == name) & (metrics_df.split == "development_test")].iloc[0]
        rows.append({
            "model": name,
            "delta_mean_ic_vs_all_three": row.mean_ic - ref.mean_ic,
            "delta_rank_ic_vs_all_three": row.mean_rank_ic - ref.mean_rank_ic,
            "delta_spread_bps_vs_all_three": row.mean_top_bottom_spread_bps - ref.mean_top_bottom_spread_bps,
            "usable_timestamps": row.usable_timestamps,
        })
    pd.DataFrame(rows).to_csv(a.output_dir / "component_attribution_vs_reference.csv", index=False)

    manifest = {
        "strategy_id": "003",
        "experiment": "003H_component_attribution",
        "locked_components": BASE,
        "specifications": COMPONENTS,
        "holdout_used": False,
        "protected_validation_used": False,
        "parameter_search": False,
        "feature_selection": False,
        "new_features": False,
        "new_transforms": False,
        "holding_period_search": False,
        "cost_optimization": False,
        "exploratory_end": str(EXPLORATORY_END.date()),
        "project_validation_start": str(VALIDATION_START.date()),
        "final_holdout_start": str(HOLDOUT_START.date()),
        "horizon_bars": HORIZON_BARS,
        "horizon_minutes": HORIZON_BARS * BAR_MINUTES,
        "splits": {k: str(v) if isinstance(v, pd.Timestamp) else v for k, v in splits.items()},
        "decision_rule": "Use component results for attribution only. Do not select the best subset by development performance.",
    }
    (a.output_dir / "run_manifest.json").write_text(json.dumps(manifest, indent=2, default=str), encoding="utf-8")
    print("Strategy 003H component attribution complete")
    print(f"Eligible equity symbols: {len(frames)}")
    print(f"Locked components: {list(COMPONENTS)}")
    print(f"Outputs: {a.output_dir}")

if __name__ == "__main__":
    main()
