from pathlib import Path
import pandas as pd

from scripts.characterize_strategy_002_reversal_mechanism import (
    END, VALIDATION_START, load, rows
)

def test_load_restricts_to_exploratory_window(tmp_path: Path):
    p = tmp_path / "NSE_TEST_5minute.csv"
    ts = pd.date_range("2025-09-18 09:15", periods=3, freq="5min", tz="Asia/Kolkata")
    df = pd.DataFrame({
        "timestamp": ts, "open":[100,101,102], "high":[101,102,103],
        "low":[99,100,101], "close":[101,102,103], "volume":[1,1,1]
    })
    df.to_csv(p, index=False)
    out = load(p)
    assert out["timestamp"].max() < VALIDATION_START
    assert out["timestamp"].max() <= END

def test_rows_contains_three_return_components():
    ts = pd.date_range("2025-09-18 09:15", periods=10, freq="5min", tz="Asia/Kolkata")
    close = [100,99,101,100,102,101,103,102,104,103]
    df = pd.DataFrame({
        "timestamp":ts, "open":close, "high":[x+1 for x in close],
        "low":[x-1 for x in close], "close":close, "volume":[1]*10
    })
    out = rows(df, "TEST")
    assert set(out["component"]) == {
        "next_close_to_close", "next_close_to_open", "next_open_to_close"
    }
