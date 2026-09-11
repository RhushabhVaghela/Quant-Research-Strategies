import pandas as pd
from src.data.validation import assert_valid, validate_ohlcv

def valid_df():
    idx = pd.date_range("2026-01-01 09:15", periods=2, freq="5min", tz="Asia/Kolkata")
    return pd.DataFrame({
        "open":[100.0,101.0],"high":[102.0,103.0],
        "low":[99.0,100.0],"close":[101.0,102.0],"volume":[1000,1200]
    }, index=idx)

def test_valid_data_passes():
    assert assert_valid(valid_df()).passed

def test_negative_volume_fails():
    df = valid_df(); df.iloc[0,4] = -1
    assert not validate_ohlcv(df).passed

def test_invalid_ohlc_fails():
    df = valid_df(); df.iloc[0,2] = 103
    assert not validate_ohlcv(df).passed

def test_duplicate_timestamp_is_detected():
    df = pd.concat([valid_df(), valid_df().iloc[[0]]])
    assert validate_ohlcv(df).duplicate_timestamps == 1
