"""Unit tests for Strategy 003H mechanism decomposition."""

from __future__ import annotations

import pandas as pd

from scripts.run_strategy_003_hypothesis_003h_mechanism import (
    MECHANISM_FEATURES,
    lineage_audit,
    quintile_table,
    time_bucket,
)


def test_mechanism_feature_set_is_locked_to_preregistered_features() -> None:
    assert MECHANISM_FEATURES == [
        "close_location_1bar",
        "intraday_position_60bar",
        "bars_since_session_open",
    ]


def test_quintile_table_preserves_all_five_buckets() -> None:
    rows = []
    ts = pd.Timestamp("2026-06-10 14:00", tz="Asia/Kolkata")
    for symbol in range(10):
        rows.append(
            {
                "timestamp": ts,
                "symbol": f"S{symbol}",
                "prediction": float(symbol),
                "target_excess_1bar": float(symbol - 5) / 10000,
            }
        )

    out = quintile_table(pd.DataFrame(rows))

    assert out["quintile"].tolist() == [1, 2, 3, 4, 5]
    assert out["observations"].tolist() == [2, 2, 2, 2, 2]


def test_time_bucket_uses_correct_clock_boundaries() -> None:
    timestamps = pd.Series(
        pd.to_datetime(
            [
                "2026-06-10 09:15",
                "2026-06-10 09:59",
                "2026-06-10 10:00",
                "2026-06-10 11:59",
                "2026-06-10 12:00",
                "2026-06-10 13:59",
                "2026-06-10 14:00",
                "2026-06-10 15:30",
            ]
        ).tz_localize("Asia/Kolkata")
    )

    assert time_bucket(timestamps).tolist() == [
        "09:15-09:59",
        "09:15-09:59",
        "10:00-11:59",
        "10:00-11:59",
        "12:00-13:59",
        "12:00-13:59",
        "14:00-15:30",
        "14:00-15:30",
    ]


def test_lineage_audit_has_no_direct_001_or_002_encoding() -> None:
    audit = lineage_audit()

    assert len(audit) == 3
    assert not audit["directly_encodes_001_signed_return"].any()
    assert not audit["directly_encodes_002_peer_residual_return"].any()
