# Strategy 002 — Repository Resource Review

**Date:** 2026-09-20  
**Purpose:** Record the existing repository resources that should be considered before implementing new Strategy 002 research code.

## Decision

Strategy 002 will reuse the repository's existing research/data infrastructure where appropriate. No new strategy engine is justified at this stage.

The review confirms that the repository already contains substantial material for the first investigation phase.

## Relevant existing resources

### 1. Financial time-series analysis

trading_resources/Concepts/Financial-Time-Series-Analysis.md

Relevant methods include returns, correlation/covariance, regression, stationarity and ADF, volatility, ACF/PACF, AR/MA/ARIMA, and ARCH/GARCH. These are appropriate building blocks for descriptive market-behavior investigation before strategy definition.

### 2. Unsupervised learning and cross-sectional structure

trading_resources/Concepts/Unsupervised-Learning-in-Trading.md

Relevant material includes variance/covariance, PCA, feature selection, correlation filtering, k-means, DBSCAN, clustering analysis, stationarity, and pairs/cointegration as one possible later research direction.

The existence of pairs-trading material does **not** mean Strategy 002 is a pairs strategy. It is simply one available research method if the data investigation later provides a reason to examine relative-value structure.

### 3. Event-study infrastructure

Existing files:

- src/research/event_study.py
- scripts/run_event_study.py

The event-study implementation is explicitly designed to measure forward returns after defined events without presenting the result as a backtest. It can therefore be reused for pattern characterization after the initial data audit, provided event definitions are treated as exploratory and the number of alternatives tested is recorded.

### 4. Existing data-audit infrastructure

Existing Strategy 001J data validation and acquisition code should be reused where the same data schema and universe apply.

Relevant resources include:

- scripts/validate_strategy_001j_data_gate.py;
- Strategy 001J universe/data specifications;
- existing broker-native data acquisition utilities;
- src/data/audit.py.

These should be used to establish data integrity before interpreting patterns.

### 5. Existing strategy ideation material

research/strategy_ideation.md

This document contains previously discussed candidate mechanisms including momentum, mean reversion, relative value, volume/price, volatility, signal ensembles, and options/volatility.

For Strategy 002, these are **not preselected hypotheses**. They are an inventory of mechanisms that can be compared against evidence emerging from the data investigation.

The old candidate ranking must not be treated as a Strategy 002 decision.

### 6. Fundamental/economic context resources

The repository contains WQU Financial Data material and concept inventories that can support economic/fundamental investigation.

Fundamental analysis will only be incorporated when reliable, point-in-time data is available for the selected universe. We will not create a fundamental strategy merely because fundamental concepts exist in the repository.

## What we will not do yet

We will not:

- build a pair-trading engine;
- define entry/exit thresholds;
- run a parameter grid;
- select a strategy based on backtest P&L;
- open the holdout;
- create a Strategy 002-specific optimizer;
- choose a mechanism because it is familiar or already present in the repository.

## Next research action

Use the existing data-audit infrastructure to establish exactly what Strategy 002 can reliably observe.

Then produce the first data-understanding report covering:

1. universe and instrument coverage;
2. history and session integrity;
3. return distributions;
4. volatility;
5. volume/liquidity;
6. autocorrelation;
7. intraday/time-of-day structure;
8. cross-sectional dependence;
9. available fundamental/economic fields and their point-in-time status;
10. known data limitations.

Only after this report should pattern-discovery experiments be registered.

## Research-control note

This resource review is itself part of the audit trail. Reusing an existing method does not make a future result validated. Every method must still satisfy the current Strategy 002 timing, data-quality, multiple-testing, economic-interpretation, and validation requirements.
