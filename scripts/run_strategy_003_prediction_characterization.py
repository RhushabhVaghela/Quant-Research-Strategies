"""Characterize the frozen Strategy 003 intraday prediction signal.

This module is descriptive only. It reuses the frozen Strategy 003 OLS/Ridge
discovery design and exploratory/development-test data, without searching
parameters, using the protected validation period, or touching the final holdout.

Diagnostics cover:
- development-test quintile distribution and monotonicity;
- feature-family ablations and coefficient contributions;
- time-of-day stability;
- stock-level stability;
- winsorized/tail sensitivity;
- model score correlation between OLS and Ridge.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd

from scripts.run_strategy_003_prediction_discovery import (
    BASE_FEATURES,
    CONTEXT_FEATURES,
    EXPLORATORY_END,
    EXPLORATORY_START,
    HOLDOUT_START,
    HORIZON_BARS,
    RIDGE_ALPHA,
    VALIDATION_START,
    add_market_context,
    build_panel,
    fit_linear,
    fit_transform,
    load_audit,
    load_candidates,
    load_intraday,
    locked_exploratory_slice,
    purged_chronological_splits,
    session_bar_features,
)


MODEL_FAMILIES = {
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
    "bar_shape_state": [
        "close_location_1bar",
        "intraday_position_60bar",
        "bars_since_session_open",
    ],
    "market_context": [
        "market_return_1bar",
        "market_vol_60bar",
    ],
}


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
        default=Path("data/reports/strategy_003_prediction_characterization"),
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


def _load_locked_panel(args: argparse.Namespace) -> pd.DataFrame:
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
        candidates.loc[
            candidates["category"].isin(equity_categories), "symbol"
        ].astype(str)
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
    if not market_path.exists():
        raise SystemExit(f"Missing required market proxy data file: {market_path}")
    market = load_intraday(market_path)
    return locked_exploratory_slice(build_panel(frames, market))


def _model_features(panel: pd.DataFrame, bases: list[str]) -> list[str]:
    return [
        col
        for base in bases
        for col in (base, f"{base}_rank", f"{base}_cs_z")
        if col in panel.columns
    ]


def _fit_frozen_model(
    panel: pd.DataFrame,
    features: list[str],
) -> tuple[pd.DataFrame, pd.DataFrame]:
    target = "target_excess_1bar"
    base = panel[["timestamp", "date", "symbol", target] + features].dropna(subset=[target]).copy()
    splits = purged_chronological_splits(base["timestamp"])

    train = base[
        (base["timestamp"] >= splits["train_start"])
        & (base["timestamp"] <= splits["train_end"])
    ].copy()
    test = base[
        (base["timestamp"] >= splits["test_start"])
        & (base["timestamp"] <= splits["test_end"])
    ].copy()

    usable = [f for f in features if train[f].notna().any()]
    train = train.dropna(subset=usable)
    test = test.dropna(subset=usable)
    train_x, test_x, kept = fit_transform(train, test, usable)
    y = train[target].to_numpy()

    outputs = []
    for name, alpha in (("ols", None), ("ridge_fixed_alpha", RIDGE_ALPHA)):
        beta = fit_linear(train_x, y, ridge_alpha=alpha)
        pred = np.column_stack([np.ones(len(test_x)), test_x]) @ beta
        scored = test[["timestamp", "date", "symbol", target]].copy()
        scored["prediction"] = pred
        scored["model"] = name
        outputs.append(scored)
    return pd.concat(outputs, ignore_index=True), test


def _quintile_table(scored: pd.DataFrame) -> pd.DataFrame:
    """Return realized excess returns for every prediction quintile.

    Quintiles are formed independently at each timestamp from the frozen
    model score. A minimum cross-section of 10 names is required so each
    quintile has at least two observations. This is descriptive only.
    """
    rows = []
    for model, frame in scored.groupby("model"):
        for ts, group in frame.groupby("timestamp"):
            if len(group) < 10:
                continue
            ordered = group.assign(
                score_rank=group["prediction"].rank(method="first", ascending=True)
            )
            ordered["quintile"] = (
                np.floor((ordered["score_rank"] - 1) * 5 / len(ordered)).astype(int) + 1
            )
            for quintile, qgroup in ordered.groupby("quintile"):
                rows.append(
                    {
                        "model": model,
                        "timestamp": ts,
                        "quintile": int(quintile),
                        "n": int(len(qgroup)),
                        "mean_target_excess_bps": float(
                            qgroup["target_excess_1bar"].mean() * 1e4
                        ),
                        "median_target_excess_bps": float(
                            qgroup["target_excess_1bar"].median() * 1e4
                        ),
                    }
                )
    return pd.DataFrame(rows)


def _quintile_distribution(quintiles: pd.DataFrame) -> pd.DataFrame:
    """Summarize Q5 minus Q1 from the full quintile table."""
    if quintiles.empty:
        return pd.DataFrame(columns=["model", "timestamp", "spread_bps"])
    wide = quintiles.pivot_table(
        index=["model", "timestamp"],
        columns="quintile",
        values="mean_target_excess_bps",
    ).reset_index()
    if 1 not in wide.columns or 5 not in wide.columns:
        return pd.DataFrame(columns=["model", "timestamp", "spread_bps"])
    return wide.dropna(subset=[1, 5]).assign(
        spread_bps=lambda x: x[5] - x[1]
    )[["model", "timestamp", "spread_bps"]]


def _quintile_summary(quintiles: pd.DataFrame) -> pd.DataFrame:
    if quintiles.empty:
        return pd.DataFrame(
            columns=[
                "model",
                "quintile",
                "timestamps",
                "mean_return_bps",
                "median_return_bps",
                "std_return_bps",
                "positive_fraction",
            ]
        )
    grouped = (
        quintiles.groupby(["model", "quintile"])["mean_target_excess_bps"]
        .agg(["count", "mean", "median", "std"])
        .reset_index()
        .rename(
            columns={
                "count": "timestamps",
                "mean": "mean_return_bps",
                "median": "median_return_bps",
                "std": "std_return_bps",
            }
        )
    )
    positive = (
        quintiles.groupby(["model", "quintile"])["mean_target_excess_bps"]
        .apply(lambda x: float((x > 0).mean()))
        .reset_index(name="positive_fraction")
    )
    return grouped.merge(positive, on=["model", "quintile"], how="left")


def _time_of_day_tables(
    scored: pd.DataFrame,
    panel: pd.DataFrame,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Report all registered buckets and distinguish frozen-feature warm-up."""
    buckets = ["09:15-09:59", "10:00-11:59", "12:00-13:59", "14:00-15:30"]
    splits = purged_chronological_splits(
        panel.loc[panel["target_excess_1bar"].notna(), "timestamp"]
    )
    raw = panel[
        (panel["timestamp"] >= splits["test_start"])
        & (panel["timestamp"] <= splits["test_end"])
        & panel["target_excess_1bar"].notna()
    ].copy()
    raw["time_bucket"] = _time_bucket(raw["timestamp"])
    scored_local = scored.copy()
    scored_local["time_bucket"] = _time_bucket(scored_local["timestamp"])

    stability_rows = []
    coverage_rows = []
    for model in sorted(scored["model"].unique()):
        model_scored = scored_local[scored_local["model"] == model]
        for bucket in buckets:
            group = model_scored[model_scored["time_bucket"] == bucket]
            spreads = []
            for _, ts_group in group.groupby("timestamp"):
                if len(ts_group) < 10:
                    continue
                rank = ts_group["prediction"].rank(method="first", pct=True)
                high = ts_group.loc[rank > 0.8, "target_excess_1bar"].mean()
                low = ts_group.loc[rank <= 0.2, "target_excess_1bar"].mean()
                if pd.notna(high) and pd.notna(low):
                    spreads.append((high - low) * 1e4)
            values = pd.Series(spreads, dtype=float)
            stability_rows.append(
                {
                    "model": model,
                    "time_bucket": bucket,
                    "count": int(len(values)),
                    "mean_spread_bps": float(values.mean()) if len(values) else np.nan,
                    "median_spread_bps": float(values.median()) if len(values) else np.nan,
                    "std": float(values.std(ddof=1)) if len(values) > 1 else np.nan,
                    "status": (
                        "scored"
                        if len(values)
                        else "no_usable_scored_observations"
                    ),
                }
            )
            raw_count = int((raw["time_bucket"] == bucket).sum())
            scored_count = int((model_scored["time_bucket"] == bucket).sum())
            coverage_rows.append(
                {
                    "model": model,
                    "time_bucket": bucket,
                    "raw_target_rows": raw_count,
                    "scored_rows": scored_count,
                    "raw_to_scored_row_ratio": (
                        float(scored_count / raw_count) if raw_count else np.nan
                    ),
                    "coverage_note": (
                        "No raw target rows in this bucket."
                        if raw_count == 0
                        else (
                            "Raw targets exist but frozen 60-bar feature warm-up "
                            "or complete-case requirements removed all rows."
                            if scored_count == 0
                            else "Scored observations available."
                        )
                    ),
                }
            )
    return pd.DataFrame(stability_rows), pd.DataFrame(coverage_rows)


def _summary_stats(values: pd.Series, prefix: str = "") -> dict[str, float]:
    x = values.dropna().astype(float)
    if x.empty:
        return {}
    return {
        f"{prefix}count": int(len(x)),
        f"{prefix}mean_bps": float(x.mean()),
        f"{prefix}median_bps": float(x.median()),
        f"{prefix}std_bps": float(x.std(ddof=1)) if len(x) > 1 else np.nan,
        f"{prefix}q10_bps": float(x.quantile(0.10)),
        f"{prefix}q25_bps": float(x.quantile(0.25)),
        f"{prefix}q75_bps": float(x.quantile(0.75)),
        f"{prefix}q90_bps": float(x.quantile(0.90)),
        f"{prefix}positive_fraction": float((x > 0).mean()),
    }


def _winsorized(values: pd.Series, lower: float = 0.01, upper: float = 0.99) -> pd.Series:
    x = values.dropna().astype(float)
    if x.empty:
        return x
    return x.clip(x.quantile(lower), x.quantile(upper))


def _time_bucket(ts: pd.Series) -> pd.Series:
    local = pd.DatetimeIndex(ts).tz_convert("Asia/Kolkata")
    minutes = local.hour * 60 + local.minute
    # pd.cut is right-closed by default. Use the final minute of each
    # bucket as the boundary so 10:00 belongs to the second bucket,
    # 12:00 to the third, and 14:00 to the fourth.
    labels = pd.cut(
        minutes,
        bins=[-1, 10 * 60 - 1, 12 * 60 - 1, 14 * 60 - 1, 15 * 60 + 30],
        labels=["09:15-09:59", "10:00-11:59", "12:00-13:59", "14:00-15:30"],
    )
    return pd.Series(labels.astype(str), index=ts.index)


def main() -> None:
    args = parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)

    panel = _load_locked_panel(args)

    all_bases = BASE_FEATURES + CONTEXT_FEATURES
    all_features = _model_features(panel, all_bases)
    scored, _ = _fit_frozen_model(panel, all_features)

    quintiles = _quintile_table(scored)
    quintiles.to_csv(args.output_dir / "quintile_returns.csv", index=False)
    _quintile_summary(quintiles).to_csv(
        args.output_dir / "quintile_summary.csv", index=False
    )

    distribution = _quintile_distribution(quintiles)

    distribution_rows = []
    for model, frame in distribution.groupby("model"):
        spread = frame["spread_bps"]
        winsor = _winsorized(spread)
        row = {"model": model}
        row.update(_summary_stats(spread, "raw_"))
        row.update(_summary_stats(winsor, "winsorized_"))
        if len(spread):
            row["top_5pct_abs_contribution_bps"] = float(
                spread.abs().nlargest(max(1, int(np.ceil(len(spread) * 0.05)))).sum()
                / len(spread)
            )
        distribution_rows.append(row)
    pd.DataFrame(distribution_rows).to_csv(
        args.output_dir / "spread_distribution.csv", index=False
    )

    tod_summary, tod_coverage = _time_of_day_tables(scored, panel)
    tod_summary.to_csv(
        args.output_dir / "time_of_day_stability.csv", index=False
    )
    tod_coverage.to_csv(
        args.output_dir / "time_of_day_coverage.csv", index=False
    )

    stock_rows = []
    for model, frame in scored.groupby("model"):
        for symbol, group in frame.groupby("symbol"):
            stock_rows.append({
                "model": model,
                "symbol": symbol,
                "n": len(group),
                "mean_target_excess_bps": group["target_excess_1bar"].mean() * 1e4,
                "prediction_target_corr": group["prediction"].corr(group["target_excess_1bar"]),
                "prediction_mean_bps": group["prediction"].mean() * 1e4,
            })
    pd.DataFrame(stock_rows).to_csv(
        args.output_dir / "stock_stability.csv", index=False
    )

    ablation_rows = []
    for family, bases in MODEL_FAMILIES.items():
        features = _model_features(panel, bases)
        family_scored, _ = _fit_frozen_model(panel, features)
        family_quintiles = _quintile_table(family_scored)
        q = _quintile_distribution(family_quintiles)
        for model, frame in q.groupby("model"):
            ablation_rows.append({
                "feature_family": family,
                "feature_count": len(features),
                "model": model,
                "mean_spread_bps": frame["spread_bps"].mean(),
                "median_spread_bps": frame["spread_bps"].median(),
                "positive_timestamp_fraction": float((frame["spread_bps"] > 0).mean()),
                "usable_timestamps": len(frame),
            })
    pd.DataFrame(ablation_rows).to_csv(
        args.output_dir / "feature_family_ablation.csv", index=False
    )

    coeff_rows = []
    target = "target_excess_1bar"
    base = panel[["timestamp", target] + all_features].dropna(subset=[target]).copy()
    splits = purged_chronological_splits(base["timestamp"])
    train = base[
        (base["timestamp"] >= splits["train_start"])
        & (base["timestamp"] <= splits["train_end"])
    ].copy()
    test = base[
        (base["timestamp"] >= splits["test_start"])
        & (base["timestamp"] <= splits["test_end"])
    ].copy()

    usable_features = [feature for feature in all_features if train[feature].notna().any()]
    if len(usable_features) < 3:
        raise ValueError("Too few features with usable training observations for coefficient decomposition")

    train = train.dropna(subset=usable_features)
    test = test.dropna(subset=usable_features)
    train_x, test_x, kept = fit_transform(train, test, usable_features)
    for model, alpha in (("ols", None), ("ridge_fixed_alpha", RIDGE_ALPHA)):
        beta = fit_linear(train_x, train[target].to_numpy(), ridge_alpha=alpha)
        for feature, coefficient in zip(kept, beta[1:]):
            coeff_rows.append({
                "model": model,
                "feature": feature,
                "coefficient_standardized": coefficient,
                "abs_coefficient": abs(coefficient),
            })
    coefficients = pd.DataFrame(coeff_rows)
    coefficients.to_csv(args.output_dir / "model_coefficients.csv", index=False)

    score_wide = scored.pivot_table(
        index=["timestamp", "symbol"], columns="model", values="prediction"
    ).reset_index()
    if {"ols", "ridge_fixed_alpha"}.issubset(score_wide.columns):
        score_corr = score_wide["ols"].corr(score_wide["ridge_fixed_alpha"])
    else:
        score_corr = np.nan

    manifest = {
        "strategy_id": "003",
        "analysis": "intraday_prediction_characterization",
        "status": "characterization_only",
        "frozen_discovery_horizon_bars": HORIZON_BARS,
        "frozen_ridge_alpha": RIDGE_ALPHA,
        "exploratory_window": {
            "start": str(EXPLORATORY_START.date()),
            "end": str(EXPLORATORY_END.date()),
        },
        "project_validation_start": str(VALIDATION_START.date()),
        "final_holdout_start": str(HOLDOUT_START.date()),
        "holdout_used": False,
        "strategy_pnl_calculated": False,
        "parameter_search": False,
        "model_escalation": False,
        "frozen_discovery_models": ["ols", "ridge_fixed_alpha"],
        "characterizations": [
            "spread distribution and winsor sensitivity",
            "quintile-by-quintile monotonicity",
            "time-of-day stability and frozen-feature coverage",
            "stock stability",
            "base feature-family ablations",
            "standardized model coefficient decomposition",
            "OLS-vs-Ridge score correlation",
        ],
        "outputs": [
            "quintile_returns.csv",
            "quintile_summary.csv",
            "spread_distribution.csv",
            "time_of_day_stability.csv",
            "time_of_day_coverage.csv",
            "stock_stability.csv",
            "feature_family_ablation.csv",
            "model_coefficients.csv",
            "run_manifest.json",
        ],
        "repository_resources_consulted": [
            "research/journal/repository_resource_policy.md",
            "trading_resources/Concepts/Data-and-Feature-Engineering-for-Trading.md",
            "trading_resources/Concepts/Trading-with-Machine-Learning-Regression.md",
            "trading_resources/WQU_resources/Financial Economics/Module 2/Lesson 3 - Penalized Regression.ipynb",
        ],
        "note": "Descriptive characterization only; no parameter or feature search.",
        "ols_ridge_prediction_correlation": score_corr,
    }
    (args.output_dir / "run_manifest.json").write_text(
        json.dumps(manifest, indent=2, default=str), encoding="utf-8"
    )

    print("Strategy 003 characterization complete")
    print(f"Outputs: {args.output_dir}")


if __name__ == "__main__":
    main()
