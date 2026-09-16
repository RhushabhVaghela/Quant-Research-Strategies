# Strategy 001H — Predefined Robustness & Chronological Holdout Validation — Results

## Status

**🟡 Implementation complete; local empirical run pending.**

001H is a validation experiment on the frozen 001D strategy. It does not optimize parameters, select filters, or reinterpret the 2026 period as pristine untouched out-of-sample evidence.

The implementation reuses the frozen 001D signal/execution logic and evaluates four fixed chronological periods, a fixed 2025-vs-2026 sample designation, and a pre-registered round-trip friction ladder.

## 1. Execution controls

Frozen 001D rules remain unchanged:

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

The cost ladder is expressed as **round-trip friction** of 0, 2, 4, 6, 8, 10, and 14 bps. These are research scenarios, not observed live spread, impact, brokerage, or tax measurements.

## 2. Historical/OOS qualification

The complete January 2025–August 2026 sample has already been examined during Strategy 001 research. Therefore:

- 2025 is labeled **development/reference**;
- 2026 is labeled **chronological holdout / OOS-style**;
- neither period is described as pristine untouched OOS discovery;
- future paper/shadow execution will be the first genuinely prospective OOS period.

## 3. Chronological performance

Populate from `chronological_performance.csv` after the local run.

| Period | Trades | Mean | Median | Win rate | PF | Cumulative | MDD | Daily Sharpe |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 2025 H1 | pending | pending | pending | pending | pending | pending | pending | pending |
| 2025 H2 | pending | pending | pending | pending | pending | pending | pending | pending |
| 2026 H1 | pending | pending | pending | pending | pending | pending | pending | pending |
| 2026 H2 | pending | pending | pending | pending | pending | pending | pending | pending |

## 4. Development vs chronological holdout

Populate from `development_vs_holdout.csv`.

| Sample designation | Trades | Mean | Median | Win rate | PF | Cumulative | MDD | Daily Sharpe |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 2025 development/reference | pending | pending | pending | pending | pending | pending | pending | pending |
| 2026 chronological holdout | pending | pending | pending | pending | pending | pending | pending | pending |

The holdout is a chronological stability check. It must not be described as a clean OOS discovery sample because the period has already been examined during research.

## 5. Cost sensitivity

Populate from `cost_sensitivity.csv`.

| Round-trip friction | Mean net | Median net | Win rate | PF | Cumulative net | MDD | Daily Sharpe |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 0 bps | pending | pending | pending | pending | pending | pending | pending |
| 2 bps | pending | pending | pending | pending | pending | pending | pending |
| 4 bps | pending | pending | pending | pending | pending | pending | pending |
| 6 bps | pending | pending | pending | pending | pending | pending | pending |
| 8 bps | pending | pending | pending | pending | pending | pending | pending |
| 10 bps | pending | pending | pending | pending | pending | pending | pending |
| 14 bps | pending | pending | pending | pending | pending | pending | pending |

The break-even region will be interpreted as an economic sensitivity range, not as a claim about actual executable friction.

## 6. Trading activity

Populate from `trading_activity.csv`.

The fixed questions are:

- Is signal frequency reasonably stable across periods?
- Do trades per active day change materially?
- Does signal spacing change materially?
- Does the fixed holding duration remain 25 minutes from next-open entry to `t+6` close?

No period is selected because it has the highest frequency or return.

## 7. Distribution stability

001H reports P10/P25/P50/P75/P90, largest winner/loser, and top-10%-winner profit share by period. This is intended to distinguish a broad effect from a small number of tail observations.

No parameter or filter will be changed from these distributions.

## 8. Charts

The plotting script writes:

```text
chronological_performance.png
development_vs_holdout.png
cost_sensitivity.png
trade_return_distributions.png
trading_activity.png
daily_equity.png
daily_drawdown.png
```

These charts are descriptive diagnostics and should be read alongside the numerical CSV outputs.

## 9. What 001H can establish

After the local run, the decision will be based on:

1. chronological persistence of the frozen gross edge;
2. distribution stability rather than cumulative return alone;
3. signal-frequency stability;
4. the predefined friction ladder;
5. whether the evidence is sufficient to justify prospective paper/shadow testing.

## 10. What 001H cannot establish

001H cannot establish:

- live bid/ask spread or market impact;
- actual Zerodha execution quality;
- pristine historical OOS discovery;
- superiority of any new parameter set;
- that MFE/MAE can be captured in live trading;
- that the strategy is ready for live capital.

## 11. Decision

**Pending local empirical run.**

Decision states remain:

- **🟢 Proceed to prospective paper/shadow validation** — evidence supports a controlled prospective test;
- **🟡 Continue research** — evidence is mixed or execution economics remain unresolved;
- **🔴 Reject/freeze** — the frozen hypothesis does not demonstrate sufficient stability or economic viability.

No Strategy 002 work begins before Strategy 001 receives a final decision.
