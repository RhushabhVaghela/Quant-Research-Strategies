# Quant Research Strategies

A modular Python repository for quantitative trading research, data layer processing, strategy development, and automated Zerodha Kite Connect API integration.

---

## 📌 Features

- **Automated Zerodha OAuth Authentication**: Zero-touch authentication flow with local HTTP redirect listener (`http://127.0.0.1:8000/callback`). Automatically exchanges request tokens and updates `.env` directly without manual file copying.
- **Historical Data Layer**: Fetch, clean, and chunk historical market data (5-minute, daily, etc.) for NSE/BSE instruments from Zerodha.
- **Data Validation & Quality Checks**: Enforces strict OHLCV validation rules (price bounds, non-negative volume, duplicate timestamp detection, monotonic ordering).
- **Extensible Architecture**: Clean separation between data ingestion, authentication, validation, and strategy development.

---

## 📁 Project Structure

```text
Quant-Research-Strategies/
├── src/
│   └── data/
│       ├── __init__.py
│       ├── kite_auth.py        # Automated OAuth & session manager
│       ├── kite_client.py      # Authenticated KiteConnect client wrapper
│       ├── historical.py       # Historical candle chunking & fetch logic
│       ├── instruments.py      # Instrument master downloader & resolver
│       └── validation.py       # Data validation rules & quality reports
├── scripts/
│   ├── authenticate_kite.py   # Standalone session verification & token refresh
│   └── download_historical.py # CLI script to download historical candle data
├── tests/
│   ├── test_auth.py           # Unit tests for authentication & environment manager
│   └── test_validation.py     # Unit tests for OHLCV validation
├── trading_resources/         # Reference materials, notebooks & strategy guides
├── .env.example               # Template for environment configuration
├── pytest.ini                 # Pytest configuration
├── requirements.txt           # Python dependencies
└── README.md                  # Project documentation
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

```bash
cp .env.example .env
```

Edit `.env`:
```env
KITE_API_KEY=your_zerodha_api_key
KITE_API_SECRET=your_zerodha_api_secret
KITE_ACCESS_TOKEN=
```

> ⚠️ **Security Note**: Never commit `.env` to version control. It is listed in `.gitignore`.

---

## 🔑 Automated Zerodha Authentication

Zerodha Kite Connect access tokens expire daily. The repository provides a zero-touch automated authentication process:

### How It Works:
1. When any script runs, `ZerodhaAuthenticator` checks if the current `KITE_ACCESS_TOKEN` in `.env` is active (`kite.profile()`).
2. If the token is missing or expired, a local HTTP callback server (`http://127.0.0.1:8000/callback`) automatically starts and opens your browser's login page.
3. Upon completing your Zerodha login, the callback listener automatically intercepts the `request_token`, exchanges it for a fresh `access_token`, and updates `.env` directly.

### Manual Session Refresh

You can manually trigger or verify your Zerodha session at any time:

```powershell
python scripts/authenticate_kite.py
```

To force a fresh login even if your token is valid:

```powershell
python scripts/authenticate_kite.py --force
```

---

## 📊 Downloading Historical Data

Download historical candle data for any exchange symbol (e.g., `NIFTYBEES`) over a specified date range:

```powershell
python scripts/download_historical.py --symbol NIFTYBEES --start 2026-08-01 --end 2026-08-31
```

### What this command does:
1. Validates or refreshes your Zerodha session token.
2. Downloads the NSE instrument master list.
3. Resolves the symbol to its Zerodha `instrument_token`.
4. Fetches 5-minute OHLCV candles in 30-day chunks with rate-limiting pauses.
5. Normalizes timestamps to `Asia/Kolkata` time zone and deduplicates records.
6. Validates data integrity (`assert_valid`).
7. Saves the output CSV to `data/raw/NSE_NIFTYBEES_5minute.csv`.

---

## 🧪 Running Unit Tests

Run the test suite using `pytest`:

```powershell
pytest
```

---

## 📜 License & Compliance

This codebase is designed for quantitative research and paper trading backtesting. Ensure compliance with your broker's API terms of service and market data usage guidelines.
