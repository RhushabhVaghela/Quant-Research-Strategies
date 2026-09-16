"""Prospective capture and paper-shadow bookkeeping for frozen Strategy 001D.

This module is deliberately separated from the historical backtest. It provides
append-only records for a live/prospective run and does not place orders.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Iterable

import numpy as np
import pandas as pd

from src.research.continuation_backtest import build_signals


IST = "Asia/Kolkata"
STRATEGY_VERSION = "001D"
PROTOCOL_VERSION = "001I"
BAR_MINUTES = 5
HOLDING_BARS = 6
COOLDOWN_BARS = 12

SIGNAL_COLUMNS = [
    "signal_id", "strategy_version", "protocol_version", "signal_timestamp",
    "session_date", "time_of_day", "time_of_day_bucket", "signal_close",
    "prior_mean_30", "prior_std_30", "z_score", "prior_return_6bar", "volume",
    "prior_volume_mean_30", "volume_ratio_30", "intended_entry_timestamp",
    "intended_entry_price", "intended_exit_timestamp", "status", "capture_timestamp",
    "capture_wallclock", "signal_bid", "signal_ask", "signal_spread_bps",
]

OUTCOME_COLUMNS = [
    "signal_id", "observable_or_paper_entry_price", "observable_or_paper_exit_price",
    "gross_return", "observed_entry_spread_bps", "observed_exit_spread_bps",
    "estimated_slippage_bps", "brokerage_and_statutory_costs", "net_return",
    "mfe_return", "mae_return", "mfe_timestamp", "mae_timestamp",
    "outcome_recorded_timestamp", "operational_exception",
]

BAR_COLUMNS = [
    "timestamp", "open", "high", "low", "close", "volume",
    "first_tick_timestamp", "last_tick_timestamp", "best_bid_last", "best_ask_last",
]


@dataclass(frozen=True)
class RunManifest:
    activation_timestamp: str
    strategy_version: str = STRATEGY_VERSION
    protocol_version: str = PROTOCOL_VERSION
    instrument: str = "NSE:GOLDBEES"
    interval: str = "5minute"
    mode: str = "paper_shadow"
    live_orders_enabled: bool = False
    notes: str = "Frozen Strategy 001D; prospective observations only."


def _as_ist_timestamp(value: Any) -> pd.Timestamp:
    ts = pd.Timestamp(value)
    if ts.tzinfo is None:
        return ts.tz_localize(IST)
    return ts.tz_convert(IST)


def _append_row(path: Path, row: dict[str, Any], columns: Iterable[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    frame = pd.DataFrame([{column: row.get(column, np.nan) for column in columns}])
    header = not path.exists()
    frame.to_csv(path, mode="a", header=header, index=False)


def _read_csv(path: Path, columns: Iterable[str]) -> pd.DataFrame:
    if not path.exists():
        return pd.DataFrame(columns=list(columns))
    return pd.read_csv(path)


def initialize_run(output_dir: str | Path, activation_timestamp: Any, notes: str = "") -> RunManifest:
    """Create the append-only prospective run structure and manifest."""
    root = Path(output_dir)
    root.mkdir(parents=True, exist_ok=True)
    activation = _as_ist_timestamp(activation_timestamp)
    manifest = RunManifest(
        activation_timestamp=activation.isoformat(),
        notes=notes or RunManifest.__dataclass_fields__["notes"].default,
    )
    (root / "run_manifest.json").write_text(json.dumps(asdict(manifest), indent=2), encoding="utf-8")
    for name, columns in (("signals.csv", SIGNAL_COLUMNS), ("outcomes.csv", OUTCOME_COLUMNS), ("bars.csv", BAR_COLUMNS)):
        path = root / name
        if not path.exists():
            pd.DataFrame(columns=columns).to_csv(path, index=False)
    return manifest


def load_live_bars(path: str | Path) -> pd.DataFrame:
    """Load completed prospective bars written by the live collector."""
    df = pd.read_csv(path)
    if df.empty:
        return pd.DataFrame(columns=BAR_COLUMNS)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    if df["timestamp"].dt.tz is None:
        df["timestamp"] = df["timestamp"].dt.tz_localize(IST)
    else:
        df["timestamp"] = df["timestamp"].dt.tz_convert(IST)
    return df.sort_values("timestamp").drop_duplicates("timestamp", keep="last").reset_index(drop=True)


def append_completed_bar(output_dir: str | Path, bar: dict[str, Any]) -> None:
    """Append one completed live 5-minute bar; duplicates are rejected."""
    root = Path(output_dir)
    existing = load_live_bars(root / "bars.csv")
    ts = _as_ist_timestamp(bar["timestamp"])
    if not existing.empty and ts in set(existing["timestamp"]):
        raise ValueError(f"Completed bar already recorded: {ts}")
    payload = dict(bar)
    payload["timestamp"] = ts.isoformat()
    _append_row(root / "bars.csv", payload, BAR_COLUMNS)


def signal_id(signal_timestamp: Any) -> str:
    return _as_ist_timestamp(signal_timestamp).strftime("001I-%Y%m%d-%H%M")


def evaluate_completed_bar(
    history_bars: pd.DataFrame,
    completed_bar: dict[str, Any],
    capture_timestamp: Any,
    intended_entry_timestamp: Any,
    signal_bid: float | None = None,
    signal_ask: float | None = None,
) -> dict[str, Any] | None:
    """Evaluate exactly one newly completed event bar using only observed bars.

    ``history_bars`` must contain bars observed before ``completed_bar``. The
    completed bar is appended only for evaluating its event condition.
    """
    prior = history_bars.copy()
    current = pd.DataFrame([completed_bar])
    combined = pd.concat([prior, current], ignore_index=True)
    combined["timestamp"] = pd.to_datetime(combined["timestamp"])
    if combined["timestamp"].dt.tz is None:
        combined["timestamp"] = combined["timestamp"].dt.tz_localize(IST)
    else:
        combined["timestamp"] = combined["timestamp"].dt.tz_convert(IST)
    combined = combined.sort_values("timestamp").drop_duplicates("timestamp", keep="last").set_index("timestamp")
    signals = build_signals(combined)
    ts = _as_ist_timestamp(completed_bar["timestamp"])
    row = signals.loc[ts]
    if not bool(row["selected_event"]):
        return None

    entry_ts = _as_ist_timestamp(intended_entry_timestamp)
    capture_ts = _as_ist_timestamp(capture_timestamp)
    if capture_ts > entry_ts:
        raise ValueError("Prospective signal was captured after the intended entry boundary")
    bid = float(signal_bid) if signal_bid is not None and np.isfinite(signal_bid) else np.nan
    ask = float(signal_ask) if signal_ask is not None and np.isfinite(signal_ask) else np.nan
    spread_bps = np.nan
    if np.isfinite(bid) and np.isfinite(ask) and bid > 0:
        spread_bps = (ask - bid) / ((ask + bid) / 2.0) * 10_000.0

    return {
        "signal_id": signal_id(ts),
        "strategy_version": STRATEGY_VERSION,
        "protocol_version": PROTOCOL_VERSION,
        "signal_timestamp": ts.isoformat(),
        "session_date": ts.strftime("%Y-%m-%d"),
        "time_of_day": ts.strftime("%H:%M"),
        "time_of_day_bucket": f"{ts.hour:02d}-{ts.hour + 1:02d}",
        "signal_close": float(row["close"]),
        "prior_mean_30": float(row["prior_mean_30"]),
        "prior_std_30": float(row["prior_std_30"]),
        "z_score": float(row["z_score"]),
        "prior_return_6bar": float(row["prior_return_6bar"]),
        "volume": float(row["volume"]),
        "prior_volume_mean_30": np.nan,
        "volume_ratio_30": np.nan,
        "intended_entry_timestamp": entry_ts.isoformat(),
        "intended_entry_price": np.nan,
        "intended_exit_timestamp": (entry_ts + pd.to_timedelta((HOLDING_BARS - 1) * BAR_MINUTES, unit="min")).isoformat(),
        "status": "signal_observed",
        "capture_timestamp": capture_ts.isoformat(),
        "capture_wallclock": pd.Timestamp.now(tz=IST).isoformat(),
        "signal_bid": bid,
        "signal_ask": ask,
        "signal_spread_bps": spread_bps,
    }


def append_signal(output_dir: str | Path, row: dict[str, Any]) -> None:
    """Append a signal record exactly once."""
    root = Path(output_dir)
    existing = _read_csv(root / "signals.csv", SIGNAL_COLUMNS)
    if not existing.empty and row["signal_id"] in set(existing["signal_id"].astype(str)):
        raise ValueError(f"Signal already recorded: {row['signal_id']}")
    _append_row(root / "signals.csv", row, SIGNAL_COLUMNS)


def finalize_paper_outcome(
    output_dir: str | Path,
    signal_row: dict[str, Any],
    bars: pd.DataFrame,
    outcome_recorded_timestamp: Any,
    estimated_slippage_bps: float = 0.0,
    brokerage_and_statutory_costs: float = 0.0,
) -> dict[str, Any]:
    """Finalize a frozen signal after its exit bar is complete.

    Entry is the observable open of the next bar; exit is the close of the
    frozen t+6 bar. MFE/MAE use OHLC ranges only and are not treated as
    intrabar-executable prices.
    """
    frame = bars.copy()
    frame["timestamp"] = pd.to_datetime(frame["timestamp"])
    if frame["timestamp"].dt.tz is None:
        frame["timestamp"] = frame["timestamp"].dt.tz_localize(IST)
    else:
        frame["timestamp"] = frame["timestamp"].dt.tz_convert(IST)
    frame = frame.sort_values("timestamp").set_index("timestamp")
    entry_ts = _as_ist_timestamp(signal_row["intended_entry_timestamp"])
    exit_bar_ts = _as_ist_timestamp(signal_row["intended_exit_timestamp"])
    if entry_ts not in frame.index or exit_bar_ts not in frame.index:
        raise ValueError("Required entry/exit completed bars are not available")
    entry = float(frame.loc[entry_ts, "open"])
    exit_price = float(frame.loc[exit_bar_ts, "close"])
    if entry <= 0 or exit_price <= 0:
        raise ValueError("Invalid paper entry/exit price")
    window = frame.loc[entry_ts:exit_bar_ts]
    mfe_return = float(window["high"].max() / entry - 1.0)
    mae_return = float(window["low"].min() / entry - 1.0)
    mfe_ts = window["high"].idxmax()
    mae_ts = window["low"].idxmin()
    gross = exit_price / entry - 1.0
    slippage_return = -2.0 * estimated_slippage_bps / 10_000.0
    net = gross + slippage_return - float(brokerage_and_statutory_costs)

    entry_spread = np.nan
    exit_spread = np.nan
    for ts, key in ((entry_ts, "entry"), (exit_bar_ts, "exit")):
        bid_col = f"best_bid_{key}"
        ask_col = f"best_ask_{key}"
        if bid_col in frame.columns and ask_col in frame.columns:
            bid = float(frame.loc[ts, bid_col])
            ask = float(frame.loc[ts, ask_col])
            if bid > 0 and ask > 0:
                value = (ask - bid) / ((ask + bid) / 2.0) * 10_000.0
                if key == "entry":
                    entry_spread = value
                else:
                    exit_spread = value

    return {
        "signal_id": signal_row["signal_id"],
        "observable_or_paper_entry_price": entry,
        "observable_or_paper_exit_price": exit_price,
        "gross_return": gross,
        "observed_entry_spread_bps": entry_spread,
        "observed_exit_spread_bps": exit_spread,
        "estimated_slippage_bps": estimated_slippage_bps,
        "brokerage_and_statutory_costs": brokerage_and_statutory_costs,
        "net_return": net,
        "mfe_return": mfe_return,
        "mae_return": mae_return,
        "mfe_timestamp": _as_ist_timestamp(mfe_ts).isoformat(),
        "mae_timestamp": _as_ist_timestamp(mae_ts).isoformat(),
        "outcome_recorded_timestamp": _as_ist_timestamp(outcome_recorded_timestamp).isoformat(),
        "operational_exception": "",
    }


def append_outcome(output_dir: str | Path, row: dict[str, Any]) -> None:
    """Append a completed outcome exactly once."""
    root = Path(output_dir)
    existing = _read_csv(root / "outcomes.csv", OUTCOME_COLUMNS)
    if not existing.empty and row["signal_id"] in set(existing["signal_id"].astype(str)):
        raise ValueError(f"Outcome already recorded: {row['signal_id']}")
    _append_row(root / "outcomes.csv", row, OUTCOME_COLUMNS)
