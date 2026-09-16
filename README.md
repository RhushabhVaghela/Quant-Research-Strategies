# Quant Research Strategies — Research Journal

This repository documents a **hypothesis-driven quantitative research journey** rather than a collection of pre-selected profitable strategies.

The main README is the interview-facing journal: what we thought, what we tested, what happened, what we learned, and what we did next.

---

## Current research status

| Stage | Status |
|---|---|
| Research design / execution constraints | ✅ Complete |
| Research-universe framework | ✅ Complete |
| Historical data validation | ✅ Complete |
| Strategy 001 — GOLDBEES mean reversion | 🔴 Rejected |
| Strategy 001A — event structure diagnostics | ✅ Complete — continuation lead identified |
| Strategy 001B — continuation attribution | 🟡 Promising research lead |
| Strategy 001C — point-in-time validation | 🟡 Promising — lead survived PIT benchmark |
| Strategy 001D — formal trading backtest | 🟡 Gross positive / cost sensitivity unresolved |
| Strategy 001E — trade distribution & execution audit | 🟡 Complete — execution economics unresolved |
| Strategy 001F — trade-level decomposition | 🟡 Promising diagnostic — not paper/live ready |
| Strategy 001G — PIT feature & forward-path replay | 🟡 Implementation complete — empirical run pending |
| Robustness / OOS validation | ⏳ Not started |
| Paper / shadow validation | ⏳ Not started |
| Controlled live validation | ⛔ Not started |
| Strategy 002 | ⛔ Intentionally deferred |

**No strategy is approved for deployment.**

---

# Research Journal

## Strategy 001 — GOLDBEES Intraday Mean Reversion

### Original hypothesis

When GOLDBEES closes unusually far from its recent intraday mean, the subsequent return should tend to have the opposite sign and move back toward the mean.

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

001A showed that positive-deviation continuation survived fixed non-overlap filtering, with prior six-bar trend the clearest conditioning variable. Negative deviations did not show a symmetric counterpart. No parameters were optimized.

**Decision: continuation became a promising exploratory lead.**

---

## Strategy 001B — Continuation Attribution

The strongest subgroup was **positive deviation + prior uptrend**. Event returns exceeded matched non-event baselines at the tested horizons.

| Horizon | Event mean | Matched baseline | Incremental |
|---|---:|---:|---:|
| 5 min | +0.0156% | +0.0025% | **+0.0128%** |
| 15 min | +0.0202% | +0.0084% | **+0.0113%** |
| 30 min | +0.0443% | +0.0177% | **+0.0255%** |
| 60 min | +0.0532% | +0.0270% | **+0.0243%** |

**Decision: 🟡 Promising research lead.**

---

## Strategy 001C — Point-in-Time Validation

001C froze the continuation hypothesis and required benchmark outcomes to have fully completed before the event timestamp. It produced **1,668 frozen events** and **401 selected non-overlapping events** under the fixed 12-bar cooldown.

At the pre-specified 30-minute primary horizon, positive deviation + prior uptrend had +0.0443% event return versus +0.0194% PIT baseline, or approximately **+2.49 bps incremental gross return**.

**Decision: 🟡 Promising — promote to formal Strategy 001D backtest.**

---

## Strategy 001D — Formal Trading Backtest

001D turns the frozen research hypothesis into an executable baseline without changing the signal rule.

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

The completed baseline contains **310 trades**. Gross performance was **+15.85% cumulative**, with a **+4.77 bps mean trade return**, **55.81% win rate**, and **2.269 profit factor**. The predefined cost grid showed that modest friction can eliminate the gross edge, so this is not paper/live ready.

---

## Strategy 001E — Trade Distribution & Execution Audit

001E found a **+2.41 bps median** and **+4.77 bps mean** gross trade return. The top 10% of winners contributed about **53.7%** of positive profit. Gross performance remained positive in each chronological period examined, with about **1.30 trades per active day** and **25 minutes median holding duration**. The predefined friction grid rapidly consumed the small per-trade edge.

**Decision: 🟡 Complete — gross edge remains interesting, execution economics unresolved.**

---

## Strategy 001F — Trade-Level Edge & Execution Decomposition

After removing the top 10% of winning trades, the remaining 292 trades still had a **+1.41 bps mean**, **+1.32 bps median**, **53.08% win rate**, and **1.354 profit factor**. Tail winners remain important, but the gross result is not solely produced by a few extremes. Later-session buckets were descriptively stronger, while z-score buckets showed no clean monotonic relationship. These are not selected filters.

The compact 001D trade export lacked the complete signal-time feature set and intermediate forward prices, motivating 001G.

**Decision: 🟡 Promising diagnostic — not paper/live ready.**

---

## Strategy 001G — Point-in-Time Feature & Forward-Path Replay

001G reconstructs the frozen 001D trades directly from validated GOLDBEES OHLCV. It retains signal-time features without look-ahead, reconciles reconstructed trades against the 001D export, and measures forward returns plus MFE/MAE.

The implementation deliberately reuses the frozen 001D signal/execution logic rather than introducing a new rule.

### Delivered implementation

```text
src/research/strategy_001g_replay.py
scripts/run_strategy_001g_replay.py
scripts/plot_strategy_001g_results.py
tests/test_strategy_001g_replay.py
research/journal/001G_point_in_time_feature_replay.md
research/journal/001G_point_in_time_feature_replay_results.md
```

### Horizon convention

The signal occurs at the close of bar `t`, entry occurs at the open of `t+1`, and the frozen exit is the close of `t+6`. Therefore the frozen **30-minute signal horizon corresponds to approximately 25 minutes of entry-to-exit elapsed time** on regular 5-minute bars. 001G records this distinction explicitly.

### Current decision

**🟡 Implementation complete — empirical run pending.**

Run locally:

```powershell
python scripts/run_strategy_001g_replay.py data/raw/NSE_GOLDBEES_5minute.csv
python scripts/plot_strategy_001g_results.py data/reports/goldbees_strategy_001g_replay
```

The runner writes replayed trades, forward paths, a forward-path summary, MFE/MAE, and a reconciliation report. The plotting script creates forward-path and MFE/MAE charts.

No 001G numerical result is treated as evidence until the run has been executed and reconciliation reviewed.

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
001G PIT feature + forward-path replay     ← CURRENT
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

Run tests:

```powershell
pytest
```

Run the 001D baseline:

```powershell
python scripts/run_strategy_001_backtest.py data/raw/NSE_GOLDBEES_5minute.csv
```

Run the 001C point-in-time audit:

```powershell
python scripts/run_point_in_time_baseline.py data/raw/NSE_GOLDBEES_5minute.csv
```

Run the 001G replay:

```powershell
python scripts/run_strategy_001g_replay.py data/raw/NSE_GOLDBEES_5minute.csv
python scripts/plot_strategy_001g_results.py data/reports/goldbees_strategy_001g_replay
```

Credentials and access tokens must remain local and must never be committed.

**The project is intentionally incomplete. The research journey is the deliverable.**
