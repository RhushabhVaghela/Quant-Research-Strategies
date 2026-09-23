"""Tests for Strategy 003 frozen-model characterization diagnostics."""

from __future__ import annotations

import pandas as pd

from scripts.run_strategy_003_prediction_characterization import (
    _quintile_table,
    _quintile_summary,
    _time_bucket,
)


def test_quintile_table_preserves_all_five_score_buckets() -> None:
    rows = []
    timestamp = pd.Timestamp("2026-06-10 14:00", tz="Asia/Kolkata")
    for model in ("ols", "ridge_fixed_alpha"):
        for symbol in range(10):
            rows.append(
                {
                    "model": model,
                    "timestamp": timestamp,
                    "symbol": f"S{symbol}",
                    "prediction": float(symbol),
                    "target_excess_1bar": float(symbol - 5) / 10000,
                }
            )

    out = _quintile_table(pd.DataFrame(rows))

    assert set(out["quintile"]) == {1, 2, 3, 4, 5}
    assert len(out) == 10
    assert (out.groupby(["model", "quintile"])["n"].sum() == 2).all()


def test_quintile_summary_retains_intermediate_quintiles() -> None:
    rows = []
    timestamp = pd.Timestamp("2026-06-10 14:00", tz="Asia/Kolkata")
    for symbol in range(10):
        rows.append(
            {
                "model": "ols",
                "timestamp": timestamp,
                "symbol": f"S{symbol}",
                "prediction": float(symbol),
                "target_excess_1bar": float(symbol) / 10000,
            }
        )

    table = _quintile_table(pd.DataFrame(rows))
    summary = _quintile_summary(table)

    assert summary["quintile"].tolist() == [1, 2, 3, 4, 5]
    assert summary["mean_return_bps"].tolist() == [0.5, 2.5, 4.5, 6.5, 8.5]


def test_time_bucket_registers_all_four_clock_segments() -> None:
    timestamps = pd.Series(
        pd.to_datetime(
            [
                "2026-06-10 09:15",
                "2026-06-10 10:00",
                "2026-06-10 12:00",
                "2026-06-10 14:00",
            ]
        ).tz_localize("Asia/Kolkata")
    )

    out = _time_bucket(timestamps)

    assert out.tolist() == [
        "09:15-09:59",
        "10:00-11:59",
        "12:00-13:59",
        "14:00-15:30",
    ]
