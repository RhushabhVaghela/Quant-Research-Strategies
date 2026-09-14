"""Run Strategy 001 GOLDBEES mean-reversion event study."""
from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd

from src.research.event_study import add_forward_returns
from src.research.mean_reversion import make_mean_reversion_events


def load_ohlcv(path: Path) -> pd.DataFrame:
    df = pd.read_csv(path)
    if "date" not in df.columns:
        raise ValueError("CSV must contain a 'date' column")
    df["date"] = pd.to_datetime(df["date"], utc=True).dt.tz_convert("Asia/Kolkata")
    df = df.set_index("date").sort_index()
    return df


def summarize_events(df: pd.DataFrame, horizons: tuple[int, ...]) -> pd.DataFrame:
    rows = []
    for direction_name, mask, direction in (
        ("all", df["event"], 0),
        ("positive", df["positive_event"], 1),
        ("negative", df["negative_event"], -1),
    ):
        for h in horizons:
            values = df.loc[mask, f"forward_return_{h}bar"].dropna()
            aligned = -direction * values if direction else pd.Series(dtype=float)
            if direction == 0:
                aligned = pd.concat(
                    [
                        -df.loc[df["positive_event"], f"forward_return_{h}bar"].dropna(),
                        df.loc[df["negative_event"], f"forward_return_{h}bar"].dropna(),
                    ]
                )
            n = len(values)
            mean = values.mean() if n else float("nan")
            std = values.std(ddof=1) if n > 1 else float("nan")
            t_stat = mean / (std / (n ** 0.5)) if n > 1 and std > 0 else float("nan")
            rows.append({
                "direction": direction_name,
                "horizon_bars": h,
                "events": int(n),
                "mean_forward_return": mean,
                "median_forward_return": values.median() if n else float("nan"),
                "std_forward_return": std,
                "win_rate_raw": (values > 0).mean() if n else float("nan"),
                "mean_reversion_aligned_return": aligned.mean() if len(aligned) else float("nan"),
                "t_stat_mean_raw": t_stat,
                "p10_forward_return": values.quantile(0.10) if n else float("nan"),
                "p90_forward_return": values.quantile(0.90) if n else float("nan"),
            })
    return pd.DataFrame(rows)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("csv", type=Path)
    parser.add_argument("--lookback", type=int, default=30)
    parser.add_argument("--z-threshold", type=float, default=2.0)
    parser.add_argument("--output-dir", type=Path, default=Path("data/reports/goldbees_mean_reversion"))
    args = parser.parse_args()

    horizons = (1, 3, 6, 12)
    df = load_ohlcv(args.csv)
    events = make_mean_reversion_events(df, args.lookback, args.z_threshold)
    events = add_forward_returns(events, horizons)
    summary = summarize_events(events, horizons)

    args.output_dir.mkdir(parents=True, exist_ok=True)
    events.to_csv(args.output_dir / "event_observations.csv")
    summary.to_csv(args.output_dir / "event_summary.csv", index=False)
    metadata = pd.DataFrame([{
        "input": str(args.csv),
        "rows": len(df),
        "sessions": df.index.date.astype("datetime64[D]").nunique(),
        "lookback_bars": args.lookback,
        "z_threshold": args.z_threshold,
        "total_events": int(events["event"].sum()),
        "positive_events": int(events["positive_event"].sum()),
        "negative_events": int(events["negative_event"].sum()),
    }])
    metadata.to_csv(args.output_dir / "metadata.csv", index=False)
    print(summary.to_string(index=False))
    print(f"\nWrote research outputs to {args.output_dir}")


if __name__ == "__main__":
    main()
