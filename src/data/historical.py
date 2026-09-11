from __future__ import annotations
import time
from datetime import date, timedelta
from pathlib import Path
import pandas as pd
from .kite_client import KiteClient

COLUMNS = ["timestamp","open","high","low","close","volume"]

def _date_chunks(start: date, end: date, chunk_days: int):
    cursor = start
    while cursor <= end:
        chunk_end = min(cursor + timedelta(days=chunk_days - 1), end)
        yield cursor, chunk_end
        cursor = chunk_end + timedelta(days=1)

def fetch_historical(
    client: KiteClient, instrument_token: int, start: date, end: date,
    interval: str = "5minute", chunk_days: int = 30, pause_seconds: float = 0.35
) -> pd.DataFrame:
    if start > end:
        raise ValueError("start must be <= end")
    if chunk_days < 1:
        raise ValueError("chunk_days must be >= 1")

    frames = []
    for chunk_start, chunk_end in _date_chunks(start, end, chunk_days):
        candles = client.kite.historical_data(
            instrument_token=instrument_token,
            from_date=chunk_start,
            to_date=chunk_end,
            interval=interval,
            continuous=False,
            oi=False,
        )
        if candles:
            chunk_df = pd.DataFrame(candles)
            if "date" in chunk_df.columns and "timestamp" not in chunk_df.columns:
                chunk_df = chunk_df.rename(columns={"date": "timestamp"})
            frames.append(chunk_df[COLUMNS])
        time.sleep(max(0.0, pause_seconds))

    if not frames:
        empty = pd.DataFrame(columns=COLUMNS)
        empty["timestamp"] = pd.to_datetime(empty["timestamp"], utc=True)
        return empty.set_index("timestamp")

    df = pd.concat(frames, ignore_index=True)
    df["timestamp"] = pd.to_datetime(df["timestamp"], utc=True).dt.tz_convert("Asia/Kolkata")
    df = df.sort_values("timestamp").drop_duplicates("timestamp", keep="last").set_index("timestamp")
    for col in ["open","high","low","close","volume"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")
    return df

def save_candles(df: pd.DataFrame, output_path: str | Path) -> Path:
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output, index=True)
    return output
