"""Diagnostics for Strategy 001 event structure and conditioning."""
from __future__ import annotations

import numpy as np
import pandas as pd

TIME_BINS = {
    "09:15-10:00": (555, 600),
    "10:00-11:00": (600, 660),
    "11:00-12:00": (660, 720),
    "12:00-13:00": (720, 780),
    "13:00-14:00": (780, 840),
    "14:00-15:30": (840, 930),
}


def _validate(df: pd.DataFrame) -> None:
    required = {"close", "volume", "event", "positive_event", "negative_event", "event_direction", "z_score"}
    missing = sorted(required.difference(df.columns))
    if missing:
        raise ValueError(f"Missing required columns: {missing}")
    if not isinstance(df.index, pd.DatetimeIndex):
        raise TypeError("DataFrame index must be a pandas DatetimeIndex")
    if not df.index.is_monotonic_increasing or df.index.has_duplicates:
        raise ValueError("DataFrame index must be increasing and unique")


def add_diagnostic_features(df: pd.DataFrame) -> pd.DataFrame:
    """Add conditioning variables using only information available before the event bar."""
    _validate(df)
    out = df.copy()
    session = pd.Series(out.index.normalize(), index=out.index)
    grouped_close = out["close"].groupby(session)
    grouped_volume = out["volume"].groupby(session)
    log_return = np.log(out["close"]).groupby(session).diff()

    out["prior_return_6bar"] = grouped_close.transform(
        lambda s: s.shift(1).div(s.shift(7)).sub(1.0)
    )
    out["prior_volatility_30bar"] = log_return.groupby(session).transform(
        lambda s: s.shift(1).rolling(30, min_periods=30).std(ddof=1)
    )
    out["prior_volume_median_30bar"] = grouped_volume.transform(
        lambda s: s.shift(1).rolling(30, min_periods=30).median()
    )
    out["volume_ratio_30bar"] = out["volume"].div(
        out["prior_volume_median_30bar"].replace(0.0, np.nan)
    )
    out["abs_z_score"] = out["z_score"].abs()

    minutes = out.index.hour * 60 + out.index.minute
    out["time_of_day"] = "outside_session"
    for label, (start, end) in TIME_BINS.items():
        out.loc[(minutes >= start) & (minutes < end), "time_of_day"] = label

    out["trend_regime"] = np.select(
        [out["prior_return_6bar"] < 0, out["prior_return_6bar"] > 0],
        ["down", "up"],
        default="flat",
    )

    # Compare the event bar's already-computed prior volatility with a
    # point-in-time baseline made only from earlier completed volatility
    # observations.  The observation window intentionally spans sessions and
    # counts valid volatility observations rather than raw dataframe rows.
    # This avoids an overnight NaN gap consuming part of the 60-observation
    # baseline and incorrectly leaving early next-session bars as "unknown".
    prior_volatility_observations = out["prior_volatility_30bar"].shift(1).dropna()
    prior_volatility_median = (
        prior_volatility_observations.rolling(60, min_periods=30).median().reindex(out.index)
    )
    out["volatility_regime"] = np.select(
        [out["prior_volatility_30bar"] >= prior_volatility_median,
         out["prior_volatility_30bar"] < prior_volatility_median],
        ["high", "low"],
        default="unknown",
    )
    out["volume_regime"] = np.select(
        [out["volume_ratio_30bar"] < 1.0, out["volume_ratio_30bar"] >= 1.0],
        ["below_prior_median", "at_or_above_prior_median"],
        default="unknown",
    )
    out["severity_regime"] = pd.cut(
        out["abs_z_score"],
        bins=[-np.inf, 2.5, 3.0, np.inf],
        labels=["2.0-2.5", "2.5-3.0", "3.0+"],
        right=False,
    ).astype("string")
    return out


def mark_non_overlapping_events(df: pd.DataFrame, cooldown_bars: int = 12) -> pd.DataFrame:
    """Mark the first event, then suppress later events for a fixed cooldown."""
    _validate(df)
    if cooldown_bars < 0:
        raise ValueError("cooldown_bars must be non-negative")
    out = df.copy()
    out["non_overlapping_event"] = False
    for _, session_df in out.groupby(out.index.normalize(), sort=False):
        last_selected = -10**9
        positions = np.flatnonzero(session_df["event"].to_numpy())
        for position in positions:
            if position - last_selected >= cooldown_bars:
                out.loc[session_df.index[position], "non_overlapping_event"] = True
                last_selected = position
    return out


def summarize_dependence(df: pd.DataFrame) -> pd.DataFrame:
    """Summarize event spacing and the effect of the non-overlap filter."""
    rows = []
    for label, column in (("all_events", "event"), ("non_overlapping", "non_overlapping_event")):
        times = df.index[df[column]]
        same_session_gaps = []
        for _, session_df in df.groupby(df.index.normalize(), sort=False):
            positions = np.flatnonzero(session_df[column].to_numpy())
            if len(positions) > 1:
                same_session_gaps.extend(np.diff(positions).tolist())
        gaps = pd.Series(same_session_gaps, dtype=float)
        rows.append({
            "event_set": label,
            "events": int(len(times)),
            "same_session_gap_median_bars": gaps.median() if len(gaps) else np.nan,
            "same_session_gap_p10_bars": gaps.quantile(0.10) if len(gaps) else np.nan,
            "same_session_gap_lt_12_bars_pct": (gaps < 12).mean() if len(gaps) else np.nan,
        })
    return pd.DataFrame(rows)


def _summary_rows(df: pd.DataFrame, horizons: tuple[int, ...], event_column: str) -> pd.DataFrame:
    rows = []
    mask = df[event_column].astype(bool)
    for direction_name, direction_mask, direction in (
        ("all", mask, 0), ("positive", mask & df["positive_event"], 1),
        ("negative", mask & df["negative_event"], -1),
    ):
        for horizon in horizons:
            values = df.loc[direction_mask, f"forward_return_{horizon}bar"].dropna()
            if direction == 1:
                aligned = -values
            elif direction == -1:
                aligned = values
            else:
                aligned = pd.concat([
                    -df.loc[direction_mask & df["positive_event"], f"forward_return_{horizon}bar"].dropna(),
                    df.loc[direction_mask & df["negative_event"], f"forward_return_{horizon}bar"].dropna(),
                ])
            n = len(values)
            mean = values.mean() if n else np.nan
            std = values.std(ddof=1) if n > 1 else np.nan
            t_stat = mean / (std / np.sqrt(n)) if n > 1 and std > 0 else np.nan
            rows.append({
                "event_set": event_column, "direction": direction_name,
                "horizon_bars": horizon, "events": int(n),
                "mean_forward_return": mean,
                "median_forward_return": values.median() if n else np.nan,
                "std_forward_return": std,
                "win_rate_raw": (values > 0).mean() if n else np.nan,
                "mean_reversion_aligned_return": aligned.mean() if len(aligned) else np.nan,
                "t_stat_mean_raw": t_stat,
            })
    return pd.DataFrame(rows)


def conditioning_summary(df: pd.DataFrame, feature: str, horizon: int = 6,
                          event_column: str = "event") -> pd.DataFrame:
    """Summarize outcomes by one predefined conditioning variable."""
    mask = df[event_column].astype(bool)
    rows = []
    for level, subset in df.loc[mask].groupby(feature, dropna=False, observed=False):
        values = subset[f"forward_return_{horizon}bar"].dropna()
        directions = subset.loc[values.index, "event_direction"]
        aligned = -directions * values
        rows.append({
            "feature": feature, "level": str(level), "event_set": event_column,
            "horizon_bars": horizon, "events": int(len(values)),
            "mean_forward_return": values.mean() if len(values) else np.nan,
            "mean_reversion_aligned_return": aligned.mean() if len(aligned) else np.nan,
            "win_rate_raw": (values > 0).mean() if len(values) else np.nan,
            "median_forward_return": values.median() if len(values) else np.nan,
        })
    return pd.DataFrame(rows).sort_values(["feature", "level"]).reset_index(drop=True)


def build_conditioning_report(df: pd.DataFrame, horizons: tuple[int, ...] = (1, 3, 6, 12)) -> pd.DataFrame:
    """Build fixed conditioning tables without parameter search."""
    frames = []
    for feature in ("time_of_day", "trend_regime", "volatility_regime", "volume_regime", "severity_regime"):
        for horizon in horizons:
            frames.append(conditioning_summary(df, feature, horizon))
            frames.append(conditioning_summary(df, feature, horizon, "non_overlapping_event"))
    return pd.concat(frames, ignore_index=True)
