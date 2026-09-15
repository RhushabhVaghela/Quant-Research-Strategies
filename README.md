# Quant Research Strategies — Research Journal

This repository documents a **hypothesis-driven quantitative research journey** rather than a collection of pre-selected profitable strategies.

The main README is the interview-facing journal: what we thought, what we tested, what happened, what we learned, and what we did next.

---

## Research lifecycle

```text
Economic hypothesis
        ↓
Prediction target
        ↓
Data validation
        ↓
Simple baseline
        ↓
Statistical experiment
        ↓
Reject / inconclusive / promising
        ↓
Refinement / attribution
        ↓
Freeze hypothesis
        ↓
Point-in-time validation
        ↓
Formal trading backtest
        ↓
Costs + slippage + execution analysis
        ↓
Out-of-sample / walk-forward validation
        ↓
Paper / shadow validation
        ↓
Controlled live validation
```

Failures are part of the portfolio. We do not delete unsuccessful hypotheses or optimize until a backtest looks attractive.

---

# Current research status

| Stage | Status |
|---|---|
| Research design / execution constraints | ✅ Complete |
| Research-universe framework | ✅ Complete |
| Historical data validation | ✅ Complete |
| Strategy 001 — GOLDBEES mean reversion | 🔴 Rejected |
| Strategy 001A — event structure diagnostics | ✅ Complete — continuation lead identified |
| Strategy 001B — continuation attribution | 🟡 Promising research lead |
| Strategy 001C — point-in-time validation | 🟡 Promising — lead survived PIT benchmark |
| Strategy 001D — formal trading backtest | 🟡 Candidate — implementation complete, result pending |
| Robustness / OOS validation | ⏳ Not started |
| Paper / shadow validation | ⏳ Not started |
| Controlled live validation | ⛔ Not started |
| Strategy 002 | ⛔ Intentionally deferred |

**No strategy is approved for deployment.**

---

# Research Journal

## Strategy 001 — GOLDBEES Intraday Mean Reversion

### Original hypothesis

> When GOLDBEES closes unusually far from its recent intraday mean, the subsequent return should tend to have the opposite sign and move back toward the mean.

The first experiment used 5-minute bars, a 30-bar prior lookback, an absolute z-score threshold of 2.0, and same-session forward horizons of 1, 3, 6, and 12 bars.

The GOLDBEES dataset contained **30,912 five-minute bars** from January 2025 through August 2026. The baseline study produced **2,953 combined event observations**.

### Experiment 001 result

The symmetric mean-reversion hypothesis was **rejected**. Reversion-aligned mean returns were negative at every tested horizon:

| Horizon | Mean reversion-aligned return |
|---|---:|
| 5 min | -0.00365% |
| 15 min | -0.00901% |
| 30 min | -0.01703% |
| 60 min | -0.02105% |

Positive deviations instead showed positive average forward returns. This was continuation-like behavior, not mean reversion.

---

## Strategy 001A — Event Structure & Conditioning Diagnostics

001A tested whether the continuation-like behavior survived dependence controls and whether it was concentrated in predefined conditions.

### What we learned

1. Raw events were highly clustered.
2. Positive-deviation continuation survived fixed non-overlap filtering.
3. Prior six-bar trend was the clearest conditioning variable.
4. Negative deviations did not show a symmetric counterpart.
5. Volume and volatility did not provide a simple primary explanation.
6. Exploratory concentrations were not optimized.

**Decision: continuation became a promising exploratory lead.**

---

## Strategy 001B — Continuation Attribution

001B asked whether continuation after a large deviation contained information beyond ordinary intraday drift and the recent trend.

The strongest subgroup was **positive deviation + prior uptrend**. In the fixed non-overlapping event set, event returns exceeded matched non-event baselines at every tested horizon:

| Horizon | Event mean | Matched baseline | Incremental |
|---|---:|---:|---:|
| 5 min | +0.0156% | +0.0025% | **+0.0128%** |
| 15 min | +0.0202% | +0.0084% | **+0.0113%** |
| 30 min | +0.0443% | +0.0177% | **+0.0255%** |
| 60 min | +0.0532% | +0.0270% | **+0.0243%** |

**Decision: 🟡 Promising research lead.**

Detailed results: `research/journal/001B_continuation_attribution_results.md`.

---

## Strategy 001C — Point-in-Time Validation

001C froze the continuation hypothesis and required benchmark outcomes to have fully completed before the event timestamp.

The implementation produced **1,668 frozen events** and **401 selected non-overlapping events** under the fixed 12-bar cooldown.

For positive deviation + prior uptrend:

| Horizon | Event return | PIT baseline | Incremental return |
|---|---:|---:|---:|
| 5 min | +0.0148% | +0.0032% | **+0.0115%** |
| 15 min | +0.0205% | +0.0099% | **+0.0106%** |
| 30 min | +0.0443% | +0.0194% | **+0.0249%** |
| 60 min | +0.0527% | +0.0279% | **+0.0247%** |

The pre-specified 30-minute primary horizon therefore showed approximately **+2.49 basis points of incremental gross return** relative to the point-in-time matched benchmark.

This is encouraging but does not establish tradable alpha. Costs, slippage, drawdown, turnover, execution realism, and chronological OOS stability remain unresolved.

**Decision: 🟡 Promising — promote to formal Strategy 001D backtest.**

Detailed results: `research/journal/001C_continuation_hypothesis_results.md`.

---

## Strategy 001D — Formal Trading Backtest

001D turns the frozen research hypothesis into an executable baseline **without changing the signal rule**.

### Frozen implementation

- 5-minute bars;
- previous 30 completed same-session closes;
- sample standard deviation;
- z-score ≥ +2.0;
- prior six-bar return > 0;
- long-only;
- signal after event-bar close;
- entry at next-bar open;
- exit at close of `t+6`;
- fixed 12-bar cooldown;
- no overnight trades;
- one position at a time;
- constant-notional normalized accounting;
- no leverage or optimized sizing;
- no parameter optimization.

The engine separately reports gross performance and explicit cost/slippage sensitivity. OHLCV alone cannot reveal exact historical execution quality, so cost assumptions are reported as transparent scenarios rather than disguised as measured historical costs.

### Implementation

```text
research/journal/001D_formal_strategy_spec.md
src/research/continuation_backtest.py
tests/test_continuation_backtest.py
scripts/run_strategy_001_backtest.py
```

### Current decision

**🟡 CANDIDATE — implementation complete; historical backtest result pending.**

The first 001D run is an evidence gate, not a deployment decision.

---

# Why the project uses reference resources without blindly copying them

The repository contains the user's WorldQuant University material and code under `trading_resources/WQU_resources/`, alongside other strategy/reference material. These resources are used for learning, implementation patterns, candidate ideas, feature engineering, and later ML/model development.

A resource implementation is not automatically a validated strategy. When we use one, we still establish its hypothesis, define its data/execution assumptions, test for leakage, and validate it under this project's research gates.

This keeps the portfolio from becoming a collection of copied backtests while still taking advantage of the substantial material already available.

---

# Strategy 001 promotion path

Strategy 001 remains the **only active strategy** until it reaches a clear promotion or rejection decision.

```text
001C point-in-time validation              🟡 promising
        ↓
001D formal baseline backtest              ← CURRENT
        ↓
Gross + cost/slippage analysis
        ↓
Predefined robustness tests
        ↓
Chronological OOS / walk-forward
        ↓
Paper / shadow validation
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

# Project structure

```text
Quant-Research-Strategies/
├── README.md                         # Interview-facing research journal
├── research/
│   ├── journal/                      # Chronological research decisions
│   ├── phase_*.md                    # Research specifications
│   └── universe_candidates.csv       # Predefined research universe
├── src/
│   ├── data/                         # Data and broker integration
│   └── research/                     # Research and backtesting utilities
├── scripts/                          # Reproducible experiments
├── tests/                            # Automated checks
├── data/
│   ├── raw/                          # Local historical datasets
│   └── reports/                      # Generated experiment outputs
└── trading_resources/
    ├── WQU_resources/                # WorldQuant University learning material
    └── Concepts/                     # Reference strategy/concept material
```

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

Run tests:

```powershell
pytest
```

Run the 001D Strategy 001 baseline backtest:

```powershell
python scripts/run_strategy_001_backtest.py data/raw/NSE_GOLDBEES_5minute.csv
```

Run the 001C point-in-time audit:

```powershell
python scripts/run_point_in_time_baseline.py data/raw/NSE_GOLDBEES_5minute.csv
```

Credentials and access tokens must remain local and must never be committed.

---

# Roadmap

```text
Research design / execution constraints             ✅
Historical data validation                           ✅
Strategy 001 mean reversion                          🔴 rejected
001A event diagnostics                                ✅
001B continuation attribution                         🟡 promising
001C point-in-time validation                         🟡 promising
001D formal trading backtest                          🟡 CURRENT
Robustness + costs + slippage                         ⏳
Chronological OOS / walk-forward                      ⏳
Paper / shadow validation                             ⏳
Controlled live validation                            ⏳
Strategy 001 final decision                           ⏳
Strategy 002                                           ⛔ deferred until 001 complete
```

**The project is intentionally incomplete. The research journey is the deliverable.**
