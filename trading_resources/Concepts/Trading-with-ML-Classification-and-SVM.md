# Trading with Machine Learning: Classification and SVM — Concept Inventory
> Scope: intraday classification trading strategy using a tuned Support Vector Machine (SVC) on 1-minute ICICI Bank futures OHLCV data.
> Modules/notebooks enumerated: **1** (`Trading Strategy Classification.ipynb`) | Data: `data_modules/ICICI Minute Data.csv` | Module files: `ReadMe.html`, `Folder Structure and How to Run Code Files.html`
> Core workflow: import data → create indicators → calculate returns → train/test split → build signal targets → hyperparameter tuning → SVM → predict signals → analyse performance → plot results.
---
## Module: Prediction and Strategy
### 1. `Trading Strategy Classification.ipynb`
Complete supervised-classification trading strategy built around an SVM classifier.
**Concepts (with prerequisites):**
- **Data loading & cleaning**
 - **Reading OHLCV data** — `pd.read_csv('...ICICI Minute Data.csv')`; 1-minute bars for two days of a futures instrument.
 - *Prereq:* CSV import, OHLCV bars.
 - **Liquidity filtering** — dropping rows with zero traded volume (avoids training on illiquid moves).
 - *Prereq:* volume/liquidity awareness.
 - **Datetime index** — converting `Time` to pandas datetime and setting as index; needed to detect market close (~15:29) for squaring-off positions.
 - *Prereq:* datetime parsing, index setting.
- **Feature engineering (indicators)**
 - **RSI (Relative Strength Indicator)** — computed via `talib` on shifted Close with `timeperiod=n`; uses prior n minutes' close prices (look-ahead avoidance).
 - *Prereq:* technical indicators, RSI definition, shifting/lagging.
 - **SMA (Simple Moving Average)** — `Close.shift(1).rolling(n).mean()` over a 10-minute window.
 - *Prereq:* moving average, rolling windows.
 - **Correlation coefficient** — rolling correlation between Close and SMA; trimmed to `[-1, 1]` because correlation is bounded.
 - *Prereq:* correlation bounds, rolling statistics.
 - **SAR (Stop and Reverse)** — computed on High/Low (sensitive to new highs/lows) with acceleration and max-step parameters (0.2, 0.2).
 - *Prereq:* Parabolic SAR indicator, support/resistance.
 - **ADX (Andrews/Directional Index)** — here computed on High/Low/Open (recent price information) rather than Close.
 - *Prereq:* ADX indicator mechanics.
 - **Previous-minute OHLC** — `Prev_High`, `Prev_Low`, `Prev_Close` via `shift(1)` to convey recent volatility.
 - *Prereq:* lags/look-ahead bias.
 - **Open-price differences** — `OO = Open − Open.shift(1)` (minute-over-minute open change) and `OC = Open − Prev_Close` (overnight/intraday gap).
 - *Prereq:* gap/change features.
 - **All indicators use past data** — `shift(1)` on the source series to avoid look-ahead leakage into the target.
 - *Prereq:* temporal causality, data leakage.
- **Returns and target**
 - **Future return target** — `Fut_Ret = (Open.shift(−1) − Open)/Open`; the one-period-ahead open-to-open return the model must predict.
 - *Prereq:* returns, forward-looking targets.
 - **Lag-return columns** — `return1 … returnN` via `Fut_Ret.shift(i)`, capturing the trend of past n periods.
 - *Prereq:* feature lags, rolling trend.
- **Output signal encoding (classification target)** — quantile-based binning of `Fut_Ret` into three classes: `1` (Buy, top tercile), `−1` (Sell, bottom tercile), `0` (hold, middle); thresholds from train data quantiles (0.66 / 0.34).
 - *Prereq:* classification, multiclass labels, quantiles.
- **Market-close squaring-off** — zeroing `Signal` and `Fut_Ret` at the 15: closing minute so the intraday strategy holds no positions overnight.
 - *Prereq:* intraday trading, position flattening.
- **Feature/target construction** — dropping raw columns (Close, Signal, High, Low, Volume, Fut_Ret) and setting `X` (features) and `y = Signal` (labels).
 - *Prereq:* features vs target, X/y.
- **Hyperparameter tuning**
 - **Pipeline** — `[('scaler', StandardScaler()), ('svc', SVC())]` chains scaling before model fitting to neutralize per-feature weight differences.
 - *Prereq:* pipelines, feature scaling.
 - **Hyperparameters of SVC** — `C` (regularization costs), `gamma` (kernel coefficient), and `kernel`; tuned over a tested grid (`rbf` kernel, several C and gamma values).
 - *Prereq:* SVM hyperparameters, kernel, regularization.
 - **RandomizedSearchCV + TimeSeriesSplit** — random hyperparameter search with time-ordered sequential CV splits (n_splits=2) to respect time order and avoid overfitting.
 - *Prereq:* hyperparameter search, time-series cross-validation.
- **Best-parameter selection** — `rcv.best_params_` yields optimal `C`, `gamma`, `kernel` for a newly instantiated `SVC(...)`.
 - *Prereq:* model selection.
- **Training & prediction**
 - **Standardisation before fit/predict** — `StandardScaler().fit_transform(train)` for training; `ss1.transform(test)` reuses the fit (no leakage) before prediction.
 - *Prereq:* scaling discipline.
 - **Prediction and saving** — `cls.predict(...)` on train and test; storing predictions into `Pred_Signal` column.
 - *Prereq:* model inference, prediction arrays.
 - **Strategy returns** — `Ret1 = Fut_Ret × Pred_Signal` (position-timed return).
 - *Prereq:* strategy/position sizing, returns.
- **Performance evaluation**
 - **Accuracy** — overall fraction of correct signal labels.
 - *Prereq:* classification accuracy.
 - **Confusion matrix** — table of true vs predicted classes; here 3×3 for classes {−1,0,1}, showing per-class true/false hits.
 - *Prereq:* classification, confusion matrix, class imbalance.
 - **Classification report — precision, recall, F-score, support** — per-class precision = tp/(tp+fp), recall = tp/(tp+fn), F-score (harmonic mean), support (class counts).
 - *Prereq:* precision, recall, F-measure.
 - **Drawdown** — cumulative returns, running max, and percentage drawdown (decline from peak); max drawdown reported.
 - *Prereq:* drawdown / peak-to-trough decline.
 - **Annualised Sharpe ratio** — risk-adjusted return scaled to annualised frequency using per-year minute count (`sqrt(252*6.25*60)`).
 - *Prereq:* Sharpe ratio, risk-free annualisation.
 - **Cumulative-return and benchmark comparison plot** — comparing strategy returns vs market returns over the test window.
 - *Prereq:* cumulative returns, buy-and-hold benchmark.
---
## Trading-with-ML-Classification-and-SVM — Section-based course structure
# — Trading with Machine Learning: Classification and SVM — Concept Inventory
**Track:** 4 — Machine Learning & Deep Learning in Trading (Beginners)
**Media note:** PDFs + resources zip only (no mp4s in folder).
**Overlaps with D: notebooks:** heavy — the D: side has notebook-based `Trading-with-ML-Classification-and-SVM` extraction (binary/multi-class classification, SVM, prediction/strategy notebooks, and paper/live templates). This course carries the corresponding maths/measurement PDFs (decision boundary, probability, performance measures, one-hot/softmax, SVM maths).
## COURSE
Using classification to build trading signals, from binary to multiclass: probability foundations; decision boundaries, cost functions, gradient descent; performance measures for classifiers; encoding categorical targets (one-hot, softmax) and class probability outputs; and **support vector machines** (SVM) from hard-margin objective to soft-margin and kernel-based nonlinear classifiers. Ends with a complete prediction-and-strategy pipeline plus live-trading (IBridgePy) template.
## Course Prerequisite Map
- **Section 1 Introduction requires:** Python + installing scikit-learn (SVC, StandardScaler, RandomizedSearchCV, pipeline). No ML prereq strictly.
- **Section 2 Binary Classification requires:** Section 1 env; core terms introduced in the decision-boundary PDF (decision boundary, cost, gradient descent).
- **Section 3 Multiclass requires:** Section 2 + Probability Concepts 1 & 2 (conditional/joint prob, total-probability rule, `.predict_proba`), plus performance-measure/confusion-matrix knowledge.
- **Section 4 Support Vector Machine requires:** Section 2 (boundary/margin/max-margin) + linear algebra/optimization basics (for the margin maximisation maths).
- **Section 5 Prediction & Strategy requires:** Section 3 (a trained classifier producing class probabilities → prediction) + features.
- **Section 9 Paper & Live Trading requires:** Section 5 (vectorised backtest) + Python env / IBridgePy; also kindred backtesting knowledge from the Python-for-ML course.
---
### Section 1 — Introduction
- **CONCEPT:** Technical references and environment setup — install scikit-learn in your Python IDE; the core sklearn APIs used: `SVC` (support-vector classifier), `StandardScaler` (feature scaling), `RandomizedSearchCV` (randomised hyperparameter search), `pipeline` + `pandas`/`numpy`/`Talib` (technical indicators). prereqs: Python env, package install.
### Section 2 — Binary Classification
- **CONCEPT:** Decision boundary — the n-dimensional plane (hyperplane) that splits feature space into two classes; binary classification aims for the boundary that best separates the two classes. prereqs: linear algebra, two-class label.
- **CONCEPT:** Cost function — the function minimised to get the boundary that minimizes classification prediction error. prereqs: decision boundary concept.
- **CONCEPT:** Gradient descent — iterative process used to minimise the cost function (partial derivatives, stepping along the gradient) to refine model parameters toward the optimal boundary. prereqs: calculus derivatives, cost function.
### Section 3 — Multiclass Classification
- **CONCEPT:** Probability fundamentals (Pt.1) — terms (experiment, event, sample space), calculating probability, two defining properties; unconditional/marginal vs conditional vs joint probability; addition and multiplication rules. prereqs: basic counting/probability.
- **CONCEPT:** Probability fused (Pt. 2) — **Total probability rule** (unconditional P(A) from conditional terms of mutually exclusive/exhaustive events), **expected value**, and `.predict_proba()` as the classifier-giving-per-class probabilities. prereqs: Pt.1 concepts + binary classifier output.
- **CONCEPT:** Performance measures in classification — **confusion matrix** (TP/FP/FN/TN), **accuracy**, **precision**, **recall**, **F-measure/F1** — quantifying a classifier's predictive capability. prereqs: Section 2 model + multiclass outputs.
- **CONCEPT:** Categorical feature encoding — one-hot encoding for categorical (non-numeric) features so a vector classifier can consume them. prereqs: feature extraction, categorical data.
- **CONCEPT:** Softmax regression — the multiclass generalisation of logistic regression; transforms a per-class logit/probabilities vector into ∝ probabilities over n classes. prereqs: one-hot encoding + Section 2 probability outputs.
### Section 4 — Support Vector Machine
- **CONCEPT:** Max-margin / hyperplane selection — the SVM picks the decision boundary by **maximising the distance between the two nearest support points of each class** (margin = max distance to nearest training points). prereqs: Section 2 boundary concepts + Euclidean geometry.
- **CONCEPT:** Maths behind SVM — maximise margin subject to constraints (hard-margin QP); then generalise to **soft-margin** (allow some misclassification via slack) and **nonlinear models** (kernel trick → transform feature space) for inseparable data. prereqs: linear algebra, convex optimisation, Section 2.
### Section 5 — Prediction and Strategy
- **CONCEPT:** Section flow — turns the fitted classifier's class-probability output into trading predictions, maps to a long/flat/short strategy, and backtests the resulting decision vector (vectorised backtesting). prereqs: Sections 3 & 4 predictions + returns data.
- **CONCEPT:** Strategy construction from predicted classes — execute long/short/flat based on the predicted direction class. prereqs: targeting from ML-for-Finance course.
### Section 9 — Paper and Live Trading
- **CONCEPT:** Template for live trading documentation — modifying the Jupyter-backtested SVM strategy for **IBridgePy** live trading on Interactive Brokers / TD Ameritrade / Robinhood (virtual env, packages installed per ReadMe, IBridgePy version binding). prereqs: Section 5 strategy + IBridgePy familiarity.
- **CONCEPT:** Live-trading determinism — a script run by IBridgePy on a cadence to place orders based on the trained SVM model. prereqs: backtesting (Python-for-ML course).
### Section 11 — Downloadable Resources
- **CONCEPT:** Full course resources (`...Classification-and-SVM-Resources.zip`) — notebooks + data for the classification/SVM pipeline. prereqs: all sections.