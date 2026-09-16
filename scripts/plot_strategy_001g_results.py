"""Create diagnostic charts from generated Strategy 001G outputs."""

from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("output_dir", type=Path)
    args = parser.parse_args()

    summary = pd.read_csv(args.output_dir / "forward_path_summary.csv")
    excursions = pd.read_csv(args.output_dir / "mfe_mae.csv")

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(summary["horizon_minutes"], summary["mean_return"] * 10_000, marker="o", label="Mean")
    ax.plot(summary["horizon_minutes"], summary["median_return"] * 10_000, marker="o", label="Median")
    ax.axhline(0, linewidth=1)
    ax.set_xlabel("Minutes from signal")
    ax.set_ylabel("Forward return (bps), measured from next-open entry")
    ax.set_title("Strategy 001G Forward-Path Returns")
    ax.legend()
    ax.grid(True, alpha=0.25)
    fig.tight_layout()
    fig.savefig(args.output_dir / "forward_path_returns.png", dpi=160)
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.hist(excursions["mfe_return"].dropna() * 10_000, bins=30, alpha=0.65, label="MFE")
    ax.hist(excursions["mae_return"].dropna() * 10_000, bins=30, alpha=0.65, label="MAE")
    ax.axvline(0, linewidth=1)
    ax.set_xlabel("Excursion from next-open entry (bps)")
    ax.set_ylabel("Trade count")
    ax.set_title("Strategy 001G MFE / MAE Distribution")
    ax.legend()
    ax.grid(True, alpha=0.25)
    fig.tight_layout()
    fig.savefig(args.output_dir / "mfe_mae_distribution.png", dpi=160)
    plt.close(fig)

    print(f"Wrote charts to {args.output_dir}")


if __name__ == "__main__":
    main()
