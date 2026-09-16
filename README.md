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
| **001H robustness/chronological holdout** | **🟡 Complete** | Positive gross performance across all examined periods; costs remain unresolved |
| **001I prospective OOS / paper-shadow** | **← CURRENT** | Capture ledger and live paper-shadow collector registered; no live orders |

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

### 001H result

001H kept the 001D strategy frozen and tested four chronological periods, a 2025 development/reference vs 2026 historical holdout designation, trading-frequency stability, return-distribution stability, and a predefined round-trip friction ladder.

The frozen gross edge remained positive in all four examined periods:

| Period | Trades | Mean gross | Median gross | Win rate | PF | Cumulative gross |
|---|---:|---:|---:|---:|---:|---:|
| 2025 H1 | 100 | +3.32 bps | +1.25 bps | 51.00% | 1.947 | +3.36% |
| 2025 H2 | 97 | +5.79 bps | +3.30 bps | 64.95% | 2.971 | +5.76% |
| 2026 H1 | 76 | +6.63 bps | +2.03 bps | 52.63% | 2.260 | +5.13% |
| 2026 H2* | 37 | +2.19 bps | +0.79 bps | 51.35% | 1.627 | +0.81% |

\* Available portion of 2026 H2 in the historical dataset.

The 2025 development/reference sample had +4.53 bps mean gross return and 2.406 PF. The 2026 chronological holdout had +5.18 bps mean gross return and 2.105 PF. This supports historical temporal persistence but is **not pristine OOS evidence**, because the full January 2025–August 2026 sample has already been examined.

The cost grid remains the main unresolved economic issue. At 4 bps round-trip friction, mean net return was +0.77 bps and cumulative net return +2.34%. At 6 bps, mean net return was -1.23 bps and cumulative net return -3.81%. At 14 bps, mean net return was -9.23 bps and cumulative net return -24.95%. These are scenario assumptions, not observed live costs.

Detailed results: `research/journal/001H_predefined_robustness_chronological_holdout_results.md`.

### 001I prospective OOS / paper-shadow

Because the historical sample has already been examined through August 2026, the repository does **not** relabel August 2026 or previously inspected September observations as pristine OOS. The first genuine prospective OOS observations are captured only after the 001I activation boundary, before their future outcomes are known.

001I keeps the 001D rules unchanged and records point-in-time signal information first. After the frozen exit candle has completed, paper outcome and execution-observation information are appended. The first phase is paper/shadow, not live capital.

The implementation now includes:

- `src/research/strategy_001i_prospective.py` — append-only prospective ledger and frozen-rule outcome finalization;
- `scripts/run_strategy_001i_paper_shadow.py` — live GOLDBEES tick capture, 5-minute bar construction, signal capture, and paper outcome finalization; **no order placement**;
- `tests/test_strategy_001i_prospective.py` — prospective ledger/no-look-ahead unit tests;
- `data/prospective/README.md` — local data handling rules.

The collector uses the existing Zerodha authentication layer and KiteTicker full-mode market data. It must be started before the session and left running; no historical backfill is allowed to create prospective observations after the fact.

The central unresolved questions are:

1. Does the frozen signal continue prospectively?
2. Does its forward-path distribution remain compatible with the historical evidence?
3. What spread/slippage/costs are actually observed?
4. Does the gross edge remain economically plausible after those observed frictions?

Review checkpoints at 20, 50, and 100 completed trades, plus an approximately three-month time/regime review, are data-quality/research checkpoints rather than success thresholds.

Protocol: `research/journal/001I_prospective_oos_paper_shadow_protocol.md`.
Results journal: `research/journal/001I_prospective_oos_paper_shadow_results.md`.

---

# Strategy 001 promotion path

```text
001C point-in-time validation                       🟡 promising
        ↓
001D formal baseline backtest                       🟡 gross positive / costs unresolved
        ↓
001E distribution + execution audit                 🟡 complete
        ↓
001F trade decomposition                            🟡 complete
        ↓
001G PIT feature + forward-path replay              🟡 complete
        ↓
001H predefined robustness + historical holdout     🟡 complete
        ↓
001I prospective OOS / paper-shadow                 ← CURRENT
        ↓
Execution-cost validation
        ↓
Separate controlled-live validation protocol
        ↓
Strategy 001 final decision
        ↓
Only then: Strategy 002
```

A failure at any gate is recorded rather than repaired by post-hoc parameter tuning.

**No strategy is approved for live deployment.**

---

# Why the project uses reference resources without blindly copying them

The repository contains WorldQuant University learning material under `trading_resources/WQU_resources/`, alongside Quantra and other strategy/reference material. These resources are used for learning, implementation patterns, candidate ideas, feature engineering, and later ML/model development.

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
11. Require genuine prospective evidence before controlled live validation.
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

Run the Strategy 001H robustness gate:

```powershell
python scripts/run_strategy_001h_robustness.py data/raw/NSE_GOLDBEES_5minute.csv
python scripts/plot_strategy_001h_results.py data/reports/goldbees_strategy_001h_robustness
```

Start the Strategy 001I prospective paper/shadow collector before a market session:

```powershell
python scripts/run_strategy_001i_paper_shadow.py
```

The collector requires valid Zerodha credentials in the local environment, uses the existing authentication layer, and **does not place orders**. It writes prospective observations to `data/prospective/strategy_001i/`, which is ignored by Git except for the directory README.

The local 001G run must reconcile the frozen 001D trades before its numerical interpretation is accepted. The 001H numerical result must be recorded only after the local empirical run is completed. The 001I results journal must only be populated from genuinely prospective records.
