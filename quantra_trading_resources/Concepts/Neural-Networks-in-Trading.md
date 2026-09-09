# Neural Networks in Trading — Concept Inventory
## COURSE: Neural Networks in Trading
Course on building neural-network trading strategies with sklearn MLPClassifier, Keras DNNs, RNNs and LSTMs, hyperparameter tuning via cross-validation, and live-trading simulation. 7 notebooks + 1 supporting module (`data_modules/Keras_CV.py`).
---
## MODULE: Neural Networks
### LESSON: MLPClassifier Hands-on
- **Neural Network (MLP):** A multi-layer perceptron is a feedforward network of neurons in layers; data flows once forward, error propagates backward (backpropagation). prereqs: linear algebra, supervised learning.
- **MLPClassifier (sklearn):** sklearn's neural-network classifier used to build a trading strategy; configured via `activation`, `hidden_layer_sizes`, `random_state`, `solver`. prereqs: neural network, classification.
- **Predictor variables (features):** Inputs to the model; here one-day returns (`ret1`), five-day returns (`ret5`), five-day std (`std5`), volume/ADV20, and price differences (H-L, O-C). prereqs: pandas, feature engineering.
- **Target variable (labels):** The output to predict; here 1 if future one-day return is positive, else 0 (binary classification). prereqs: classification, returns.
- **pct_change():** pandas method computing percentage change from the previous row. prereqs: pandas.
- **rolling(window).sum() / .std():** Rolling-window aggregation computing sum/std over the previous N rows. prereqs: pandas, time series.
- **shift(periods):** Shifts values forward/backward in time; used to create future returns (`retFut1`). prereqs: pandas, time series.
- **dropna():** Removes rows with missing values (e.g. the last day whose future return is unknown). prereqs: pandas.
- **Train/test split:** Splitting data into a training set (80%) to build the model and a test set (20%) to verify it. prereqs: model validation.
- **Regime change / non-stationarity:** Time-series statistics change over time; a model trained on earlier data is more realistic than random sampling, and ML strategies must be robust to non-stationary regimes. prereqs: time series, stationarity.
- **StandardScaler:** Standardizes features by removing the mean and scaling to unit variance; prevents unexpected model behavior from unscaled predictors. prereqs: feature scaling.
- **Activation function:** Non-linear function defining neuron output (e.g. logistic/sigmoid); adds non-linearity so the network can fit complex patterns. prereqs: neural network.
- **hidden_layer_sizes:** Tuple specifying number of hidden layers and neurons per layer, e.g. `(5)` = one hidden layer of 5 neurons. prereqs: MLP architecture.
- **random_state / seed:** Sets the random seed for weight/bias initialization so results are reproducible. prereqs: reproducibility.
- **solver (sgd):** Optimization function (stochastic gradient descent) used to update weights during backpropagation. prereqs: gradient descent.
- **fit():** Trains the model on the predictor/target training data. prereqs: MLP, training.
- **predict():** Uses the trained model to output class predictions for new input data. prereqs: MLP, inference.
- **Trading signal / strategy returns:** Signal (+1 buy, 0 no-buy) from predictions multiplied by future returns to generate strategy returns. prereqs: trading strategy, returns.
- **Sharpe Ratio:** Risk-adjusted return = sqrt(N) * mean(excess return)/std(excess return); higher is better, >1.5 preferred. prereqs: returns, risk metrics.
- **Excess return:** Strategy return minus the risk-free rate (assumed 5% p.a., daily = 0.05/252). prereqs: Sharpe ratio.
- **CAGR (Compound Annual Growth Rate):** Annualized compounded return = (cumulative returns)^(252/days) - 1. prereqs: compounding, returns.
- **Cumulative returns:** Product of (1+returns) over time; plotted to visualize strategy growth. prereqs: returns.
- **classification_report (sklearn.metrics):** Reports precision, recall, F1-score, and support per class. prereqs: classification metrics.
- **Precision:** tp/(tp+fp); ability of the classifier not to label a negative sample as positive. prereqs: classification metrics.
- **Recall:** tp/(tp+fn); ability of the classifier to find all positive samples. prereqs: classification metrics.
- **F1-score:** Weighted harmonic mean of precision and recall; best at 1, worst at 0. prereqs: precision, recall.
- **Support:** Number of occurrences of each class in the true labels. prereqs: classification metrics.
---
## MODULE: Deep Learning in Trading
### LESSON: DNN Trading Strategy Code
- **Deep Neural Network (DNN):** A neural network with many hidden layers; deeper models create more complex features but risk overfitting. prereqs: neural network, MLP.
- **MinMaxScaler:** sklearn scaler that maps values to [0,1]; used for the Volume column. prereqs: feature scaling.
- **Manual OHLC scaling:** Scaling Open/High/Low/Close together using global min/max to preserve the relationship High >= Close >= Low (MinMaxScaler scales columns independently and would break it). prereqs: feature scaling, OHLC data.
- **Look-ahead bias avoidance:** Scaling using only train-data min/max so test data is not leaked into the scaler. prereqs: data leakage, train/test split.
- **Feature/target datasets:** X = OHLCV features; y = 1 if close 5 days ahead is higher, else 0 (weekly trend prediction). prereqs: feature engineering, classification.
- **Class imbalance / class weights:** When one class dominates, the model over-learns it; class weights rebalance so both classes get equal learning weightage. prereqs: classification, imbalanced data.
- **Sequential model (Keras):** Linear stack of layers built with `model.add()`. prereqs: Keras, DNN.
- **Dense layer:** Fully connected layer; each neuron connects to all neurons of the previous layer. prereqs: neural network, Keras.
- **Activation layer (Keras):** Applies an activation function (e.g. tanh) to layer outputs. prereqs: activation functions, Keras.
- **Dropout layer:** Randomly switches off a fraction of neurons during training to reduce overfitting. prereqs: regularization, overfitting.
- **BatchNormalization:** Normalizes layer inputs to stabilize and speed up training. prereqs: DNN, normalization.
- **kernel_initializer (he_normal):** Initializes weights from He-normal distribution at first run. prereqs: weight initialization.
- **bias_initializer (zeros):** Initializes bias terms to zero. prereqs: weight initialization.
- **input_shape:** Defines the number of input features (columns) for the first layer. prereqs: Keras, DNN.
- **Hyperparameters:** Configuration values set before training (neurons, dropout ratio, activation, epochs, batch size, momentum); tweaked to improve the model. prereqs: model training.
- **ModelCheckpoint callback:** Saves the best model weights during training by monitoring a metric (e.g. val_loss); `save_best_only=True`, `mode='auto'`. prereqs: Keras callbacks, validation.
- **model.summary():** Prints layer-by-layer architecture with output shapes and parameter counts. prereqs: Keras.
- **compile():** Configures the model with loss function, optimizer, and metrics. prereqs: Keras.
- **Loss function (binary_crossentropy):** Quantifies how far predictions are from ground truth for binary classification. prereqs: loss functions, classification.
- **Optimizer (adam):** Algorithm that updates weights to minimize loss. prereqs: gradient descent, optimization.
- **Metrics (accuracy):** Metric reported during training to evaluate model performance. prereqs: classification metrics.
- **epochs:** Number of full passes over the training data. prereqs: training.
- **batch_size:** Number of training samples processed before updating weights. prereqs: training.
- **validation_split:** Fraction of training data held out to evaluate the model on unseen data each epoch. prereqs: validation.
- **training.history:** Dict of per-epoch metrics (loss, val_loss, accuracy, val_accuracy) used to plot convergence. prereqs: training, validation.
- **Overfitting / underfitting:** Diagnosed by comparing train vs validation loss curves; overfit = train loss low, val loss high. prereqs: validation, bias-variance.
- **load_weights():** Loads the best saved weights back into the model before prediction. prereqs: model checkpointing.
- **predict() probability threshold:** Keras predict returns a probability; >0.5 maps to class 1 (buy), <=0.5 to class 0. prereqs: classification, inference.
- **accuracy_score:** Fraction of correct predictions on the test set. prereqs: classification metrics.
- **Buy and hold benchmark:** Comparing strategy cumulative returns against simply holding the market. prereqs: trading strategy, returns.
- **Risk-free rate adjustment:** Subtracting daily risk-free rate (e.g. 5%/252) from strategy returns to compute excess returns. prereqs: Sharpe ratio.
---
## MODULE: Cross Validation in Keras
### LESSON: Trading Strategy using Cross Validation
- **Cross-validation:** Technique to evaluate a model on multiple train/validation splits to find the best hyperparameters. prereqs: model validation, train/test split.
- **GridSearchCV (sklearn):** Exhaustively searches a grid of hyperparameter combinations using k-fold cross-validation to find the best set. prereqs: cross-validation, hyperparameters.
- **KerasModelWrapper (BaseEstimator, ClassifierMixin):** Custom wrapper class making a Keras model compatible with sklearn's GridSearchCV (implements fit/predict/score). prereqs: sklearn API, Keras.
- **Pipeline (sklearn):** Chains steps (e.g. classifier) so they can be cross-validated together; parameters set via `step__param` naming. prereqs: sklearn, cross-validation.
- **param_grid:** Dictionary of hyperparameter values to search (neurons, activation, dropout ratio). prereqs: GridSearchCV.
- **n_jobs / verbose:** Parallelism and logging controls for GridSearchCV. prereqs: GridSearchCV.
- **best_params_:** The best hyperparameter combination found by GridSearchCV. prereqs: GridSearchCV.
- **pickle save/load:** Serializing the best parameters to a `.sav` file for reuse. prereqs: serialization.
- **create_new_model() (data_modules/Keras_CV.py):** Reusable function building a 5-hidden-layer DNN (Dense+Activation+Dropout) with configurable neurons/activation/dropout, compiled with binary_crossentropy + adam. prereqs: Keras, DNN.
- **ModelCheckpoint on best model:** Saving best weights of the tuned model during training. prereqs: callbacks, validation.
- **Predicting trend with best model:** Using the tuned model to predict buy/sell signals on test data and computing accuracy. prereqs: inference, classification.
- **Strategy vs market returns comparison:** Multiplying signals by future returns and comparing cumulative strategy vs market returns. prereqs: trading strategy, returns.
- **Conclusion — time cost of CV:** Cross-validation is time-consuming but saves manual hyperparameter tuning effort. prereqs: cross-validation.
---
## MODULE: Long Short Term Memory Unit (LSTMs)
### LESSON: LSTM Based Strategy
- **LSTM (Long Short-Term Memory):** A recurrent neural network variant with gated memory cells that captures long-term dependencies in sequences; used to predict future close prices. prereqs: RNN, sequence modeling.
- **Timestep / lookback window:** Number of past days (e.g. 20) fed to the model at each step to predict the next value. prereqs: sequence modeling, time series.
- **3D input shape (samples, timesteps, features):** LSTM input is (batch, timesteps, features); here (n, 20, 5) for 20 days of OHLCV. prereqs: LSTM, tensor shapes.
- **return_sequences=True:** LSTM returns output for every timestep (keeps sequence dimension) rather than only the last. prereqs: LSTM.
- **StandardScaler for LSTM:** Standardizing train and test sets separately before building sequences. prereqs: feature scaling.
- **Deep LSTM + Dense stack:** LSTM layer followed by several Dense+Dropout layers; depth increases feature complexity but risks overfitting. prereqs: LSTM, DNN.
- **mean_squared_error (MSE) loss:** Regression loss used because the LSTM predicts continuous close prices. prereqs: loss functions, regression.
- **mse metric:** Mean squared error reported during training. prereqs: regression metrics.
- **ModelCheckpoint (val_loss):** Saves best weights whenever validation loss improves. prereqs: callbacks, validation.
- **load_weights:** Loading best weights before predicting test close prices. prereqs: checkpointing.
- **Predicted vs actual close:** Building a performance dataframe comparing predicted and actual close prices. prereqs: regression evaluation.
- **Spread (Actual - Predicted):** Difference between actual and predicted prices; if mean-reverting, it can generate entry/exit signals. prereqs: mean reversion, pairs trading.
- **Bollinger-style bands on spread:** Plotting expanding mean ± s*std of the spread; buy when spread below lower band, sell when above upper band. prereqs: mean reversion, standard deviation.
- **Mean-reverting strategy caveat:** Such a strategy is for paper trading only; not for real trading without extensive backtesting. prereqs: backtesting, risk.
---
## MODULE: Recurrent Neural Networks
### LESSON: Predicting Prices using RNN
- **RNN (Recurrent Neural Network):** A network with recurrent connections that processes sequences step by step, carrying hidden state across time; used to predict future close prices. prereqs: neural network, sequence modeling.
- **SimpleRNN (Keras):** Basic recurrent layer; here with `timestep` units and input shape (timesteps, features). prereqs: RNN, Keras.
- **Timestep of 20 days:** Feeding the past 20 days of OHLCV at each step; can be changed to predict a sequence of 5 days. prereqs: sequence modeling.
- **Dropout ratio 0.5:** Half the neurons in the preceding layer are switched off during training to reduce overfitting. prereqs: dropout, overfitting.
- **Deep RNN + Dense stack:** SimpleRNN followed by progressively wider Dense+Dropout layers (32→2048). prereqs: RNN, DNN.
- **mean_squared_error loss:** Regression loss for predicting continuous prices. prereqs: loss functions, regression.
- **ModelCheckpoint (val_loss):** Saves best weights on validation loss improvement. prereqs: callbacks.
- **load_weights:** Loading best weights before prediction. prereqs: checkpointing.
- **Reshape predictions:** Reshaping model output to a single column vector to match y_test for the performance dataframe. prereqs: numpy, tensor shapes.
- **Lagging predictions:** RNN predictions look lagging; accuracy improves by tuning hyperparameters (e.g. via GridSearch). prereqs: RNN, hyperparameters.
### LESSON: Strategy Analytics for RNN
- **Trade-wise analytics:** Per-trade list with entry time, entry price, exit time, exit price, and PnL for each trade. prereqs: backtesting, trading.
- **Signal generation:** Signal = 1 if predicted price > previous day's actual price, else -1. prereqs: trading signals.
- **get_trades() function:** Iterates over signals, records position changes (long/short/neutral) and builds a trade log with entry/exit and PnL. prereqs: backtesting, pandas.
- **PnL per trade:** (Exit price - Entry price) * Position; position is +1 long, -1 short. prereqs: trading, PnL.
- **Strategy analytics (get_analytics()):** Computes number of long/short trades, total trades, gross profit/loss, net profit, winners/losers, win/loss percentage, and average profit/loss per trade. prereqs: trade statistics.
- **Win percentage:** 100 * winners / total trades. prereqs: trade statistics.
- **Equity curve:** Cumulative product of (1 + strategy returns) plotted against benchmark cumulative returns. prereqs: returns, performance.
- **Strategy returns:** Daily returns * signal shifted by one day (position applied next day). prereqs: returns, trading.
- **Drawdown:** Percentage decline from the running maximum of cumulative returns. prereqs: performance metrics.
- **Maximum drawdown:** The largest peak-to-trough decline in the equity curve. prereqs: drawdown, risk.
---
## MODULE: Challenges in Live Trading
### LESSON: Trading Simulation using Deep Learning
- **Live-trading simulation:** Using a trained ML model in a rolling simulation, retraining it whenever performance drops. prereqs: DNN, backtesting.
- **create_features() function:** Reusable function generating features and target from raw data at every data point. prereqs: feature engineering.
- **Simulation parameters:** `simulation_length` (number of simulation points), `performance_length` (past window to check model performance), `minimum_feature_length` (min data needed for one feature point). prereqs: simulation design.
- **Train/simulation split:** Splitting raw data into a training set (to build the initial model) and a simulation set (to walk forward). prereqs: train/test split.
- **train_model() function:** Builds and fits a DNN (via create_new_model) with a ModelCheckpoint, returning the trained model. prereqs: Keras, DNN.
- **save_model() function:** Saves model architecture as JSON and weights as HDF5. prereqs: model serialization.
- **load_model() function:** Reconstructs the model from JSON and loads weights. prereqs: model serialization.
- **model_from_json / to_json:** Keras methods to serialize/deserialize model architecture. prereqs: Keras, serialization.
- **train_new_model() function:** Retrains a model by creating features, training, and saving — used when performance degrades. prereqs: retraining, simulation.
- **Performance-based trading decision:** If past accuracy > threshold (0.55), trade on the latest prediction; otherwise retrain and skip trading that day. prereqs: model monitoring, simulation.
- **Rolling retraining:** Rolling the training window forward and retraining as new data becomes available. prereqs: online learning, simulation.
- **Cumulative strategy returns in simulation:** Multiplying signals by future returns and cumulating to measure simulation performance. prereqs: returns, simulation.
---
## MODULE: data_modules (supporting module)
### LESSON: Keras_CV.py
- **create_new_model(neurons, act_1, dropout_ratio):** Reusable Keras function building a 5-hidden-layer DNN (Dense+Activation+Dropout, neurons doubling per layer) with a sigmoid output, compiled with binary_crossentropy + adam + accuracy. prereqs: Keras, DNN.
- **he_normal kernel initializer:** Weight initialization suited to ReLU/tanh activations. prereqs: weight initialization.
---
## Neural-Networks-in-Trading — Section-based course structure (full lesson-by-lesson view)
# — Neural Networks — Concept Inventory
**Track:** 5 — Artificial Intelligence in Trading (Advanced)
**Media note:** PDFs only (no mp4s present).
**Overlap with D: notebooks:** light — D: holds notebook-based DL/neural-network extraction; this course is the maths + Keras-hyperparameter companion (forward propagation, backprop, activation functions, normalisation, cross-entropy, early stopping).
## COURSE
Handling of neural networks for trading strategies built on the math: forward propagation (moving input through a 3-layer net), backward propagation (gradient-based weight updates), and their mathematical machinery (function derivatives + chain rule); then building/regularising deep models in Keras — activation functions (ReLU, sigmoid/softmax), data normalization/batch, cross-entropy loss; concludes with cross-validation and hyperparameter tuning, paper/live deployment via IBridgePy.
## Course Prerequisite Map
- **Section 1 (Neural Networks complete history):** requires calculus (derivative, chain rule) — serves upward as core for the rest of course.
- **Section 4 (Deep Learning in Trading):** requires Section 1 math + install Keras/TensorFlow; activation functions, normalisation, cross-entropy.
- **Section 7 (Cross Validation in Keras):** requires Section 4 (a K sequence model) + every slight hyperparameter concept.
- **Section 10 Paper & Live:** requires Section 7 model + IB bridge.
- **Section 11 Downloadable Resources** wraps.
---
### Section 1 — Neural Networks
- **CONCEPT:** Derivative and chain rule — student prerequisite for "Math behind backprop": the derivative measures change/slope, and the chain rule composes derivatives across layers (∂L/∂w via backprop). prereqs: calculus/analysis prerequisite.
- **CONCEPT:** Forward propagation — compute the network output by multiplying input vector × weights across layers, through activation, layer by layer (the 3-layer example: input → hidden = 2 units → output = 2 units). prereqs: network architecture, matrix multiply.
- **CONCEPT:** Backpropagation — after forward pass, compute the loss and propagate error gradients backward via the chain rule, updating each weight to reduce loss — the training algorithm. prereqs: forward pass + chain rule + loss.
### Section 4 — Deep Learning in Trading
- **CONCEPT:** Activation functions — **ReLU**, **ELU**, **sigmoid**, **tanh**, **softmax**. They introduce nonlinearity; softmax used for classification output, ReLU most common hidden. prereqs: forward propagation, binary/multiclass features.
- **CONCEPT:** Normalization / Standardization and batch norm — scaler/standardization brings values to comparable scale; **batch normalization** stabilises and accelerates training within dense blocks. prereqs: data range divergence, deep layering.
- **CONCEPT:** Cross-entropy loss — measures the error for classification prediction: from **entropy** (uncertainty) it links predicted-class probabilities to ground truth. prereqs: entropy, probability distribution, loss.
- **CONCEPT:** Keras/TensorFlow installation — version-guided install on Windows (VS), Mac, Ubuntu; Keras backend on TensorFlow. prereqs: Python + a DL env.
### Section 7 — Cross Validation in Keras
- **CONCEPT:** Keras layer/hyperparameter building blocks — Dense layer, constraints, activation, **Dropout**, ModelCheckpoint. **Early stopping** (monitor-val loss, restore best, patience) avoids overfitting. prereqs: Section 4 model + tuning concepts.
- **CONCEPT:** Important hyperparameters — hyperparameters of RNNs incl. recurrent initializer, entropy, recurrent_regularizer, recurrent_constraint, recurrent_dropout, stateful semantics for sequence data. prereqs: Keras + recurrent/region intuition.
- **CONCEPT:** Cross-validation of the Keras model — using validation-fold(s) and early stopping to pick epoch count/architecture robustly. prereqs: Sections 4 + 7.
### Section 10 — Paper and Live Trading
- **CONCEPT:** IBridgePy / paper-live — deploy the Keras NN strategy through IBridgePy (template `IBridgePyNN.zip`) into a broker/paper account. prereqs: trained model + broker interface.
### Section 11 — Downloadable Resources
- **CONCEPT:** Class resources (`Neural-Networks-in-Trading-Resources.zip`) — notebooks/data + templates for the whole NN-in-trading workflow. prereqs: entire course.