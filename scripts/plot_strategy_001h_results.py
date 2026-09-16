"""Create diagnostic charts from Strategy 001H outputs."""

from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

from src.research.strategy_001h_robustness import add_period


PERIOD_ORDER = ["2025_H1", "2025_H2", "2026_H1", "2026_H2"]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("output_dir", type=Path)
    args = parser.parse_args()

    chronological = pd.read_csv(args.output_dir / "chronological_performance.csv")
    holdout = pd.read_csv(args.output_dir / "development_vs_holdout.csv")
    costs = pd.read_csv(args.output_dir / "cost_sensitivity.csv")
    activity = pd.read_csv(args.output_dir / "trading_activity.csv")
    trades = pd.read_csv(args.output_dir / "trades.csv")
    daily = pd.read_csv(args.output_dir / "daily_equity.csv")

    # The trade export intentionally contains only frozen-trade fields, not the
    # derived period label. Recreate that label from the original signal time.
    trades = add_period(trades)

    # 1. Chronological gross performance.
    fig, ax = plt.subplots(figsize=(8, 5))
    ordered = chronological.set_index("period").reindex(PERIOD_ORDER).reset_index()
    ax.bar(ordered["period"], ordered["cumulative_gross_return"] * 100)
    ax.axhline(0, linewidth=1)
    ax.set_xlabel("Chronological period")
    ax.set_ylabel("Cumulative gross return (%)")
    ax.set_title("Strategy 001H Chronological Gross Performance")
    ax.grid(True, axis="y", alpha=0.25)
    fig.tight_layout()
    fig.savefig(args.output_dir / "chronological_performance.png", dpi=160)
    plt.close(fig)

    # 2. Development vs chronological holdout.
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.bar(holdout["period"], holdout["cumulative_gross_return"] * 100)
    ax.axhline(0, linewidth=1)
    ax.set_xlabel("Sample designation")
    ax.set_ylabel("Cumulative gross return (%)")
    ax.set_title("Development vs Chronological Holdout")
    ax.grid(True, axis="y", alpha=0.25)
    fig.tight_layout()
    fig.savefig(args.output_dir / "development_vs_holdout.png", dpi=160)
    plt.close(fig)

    # 3. Cost sensitivity.
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(costs["round_trip_friction_bps"], costs["cumulative_net_return"] * 100, marker="o")
    ax.axhline(0, linewidth=1)
    ax.set_xlabel("Round-trip friction (bps)")
    ax.set_ylabel("Cumulative net return (%)")
    ax.set_title("Strategy 001H Cost Sensitivity")
    ax.grid(True, alpha=0.25)
    fig.tight_layout()
    fig.savefig(args.output_dir / "cost_sensitivity.png", dpi=160)
    plt.close(fig)

    # 4. Trade-return distributions by fixed chronological period.
    groups = []
    labels = []
    for period in PERIOD_ORDER:
        values = trades.loc[trades["period"] == period, "gross_return"].dropna() * 10_000
        if len(values):
            groups.append(values.to_numpy())
            labels.append(period)
    fig, ax = plt.subplots(figsize=(8, 5))
    if groups:
        ax.boxplot(groups, tick_labels=labels, showfliers=False)
    ax.axhline(0, linewidth=1)
    ax.set_xlabel("Chronological period")
    ax.set_ylabel("Trade gross return (bps)")
    ax.set_title("Strategy 001H Trade-Return Distribution")
    ax.grid(True, axis="y", alpha=0.25)
    fig.tight_layout()
    fig.savefig(args.output_dir / "trade_return_distributions.png", dpi=160)
    plt.close(fig)

    # 5. Trading activity.
    fig, ax = plt.subplots(figsize=(8, 5))
    ordered_activity = activity.set_index("period").reindex(PERIOD_ORDER).reset_index()
    ax.bar(ordered_activity["period"], ordered_activity["trades_per_active_day"])
    ax.set_xlabel("Chronological period")
    ax.set_ylabel("Trades per active day")
    ax.set_title("Strategy 001H Trading Activity")
    ax.grid(True, axis="y", alpha=0.25)
    fig.tight_layout()
    fig.savefig(args.output_dir / "trading_activity.png", dpi=160)
    plt.close(fig)

    # 6. Daily equity and drawdown on the completed-trade daily proxy.
    if len(daily):
        fig, ax = plt.subplots(figsize=(9, 5))
        ax.plot(pd.to_datetime(daily["date"]), daily["equity"])
        ax.set_xlabel("Date")
        ax.set_ylabel("Equity (gross, normalized)")
        ax.set_title("Strategy 001H Daily Completed-Trade Equity")
        ax.grid(True, alpha=0.25)
        fig.tight_layout()
        fig.savefig(args.output_dir / "daily_equity.png", dpi=160)
        plt.close(fig)

        fig, ax = plt.subplots(figsize=(9, 4))
        ax.plot(pd.to_datetime(daily["date"]), daily["drawdown"] * 100)
        ax.axhline(0, linewidth=1)
        ax.set_xlabel("Date")
        ax.set_ylabel("Drawdown (%)")
        ax.set_title("Strategy 001H Daily Completed-Trade Drawdown")
        ax.grid(True, alpha=0.25)
        fig.tight_layout()
        fig.savefig(args.output_dir / "daily_drawdown.png", dpi=160)
        plt.close(fig)

    print(f"Wrote Strategy 001H charts to {args.output_dir}")


if __name__ == "__main__":
    main()
