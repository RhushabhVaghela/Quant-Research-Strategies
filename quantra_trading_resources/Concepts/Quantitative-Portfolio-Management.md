# Quantitative Portfolio Management — Concept Inventory
> 11 notebooks (no shared code module; data files in `data_modules/`).
Course flow: portfolio construction mathematics → Modern Portfolio Theory → risk-based weights (Risk Parity, Kelly) → single-asset risk (Beta) → factor models (Momentum, Short-Term Reversal, Fama-French) → performance measurement → capstone.
---
## Notebooks
### 1. Basics of Portfolio Construction — **Basics of Portfolio Construction_/Basics of Portfolio Construction.ipynb**
- **Annualized returns** of individual stocks (compound/geometric annualization of cumulative returns over trading days). *Prereq: daily returns, pct_change, trading days/year.
- **Annualized standard deviation (volatility)** of stock returns (daily σ × √trading days). *Prereq: standard deviation, sqrt rule.
- **Portfolio returns** — weighted sum of component expected returns. *Prereq: weights, expected returns.
- **Covariance** — measure of co-movement between two asset return series. *Prereq: return series, variance.
- **Portfolio standard deviation** — combining individual σ with covariance (two-asset covariance including weights). *Prereq: covariance, weights.
- Built on MSFT + GOOGL price CSV read via `.read_csv`. *Prereq: pandas, price data.
### 2. Modern Portfolio Theory — **Modern Portfolio Theory/Implement Modern Portfolio Theory in Python.ipynb**
- **Portfolio return & variance** — extends baseline to a three-asset portfolio (CVX, MSFT, GOOGL). *Prereq: portfolio construction.
- **Efficient frontier** — varying weight combinations (a,b) to trace the set of optimal risk/return portfolios. *Prereq: portfolio σ/return, optimization over weights.
- **Optimal weights / minimum-variance and max-return portfolios** — identifying best weight allocation on the frontier. *Prereq: efficient frontier, constraint formulation.
- **Experimental exploration** — changing stocks and the weight parameters to see effects on frontier shape. *Prereq: MPT math.
### 3. Risk Parity — **Risk Parity_/Risk Parity.ipynb**
- **Risk-parity capital allocation (2 stocks)** — weights inversely proportional to each security's risk (annualized σ), equalizing risk contribution. *Prereq: annualized returns/volatility, risk-based allocation.
### 4. Risk Parity for Multiple Stocks — **Risk Parity_/Risk Parity for Multiple Stocks.ipynb**
- **Risk parity for multiple stocks (CVX/IBM/JPM)** — generalize the two-stock allocation to N assets by equal risk contribution per stock. *Prereq: risk parity two-stock, covariance matrix, weights.
- **Portfolio returns of the risk-parity allocation** for evaluation. *Prereq: portfolio returns.
### 5. Kelly Criterion — **Kelly Criterion_/Create a Portfolio Based on Kelly Criterion.ipynb**
- **Kelly criterion** — optimal growth (fractional) betting/position-size rule maximizing long-run portfolio growth (f = edge/odds). *Prereq: portfolio returns, wealth growth, probability theory.
- **Kelly portfolio via cvxpy** — optimize the Kelly criterion to get best weight combination for Chevron (CVX) + IBM. *Prereq: cvxpy optimization, daily returns.
### 6. Beta of an Asset — **Beta/Beta of an Asset in Python.ipynb**
- **Beta via regression (OLS)** — regress asset daily returns vs market (S&P 500 SPY) returns over ~1yr; slope = β. *Prereq: returns, OLS, market benchmark.
- **Beta via variance-covariance method** — β = Cov(asset, market)/Var(market). *Prereq: covariance, variance.
- **Uses & caveats** — systematic-risk measure; needs ≥1 year data; AMZN vs SPY. *Prereq: correlation, market risk.
### 7. Multi-Factor Model — **Multi Factor Model/The Momentum Factor in Python.ipynb**
- **Momentum factor construction** — a factor = a cumulative or trailing price/return series representing momentum across the stock set. *Prereq: daily % change, factor definition.
- **From factor to a factor-based portfolio** — accumulate the momentum factor into a multi-factor model input. *Prereq: daily returns, portfolio construction.
### 8. Multi-Factor Model — **Multi Factor Model/The Short-Term Reversal Factor in Python.ipynb**
- **Short-term reversal factor** — capture mean-reversal of recent losers/winners as a factor. *Prereq: daily returns, reversal effect.
- **Combining momentum + reversal into a multi-factor portfolio** — weighted combination of factor signals into an aggregate factor-based strategy. *Prereq: momentum factor, reversal factor, portfolio weighting.
### 9. Fama-French Three-Factor Model — **Fama-French Three- Factor Model/Expected Returns using Fama-French Model.ipynb**
- **Fama-French three-factor regression** — expected return modeled on : market excess (Rm−Rf), size (SMB = Small minus Big), value (HML = High minus Low), plus Rf. *Prereq: excess returns, multiple linear regression, factor definitions.
- **Daily/excess returns of the stock**, then **coefficients of the Fama-French factors** via regression. *Prereq: returns computation, OLS.
- **Annualized factor returns + expected stock return** — using the fitted coefficients to compute expected return (AMZN, 2016–2019 dataset). *Prereq: coefficient application, annualization.
### 10. Portfolio Performance Analysis — **Portfolio Performance Analysis/Portfolio Performance Analysis.ipynb**
- Portfolio performance measures (all computed on a multi-factor/factor strategy returns series)
 - **Annualized returns** and **annualized volatility** (σ×√252). *Prereq: returns, std.
 - **Sharpe Ratio** (excess return / volatility). *Prereq: risk-free, std.
 - **Sortino Ratio** (return / downside deviation). *Prereq: downside semi-deviation.
 - **Beta** (market co-movement). *Prereq: regression/covariance.
 - **Treynor Ratio** (excess return / β). *Prereq: β.
 - **Information Ratio** (active return / tracking error). *Prereq: benchmark, tracking error.
 - **Skewness** and **Kurtosis** (distribution shape of returns). *Prereq: moments.
 - **Maximum drawdown** (peak-to-trough peak of the aggregate curve). *Prereq: drawdown/equity curve.
### 11. QPM Capstone Project — **Capstone Project/Model Solution_ QPM Capstone Project.ipynb**
- **MPT on multiple assets (capstone)** — import data, annualized returns, random-weight portfolios, compute portfolio metrics, locate minimum-risk / maximum-return / optimal-weight portfolio. *Prereq: MPT notebook, annualized returns/variance, random weights; all portfolio-module concepts.
## Data files (`data_modules/`)
- `AMZN_SPY_Prices_2018_to_2019_Beta.csv` — Beta notebook (AMZN + SPY).
- `Stock_Prices_2016_To_2017_MPT.csv` / `..._RP_3stocks.csv` / `..._RP.csv` — MPT & Risk Parity.
- `Capstone_data.csv` — capstone MPT multiple-asset input.
- `Data_2016_to_2019_FF.csv` — Fama-French factors (Rm−Rf, SMB, HML, Rf) + AMZN.
- `Stock_Prices_2012_To_2017_Factor.csv` — multi-factor (momentum / short-term reversal) stocks.
- `Returns_2012_To_2017_Portfolio_Analysis.csv` / `Momentum_Performance_2012_To_2017.csv` — performance-analysis returns series.
- `Stock_Prices_2011_To_2017_Kelly_Portfolio.csv` — Kelly criterion.
## Non-code support
- `Folder Structure and How to Run Code Files.html`, `ReadMe.html` — setup/run instructions.
## Concept prerequisite flow
portfolio-construction math → MPT → risk-based allocation (Risk Parity → Kelly) → Beta → factor models (Momentum → Short-Term Reversal → Fama-French) → performance measures → capstone MPT model solution.
---
## Quantitative-Portfolio-Management — Section-based course structure
# Concept Inventory: Quantitative Portfolio Management
> Inventoried Sections: 3, 4, 7, 10, 11, 16, 17 (as they appear on disk). PDFs read per section; code confirmed from `QPMResources.zip`.
## COURSE
Quantitative portfolio *construction*, *optimization*, and *position sizing* over a multi-asset equity portfolio. Comprises Modern Portfolio Theory (returns/risk/covariance matrices, efficient frontier), Kelly Criterion (log-optimal bet sizing), Risk Parity (equal risk-contribution weighting), and Fama-French multi-factor expected-return models (3-factor and 5-factor), culminating in a capstone applying MPT to a multi-asset portfolio.
### Section 3 — Modern Portfolio Theory (MPT)
Sources: `Section 3 - Modern Portfolio Theory/11 - Construct Multiple Stocks Portfolio using MPT.pdf` • notebooks: `Implement Modern Portfolio Theory in Python.ipynb`
- **Generalized portfolio returns equation**: `Portfolio returns = Σ(Wi·Xi)`; for two stocks `W1*X1 + W2*X2`.
- **Matrix form**: returns row-vector `X` (1×n annualized returns) × weights column-vector `W` (n×1) → `Portfolio returns = X·W`.
- **Generalized portfolio standard deviation**: `√(Wᵀ · Covariance Matrix · W)`.
- **Two-stock std dev**: `√(W1²σ11 + W2²σ22 + 2·W1·W2·σ12)`; notation σXY = covariance, σXX = variance.
- **Covariance Matrix**: diagonal = variances (self), off-diagonal = covariances (σij=σji); MPT: favor low covariance to maximize risk-return trade-off.
- **Optimization objective**: maximize returns/risk ratio subject to `ΣWi=1` (weights sum to 1).
- **Efficient frontier**: construct many random-weight portfolios, simulate, plot return-vs-risk frontier; **optimal weights** = max (returns/standard deviation) point (max Sharpe-type ratio in the two-asset → multi-asset generalization).
- Python: compute annualized returns & std dev, covariance, change stocks/weights, plot efficient frontier, output min-risk & max-return-risk portfolios.
**Prereqs**: matrix transpose & multiplication; covariance/variance statistics; expected-return concept; some Pandas (returns, cov/corr, portfolio simulation).
### Section 4 — Kelly Criterion
Files: `Section 4 - Kelly Criterion/5 - Kelly-Criterion.pdf` • notebook: `Create a Portfolio Based on Kelly Criterion.ipynb`
- **Formula origin**: J.L. Kelly, Jr., Bell Labs 1956; **Kelly bet size = argmax expected log wealth** (max expected geometric growth rate); used successfully by Warren Buffett / Berkshire Hathaway.
- **Portfolio return (daily)**: `Σ(AssetWeight_i × Asset RateOfReturn_i)`.
- **Portfolio value**: `1 + daily portfolio return` each day.
- **Final portfolio value**: product (compounding) of daily values `∏(1 + Σ W·r)` over j=1..days.
- **Kelly derivation**: maximize logarithm of final portfolio value; because `max(A·B) = max(log A + log B)`, the log transforms the multiplicative-compounding problem into an **additive summation** you can solve directly.
- **Kelly Criterion equation**: `E[ Σ_j log(1 + Σ_i AssetWeight_i · AssetRateOfReturn_i) ]` — maximize expected sum of log daily portfolio values.
- **Application in Python**: compute daily returns across candidate weights, formulate log-sum objective, optimize weights (via python solver); build the Kelly portfolio with those optimized weights; compare performance against a benchmark.
- Core intuition: **_growth-maximizing position sizing** — over/under-sizing reduces compounding growth.
**Prerequisites**: MPT returns formula (Section 3); logarithms / laws of logs; expectation notation; portfolio annualization & compounding; absolute basis for optimization.
### Section 7 — Risk Parity (RP)
Files: `Section 7 - Risk Parity/7 - Portfolio with Multiple Stocks.pdf` • notebook: `Risk Parity.ipynb`
- **Risk Parity principle**: each security's marginal risk contribution to the portfolio is made *equal* — balanced risk across constituents rather than cap-weighting.
- **Two-stock weight formula**: `W1 = (1/σ11) / (1/σ11 + 1/σ22)`, `W2 = (1/σ22) / (1/σ11 + 1/σ22)` generalizes to `wi ∝ 1/σii` normalized.
- **Derivation**: start from portfolio std dev; force equal per-stock variance contribution: `W1²·σ11 = W2²·σ22` (cancels cross-covariance term); yields inverse relationship `Wi·σi = Wj·σj` for each pair → weights inversely prop. to (own) std dev.
- **Multi-stock RP condition**: equate each stock's contribution `Wi·Σ(W·σ)`, i.e. `Σ_n contributions equal for every stock`, subject to `ΣWi=1`.
- **Multi-stock solution**: derivations require advanced math (solving nonlinear parity equations) — out of course scope; practical approach = solve statistically via **scipy / sklearn** library optimizers.
- Notebook: compute annualized returns and std dev, then calculate weights using risk parity.
**Prereqs**: covariance matrix, std dev/variance, weights-normalization, solver literacy (scipy/sklearn), same matrix prereq as MPT/SD.
### Section 10 — Fama-French Three-Factor Model
Files: `Section 10 - Fama-French Three- Factor Model/5 - Calculation of SMB and HML Factor.pdf` • notebook: `Expected Returns using Fama-French Model.ipynb`
- **Three factors**: market, size (SMB – Small minus Big), value (HML – High minus Low).
 - `R_i = Rf + βm(Rm−Rf) + βSMB·SMB + βHML·HML`.
- **Six buckets via two sort dimensions**
 - **Size axis**: rank by market cap; below median = *small*; above median = *big*.
 - **Value axis (B/M ratio)**: rank by Book/Market; >70th pct = *value* (cheap); <30th = *growth* (expensive); 30–70 = *neutral*.
 - Resulting 6 portfolios: Small Value, Small Neutral, Small Growth, Big Value, Big Neutral, Big Growth.
- **SMB factor** = «avg small minus avg big»: `SMB = ⅓(Small V+Neutral+G) − ⅓(Big V+Neutral+G)`.
- **HML factor** = «avg high − avg low»: `HML = ½(Small Value + Big Value) − ½(Small Growth + Big Growth)`.
- **Use**: compute expected returns of a stock (Amazon example) by regressing returns vs the three factors and plugging betas & factor premia into the return formula.
**Prereqs**: CAPM fundamentals (beta, market risk premium), factor regression fit, market-cap & B/M construction, arithmetic averaging.
### Section 11 — Fama-French Five-Factor Model
Files: `Section 11 - Fama-French Five-Factor Model/1 - Fama-French-Five-Factor-Model.pdf`
- Extends 3-factor (CAPM + size + value) with 2 more factors: **Profitability** and **Investment**.
- **Profitability factor (RMW, Robust minus Weak)**: high-profitable firms (gross-profits/assets) yield higher returns than low-profitability. RMW = avg returns of the two robust portfolios minus avg of the two weak.
- **Investment factor (CMA, Conservative minus Aggressive)**: low asset-growth firms outperform high-asset-growth; CMA analogous averaging.
- **Model equation**: `Ri = Rf + β1·(Rm−Rf) + β2·(SMB) + β3·(HML) + β4·(RMW) + β5·(CMA)`.
- **Factor construction** uses 6 portfolios on (each pair of) size-and-book-to-market, size-and-profitability, size-and-investment; SMB is computed by averaging per dimensions: `(SMB)_BM, (SMB)_OP, (SMB)_Inv` then `SMB = ⅓(...)`.
**Prereqs**: 3-factor model (above), factor-style regression, gross-profit margins, asset growth-accounting, portfolio construction.
### Section 16 — Capstone Project
Files: `Section 16 - Capstone Project/2 - Problem Statement.pdf` • templates `4 - QPMCapstoneTemplate.zip` • solution `6 - QPMCapstoneSolution.zip`
- **Goal**: apply Modern Portfolio Theory end-to-end to a **multi-asset** portfolio.
- **Steps**
 1. **Price data**: gather any number of assets; sample data = 3 assets.
 2. **Random portfolios w/ different weights**: generate random weight vectors for multi-asset portfolio; compute and store portfolio metrics.
 3. **Identify max-return/risk & min-risk**: pick portfolios with min risk and max Sharpe (returns/risk).
 4. **Plot the Efficient Frontier** and print optimal weights.
- Deliverable: template notebook with helper fx (data reading, plotting); solution notebook present.
**Prereqs**: all sections 3–11 (MPT, efficient frontier, basic portfolio metrics, data reading & plotting).
### Section 17 — Summary / Course Recap
Files: `Section 17 - Summary/2 - QPMResources.zip` (all course notebooks + data packed)
- Notebook recap across topics: **Basic Portfolio Construction**, **Beta of an Asset** (regression vs variance-covariance), **MPT**, **Kelly Criterion**, **Risk Parity**, **Fama-French (expected returns)**, **Multi-Factor Model** (Momentum factor, Short-Term Reversal factor), **Portfolio Performance & annualized measures** (Sharpe, Sortino, Treynor, Beta, Information ratio, skewness, kurtosis, max drawdown, monthly-returns heatmap, cumulative vs S&P500).
- Consolidates the entire course into reusable functions and summary analyses.
**Prereqs**: everything above; performance-measure calculus, time-series plotting metrics.
## Course Prerequisite Map
- **Statistical / matrix literacy** → covariance & variance → Σ (weighted) returns & portfolio std dev → **MPT efficient frontier**.
- **MPT** → returns formula reused in **Kelly portfolio** derivation → log-optimal sizing.
- **MPT / covariance** → each stock contributes to total risk → derive risk-parity weight → **Risk Parity** (library-based solution).
- **CAPM(beta, risk-free premium)** → **Fama-French 3-factor** (apply size/value) → **Fama-French 5-factor** (add profitability/investment factors).
- **All optimization & factor results** → **Capstone application** on multi-asset portfolios.
- D-overlap with sibling track topics: beta regression, factor modeling, Sharpe/Sortino analytics all recur in continuous courses (Track 1 Quant methods, Track 4 ML). Course-specific distinctness: REER/value weighting (Track 6), position sizing via Kelly/risk-parity (Track 7) — mechanisms unique to this track.