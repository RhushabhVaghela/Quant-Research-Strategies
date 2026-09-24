"""Evaluate frozen Strategy 003 under fixed executable economics.

The portfolio rule is frozen: top Q5 long / bottom Q1 short, equal notional,
50% long / 50% short, one 5-minute holding interval, no thresholds or search.
This runner adds only implementation accounting:
- explicit rupee gross portfolio notionals;
- order-level brokerage with the ₹20/order cap;
- actual turnover from position changes;
- statutory charges on executed turnover;
- separate frozen spread/slippage and impact scenarios;
- late-session / closing-auction exposure flags.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd

BROKER_RATE = 0.0003
BROKER_CAP = 20.0
STT_RATE = 0.00025
NSE_TX_RATE = 0.0000307
STAMP_RATE = 0.00003
SEBI_RATE = 0.000001
GST_RATE = 0.18

FRICTIONS = {
    "fee_floor": (0.0, 0.0),
    "low": (0.00005, 0.00005),
    "base": (0.00010, 0.00005),
    "stress": (0.00020, 0.00010),
}

DEFAULT_PORTFOLIO_NOTIONAL = 100_000.0
HOLDOUT_START = pd.Timestamp("2026-08-20 00:00:00", tz="Asia/Kolkata")
CAS_START = pd.Timedelta(15, unit="h") + pd.Timedelta(15, unit="m")
CAS_END = pd.Timedelta(15, unit="h") + pd.Timedelta(35, unit="m")
NORMAL_CLOSE = pd.Timedelta(15, unit="h") + pd.Timedelta(30, unit="m")
LATE_SESSION_START = pd.Timedelta(15, unit="h")

def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument(
        "directory",
        type=Path,
        nargs="?",
        default=Path("data/raw/strategy_002_universe"),
    )
    p.add_argument(
        "--validation-dir",
        type=Path,
        default=Path("data/reports/strategy_003_protected_validation"),
    )
    p.add_argument(
        "--output-dir",
        type=Path,
        default=Path("data/reports/strategy_003_economic_execution"),
    )
    p.add_argument(
        "--portfolio-notional",
        type=float,
        default=DEFAULT_PORTFOLIO_NOTIONAL,
        help="Gross portfolio notional in INR. Fixed portfolio rule; this only sets capital scale.",
    )
    if hasattr(p, "parse_known_args"):
        return p.parse_args()

def brokerage(turnover: float | np.ndarray) -> float | np.ndarray:
    return np.minimum(BROKER_CAP, BROKER_RATE * turnover)

def fee_breakdown(orders: pd.DataFrame) -> dict[str, float]:
    if orders.empty:
        return {
            "brokerage": 0.0, "stt": 0.0, "stamp_duty": 0.0,
            "sebi": 0.0, "gst": 0.0, "fee_total": 0.0,
            "buy_turnover": 0.0, "sell_turnover": 0.0, "total_turnover": 0.0,
        }
    buy = float(orders.loc[orders.side == "buy", "notional"].sum())
    sell = float(orders.loc[orders.side == "sell", "notional"].sum())
    total = buy + sell
    broker = float(np.sum(brokerage(orders["notional"].to_numpy(dtype=float))))
    tx = NSE_TX_RATE * total
    stt = STT_RATE * sell
    stamp = STAMP_RATE * buy
    sebi = SEBI_RATE * total
    gst = GST_RATE * (broker + tx + sebi)
    fee_total = broker + stt + stamp + sebi + gst
    return {
        "brokerage": broker,
        "stt": stt,
        "stamp_duty": stamp,
        "sebi": sebi,
        "gst": gst,
        "fee_total": fee_total,
        "buy_turnover": buy,
        "sell_turnover": sell,
        "total_turnover": total,
    }

def assign_quintiles(scored: pd.DataFrame) -> pd.DataFrame:
    work = scored.copy()
    work["quintile"] = work.groupby("timestamp").prediction.rank(
        method="first", pct=True
    ).map(lambda x: min(5, int(np.ceil(x * 5))))
    return work

def build_target_portfolios(scored: pd.DataFrame, portfolio_notional: float) -> tuple[pd.DataFrame, pd.DataFrame]:
    rows = []
    weights = {}
    for ts, g in scored.groupby("timestamp", sort=True):
        long = g[g.quintile == 5]
        short = g[g.quintile == 1]
        if len(long) != 3 or len(short) != 3:
            continue
        long_weight = 0.5 / 3.0
        short_weight = -0.5 / 3.0
        ts_weights = {row.symbol: long_weight for _, row in long.iterrows()}
        ts_weights.update({row.symbol: short_weight for _, row in short.iterrows()})
        weights[pd.Timestamp(ts)] = ts_weights
        gross_return = (
            0.5 * float(long.target_excess_1bar.mean())
            - 0.5 * float(short.target_excess_1bar.mean())
        )
        rows.append(
            {
                "timestamp": pd.Timestamp(ts),
                "gross_return": gross_return,
                "long_count": len(long),
                "short_count": len(short),
            }
        )
    bars = pd.DataFrame(rows)
    if bars.empty:
        raise ValueError("No complete Q1/Q5 portfolios")
    order_rows = []
    previous: dict[str, float] = {}
    first = True
    for ts in bars.timestamp:
        current = weights[ts]
        symbols = set(previous) | set(current)
        for symbol in sorted(symbols):
            delta = current.get(symbol, 0.0) - previous.get(symbol, 0.0)
            if np.isclose(delta, 0.0):
                continue
            side = "buy" if delta > 0 else "sell"
            order_rows.append(
                {
                    "timestamp": ts,
                    "symbol": symbol,
                    "side": side,
                    "notional": abs(delta) * portfolio_notional,
                    "weight_change": abs(delta),
                    "opening_rebalance": first,
                }
            )
        previous = current
        first = False
    # Close any residual positions at the final timestamp.
    if previous:
        final_ts = bars.timestamp.iloc[-1]
        for symbol, weight in sorted(previous.items()):
            if np.isclose(weight, 0.0):
                continue
            order_rows.append(
                {
                    "timestamp": final_ts,
                    "symbol": symbol,
                    "side": "sell" if weight > 0 else "buy",
                    "notional": abs(weight) * portfolio_notional,
                    "weight_change": abs(weight),
                    "opening_rebalance": False,
                }
            )
    orders = pd.DataFrame(order_rows)
    return bars, orders

def execution_flags(timestamp: pd.Timestamp) -> dict[str, object]:
    local = pd.Timestamp(timestamp).tz_convert("Asia/Kolkata")
    tod = local - local.normalize()
    return {
        "late_session": bool(tod >= LATE_SESSION_START),
        "closing_auction_window": bool(
            tod >= CAS_START and tod < CAS_END
        ),
        "continuous_trading_window_ends": bool(tod < NORMAL_CLOSE),
    }

def main() -> None:
    args = parse_args()
    if args.portfolio_notional <= 0:
        raise ValueError("portfolio-notional must be positive")
    args.output_dir.mkdir(parents=True, exist_ok=True)

    scored_path = args.validation_dir / "protected_validation_scored_observations.csv"
    scored = pd.read_csv(scored_path, parse_dates=["timestamp"])
    scored["timestamp"] = pd.DatetimeIndex(scored["timestamp"]).tz_convert("Asia/Kolkata")

    # Hard boundary: only the already-generated protected validation sample is read.
    if (scored["timestamp"] >= HOLDOUT_START).any():
        raise ValueError("Protected scored observations contain final-holdout timestamps")

    scored = assign_quintiles(scored)
    bars, orders = build_target_portfolios(scored, args.portfolio_notional)
    fees = fee_breakdown(orders)

    flags = pd.DataFrame(
        [{"timestamp": ts, **execution_flags(ts)} for ts in bars.timestamp]
    )
    bars = bars.merge(flags, on="timestamp", how="left")
    late_count = int(bars["late_session"].sum())
    auction_count = int(bars["closing_auction_window"].sum())

    gross_returns = bars["gross_return"].to_numpy(dtype=float)
    gross_cumulative_return = float(np.prod(1.0 + gross_returns) - 1.0)
    gross_bps_per_bar = float(bars["gross_return"].mean() * 1e4)

    total_turnover = float(orders["notional"].sum())
    turnover_multiple = total_turnover / args.portfolio_notional
    fee_only_bps_on_turnover = (
        fees["fee_total"] / total_turnover * 1e4 if total_turnover else 0.0
    )

    out = []
    for name, (spread, impact) in FRICTIONS.items():
        extra_cost = float((spread + impact) * total_turnover)
        total_cost = fees["fee_total"] + extra_cost
        net_currency = gross_cumulative_return * args.portfolio_notional - total_cost
        net_return = net_currency / args.portfolio_notional
        out.append(
            {
                "scenario": name,
                "portfolio_notional_inr": args.portfolio_notional,
                "timestamps": int(len(bars)),
                "gross_cumulative_return": gross_cumulative_return,
                "gross_cumulative_bps": gross_cumulative_return * 1e4,
                "mean_gross_bps_per_bar": gross_bps_per_bar,
                "fee_only_cost_inr": fees["fee_total"],
                "fee_only_cost_bps_on_turnover": fee_only_bps_on_turnover,
                "additional_execution_friction_inr": extra_cost,
                "total_cost_inr": total_cost,
                "total_cost_bps_on_turnover": total_cost / total_turnover * 1e4 if total_turnover else 0.0,
                "net_cumulative_return": net_return,
                "net_cumulative_bps": net_return * 1e4,
                "mean_net_bps_per_bar": net_return / len(bars) * 1e4,
                "turnover_inr": total_turnover,
                "turnover_multiple_of_gross_portfolio": turnover_multiple,
            }
        )

    pd.DataFrame(out).to_csv(
        args.output_dir / "economic_scenario_summary.csv", index=False
    )
    pd.DataFrame([fees]).to_csv(
        args.output_dir / "fee_breakdown.csv", index=False
    )
    bars.to_csv(args.output_dir / "gross_portfolio_bars.csv", index=False)
    orders.to_csv(args.output_dir / "executed_order_turnover.csv", index=False)

    diagnostics = {
        "portfolio_notional_inr": args.portfolio_notional,
        "portfolio_rule": "Q5 long / Q1 short, equal-notional within side, 50%/50%, one-bar hold",
        "timestamps": int(len(bars)),
        "late_session_timestamps": late_count,
        "closing_auction_flagged_timestamps": auction_count,
        "turnover_inr": total_turnover,
        "turnover_multiple_of_gross_portfolio": turnover_multiple,
        "brokerage_order_count": int(len(orders)),
        "average_order_notional_inr": float(orders["notional"].mean()) if not orders.empty else 0.0,
        "short_side_present": bool((orders.side == "sell").any()),
        "final_holdout_used": False,
    }
    (args.output_dir / "execution_diagnostics.json").write_text(
        json.dumps(diagnostics, indent=2), encoding="utf-8"
    )

    manifest = {
        "experiment": "003_economic_execution",
        "status": "executed_on_frozen_protected_validation_signal",
        "portfolio_notional_inr": args.portfolio_notional,
        "portfolio": "top_Q5_long_bottom_Q1_short_equal_notional_50_50_gross",
        "holding_bars": 1,
        "gross_exposure": 1.0,
        "net_exposure": 0.0,
        "turnover_accounting": "actual_position_changes_plus_final_close",
        "brokerage_accounting": "per_executed_order_with_20_inr_cap",
        "protected_validation_source_only": True,
        "final_holdout_used": False,
        "closing_auction_timestamps_flagged": True,
        "feature_search": False,
        "threshold_search": False,
        "holding_period_search": False,
        "universe_search": False,
        "cost_search": False,
    }
    (args.output_dir / "run_manifest.json").write_text(
        json.dumps(manifest, indent=2), encoding="utf-8"
    )

    print("Strategy 003 economic execution test complete")
    print(f"Portfolio timestamps: {len(bars)}")
    print(f"Portfolio notional: INR {args.portfolio_notional:,.0f}")
    print(f"Executed turnover: INR {total_turnover:,.2f} ({turnover_multiple:.3f}x gross portfolio)")
    print(f"Late-session flagged timestamps: {late_count}; closing-auction flagged: {auction_count}")
    print(f"Outputs: {args.output_dir}")

if __name__ == "__main__":
    main()
