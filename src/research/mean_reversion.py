"""Leakage-aware event study for intraday mean reversion."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import numpy as np
import pandas as pd


@dataclass(frozen=True)
class MeanReversionConfig:
    lookback_bars: int = 30
    z_threshold: float = 2.0
    horizons: tuple[int, ...] = (1, 3, 6, 12)


@dataclass(frozen=True)
class MeanReversionEventStudy:
    events: pd.DataFrame
    summary: pd.DataFrame


def load_ohlcv_csv(path: str | Path) -> pd.DataFrame:
    """Load an OHLCV CSV and normalize its timestamp index."""
    frame = pd.read_csv(path)
    if "date" in frame.columns:
        timestamp_col = "date"
    elif "timestamp" in frame.columns:
        timestamp_col = "timestamp"
    else:
        raise ValueError("CSV must contain a 'date' or 'timestamp' column")

    frame[timestamp_col] = pd.to_datetime(frame[timestamp_col], utc=True).dt.tz_convert("Asia/Kolkata")
    frame = frame.set_index(timestamp_col).sort_index()
    required = {"open", "high", "low", "close", "volume"}
    missing = required.difference(frame.columns)
    if missing:
        raise ValueError(f"Missing OHLCV columns: {sorted(missing)}")
    return frame


def add_deviation_features(frame: pd.DataFrame, config: MeanReversionConfig) -> pd.DataFrame:
    """Add point-in-time deviation features.

    The rolling mean/std are shifted by one bar so the event threshold is
    defined only from previously completed observations. The current close
    is then compared with that prior equilibrium.
    """
    if config.lookback_bars < 2:
        raise ValueError("lookback_bars must be >= 2")
    if config.z_threshold <= 0:
        raise ValueError("z_threshold must be > 0")

    result = frame.copy()
    grouped = result["close"].groupby(result.index.date)
    prior_mean = grouped.transform(lambda s: s.rolling(config.lookback_bars, min_periods=config.lookback_bars).mean().shift(1))
    prior_std = grouped.transform(lambda s: s.rolling(config.lookback_bars, min_periods=config.lookback_bars).std(ddof=1).shift(1))
    result["equilibrium"] = prior_mean
    result["equilibrium_std"] = prior_std
    result["deviation_z"] = (result["close"] - result["equilibrium"]) / result["equilibrium_std"]
    result["deviation_pct"] = (result["close"] / result["equilibrium"]) - 1.0
    result["event_direction"] = np.select(
        [result["deviation_z"] >= config.z_threshold, result["deviation_z"] <= -config.z_threshold],
        [1, -1],
        default=0,
    ).astype(int)
    return result


def _same_session_forward_return(close: pd.Series, horizon: int) -> pd.Series:
    """Forward close return that never crosses a trading session boundary."""
    session = close.index.date
    future = close.shift(-horizon) / close - 1.0
    future_session = pd.Series(session, index=close.index).shift(-horizon)
    future[future_session.to_numpy() != session] = np.nan
    return future


def run_event_study(frame: pd.DataFrame, config: MeanReversionConfig | None = None) -> MeanReversionEventStudy:
    """Run the baseline mean-reversion event study."""
    config = config or MeanReversionConfig()
    work = add_deviation_features(frame, config)

    for horizon in config.horizons:
        if horizon <= 0:
            raise ValueError("All horizons must be positive")
        work[f"forward_return_{horizon}"] = _same_session_forward_return(work["close"], horizon)
        work[f"reversion_return_{horizon}"] = -work["event_direction"] * work[f"forward_return_{horizon}"]

    events = work.loc[work["event_direction"] != 0].copy()
    rows: list[dict[str, float | int | str]] = []

    for direction_name, direction in (("all", 0), ("positive_deviation", 1), ("negative_deviation", -1)):
        subset = events if direction == 0 else events.loc[events["event_direction"] == direction]
        for horizon in config.horizons:
            raw = subset[f"forward_return_{horizon}"].dropna()
            aligned = subset[f"reversion_return_{horizon}"].dropna()
            if len(raw) == 0:
                rows.append({
                    "direction": direction_name,
                    "horizon_bars": horizon,
                    "events": 0,
                    "mean_forward_return": np.nan,
                    "median_forward_return": np.nan,
                    "std_forward_return": np.nan,
                    "win_rate_forward": np.nan,
                    "mean_reversion_aligned_return": np.nan,
                    "win_rate_reversion_aligned": np.nan,
                    "t_stat_reversion_aligned": np.nan,
                    "ci95_low": np.nan,
                    "ci95_high": np.nan,
                })
                continue

            mean = float(aligned.mean())
            std = float(aligned.std(ddof=1)) if len(aligned) > 1 else np.nan
            se = std / np.sqrt(len(aligned)) if np.isfinite(std) else np.nan
            t_stat = mean / se if se and np.isfinite(se) and se > 0 else np.nan
            rows.append({
                "direction": direction_name,
                "horizon_bars": horizon,
                "events": int(len(raw)),
                "mean_forward_return": float(raw.mean()),
                "median_forward_return": float(raw.median()),
                "std_forward_return": float(raw.std(ddof=1)) if len(raw) > 1 else np.nan,
                "win_rate_forward": float((raw > 0).mean()),
                "mean_reversion_aligned_return": mean,
                "win_rate_reversion_aligned": float((aligned > 0).mean()),
                "t_stat_reversion_aligned": t_stat,
                "ci95_low": mean - 1.96 * se if np.isfinite(se) else np.nan,
                "ci95_high": mean + 1.96 * se if np.isfinite(se) else np.nan,
            })

    return MeanReversionEventStudy(events=events, summary=pd.DataFrame(rows))


def event_level_results(study: MeanReversionEventStudy, horizons: tuple[int, ...]) -> pd.DataFrame:
    """Return compact event-level results for CSV export."""
    columns = ["close", "equilibrium", "equilibrium_std", "deviation_z", "deviation_pct", "event_direction"]
    columns += [f"forward_return_{h}" for h in horizons]
    columns += [f"reversion_return_{h}" for h in horizons]
    return study.events.loc[:, columns].copy()
