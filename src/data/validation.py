from __future__ import annotations
from dataclasses import dataclass
import pandas as pd

@dataclass
class ValidationReport:
    rows: int
    duplicate_timestamps: int
    missing_ohlc: int
    invalid_ohlc: int
    invalid_volume: int
    non_monotonic_index: bool

    @property
    def passed(self) -> bool:
        return (
            self.duplicate_timestamps == 0
            and self.missing_ohlc == 0
            and self.invalid_ohlc == 0
            and self.invalid_volume == 0
            and not self.non_monotonic_index
        )

def validate_ohlcv(df: pd.DataFrame) -> ValidationReport:
    required = ["open","high","low","close","volume"]
    missing_columns = [c for c in required if c not in df.columns]
    if missing_columns:
        raise ValueError(f"Missing required columns: {missing_columns}")

    duplicate_timestamps = int(df.index.duplicated().sum())
    missing_ohlc = int(df[["open","high","low","close"]].isna().any(axis=1).sum())
    invalid_ohlc = int((
        (df["high"] < df[["open","close","low"]].max(axis=1))
        | (df["low"] > df[["open","close","high"]].min(axis=1))
        | (df[["open","high","low","close"]] <= 0).any(axis=1)
    ).sum())
    invalid_volume = int((df["volume"].isna() | (df["volume"] < 0)).sum())

    return ValidationReport(
        rows=len(df),
        duplicate_timestamps=duplicate_timestamps,
        missing_ohlc=missing_ohlc,
        invalid_ohlc=invalid_ohlc,
        invalid_volume=invalid_volume,
        non_monotonic_index=not df.index.is_monotonic_increasing,
    )

def assert_valid(df: pd.DataFrame) -> ValidationReport:
    report = validate_ohlcv(df)
    if not report.passed:
        raise ValueError(f"OHLCV validation failed: {report}")
    return report
