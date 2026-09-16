"""Point-in-time replay and forward-path diagnostics for frozen Strategy 001D.

This module reconstructs the frozen trades from raw OHLCV, preserves signal-time
features, measures the forward path, and reconciles against the compact 001D
trade export. It deliberately contains no parameter search or strategy changes.
"""

from __future__ import annotations

from pathlib import Path
from typing import Iterable

import numpy as np
import pandas as pd

from src.research.continuation_backtest import build_signals, generate_trades


FORWARD_HORIZONS_MINUTES: tuple[int, ...] = (5, 10, 15, 20, 25, 30, 45, 60)


def _session_key(index: pd.DatetimeIndex) -> pd.Series:
    return pd.Series(index.normalize(), index=index)


def load_ohlcv(path: str | Path) -> pd.DataFrame:
    """Load and normalize an OHLCV CSV using the repository's timestamp contract."""
    df = pd.read_csv(path)
    required = {"timestamp", "open", "high", "low", "close", "volume"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")
    ts = pd.to_datetime(df["timestamp"], errors="raise")
    if ts.dt.tz is None:
        ts = ts.dt.tz_localize("Asia/Kolkata")
    else:
        ts = ts.dt.tz_convert("Asia/Kolkata")
    out = df.copy()
    out["timestamp"] = ts
    out = out.set_index("timestamp").sort_index()
    if out.index.has_duplicates:
        raise ValueError("Data contains duplicate timestamps")
    return out


def build_replay_features(df: pd.DataFrame) -> pd.DataFrame:
    """Build frozen signals plus additional point-in-time diagnostic features."""
    out = build_signals(df)
    session = _session_key(out.index)
    prior_volume = out["volume"].groupby(session, sort=False).shift(1)
    out["prior_volume_mean_30"] = prior_volume.groupby(session, sort=False).transform(
        lambda s: s.rolling(30, min_periods=30).mean()
    )
    out["volume_ratio_30"] = out["volume"] / out["prior_volume_mean_30"].replace(0, np.nan)
    out["session_date"] = out.index.strftime("%Y-%m-%d")
    out["time_of_day"] = out.index.strftime("%H:%M")
    out["time_of_day_bucket"] = (
        out.index.hour.astype(str).str.zfill(2)
        + "-"
        + (out.index.hour + 1).astype(str).str.zfill(2)
    )
    return out


def _trade_rows_from_signals(signals: pd.DataFrame) -> pd.DataFrame:
    """Recreate gross 001D trades while retaining signal-time features."""
    trades = generate_trades(signals)
    if trades.empty:
        return trades
    feature_cols = [
        "session_date", "time_of_day", "time_of_day_bucket", "close",
        "prior_mean_30", "prior_std_30", "z_score", "prior_return_6bar",
        "volume", "prior_volume_mean_30", "volume_ratio_30",
    ]
    feature_frame = signals.loc[trades["signal_timestamp"], feature_cols].copy()
    feature_frame = feature_frame.rename(columns={"close": "signal_close"})
    feature_frame.index.name = "signal_timestamp"
    out = trades.merge(
        feature_frame.reset_index(), on="signal_timestamp", how="left", validate="one_to_one"
    )
    out["trade_id"] = out["signal_timestamp"].astype(str)
    out["signal_horizon_minutes"] = (
        out["exit_timestamp"] - out["signal_timestamp"]
    ).dt.total_seconds() / 60.0
    out["entry_to_exit_minutes"] = (
        out["exit_timestamp"] - out["entry_timestamp"]
    ).dt.total_seconds() / 60.0
    return out


def _same_session_position(index: pd.DatetimeIndex, timestamp: pd.Timestamp) -> int | None:
    matches = np.flatnonzero(index == timestamp)
    return int(matches[0]) if len(matches) else None


def forward_path(
    signals: pd.DataFrame,
    trades: pd.DataFrame,
    horizons_minutes: Iterable[int] = FORWARD_HORIZONS_MINUTES,
) -> pd.DataFrame:
    """Measure forward returns at fixed signal-relative horizons."""
    rows: list[dict] = []
    index = signals.index
    session = _session_key(index).to_numpy()
    close = signals["close"].to_numpy(dtype=float)

    for trade in trades.itertuples(index=False):
        signal_pos = _same_session_position(index, trade.signal_timestamp)
        entry_pos = _same_session_position(index, trade.entry_timestamp)
        if signal_pos is None or entry_pos is None:
            continue
        entry_price = float(trade.entry_price_raw)
        for horizon in horizons_minutes:
            target_ts = trade.signal_timestamp + pd.to_timedelta(int(horizon), unit="min")
            target_pos = _same_session_position(index, target_ts)
            valid = (
                target_pos is not None
                and target_pos >= entry_pos
                and session[target_pos] == session[signal_pos]
            )
            forward_return = np.nan
            if valid:
                forward_return = float(close[target_pos] / entry_price - 1.0)
            rows.append({
                "trade_id": trade.trade_id,
                "signal_timestamp": trade.signal_timestamp,
                "entry_timestamp": trade.entry_timestamp,
                "horizon_minutes": int(horizon),
                "target_timestamp": target_ts if valid else pd.NaT,
                "forward_return": forward_return,
                "available": bool(valid),
            })
    return pd.DataFrame(rows)


def excursion_metrics(signals: pd.DataFrame, trades: pd.DataFrame) -> pd.DataFrame:
    """Calculate OHLC-range MFE/MAE from next-open entry through frozen exit."""
    index = signals.index
    session = _session_key(index).to_numpy()
    rows: list[dict] = []
    for trade in trades.itertuples(index=False):
        entry_pos = _same_session_position(index, trade.entry_timestamp)
        exit_pos = _same_session_position(index, trade.exit_timestamp)
        if entry_pos is None or exit_pos is None or exit_pos < entry_pos:
            continue
        positions = np.arange(entry_pos, exit_pos + 1)
        positions = positions[session[positions] == session[entry_pos]]
        entry = float(trade.entry_price_raw)
        highs = signals.iloc[positions]["high"].to_numpy(dtype=float)
        lows = signals.iloc[positions]["low"].to_numpy(dtype=float)
        mfe_pos = int(positions[int(np.nanargmax(highs))])
        mae_pos = int(positions[int(np.nanargmin(lows))])
        rows.append({
            "trade_id": trade.trade_id,
            "mfe_return": float(np.nanmax(highs) / entry - 1.0),
            "mae_return": float(np.nanmin(lows) / entry - 1.0),
            "mfe_timestamp": index[mfe_pos],
            "mae_timestamp": index[mae_pos],
            "mfe_minutes_from_entry": float((index[mfe_pos] - trade.entry_timestamp).total_seconds() / 60.0),
            "mae_minutes_from_entry": float((index[mae_pos] - trade.entry_timestamp).total_seconds() / 60.0),
        })
    return pd.DataFrame(rows)


def reconcile_trades(replayed: pd.DataFrame, reference: pd.DataFrame, atol: float = 1e-12) -> pd.DataFrame:
    """Compare replayed 001D trades with the compact reference export."""
    if "signal_timestamp" not in reference.columns or "gross_return" not in reference.columns:
        raise ValueError("Reference trade export must contain signal_timestamp and gross_return")
    ref = reference.copy()
    ref["signal_timestamp"] = pd.to_datetime(ref["signal_timestamp"])
    if ref["signal_timestamp"].dt.tz is None:
        ref["signal_timestamp"] = ref["signal_timestamp"].dt.tz_localize("Asia/Kolkata")
    else:
        ref["signal_timestamp"] = ref["signal_timestamp"].dt.tz_convert("Asia/Kolkata")
    left = replayed[["trade_id", "signal_timestamp", "entry_timestamp", "exit_timestamp", "gross_return"]].copy()
    right = ref[["signal_timestamp", "gross_return"]].copy().rename(columns={"gross_return": "reference_gross_return"})
    merged = left.merge(right, on="signal_timestamp", how="outer", indicator=True)
    merged["gross_return_abs_diff"] = (merged["gross_return"] - merged["reference_gross_return"]).abs()
    merged["match"] = (merged["_merge"] == "both") & (merged["gross_return_abs_diff"] <= atol)
    return merged


def run_replay(
    data: pd.DataFrame,
    reference_trades: pd.DataFrame,
    horizons_minutes: Iterable[int] = FORWARD_HORIZONS_MINUTES,
) -> dict[str, pd.DataFrame]:
    """Run the complete 001G replay pipeline."""
    signals = build_replay_features(data)
    replayed = _trade_rows_from_signals(signals)
    path = forward_path(signals, replayed, horizons_minutes)
    excursions = excursion_metrics(signals, replayed)
    reconciliation = reconcile_trades(replayed, reference_trades)
    replayed = replayed.merge(excursions, on="trade_id", how="left", validate="one_to_one")
    return {
        "signals": signals,
        "trades": replayed,
        "forward_path": path,
        "excursions": excursions,
        "reconciliation": reconciliation,
    }


def summarize_forward_path(path: pd.DataFrame) -> pd.DataFrame:
    """Summarize available forward returns by fixed signal-relative horizon."""
    rows: list[dict] = []
    for horizon, group in path.groupby("horizon_minutes", sort=True):
        values = group["forward_return"].dropna().astype(float)
        rows.append({
            "horizon_minutes": int(horizon),
            "observations": int(len(values)),
            "mean_return": float(values.mean()) if len(values) else np.nan,
            "median_return": float(values.median()) if len(values) else np.nan,
            "win_rate": float((values > 0).mean()) if len(values) else np.nan,
            "p10_return": float(values.quantile(0.10)) if len(values) else np.nan,
            "p90_return": float(values.quantile(0.90)) if len(values) else np.nan,
        })
    return pd.DataFrame(rows)
