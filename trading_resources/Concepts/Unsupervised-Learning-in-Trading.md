# Unsupervised Learning in Trading — Concept Inventory
**Totals:** 14 modules, 17 notebooks + 2 support Python modules
End-to-end unsupervised learning workflow for trading: covariance/PCA fundamentals → feature selection (stationarity, correlation) → scaling (min-max vs standard) → k-means clustering + choosing cluster count → cluster analysis for signal generation (hit ratio, skewness) → DBSCAN (density-based, outlier-robust) → pairs trading (feature engineering, DBSCAN pairs, cointegration test) → compiled "putting it all together" + a capstone project.
---
## Module: Introduction to Principal Component Analysis
**Notebook:** `Variance and Covariance.ipynb`
### Prerequisites
- Basic statistics; mean, standard deviation
- **PCA** (conceptual) — finds the "best" line maximizing the spread of points
### Concepts
- **Variance (σ²):** how far values are from the mean: `Σ(xᵢ − x̄)² / (n−1)`; squaring gives equal weight to points above/below the mean and more weight to farther points.
- **Covariance:** direction of co-movement of two features; positive when they move together, negative otherwise: `Σ(xᵢ − x̄)(yᵢ − ȳ) / (n−1)`.
- **Covariance matrix (via pandas `.cov(ddof=1)`):** a square matrix where **diagonal = variances**, **off-diagonal = covariances**; shape n×n for n columns. This is the core object PCA is built on.
- Read RSI/ADX data to compute variance, covariance and the covariance matrix as a foundation for eigenvalues/eigenvectors.
---
## Module: Maths Behind Principal Component Analysis
**Notebooks:** `Maths Behind PCA.ipynb`, `PCA Example.ipynb`
### Prerequisites
- Variance and covariance
- **Eigenvalues and eigenvectors** — of the covariance matrix
- **PCA** — unsupervised dimensionality reduction
### Concepts (Maths Behind PCA.ipynb)
- **PCA as dimension reduction:** projects data onto directions (components) that maximize variance.
- **Eigen-decomposition:** `numpy.linalg.eig(cov_matrix)` returns eigenvalues and eigenvectors; the eigenvector of the **largest eigenvalue** is the **first principal component**.
- **Orthogonality:** principal components are perpendicular; spread is largest along PC1.
- **De-meaning:** subtract the mean so eigenvectors pass through the origin; project de-meaned data onto PC1 via dot product.
- **1D reduction:** `data_shifted.dot(pc1)` collapses data onto one axis.
- **sklearn implementation:** `PCA().fit(data)`, `.components_` (eigenvectors), `.explained_variance_` (eigenvalues), `.fit_transform(data)`; the sign of eigenvectors is arbitrary — magnitude (variance captured) is what matters.
- **3D→2D example** (PCA Example.ipynb): generate 100 3-D points with noise+rotation; `PCA(n_components=2)`; verify reduced shape (100,2) retains the data's structure (semi-circular distribution), showing PCA keeps information while lowering dimension.
---
## Module: Principal Component Analysis (choosing features)
**Notebook:** `Choosing the Number of Features in PCA.ipynb`
### Prerequisites
- PCA mechanics and eigenvalues/eigenvectors
- Explained variance ratio
### Concepts
- **Returns data for 473 stocks** (365 trading days), transposed to date×stock returns matrix.
- **explained_variance_ratio_:** proportion of total variance explained by each principal component (e.g., PC1 ≈ 0.443).
- **Selecting components by cumulative variance:** plot cumulative `explained_variance_ratio_` vs number of features; pick the number achieving a target (e.g., 90%) — here ~81 of 473 features.
- **n_components shortcut:** if `n_components` is between 0 and 1 it is read as proportion of variance; if an integer >1 it is the number of components — both routes give the same result (81).
- **Takeaway:** 473-dimensional data reduced to 81 dimensions at 90% explained variance.
---
## Module: Feature Selection (for k-means)
**Notebook:** `Feature Selection.ipynb`
### Prerequisites
- **Stationarity** of a time series
- **Correlation** between features
- **k-means** requirements for input features
### Concepts
- **Why feature selection for clustering:** k-means inputs must be **stationary** (value not dependent on time) and **not highly correlated** (correlated features overweight a common signal).
- **Features produced from 15-minute Apple data:** 3.75-hour return, 14-day return, 1-day SMA, 1-day & 14-day volatility, RSI, ADX, ATR.
- **Stationarity test:** **ADF test** (`statsmodels.tsa.stattools.adfuller`); p-value < 0.05 ⇒ stationary; non-stationary features (SMA, Volatility14) are dropped.
- **Correlation check:** absolute correlation matrix; drop any feature pair with |corr| > 0.7 (ATR correlative with Volatility) — remove ATR to keep the most features.
- **Outcome:** a clean stationary, low-correlation feature set (ret375_hours, ret14_days, Volatility, RSI, ADX) for k-means.
---
## Module: Scaling the Data
**Notebook:** `Scaling the Data.ipynb`
### Prerequisites
- k-means sensitivity to feature scale
- RSI/volatility features of different ranges
### Concepts
- **Why scaling:** with un-scaled features of different ranges (RSI 0–100 vs volatility 0–1.4) k-means effectively ignores the smaller-range feature; distance to centroid is dominated by scale.
- **Min-max scaling:** `x_scaled = (x − x_min)/(x_max − x_min)` → range 0–1, via `sklearn.preprocessing.MinMaxScaler`.
- **Standard scaling:** `x_scaled = (x − μ)/σ` → mean 0, std 1, via `StandardScaler`; assumes normality; range is not fixed.
- **Tradeoff:** StandardScaler can still overweight features with extreme tails; MinMaxScaler is preferred when the feature range is known (RSI) or estimable (volatility) — the course uses **MinMaxScaler** going forward.
---
## Module: K-Means for Financial Data
**Notebook:** `Applying K-Means to Create Clusters.ipynb`
### Prerequisites
- **k-means** algorithm (centroids, iterative reassignment)
- Technical indicators: **RSI**, **ADX**, **volatility**
### Concepts
- **Feature computation with TA-Lib:** RSI (`ta.RSI`), ADX (`ta.ADX`), and volatility from rolling std of returns; for 15-min data the 1-day period = 6.5×4 ≈ 26 periods.
- **k-means model:** `sklearn.cluster.KMeans(n_clusters, random_state)`; fit on features (RSI+ADX); access centroids via `model.cluster_centers_`.
- **Assigning points:** `model.predict(features)` gives cluster labels; scatter plot with centroids shows cluster structure.
- **Reusable function `plot_kmeans_clusters`:** fits k-means and plots clusters for 2 features (used across later modules).
- **Observation that motivates scaling:** RSI+volatility clusters look distorted because of scale mismatch — leads into the scaling module.
---
## Module: Selecting Clusters for K-Means
**Notebook:** `Choosing the Number of Clusters.ipynb`
### Prerequisites
- k-means (needs pre-chosen `n_clusters`)
- WCSS / inertia concept
- Min-max scaled features
### Concepts
- **WCSS / inertia:** within-cluster sum of squares; `KMeans.inertia_`.
- **Elbow curve:** plot WCSS vs number of clusters (1–30); WCSS declines monotonically.
- **Change in WCSS plot:** find where the reduction flattens/becomes ~constant (here ~10–12).
- **Percentage-change rule:** choose the number of clusters where % change in WCSS drops below a threshold (here 4.5%) → ~11 clusters; implementable in `get_number_of_clusters(features, threshold, max_range)` (takes WCSS and threshold).
---
## Module: Analysing Clusters (Hit Ratio & Skewness)
**Notebooks:** `Cluster Analysis with Hit Ratio.ipynb`, `Strategy Analytics for Hit Ratio.ipynb`, `Cluster Analysis with Skewness.ipynb`
### Prerequisites
- k-means clustering output (train/test cluster labels)
- Future-return labeling and train/test split
- **Hit ratio** and **skewness** metrics; backtesting metrics
### Concepts (Cluster Analysis with Hit Ratio.ipynb)
- Feature pipeline: `calculate_features()` (ret375_hours, ret14_days, Volatility, Volatility14, RSI, ADX, ATR) + 15-period future returns (`fut_ret`); drop SMA & ATR.
- 75/25 train/test split; fit MinMaxScaler on train, transform both.
- Fit k-means (11 clusters) on train; assign cluster labels to test via `predict`.
- **Hit-ratio signal rule:** per cluster, compute % positive and % negative future returns; long if positive ≥55%, short if negative ≥55%, else neutral; map direction to test rows.
- **Backtest:** strategy returns = `close.pct_change() × direction.shift(1)`; cumulative returns; metrics: total returns, annualized (CAGR), max drawdown (MDD), return-to-MDD ratio via `performance_analysis()`.
- **Result:** hit-ratio strategy on Apple underperforms buy-and-hold.
### Concepts (Strategy Analytics for Hit Ratio.ipynb)
- Trade-wise log generation: `get_trades(data, close_column, signal_column)` — columns Position, Entry Time, Entry Price, Exit Time, Exit Price, PnL (PnL = Δprice × position).
- **Strategy analytics:** `get_analytics(trades)` → #long/#short/total trades, gross profit/loss, net profit, winners/losers, win %/loss %, avg profit/loss per trade.
- **pyfolio tear sheet:** `pf.create_simple_tear_sheet(strategy_returns, benchmark_rets)` for detailed trade metrics.
### Concepts (Cluster Analysis with Skewness.ipynb)
- **Skewness** of future-return distributions: histogram per cluster; negative skew = left tail, positive skew = right tail (fat tails).
- **Interpretation scale:** symmetric −0.5…0.5; moderate ±(0.5–1); high <−1 or >1.
- **Skewness signal rule:** long clusters with skewness > 1, short clusters with skewness < −1, else neutral.
- **Result:** skewness-based strategy on Apple outperforms buy-and-hold (total ~77%, return-to-MDD ~6.2) — capturing tail events works well.
---
## Module: Putting It All Together (k-means strategy)
**Notebook:** `Putting It All Together.ipynb`
### Prerequisites
### Concepts
- Reuses the module helpers: `performance_analysis, calculate_features, stationary, get_number_of_clusters, hit_ratio_analysis, skewness_analysis, get_trades, get_analytics`.
- **Full pipeline from scratch on Apple:** read 15-min data → compute features → check stationarity (drop SMA) → correlation check (drop ATR) → 75/25 split → MinMax scaling → elbow/threshold cluster count → fit k-means → `hit_ratio_analysis` and `skewness_analysis` add `direction_hit_ratio` / `direction_skewness` columns → compute & plot cumulative returns.
- **Comparison:** hit-ratio strategy poor (negative returns); skewness strategy strong (total ~56%, return-to-MDD ~4.1) — template for creating trading signals from k-means on any asset.
---
## Module: DBSCAN
**Notebook:** `K-Means Vs DBSCAN.ipynb`
### Prerequisites
- k-means (spherical clusters, pre-set clusters count)
- **DBSCAN** (density-based clustering)
### Concepts
- **DBSCAN (Density-Based Spatial Clustering of Applications with Noise):** density-based; robust to noise/outliers; separates regions of high density from low density; doesn't need a pre-defined `n_clusters`.
- **Hyperparameters:** `eps` (max distance for neighborhood) and `min_samples` (min points to consider a cluster dense); noise points given label `-1`.
- **sklearn:** `sklearn.cluster.DBSCAN(eps, min_samples).fit(data)`; `.labels_`.
- **When DBSCAN beats k-means:** non-globular/irregular clusters; varying densities; outlier detection (outliers get −1); noisy data. Both have strengths; choice depends on the problem.
---
## Module: Application of Unsupervised Learning for Pairs Trading
**Notebook:** `Feature Engineering for Pairs Trading.ipynb`
### Prerequisites
- PCA & variance selection; StandardScaler; fundamentals data
### Concepts
- **Pairs selection goal:** use unsupervised clustering to find similar stocks (e.g., same-sector banks) for pairs trading.
- **Read 473 S&P 500 returns** (`SP_500_data.csv`), `.pct_change()`.
- **Standardize returns** with `StandardScaler` so stocks are comparable.
- **PCA reduction:** reduce to the components explaining 90% variance (→ 78 components).
- **Combine fundamentals:** append `profitMargins`, `revenueGrowth`, `returnOnEquity` from `fundamentals.csv` (→ 78 + 3 = 81 features).
- **Re-standardize the combined matrix** so PC features and fundamentals are comparable; export as `SP500_principal_components.csv`.
---
## Module: Pairs Trading using Clustering Algorithms
**Notebooks:** `Create Pairs using DBSCAN.ipynb`, `Cointegration Test.ipynb`
### Prerequisites
- DBSCAN; PCA-reduced + fundamental features; t-SNE visualization; **cointegration** and ADF test
### Concepts (Create Pairs using DBSCAN.ipynb)
- DBSCAN on the 81-feature matrix (`eps=5, min_samples=3`) → 9 clusters; stocks with label −1 are noise (excluded).
- **Clusters as similarity groups:** stocks in the same cluster are similar (e.g., cluster 5 = BAC, JPM, PNC, USB — banks) and likely to form good pairs.
- **t-SNE visualization:** `sklearn.manifold.TSNE(n_components=2, learning_rate, perplexity, random_state)` reduces 81-D to 2-D to visualize clusters; grey points = noise.
- **Pair creation:** within each cluster, `itertools.combinations(cluster_stocks, 2)` → nC2 pairs; cluster sizes determine pair counts.
### Concepts (Cointegration Test.ipynb)
- **Cointegration:** two non-stationary series whose linear portfolio is stationary (even if each alone wanders) — required for mean-reversion/pairs trading.
- **Hedge ratio via OLS:** `sm.OLS(stock1, stock2)` to build portfolio = stock1 − hedge×stock2.
- **ADF test** on the portfolio, null = not stationary; reject (test stat < critical value at 10%) ⇒ cointegrated.
- **`is_coint(pair)` function:** returns True/False per pair; applied across all DBSCAN pairs; at 90% confidence ~55 cointegrated pairs selected for pairs trading.
---
## Module: Capstone Project
**Notebook:** `Capstone Project Model Solution.ipynb`
### Prerequisites
- Everything in the course; `unsup_capstone_util.py` helpers (`check_stationarity, correlation_check, get_number_of_clusters, performance_analysis`)
### Concepts
- **Reference solution template** on daily GOOG (2011–2021): train 2011–2017, backtest 2018–2021.
- **Feature set:** 5-day returns, 20-day SMA, 14/50-day volatility, RSI, ADX, ATR, Williams %R (`TA-lib`).
- **Feature engineering checks:** stationarity (drop non-stationary SMA, ATR) → correlation (drop WILLR, correlated with returns/RSI) → MinMax scaling on train, transformed test.
- **Clustering:** `get_number_of_clusters` (elbow/threshold) → k-means fit on train; label train/test observations.
- **Cluster analysis:** 5-day future returns; histogram per cluster; observe skewness.
- **Trading strategy rules:** long if skewness > 0.5, mean return > 0, and trades ≥ 22; short if skewness < −0.5, mean return < 0, and trades ≥ 22; else neutral. Trade daily based on previous day's cluster prediction.
- **Performance:** `performance_analysis` vs buy-and-hold — total return, CAGR, max drawdown, return-to-MDD.
---
## Support Python Modules (data_modules)
- **`unsup_capstone_util.py`:** `check_stationarity`, `correlation_check`, `get_number_of_clusters`, `performance_analysis` — helpers for the capstone solution.
## Cross-cutting prerequisite lenses
- **PCA prerequisite chain:** variance/covariance → eigenvalues/eigenvectors/maths → PCA example → choosing number of features.
- **Clustering prerequisite chain:** feature selection (stationarity+correlation) → scaling → k-means → choosing clusters → cluster analysis (hit ratio/skewness).
- **Pairs prerequisite chain:** PCA+fundamentals feature engineering → DBSCAN clustering/pairs → cointegration test.
- **Supported by** custom utility modules (data_modules) used throughout.
---
## Unsupervised-Learning-in-Trading — Section-based course structure
# — Unsupervised Learning in Trading — Concept Inventory
**Track:** 5 — Artificial Intelligence in Trading (Advanced)
**Media note:** PDFs only (no mp4s).
**Overlap with D: notebooks:** significant — the D: side carries notebook-based `Unsupervised-Learning-in-Trading` extraction covering k-means on financial data, feature scaling/selection, hit-ratio/skewness cluster analysis, PCA and pairs trading in `.ipynb` form. This course mirrors it and adds the maths/parameter PDFs (k-means, PCA math, DBSCAN parameter selection, pairs-trading/clustering, capstone).
---
## COURSE
Unsupervised learning to discover structure in financial data and trade it: **k-means clustering** for grouping stocks into regimes (with data scaling, feature selection, and choosing the number of clusters via elbow/kurtosis), **evaluating** clusters by hit-ratio and skewness, **principal component analysis (PCA)** for dimensionality reduction (from curse-of-dimensionality rationale through to eigenvalue/eigenvector maths and application), **DBSCAN** (density-based clustering) as a non-k alternative, and pairs-trading / statistical-arbitrage built from mean-reverting cointegrated pairs identified via clustering — closing with an IBridgePy automated strategy and a capstone.
## Course Prerequisite Map
- **Section 4 K-Means requires:** distance/Euclidean measurements + centroid concepts.
- **Section 5 K-Means for financial data requires:** Section 4 + technical indicators (RSI, ADX from prerequisites).
- **Section 6 Scaling the Data requires:** Sections 4–5 (features differing in scale break clustering).
- **Section 7 Feature Selection requires:** Section 5/6 + stationarity (ADF test), correlation.
- **Section 8 Selecting Clusters requires:** Section 4 (inertia) + elbow-curve logic.
- **Section 9 Hit Ratio requires:** Section 8 (a labelled cluster mapping) + backtesting.
- **Section 10 Skewness requires:** Section 9 (cluster distributions) + moment stats (skew/kurtosis).
- **Section 11 Putting It All Together requires:** Sections 4–10 (parse the full k-means strategy).
- **Section 12 Curse of Dimensionality requires:** SQL / high-dimensional space intuition.
- **Section 13 PCA Intro requires:** Section 12 + dimensional reduction need.
- **Section 14 Maths Behind PCA requires:** Section 13 + matrix multiply + eigenvector/eigenvalue.
- **Section 15 PCA requires:** Section 14 + choosing principal components (variance explained).
- **Section 16 Pairs Trading App requires:** Sections 4–15 (clustering) + cointegration/mean-reversion.
- **Section 17 DBSCAN requires:** Section 4-16 clustering comparison + density logic.
- **Section 18 Pairs Trading using Clustering requires:** Sections 16 & 17 (identify cointegrated pairs via clustering) + Bollinger-bands pairs basier.
- **Section 20 Capstone requires:** all prior.
- **Section 21 Automate requires:** Section 18-capstone model + IBridgePy.
---
### Section 4 — K-Means Clustering
- **CONCEPT:** k-means algorithm — partition data into k clusters by iterative assignment to the nearest centroid; distances measured with **Euclidean distance** (plus standardised/weighted variants); centroid updates recomputed from cluster means; variations exist (efficiency vs computational strain). prereqs: distance geometry, averaging.
### Section 5 — K-Means for Financial Data
- **CONCEPT:** Apply k-means to stocks — cluster stocks on indicator features (RSI, ADX, etc.) to group similar behaviours; the DocRead also (review the RSI/ADX calculations) so clustering features are interpretable. prereqs: Section 4 + indicator/feature knowledge.
### Section 6 — Scaling the Data
- **CONCEPT:** Feature scaling — **min-max scaler** and **standard scaler** (and other techniques) so no single feature dominates the Euclidean distance used in clustering. prereqs: Sections 4–5.
### Section 7 — Feature Selection
- **CONCEPT:** Feature selection — select features that add signal: test **stationarity** (augmented Dickey-Fuller test), prune highly correlated/redundant features (similarity measure / max-information-compression index). prereqs: Sections 4–6 + statistics.
### Section 8 — Selecting Clusters for K-Means
- **CONCEPT:** Choosing the number of clusters k — **elbow curve** of inertia (within-cluster sum of squares): pick the k at the elbow; alternatives such as scaled-inertia heuristics. (1D data often needs kernel density estimators instead.) prereqs: Section 4 + inertia plot.
### Section 9 — Analysing Clusters: Hit Ratio
- **CONCEPT:** Hit ratio — fraction of instances in which the next-day return sign matches the cluster-implied direction; a backtester uses hit ratio to score cluster fidelity. prereqs: Section 8 + daily return/forward-return labels.
- **CONCEPT:** Backtesting the cluster-based strategy — walk-forward testing, performance metrics (Sharpe, Sortino), strategy validation in a notebook. prereqs: Section 9 + backtesting.
### Section 10 — Analysing Clusters: Skewness
- **CONCEPT:** Skewness & kurtosis of cluster-return distributions — skewness measures distribution symmetry; kurtosis measures tail risk (both applied to cluster-predicted returns vs benchmark S&P/Bitcoin tail-risk). prereqs: distribution moments, Section 9.
### Section 11 — Putting It All Together
- **CONCEPT:** The full k-means trading strategy — from OHLC data → indicator features → scale → reduce (PCA preview) → cluster → hit-ratio / skewness analysis → backtest a lower-timeframe strategy; papers applying k-means + regression / commodity cluster analysis inform this. prereqs: Sections 4–10.
### Section 12 — Curse of Dimensionality
- **CONCEPT:** Curse of dimensionality — as feature dimensions grow, data becomes sparse and distance measures break down; prefer fewer effective dimensions (same result with less). prereqs: high-dimensional geometry intuition.
### Section 13 — Introduction to Principal Component Analysis (PCA)
- **CONCEPT:** PCA — linear, unsupervised dimensionality reduction that projects data onto the directions of greatest variance using **variance and covariance** of features (mutual experience: two features, reduces to one while retaining variance). prereqs: Section 12 + feature covariance.
### Section 14 — Maths Behind Principal Component Analysis
- **CONCEPT:** Matrix multiply + eigenvalues/eigenvectors — PCA's principal components are the **eigenvectors of the covariance matrix** (with eigenvalue = variance explained) gained via linear algebra; you must be comfortable multiplying matrices and computing eigenvectors/eigenvalues. prereqs: Section 13 + matrix algebra.
### Section 15 — Principal Component Analysis (implementation)
- **CONCEPT:** Choose principal components — retain PCs by explained-variance ratio, cumulative variance, or other heuristics; uses log / linear returns as features; can build **eigen-portfolios** (weights from eigenvectors/eigenvalues). prereqs: Section 14 + covariance.
### Section 16 — Application of Unsupervised Learning for Pairs Trading
- **CONCEPT:** Pairs / statistical arbitrage trading — a **mean-reverting** time-series profile where you buy low/sell high; natural mean-reverting financial series a rare, so you **fabricate** one by combining two price series; clustering selects candidate pairs (cointegrated price series) — pairs spread from their combined mean-reverting. prereqs: Section 15 + cointegration.
### Section 17 — DBSCAN
- **CONCEPT:** DBSCAN — density-based clustering (clusters formed only where points are dense; noise tolerated) — vs k-means; **parameters**: **minPts** (≥2; rule of thumb ≥1 more than features, ~2× dimension for large sets) and **epsilon (eps) distance**. HDBSCAN = advanced variant. prereqs: clustering intuition + geometry.
### Section 18 — Pairs Trading using Clustering Algorithms
- **CONCEPT:** Select pairs via clustering — using the clusters (k-means/DBSCAN) to find cointegrated pairs for pairs trading; **correlation** and **cointegration** are the selection criterion; common trade approach via Bollinger bands on the spread. prereqs: Sections 16–17 + cointegration stats + Bollinger bands; TSNE visualisation for pre-cluster inspection.
### Section 20 — Capstone Project
- **CONCEPT:** Capstone: build an end-to-end unsupervised trading strategy — read your dataset (e.g. GOOG daily CSV), define/engineering features with sanity checks (correlation, stationarity), normalize, cluster select, evaluate, strategy; template/solutions zips. prereqs: entire course.
### Section 21 — Automate Trading Strategy Using IBridgePy
- **CONCEPT:** IBridgePy automation — deploy the k-means/live strategy through IBridgePy (`unsupkmeansliveibridgepy.zip`) into paper/live account flow. prereqs: Section 18 model + broker.
### Section 22 — Course Summary
- **CONCEPT:** Recap + resources (`UnsupervisedLearningResources.zip`). prereqs: entire course.