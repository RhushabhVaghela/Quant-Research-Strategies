"""Build the formation-only candidate pair set for Strategy 002.

No development or holdout data is read. Pair eligibility is determined only
from the frozen 20-session formation window and the locked U1 universe.
"""

from __future__ import annotations

import argparse
from datetime import timedelta
from itertools import combinations
from pathlib import Path

import numpy as np
import pandas as pd

from scripts.run_strategy_001j_baseline import (
    apply_point_in_time_membership,
    load_membership,
    load_symbol_csv,
)

FORMATION_START = "2026-05-12"
FORMATION_END = "2026-06-09"
MIN_RETURN_CORRELATION = 0.75
MIN_HALF_LIFE_BARS = 2.0
MAX_HALF_LIFE_BARS = 120.0
MAX_PAIRS = 20
MAX_PAIRS_PER_SYMBOL = 2


def _window(value: str, end_of_day: bool = False) -> pd.Timestamp:
    ts = pd.Timestamp(value).tz_localize("Asia/Kolkata")
    if end_of_day:
        ts += timedelta(days=1)
    return ts


def _load_frames(membership_path: Path, input_dir: Path) -> dict[str, pd.DataFrame]:
    membership = load_membership(membership_path)
    start = _window(FORMATION_START)
    end = _window(FORMATION_END, end_of_day=True)
    frames: dict[str, pd.DataFrame] = {}
    for symbol in sorted(membership["symbol"].unique()):
        path = input_dir / f"{symbol}.csv"
        if not path.exists():
            raise SystemExit(f"Missing U1 data for {symbol}: {path}")
        raw = load_symbol_csv(path, None, start, end)
        frames[symbol] = apply_point_in_time_membership(symbol, raw, membership)
    return frames


def _pair_stats(a: pd.DataFrame, b: pd.DataFrame) -> dict[str, float | int] | None:
    joined = pd.concat(
        [a["close"].rename("a"), b["close"].rename("b")],
        axis=1,
        join="inner",
    ).dropna()
    if len(joined) < 500:
        return None

    log_a = np.log(joined["a"].astype(float))
    log_b = np.log(joined["b"].astype(float))
    returns = pd.concat(
        [log_a.diff().rename("ra"), log_b.diff().rename("rb")],
        axis=1,
    ).dropna()
    if len(returns) < 400:
        return None

    corr = float(returns["ra"].corr(returns["rb"]))
    if not np.isfinite(corr) or corr < MIN_RETURN_CORRELATION:
        return None

    x = log_b.to_numpy()
    y = log_a.to_numpy()
    beta = float(np.cov(x, y, ddof=1)[0, 1] / np.var(x, ddof=1))
    spread = y - beta * x
    lag = spread[:-1]
    delta = np.diff(spread)
    lag_centered = lag - lag.mean()
    delta_centered = delta - delta.mean()
    denom = float(np.dot(lag_centered, lag_centered))
    if denom <= 0:
        return None
    kappa = float(np.dot(lag_centered, delta_centered) / denom)
    if not np.isfinite(kappa) or not (-1.0 < kappa < 0.0):
        return None
    ar1 = 1.0 + kappa

    half_life = float(-np.log(2.0) / np.log(ar1))
    if not (MIN_HALF_LIFE_BARS <= half_life <= MAX_HALF_LIFE_BARS):
        return None

    spread_std = float(np.std(spread, ddof=1))
    if not np.isfinite(spread_std) or spread_std <= 0:
        return None

    return {
        "overlap_bars": int(len(joined)),
        "return_correlation": corr,
        "hedge_beta": beta,
        "ar1": ar1,
        "half_life_bars": half_life,
        "spread_std": spread_std,
    }


def select_pairs(frames: dict[str, pd.DataFrame]) -> pd.DataFrame:
    rows: list[dict] = []
    for a_symbol, b_symbol in combinations(sorted(frames), 2):
        stats = _pair_stats(frames[a_symbol], frames[b_symbol])
        if stats is None:
            continue
        rows.append({"symbol_a": a_symbol, "symbol_b": b_symbol, **stats})

    candidates = pd.DataFrame(rows)
    if candidates.empty:
        return pd.DataFrame(
            columns=[
                "pair_id", "symbol_a", "symbol_b", "overlap_bars",
                "return_correlation", "hedge_beta", "ar1",
                "half_life_bars", "spread_std",
            ]
        )

    candidates = candidates.sort_values(
        ["return_correlation", "overlap_bars", "half_life_bars"],
        ascending=[False, False, True],
        kind="mergesort",
    )

    selected: list[dict] = []
    counts: dict[str, int] = {}
    for row in candidates.to_dict("records"):
        a = row["symbol_a"]
        b = row["symbol_b"]
        if counts.get(a, 0) >= MAX_PAIRS_PER_SYMBOL:
            continue
        if counts.get(b, 0) >= MAX_PAIRS_PER_SYMBOL:
            continue
        selected.append(row)
        counts[a] = counts.get(a, 0) + 1
        counts[b] = counts.get(b, 0) + 1
        if len(selected) >= MAX_PAIRS:
            break

    out = pd.DataFrame(selected)
    if out.empty:
        return candidates.head(0).copy()
    out.insert(0, "pair_id", [f"002P{i:02d}" for i in range(1, len(out) + 1)])
    return out


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--membership", default="data/universe/strategy_001j_u1_membership.csv")
    parser.add_argument("--input-dir", default="data/raw/strategy_001j_u1")
    parser.add_argument(
        "--output-dir",
        default="data/universe/strategy_002_pairs",
    )
    args = parser.parse_args()

    output = Path(args.output_dir)
    output.mkdir(parents=True, exist_ok=True)
    frames = _load_frames(Path(args.membership), Path(args.input_dir))
    pairs = select_pairs(frames)

    pairs.to_csv(output / "formation_pairs.csv", index=False)
    pd.DataFrame(
        [{
            "formation_start": FORMATION_START,
            "formation_end": FORMATION_END,
            "universe_symbols": len(frames),
            "return_correlation_floor": MIN_RETURN_CORRELATION,
            "half_life_min_bars": MIN_HALF_LIFE_BARS,
            "half_life_max_bars": MAX_HALF_LIFE_BARS,
            "max_pairs": MAX_PAIRS,
            "max_pairs_per_symbol": MAX_PAIRS_PER_SYMBOL,
            "selection_rule": "formation-only; sort by return correlation, then overlap, then half-life; cap two pairs per symbol",
            "development_access": "none",
            "holdout_access": "none",
        }]
    ).to_csv(output / "formation_metadata.csv", index=False)

    print(
        f"Strategy 002 formation pair selection complete: {len(pairs)} pair(s) selected."
    )
    print(f"Results: {output / 'formation_pairs.csv'}")
    print("No development or holdout data was loaded.")


if __name__ == "__main__":
    main()
