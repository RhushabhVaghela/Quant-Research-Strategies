# Quant Research Strategies

A modular Python repository for **research-grade quantitative trading**: historical market-data ingestion, data-quality auditing, hypothesis-driven intraday event studies, strategy development, backtesting, and controlled Zerodha Kite Connect integration.

The project is intentionally built as a research process rather than a collection of indicator-based trading scripts. The objective is to identify repeatable intraday behavior, test it without look-ahead bias, and only then consider strategy construction and machine-learning filters.

---

## 📌 Research Principles

- Start with a **financial hypothesis**, not a machine-learning model.
- Treat reference/Quantra strategies as educational building blocks, not assumed profitable systems.
- Prefer intraday research with realistic execution constraints.
- Separate **regulatory design → data validation → event study → baseline → ML → backtest → walk-forward validation → paper/live validation**.
- Prevent look-ahead bias, leakage, survivorship bias, and unnecessary data snooping.
- Include realistic transaction costs and slippage before judging a strategy.
- Never infer future performance from a small in-sample result.
- Respect the realities of a **₹30,000 total-account-capital constraint**.
- Prefer a small number of well-tested strategies over a large collection of weak ones.

Current research question:

> **Can we identify repeatable intraday conditions under which a directional price move is more likely to continue or reverse, and use statistical/ML methods to selectively trade only the conditions that demonstrate robust out-of-sample evidence?**

---

## ⚠️ Current Project Status

**We are deliberately not live trading yet.**

NIFTYBEES was used first because it successfully exercised the historical-data pipeline. It is **not** automatically the final strategy instrument.

Before we build an ML model or deploy capital, the project now inserts a Phase 0 specification covering:

- Indian retail algorithmic-trading/API constraints;
- Zerodha execution requirements;
- ₹30,000 capital feasibility;
- transaction-cost and slippage assumptions;
- reproducible research-universe selection.

See:

- `research/phase_00_india_retail_trading_spec.md`
- `research/phase_00_capital_and_execution_spec.md`
- `research/phase_00_research_universe_spec.md`

These documents are project controls, not legal/tax/investment advice. Current rules must be re-verified before live deployment.

---

## 📌 Regulatory / Execution Baseline

SEBI issued its February 4, 2025 circular on safer participation of retail investors in algorithmic trading, followed by implementation-timeline extensions and exchange implementation standards. NSE's current retail-algo material treats client API orders as algo orders and provides a framework for client-generated algorithms below the applicable order-rate threshold.

Current Zerodha documentation states that API-based order placement requires a whitelisted static IP and that its API order rate is capped at 10 orders/second per client account. These requirements are treated as part of the execution design rather than added after the strategy is finished.

Primary references:

- SEBI: https://www.sebi.gov.in/legal/circulars/feb-2025/safer-participation-of-retail-investors-in-algorithmic-trading_91614.html
- NSE: https://www.nseindia.com/static/trade/platform-services-non-neat-decision-support-tools-algorithm-trading
- Zerodha Kite Connect: https://zerodha.com/products/api
- Zerodha Kite Connect FAQ: https://support.zerodha.com/category/trading-and-markets/general-kite/kite-api/articles/kite-connect-api-faqs

---

## 📌 Features

- **Automated Zerodha OAuth Authentication**: Zero-touch authentication flow with local HTTP redirect listener (`http://127.0.0.1:8000/callback`). Automatically exchanges request tokens and updates `.env` directly without manual file copying.
- **Historical Data Layer**: Fetch, clean, and chunk historical market data (5-minute, daily, etc.) for NSE/BSE instruments from Zerodha.
- **Data Validation & Quality Checks**: Enforces strict OHLCV validation rules including price bounds, non-negative volume, duplicate timestamps, and monotonic ordering.
- **Intraday Dataset Audit**: Verifies session structure, expected bar spacing, bar counts, zero-volume rows, and basic within-session return distributions.
- **Leakage-Safe Event Study**: Measures forward returns after explicitly defined intraday events without using future observations to define the event.
- **Universe-Level Audit**: Compares multiple saved 5-minute datasets using the same structural quality rules without selecting instruments by historical strategy performance.
- **Capital/Execution Research Controls**: Documents the small-account feasibility, regulatory/API constraints, live-trading safety gates, and research-universe rules before deployment.
- **Extensible Architecture**: Clean separation between data ingestion, authentication, validation, auditing, research, and future strategy modules.

---

## 📁 Project Structure

```text
Quant-Research-Strategies/
├── src/
│   ├── data/
│   │   ├── __init__.py
│   │   ├── audit.py            # Intraday dataset structure/distribution audit
│   │   ├── kite_auth.py        # Automated OAuth & session manager
│   │   ├── kite_client.py      # Authenticated KiteConnect client wrapper
│   │   ├── historical.py       # Historical candle chunking & fetch logic
│   │   ├── instruments.py      # Instrument master downloader & resolver
│   │   └── validation.py       # Data validation rules & quality reports
│   └── research/
│       ├── __init__.py
│       ├── event_study.py      # Forward-return event-study framework
│       └── universe.py         # Comparable multi-instrument audit utilities
├── scripts/
│   ├── authenticate_kite.py    # Standalone session verification & token refresh
│   ├── audit_historical.py     # CLI for historical OHLCV dataset audit
│   ├── audit_universe.py       # CLI for multi-instrument universe audit
│   ├── download_historical.py  # CLI to download historical candle data
│   └── run_event_study.py      # CLI for exploratory intraday event study
├── tests/
│   ├── test_auth.py            # Authentication/environment tests
│   ├── test_validation.py      # OHLCV validation tests
│   ├── test_audit.py           # Intraday dataset audit tests
│   ├── test_event_study.py     # Event-study leakage/behavior tests
│   └── test_universe.py        # Universe selection safeguards
├── research/                   # Research notes, hypotheses & methodology
├── trading_resources/          # Reference materials, notebooks & strategy guides
├── .env.example                # Template for environment configuration
├── pytest.ini                  # Pytest configuration
├── requirements.txt             # Python dependencies
└── README.md                   # Project documentation
```

---

## ⚡ Quick Start

### 1. Prerequisites & Environment Setup

Clone the repository and install dependencies inside a virtual environment:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### 2. Configure Credentials

Copy `.env.example` to `.env` and configure your Zerodha API credentials:

```powershell
copy .env.example .env
```

Edit `.env`:

```env
KITE_API_KEY=your_zerodha_api_key
KITE_API_SECRET=your_zerodha_api_secret
KITE_ACCESS_TOKEN=
```

> ⚠️ **Security Note**: Never commit `.env` or broker access tokens to version control. They must remain local/secrets-only.

---

## 🔑 Automated Zerodha Authentication

Zerodha Kite Connect access tokens expire daily. The repository provides a zero-touch automated authentication process.

### How It Works

1. `ZerodhaAuthenticator` checks whether the current `KITE_ACCESS_TOKEN` is active (`kite.profile()`).
2. If the token is missing or expired, a local HTTP callback server (`http://127.0.0.1:8000/callback`) starts and opens the broker login page.
3. After login, the callback listener captures the `request_token`, exchanges it for a fresh `access_token`, and updates `.env`.

### Manual Session Refresh

```powershell
python scripts/authenticate_kite.py
```

To force a fresh login:

```powershell
python scripts/authenticate_kite.py --force
```

---

## 📊 Downloading Historical Data

Download historical 5-minute candle data for an NSE/BSE symbol:

```powershell
python scripts/download_historical.py --symbol NIFTYBEES --start 2026-08-01 --end 2026-08-31
```

The pipeline:

1. Validates or refreshes the Zerodha session.
2. Downloads the instrument master list.
3. Resolves the symbol dynamically to its Zerodha instrument token.
4. Fetches historical candles in chunks with rate limiting.
5. Normalizes timestamps to `Asia/Kolkata` and removes duplicate records.
6. Runs OHLCV validation.
7. Saves the resulting CSV under `data/raw/`.

### Current NIFTYBEES data checkpoint

The August 2026 NIFTYBEES 5-minute sample currently used to validate the pipeline contains **1,575 rows across 21 trading sessions**, with 75 bars per session, zero duplicate timestamps, zero unexpected intraday gaps, and zero zero-volume rows.

This is a **data-quality checkpoint, not evidence that NIFTYBEES contains a tradable edge**. The sample is also too short to support a final strategy conclusion.

---

## 🔎 Dataset Audit

Run the audit against a downloaded OHLCV file:

```powershell
python scripts/audit_historical.py data/raw/NSE_NIFTYBEES_5minute.csv
```

The audit checks:

- number of rows and trading sessions,
- first/last timestamp,
- duplicate timestamps,
- timestamp ordering,
- unexpected within-session intervals,
- bars per trading day,
- zero-volume rows,
- within-session 5-minute return statistics,
- time-of-day return and volume behavior.

The audit is deliberately separate from the trading strategy. It tells us whether the data is structurally trustworthy enough to support the next research step.

---

## 🧭 Multi-Instrument Universe Audit

Once several candidate datasets have been downloaded, run:

```powershell
python scripts/audit_universe.py data/raw --output data/reports/universe_audit.csv
```

The command compares all `*_5minute.csv` datasets using the same structural checks.

The default eligibility filter requires at least 20 trading sessions and 1,000 rows, with zero duplicate timestamps, zero unexpected intraday gaps, and zero zero-volume rows. **It does not rank instruments by returns or strategy P&L.**

This keeps universe selection separate from strategy optimization and reduces the risk of selecting instruments because they happen to produce attractive historical results.

---

## 🧪 Intraday Event Study

The first research layer after the data audit is an **event study**. Instead of immediately optimizing a trading strategy, we ask whether a measurable market condition is followed by statistically different forward returns.

The framework provides:

- configurable forward horizons in bars,
- strict same-session forward-return calculation,
- event masks aligned exactly to the OHLCV index,
- an exploratory momentum + volume event definition,
- mean and median forward returns,
- standard deviation,
- win rate,
- 10th/90th percentile outcomes.

Example:

```powershell
python scripts/run_event_study.py data/raw/NSE_NIFTYBEES_5minute.csv
```

The default exploratory event asks roughly:

> **When short-term price movement is unusually large and current volume is unusually high relative to its prior intraday history, what happens over the next 5, 15, 30, and 60 minutes?**

This is intentionally an **investigative hypothesis**, not a claim that the event is profitable.

### Current interpretation

The first NIFTYBEES event study generated only 23 events. Usable observations fell to 12 at the longest horizon. The result did not provide convincing evidence of a robust continuation edge. This is exactly why the project does not proceed directly to ML optimization.

The result should be treated as an exploratory diagnostic, not as a failed final strategy and not as evidence of a profitable reversal strategy.

### Leakage controls

The implementation is designed so that:

- the event definition uses information available at the event bar,
- the volume baseline is shifted so the current bar does not influence its own baseline,
- forward returns use future bars only,
- forward returns never cross an overnight/session boundary,
- events must share the exact same index as the source OHLCV data.

A positive event-study result is **not sufficient** to create a strategy. We still need statistical robustness, multiple market regimes, realistic execution costs, out-of-sample testing, and walk-forward validation.

---

## 🧪 Running Unit Tests

Run the complete test suite:

```powershell
pytest
```

Tests cover authentication helpers, OHLCV validation, dataset auditing, event-study leakage safeguards, and universe-selection safeguards.

---

## 🗺️ Research Roadmap

```text
Phase 0 — Research design & data specification        ✅
Phase 0 — India regulatory/execution specification    ✅
Phase 0 — ₹30k capital feasibility specification     ✅
Phase 0 — Research universe specification             ✅
Phase 1 — Historical data validation & audit          ✅
Phase 1 — Initial intraday event study               ✅ exploratory
Phase 1 — Multi-instrument universe audit             ▶ current
Phase 2 — Directional event studies + statistics
Phase 3 — Baseline strategy construction
Phase 4 — Feature engineering
Phase 5 — ML conditional signal/filter
Phase 6 — Robust backtesting + transaction costs
Phase 7 — Walk-forward / out-of-sample validation
Phase 8 — Paper / shadow trading
Phase 9 — Broker execution validation
Phase 10 — Small controlled live validation
Phase 11 — Portfolio of validated strategies
```

The project will not move to ML merely because ML is available. A model must demonstrate that it adds information beyond a defensible statistical baseline.

---

## 📜 License & Compliance

This codebase is designed for quantitative research, backtesting, and controlled paper/live validation. Ensure compliance with your broker's API terms, market-data licensing requirements, exchange rules, and applicable regulations.

**Last regulatory baseline review:** 2026-09-11.
