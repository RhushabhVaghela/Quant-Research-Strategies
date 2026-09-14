"""Plot Strategy 001 event-study outputs."""
from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("summary_csv", type=Path)
    parser.add_argument("--output-dir", type=Path, default=None)
    args = parser.parse_args()

    summary = pd.read_csv(args.summary_csv)
    output_dir = args.output_dir or args.summary_csv.parent
    output_dir.mkdir(parents=True, exist_ok=True)

    all_rows = summary[summary["direction"] == "all"].copy()
    plt.figure(figsize=(8, 5))
    for direction in ("positive", "negative"):
        rows = summary[summary["direction"] == direction]
        plt.plot(rows["horizon_bars"], rows["mean_reversion_aligned_return"], marker="o", label=direction)
    plt.axhline(0, linewidth=1)
    plt.xlabel("Forward horizon (bars)")
    plt.ylabel("Mean reversion-aligned return")
    plt.title("GOLDBEES mean-reversion event study")
    plt.legend()
    plt.tight_layout()
    plt.savefig(output_dir / "mean_reversion_by_direction.png", dpi=160)
    plt.close()

    plt.figure(figsize=(8, 5))
    plt.plot(all_rows["horizon_bars"], all_rows["mean_forward_return"], marker="o")
    plt.axhline(0, linewidth=1)
    plt.xlabel("Forward horizon (bars)")
    plt.ylabel("Mean raw forward return")
    plt.title("GOLDBEES raw event outcomes")
    plt.tight_layout()
    plt.savefig(output_dir / "mean_forward_return.png", dpi=160)
    plt.close()

    print(f"Wrote charts to {output_dir}")


if __name__ == "__main__":
    main()
