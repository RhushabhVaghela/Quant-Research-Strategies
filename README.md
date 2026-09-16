# Quant Research Strategies

This repository is a research journal and implementation workspace for developing, testing, and validating systematic trading strategies in Python.

The goal is not to collect a large number of backtests. The goal is to demonstrate a reproducible research process: hypothesis → data audit → signal discovery → point-in-time validation → frozen strategy → trade-level backtest → execution/cost audit → robustness → chronological validation → prospective paper/shadow test → controlled live validation.

Negative and inconclusive results are preserved as part of the research record.

---

## Strategy 001 — GOLDBEES intraday continuation

Strategy 001 began as a mean-reversion hypothesis and was rejected. The research then investigated the observed continuation structure and produced a frozen long-only continuation strategy for GOLDBEES 5-minute data.

### Research status

| Stage | Status | Key result |
|---|---|---|
| 001 mean reversion | 🔴 Rejected | Large positive deviations did not reliably revert |
| 001A diagnostics | 🟢 Complete | Positive continuation and prior-trend conditioning identified |
| 001B attribution | 🟡 Promising | Continuation exceeded descriptive matched non-event baselines |
| 001C PIT baseline | 🟡 Promising | 30-min positive/up incremental result ≈ +2.49 bps |
| 001D frozen backtest | 🟡 Candidate | +4.77 bps mean gross trade, 310 trades; costs unresolved |
| 001E execution audit | 🟡 Complete | Small gross edge is highly friction-sensitive |
| 001F decomposition | 🟡 Complete | Edge not solely dependent on top tail winners |
| 001G replay | 🟡 Complete | 310/310 trades reconciled; forward path and MFE/MAE recovered |
| **001H robustness/chronological holdout** | **← CURRENT** | Predefined validation gate |

### Frozen 001D strategy

- 5-minute GOLDBEES OHLCV;
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
- no leverage or optimized sizing;
- no parameter optimization in the baseline.

### 001G result

The frozen strategy was reconstructed directly from validated GOLDBEES OHLCV and reconciled against the 001D gross trade export:

- 310 replayed trades;
- 310 reference trades;
- 310 exact reconciliations within tolerance;
- 0 discrepancies.

The forward path was positive before the frozen exit: mean forward return was +1.36 bps at 5 minutes, +2.44 bps at 10 minutes, +3.40 bps at 20 minutes, +4.51 bps at 25 minutes, and +4.77 bps at 30 minutes. Median return at 30 minutes was +2.41 bps.

MFE averaged +15.35 bps with a +9.48 bps median; MAE averaged -9.63 bps with a -6.88 bps median. These are OHLC-range diagnostics and do not imply that intrabar highs/lows were executable.

The 001G feature slices are descriptive only. Later-session buckets were stronger in this sample, while z-score, prior six-bar return, and volume-ratio relationships did not show a clean monotonic pattern. No new filter has been selected from these observations.

Detailed journal: `research/journal/001G_point_in_time_feature_replay_results.md`.

### Important OOS qualification

The full January 2025–August 2026 historical sample has already been examined during Strategy 001 research. Therefore a split inside that sample cannot honestly be presented as pristine untouched OOS evidence. 001H will use 2025 as a development/reference period and 2026 as a chronological holdout/OOS-style check. Future paper/shadow trading will provide genuinely prospective out-of-sample evidence.

---

# Strategy 001 promotion path

```text
001C point-in-time validation              🟡 promising
        ↓
001D formal baseline backtest              🟡 gross positive / costs unresolved
        ↓
001E distribution + execution audit        🟡 complete
        ↓
001F trade decomposition                   🟡 complete
        ↓
001G PIT feature + forward-path replay     🟡 complete
        ↓
001H predefined robustness + chronological holdout   ← CURRENT
        ↓
Prospective paper / shadow validation
        ↓
Execution validation
        ↓
Controlled live validation
        ↓
Strategy 001 final decision
        ↓
Only then: Strategy 002
```

A failure at any gate is recorded rather than repaired by post-hoc parameter tuning.

---

# Why the project uses reference resources without blindly copying them

The repository contains WorldQuant University material under `trading_resources/WQU_resources/`, alongside Quantra and other strategy/reference material. These resources are used for learning, implementation patterns, candidate ideas, feature engineering, and later ML/model development.

A resource implementation is not automatically a validated strategy. When we use one, we still establish its hypothesis, define its data/execution assumptions, test for leakage, and validate it under this project's research gates.

---

# Research standards

1. Start with an economic hypothesis, not a model.
2. Define the prediction target before choosing a model.
3. Use point-in-time information for prospective strategy construction.
4. Keep event definitions and forward outcomes strictly separated.
5. Establish a simple baseline before ML.
6. Record negative and inconclusive results.
7. Avoid parameter optimization before establishing evidence.
8. Test across time and market regimes.
9. Include transaction costs and slippage before judging economic value.
10. Treat backtests as evidence, not guarantees.
11. Require chronological out-of-sample evidence before paper validation.
12. Never deploy simply because a backtest looks attractive.

---

# Reproducibility

Install dependencies:

```powershell
python -m venv .venv
.venv\\Scripts\\Activate.ps1
pip install -r requirements.txt
```

Run the complete test suite:

```powershell
pytest
```

Run the Strategy 001G replay:

```powershell
python scripts/run_strategy_001g_replay.py data/raw/NSE_GOLDBEES_5minute.csv
python scripts/plot_strategy_001g_results.py data/reports/goldbees_strategy_001g_replay
```

The local 001G run should reconcile the frozen 001D trades before any numerical interpretation is accepted.
