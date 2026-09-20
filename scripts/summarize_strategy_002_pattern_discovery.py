"""Summarize Strategy 002 exploratory pattern diagnostics without selecting a strategy.

This report is descriptive only. It reads outputs produced by the locked
exploratory pattern-discovery runner and does not read validation/holdout data.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import pandas as pd


EXPECTED = {
    "return_dynamics.csv",
    "forward_horizon_diagnostics.csv",
    "intraday_diagnostics.csv",
    "cross_sectional_correlation.csv",
    "daily_correlation.csv",
    "lead_lag_diagnostics.csv",
    "cross_sectional_dispersion.csv",
    "pca_explained_variance.csv",
    "run_manifest.json",
}


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("directory", type=Path)
    p.add_argument("--output", type=Path)
    return p.parse_args()


def q(s: pd.Series) -> dict[str, float]:
    s = pd.to_numeric(s, errors="coerce").dropna()
    if s.empty:
        return {"n": 0}
    return {
        "n": int(s.size),
        "median": float(s.median()),
        "mean": float(s.mean()),
        "q25": float(s.quantile(0.25)),
        "q75": float(s.quantile(0.75)),
        "min": float(s.min()),
        "max": float(s.max()),
    }


def signed_consistency(s: pd.Series) -> str:
    s = pd.to_numeric(s, errors="coerce").dropna()
    if s.empty:
        return "no observations"
    pos = int((s > 0).sum())
    neg = int((s < 0).sum())
    zero = int((s == 0).sum())
    return f"positive={pos}, negative={neg}, zero={zero}"


def main() -> None:
    args = parse_args()
    missing = sorted(EXPECTED - {p.name for p in args.directory.iterdir()})
    if missing:
        raise SystemExit(f"Missing discovery outputs: {missing}")

    manifest = json.loads((args.directory / "run_manifest.json").read_text(encoding="utf-8"))
    if manifest.get("holdout_used") is not False:
        raise SystemExit("Refusing to summarize: manifest does not state holdout_used=false")
    if manifest.get("strategy_pnl_calculated") is not False:
        raise SystemExit("Refusing to summarize: strategy P&L was calculated")

    dynamics = pd.read_csv(args.directory / "return_dynamics.csv")
    forward = pd.read_csv(args.directory / "forward_horizon_diagnostics.csv")
    corr = pd.read_csv(args.directory / "cross_sectional_correlation.csv")
    daily_corr = pd.read_csv(args.directory / "daily_correlation.csv")
    lead = pd.read_csv(args.directory / "lead_lag_diagnostics.csv")
    pca = pd.read_csv(args.directory / "pca_explained_variance.csv")

    lines = [
        "# Strategy 002 — Exploratory Pattern Discovery Summary",
        "",
        "**Status:** descriptive/exploratory only. No hypothesis or strategy selected.",
        "",
        "## Research controls",
        "",
        f"- Exploratory window: {manifest['exploratory_start']} through {manifest['exploratory_end']}",
        f"- Instruments included: {len(manifest.get('included_symbols', []))}",
        f"- Instruments excluded: {len(manifest.get('excluded_symbols', []))}",
        "- Holdout used: **false**",
        "- Strategy P&L calculated: **false**",
        "",
        "## 1. Return dynamics",
        "",
        "The table below describes the cross-instrument distribution of autocorrelation diagnostics. It does not identify a preferred lag or instrument.",
        "",
        "| Lag | Median return ACF | Q25 | Q75 | Median absolute-return ACF | Q25 | Q75 |",
        "|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for lag, g in dynamics.groupby("lag_bars", sort=True):
        a = q(g["return_autocorr"])
        v = q(g["absolute_return_autocorr"])
        lines.append(f"| {lag} | {a.get('median', float('nan')):.6f} | {a.get('q25', float('nan')):.6f} | {a.get('q75', float('nan')):.6f} | {v.get('median', float('nan')):.6f} | {v.get('q25', float('nan')):.6f} | {v.get('q75', float('nan')):.6f} |")

    lines += [
        "",
        "## 2. Forward-horizon behavior",
        "",
        "Conditional forward-return distributions are shown by state and horizon. Differences here are exploratory and are not entry/exit rules.",
        "",
        "| State | Bucket | Horizon | Median forward return | Q25 | Q75 | Sign counts |",
        "|---|---|---:|---:|---:|---:|---|",
    ]
    grouped = forward.groupby(["state", "bucket", "horizon_bars"], sort=True)
    for (state, bucket, horizon), g in grouped:
        s = pd.to_numeric(g["mean_forward_return"], errors="coerce")
        stats = q(s)
        lines.append(f"| {state} | {bucket} | {horizon} | {stats.get('median', float('nan')):.8f} | {stats.get('q25', float('nan')):.8f} | {stats.get('q75', float('nan')):.8f} | {signed_consistency(s)} |")

    lines += [
        "",
        "## 3. Cross-sectional dependence",
        "",
        f"- 5-minute pair correlations: {len(corr)} directional-free pairs.",
        f"- Daily pair correlations: {len(daily_corr)} pairs.",
        "",
        "| Diagnostic | Median | Q25 | Q75 | Min | Max |",
        "|---|---:|---:|---:|---:|---:|",
    ]
    for name, frame in [("5-minute correlation", corr), ("Daily correlation", daily_corr)]:
        stats = q(frame["correlation"])
        lines.append(f"| {name} | {stats.get('median', float('nan')):.6f} | {stats.get('q25', float('nan')):.6f} | {stats.get('q75', float('nan')):.6f} | {stats.get('min', float('nan')):.6f} | {stats.get('max', float('nan')):.6f} |")

    lines += [
        "",
        "## 4. Lead-lag diagnostics",
        "",
        "These are directional dependence diagnostics only. They are not treated as arbitrage evidence.",
        "",
        "| Lag | Median correlation | Q25 | Q75 | Min | Max |",
        "|---:|---:|---:|---:|---:|---:|",
    ]
    for lag, g in lead.groupby("lag_bars", sort=True):
        stats = q(g["correlation"])
        lines.append(f"| {lag} | {stats.get('median', float('nan')):.6f} | {stats.get('q25', float('nan')):.6f} | {stats.get('q75', float('nan')):.6f} | {stats.get('min', float('nan')):.6f} | {stats.get('max', float('nan')):.6f} |")

    lines += [
        "",
        "## 5. PCA/common-factor structure",
        "",
        "| Component | Explained variance | Cumulative explained variance |",
        "|---:|---:|---:|",
    ]
    for _, row in pca.head(10).iterrows():
        lines.append(f"| {int(row['component'])} | {row['explained_variance_ratio']:.6f} | {row['cumulative_explained_variance']:.6f} |")

    lines += [
        "",
        "## Interpretation guardrails",
        "",
        "- This summary does not rank instruments or declare a winning pattern.",
        "- No parameter, threshold, holding period, or strategy rule is selected here.",
        "- Any potentially interesting pattern must be characterized for breadth, stability, economic mechanism, and execution implications before a hypothesis is written.",
        "- Development validation and the final chronological holdout remain untouched.",
    ]

    report = "\n".join(lines) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(report, encoding="utf-8")
    else:
        print(report)


if __name__ == "__main__":
    main()
