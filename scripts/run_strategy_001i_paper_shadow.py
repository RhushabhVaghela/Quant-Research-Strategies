"""Run frozen Strategy 001D prospectively in paper/shadow mode.

The process uses KiteTicker only for live market data. It never places orders.
Start it before the market session and leave it running through the session.
Historical data is used only for pre-activation warm-up; prospective bars are
written locally as they complete.
"""

from __future__ import annotations

import argparse
import threading
import time
from datetime import date, datetime, time as dt_time, timedelta
from pathlib import Path

import numpy as np
import pandas as pd
from kiteconnect import KiteTicker

from src.data.kite_client import KiteClient
from src.research.strategy_001i_prospective import (
    BAR_MINUTES,
    IST,
    append_completed_bar,
    append_outcome,
    append_signal,
    evaluate_completed_bar,
    finalize_paper_outcome,
    initialize_run,
    load_live_bars,
    load_run_manifest,
)

MARKET_OPEN = dt_time(9, 15)
MARKET_CLOSE = dt_time(15, 30)
SYMBOL = "GOLDBEES"
EXCHANGE = "NSE"


def _next_weekday(day: date) -> date:
    candidate = day + timedelta(days=1)
    while candidate.weekday() >= 5:
        candidate += timedelta(days=1)
    return candidate


def _next_session_open(now: pd.Timestamp) -> pd.Timestamp:
    day = now.date()
    if now.time() >= MARKET_CLOSE or now.weekday() >= 5:
        day = _next_weekday(day) if now.weekday() < 5 else day
        while day.weekday() >= 5:
            day += timedelta(days=1)
        return pd.Timestamp(datetime.combine(day, MARKET_OPEN), tz=IST)
    if now.time() < MARKET_OPEN:
        return pd.Timestamp(datetime.combine(day, MARKET_OPEN), tz=IST)
    return now


class TickBarBuffer:
    """Thread-safe in-memory tick buffer keyed by 5-minute candle start."""

    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._ticks: dict[pd.Timestamp, list[dict]] = {}

    @staticmethod
    def _timestamp(tick: dict) -> pd.Timestamp:
        value = tick.get("exchange_timestamp") or tick.get("timestamp") or tick.get("last_trade_time")
        if value is None:
            raise ValueError("Tick has no exchange timestamp")
        ts = pd.Timestamp(value)
        if ts.tzinfo is None:
            ts = ts.tz_localize(IST)
        else:
            ts = ts.tz_convert(IST)
        return ts

    def add(self, tick: dict) -> None:
        ts = self._timestamp(tick)
        bucket = ts.floor(f"{BAR_MINUTES}min")
        with self._lock:
            self._ticks.setdefault(bucket, []).append(dict(tick))

    def pop(self, bucket: pd.Timestamp) -> list[dict]:
        with self._lock:
            return self._ticks.pop(bucket, [])


def _best_bid_ask(tick: dict) -> tuple[float, float]:
    depth = tick.get("depth") or {}
    buys = depth.get("buy") or []
    sells = depth.get("sell") or []
    bid = float(buys[0]["price"]) if buys else np.nan
    ask = float(sells[0]["price"]) if sells else np.nan
    return bid, ask


def _build_bar(bucket: pd.Timestamp, ticks: list[dict]) -> dict:
    if not ticks:
        raise ValueError(f"No ticks captured for {bucket}")
    ordered = sorted(ticks, key=lambda t: pd.Timestamp(t.get("exchange_timestamp") or t.get("timestamp")))
    prices = [float(t["last_price"]) for t in ordered if t.get("last_price") is not None]
    if not prices:
        raise ValueError(f"No last_price values captured for {bucket}")
    volumes = [float(t.get("volume_traded", t.get("volume", np.nan))) for t in ordered]
    finite_volumes = [v for v in volumes if np.isfinite(v)]
    volume = max(finite_volumes) - min(finite_volumes) if len(finite_volumes) >= 2 else np.nan
    bid, ask = _best_bid_ask(ordered[-1])
    first_ts = pd.Timestamp(ordered[0].get("exchange_timestamp") or ordered[0].get("timestamp"))
    last_ts = pd.Timestamp(ordered[-1].get("exchange_timestamp") or ordered[-1].get("timestamp"))
    return {
        "timestamp": bucket.isoformat(),
        "open": prices[0],
        "high": max(prices),
        "low": min(prices),
        "close": prices[-1],
        "volume": volume,
        "first_tick_timestamp": first_ts.isoformat(),
        "last_tick_timestamp": last_ts.isoformat(),
        "best_bid_last": bid,
        "best_ask_last": ask,
    }


def _warmup_history(kite, token: int, end_date: date) -> pd.DataFrame:
    start = end_date - timedelta(days=7)
    rows = kite.historical_data(
        token,
        start.strftime("%Y-%m-%d 09:15:00"),
        end_date.strftime("%Y-%m-%d 15:30:00"),
        "5minute",
    )
    frame = pd.DataFrame(rows)
    if frame.empty:
        raise RuntimeError("Kite historical API returned no warm-up candles")
    if "date" in frame.columns:
        frame = frame.rename(columns={"date": "timestamp"})
    frame["timestamp"] = pd.to_datetime(frame["timestamp"])
    if frame["timestamp"].dt.tz is None:
        frame["timestamp"] = frame["timestamp"].dt.tz_localize(IST)
    else:
        frame["timestamp"] = frame["timestamp"].dt.tz_convert(IST)
    frame = frame.set_index("timestamp").sort_index()
    frame = frame[frame.index.date <= end_date]
    return frame[["open", "high", "low", "close", "volume"]]


def _session_boundaries(day: date) -> list[pd.Timestamp]:
    start = pd.Timestamp(datetime.combine(day, MARKET_OPEN), tz=IST)
    end = pd.Timestamp(datetime.combine(day, MARKET_CLOSE), tz=IST)
    return list(pd.date_range(start + pd.Timedelta(minutes=BAR_MINUTES), end, freq=f"{BAR_MINUTES}min"))


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", default="data/prospective/strategy_001i", help="Prospective run directory")
    parser.add_argument(
        "--activation",
        default=None,
        help="Activation timestamp in IST. Used only when creating a new run directory.",
    )
    args = parser.parse_args()

    root = Path(args.output)
    now = pd.Timestamp.now(tz=IST)
    existing_manifest = load_run_manifest(root) if (root / "run_manifest.json").exists() else None
    if existing_manifest is not None:
        if args.activation is not None and _as_activation(args.activation, now) != pd.Timestamp(existing_manifest.activation_timestamp):
            raise ValueError("Existing prospective run already has an immutable activation timestamp")
        manifest = existing_manifest
    else:
        requested_activation = _as_activation(args.activation, now)
        manifest = initialize_run(root, requested_activation, notes="Prospective paper/shadow capture. Live orders disabled.")
    activation = pd.Timestamp(manifest.activation_timestamp).tz_convert(IST)
    session_day = activation.date()

    client = KiteClient()
    instruments = pd.DataFrame(client.instruments(EXCHANGE))
    matches = instruments[instruments["tradingsymbol"].eq(SYMBOL)]
    if matches.empty:
        raise RuntimeError(f"Could not resolve {EXCHANGE}:{SYMBOL} in current instrument master")
    token = int(matches.iloc[0]["instrument_token"])
    print(f"Resolved {EXCHANGE}:{SYMBOL} instrument token {token}")
    print(f"Prospective activation boundary: {activation.isoformat()}")

    warmup_date = _previous_weekday(session_day)
    warmup = _warmup_history(client.kite, token, warmup_date)
    live_bars = load_live_bars(root / "bars.csv")
    buffer = TickBarBuffer()
    ticker = KiteTicker(client.api_key, client.access_token)

    def on_connect(ws, _response):
        ws.subscribe([token])
        ws.set_mode(ws.MODE_FULL, [token])
        print("KiteTicker connected; full-mode market data subscribed.")

    def on_ticks(_ws, ticks):
        for tick in ticks:
            if int(tick.get("instrument_token", -1)) == token:
                buffer.add(tick)

    def on_close(_ws, code, reason):
        print(f"KiteTicker closed: code={code}, reason={reason}")

    ticker.on_connect = on_connect
    ticker.on_ticks = on_ticks
    ticker.on_close = on_close
    ticker.connect(threaded=True)

    session_open = pd.Timestamp(datetime.combine(session_day, MARKET_OPEN), tz=IST)
    if pd.Timestamp.now(tz=IST) < session_open:
        while pd.Timestamp.now(tz=IST) < session_open:
            time.sleep(1.0)

    print("001I paper/shadow collector running. No orders will be placed.")
    for boundary in _session_boundaries(session_day):
        if boundary < activation:
            continue
        while pd.Timestamp.now(tz=IST) < boundary:
            time.sleep(0.2)
        completed_bucket = boundary - pd.Timedelta(minutes=BAR_MINUTES)
        ticks = buffer.pop(completed_bucket)
        if not ticks:
            print(f"DATA_MISSING {completed_bucket}: no ticks captured; no retrospective reconstruction")
            continue

        bar = _build_bar(completed_bucket, ticks)
        append_completed_bar(root, bar)
        live_bars = load_live_bars(root / "bars.csv")

        prior_live = live_bars.iloc[:-1].copy()
        current = live_bars.iloc[-1].to_dict()
        current["timestamp"] = pd.Timestamp(current["timestamp"])
        history = warmup.reset_index().rename(columns={"index": "timestamp"})
        combined_history = pd.concat([history, prior_live], ignore_index=True)

        try:
            signal = evaluate_completed_bar(
                combined_history,
                current,
                capture_timestamp=boundary,
                intended_entry_timestamp=boundary,
                signal_bid=bar.get("best_bid_last"),
                signal_ask=bar.get("best_ask_last"),
                activation_timestamp=activation,
            )
        except ValueError as exc:
            print(f"OPERATIONAL_ERROR {completed_bucket}: {exc}")
            signal = None
        if signal is not None:
            append_signal(root, signal)
            print(f"SIGNAL {signal['signal_id']} z={signal['z_score']:.3f} entry={signal['intended_entry_timestamp']}")

        signals = pd.read_csv(root / "signals.csv")
        outcomes = pd.read_csv(root / "outcomes.csv")
        done = set(outcomes["signal_id"].astype(str)) if not outcomes.empty else set()
        for _, signal_row in signals.iterrows():
            if str(signal_row["signal_id"]) in done:
                continue
            exit_ts = pd.Timestamp(signal_row["intended_exit_timestamp"])
            if exit_ts.tzinfo is None:
                exit_ts = exit_ts.tz_localize(IST)
            else:
                exit_ts = exit_ts.tz_convert(IST)
            exit_completion = exit_ts + pd.Timedelta(minutes=BAR_MINUTES)
            if boundary < exit_completion:
                continue
            try:
                outcome = finalize_paper_outcome(
                    root,
                    signal_row.to_dict(),
                    live_bars,
                    outcome_recorded_timestamp=boundary,
                )
                append_outcome(root, outcome)
                print(f"OUTCOME {signal_row['signal_id']} gross={outcome['gross_return']:.6f}")
            except ValueError as exc:
                print(f"OPERATIONAL_ERROR {signal_row['signal_id']}: {exc}")

    ticker.close()
    print("001I session complete. Review signals.csv, outcomes.csv, bars.csv and run_manifest.json.")


def _previous_weekday(day: date) -> date:
    candidate = day - timedelta(days=1)
    while candidate.weekday() >= 5:
        candidate -= timedelta(days=1)
    return candidate


def _as_activation(raw: str | None, now: pd.Timestamp) -> pd.Timestamp:
    if raw:
        ts = pd.Timestamp(raw)
        if ts.tzinfo is None:
            ts = ts.tz_localize(IST)
        else:
            ts = ts.tz_convert(IST)
        return ts
    return _next_session_open(now)


if __name__ == "__main__":
    main()
