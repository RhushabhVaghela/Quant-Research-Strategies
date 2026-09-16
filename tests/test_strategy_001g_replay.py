from __future__ import annotations

import numpy as np
import pandas as pd

from src.research.strategy_001g_replay import (
    build_replay_features,
    excursion_metrics,
    forward_path,
    reconcile_trades,
    summarize_forward_path,
)


def make_session_frame(days: int = 2, bars_per_day: int = 40) -> pd.DataFrame:
    rows = []
    start = pd.Timestamp("2026-01-05 09:15", tz="Asia/Kolkata")
    for d in range(days):
        day = start + pd.Timedelta(days=d)
        for i in range(bars_per_day):
            ts = day + pd.Timedelta(minutes=5 * i)
            close = 100.0 + d * 10 + i * 0.2 + (0.05 if i == 30 else 0)
            rows.append({
                "timestamp": ts,
                "open": close - 0.05,
                "high": close + 0.20,
                "low": close - 0.20,
                "close": close,
                "volume": 1000.0 + i,
            })
    return pd.DataFrame(rows).set_index("timestamp")


def test_signal_features_are_point_in_time_and_session_local() -> None:
    df = make_session_frame()
    out = build_replay_features(df)
    first_day = out.iloc[:40]
    second_day = out.iloc[40:]
    # The first bar of each session cannot have a prior 30-bar feature window.
    assert pd.isna(first_day.iloc[0]["prior_mean_30"])
    assert pd.isna(second_day.iloc[0]["prior_mean_30"])
    # The second session must not inherit the first session's bars.
    assert pd.isna(second_day.iloc[0]["prior_std_30"])
    # At local bar 30, the current event bar is excluded from the rolling window.
    expected = first_day.iloc[:30]["close"].mean()
    assert np.isclose(first_day.iloc[30]["prior_mean_30"], expected)


def test_forward_path_uses_signal_relative_horizons_and_next_open_entry() -> None:
    df = make_session_frame(days=1)
    signals = build_replay_features(df)
    selected = signals.index[30]
    # Construct a minimal trade using the same timestamps as the frozen execution rule.
    trade = pd.DataFrame([{
        "trade_id": str(selected),
        "signal_timestamp": selected,
        "entry_timestamp": signals.index[31],
        "exit_timestamp": signals.index[36],
        "entry_price_raw": float(signals.iloc[31]["open"]),
    }])
    path = forward_path(signals, trade, horizons_minutes=(5, 30))
    h5 = path.loc[path["horizon_minutes"] == 5].iloc[0]
    h30 = path.loc[path["horizon_minutes"] == 30].iloc[0]
    assert h5["target_timestamp"] == selected + pd.Timedelta(minutes=5)
    assert h30["target_timestamp"] == selected + pd.Timedelta(minutes=30)
    assert np.isclose(
        h30["forward_return"],
        signals.loc[selected + pd.Timedelta(minutes=30), "close"] / trade.loc[0, "entry_price_raw"] - 1,
    )


def test_excursions_include_entry_through_frozen_exit() -> None:
    df = make_session_frame(days=1)
    signals = build_replay_features(df)
    selected = signals.index[30]
    trade = pd.DataFrame([{
        "trade_id": str(selected),
        "signal_timestamp": selected,
        "entry_timestamp": signals.index[31],
        "exit_timestamp": signals.index[36],
        "entry_price_raw": float(signals.iloc[31]["open"]),
    }])
    excursions = excursion_metrics(signals, trade).iloc[0]
    highs = signals.loc[signals.index[31]:signals.index[36], "high"]
    lows = signals.loc[signals.index[31]:signals.index[36], "low"]
    entry = trade.loc[0, "entry_price_raw"]
    assert np.isclose(excursions["mfe_return"], highs.max() / entry - 1)
    assert np.isclose(excursions["mae_return"], lows.min() / entry - 1)


def test_reconciliation_flags_matching_and_missing_trades() -> None:
    ts = pd.Timestamp("2026-01-05 12:00", tz="Asia/Kolkata")
    replayed = pd.DataFrame([{
        "trade_id": str(ts),
        "signal_timestamp": ts,
        "entry_timestamp": ts + pd.Timedelta(minutes=5),
        "exit_timestamp": ts + pd.Timedelta(minutes=30),
        "gross_return": 0.001,
    }])
    reference = pd.DataFrame([{
        "signal_timestamp": str(ts),
        "gross_return": 0.001,
    }])
    result = reconcile_trades(replayed, reference)
    assert bool(result.iloc[0]["match"])

    reference.loc[0, "gross_return"] = 0.002
    result = reconcile_trades(replayed, reference)
    assert not bool(result.iloc[0]["match"])


def test_forward_summary_is_descriptive() -> None:
    path = pd.DataFrame({
        "horizon_minutes": [5, 5, 30, 30],
        "forward_return": [0.001, -0.001, 0.002, 0.004],
    })
    summary = summarize_forward_path(path)
    assert list(summary["horizon_minutes"]) == [5, 30]
    assert np.isclose(summary.loc[summary["horizon_minutes"] == 30, "mean_return"].iloc[0], 0.003)
    assert np.isclose(summary.loc[summary["horizon_minutes"] == 30, "win_rate"].iloc[0], 1.0)
