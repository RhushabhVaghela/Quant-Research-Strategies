"""Unit tests for Strategy 003 intraday discovery controls."""

from __future__ import annotations

from pathlib import Path

import pandas as pd

from scripts.run_strategy_003_prediction_discovery import (
    BAR_MINUTES,
    EXPLORATORY_END,
    EXPLORATORY_START,
    HORIZON_BARS,
    HOLDOUT_START,
    VALIDATION_START,
    build_symbol_panel,
    feature_columns,
    load_intraday,
    model_diagnostics,
    session_bar_features,
    locked_exploratory_slice,
    purged_chronological_splits,
)


def test_locked_exploratory_slice_excludes_protected_periods() -> None:
    frame = pd.DataFrame(
        {
            "date": pd.to_datetime(
                [
                    "2025-09-18",
                    "2026-06-09",
                    "2026-06-10",
                    "2026-08-20",
                ]
            ),
            "value": [1, 2, 3, 4],
        }
    )

    out = locked_exploratory_slice(frame)

    assert out["date"].min() >= EXPLORATORY_START
    assert out["date"].max() <= EXPLORATORY_END
    assert out["date"].max() < VALIDATION_START
    assert out["date"].max() < HOLDOUT_START
    assert len(out) == 2


def test_constants_are_chronological() -> None:
    assert EXPLORATORY_START < EXPLORATORY_END
    assert EXPLORATORY_END < VALIDATION_START
    assert VALIDATION_START < HOLDOUT_START


def test_intraday_horizon_is_one_five_minute_bar() -> None:
    assert HORIZON_BARS == 1
    assert BAR_MINUTES == 5


def test_purged_split_removes_one_decision_timestamp_from_each_prior_split() -> None:
    timestamps = pd.date_range(
        "2026-01-01 09:15",
        periods=300,
        freq="5min",
    )
    splits = purged_chronological_splits(timestamps)

    assert splits["train_end"] < splits["validation_start"]
    assert splits["validation_end"] < splits["test_start"]
    assert splits["train_purge_count"] == 1
    assert splits["validation_purge_count"] == 1
    assert splits["horizon_bars"] == 1

    unique = pd.DatetimeIndex(timestamps)
    unpurged_train_end = splits["train_end_unpurged"]
    expected_train_end = unique[unique.get_loc(unpurged_train_end) - 1]
    assert splits["train_end"] == expected_train_end


def test_last_bar_of_each_session_has_no_overnight_target() -> None:
    data_dir = Path("data/raw/strategy_002_universe")
    stock = load_intraday(data_dir / "NSE_RELIANCE_5minute.csv")
    market = load_intraday(data_dir / "NSE_NIFTYBEES_5minute.csv")

    panel = build_symbol_panel(stock, market)
    last_bars = panel.groupby("date").tail(1)

    assert last_bars["future_return_1bar"].isna().all()


def test_long_feature_window_fits_within_indian_equity_session() -> None:
    timestamps = pd.date_range(
        "2026-01-01 09:15",
        periods=75,
        freq="5min",
        tz="Asia/Kolkata",
    )
    frame = pd.DataFrame(
        {
            "timestamp": timestamps,
            "open": 100.0 + 0.01 * pd.Series(range(75)),
            "high": 101.0 + 0.01 * pd.Series(range(75)),
            "low": 99.0 + 0.01 * pd.Series(range(75)),
            "close": 100.0 + 0.02 * pd.Series(range(75)),
            "volume": 1000.0 + 10.0 * pd.Series(range(75)),
        }
    )

    enriched = session_bar_features(frame)

    assert enriched["volume_z_60bar"].notna().sum() > 0
    assert enriched["realized_vol_60bar"].notna().sum() > 0
    assert enriched["range_z_60bar"].notna().sum() > 0
    assert enriched["intraday_position_60bar"].notna().sum() > 0


def test_feature_set_excludes_signed_return_direction_features() -> None:
    frame = pd.DataFrame(
        columns=[
            "log_volume",
            "volume_change_1bar",
            "volume_z_12bar",
            "realized_vol_12bar",
            "range_1bar",
            "market_return_1bar",
        ]
    )
    features = feature_columns(frame)

    forbidden = {
        "ret_1d",
        "ret_5d",
        "ret_20d",
        "market_rel_1d",
        "market_rel_5d",
        "market_beta_20d",
    }
    assert forbidden.isdisjoint(features)


def test_feature_ic_handles_structurally_undefined_feature_transforms() -> None:
    from scripts.run_strategy_003_prediction_discovery import univariate_ic

    timestamps = pd.date_range(
        "2026-01-01 09:15",
        periods=10,
        freq="5min",
        tz="Asia/Kolkata",
    )
    rows = []
    for i, ts in enumerate(timestamps):
        for j in range(5):
            rows.append(
                {
                    "timestamp": ts,
                    "date": ts.tz_convert("Asia/Kolkata").normalize().tz_localize(None),
                    "target_excess_1bar": float(j - 2) * (1 + i / 10),
                    "useful_feature": float(j) + i / 10,
                    "market_context": 0.001 * i,
                    "market_context_cs_z": float("nan"),
                }
            )
    panel = pd.DataFrame(rows)

    result = univariate_ic(
        panel,
        ["useful_feature", "market_context", "market_context_cs_z"],
    )

    assert set(result["feature"]) == {"useful_feature", "market_context"}
    assert result["usable_dates"].min() > 0


def test_model_diagnostics_ignores_structurally_undefined_registered_features() -> None:
    from scripts.run_strategy_003_prediction_discovery import QUINTILES

    timestamps = pd.date_range(
        "2026-01-01 09:15",
        periods=30,
        freq="5min",
        tz="Asia/Kolkata",
    )
    rows = []
    for i, ts in enumerate(timestamps):
        for j in range(10):
            rows.append(
                {
                    "timestamp": ts,
                    "symbol": f"S{j:02d}",
                    "target_excess_1bar": float(j - 4.5) * (1 + i / 100),
                    "feature_a": float(j) + i / 10,
                    "feature_b_cs_z": float("nan"),
                }
            )
    panel = pd.DataFrame(rows)

    models, quintiles = model_diagnostics(panel, ["feature_a", "feature_b_cs_z"])

    assert not models.empty
    assert set(models["model"]) == {"zero_baseline", "ols", "ridge_fixed_alpha"}
    assert models["split"].isin({"validation", "development_test"}).all()
    assert len(quintiles) > 0
    assert quintiles["model"].isin({"ols", "ridge_fixed_alpha"}).all()
    assert (quintiles["horizon_bars"] == HORIZON_BARS).all()
    assert (quintiles["horizon_minutes"] == BAR_MINUTES).all()
