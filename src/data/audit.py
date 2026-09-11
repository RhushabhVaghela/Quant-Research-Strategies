"""Research-grade intraday OHLCV dataset audit utilities.

This module sits after historical download/validation and before any strategy
research. It checks session structure, bar spacing, and basic distribution
statistics without inventing missing bars.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path

import pandas as pd


@dataclass
class DatasetAuditReport:
    rows: int
    trading_days: int
    first_timestamp: str | None
    last_timestamp: str | None
    duplicate_timestamps: int
    non_monotonic_index: bool
    unexpected_interval_count: int
    bars_per_day_min: int
    bars_per_day_max: int
    bars_per_day_median: float
    zero_volume_rows: int
    return_count: int
    mean_5m_return: float | None
    std_5m_return: float | None
    median_abs_5m_return: float | None
    p01_5m_return: float | None
    p99_5m_return: float | None

    def to_dict(self) -> dict:
        return asdict(self)


def load_ohlcv_csv(path: str | Path) -> pd.DataFrame:
    """Load the project's saved OHLCV CSV with an Asia/Kolkata index."""
    df = pd.read_csv(path, index_col=0, parse_dates=True)
    if df.index.tz is None:
        df.index = df.index.tz_localize("Asia/Kolkata")
    else:
        df.index = df.index.tz_convert("Asia/Kolkata")
    return df.sort_index()


def _return_stats(df: pd.DataFrame) -> dict[str, float | int | None]:
    # Do not calculate returns across overnight/session boundaries.
    session_close_to_close = df.groupby(df.index.date)["close"].pct_change()
    returns = session_close_to_close.dropna()
    if returns.empty:
        return {
            "return_count": 0,
            "mean_5m_return": None,
            "std_5m_return": None,
            "median_abs_5m_return": None,
            "p01_5m_return": None,
            "p99_5m_return": None,
        }

    return {
        "return_count": int(returns.size),
        "mean_5m_return": float(returns.mean()),
        "std_5m_return": float(returns.std(ddof=1)),
        "median_abs_5m_return": float(returns.abs().median()),
        "p01_5m_return": float(returns.quantile(0.01)),
        "p99_5m_return": float(returns.quantile(0.99)),
    }


def audit_ohlcv(df: pd.DataFrame, expected_minutes: int = 5) -> DatasetAuditReport:
    """Audit an intraday OHLCV DataFrame without modifying its observations."""
    required = {"open", "high", "low", "close", "volume"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")
    if not isinstance(df.index, pd.DatetimeIndex):
        raise TypeError("OHLCV index must be a pandas DatetimeIndex")

    ordered = df.sort_index()
    duplicate_count = int(ordered.index.duplicated().sum())
    non_monotonic = not df.index.is_monotonic_increasing

    # Gaps are evaluated within a trading day. Overnight/weekend gaps are not
    # treated as missing market bars.
    day = ordered.index.date
    delta = ordered.index.to_series().diff()
    same_day = pd.Series(day, index=ordered.index).eq(pd.Series(day, index=ordered.index).shift(1))
    unexpected = int((delta.gt(pd.Timedelta(minutes=expected_minutes)) & same_day).sum())

    bars_per_day = ordered.groupby(ordered.index.date).size()
    stats = _return_stats(ordered)

    return DatasetAuditReport(
        rows=len(ordered),
        trading_days=int(len(bars_per_day)),
        first_timestamp=ordered.index.min().isoformat() if len(ordered) else None,
        last_timestamp=ordered.index.max().isoformat() if len(ordered) else None,
        duplicate_timestamps=duplicate_count,
        non_monotonic_index=non_monotonic,
        unexpected_interval_count=unexpected,
        bars_per_day_min=int(bars_per_day.min()) if len(bars_per_day) else 0,
        bars_per_day_max=int(bars_per_day.max()) if len(bars_per_day) else 0,
        bars_per_day_median=float(bars_per_day.median()) if len(bars_per_day) else 0.0,
        zero_volume_rows=int((ordered["volume"] == 0).sum()),
        **stats,
    )


def daily_bar_counts(df: pd.DataFrame) -> pd.DataFrame:
    """Return one row per trading day with bar counts and volume totals."""
    grouped = df.groupby(df.index.date)
    out = grouped.agg(
        bars=("close", "size"),
        volume=("volume", "sum"),
        first_timestamp=("close", lambda s: s.index.min()),
        last_timestamp=("close", lambda s: s.index.max()),
    )
    out.index.name = "session_date"
    return out


def time_of_day_profile(df: pd.DataFrame) -> pd.DataFrame:
    """Summarize return/volume behavior by 5-minute clock time."""
    work = df.copy()
    work["session_return"] = work.groupby(work.index.date)["close"].pct_change()
    work["clock"] = work.index.strftime("%H:%M")
    return work.groupby("clock").agg(
        observations=("close", "size"),
        mean_return=("session_return", "mean"),
        mean_abs_return=("session_return", lambda s: s.abs().mean()),
        median_volume=("volume", "median"),
    )
