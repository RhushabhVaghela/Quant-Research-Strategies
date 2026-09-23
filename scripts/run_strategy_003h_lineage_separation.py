"""Run the preregistered Strategy 003H lineage-separation experiment.

Development-only. Tests whether the 003H explanatory core retains predictive
information after the frozen Strategy 001 and Strategy 002 mechanisms are
represented explicitly. No parameter search or protected-period access.
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
    HOLDOUT_START,
    VALIDATION_START,
    build_panel,
    fit_linear,
    locked_exploratory_slice,
    load_audit,
    load_candidates,
    load_intraday,
    purged_chronological_splits,
    score_predictions,
)

CORE = ["close_location_1bar", "intraday_position_60bar"]
LINEAGE = ["strategy_001_event", "strategy_002_prior_loo_residual"]
SPECS = {
    "003h_core": CORE,
    "001_lineage": ["strategy_001_event"],
    "002_lineage": ["strategy_002_prior_loo_residual"],
    "001_plus_002_lineage": LINEAGE,
    "003h_plus_001_plus_002": CORE + LINEAGE,
}


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("directory", type=Path, nargs="?", default=Path("data/raw/strategy_002_universe"))
    p.add_argument("--output-dir", type=Path, default=Path("data/reports/strategy_003h_lineage_separation"))
    p.add_argument("--audit-report", type=Path, default=Path("data/reports/strategy_002_universe_audit.csv"))
    p.add_argument("--universe", type=Path, default=Path("research/universe_candidates.csv"))
    return p.parse_args()


def add_lineage_features(panel: pd.DataFrame) -> pd.DataFrame:
    out = panel.copy().sort_values(["symbol", "timestamp"]).reset_index(drop=True)
    session = out["date"]

    prior_mean = out.groupby(["symbol", session], sort=False)["close"].shift(1).groupby(
        [out["symbol"], session], sort=False
    ).transform(lambda s: s.rolling(30, min_periods=30).mean())
    prior_std = out.groupby(["symbol", session], sort=False)["close"].shift(1).groupby(
        [out["symbol"], session], sort=False
    ).transform(lambda s: s.rolling(30, min_periods=30).std(ddof=1))
    z = (out["close"] - prior_mean) / prior_std.replace(0, np.nan)
    prior_6 = out.groupby(["symbol", session], sort=False)["close"].shift(1)
    prior_7 = out.groupby(["symbol", session], sort=False)["close"].shift(7)
    prior_return_6bar = prior_6 / prior_7 - 1.0
    out["strategy_001_event"] = (z >= 2.0) & (prior_return_6bar > 0)

    one_bar_return = out.groupby(["symbol", session], sort=False)["close"].pct_change(fill_method=None)
    tmp = out[["timestamp", "symbol"]].copy()
    tmp["ret"] = one_bar_return.to_numpy()
    cross = tmp.groupby("timestamp")["ret"].transform(lambda s: (s.sum() - s) / (s.notna().sum() - 1))
    out["strategy_002_prior_loo_residual"] = one_bar_return - cross
    return out.sort_values(["timestamp", "symbol"]).reset_index(drop=True)


def fit_component_transform(train: pd.DataFrame, other: pd.DataFrame, features: list[str]):
    means = train[features].mean()
    stds = train[features].std(ddof=1)
    keep = stds[(stds > 0) & stds.notna()].index.tolist()
    if len(keep) != len(features):
        missing = [f for f in features if f not in keep]
        raise ValueError(f"A registered lineage feature became constant/unusable: {missing}")
    train_x = ((train[keep] - means[keep]) / stds[keep]).to_numpy()
    other_x = ((other[keep] - means[keep]) / stds[keep]).to_numpy()
    return train_x, other_x


def score_spec(panel: pd.DataFrame, features: list[str], name: str, splits: dict[str, pd.Timestamp]):
    target = "target_excess_1bar"
    cols = ["timestamp", "symbol", target] + features
    base = panel[cols].dropna().copy()
    train = base[(base.timestamp >= splits["train_start"]) & (base.timestamp <= splits["train_end"])].copy()
    valid = base[(base.timestamp >= splits["validation_start"]) & (base.timestamp <= splits["validation_end"])].copy()
    test = base[(base.timestamp >= splits["test_start"]) & (base.timestamp <= splits["test_end"])].copy()
    train_x, valid_x = fit_component_transform(train, valid, features)
    _, test_x = fit_component_transform(train, test, features)
    beta = fit_linear(train_x, train[target].to_numpy())
    rows = []
    scored = None
    for split_name, frame, x in [("validation", valid, valid_x), ("development_test", test, test_x)]:
        pred = pd.Series(np.column_stack([np.ones(len(x)), x]) @ beta, index=frame.index)
        rows.append({
            "model": name,
            "split": split_name,
            "features": ";".join(features),
            "feature_count": len(features),
            "usable_timestamps": int(frame.timestamp.nunique()),
            "observations": int(len(frame)),
            "horizon_bars": 1,
            "horizon_minutes": BAR_MINUTES,
            **score_predictions(frame, pred, target),
        })
        if split_name == "development_test":
            scored = frame[["timestamp", "symbol", target]].copy()
            scored["prediction"] = pred.to_numpy()
    return pd.DataFrame(rows), scored


def quintiles(scored: pd.DataFrame, model_name: str) -> pd.DataFrame:
    w = scored.copy()
    w["quintile"] = w.groupby("timestamp").prediction.rank(method="first", pct=True).map(
        lambda x: min(5, int(np.ceil(x * 5)))
    )
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
    panel = add_lineage_features(panel)
    splits = purged_chronological_splits(panel.timestamp)

    metrics = []
    qframes = []
    for name, features in SPECS.items():
        m, scored = score_spec(panel, features, name, splits)
        metrics.append(m)
        qframes.append(quintiles(scored, name))
    metrics_df = pd.concat(metrics, ignore_index=True)
    q_df = pd.concat(qframes, ignore_index=True)
    metrics_df.to_csv(a.output_dir / "lineage_metrics.csv", index=False)
    q_df.to_csv(a.output_dir / "lineage_quintiles.csv", index=False)

    ref = metrics_df[(metrics_df.model == "003h_plus_001_plus_002") & (metrics_df.split == "development_test")].iloc[0]
    rows = []
    for name in SPECS:
        row = metrics_df[(metrics_df.model == name) & (metrics_df.split == "development_test")].iloc[0]
        rows.append({
            "model": name,
            "delta_mean_ic_vs_combined": row.mean_ic - ref.mean_ic,
            "delta_rank_ic_vs_combined": row.mean_rank_ic - ref.mean_rank_ic,
            "delta_spread_bps_vs_combined": row.mean_top_bottom_spread_bps - ref.mean_top_bottom_spread_bps,
            "usable_timestamps": row.usable_timestamps,
        })
    pd.DataFrame(rows).to_csv(a.output_dir / "lineage_attribution_vs_combined.csv", index=False)

    manifest = {
        "experiment": "003H_lineage_separation",
        "core": CORE,
        "lineage_features": LINEAGE,
        "specifications": SPECS,
        "strategy_001_event_definition": "z_score >= 2.0 and prior_return_6bar > 0",
        "strategy_002_definition": "one-bar close-to-close return minus timestamp-level mean of other eligible equities",
        "exploratory_start": str(EXPLORATORY_START.date()),
        "exploratory_end": str(EXPLORATORY_END.date()),
        "project_validation_start": str(VALIDATION_START.date()),
        "final_holdout_start": str(HOLDOUT_START.date()),
        "holdout_used": False,
        "protected_validation_used": False,
        "parameter_search": False,
        "feature_selection": False,
        "new_features": False,
        "new_transforms": False,
        "common_complete_case_support": True,
        "decision_rule": "Lineage falsification only; do not select the highest-performing specification as a trading model.",
        "splits": {k: str(v) if isinstance(v, pd.Timestamp) else v for k, v in splits.items()},
    }
    (a.output_dir / "run_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    print("Strategy 003H lineage separation complete")
    print(f"Eligible equity symbols: {len(frames)}")
    print(f"Specifications: {list(SPECS)}")
    print(f"Outputs: {a.output_dir}")


if __name__ == "__main__":
    main()
