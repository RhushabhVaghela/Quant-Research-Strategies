from __future__ import annotations
from pathlib import Path
from typing import Any
import pandas as pd
from .kite_client import KiteClient

REQUIRED_COLUMNS = {
    "instrument_token","exchange_token","tradingsymbol","name","last_price",
    "expiry","strike","tick_size","lot_size","instrument_type","segment","exchange"
}

def download_instruments(client: KiteClient, output_path: str | Path, exchange: str = "NSE") -> Path:
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    rows = client.instruments(exchange)
    if not rows:
        raise RuntimeError(f"No instruments returned for exchange={exchange!r}")
    df = pd.DataFrame(rows)
    missing = REQUIRED_COLUMNS - set(df.columns)
    if missing:
        raise ValueError(f"Instrument response is missing columns: {sorted(missing)}")
    df.to_csv(output, index=False)
    return output

def load_instruments(path: str | Path) -> pd.DataFrame:
    df = pd.read_csv(path, low_memory=False)
    missing = REQUIRED_COLUMNS - set(df.columns)
    if missing:
        raise ValueError(f"Cached instrument file is missing: {sorted(missing)}")
    return df

def resolve_instrument(df: pd.DataFrame, exchange: str, tradingsymbol: str) -> dict[str, Any]:
    mask = df["exchange"].eq(exchange.upper()) & df["tradingsymbol"].eq(tradingsymbol.upper())
    matches = df.loc[mask]
    if matches.empty:
        raise KeyError(f"Instrument not found: {exchange}:{tradingsymbol}")
    if len(matches) > 1:
        raise ValueError(f"Multiple instruments found for {exchange}:{tradingsymbol}")
    record = matches.iloc[0].to_dict()
    record["instrument_token"] = int(record["instrument_token"])
    return record
