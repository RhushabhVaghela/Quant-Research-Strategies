# Options Trading Strategies in Python — Advanced (Concept Inventory)
Data modules (`data_modules/`): `AAPL_new.csv`, `closeprice.csv` (7-stock portfolio), `BankNifty_Futures_Data.csv`, `BankNifty_Options_Data.csv`, `BankNifty_Preprocessed_Options_Data.csv`, `NIFTY_GS_data.csv`, `Nifty_ML_data.csv`, `spx_options_raw_data/*.7z`.
Key conventions: `mibian.BS` for implied volatility and Greeks; futures price as the underlying with `interest_rate = 0`; lot sizes (Nifty 75, BankNifty 40) applied when aggregating Greeks.
---
## MODULE: Sourcing Options Data
### LESSON: Options Data Storing.ipynb
- **Bulk options data sourcing** — extract SPX `.7z` bundles with `py7zr`, concatenate monthly CSVs into a master frame. prereqs: pandas I/O, 7z/ZIP handling
- **File housekeeping** — `os.listdir`/`os.remove` plumbing. prereqs: Python os
- **Raw option-quote schema** — quote unix/readtime/date/hour, underlying last, expire date, DTE, strike distance, per-leg Δ Γ V Θ ρ, IV, volume. prereqs: options data
## MODULE: Dispersion Trading
### LESSON: Dispersion Trading Strategy.ipynb
- **Dispersion trading** — profit from mean-reversion in the implied correlation between an index and its constituents. prereqs: implied volatility, straddle payoff
- **Data required** — ATM strikes/IV for the index (BankNifty) and top constituents, weighted-constituent IV, "dirty" implied correlation, lot sizes and index weights. prereqs: dispersion trading
- **Pipeline** — read per-instrument options CSV → time-to-expiry → ATM strike (min |future − strike|) → daily straddle PnL → IV via `mibian.BS.impliedVolatility` → straddle delta per leg. prereqs: Black-Scholes IV, pandas
- **Straddle construction** — ATM call + ATM put; straddle delta near zero → Delta hedging with futures skipped (kept ~neutral). prereqs: straddle payoff, delta
- **Dirty implied correlation** — `(index IV / weighted-average constituents IV)²`, i.e. squared vol ratio. prereqs: implied volatility, correlation
- **Trading rule** — long index-straddle + short-constituent-straddles when correlation is low (below mean − ½·std); reverse when high; exit on reversion (signal +1/−1/0). prereqs: mean-reversion signal construction
- **Constituent leg PnL** — opposite sign of index signal; aggregate with weighted × lot-size PnL → cumulative strategy PnL. prereqs: dispersion trading
- **Expiry-day caveat** — correlation spike (≈5) ignored; no positions on expiry. prereqs: dispersion trading
## MODULE: Exotic Options (Value at Risk)
### LESSON: VaR (Historical Method).ipynb
- **Value at Risk (VaR)** — maximum portfolio loss not exceeded over a horizon at a given confidence level; three components: confidence level, time horizon, expected loss. prereqs: daily returns, percentiles/quantiles
- **Historical (non-parametric) method** — compute daily returns → sort worst-to-best → VaR at 90/95/99% = 10th/5th/1st percentile. prereqs: VaR, percentiles
- **Motivating histogram** — few days lose more than −4%. prereqs: returns distribution
- **Application** — single stock (Apple) and equally-weighted 7-stock portfolio; daily VaR in %. prereqs: portfolio maths
- **Diversification effect** — portfolio VaR lower than single-stock VaR → diversification cuts stock-specific risk. prereqs: portfolio maths
### LESSON: VaR (Monte Carlo Simulation).ipynb
- **Monte Carlo VaR** — simulate stock returns by geometric Brownian motion `ST = S0·exp((μ − ½σ²)T + σ√T·ε)` with normal random shocks. prereqs: GBM, normal RNG
- **Parameters** — `S0`, drift μ, vol σ, horizon T, number of simulations I (e.g., 500). prereqs: Monte Carlo VaR
- **VaR from simulations** — sort simulated terminal returns worst→best, take percentiles for 90/95/99% VaR. prereqs: Monte Carlo VaR, percentiles
- **Simulation dispersion** — each simulation yields slightly different results; supports confidence-interval intuition. prereqs: Monte Carlo VaR
### LESSON: VaR (Variance-Covariance Method).ipynb
- **Parametric VaR** — assumes normally distributed returns; estimate mean/σ from history, overlay normal pdf, read VaR off quantiles. prereqs: normal distribution, VaR
- **Closed-form** — at 95% → mean − 1.65·σ; at 99% → mean − 2.33·σ (via `scipy.stats.norm.ppf`). prereqs: parametric VaR, scipy
- **Application** — single stock (Apple) and equally-weighted portfolio; smoother/gaussian-model-based values. prereqs: parametric VaR
- **Three VaR styles** — contrast historical (empirical), Monte Carlo, and parametric approaches. prereqs: VaR methods
## MODULE: Machine Learning
### LESSON: Options Price Prediction Using Decision Tree.ipynb
- **Supervised classifier** — learns decision rules from predictor variables (IV, Delta, Gamma, Theta, Vega) to predict whether tomorrow's option price moves up (+1) or down (−1). prereqs: option Greeks, basic supervised classification
- **Target definition** — `+1` if next-day LTP > today's LTP, else `−1` (`np.where(LTP.shift(-1) > LTP, 1, -1)`). prereqs: numpy, pandas
- **Train/test split** — e.g., first 70 days train, remainder test; hyper-params `max_depth=6, min_samples_split=2, max_leaf_nodes=8`. prereqs: train/test splitting
- **Model fit & accuracy** — `DecisionTreeClassifier.fit(...)` then `accuracy_score` on train (80%) and test (55.7%). prereqs: decision tree, accuracy
- **Strategy returns** — predicted signal × next-day return; plot cumulative strategy returns in test period. prereqs: strategy returns
## MODULE: Risk Management
### LESSON: Delta Hedging Strategy.ipynb
- **Delta hedging** — removes the portfolio's sensitivity to the underlying move; Delta = change in option price per unit change in underlying. prereqs: delta, implied volatility
- **Compute IV then Delta** — IV from observed option price → Delta via `mibian.BS(...).callDelta`. prereqs: mibian, implied volatility
- **Contract-delta scaling** — multiply Delta by option lot size (Nifty 75) to get total delta. prereqs: lot sizing, delta
- **Delta neutrality** — sell futures to offset a long call's positive delta (round futures to a tradable multiple). prereqs: futures mechanics, delta
- **PnL decomposition** — futures PnL + call PnL = portfolio PnL; residual loss (≈ ₹600) because higher-order Greeks (Gamma, Theta) are unhedged. prereqs: delta hedging
- **Bridge to gamma scalping** — full Delta-neutrality with Gamma/theta effects feeds into Gamma scalping. prereqs: delta hedging, gamma
### LESSON: Gamma Scalping Strategy.ipynb
- **Gamma scalping** — repeatedly re-hedging a long-Gamma (long-vega) position to monetise convexity earned from committed vs re-hedged moves, offsetting daily time decay (theta). prereqs: delta/gamma, straddle payoff
- **Structure** — buy an ATM straddle (ATM call + ATM put) on Nifty; track the straddle's aggregate Delta. prereqs: straddle payoff, delta
- **Rebalancing rule** — underlying rises → straddle delta-positive → sell Nifty futures; underlying falls → straddle delta-negative → buy futures; keep futures book-neutral in lot-size multiples. prereqs: delta hedging, futures mechanics
- **PnL** — straddle PnL (call + put daily delta×lot) + Nifty futures PnL → cumulative strategy PnL. prereqs: gamma scalping
- **Demonstration** — profitability (≈ ₹1000) purely from delta re-hedging momentum. prereqs: gamma scalping
## Course-level prerequisite map
- Sourcing (1) is a prerequisite; IV/Delta/sigma helpers employed throughout.
- Risk notebooks (7–8) consume the Greeks/hedging from Intermediate, forming the "delta-neutral" theme.
- VaR notebooks (3–5) cover risk estimation (historical / Monte-Carlo / parametric).
- Dispersion (2) pulls together straddles, implied vol, correlation, delta-neutral hedging, and lot-size aggregation.
- ML notebook (6) applies classifier modelling to option-price direction.