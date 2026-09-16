# Strategy 001I — Prospective OOS & Paper/Shadow Validation Protocol

## Purpose

001I is the first genuinely prospective out-of-sample gate for Strategy 001. Unlike the historical 2025/2026 analysis, observations collected after the freeze date must not be used to alter the signal definition, threshold, holding period, filters, or execution logic before their outcomes are observed.

## OOS boundary

**Prospective OOS start:** 2026-09-16 market session, or the first complete market session after this protocol is committed and the logging system is operational.

The existing GOLDBEES dataset through August 2026 remains historical research data. Any September 2026 data already downloaded and inspected before the OOS start is not considered prospective OOS evidence.

The historical 2026 sample in 001H remains an **OOS-style chronological holdout**, not pristine OOS.

## Frozen strategy

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

**No changes are permitted during the prospective observation window.**

## What is logged before the outcome is known

For every signal, record:

- strategy/version identifier;
- signal timestamp;
- session date and time-of-day bucket;
- signal close;
- prior 30-bar mean and sample standard deviation;
- z-score;
- prior six-bar return;
- volume and prior-volume baseline/ratio when defined point-in-time;
- intended next-bar-open entry;
- intended `t+6` exit;
- signal acceptance/rejection;
- reason for rejection if operationally relevant;
- timestamp of the log event.

The pre-outcome record must be append-only. Do not overwrite a signal after seeing its future return.

## What is recorded after the outcome

After the fixed exit is complete, append:

- realized entry and exit prices;
- gross return;
- timestamped execution/paper prices;
- spread/bid-ask observations if available;
- estimated slippage;
- brokerage/fees/taxes where applicable;
- net return under the documented execution model;
- MFE/MAE as a diagnostic only;
- operational exceptions.

## Paper/shadow rules

The first phase is **paper/shadow**, not live capital.

The signal engine should generate the same intended orders that the frozen strategy would generate, but no capital is required for the research decision. If Zerodha/API execution is later tested, actual orders must remain separately identified from paper observations.

Do not use hindsight to change a paper trade's entry or exit.

## Evaluation windows

Do not declare success from a handful of trades. Review the prospective sample only at predeclared checkpoints, for example:

- 20 completed trades — operational/data-quality review only;
- 50 completed trades — first statistical review;
- 100 completed trades — stronger stability review;
- approximately 3 months of prospective sessions — time/regime review.

These are review checkpoints, not success thresholds.

## Primary prospective metrics

Track:

- completed trades;
- gross mean/median return;
- net mean/median return;
- win rate;
- profit factor;
- cumulative return;
- drawdown;
- daily return series;
- daily Sharpe diagnostic;
- realized spread/slippage;
- turnover/trading frequency;
- execution exceptions;
- cost-adjusted expectancy.

## Critical economic test

The historical 001H grid shows that the gross mean trade return is only a few basis points. Therefore prospective execution measurement is central.

The goal is not to demonstrate that the backtest can survive an arbitrarily chosen cost assumption. The goal is to measure the actual friction experienced by the intended execution workflow and compare it with the frozen gross edge.

## No-lookahead rules

During the prospective window:

1. Do not download future bars into the research dataset and inspect them before signal generation.
2. Do not retune z-score, lookback, holding period, cooldown, time-of-day, or volume filters.
3. Do not remove losing trades manually.
4. Do not add a stop/target because of observed MFE/MAE.
5. Do not select an execution time after seeing intrabar movement.
6. Do not train ML models using post-freeze outcome data unless a separately registered experiment explicitly defines a walk-forward training protocol.
7. Preserve the original frozen signal record.

## Promotion decision

001I may support progression toward controlled live validation only if:

- the signal engine operates reproducibly;
- prospective records are complete and point-in-time safe;
- realized execution costs are measured;
- net performance is economically meaningful under observed friction;
- the result is not dependent on a small number of unrepresentative observations;
- no material operational or data-quality failure is found.

Otherwise the strategy remains in research or is frozen/rejected. A weak prospective result is a valid research outcome.

## Relationship to 001H

```text
Historical research through Aug 2026
        ↓
001H chronological robustness
        ↓
Historical evidence: encouraging but not pristine OOS
        ↓
001I prospective OOS starts after freeze
        ↓
Paper/shadow observation
        ↓
Execution-cost validation
        ↓
Controlled live validation (only if justified)
```

This separation is intentional: **the historical data answer whether the frozen hypothesis has shown persistence; prospective data answer whether the frozen process continues to work without hindsight.**
