import pandas as pd

from src.research.universe import apply_minimum_quality_filter, symbol_from_path


def test_symbol_from_standard_filename() -> None:
    assert symbol_from_path("data/raw/NSE_NIFTYBEES_5minute.csv") == "NIFTYBEES"


def test_symbol_from_unexpected_filename_is_safe() -> None:
    assert symbol_from_path("foo.csv") == "foo"


def test_quality_filter_uses_structure_not_performance() -> None:
    report = pd.DataFrame(
        [
            {
                "symbol": "GOOD",
                "rows": 1500,
                "trading_days": 30,
                "duplicate_timestamps": 0,
                "unexpected_interval_count": 0,
                "zero_volume_rows": 0,
                "median_abs_5m_return": 0.0001,
            },
            {
                "symbol": "BAD",
                "rows": 1500,
                "trading_days": 30,
                "duplicate_timestamps": 1,
                "unexpected_interval_count": 0,
                "zero_volume_rows": 0,
                "median_abs_5m_return": 0.0100,
            },
        ]
    )

    eligible = apply_minimum_quality_filter(report)
    assert eligible["symbol"].tolist() == ["GOOD"]
