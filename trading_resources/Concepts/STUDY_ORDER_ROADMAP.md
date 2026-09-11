# 🗺️ Study-Order Roadmap — Beginner → Master

> **How to use this roadmap:** Follow the levels in order; within a level, courses are ordered by dependency. Each course is a single file in this folder with its full concept list (concepts + per-concept prerequisites) plus a section-by-section view. Every course and the prerequisite reference is also combined in `MASTER_Complete_Concept_Curriculum.md`.
>
> **📖 First, study `CORE_CONCEPTS_LIBRARY.md`** — it defines every foundational concept the courses assume (put-call parity, Black-Scholes, greeks, covariance, stationarity, ADF, cointegration, train-test, metrics, etc.), so you don't need a separate textbook.
>
> **Legend:** 🟢 Beginner → 🟡 Intermediate → 🟠 Advanced → 🔴 Master.

---

## 🟢 LEVEL 1 — BEGINNER (Foundations)
*Prereq: none. Goal: Python + data + first backtest.*

### 1. Python for Trading (Basic)
- **File:** `Python-for-Trading-Basic.md`
- **Teaches:** Python syntax (variables, types, control flow, functions, loops), data structures (list/dict/tuple/set), NumPy arrays & vectorization, pandas Series/DataFrame, matplotlib plotting, importing CSV/web data, and a closing Buy-and-Hold strategy.
- **Prereqs:** none.

### 2. Getting Started with Algorithmic Trading
- **File:** `Getting-Started-with-Algorithmic-Trading.md`
- **Teaches:** financial data import (yfinance/CSV), pandas DataFrame basics, matplotlib, and the full moving-average-crossover strategy (signals, shift, transaction costs, cumulative returns, Sharpe, drawdown).
- **Prereqs:** Python for Trading (Basic).

### 3. Python for Machine Learning
- **File:** `Python-for-Machine-Learning.md`
- **Teaches:** ML workflow — features & target, train-test split, RandomForest fit/predict, classifier & regressor metrics, backtesting metrics.
- **Prereqs:** Python for Trading (Basic).

### 4. Backtesting Trading Strategies
- **File:** `Backtesting-Trading-Strategies.md`
- **Teaches:** data quality/cleaning, entry/exit signal generation, trade-sheet backtesting, trade-level analytics, performance metrics (equity curve, CAGR, volatility, Sharpe, max drawdown), stop-loss/take-profit, transaction costs & slippage, capstone.
- **Prereqs:** Python for Trading (Basic), Getting Started with Algorithmic Trading.

### 5. Swing Trading Strategies
- **File:** `Swing-Trading-Strategies.md`
- **Teaches:** MACD, resampling, stock screener filters (penny/liquidity/mcap/ADX/Hurst/52wk), Williams Fractals + Alligator, trade book, SL/TP, backtesting, Sharpe/Sortino/Calmar metrics, IBridgePy automation.
- **Prereqs:** Backtesting Trading Strategies, Technical Indicators (Level 2).

---

## 🟡 LEVEL 2 — INTERMEDIATE (Technical Analysis & ML)
*Prereq: Level 1. Goal: indicators, ML models, options/risk basics.*

### 6. Technical Indicators Strategies in Python
- **File:** `Technical-Indicators-Strategies-Using-Python.md`
- **Teaches:** SMA/EMA/WMA + crossovers, MACD, ROC, RSI, Chaikin A/D + oscillator, Bollinger Bands, TRIN, multi-timeframe, ATR stops, screener, transaction costs, Supertrend capstone.
- **Prereqs:** Python for Trading (Basic), Backtesting.

### 7. Candlestick Patterns
- **File:** `Candlestick-Patterns.md`
- **Teaches:** bullish marubozu, hammer, hanging man, shooting star via TA-Lib, mplfinance plotting, SL/TP backtesting, trade analytics, resampling, multi-asset capstone.
- **Prereqs:** Technical Indicators, Backtesting.

### 8. Price Action Trading Strategies Using Python
- **File:** `Price-Action-Trading-Strategies.md`
- **Teaches:** head & shoulders, double/triple tops & bottoms, support/resistance, pivot systems (traditional/Woodie's/Camarilla), Fibonacci retracements, trade analytics, performance metrics, transaction costs.
- **Prereqs:** Technical Indicators, Backtesting.

### 9. Quantitative Trading Strategies and Models
- **File:** `Quantitative-Trading-Strategies-and-Models.md`
- **Teaches:** ARIMA price forecasting, GARCH volatility forecasting, technical strategies (Bollinger, EMA/SAR/Stochastic, Volume Reversal), drawdown/Sharpe evaluation.
- **Prereqs:** Financial Time Series (below), Technical Indicators.

### 10. Financial Time Series Analysis for Trading
- **File:** `Financial-Time-Series-Analysis.md`
- **Teaches:** returns/log returns, correlation, regression, error metrics, stationarity/ADF, volatility, ACF/PACF, AR/MA/ARIMA (AIC selection), ARCH/GARCH, capstone.
- **Prereqs:** Python for Trading (Basic), basic statistics.

### 11. Statistical Arbitrage Trading
- **File:** `Statistical-Arbitrage.md`
- **Teaches:** pairs trading, ADF test, cointegration, spread/hedge ratio, statistical concepts overview.
- **Prereqs:** Financial Time Series (ADF/stationarity), regression.

### 12. Event-Driven Strategies
- **File:** `Event-Driven-Strategies.md`
- **Teaches:** calendar/seasonal anomalies — turn-of-month, payday, FED day, options expiration, auction effect (fixed income), end-of-month, calendar & December effects (volatility), composite strategy, paper/live trading.
- **Prereqs:** Backtesting, Financial Time Series.

### 13. Volatility Trading for Beginners
- **File:** `Volatility-Trading-Beginners.md`
- **Teaches:** beta & CAPM, Betting-Against-Beta (BAB) research, Bollinger Bands, breakout strategy, entry signals, fixed SL/TP, hedging using VIX, selective long on VIX.
- **Prereqs:** Technical Indicators, Financial Time Series.

### 14. Position Sizing
- **File:** `Position-Sizing.md`
- **Teaches:** fixed units/sum/percentage sizing, volatility models (EWMA/ATR/GARCH), volatility targeting, CPPI, TIPP, Kelly criterion, optimal F, bootstrap simulation, conservative framework.
- **Prereqs:** Backtesting, Risk Management basics.

### 15. Short Selling in Trading
- **File:** `Short-Selling-in-Trading.md`
- **Teaches:** returns, relative/rebased series, stock screener, regime methods (MA crossover, breakout/breakdown, floor & ceiling), strategy creation/optimization, Kelly/gain-expectancy, position sizing.
- **Prereqs:** Technical Indicators, Position Sizing.

### 16. Futures Trading — Concepts & Strategies
- **File:** `Futures-Trading-Concepts-Strategies.md`
- **Teaches:** expected PnL, trend-following entries/exits/returns, diversification, counter-trend entries/exits, futures continuations (additive/proportional adjustment), futures PnL, term structure/annualised implied yield, position allocation, strategy analysis.
- **Prereqs:** Backtesting, Position Sizing.

### 17. Algo Trading (Zerodha)
- **File:** `Algo-Trading-Zerodha.md`
- **Teaches:** KiteConnect auth/session, instrument list, quotes, rate limiting/batching, historical data + OI, WebSockets/KiteTicker, SMA crossover signals, order types (SL/SL-M/CO/GTT/AMO/Iceberg), order management, positions/holdings, low-frequency + full automated system.
- **Prereqs:** Python for Trading (Basic), Backtesting.

### 18. Introduction to Machine Learning for Trading
- **File:** `Introduction-to-Machine-Learning-for-Trading.md`
- **Teaches:** supervised learning, predict trend using classification, features/target, train-test, model evaluation.
- **Prereqs:** Python for Machine Learning.

### 19. Trading with Machine Learning — Regression
- **File:** `Trading-with-Machine-Learning-Regression.md`
- **Teaches:** data generation, preprocessing, pipeline, cross-validation, linear regression, strategy/performance, next-day high/low prediction.
- **Prereqs:** Intro to ML for Trading.

### 20. Trading with ML — Classification & SVM
- **File:** `Trading-with-ML-Classification-and-SVM.md`
- **Teaches:** SVM classification strategy with RSI/SMA/SAR/ADX features, quantile signal encoding, RandomizedSearchCV, confusion matrix, classification report, drawdown, Sharpe.
- **Prereqs:** Intro to ML for Trading.

### 21. Decision Trees in Trading
- **File:** `Decision-Trees-in-Trading.md`
- **Teaches:** regression trees, classification (gini, class weights), cross-validation & hyperparameter tuning (KFold, GridSearch), parallel ensembles (Bagging, Random Forest), sequential ensembles (AdaBoost, Gradient Boosting), live-trading challenges.
- **Prereqs:** Intro to ML for Trading.

### 22. Unsupervised Learning in Trading
- **File:** `Unsupervised-Learning-in-Trading.md`
- **Teaches:** PCA (math + application), feature selection (ADF + correlation), scaling, k-means, WCSS/elbow, cluster analysis (hit ratio + skewness), DBSCAN, pairs trading via clustering, cointegration/ADF.
- **Prereqs:** Intro to ML, Financial Time Series (ADF).

### 23. Data & Feature Engineering for Trading
- **File:** `Data-and-Feature-Engineering-for-Trading.md`
- **Teaches:** EDA (ydata_profiling), bars (time/tick/volume/dollar), information/imbalance bars, fractional differentiation, outliers, survivorship bias, redundant stocks, multiple stock classes, news numerical/categorical features, labeling (fixed-time, triple-barrier), fundamental merge (Sharadar).
- **Prereqs:** Intro to ML, Financial Time Series.

---

## 🟠 LEVEL 3 — ADVANCED (Options, Portfolio, Crypto/FX)
*Prereq: Level 2. Goal: options greeks/vol, portfolio theory, systematic strategies.*

### 24. Options Trading Strategies in Python — Basic
- **File:** `Options-Trading-Strategies-Basic.md`
- **Teaches:** call/put payoff, bull call & bear put spreads, covered call, protective put, historical volatility.
- **Prereqs:** Python for Trading (Basic), basic options concept.

### 25. Options Trading Strategies in Python — Intermediate
- **File:** `Options-Trading-Strategies-Intermediate.md`
- **Teaches:** full Greeks calculator (delta/gamma/vega/theta/rho), delta+gamma & vega price approximation, Black-Scholes pricing, calendar spread, options data sourcing, volatility skew/smile/forward strategies.
- **Prereqs:** Options Basic, Black-Scholes.

### 26. Options Trading Strategies in Python — Advanced
- **File:** `Options-Trading-Strategies-Advanced.md`
- **Teaches:** dispersion trading (implied dirty correlation), three VaR methods (historical, Monte Carlo, variance-covariance), decision-tree option-price prediction, delta hedging + gamma scalping.
- **Prereqs:** Options Intermediate, Risk Management.

### 27. Options Volatility Trading — Concepts & Strategies
- **File:** `Options-Volatility-Trading-Concepts-and-Strategies.md`
- **Teaches:** close-to-close, Garman-Klass, Parkinson estimators, variance premium, Monte Carlo simulation, options valuation, PnL distribution of options strategies, paper/live trading.
- **Prereqs:** Options Intermediate, Volatility Trading.

### 28. Advanced Options Volatility — Strategies & Risk Management
- **File:** `Advanced-Options-Volatility-Strategies-and-Risk-Management.md`
- **Teaches:** volatility skew calculation, IV rank, delta-hedging implementation, delta-neutral skew analysis, forecasting IV using ML, capstone (strangle, risk management).
- **Prereqs:** Options Volatility Concepts, Options Advanced.

### 29. Systematic Options Trading
- **File:** `Systematic-Options-Trading.md`
- **Teaches:** options screener, butterfly strategy (payoff/setup/backtest), expected profit, data pre-processing, distributions/POP (lognormal, empirical), iron condor, SL/TP, trade-level analytics.
- **Prereqs:** Options Intermediate, Backtesting.

### 30. Trading Using Options Sentiment Indicators
- **File:** `Trading-Using-Options-Sentiment-Indicators.md`
- **Teaches:** breadth measures (TRIN), option trading measures (PCR), volatility measures (VIX), sentiment/fear-greed, volume & open interest, strategies.
- **Prereqs:** Options Basic, Technical Indicators.

### 31. Machine Learning for Options Trading
- **File:** `Machine-Learning-for-Options-Trading.md`
- **Teaches:** implied volatility concepts & forecasting, features to predict underlying, decision-tree direction forecast, ensemble classifiers, blending models, classifier metrics, best-option-strategy selection.
- **Prereqs:** Options Intermediate, Decision Trees, Intro to ML.

### 32. Quantitative Portfolio Management
- **File:** `Quantitative-Portfolio-Management.md`
- **Teaches:** portfolio construction, Modern Portfolio Theory / efficient frontier, Risk Parity, Kelly criterion, Beta, momentum & short-term-reversal factors, Fama-French 3-factor, multi-factor model, performance analysis (Sharpe/Sortino/Treynor/Info ratio, drawdown).
- **Prereqs:** Financial Time Series, Position Sizing.

### 33. Value Strategy in Forex
- **File:** `Value-Strategy-in-Forex.md`
- **Teaches:** REER valuation mean-reversion, rolling-mean signal, publication-lag/look-ahead handling, multi-pair equal-weight portfolio, Sharpe/CAGR/MDD.
- **Prereqs:** Financial Time Series, Portfolio Management.

### 34. Forex Trading with Python — Basics
- **File:** `Forex-Trading-with-Python-Basics.md`
- **Teaches:** forex market basics, currency pairs, data sourcing and FX data handling before strategy work.
- **Prereqs:** Python for Trading (Basic).

### 35. Crypto Trading Strategies — Intermediate
- **File:** `Crypto-Trading-Strategies-Intermediate.md`
- **Teaches:** cryptocompare data, RSI/Aroon divergence, Ichimoku Cloud, performance metrics, trade-level analytics, day-of-week calendar anomaly, transaction cost & slippage.
- **Prereqs:** Technical Indicators, Backtesting.

### 36. Crypto Trading Strategies — Advanced
- **File:** `Crypto-Trading-Strategies-Advanced.md`
- **Teaches:** Hurst exponent regime strategy, cross-sectional long-only momentum, pairs trading with OLS hedge ratio & ADF cointegration, K-Means clustering regime filter.
- **Prereqs:** Crypto Intermediate, Statistical Arbitrage, Unsupervised Learning.

### 37. Getting Market Data — Stocks, Crypto, News & Fundamental
- **File:** `Getting-Market-Data-Stocks-Crypto-News.md`
- **Teaches:** yfinance (equity/index/minute/FX/futures), futures continuations, macro (FRED/wbgapi), crypto (cryptocompare), news (NewsAPI), options chains, SimFin fundamentals, data cleaning.
- **Prereqs:** Python for Trading (Basic).

---

## 🔴 LEVEL 4 — MASTER (Deep Learning, NLP, RL, LLMs)
*Prereq: Level 3. Goal: modern AI for trading.*

### 38. Neural Networks in Trading
- **File:** `Neural-Networks-in-Trading.md`
- **Teaches:** MLP/neural nets, activation functions, Keras layers, cross-validation in Keras, LSTM, RNN, deep-learning trading strategy, live-trading challenges.
- **Prereqs:** Intro to ML, Python for Machine Learning.

### 39. Deep Reinforcement Learning in Trading
- **File:** `Deep-Reinforcement-Learning-in-Trading.md`
- **Teaches:** ANN implementation, DQN/DDQN, state/action construction, experience replay, backtesting implementation, capstone.
- **Prereqs:** Neural Networks, Backtesting.

### 40. Natural Language Processing in Trading
- **File:** `Natural-Language-Processing-in-Trading.md`
- **Teaches:** bag of words, TF-IDF, BERT, sentiment score & strategy logic, sentiment strategies on bonds, XGBoost, paper/live trading.
- **Prereqs:** Intro to ML, Python for Machine Learning.

### 41. Trading Using LLMs
- **File:** `Trading-Using-LLM.md`
- **Teaches:** data collection & preprocessing, sentiment analysis of FOMC transcripts, sentiment analysis using audio data, strategy variations to trade FOMC, trade FOMC using sentiment score.
- **Prereqs:** NLP, Financial Time Series.

---

## 📌 Cross-cutting Prerequisite Map
- **Python & pandas** → everything (Level 1).
- **Returns / log returns / compounding** → all backtesting, performance metrics, options, portfolio.
- **Stationarity / ADF / cointegration** → Statistical Arbitrage, Unsupervised (pairs), Crypto Advanced.
- **Black-Scholes & implied volatility** → all options courses (Level 3).
- **Greeks (delta/gamma/vega/theta/rho)** → Options Intermediate → Advanced (delta hedging, gamma scalping, dispersion).
- **Train-test split & model metrics** → all ML/DL/NLP courses.
- **Sharpe / Sortino / drawdown / CAGR** → every strategy course's evaluation.

> Full definitions of all these foundations are in `CORE_CONCEPTS_LIBRARY.md`.