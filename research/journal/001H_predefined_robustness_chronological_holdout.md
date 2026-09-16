# Strategy 001H — Predefined Robustness & Chronological Holdout Validation

## Purpose

001H is the next validation gate after the successful 001G replay. Its purpose is to determine whether the frozen Strategy 001D gross edge is stable across time and under progressively less favorable execution assumptions.

This is a **validation experiment, not a strategy-improvement exercise**. No parameter will be selected because it performs best on the historical sample.

## Important OOS limitation

The complete January 2025–August 2026 GOLDBEES sample has already been examined during Strategy 001 research. Therefore a historical split within this dataset cannot honestly be described as a fully untouched out-of-sample test.

001H will use:

- **2025:** historical development/reference period;
- **2026:** chronological holdout / OOS-style period;
- future paper/shadow trading: the first genuinely prospective out-of-sample period.

The 2026 results must not be described as pristine OOS evidence in the final portfolio documentation.

## Frozen baseline

Unless a separate experiment explicitly states otherwise, 001H uses the exact 001D rules:

- GOLDBEES 5-minute OHLCV;
- previous 30 completed same-session closes;
- sample standard deviation;
- z-score ≥ +2.0;
- prior six-bar return > 0;
- long-only;
- signal at event-bar close;
- next-bar-open entry;
- close of `t+6` exit;
- fixed 12-bar session cooldown;
- no overnight feature construction;
- one position at a time;
- no leverage or optimized sizing.

## Validation questions

### H1 — Temporal stability

Does the frozen strategy remain positive across chronological periods rather than relying on one historical segment?

Report separately for:

- 2025 H1;
- 2025 H2;
- 2026 H1;
- available 2026 H2.

For each period report:

- trade count;
- mean and median gross return;
- win rate;
- profit factor;
- cumulative gross return;
- maximum drawdown;
- annualized time-series Sharpe only when the construction is appropriate for the period.

### H2 — Chronological holdout

Run the frozen strategy separately on:

- 2025 development/reference period;
- 2026 chronological holdout.

The holdout result is a stability check, not a claim of untouched OOS discovery.

### H3 — Execution-cost sensitivity

Re-run the frozen strategy under a predefined round-trip friction ladder, with no cost level selected after seeing results.

Minimum grid:

- 0 bps round trip;
- 2 bps;
- 4 bps;
- 6 bps;
- 8 bps;
- 10 bps;
- 14 bps.

The current 001E per-side grid remains the historical execution-sensitivity reference. 001H adds a simpler round-trip presentation so the economic break-even region is easy to interpret.

These are research scenarios, not claims about observed live GOLDBEES spread or actual Zerodha charges.

### H4 — Trade-frequency stability

Compare:

- trades per active day;
- signal spacing;
- holding duration;
- proportion of days with trades;

across chronological periods. A strategy that only works during unusually dense signal periods should be identified explicitly.

### H5 — Return-distribution stability

Compare the distribution of trade returns across chronological periods, including:

- median;
- interquartile range;
- P10/P90;
- largest winner and loser;
- winner concentration.

The objective is to distinguish a broad effect from a small number of tail observations.

### H6 — Optional parameter-stability diagnostic

Only after the temporal/cost gate is complete, a separate one-dimensional sensitivity experiment may test a **pre-registered** neighborhood around the frozen baseline. It must not be used to select a replacement parameter set on the same historical data.

If performed, the perturbations must be fixed before viewing results and evaluated one variable at a time rather than as a combinatorial optimization grid.

## Leakage and selection controls

001H must not:

- optimize parameters to improve the 2026 result;
- choose a time-of-day filter because it looked strongest in 001G;
- choose a stop or profit target from MFE/MAE;
- choose a cost assumption because it produces a desired conclusion;
- tune the strategy separately for 2026;
- use future-period observations to construct signal features;
- report the best historical slice as if it were representative of the whole strategy.

## Promotion gate

001H can advance only if the evidence is sufficient to justify a prospective paper/shadow test. It does **not** require every historical period to be profitable, but any instability must be documented and explained rather than averaged away.

The decision should consider:

1. whether the frozen edge persists chronologically;
2. how quickly realistic friction consumes the edge;
3. whether losses and winners remain distributed similarly across periods;
4. whether the signal remains sufficiently frequent to evaluate prospectively;
5. whether there is enough evidence to justify paper/shadow execution.

## Expected outputs

```text
research/journal/001H_predefined_robustness_chronological_holdout.md
research/journal/001H_predefined_robustness_chronological_holdout_results.md
src/research/strategy_001h_robustness.py
scripts/run_strategy_001h_robustness.py
scripts/plot_strategy_001h_results.py
tests/test_strategy_001h_robustness.py
```

Expected analytical outputs should include tables and charts for:

- chronological performance;
- development vs chronological holdout;
- cost sensitivity;
- trade-return distributions;
- trading activity;
- cumulative/equity and drawdown where meaningful.

## Decision states

Use one of:

- **🟢 Proceed to prospective paper/shadow validation** — evidence supports a controlled prospective test;
- **🟡 Continue research** — evidence is mixed or execution economics remain unresolved;
- **🔴 Reject/freeze** — the frozen hypothesis does not demonstrate sufficient stability or economic viability.

No Strategy 002 work begins before Strategy 001 receives a final decision.
