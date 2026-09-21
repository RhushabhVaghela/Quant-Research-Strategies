"""Decompose turnover and execution activity for the frozen Strategy 002 baseline.

This diagnostic uses only the chronological validation period. It does not optimize
the signal and does not read the final holdout.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd

VALIDATION_START = pd.Timestamp("2026-06-10", tz="Asia/Kolkata")
HOLDOUT_START = pd.Timestamp("2026-08-20", tz="Asia/Kolkata")
MIN_INSTRUMENTS = 4


def parse_args():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("directory", type=Path)
    p.add_argument(
        "--audit-report",
        type=Path,
        default=Path("data/reports/strategy_002_universe_audit.csv"),
    )
    p.add_argument(
        "--output-dir",
        type=Path,
        default=Path("data/reports/strategy_002_turnover_decomposition"),
    )
    return p.parse_args()


def load_validation(path: Path) -> pd.DataFrame:
    df = pd.read_csv(path, parse_dates=["timestamp"])
    required = {"timestamp", "open", "close", "volume"}
    if not required.issubset(df.columns):
        raise ValueError(f"{path}: missing required columns")

    ts = pd.DatetimeIndex(df["timestamp"])
    if ts.tz is None:
        raise ValueError(f"{path}: timestamps must be timezone-aware")
    df["timestamp"] = ts.tz_convert("Asia/Kolkata")
    df = df.sort_values("timestamp")

    if df["timestamp"].duplicated().any() or not df["timestamp"].is_monotonic_increasing:
        raise ValueError(f"{path}: invalid timestamps")

    for column in ("open", "close", "volume"):
        df[column] = pd.to_numeric(df[column], errors="coerce")

    if df[["open", "close"]].isna().any().any() or (df[["open", "close"]] <= 0).any().any():
        raise ValueError(f"{path}: invalid prices")
    if df["volume"].isna().any() or (df["volume"] < 0).any():
        raise ValueError(f"{path}: invalid volume")

    out = df.loc[
        (df["timestamp"] >= VALIDATION_START)
        & (df["timestamp"] < HOLDOUT_START),
        ["timestamp", "open", "close"],
    ].copy()

    if out.empty:
        raise ValueError(f"{path}: no validation observations")
    if out["timestamp"].min() < VALIDATION_START or out["timestamp"].max() >= HOLDOUT_START:
        raise AssertionError(f"{path}: crossed validation boundaries")

    return out.set_index("timestamp")


def load_universe(directory: Path, audit_report: Path):
    audit = pd.read_csv(audit_report)
    eligible = set(
        audit.loc[
            (audit["unexpected_interval_count"] == 0)
            & (audit["zero_volume_rows"] == 0),
            "symbol",
        ].astype(str)
    )

    series = {}
    excluded = []
    for path in sorted(directory.glob("*_5minute.csv")):
        symbol = path.name.removeprefix("NSE_").removesuffix("_5minute.csv")
        if symbol not in eligible:
            excluded.append(
                {"symbol": symbol, "reason": "failed structural universe audit"}
            )
            continue
        try:
            series[symbol] = load_validation(path)
        except (ValueError, AssertionError) as exc:
            excluded.append({"symbol": symbol, "reason": str(exc)})

    if len(series) < MIN_INSTRUMENTS:
        raise SystemExit(f"Need at least {MIN_INSTRUMENTS} eligible instruments")
    return series, excluded


def build_target_weights(residual: pd.Series) -> pd.Series:
    negative = residual[residual < 0].index
    positive = residual[residual > 0].index
    if len(negative) == 0 or len(positive) == 0:
        return pd.Series(dtype=float)

    weights = pd.Series(0.0, index=residual.index, dtype=float)
    weights.loc[negative] = 0.5 / len(negative)
    weights.loc[positive] = -0.5 / len(positive)
    return weights


def calculate_turnover(previous: pd.Series, current: pd.Series) -> dict:
    """Calculate target-weight changes between consecutive portfolios.

    This is a diagnostic decomposition only. The frozen baseline actually closes
    every prior position and opens the next portfolio, so this target-weight
    turnover is not the same thing as executed round-trip turnover.
    """
    if previous.empty:
        return {
            "absolute_weight_change": np.nan,
            "one_way_turnover": np.nan,
            "opened_notional": np.nan,
            "closed_notional": np.nan,
            "flipped_notional": np.nan,
            "unchanged_notional": np.nan,
        }

    idx = previous.index.union(current.index)
    old = previous.reindex(idx, fill_value=0.0)
    new = current.reindex(idx, fill_value=0.0)

    delta = new - old
    same_side = (old != 0) & (new != 0) & (np.sign(old) == np.sign(new))
    opened = (old == 0) & (new != 0)
    closed = (old != 0) & (new == 0)
    flipped = (old * new) < 0

    return {
        "absolute_weight_change": float(delta.abs().sum()),
        "one_way_turnover": float(0.5 * delta.abs().sum()),
        "opened_notional": float(new.abs().where(opened, 0.0).sum()),
        "closed_notional": float(old.abs().where(closed, 0.0).sum()),
        "flipped_notional": float((old.abs() + new.abs()).where(flipped, 0.0).sum()),
        "unchanged_notional": float(new.abs().where(same_side, 0.0).sum()),
    }


def build_records(series: dict[str, pd.DataFrame]) -> pd.DataFrame:
    closes = pd.DataFrame({symbol: frame["close"] for symbol, frame in series.items()}).sort_index()
    opens = pd.DataFrame({symbol: frame["open"] for symbol, frame in series.items()}).sort_index()
    returns = closes.pct_change(fill_method=None)

    records = []
    target_weights = []

    for ts in returns.index:
        valid = returns.loc[ts].dropna()
        if len(valid) < MIN_INSTRUMENTS:
            continue

        cross_sum = valid.sum()
        n = len(valid)
        residual = valid - (cross_sum - valid) / (n - 1)

        next_ts = pd.Timestamp(ts) + pd.Timedelta(minutes=5)
        if next_ts not in opens.index or next_ts not in closes.index:
            continue
        if next_ts.date() != ts.date():
            continue

        weights = build_target_weights(residual)
        if weights.empty:
            continue

        long_count = int((weights > 0).sum())
        short_count = int((weights < 0).sum())
        target_weights.append((ts, weights))

        records.append(
            {
                "signal_timestamp": ts,
                "entry_timestamp": next_ts,
                "exit_timestamp": next_ts,
                "long_count": long_count,
                "short_count": short_count,
                "gross_exposure": float(weights.abs().sum()),
                "net_exposure": float(weights.sum()),
                # The frozen baseline enters 100% gross exposure at the next
                # open and closes that same exposure at the next close.
                "entry_notional": 1.0,
                "exit_notional": 1.0,
                "executed_round_trip_turnover": 2.0,
                "holding_bars": 1,
                "holding_minutes": 5.0,
            }
        )

    turnover_rows = []
    previous_ts = None
    previous = pd.Series(dtype=float)

    for ts, current in target_weights:
        turnover_rows.append(
            {
                "signal_timestamp": ts,
                "previous_signal_timestamp": previous_ts,
                **calculate_turnover(previous, current),
            }
        )
        previous = current
        previous_ts = ts

    return pd.DataFrame(records).merge(
        pd.DataFrame(turnover_rows),
        on="signal_timestamp",
        how="left",
    )


def summarize(portfolio: pd.DataFrame, included: list[str], excluded: list[dict]) -> dict:
    target_turnover = portfolio["one_way_turnover"].dropna()
    round_trip = portfolio["executed_round_trip_turnover"]

    summary = {
        "validation_start": str(VALIDATION_START),
        "validation_end_exclusive": str(HOLDOUT_START),
        "included_instruments": included,
        "excluded_instruments": excluded,
        "portfolio_observations": int(len(portfolio)),
        "target_turnover_observations": int(len(target_turnover)),
        "mean_one_way_target_turnover_pct": float(target_turnover.mean() * 100.0),
        "median_one_way_target_turnover_pct": float(target_turnover.median() * 100.0),
        "p95_one_way_target_turnover_pct": float(target_turnover.quantile(0.95) * 100.0),
        "mean_long_count": float(portfolio["long_count"].mean()),
        "median_long_count": float(portfolio["long_count"].median()),
        "mean_short_count": float(portfolio["short_count"].mean()),
        "median_short_count": float(portfolio["short_count"].median()),
        "mean_gross_exposure": float(portfolio["gross_exposure"].mean()),
        "mean_net_exposure": float(portfolio["net_exposure"].mean()),
        "mean_executed_round_trip_turnover_pct": float(round_trip.mean() * 100.0),
        "daily_executed_round_trip_turnover_multiple": float(
            round_trip.groupby(portfolio["signal_timestamp"].dt.date).sum().mean()
        ),
        "median_holding_bars": float(portfolio["holding_bars"].median()),
        "mean_holding_minutes": float(portfolio["holding_minutes"].mean()),
        "holdout_used": False,
        "optimization_performed": False,
    }
    return summary


def main():
    args = parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)

    series, excluded = load_universe(args.directory, args.audit_report)
    portfolio = build_records(series)
    if portfolio.empty:
        raise SystemExit("No validation portfolio observations were generated")

    summary = summarize(portfolio, sorted(series), excluded)

    portfolio.to_csv(args.output_dir / "turnover_by_rebalance.csv", index=False)
    pd.DataFrame([summary]).to_csv(args.output_dir / "turnover_summary.csv", index=False)

    manifest = {
        "analysis": "strategy_002_turnover_execution_decomposition",
        "validation_start": str(VALIDATION_START),
        "holdout_start": str(HOLDOUT_START),
        "holdout_used": False,
        "optimization_performed": False,
        "signal_definition": "frozen Strategy 002 leave-one-out residual sign",
        "execution_definition": "next 5-minute bar open to next 5-minute bar close",
        "position_lifecycle": "enter next-bar open and close next-bar close; no position carried to the following signal",
        "target_turnover_definition": "0.5 * sum(abs(current_target_weight - previous_target_weight))",
        "executed_round_trip_turnover_definition": "entry gross notional + exit gross notional; normalized to 2.0 per one-bar 100%-gross round trip",
    }
    (args.output_dir / "run_manifest.json").write_text(
        json.dumps(manifest, indent=2),
        encoding="utf-8",
    )

    print(f"Included instruments: {len(series)}")
    print(f"Excluded instruments: {len(excluded)}")
    print(f"Validation portfolios: {len(portfolio)}")
    print(f"Outputs: {args.output_dir}")


if __name__ == "__main__":
    main()
