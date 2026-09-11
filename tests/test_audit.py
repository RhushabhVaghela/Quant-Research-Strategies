import pandas as pd

from src.data.audit import audit_ohlcv, daily_bar_counts, time_of_day_profile


def make_df():
    idx = pd.DatetimeIndex(
        [
            "2026-08-03 09:15:00+05:30",
            "2026-08-03 09:20:00+05:30",
            "2026-08-03 09:25:00+05:30",
            "2026-08-04 09:15:00+05:30",
            "2026-08-04 09:20:00+05:30",
        ]
    )
    return pd.DataFrame(
        {
            "open": [100, 101, 102, 103, 104],
            "high": [101, 102, 103, 104, 105],
            "low": [99, 100, 101, 102, 103],
            "close": [101, 102, 103, 104, 105],
            "volume": [1000, 1100, 1200, 1300, 1400],
        },
        index=idx,
    )


def test_audit_counts_sessions_and_bars():
    report = audit_ohlcv(make_df())
    assert report.rows == 5
    assert report.trading_days == 2
    assert report.bars_per_day_min == 2
    assert report.bars_per_day_max == 3
    assert report.unexpected_interval_count == 0


def test_overnight_gap_is_not_called_intraday_missing_data():
    report = audit_ohlcv(make_df())
    assert report.unexpected_interval_count == 0


def test_daily_bar_counts():
    counts = daily_bar_counts(make_df())
    assert counts["bars"].tolist() == [3, 2]


def test_time_of_day_profile():
    profile = time_of_day_profile(make_df())
    assert "09:15" in profile.index
    assert profile.loc["09:15", "observations"] == 2
