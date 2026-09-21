"""Summarize Strategy 002 residual temporal-conditioning results and apply the preregistered gate."""
from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd

PERIODS = ("Q1_time", "Q2_time", "Q3_time", "Q4_time")


def parse_args():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("directory", type=Path)
    p.add_argument(
        "--output",
        type=Path,
        default=None,
        help="Markdown output path; defaults to <directory>/summary.md",
    )
    return p.parse_args()


def main():
    args = parse_args()
    breadth_path = args.directory / "residual_temporal_conditioning_breadth.csv"
    manifest_path = args.directory / "run_manifest.json"
    if not breadth_path.exists() or not manifest_path.exists():
        raise SystemExit("Expected breadth CSV and run_manifest.json are missing")

    breadth = pd.read_csv(breadth_path)
    manifest = pd.read_json(manifest_path, typ="series")

    if bool(manifest.get("holdout_used", True)):
        raise SystemExit("Refusing to summarize: holdout_used is not false")
    if bool(manifest.get("strategy_pnl_calculated", True)):
        raise SystemExit("Refusing to summarize: strategy_pnl_calculated is not false")
    if bool(manifest.get("optimization_performed", True)):
        raise SystemExit("Refusing to summarize: optimization_performed is not false")

    primary = breadth[
        (breadth["component"] == "close_to_close")
        & (breadth["horizon_bars"] == 1)
        & (breadth["condition"].isin(["prior_negative", "prior_positive"]))
    ].copy()

    lines = [
        "# Strategy 002 — Residual Temporal Conditioning Summary",
        "",
        "**Purpose:** Review the preregistered chronological-stability gate before opening validation.",
        "",
        "## Research controls",
        "",
        f"- Exploratory period: {manifest['exploratory_start']} through {manifest['exploratory_end']}",
        f"- Included instruments: {len(manifest['included_instruments']) if isinstance(manifest.get('included_instruments'), list) else 'see manifest'}",
        "- Validation used: false",
        "- Holdout used: false",
        "- Strategy P&L calculated: false",
        "- Optimization performed: false",
        "",
        "## One-bar conditional residual reversal by period",
        "",
        "| Period | Condition | Median instrument mean (bps) | Positive-instrument fraction |",
        "|---|---|---:|---:|",
    ]

    for period in PERIODS:
        for condition in ("prior_negative", "prior_positive"):
            row = primary[
                (primary["period"] == period) & (primary["condition"] == condition)
            ]
            if row.empty:
                continue
            r = row.iloc[0]
            mean_bps = 1e4 * float(r["median_instrument_mean"])
            breadth = 100 * float(r["positive_instrument_fraction"])
            lines.append(
                f"| {period} | {condition} | {mean_bps:.4f} | {breadth:.1f}% |"
            )

    lines += [
        "",
        "## Gate interpretation",
        "",
        "The primary temporal-stability gate is not a profitability test. Review whether the negative-residual condition remains positive and the positive-residual condition remains negative across chronological periods, without selecting a favorable period.",
        "",
        "This summary does not authorize validation or live trading. A mixed/sign-changing result should remain unresolved rather than being repaired through parameter changes.",
        "",
        "## Next step",
        "",
        "If the chronological pattern is directionally coherent and broad, document the finding and proceed to the fixed-baseline validation runner. If it is materially unstable, record the result and do not open validation for this candidate.",
    ]

    output = args.output or (args.directory / "summary.md")
    output.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {output}")


if __name__ == "__main__":
    main()
