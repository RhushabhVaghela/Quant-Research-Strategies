# Introduction to Machine Learning for Trading — Concept Inventory
> Scope: supervised machine-learning classifiers/regressors for price-direction and return prediction on S&P 500 (SPY) data.
> Modules/notebooks enumerated: **7** | Data: `data/SPY.csv`, `data/BAC_2010_2021.csv` | Module files: `ReadMe.html`, `Folder Structure and How to Run Code Files.html`
---
## Module: Supervised Learning
### 1. `Linear Regression.ipynb`
Statistical/ML baseline for predicting a real-valued target from inputs.
**Concepts (with prerequisites):**
- **Linear regression model equation** — y = β₀ + β₁x₁ + β₂x₂ + … + ε; output is a weighted sum of inputs.
 - *Prereq:* basic algebra, equation of a line, what a coefficient/slope means.
- **Supervised learning framing** — model learns a mapping from inputs X to output y using labelled examples (X, y pairs).
 - *Prereq:* none.
- **Features (independent variables)** — input columns used to predict; here `prev_day_returns` (previous day's return) built via `pct_change()` and `shift()`.
 - *Prereq:* what a feature/predictor is; pandas column math.
- **Target (dependent variable)** — the outcome being predicted; here today's `return`.
 - *Prereq:* none.
- **Feature engineering from prices** — computing daily returns as `Close.pct_change()` and shifting to lag returns (prevents look-ahead bias).
 - *Prereq:* understanding of prices vs returns, time lags.
- **Train–test split (time-ordered)** — keeping chronological order and holding out the last 20% as test; no shuffling because of temporal data.
 - *Prereq:* why we need held-out data for honest evaluation.
- **Fitting a model** — `LinearRegression().fit(X_train, y_train)` learns coefficients; `predict(X_test)` gets predictions.
 - *Prereq:* what training/fitting means.
- **Regression metrics — Mean Squared Error (MSE)** — average of squared errors; larger = worse fit.
 - *Prereq:* concept of prediction error/residuals.
- **R² score (coefficient of determination)** — proportion of variance explained; 1.0 = perfect fit, ≤0 = worse than the mean. Here ~0.05, interpreted as underfitting.
 - *Prereq:* variance, correlation intuition.
- **Regression line visualisation** — plotting fitted line over data points.
 - *Prereq:* scatter plot reading.
### 2. `Random Forest.ipynb`
Ensemble of decision trees for classification (also regression).
**Concepts (with prerequisites):**
- **Random Forest (Random Decision Forest)** — ensemble method combining many decision trees; for classification each tree "votes" and majority wins; for regression outputs are averaged.
 - *Prereq:* what a decision tree is, majority voting, averaging.
- **Decision trees / CART model** — trees of decisions; single tree aggregated into the forest.
 - *Prereq:* none.
- **Bagging (bootstrap sampling)** — each tree trained on a random sample with replacement of N cases.
 - *Prereq:* random sampling, "with replacement".
- **Random feature subsampling** — at each split, only m of M total input variables considered; m held constant while trees grow.
 - *Prereq:* none.
- **Classification vs regression usage of Random Forest** — classifier predicts class labels; regression averages outputs.
 - *Prereq:* classification vs regression distinction.
- **Features (independent variables)** — here 4: `Open/Close`, `High/Low` ratios, 1-day lag returns, 2-day lag returns.
 - *Prereq:* ratio/indicator construction from OHLC data.
- **Target (dependent variable)** — binary signal: +1 if tomorrow's close > today's close, else −1 (via `np.where`).
 - *Prereq:* classification labels, forward-looking signal.
- **Train–test split (75/25, time-ordered)** — first 75% train, last 25% test.
 - *Prereq:* train/test split rationale.
- **Model fitting** — `RandomForestClassifier(random_state=5).fit(X_train, y_train)`; `random_state` for reproducibility.
 - *Prereq:* what fitting does, seed/reproducibility.
- **Classification metric — accuracy score** — fraction of correct predictions out of total.
 - *Prereq:* none.
- **Out-of-bag (OOB) error advantage** — reduces need for a separate validation split.
 - *Prereq:* validation set concept (advanced).
- **Advantages** (error balancing, missing-data robustness, feature-importance/outlier use) and **disadvantages** (poor continuous extrapolation, limited range beyond training data).
 - *Prereq:* none.
### 3. `KNN_Classification.ipynb`
K-Nearest Neighbours — a lazy, distance-based classifier.
**Concepts (with prerequisites):**
- **K-Nearest Neighbours (KNN) classifier** — classifies a point by the majority class of its k closest training neighbours; decision based on local distance.
 - *Prereq:* Euclidean distance intuition, majority voting.
- **Features (lagged returns)** — `1_day_lag_returns` and `2_day_lag_returns` from `Close.pct_change().shift()`.
 - *Prereq:* feature engineering, lags, look-ahead avoidance.
- **Target variable** — binary: 1 if today's return > 0 else 0.
 - *Prereq:* binary classification.
- **Time-ordered train/test split** — last 20% test, respecting chronological order.
 - *Prereq:* why we don't shuffle time series.
- **Model instantiation & fit** — `KNeighborsClassifier()` with default k=5; `fit(X_train, y_train)`.
 - *Prereq:* k hyperparameter concept.
- **Prediction & evaluation** — `predict(X_test)`, `accuracy_score`, `confusion_matrix`.
 - *Prereq:* accuracy, confusion matrix (TP/FP/TN/FN).
- **Decision-region plot** — shaded regions where model predicts class 0 vs 1; "island-like" non-linear boundaries typical of KNN.
 - *Prereq:* scatter plots, decision boundary intuition.
- **Confidence interpretation** — points far from boundary more confident; near boundary uncertain.
 - *Prereq:* probability/confidence intuition.
### 4. `SVM_Trading.ipynb`
Support Vector Machine — max-margin linear classifier.
**Concepts (with prerequisites):**
- **Support Vector Machine (SVM)** — finds a hyperplane separating classes that **maximises the margin** to the closest points (support vectors).
 - *Prereq:* 2D geometry of a line, distance to a line, maximisation.
- **Hyperplane / decision boundary** — the separating line (2D) or plane (3D) where the SVM score = 0.
 - *Prereq:* none.
- **Margins and support vectors** — dashed lines at score = ±1; support vectors lie on/inside margins and determine boundary.
 - *Prereq:* none.
- **Kernel (here linear)** — `SVC(kernel='linear')` draws a straight-line boundary; other kernels extend to non-linear data.
 - *Prereq:* what linear vs non-linear means.
- **Regularization parameter C** — `C=1.0`; lower C → wider margin/more regularisation; higher C → tighter fit to training data.
 - *Prereq:* bias–variance / overfitting idea.
- **Features** — two lagged returns; **target** — binary direction (1 if return > 0).
 - *Prereq:* features, target, labels.
- **Train–test split (time-aware, last 20% test)**.
 - *Prereq:* train/test split.
- **Model coefficients** — `coef_` and `intercept_` define the boundary for linear kernel.
 - *Prereq:* equation of a line from weights.
- **Evaluation** — test accuracy (0.625) and confusion matrix; note class-imbalance pitfall (all predictions one class while still ~62%).
 - *Prereq:* accuracy, confusion matrix, class imbalance.
- **`decision_function`** — signed distance from boundary; sign gives class, magnitude gives confidence.
 - *Prereq:* distance to a hyperplane.
### 5. `Logistic Regression.ipynb`
Linear model for **binary classification** via the sigmoid function.
**Concepts (with prerequisites):**
- **Logistic (sigmoid) function** — y = 1/(1 + e^(−x)); S-shaped curve squashing any input to (0,1), the probability of the positive class.
 - *Prereq:* exponential function, graphing a curve.
- **Classification vs regression** — despite the name, logistic regression is a **classifier** for a categorical/binary dependent variable (0/1, −1/1, True/False).
 - *Prereq:* classification vs regression distinction.
- **From linear to logistic regression** — computes a weighted sum of inputs (like linear regression) then passes it through the sigmoid to get a probability.
 - *Prereq:* linear regression, weighted sum.
- **Decision boundary** — the straight line where P(up) = 0.5; axis of the two lagged-return features.
 - *Prereq:* linear boundary, probability = 0.5 threshold.
- **Features** — `1_day_lag_returns`, `2_day_lag_returns` (prior days' returns to prevent look-ahead).
 - *Prereq:* feature engineering, lags.
- **Target** — binary `(return > 0).astype(int)`.
 - *Prereq:* binary labels.
- **Train–test split** — last 20% kept chronological as test.
 - *Prereq:* train/test split.
- **Regularization parameter C** — `LogisticRegression(C=1e5)`; high C gives training data more weight than the complexity penalty.
 - *Prereq:* regularization intent.
- **`predict` vs `predict_proba`** — class labels vs `P(up)` for each day.
 - *Prereq:* class vs probability output.
- **Metrics — accuracy and confusion matrix** — overall hit rate; rows=true class, columns=predicted class (TN/FP/FN/TP).
 - *Prereq:* accuracy, confusion matrix.
- **Decision-region visualisation** — shaded class regions, test points, straight separating line.
 - *Prereq:* scatter/contour plots.
- **Limitations** — accuracy inflated by class imbalance; teaching demo only.
 - *Prereq:* class imbalance.
### 6. `Artificial Neural Network.ipynb`
Multi-Layer Perceptron (MLP) classifier.
**Concepts (with prerequisites):**
- **Artificial Neural Network (ANN)** — supervised learning loosely inspired by the brain; nodes (neurons) connected by links pass and transform data.
 - *Prereq:* none.
- **Architecture — input/hidden/output layers** — input layer, one or more hidden layers, output layer; each layer has nodes; fully connected between adjacent layers.
 - *Prereq:* none.
- **Multi-Layer Perceptron (MLP)** — a neural network with multiple fully-connected layers of nodes.
 - *Prereq:* what a layer is.
- **Weights and bias** — each link has a weight; algorithm adjusts weights during training based on errors.
 - *Prereq:* what a weight does (analogous to β coefficients in linear regression).
- **Backpropagation and gradient descent** — gradients computed by backpropagation; weights updated via gradient descent to minimise loss.
 - *Prereq:* partial derivatives, gradient (introductory).
- **Loss: Cross-Entropy** — default loss for classification; produces per-sample class probability vectors via `predict_proba`.
 - *Prereq:* probability, what a loss function is.
- **Model parameters (coefs_)** — weight matrices; shapes show layer connectivity, e.g. `[(2,5),(5,2),(2,1)]`.
 - *Prereq:* matrix shape/size.
- **Hyperparameters** — `hidden_layer_sizes=(5,2)`, `solver='lbfgs'`, `alpha` (regularization), `random_state`.
 - *Prereq:* what a hyperparameter is.
- **`fit` / `predict` / `predict_proba`** — train, label new samples, output class probabilities.
 - *Prereq:* model lifecycle API.
- **Feature/label arrays** — X shape `(n_samples, n_features)`, y shape `(n_samples)`.
 - *Prereq:* matrix/array dimensions.
---
## Module: Predict Trend Using Classification
### 7. `Support Vector Classifier Strategy.ipynb`
End-to-end SVC trading-signal pipeline (S&P 500 / SPY).
**Concepts (with prerequisites):**
- **Support Vector Classifier (SVC)** — SVM used for classification; finds a hyperplane separating classes (max-margin).
 - *Prereq:* SVM, hyperplane, margin (see notebook 4).
- **Hyperplane dimensionality** — hyperplane dimension = number of features − 1 (line in 2D, plane in 3D).
 - *Prereq:* coordinate geometry.
- **Features (explanatory variables)** — `Open/Close` and `High/Low` ratios as indicator-like predictors; choice described as somewhat arbitrary (can extend).
 - *Prereq:* OHLC data, ratio indicators.
- **Target (dependent variable / signal)** — +1 buy signal if tomorrow's close > today's close, −1 otherwise; built with `np.where(condition, if_true, if_false)`.
 - *Prereq:* numpy `np.where`, forward-looking labels.
- **Train–test split** — first 80% train, last 20% test (chronological).
 - *Prereq:* train/test split, no look-ahead.
- **Model training** — `SVC().fit(X_train, y_train)`; `predict(X_test)` for signals.
 - *Prereq:* fit/predict API.
- **Classifier accuracy** — `accuracy_score(y_true, y_pred)` on both train and test; ~58% test accuracy interpreted as above chance (effective classifer).
 - *Prereq:* accuracy metric.
- **Strategy implementation & backtest-style returns** — generate `Predicted_Signal` on full data, compute daily `Returns = Close.pct_change()`, strategy returns = `Returns * signal.shift(1)`, geometric cumulative returns via `.cumprod()`.
 - *Prereq:* log/simple returns, `shift()` to avoid look-ahead, cumulative product.
- **Signal shifting** — `shift(1)` applies today's signal from the previous bar's close (avoids look-ahead).
 - *Prereq:* time lags, look-ahead bias.
- **Cumulative-returns visualisation** — plot of strategy equity/returns over test period (~10% return).
 - *Prereq:* line plots, compounding returns.
- **Model iteration / tweaking** — trying different datasets and engineered indicators to improve accuracy.
 - *Prereq:* none.