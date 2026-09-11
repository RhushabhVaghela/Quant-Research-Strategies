# Decision Trees in Trading — Concept Inventory
**Totals:** 6 modules, 12 notebooks
Supervised learning applied to trading: building tree-based models (regression and classification trees) that extract trading rules from price data, then layering in ensemble methods (bagging, random subspace, random forest, boosting) to control overfitting, followed by model evaluation (cross-validation, hyperparameter tuning) and a live-trading simulation with model retraining.
---
## Module: Regression Trees
**Notebooks:** `Regression Tree Model.ipynb`, `Strategy Analytics.ipynb`
### Prerequisites to this module
- OHLV / adjusted close price data (Open, High, Low, Close, Volume, adjusted prices)
- One-day / multi-day returns (percent change) and rolling standard deviation as features
- Concept of a target variable forecast one day ahead (shifted future return)
- Train/test split of time-series data
- **Regression trees** — a supervised model that auto-selects important predictors and splits data into leaves, each leaf predicting a value (expected return) used to define trading rules
- Strategy performance metrics: **Sharpe ratio** and **CAGR** (compounded annual growth rate)
### Concepts
- **Predictor engineering from OHLCV:** rolling returns (ret1, ret5, ret10, ret20, ret40 via `pct_change()` + `rolling().sum()`) and rolling standard deviations (std5, std10, std20, std40) as input features; volume as an additional predictor.
- **Target: one-day future return** — `retFut1 = ret1.shift(-1)` forecasts the next day's return.
- **Train/test split:** first 80% train, last 20% test to validate on unseen data while preserving temporal order.
- **Regression tree model (`DecisionTreeRegressor`):** `min_samples_leaf=400` to avoid overfitting (leaf should not be too small); `fit()` on train.
- **Tree visualization:** `sklearn.tree.export_graphviz` + graphviz to inspect splits, feature importance, and leaf expected values.
- **Trading rule from single leaf:** pick the leaf with the highest expected return and map its split conditions (e.g., `ret5 > 0.0014 AND std5 > 0.0155` ⇒ buy/1 else hold/0).
- **Trading rule from full tree:** use **all** leaves — predict expected return for every point (`dtr.predict(X) > 0` ⇒ +1 buy, else −1 sell) and multiply future returns by signal for strategy returns.
- **Performance evaluation:** annualized Sharpe ratio (`sqrt(252) * mean/std` of excess returns over risk-free ~5% p.a. / 252) and CAGR (`(cumprod)^(252/days) − 1`).
- **Comparison:** single-leaf vs full-tree rules on train and test; cumulative return plots.
### Pre-requisite concepts
Decision trees; returns and rolling statistics; supervised regression; Sharpe ratio; CAGR; train/test split.
---
## Module 2: Classification Model
**Notebooks:** `Classification Decision Tree Model.ipynb`, `Class Weights In Decision Trees.ipynb`
### Prerequisites to include classification
- **Classification trees** — predict a discrete label (direction of next-day return) instead of a continuous value
- **Technical indicators** via TA-Lib: **ADX** (Average Directional Index), **RSI** (Relative Strength Index), **SMA** (Simple Moving Average)
- **Labeling returns** into classes (binary 0/1, or multi-class buckets)
- **Gini impurity** as the split criterion
- **Class imbalance** and re-weighting
### Concepts (Classification Decision Tree Model.ipynb)
- **Classification tree setup:** `DecisionTreeClassifier(criterion='gini', max_depth=3, min_samples_leaf=5)` predicting binary next-day direction.
- **Feature set:** ADX, RSI, SMA (14- and 20-period windows) from TA-Lib.
- **Binary target labeling:** `np.where(Return > 0, 1, 0)` — 1 for positive next-day return, 0 otherwise.
- **Split & train/test:** 80/20 split; fit on train.
- **Visualizing the tree:** each node shows split feature, gini value, `samples`, and per-class `value` counts; a leaf path (e.g., RSI ≤ 55.868, SMA bands) yields a pure node usable as a long (buy) rule.
- **Predictions:** `clf.predict(X_test)`.
- **Classification metrics:** precision, recall, F1-score, support from `classification_report`; F1 is harmonic mean of precision & recall; values above ~0.5 considered good.
- **Backtest strategy:** multiply lagged signal by close `pct_change()` for strategy returns; plot cumulative product for out-of-sample performance.
### Concepts (Class Weights In Decision Trees.ipynb)
- **Class imbalance problem:** when one class dominates, the tree maximizes accuracy on common labels and ignores rare/important classes.
- **Multi-class labeling:** `returns_to_class()` buckets returns by range (≤0 → 0; 0–0.02 → 1; 0.02–0.03 → 2; else 3) creating a skewed distribution.
- **Unweighted model baseline:** `classification_report` shows near-zero precision/recall on underrepresented classes (2, 3).
- **Class weight rebalancing:** `class_weight='balanced'` re-weights so classes appear with equal frequency, trading overall accuracy for better coverage of rare classes; note the tradeoff (a previously good model may look worse overall).
### Prebuiltin concepts
Decision trees; classification; technical indicators (RSI, SMA, ADX); labeling; class imbalance / imbalanced data; precision/recall/F1.
---
## Module: Cross Validation and Hyperparameter Tuning
**Notebooks:** `K-Fold Cross Validation.ipynb`, `Hyperparameter Tuning.ipynb`
### Prerequisites
- **Random forest** model
- **Cross-validation** — estimate performance from multiple train-validation splits
- **Hyperparameters** — model settings set before training (cannot be learned)
- **Grid / random search** over hyperparameter space
### Concepts (K-Fold Cross Validation.ipynb)
- **Cross-validation rationale:** evaluate model on multiple train/validation splits for a more reliable performance estimate than a single split.
- **KFold** (`sklearn.model_selection`): `n_splits` (number of folds, ≥2) and `shuffle` (pre-shuffle ordering); splits data into k consecutive train/test sets.
- **cross_val_score:** accepts estimator, X, y, cv; returns an array of per-fold scores (e.g., 5 accuracy scores for a random forest classifier).
- **Summarizing:** mean ± standard deviation of fold scores as the model's robustness measure (e.g., "Accuracy: 53.14% ± 1.95%").
### Concepts (Hyperparameter Tuning.ipynb)
- **Hyperparameters of a random forest:** `n_estimators`, `max_features`, `max_depth`, `min_samples_leaf`, `bootstrap`.
- **Parameter grid:** dictionary of hyperparameter names → value ranges (n_estimators 10–20; max_features 0.3–1.0; max_depth 2–10; min_samples_leaf 300–600; bootstrap True/False).
- **RandomizedSearchCV:** samples `n_iter` parameter combinations at random, tuned with CV; `.best_params_`, `.best_estimator_`.
- **GridSearchCV:** exhaustively tries all combinations (more thorough but slower); `.best_params_`.
- **Bias/variance tradeoff:** smaller `max_features` reduces variance (overfit) but increases bias (underfit); larger `n_estimators` improves until a critical point.
### Prebuiltins
Ensembles (random forest); cross-validation; hyperparameter optimization; bias-variance tradeoff.
---
## Module: Parallel Ensemble Methods
**Notebooks:** `Bagging Model.ipynb`, `Random Subspace Model.ipynb`, `Random Forest Model.ipynb`
### Prerequisites
- **Ensembles** — combine multiple models to reduce variance/overfitting
- **Regression trees** as the base estimator
- **Bootstrap sampling** (with replacement)
### Concepts
- **Bagging (Bootstrap Aggregating):** create 'N' random subsets **with replacement** from training data, fit one model per subset, and combine by averaging (regression) or majority voting (classification); reduce variance/overfit of a single tree. Implemented with `BaggingRegressor(estimator=DecisionTreeRegressor, n_estimators, random_state=)return`.
- **Random Subspace (attribute/feature bagging):** sample the **predictors** (with replacement) instead of the data rows; via `BaggingRegressor(bootstrap=False, bootstrap_features=True, max_features=0.7)` — offers diversity across feature subsets.
- **Random Forest:** hybrid of bagging + random subspace — bootstrap-sample rows **and** randomly select a predictor subset at each split; average or majority-vote all trees. `RandomForestRegressor(n_estimators=20, bootstrap=True, max_features=0.6, min_samples_leaf=400, random_state=42)`.
- **Parameter intuition:** `n_estimators` (higher = better up to a critical point), `max_features` (smaller reduces variance but risks bias), `min_samples_leaf` guards against tiny leaves/overfit.
### Prebuiltins
Ensembles; bagging; random subspace; random forests; bias–variance.
---
## Sequential Ensemble Modules (Boosting)
**Notebooks:** `AdaBoosting Model.ipynb`, `Gradient Boosting Model.ipynb`
### Prerequisites (Boosting)
- **Boosting** / sequential ensembles — models added sequentially that each correct the previous model's mistakes
- **Adaptive Boosting** (AdaBoost, Freund & Schapire 1996)
- **Gradient boosting** (Friedman) — additive models following gradient descent on loss
### Concepts
- **AdaBoost naming & idea:** adaptive; builds a sequence where each model improves its predecessor; add models until all train data are correct or a max model count is reached.
- **AdaBoostRegressor** implementation: `AdaBoostRegressor(estimator=DecisionTreeRegressor(min_samples_leaf=400), n_estimators=4, random_state=42)`.
- **Gradient Boosting:** extension of AdaBoost by Friedman; each added model reduces the loss, following gradient descent on the residual.
- **GradientBoostingRegressor:** `GradientBoostingRegressor(n_estimators=4, random_state=42)`.
- **Comparison practice:** import data, define features/target, train/test split, compute strategy returns, compare across all models.
### Covered outcome
Boosting sequential ensembles reduce overfit so that **all leaves** can be used for prediction (contrast with single-tree full-leaves fear of overfit).
---
## Module: Challenges in Live Trading
**Notebook:** `Trading Simulation Using Decision Trees.ipynb`
### Prerequisites
- **Random forest classifier** (balanced class weights)
- **Feature generation** from OHLCV returns/rolling stats
- **Model persistence:** pickle save/load
- **Simulation / walk-forward trading** — point-by-point, rolling re-fit of the model, monitoring performance
- **Data leakage avoidance** — never let future data leak into features
### Concepts
- **Data & libraries:** BAC.csv daily data; pandas, sklearn RandomForestClassifier, pickle, accuracy_score, matplotlib.
- **Feature generation as a function:** `create_features(data)` builds return (ret1/3/5/10/20) and rolling std (std3/5/10/20) features, drops NaNs, constructs future returns `retFut1`, and returns predictor matrix X and target y (class 1/−1 for up/down).
- **Simulation parameters:** `simulation_length` (trading horizon), `minimum_feature_length` (rows needed to form a full feature row), `performance_length` (rows over which past performance is checked).
- **Train/simulation split:** reserve enough prior rows so features and performance checks are free of data leakage.
- **Train, save, load, retrain functions:** `train_model(X,y)` returns an `RandomForestClassifier(n_estimators=200, class_weight='balanced')`; `save_model` / `load_model` via pickle (model_save.pkl); `create_new_model` reuses feature + trainTransform + save.
- **Walk-forward simulation loop:** for each iteration, load past window; compute features; load model; predict; check rolling accuracy over `performance_length` (threshold ~0.55), then
 - good performance → use today's "Buy"/"Sell" signal;
 - poor performance → do NOT trade (append 0), roll the train set forward and **retrain** (create_new_model).
- **Simulated performance:** multiply signals by future returns; plot cumulative product (`np.nancumprod`) to view P&L.
### Prebuiltins
Random forests; classification; feature engineering; cross-validation; simulation; model persistence.
---
## Cross-cutting prerequisite links (recommendations)
- Before **Regression Trees**: OHLCV data, returns/rolling std, Sharpe/CAGR.
- Before **Classification**: regression-trees module; technical indicators; labeling of direction.
- Before **Class Weights**: classification, unbalanced data, classification metrics.
- Before **Cross Validation / Tuning**: random forest.
- Before **Ensiebles**: regression trees, overfitting.
- Before **Boosting**: ensembles, overfitting via all-leaves rule.
- Before **Live Trading**: all tree + ensemble + tuning concepts and pickle persistence.
---
## Decision-Trees-in-Trading — Section-based course structure
# — Decision Trees in Trading — Concept Inventory
**Track:** 4 — Machine Learning & Deep Learning in Trading (Beginners)
**Media note:** PDFs + a downloadable code zip only (no mp4s in this course folder).
**Overlap with D: notebooks:** The D: side has notebook-based decision-tree content (splitting criteria, tree visualisation, hyperparameter search in `.ipynb`); here the PDFs supply the underlying loss functions, ensemble math, and installation/verification steps.
## COURSE
Building decision-tree models for trading: how trees partition feature space via splitting, stopping and pruning; training classification trees; combining trees sequentially into ensembles (boosting, specifically AdaBoost); and tuning/generalising trees via cross-validation and hyperparameter selection.
## Course Prerequisite Map
- **Section 2 requires:** basics of supervised classification/regression, overfitting bias-variance intuition.
- **Section 3 requires:** slicing/decision-tree logic + a Python environment for tree visualisation.
- **Section 8 requires:** Section 2 (weighted splitting) + idea that a tree can be fit on a weighted random subsample (bootstrapping/boosting intuition).
- **Section 9 requires:** Sections 2 & 3 (a trained tree + a labelled dataset to fold/split). Prereqs for Section 9 also intersect with metrics (gini/entropy, confusion matrix) used to score CV folds.
---
### Section 2 — Splitting, Stopping and Pruning Methods
- **CONCEPT:** Loss function — a metric evaluating how well a trained ML algorithm generalises to unseen data; small loss = viable model, and it drives fine-tuning of model. prereqs: ML train/test split, supervised learning.
- **CONCEPT:** Tree splitting loss for classification — **gini impurity** and **entropy** (both distribution-purity measures) chosen as split criteria for classification trees. prereqs: probability/distribution basics, tree structure.
- **CONCEPT:** Tree-splitting loss for regression — **mean squared error (MSE)** and **mean absolute error (MAE)** as node-impurity/cost criteria for regression trees; custom loss functions also possible. prereqs: regression error metrics, node prediction.
- **CONCEPT:** Splitting — recursively choosing the feature split that most reduces impurity/loss at each node. prereqs: loss functions above.
- **CONCEPT:** Stopping/pruning — early depth/leaf thresholds or post-hoc pruning to prevent overfitting (too-deep trees memorising noise). prereqs: bias-variance trade-off, overfitting.
### Section 3 — Classification Model
- **CONCEPT:** Classification decision-tree model — recursively partitioned data into pure classes; predictions produced by following splits to a leaf (majority/class confidence). Built on the gini/entropy criteria from Section 2. prereqs: Section 2, classification labels.
- **CONCEPT:** Visualising the tree in Python — `pip install graphviz` (fallback `pip install python-graphviz`) and `pydot` to render the trained tree; alternative planners packages (Box3d, Gephi). Gives sharers introspective clarity on the final tree structure. prereqs: a trained model, Python env.
### Section 8 — Sequential Ensemble Methods
- **CONCEPT:** Sequential/boosting ensembles — combine sheaves of weak tree learners sequentially, each new tree corrects the mistakes of previous ones; AdaBoost is the canonical example. prereqs: decision tree, weighted-sample sampling.
- **CONCEPT:** AdaBoost math — (1) initialise all n training items with equal weight W_i = 1/n; (2) draw a random subsets with replacement (sample weights = selection probabilities); (3) fit a weak tree on that subset; (4) re-raise weights of misclassified items (formula doubles down on errors) so the next learner focuses on them, improving the ensemble over iterations. prereqs: sampling with replacement, weighted loss, sequential fitting.
- **CONCEPT:** Ensemble learning is a foundation concept progressively feeding into gradient boosting models used in gradient-boosting/DNN trading strategies later. prereqs: Section 2 splitting/entropy + Section 3 classification.
### Section 9 — Cross Validation and Hyperparameter Tuning
- **CONCEPT:** Cross-validation (k-fold) — splitting the dataset into k folds, training k times (each fold held out once) and averaging performance → robust generalisation estimates of a trading model. prereqs: evaluation metrics, data partitioning, confusion matrix (to threshold misclassification).
- **CONCEPT:** x-tables/hyperparameter tuning — selecting tree depth, min-split, max-features, etc. using CV score as the selection signal rather than a single train/test split. prereqs: Section 8 (ensemble) + Section 2 loss.
- **CONCEPT:** Confusion matrix helps judge a CV-selected classifier beyond accuracy (TPR/FPR, precision for trading). prereqs: Section 2, prediction outputs.
### Section 12 — Downloadable Code
- **CONCEPT:** Course code/resources (`DTResources.zip`) — the decision-tree notebook(s) and data for reproducing the splitting/ensemble/CV workflow locally. prereqs: all prior sections.