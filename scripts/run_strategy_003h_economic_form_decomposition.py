"""Run the preregistered Strategy 003H economic-form decomposition.

Development-only final exploratory gate for the current 003H core.
Tests exactly four fixed representations of the two locked variables.
No protected validation/holdout access, feature search, threshold search,
holding-period search, cost optimization, nonlinear escalation, or portfolio.
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
    load_audit,
    load_candidates,
    load_intraday,
    locked_exploratory_slice,
    purged_chronological_splits,
    score_predictions,
)

FEATURES = ["close_location_1bar", "intraday_position_60bar"]
SPECS = {
    "close_location_only": ["close_location_1bar"],
    "intraday_position_only": ["intraday_position_60bar"],
    "additive_core": ["close_location_1bar", "intraday_position_60bar"],
    "joint_interaction": [
        "close_location_1bar",
        "intraday_position_60bar",
        "close_location_x_intraday_position",
    ],
}


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("directory", type=Path, nargs="?", default=Path("data/raw/strategy_002_universe"))
    p.add_argument(
        "--output-dir",
        type=Path,
        default=Path("data/reports/strategy_003h_economic_form_decomposition"),
    )
    p.add_argument(
        "--audit-report",
        type=Path,
        default=Path("data/reports/strategy_002_universe_audit.csv"),
    )
    p.add_argument("--universe", type=Path, default=Path("research/universe_candidates.csv"))
    return p.parse_args()


def fit_component_transform(
    train: pd.DataFrame, other: pd.DataFrame, features: list[str]
) -> tuple[np.ndarray, np.ndarray]:
    means = train[features].mean()
    stds = train[features].std(ddof=1)
    keep = stds[(stds > 0) & stds.notna()].index.tolist()
    if keep != features:
        missing = [f for f in features if f not in keep]
        raise ValueError(f"Registered feature became constant/unusable: {missing}")
    train_x = ((train[features] - means[features]) / stds[features]).to_numpy()
    other_x = ((other[features] - means[features]) / stds[features]).to_numpy()
    return train_x, other_x


def score_spec(
    panel: pd.DataFrame,
    spec_name: str,
    features: list[str],
    splits: dict[str, pd.Timestamp],
):
    target = "target_excess_1bar"
    cols = ["timestamp", "symbol", target] + features
    base = panel[cols].dropna().copy()
    train = base[
        (base.timestamp >= splits["train_start"]) & (base.timestamp <= splits["train_end"])
    ].copy()
    valid = base[
        (base.timestamp >= splits["validation_start"])
        & (base.timestamp <= splits["validation_end"])
    ].copy()
    test = base[
        (base.timestamp >= splits["test_start"]) & (base.timestamp <= splits["test_end"])
    ].copy()

    train_x, valid_x = fit_component_transform(train, valid, features)
    _, test_x = fit_component_transform(train, test, features)

    beta = fit_linear(train_x, train[target].to_numpy())
    rows = []
    scored = None

    for split_name, frame, x in [
        ("validation", valid, valid_x),
        ("development_test", test, test_x),
    ]:
        prediction = pd.Series(
            np.column_stack([np.ones(len(x)), x]) @ beta, index=frame.index
        )
        diag = score_predictions(frame, prediction, target)
        rows.append(
            {
                "model": spec_name,
                "split": split_name,
                "features": ";".join(features),
                "feature_count": len(features),
                "usable_timestamps": int(frame.timestamp.nunique()),
                "observations": int(len(frame)),
                "horizon_bars": HORIZON_BARS,
                "horizon_minutes": BAR_MINUTES * HORIZON_BARS,
                **diag,
            }
        )
        if split_name == "development_test":
            scored = frame[["timestamp", "symbol", target]].copy()
            scored["prediction"] = prediction.to_numpy()

    interaction_beta = np.nan
    if "close_location_x_intraday_position" in features:
        interaction_beta = float(beta[-1])

    return pd.DataFrame(rows), scored, interaction_beta


def quintiles(scored: pd.DataFrame, model_name: str) -> pd.DataFrame:
    work = scored.copy()
    work["quintile"] = work.groupby("timestamp").prediction.rank(
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
        .assign(model=model_name)
    )


def main() -> None:
    a = parse_args()
    a.output_dir.mkdir(parents=True, exist_ok=True)

    candidates = load_candidates(a.universe)
    audit = load_audit(a.audit_report)
    eligible = set(
        audit.loc[
            (audit.unexpected_interval_count == 0) & (audit.zero_volume_rows == 0), "symbol"
        ].astype(str)
    )
    symbols = set(
        candidates.loc[
            candidates.category.isin({"large_cap_equity", "liquid_auto"}), "symbol"
        ].astype(str)
    ) & eligible

    if "NIFTYBEES" not in eligible:
        raise SystemExit("NIFTYBEES is required as the market reference")

    frames = {
        symbol: load_intraday(a.directory / f"NSE_{symbol}_5minute.csv")
        for symbol in sorted(symbols)
    }
    market = load_intraday(a.directory / "NSE_NIFTYBEES_5minute.csv")
    panel = locked_exploratory_slice(build_panel(frames, market))

    panel["close_location_x_intraday_position"] = (
        panel["close_location_1bar"] * panel["intraday_position_60bar"]
    )

    # Enforce identical complete-case support for the two locked raw variables.
    panel = panel.dropna(subset=FEATURES).copy()
    splits = purged_chronological_splits(panel.timestamp)

    metrics = []
    quintile_frames = []
    interaction_rows = []

    for name, features in SPECS.items():
        m, scored, interaction_beta = score_spec(panel, name, features, splits)
        metrics.append(m)
        quintile_frames.append(quintiles(scored, name))
        interaction_rows.append(
            {
                "model": name,
                "interaction_coefficient_standardized": interaction_beta,
            }
        )

    metrics_df = pd.concat(metrics, ignore_index=True)
    quintiles_df = pd.concat(quintile_frames, ignore_index=True)
    coef_df = pd.DataFrame(interaction_rows)

    metrics_df.to_csv(a.output_dir / "form_metrics.csv", index=False)
    quintiles_df.to_csv(a.output_dir / "form_quintiles.csv", index=False)
    coef_df.to_csv(a.output_dir / "interaction_coefficients.csv", index=False)

    dev = metrics_df[metrics_df.split == "development_test"].copy()
    ref = dev.loc[dev.model == "additive_core"].iloc[0]
    deltas = []
    for _, row in dev.iterrows():
        deltas.append(
            {
                "model": row.model,
                "delta_mean_ic_vs_additive": row.mean_ic - ref.mean_ic,
                "delta_rank_ic_vs_additive": row.mean_rank_ic - ref.mean_rank_ic,
                "delta_spread_bps_vs_additive": (
                    row.mean_top_bottom_spread_bps - ref.mean_top_bottom_spread_bps
                ),
                "usable_timestamps": row.usable_timestamps,
            }
        )
    pd.DataFrame(deltas).to_csv(
        a.output_dir / "form_attribution_vs_additive.csv", index=False
    )

    manifest = {
        "experiment": "003H_economic_form_decomposition",
        "locked_features": FEATURES,
        "specifications": SPECS,
        "interaction_definition": "close_location_1bar * intraday_position_60bar",
        "exploratory_start": str(EXPLORATORY_START.date()),
        "exploratory_end": str(EXPLORATORY_END.date()),
        "project_validation_start": str(VALIDATION_START.date()),
        "final_holdout_start": str(HOLDOUT_START.date()),
        "horizon_bars": HORIZON_BARS,
        "horizon_minutes": BAR_MINUTES * HORIZON_BARS,
        "common_support": True,
        "protected_validation_used": False,
        "holdout_used": False,
        "parameter_search": False,
        "feature_selection": False,
        "new_feature_families": False,
        "new_lookbacks": False,
        "threshold_search": False,
        "holding_period_search": False,
        "cost_optimization": False,
        "nonlinear_search": False,
        "portfolio_construction": False,
        "decision_rule": (
            "Explanatory decomposition only. The joint model may not be selected "
            "solely because it has the largest development metric."
        ),
        "splits": {
            k: str(v) if isinstance(v, pd.Timestamp) else v for k, v in splits.items()
        },
    }
    (a.output_dir / "run_manifest.json").write_text(
        json.dumps(manifest, indent=2, default=str), encoding="utf-8"
    )

    print("Strategy 003H economic-form decomposition complete")
    print(f"Eligible equity symbols: {len(frames)}")
    print(f"Specifications: {list(SPECS)}")
    print(f"Outputs: {a.output_dir}")


if __name__ == "__main__":
    main()
