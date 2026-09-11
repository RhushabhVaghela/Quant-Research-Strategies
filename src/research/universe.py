"""Universe-level diagnostics for comparable intraday OHLCV datasets."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path

import pandas as pd

from src.data.audit import audit_ohlcv, load_ohlcv_csv


@dataclass
class UniverseAuditRow:
    """Comparable diagnostics for one instrument dataset."""

    symbol: str
    path: str
    rows: int
    trading_days: int
    bars_per_day_median: float
    duplicate_timestamps: int
    unexpected_interval_count: int
    zero_volume_rows: int
    mean_5m_return: float | None
    std_5m_return: float | None
    median_abs_5m_return: float | None
    p01_5m_return: float | None
    p99_5m_return: float | None

    def to_dict(self) -> dict:
        return asdict(self)


def symbol_from_path(path: str | Path) -> str:
    """Infer a symbol from the project's ``NSE_SYMBOL_5minute.csv`` naming convention."""
    stem = Path(path).stem
    parts = stem.split("_")
    if len(parts) >= 3 and parts[-1].lower() == "5minute":
        return "_".join(parts[1:-1])
    return stem


def audit_file(path: str | Path) -> UniverseAuditRow:
    """Audit one saved OHLCV CSV and convert the result to a universe row."""
    path = Path(path)
    df = load_ohlcv_csv(path)
    report = audit_ohlcv(df, expected_minutes=5)
    return UniverseAuditRow(
        symbol=symbol_from_path(path),
        path=str(path),
        rows=report.rows,
        trading_days=report.trading_days,
        bars_per_day_median=report.bars_per_day_median,
        duplicate_timestamps=report.duplicate_timestamps,
        unexpected_interval_count=report.unexpected_interval_count,
        zero_volume_rows=report.zero_volume_rows,
        mean_5m_return=report.mean_5m_return,
        std_5m_return=report.std_5m_return,
        median_abs_5m_return=report.median_abs_5m_return,
        p01_5m_return=report.p01_5m_return,
        p99_5m_return=report.p99_5m_return,
    )


def audit_directory(directory: str | Path) -> pd.DataFrame:
    """Audit all 5-minute CSV files in a directory.

    Files that do not match ``*_5minute.csv`` are ignored so the report is
    reproducible when the raw-data directory contains other artifacts.
    """
    directory = Path(directory)
    paths = sorted(directory.glob("*_5minute.csv"))
    rows = [audit_file(path).to_dict() for path in paths]
    return pd.DataFrame(rows)


def apply_minimum_quality_filter(
    report: pd.DataFrame,
    *,
    min_trading_days: int = 20,
    min_rows: int = 1000,
) -> pd.DataFrame:
    """Return candidates meeting structural minimums only.

    This is deliberately *not* a performance ranking. No return or P&L metric
    is used in the eligibility decision.
    """
    if report.empty:
        return report.copy()

    mask = (
        (report["trading_days"] >= min_trading_days)
        & (report["rows"] >= min_rows)
        & (report["duplicate_timestamps"] == 0)
        & (report["unexpected_interval_count"] == 0)
        & (report["zero_volume_rows"] == 0)
    )
    return report.loc[mask].copy()
