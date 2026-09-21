from pathlib import Path

import pandas as pd

from scripts.run_strategy_002_validation import load_validation


def test_load_validation_excludes_holdout(tmp_path: Path):
    p = tmp_path / "NSE_TEST_5minute.csv"
    ts = pd.DatetimeIndex(
        [
            "2026-06-10 09:15",
            "2026-08-19 15:10",
            "2026-08-20 09:15",
        ],
        tz="Asia/Kolkata",
    )
    pd.DataFrame(
        {
            "timestamp": ts,
            "open": [100, 101, 102],
            "close": [101, 100, 103],
            "volume": [1, 1, 1],
        }
    ).to_csv(p, index=False)
    out = load_validation(p)
    assert out.index.min() >= pd.Timestamp("2026-06-10", tz="Asia/Kolkata")
    assert out.index.max() < pd.Timestamp("2026-08-20", tz="Asia/Kolkata")
