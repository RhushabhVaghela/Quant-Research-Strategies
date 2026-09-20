from pathlib import Path
import pandas as pd
import pytest

from scripts.run_strategy_002_leave_one_out_residual import (
    END, START, VALIDATION_START, leave_one_out, load,
)

def test_leave_one_out_excludes_self():
    panel = pd.DataFrame({"A":[0.01], "B":[0.03], "C":[0.05], "D":[0.07]})
    out = leave_one_out(panel)
    assert out.loc[0, "A"] == pytest.approx(0.01 - (0.03+0.05+0.07)/3)
    assert out.loc[0, "B"] == pytest.approx(0.03 - (0.01+0.05+0.07)/3)

def test_load_slices_before_validation(tmp_path: Path):
    ts = pd.date_range("2025-09-18 09:15", periods=3, freq="5min", tz="Asia/Kolkata")
    later = pd.date_range("2026-06-10 09:15", periods=1, freq="5min", tz="Asia/Kolkata")
    timestamps = ts.append(later)
    df = pd.DataFrame({
        "timestamp": timestamps, "open":[100,101,102,103], "high":[101]*4,
        "low":[99]*4, "close":[100,101,102,103], "volume":[1]*4
    })
    p=tmp_path/"NSE_TEST_5minute.csv"; df.to_csv(p,index=False)
    out=load(p)
    assert out.index.max() <= END
    assert out.index.min() >= START
    assert out.index.max() < VALIDATION_START
