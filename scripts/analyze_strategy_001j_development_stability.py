"""Analyze preregistered Strategy 001J development results before holdout.

This script does not inspect the chronological holdout and does not choose a
candidate automatically. It evaluates each configuration on the development
trade ledger using chronological subperiods and cross-sectional breadth.

The purpose is to prevent selection on a single aggregate metric such as
profit factor or cumulative return.
"""

from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import pandas as pd

DEVELOPMENT_START = pd.Timestamp("2026-06-10", tz="Asia/Kolkata")
DEVELOPMENT_END = pd.Timestamp("2026-08-19", tz="Asia/Kolkata")
DEVELOPMENT_END_EXCLUSIVE = pd.Timestamp("2026-08-20", tz="Asia/Kolkata")
PERIODS = {
    "dev_early": (DEVELOPMENT_START, pd.Timestamp("2026-07-06", tz="Asia/Kolkata")),
    "dev_middle": (pd.Timestamp("2026-07-07", tz="Asia/Kolkata"), pd.Timestamp("2026-07-31", tz="Asia/Kolkata")),
    "dev_late": (pd.Timestamp("2026-08-01", tz="Asia/Kolkata"), DEVELOPMENT_END_EXCLUSIVE),
}


def _load_trades(path: Path) -> pd.DataFrame:
    df = pd.read_csv(path)
    required = {"config_id", "symbol", "signal_timestamp", "exit_timestamp", "gross_return"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"development_trades.csv missing columns: {sorted(missing)}")
    for col in ("signal_timestamp", "exit_timestamp"):
        df[col] = pd.to_datetime(df[col], utc=True).dt.tz_convert("Asia/Kolkata")
    df["gross_return"] = pd.to_numeric(df["gross_return"], errors="raise")
    return df.sort_values(["signal_timestamp", "symbol"]).reset_index(drop=True)


def _profit_factor(r: pd.Series) -> float:
    wins = r[r > 0].sum()
    losses = -r[r < 0].sum()
    return float(wins / losses) if losses > 0 else np.inf


def _metrics(df: pd.DataFrame) -> dict[str, float | int]:
    if df.empty:
        return {"trades": 0, "symbols": 0, "mean": np.nan, "median": np.nan, "win_rate": np.nan, "profit_factor": np.nan, "sum": 0.0}
    r = df["gross_return"]
    return {
        "trades": int(len(df)),
        "symbols": int(df["symbol"].nunique()),
        "mean": float(r.mean()),
        "median": float(r.median()),
        "win_rate": float((r > 0).mean()),
        "profit_factor": _profit_factor(r),
        "sum": float(r.sum()),
    }


def _breadth(df: pd.DataFrame) -> dict[str, float | int]:
    if df.empty:
        return {"symbol_count": 0, "positive_symbol_fraction": np.nan, "symbol_median_return": np.nan, "top5_share_abs": np.nan}
    by_symbol = df.groupby("symbol")["gross_return"].agg(["sum", "count"])
    positive_fraction = float((by_symbol["sum"] > 0).mean())
    ordered = by_symbol["sum"].abs().sort_values(ascending=False)
    total_abs = float(ordered.sum())
    top5_share = float(ordered.head(5).sum() / total_abs) if total_abs > 0 else np.nan
    return {
        "symbol_count": int(len(by_symbol)),
        "positive_symbol_fraction": positive_fraction,
        "symbol_median_return": float(by_symbol["sum"].median()),
        "top5_share_abs": top5_share,
    }


def _parse_periods(df: pd.DataFrame) -> pd.DataFrame:
    rows: list[dict] = []
    ts = df["signal_timestamp"]
    for period_name, (start, end) in PERIODS.items():
        subset = df[(ts >= start) & (ts < end)]
        for config_id, g in subset.groupby("config_id"):
            row = {"config_id": int(config_id), "period": period_name}
            row.update(_metrics(g))
            row.update(_breadth(g))
            rows.append(row)
    return pd.DataFrame(rows)


def _rank_candidates(grid: pd.DataFrame, stability: pd.DataFrame) -> pd.DataFrame:
    """Produce a screening view, not an automatic winner."""
    grouped = stability.groupby("config_id")
    rows = []
    for config_id, g in grouped:
        positive_periods = int((g["mean"] > 0).sum())
        positive_pf_periods = int((g["profit_factor"] > 1.0).sum())
        breadth_median = float(g["positive_symbol_fraction"].median())
        rows.append({
            "config_id": int(config_id),
            "positive_mean_periods": positive_periods,
            "positive_pf_periods": positive_pf_periods,
            "median_period_mean": float(g["mean"].median()),
            "median_period_pf": float(g["profit_factor"].median()),
            "median_positive_symbol_fraction": breadth_median,
            "worst_period_mean": float(g["mean"].min()),
            "worst_period_pf": float(g["profit_factor"].min()),
        })
    result = pd.DataFrame(rows).merge(grid, on="config_id", how="left")
    # This ordering is only a review convenience; it is explicitly not a
    # production-selection rule. It emphasizes consistency before magnitude.
    return result.sort_values(
        ["positive_mean_periods", "positive_pf_periods", "median_period_mean", "median_period_pf"],
        ascending=[False, False, False, False],
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--grid", default="data/reports/strategy_001j_development_grid/development_grid.csv")
    parser.add_argument("--trades", default="data/reports/strategy_001j_development_grid/development_trades.csv")
    parser.add_argument("--output-dir", default="data/reports/strategy_001j_development_stability")
    args = parser.parse_args()

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    grid = pd.read_csv(args.grid)
    trades = _load_trades(Path(args.trades))

    if trades["signal_timestamp"].min() < DEVELOPMENT_START or trades["signal_timestamp"].max() >= DEVELOPMENT_END_EXCLUSIVE:
        raise ValueError("Development trade ledger contains timestamps outside the frozen development window.")

    stability = _parse_periods(trades)
    screening = _rank_candidates(grid, stability)
    stability.to_csv(output_dir / "development_subperiod_stability.csv", index=False)
    screening.to_csv(output_dir / "development_candidate_screen.csv", index=False)

    pd.DataFrame([{
        "phase": "development_diagnostics",
        "start": DEVELOPMENT_START.date().isoformat(),
        "end": DEVELOPMENT_END.date().isoformat(),
        "periods": ";".join(PERIODS),
        "candidate_selection": "manual review required; this report is diagnostic and does not freeze a candidate",
        "holdout_access": "none",
    }]).to_csv(output_dir / "analysis_metadata.csv", index=False)

    print("001J development stability analysis complete. No holdout data was loaded.")
    print(f"Subperiod results: {output_dir / 'development_subperiod_stability.csv'}")
    print(f"Candidate screen: {output_dir / 'development_candidate_screen.csv'}")


if __name__ == "__main__":
    main()
