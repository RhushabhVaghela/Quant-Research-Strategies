# Strategy 001I — Prospective OOS / Paper-Shadow Validation Protocol

## Purpose

001I is the first genuinely prospective out-of-sample gate for Strategy 001.

The historical research sample has been examined through August 2026. Therefore August 2026, and any September 2026 observations already downloaded or inspected before the prospective process is operational, are **not** treated as pristine OOS evidence.

001I observes the already-frozen 001D strategy prospectively, with each signal recorded before its future outcome is known.

## 1. OOS boundary

**Prospective OOS start:** the activation timestamp recorded in `data/prospective/strategy_001i/run_manifest.json`. A signal becomes eligible only when its event-bar completion/capture occurs at or after that boundary.

The previously proposed September 16 date is not automatically used if the capture system was not operational then. No session is retroactively declared prospective.

Rules:

1. Data observed before activation remains historical/research data.
2. A signal must be captured at the event-bar boundary, before the fixed future exit is known.
3. Once a prospective signal is logged, its strategy parameters cannot be changed for that signal.
4. No prospective outcome may be used to alter the frozen rules during the same validation window.
5. If a strategy rule is later changed, the current 001I cohort is closed; the changed version receives a new version identifier and a new prospective OOS boundary.
6. Restarting the collector against the same run directory must not move the activation boundary. To start a new cohort, use a new run directory and a new registered activation timestamp.
7. If the collector starts after the session has begun, previously completed bars are not reconstructed as prospective observations. The first eligible completed bar is the first one actually captured after activation.

## 2. Frozen strategy

001I uses Strategy 001D exactly as frozen:

- GOLDBEES 5-minute OHLCV;
- previous 30 completed same-session closes;
- sample standard deviation;
- z-score ≥ +2.0;
- prior six-bar return > 0;
- long-only;
- signal at event-bar close;
- next-bar-open entry;
- close of `t+6` exit;
- 12-bar cooldown;
- no overnight feature construction;
- one position at a time;
- no leverage or optimized sizing.

For the live collector, a candle timestamp is treated as the start of the 5-minute candle. Thus a signal on candle `t` is captured when that candle completes at `t+5`, the intended entry is the next candle open at `t+5`, and the frozen exit price is the close of the candle starting at `t+30`, which becomes known when that exit candle completes at `t+35`.

**No threshold, lookback, holding period, cooldown, time-of-day filter, stop, target, or ML filter may be introduced during the prospective window.**

Because the baseline uses previous **same-session** bars, a run started after the session begins may have an initial warm-up period before 30 newly captured same-session bars are available. This is an operational consequence of the frozen feature definition, not a reason to backfill or relabel pre-activation bars as prospective observations.

## 3. Paper/shadow phase

The first phase is **paper/shadow**, not live capital deployment.

The signal engine generates the same intended action as the frozen strategy. No capital is required for a signal to count as a prospective observation.

The repository provides `scripts/run_strategy_001i_paper_shadow.py`. It uses the existing Zerodha authentication/data layer, subscribes to GOLDBEES live ticks in full mode, builds completed 5-minute bars, logs point-in-time signals, and finalizes paper outcomes after the frozen exit bar completes. It never places orders.

The collector should normally be started before the market session. Its activation boundary is immutable for a run. It can be restarted during the same run without changing that boundary.

If actual Zerodha orders are later tested, actual orders must be separately identified from paper observations and governed by a separate controlled-live protocol.

## 4. Point-in-time signal record

Every qualifying signal must be appended before its fixed future outcome is known.

Minimum fields:

```text
signal_id
strategy_version
protocol_version
signal_timestamp
session_date
time_of_day
time_of_day_bucket
signal_close
prior_mean_30
prior_std_30
z_score
prior_return_6bar
volume
prior_volume_mean_30
volume_ratio_30
intended_entry_timestamp
intended_entry_price
intended_exit_timestamp
status
capture_timestamp
capture_wallclock
signal_bid
signal_ask
signal_spread_bps
```

The pre-outcome record is append-only. It must not be overwritten after the forward path is known.

## 5. Outcome record

Only after the frozen exit candle has completed should outcome fields be appended:

```text
observable_or_paper_entry_price
observable_or_paper_exit_price
gross_return
observed_entry_spread_bps
observed_exit_spread_bps
estimated_slippage_bps
brokerage_and_statutory_costs
net_return
MFE
MAE
outcome_recorded_timestamp
operational_exception
```

MFE/MAE remain diagnostics. If they are derived from OHLC ranges, they must not be interpreted as proof that intrabar highs/lows were executable.

The implementation rejects outcome finalization before the frozen exit bar's completion boundary.

## 6. Execution-cost measurement

001H used a simple round-trip friction grid. 001I should replace that assumption with observed execution information where available.

Record separately:

- quoted bid/ask spread at or near signal/entry where observable;
- intended next-bar-open price;
- observable next-bar-open price;
- paper-fill assumption;
- realized slippage if an actual order is eventually tested;
- brokerage and statutory charges when applicable;
- other explicitly modeled friction.

Do not collapse these into one unexplained cost number.

The purpose is to determine whether the small historical gross edge is compatible with actual execution economics.

## 7. Operational controls

Record explicit statuses or exceptions such as:

- `signal_observed`
- `paper_trade_completed`
- `data_missing`
- `session_boundary`
- `execution_observation_missing`
- `operational_error`

Operational failures must be distinguished from strategy failures.

If a bar is missing or delayed, do not reconstruct a signal with later information and label it prospective.

The repository also provides `scripts/validate_strategy_001i_run.py`, which checks the manifest, activation boundary, timestamp ordering, frozen entry/exit timing, duplicate identifiers, orphan outcomes, and outcome-finalization timing.

## 8. No-look-ahead controls

During the prospective window:

1. Do not inspect future bars before signal generation.
2. Do not retune z-score, lookback, holding period, cooldown, or filters.
3. Do not remove losing observations manually.
4. Do not add stops/targets based on observed MFE/MAE.
5. Do not select entry/exit prices after seeing intrabar movement.
6. Do not train a new ML model on post-freeze outcomes unless a separately registered walk-forward experiment defines the training protocol before those outcomes are used.
7. Preserve the original frozen signal record.
8. Do not move an existing run's activation timestamp by restarting the collector.

## 9. Review checkpoints

The following are **review checkpoints, not success thresholds**:

- **20 completed trades:** operational/data-quality review;
- **50 completed trades:** first prospective statistical review;
- **100 completed trades:** stronger stability review;
- **approximately 3 months of prospective sessions:** time/regime review.

A checkpoint cannot be used to stop early because the result is good or bad. The purpose is to inspect data integrity and predefined diagnostics.

## 10. Primary prospective metrics

Track:

- completed signals and trades;
- gross mean/median return;
- net mean/median return;
- win rate;
- profit factor;
- cumulative return;
- drawdown;
- daily return series;
- daily Sharpe diagnostic;
- MFE/MAE;
- realized spread/slippage;
- total costs;
- turnover/trading frequency;
- execution exceptions;
- cost-adjusted expectancy.

Compare prospective distributions against the historical 001G/001H distributions without changing the frozen strategy to match them.

## 11. Promotion decision

001I may support progression toward controlled live validation only if:

- the signal engine operates reproducibly;
- prospective records are complete and point-in-time safe;
- realized execution costs are measured;
- net performance is economically plausible under observed friction;
- the result is not dependent on a small number of unrepresentative observations;
- no material operational or data-quality failure is found.

Possible outcomes:

- **🟢 Proceed to a separate controlled-live validation protocol**;
- **🟡 Extend paper/shadow validation** because evidence or execution information remains limited/mixed;
- **🔴 Reject/freeze Strategy 001** if prospective evidence materially contradicts the historical research or the economics are not viable.

These are research-gate states, not guarantees of future performance.

## 12. Relationship to 001H

001H established historical robustness across the examined January 2025–August 2026 sample and showed that the simple friction grid becomes negative between 4 and 6 bps round-trip.

However, the historical sample has already been examined, so its 2026 holdout is **OOS-style rather than pristine OOS**.

001I addresses the unresolved question:

```text
Does the frozen signal continue when future outcomes are unknown?
                ↓
What forward path is actually observed?
                ↓
What execution friction is actually observed?
                ↓
Does the signal remain economically plausible after that friction?
```

## 13. Capital control

The existence of approximately ₹30,000 in the brokerage account is not treated as evidence that the strategy should receive capital.

No live order is implied by 001I. Any later live experiment must have its own explicit capital limit, position sizing, risk limits, order controls, and operational rollback procedure.

## 14. Current status

**🟡 Protocol hardened — prospective paper/shadow data collection is the next gate.**

No Strategy 002 work begins before Strategy 001 receives a final decision.
