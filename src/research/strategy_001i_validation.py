"""Integrity checks for a Strategy 001I prospective paper/shadow run."""

from __future__ import annotations

from pathlib import Path

import pandas as pd

from src.research.strategy_001i_prospective import BAR_MINUTES, IST, load_run_manifest


def _ts(value: object) -> pd.Timestamp:
    ts = pd.Timestamp(value)
    if ts.tzinfo is None:
        return ts.tz_localize(IST)
    return ts.tz_convert(IST)


def validate_run(output_dir: str | Path) -> list[str]:
    """Return integrity errors; an empty list means the run passes checks."""
    root = Path(output_dir)
    manifest = load_run_manifest(root)
    activation = _ts(manifest.activation_timestamp)
    errors: list[str] = []

    bars = pd.read_csv(root / "bars.csv")
    signals = pd.read_csv(root / "signals.csv")
    outcomes = pd.read_csv(root / "outcomes.csv")

    if not bars.empty:
        bar_ts = pd.to_datetime(bars["timestamp"])
        bar_ts = bar_ts.dt.tz_localize(IST) if bar_ts.dt.tz is None else bar_ts.dt.tz_convert(IST)
        if bar_ts.duplicated().any():
            errors.append("bars.csv contains duplicate timestamps")
        if not bar_ts.is_monotonic_increasing:
            errors.append("bars.csv is not monotonically ordered")
        if ((bar_ts + pd.to_timedelta(BAR_MINUTES, unit="min")) < activation).any():
            errors.append("bars.csv contains a bar whose completion predates activation")

    if not signals.empty:
        signal_ts = pd.to_datetime(signals["signal_timestamp"])
        capture_ts = pd.to_datetime(signals["capture_timestamp"])
        entry_ts = pd.to_datetime(signals["intended_entry_timestamp"])
        exit_ts = pd.to_datetime(signals["intended_exit_timestamp"])
        for series_name, series in (("signal_timestamp", signal_ts), ("capture_timestamp", capture_ts), ("intended_entry_timestamp", entry_ts), ("intended_exit_timestamp", exit_ts)):
            if series.dt.tz is None:
                series = series.dt.tz_localize(IST)
            else:
                series = series.dt.tz_convert(IST)
            locals()[series_name] = series
        if signals["signal_id"].duplicated().any():
            errors.append("signals.csv contains duplicate signal_id values")
        capture_ts = capture_ts.dt.tz_localize(IST) if capture_ts.dt.tz is None else capture_ts.dt.tz_convert(IST)
        entry_ts = entry_ts.dt.tz_localize(IST) if entry_ts.dt.tz is None else entry_ts.dt.tz_convert(IST)
        exit_ts = exit_ts.dt.tz_localize(IST) if exit_ts.dt.tz is None else exit_ts.dt.tz_convert(IST)
        if (capture_ts < activation).any():
            errors.append("signals.csv contains a signal captured before activation")
        if (capture_ts > entry_ts).any():
            errors.append("signals.csv contains a signal captured after its entry boundary")
        if ((entry_ts - signal_ts) != pd.to_timedelta(BAR_MINUTES, unit="min")).any():
            errors.append("signals.csv contains a non-frozen next-bar entry timestamp")
        if ((exit_ts - signal_ts) != pd.to_timedelta(6 * BAR_MINUTES, unit="min")).any():
            errors.append("signals.csv contains a non-frozen exit timestamp")

    if not outcomes.empty:
        if outcomes["signal_id"].duplicated().any():
            errors.append("outcomes.csv contains duplicate signal_id values")
        signal_ids = set(signals["signal_id"].astype(str)) if not signals.empty else set()
        orphaned = set(outcomes["signal_id"].astype(str)) - signal_ids
        if orphaned:
            errors.append(f"outcomes.csv contains orphan signal_id values: {sorted(orphaned)}")
        outcome_ts = pd.to_datetime(outcomes["outcome_recorded_timestamp"])
        if outcome_ts.dt.tz is None:
            outcome_ts = outcome_ts.dt.tz_localize(IST)
        else:
            outcome_ts = outcome_ts.dt.tz_convert(IST)
        if not signals.empty:
            signal_lookup = signals.set_index("signal_id")
            for idx, row in outcomes.iterrows():
                sid = str(row["signal_id"])
                if sid not in signal_lookup.index:
                    continue
                exit_ts = _ts(signal_lookup.loc[sid, "intended_exit_timestamp"])
                if outcome_ts.iloc[idx] < exit_ts + pd.to_timedelta(BAR_MINUTES, unit="min"):
                    errors.append(f"outcome {sid} was recorded before the frozen exit bar completed")
                    break

    return errors
