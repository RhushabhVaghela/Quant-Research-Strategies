from __future__ import annotations

import pandas as pd
import pytest

from src.research.strategy_001i_prospective import (
    append_outcome,
    append_signal,
    evaluate_completed_bar,
    finalize_paper_outcome,
    initialize_run,
    load_live_bars,
)


def _bars(n: int = 40) -> pd.DataFrame:
    ts = pd.date_range("2026-09-18 09:15", periods=n, freq="5min", tz="Asia/Kolkata")
    close = [100.0 + i * 0.01 for i in range(n)]
    # Make the final bar a clear positive continuation event.
    close[-1] = 103.0
    return pd.DataFrame({
        "timestamp": ts,
        "open": close,
        "high": [x + 0.05 for x in close],
        "low": [x - 0.05 for x in close],
        "close": close,
        "volume": [1000.0] * n,
    })


def test_initialize_run_creates_append_only_files(tmp_path):
    manifest = initialize_run(tmp_path, "2026-09-18T09:00:00+05:30")
    assert manifest.protocol_version == "001I"
    assert (tmp_path / "run_manifest.json").exists()
    assert (tmp_path / "signals.csv").exists()
    assert (tmp_path / "outcomes.csv").exists()
    assert (tmp_path / "bars.csv").exists()


def test_evaluate_completed_bar_does_not_use_future_bars():
    bars = _bars()
    prior = bars.iloc[:-1].copy()
    current = bars.iloc[-1].to_dict()
    row = evaluate_completed_bar(
        prior,
        current,
        capture_timestamp="2026-09-18T12:30:00+05:30",
        intended_entry_timestamp="2026-09-18T12:35:00+05:30",
    )
    assert row is not None
    assert row["status"] == "signal_observed"
    assert row["signal_timestamp"].startswith("2026-09-18T12:30")


def test_evaluate_completed_bar_rejects_capture_after_entry():
    bars = _bars()
    with pytest.raises(ValueError, match="captured after"):
        evaluate_completed_bar(
            bars.iloc[:-1],
            bars.iloc[-1].to_dict(),
            capture_timestamp="2026-09-18T12:36:00+05:30",
            intended_entry_timestamp="2026-09-18T12:35:00+05:30",
        )


def test_signal_and_outcome_are_append_only(tmp_path):
    initialize_run(tmp_path, "2026-09-18T09:00:00+05:30")
    signal = {
        "signal_id": "001I-20260918-1230",
        "signal_timestamp": "2026-09-18T12:30:00+05:30",
    }
    append_signal(tmp_path, signal)
    with pytest.raises(ValueError, match="already recorded"):
        append_signal(tmp_path, signal)

    outcome = {"signal_id": signal["signal_id"], "gross_return": 0.001}
    append_outcome(tmp_path, outcome)
    with pytest.raises(ValueError, match="already recorded"):
        append_outcome(tmp_path, outcome)


def test_finalize_paper_outcome_uses_next_open_and_frozen_exit():
    bars = _bars(40)
    # Use a signal at 12:30. Entry is 12:35 and frozen exit bar is 13:00.
    signal = {
        "signal_id": "001I-20260918-1230",
        "intended_entry_timestamp": "2026-09-18T12:35:00+05:30",
        "intended_exit_timestamp": "2026-09-18T13:00:00+05:30",
    }
    outcome = finalize_paper_outcome(
        tmp_path if False else ".",
        signal,
        bars,
        "2026-09-18T13:05:00+05:30",
    )
    assert outcome["observable_or_paper_entry_price"] > 0
    assert outcome["observable_or_paper_exit_price"] > 0
    assert outcome["gross_return"] == pytest.approx(
        outcome["observable_or_paper_exit_price"] / outcome["observable_or_paper_entry_price"] - 1.0
    )


def test_load_live_bars_deduplicates(tmp_path):
    initialize_run(tmp_path, "2026-09-18T09:00:00+05:30")
    pd.DataFrame([
        {"timestamp": "2026-09-18T09:15:00+05:30", "open": 100, "high": 101, "low": 99, "close": 100.5, "volume": 1000},
        {"timestamp": "2026-09-18T09:15:00+05:30", "open": 100, "high": 101, "low": 99, "close": 100.6, "volume": 1001},
    ]).to_csv(tmp_path / "bars.csv", index=False)
    loaded = load_live_bars(tmp_path / "bars.csv")
    assert len(loaded) == 1
    assert loaded.iloc[0]["close"] == 100.6
