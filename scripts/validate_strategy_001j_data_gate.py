"""Validate Strategy 001J intraday data for a frozen session-level window.

This is a pre-backtest gate. It does not create membership, infer missing
symbols, or select a universe. The requested window is expressed as inclusive
calendar dates; validation is performed at the NSE 5-minute session level.

A valid session must:
- begin at 09:15 IST;
- contain regular 5-minute timestamps with no interior gaps;
- contain at least one complete trade opportunity for the frozen 001D
  baseline (37 bars = 30 lookback + signal + entry + 6-bar exit);
- end on or before the normal final 5-minute bar (15:25 IST).

A session may legitimately end before 15:25 (for example, a 15:10 final bar)
provided all bars up to that endpoint are contiguous. This distinguishes
terminal truncation from missing interior data.
"""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd

REQUIRED_MEMBERSHIP = {"symbol", "effective_from", "effective_to"}
REQUIRED_BARS = {"timestamp", "open", "high", "low", "close", "volume"}
SESSION_OPEN = pd.Timedelta("9h15min")
SESSION_LAST_BAR = pd.Timedelta("15h25min")
BAR_INTERVAL = pd.Timedelta("5min")
ONE_DAY = pd.Timedelta("1D")
MIN_BARS_FOR_BASELINE_TRADE = 37


def _parse_window(start: str, end: str) -> tuple[pd.Timestamp, pd.Timestamp]:
    left = pd.Timestamp(start).normalize()
    right = pd.Timestamp(end).normalize()
    if left.tzinfo is None:
        left = left.tz_localize("Asia/Kolkata")
    else:
        left = left.tz_convert("Asia/Kolkata")
    if right.tzinfo is None:
        right = right.tz_localize("Asia/Kolkata")
    else:
        right = right.tz_convert("Asia/Kolkata")
    if right < left:
        raise SystemExit("Research end must be on or after research start.")
    return left, right


def _localize_timestamp(value: pd.Timestamp) -> pd.Timestamp:
    if value.tzinfo is None:
        return value.tz_localize("Asia/Kolkata")
    return value.tz_convert("Asia/Kolkata")


def _load_membership(path: Path) -> pd.DataFrame:
    if not path.exists():
        raise SystemExit(f"Membership file not found: {path}")
    df = pd.read_csv(path)
    missing = REQUIRED_MEMBERSHIP - set(df.columns)
    if missing:
        raise SystemExit(f"Membership missing columns: {sorted(missing)}")
    if df.empty:
        raise SystemExit("U1 membership is empty; a frozen membership file is required.")
    df = df.copy()
    df["symbol"] = df["symbol"].astype(str).str.strip().str.upper()
    df["effective_from"] = pd.to_datetime(df["effective_from"], errors="raise")
    df["effective_to"] = pd.to_datetime(df["effective_to"], errors="raise")
    return df


def _load_bars(path: Path) -> pd.DataFrame:
    frame = pd.read_csv(path, usecols=lambda c: c in REQUIRED_BARS)
    missing = REQUIRED_BARS - set(frame.columns)
    if missing:
        raise ValueError(f"{path}: missing columns {sorted(missing)}")
    ts = pd.to_datetime(frame["timestamp"], errors="raise")
    if ts.dt.tz is None:
        ts = ts.dt.tz_localize("Asia/Kolkata")
    else:
        ts = ts.dt.tz_convert("Asia/Kolkata")
    frame = frame.copy()
    frame["timestamp"] = ts
    frame = frame.set_index("timestamp").sort_index()
    if frame.empty:
        raise ValueError(f"{path}: no rows")
    if frame.index.has_duplicates:
        raise ValueError(f"{path}: duplicate timestamps")
    if (frame[["open", "high", "low", "close"]] <= 0).any().any():
        raise ValueError(f"{path}: non-positive OHLC")
    if (frame["volume"] < 0).any():
        raise ValueError(f"{path}: negative volume")
    return frame


def _apply_membership(symbol: str, frame: pd.DataFrame, membership: pd.DataFrame) -> pd.DataFrame:
    intervals = membership[membership["symbol"] == symbol]
    if intervals.empty:
        raise ValueError(f"No membership interval found for {symbol}")
    keep = pd.Series(False, index=frame.index)
    for row in intervals.itertuples(index=False):
        start = _localize_timestamp(row.effective_from)
        end = _localize_timestamp(row.effective_to)
        keep |= (frame.index >= start) & (frame.index < end)
    return frame.loc[keep]


def _session_diagnostics(frame: pd.DataFrame) -> dict:
    local = frame.index.tz_convert("Asia/Kolkata")
    session_dates = pd.Index(local.normalize().unique()).sort_values()
    missing_interior = 0
    invalid_open = 0
    invalid_close = 0
    short_sessions = 0
    terminal_truncation_sessions = 0
    max_gap_minutes = 0.0

    for session_date in session_dates:
        session = frame[local.normalize() == session_date]
        times = session.index.tz_convert("Asia/Kolkata")
        first_offset = times[0] - times[0].normalize()
        last_offset = times[-1] - times[-1].normalize()
        if first_offset != SESSION_OPEN:
            invalid_open += 1
        if last_offset > SESSION_LAST_BAR:
            invalid_close += 1
        diffs = times[1:] - times[:-1]
        if len(diffs):
            max_gap_minutes = max(max_gap_minutes, float(diffs.max().total_seconds() / 60.0))
            missing_interior += int((diffs != BAR_INTERVAL).sum())
        if len(session) < MIN_BARS_FOR_BASELINE_TRADE:
            short_sessions += 1
        if last_offset < SESSION_LAST_BAR:
            terminal_truncation_sessions += 1

    return {
        "sessions": int(len(session_dates)),
        "missing_interior_gaps": missing_interior,
        "invalid_session_open": invalid_open,
        "invalid_session_close": invalid_close,
        "short_sessions": short_sessions,
        "terminal_truncation_sessions": terminal_truncation_sessions,
        "max_gap_minutes": max_gap_minutes,
    }


def validate(membership_path: Path, data_dir: Path, start: str, end: str) -> pd.DataFrame:
    window_start, window_end = _parse_window(start, end)
    membership = _load_membership(membership_path)
    membership_start = pd.to_datetime(membership["effective_from"]).map(_localize_timestamp)
    membership_end = pd.to_datetime(membership["effective_to"]).map(_localize_timestamp)
    active = membership[(membership_start < window_end + ONE_DAY) & (membership_end > window_start)]
    required_symbols = sorted(active["symbol"].unique())
    if not required_symbols:
        raise SystemExit("No U1 symbols are active in the requested research window.")

    frames: dict[str, pd.DataFrame] = {}
    rows: list[dict] = []
    for symbol in required_symbols:
        path = data_dir / f"{symbol}.csv"
        if not path.exists():
            rows.append({"symbol": symbol, "status": "missing_file"})
            continue
        try:
            frame = _load_bars(path)
            frame = frame.loc[(frame.index >= window_start) & (frame.index < window_end + ONE_DAY)]
            frame = _apply_membership(symbol, frame, membership)
            if frame.empty:
                rows.append({"symbol": symbol, "status": "no_data_in_window"})
                continue
            frames[symbol] = frame
        except (ValueError, pd.errors.ParserError) as exc:
            rows.append({"symbol": symbol, "status": f"invalid_data: {exc}"})

    # The reference session set is the union of sessions actually observed
    # across the locked U1. This avoids hard-coding exchange holidays while
    # still requiring every selected symbol to cover every observed session.
    reference_sessions: set[pd.Timestamp] = set()
    for frame in frames.values():
        local = frame.index.tz_convert("Asia/Kolkata")
        reference_sessions.update(local.normalize().unique())

    for symbol in required_symbols:
        if any(r["symbol"] == symbol for r in rows):
            continue
        frame = frames[symbol]
        diagnostics = _session_diagnostics(frame)
        local_dates = set(frame.index.tz_convert("Asia/Kolkata").normalize())
        missing_sessions = sorted(reference_sessions - local_dates)
        status = "ok"
        if missing_sessions:
            status = "missing_session"
        elif diagnostics["missing_interior_gaps"]:
            status = "interior_gap"
        elif diagnostics["invalid_session_open"]:
            status = "invalid_session_open"
        elif diagnostics["invalid_session_close"]:
            status = "invalid_session_close"
        elif diagnostics["short_sessions"]:
            status = "short_session"
        rows.append({
            "symbol": symbol,
            "status": status,
            "first_timestamp": frame.index.min().isoformat(),
            "last_timestamp": frame.index.max().isoformat(),
            "sessions": diagnostics["sessions"],
            "missing_sessions": len(missing_sessions),
            "missing_interior_gaps": diagnostics["missing_interior_gaps"],
            "invalid_session_open": diagnostics["invalid_session_open"],
            "invalid_session_close": diagnostics["invalid_session_close"],
            "short_sessions": diagnostics["short_sessions"],
            "terminal_truncation_sessions": diagnostics["terminal_truncation_sessions"],
            "max_gap_minutes": diagnostics["max_gap_minutes"],
        })

    report = pd.DataFrame(rows).sort_values("symbol").reset_index(drop=True)
    failed = report[report["status"] != "ok"]
    if not failed.empty:
        counts = failed["status"].value_counts().to_dict()
        raise SystemExit(
            f"001J data gate FAILED for {len(failed)} of {len(report)} required symbols: {counts}. "
            "Repair the underlying data; do not relax the gate to force a pass."
        )
    print(
        f"001J data gate PASSED: {len(report)} U1 symbols cover "
        f"{window_start.date()} through {window_end.date()} with session-level integrity."
    )
    return report


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--membership", default="data/universe/strategy_001j_u1_membership.csv")
    parser.add_argument("--data-dir", default="data/raw/strategy_001j_u1")
    parser.add_argument("--start", required=True, help="Inclusive research start date YYYY-MM-DD")
    parser.add_argument("--end", required=True, help="Inclusive research end date YYYY-MM-DD")
    parser.add_argument("--output", default="data/reports/strategy_001j_data_gate.csv")
    args = parser.parse_args()
    report = validate(Path(args.membership), Path(args.data_dir), args.start, args.end)
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    report.to_csv(output, index=False)


if __name__ == "__main__":
    main()
