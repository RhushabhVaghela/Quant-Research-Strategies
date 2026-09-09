# Deep Reinforcement Learning in Trading — Concept Inventory
## COURSE: Deep Reinforcement Learning in Trading
---
## MODULE: Initialise Game Class
### LESSON: Initialise Game Class
- **Gamification of trading:** Treating each individual trade as a game with a start, play period, and end; the RL agent plays these games. prereqs: reinforcement learning, trading.
- **Game class:** The environment the agent explores; generates input features, assembles states, updates positions, and computes rewards. prereqs: RL environment, OOP.
- **OHLCV data:** Open, High, Low, Close, Volume price bars; here 5-minute data from a compressed pickle file. prereqs: market data.
- **read_pickle():** pandas method to read a (compressed) pickle file, e.g. `PriceData5m.bz2`. prereqs: pandas, serialization.
- **Resample / agg():** Converting high-frequency data to lower frequency (5m → 1h → 1d) using `resample(freq, label, closed).agg(ohlcv_dict)`. prereqs: pandas, time series.
- **ohlcv_dict aggregation:** Mapping open→first, high→max, low→min, close→last, volume→sum when resampling. prereqs: resampling, OHLCV.
- **label / closed parameters:** `label` chooses which side labels the interval; `closed` sets interval inequality (left=(start,end], right=[start,end)). prereqs: resampling.
- **reset():** Resets all state values to defaults when a trade game is over, before starting a new game. prereqs: Game class, RL episode.
### LESSON: Working With Pickle File
- **Pickle file (.bz2):** Python serialization format; retains column datatypes (e.g. DatetimeIndex) unlike CSV. prereqs: serialization, pandas.
- **bz2 compression:** Compressed pickle format for smaller file sizes. prereqs: serialization.
- **to_pickle() / read_pickle():** pandas methods to save/load dataframes as pickle files. prereqs: pandas, serialization.
- **Python-version compatibility:** Pickle files are Python-version-specific and backward compatible; version mismatches cause errors. prereqs: serialization.
- **Common pickle errors:** `AttributeError: Can't get attribute '_unpickle_block'` (pandas version mismatch) and `ValueError: unsupported pickle protocol: 4` (older Python). prereqs: serialization, debugging.
---
## MODULE: Construct and Assemble State
### LESSON: Minute Price Data and Resampling Techniques
- **Minute-level data:** Higher-granularity price data (1m, 5m) used to test strategies; you can resample high→low frequency but not the reverse. prereqs: market data, time series.
- **yfinance download():** Downloads minute data (e.g. `period="5d", interval="1m"`); minute data limited to ~7 days. prereqs: data acquisition.
- **Resample to custom frequency:** Using `resample('15T'/'1H'/'4H').agg(ohlcv_dict)` to build 15-min, 1-hour, 4-hour candles from minute data. prereqs: resampling, OHLCV.
### LESSON: Get Last N Time Bars
- **Lookback period (lkbk):** Number of past bars (N) used to build input features; a hyperparameter. prereqs: time series, hyperparameters.
- **get_last_N_timebars():** Function returning the last N bars for 5m, 1h, and 1d resolutions before the current time. prereqs: time series, pandas slicing.
- **Window width (wdw):** Time interval (in days) pulled before the current time to ensure enough bars; e.g. wdw5m=9, wdw1h=ceil(lkbk*15/24), wdw1d=ceil(lkbk*15). prereqs: time series.
- **assert keyword:** Tests a condition (e.g. bar length == lookback) and raises an exception if false. prereqs: Python, debugging.
- **np.ceil():** Returns the smallest integer not less than x; used to widen time windows. prereqs: numpy.
### LESSON: Assemble States
- **State (RL):** The input feature vector the agent observes; passed to the neural network to predict an action. prereqs: RL, feature engineering.
- **State construction:** Building the state from (1) stationary candlestick bars, (2) technical indicators, (3) time signature, (4) position. prereqs: RL, feature engineering.
- **Flatten():** Converting a dataframe to a 1-D array (neural networks prefer array input). prereqs: numpy.
- **Stationary candlestick bars:** Candlesticks are non-stationary; z-scoring them (bar - mean)/std makes them stationary, which NNs prefer. prereqs: stationarity, normalization.
- **Z-score:** (value - mean)/standard deviation; used to normalize candlestick bars. prereqs: statistics, normalization.
- **Technical indicators (TA-Lib):** Features computed from price bars; here relative difference of two SMAs, RSI, Momentum, Balance of Power (BOP), and Aroon Oscillator. prereqs: technical analysis.
- **Relative Strength Index (RSI):** Momentum oscillator measuring speed/change of price moves. prereqs: technical indicators.
- **Momentum (MOM):** Rate of change of price. prereqs: technical indicators.
- **Balance of Power (BOP):** Indicator measuring the strength of buyers vs sellers. prereqs: technical indicators.
- **Aroon Oscillator:** Indicator measuring trend strength/direction. prereqs: technical indicators.
- **Time signature:** Time-of-day (hours*60+minutes)/(24*60) and day-of-week (weekday()/6), normalized, added to the state. prereqs: feature engineering.
- **Position feature:** Current position (long/short/flat) appended to the state. prereqs: RL, trading.
- **State size:** 120 (normalized candlesticks) + 15 (5 indicators × 3 granularities) + 3 (time, day, position) = 138 features. prereqs: feature engineering.
---
## MODULE: Positions and Rewards
### LESSON: Update the Positions
- **update_position():** Updates the trading position in response to the action suggested by the neural network. prereqs: RL, trading.
- **Actions (buy/sell/hold):** Action 0 = hold/do nothing, action 2 = buy (enter long / exit short), action 1 = sell (enter short / exit long). prereqs: RL, trading.
- **Position update rules:** Do nothing if action matches current position or is hold; open a new position if flat; close the position (game over) if action is opposite to current position. prereqs: RL, trading.
- **Game over:** When a position is closed by an opposite action, the trade game ends. prereqs: RL episode.
### LESSON: Reward System
- **Reward function:** Defines the scalar reward the agent receives; design significantly impacts algorithm performance. prereqs: RL, reward design.
- **get_pnl():** Percentage PnL = (curr*(1-tc) - entry*(1+tc))/entry*(1+tc)*position, incorporating transaction cost/commissions (tc=0.001). prereqs: trading, PnL.
- **Transaction cost / commissions:** Costs deducted from PnL; configurable to match local markets/brokers. prereqs: trading costs.
- **Slippage:** Difference between expected and executed price; noted but not included to avoid complexity. prereqs: trading costs.
- **reward_pure_pnl:** Returns the raw percentage PnL. prereqs: reward design.
- **reward_positive_pnl:** Returns PnL only when positive, else 0 (positive reinforcement only). prereqs: reward design.
- **reward_pos_log_pnl:** For positive PnL returns ceil(log(pnl*100+1)), else 0; compresses large gains. prereqs: reward design, log transform.
- **np.ceil():** Smallest integer not less than x. prereqs: numpy.
- **reward_categorical_pnl:** Returns sign of PnL (+1 win, -1 loss). prereqs: reward design.
- **reward_positive_categorical_pnl:** Returns 1 for win, 0 for loss; suited to long-only strategies. prereqs: reward design.
- **reward_exponential_pnl:** Returns exp(PnL); penalizes small PnL changes and rewards large gains exponentially (used in the algorithm). prereqs: reward design, exponential.
- **get_reward():** Computes reward only when the game is over; no reward mid-game. prereqs: reward design, RL.
- **Custom reward systems:** Reward can be based on Sharpe ratio, max drawdown, average return, etc., not just PnL. prereqs: reward design, performance metrics.
---
## MODULE: Game Class
### LESSON: Game Class
- **Game class (full):** Combines position updates, reward design, feature creation, and state assembly into the environment. prereqs: RL environment, OOP.
- **get_state():** Returns the assembled state (candlesticks, indicators, day of week, time of day, position). prereqs: RL, state.
- **act():** Takes an action from the neural network, updates the game, and returns (reward, game_over flag). prereqs: RL, environment.
- **Game over on opposite action:** Passing an action opposite to the current position ends the game and yields the reward. prereqs: RL, trading.
- **Agent as action source:** The neural network (agent) suggests actions; the Game class executes them. prereqs: RL, ANN.
---
## MODULE: Experience Replay
### LESSON: Experience Replay Implementation
- **Experience replay:** Mechanism where the agent stores past experiences and samples them to train the network, breaking correlation and stabilizing learning. prereqs: RL, DQN.
- **Memory / replay buffer:** A list storing experiences (state, action, reward, next state) up to a maximum size. prereqs: RL, DQN.
- **ExperienceReplay class:** Implements `init()` (buffer + max size), `remember()` (add experience, truncate oldest), and `process()` (build input states and target Q-values). prereqs: RL, DQN.
- **remember():** Appends [state_t, action, reward, state_tp1, game_over] to memory; deletes oldest when over max_memory. prereqs: RL, memory buffer.
- **process():** Randomly samples experiences (S.A.R.S: state, action, reward, next state) and computes target Q-values for training. prereqs: RL, DQN.
- **Target Q-value (Bellman update):** Q_new(s,a) = reward_t + discount * max_a' Q(s',a'); for terminal states target = reward_t. prereqs: RL, Bellman equation.
- **Discount rate (gamma):** Tradeoff between immediate reward and future Q-value of the next state (e.g. 0.99). prereqs: RL, Bellman equation.
- **Model R vs Model Q:** Model R provides current Q-values per action (target vector); Model Q provides the max Q-value of the next state. prereqs: DDQN.
- **train_on_batch():** Trains the Q-network on a batch of (inputs, targets) to reduce loss. prereqs: Keras, DQN.
---
## MODULE: Artificial Neural Network Implementation
### LESSON: ANN in Keras
- **Agent (RL):** The learner/decision-maker; in deep RL it is modeled with an Artificial Neural Network (ANN). prereqs: RL, ANN.
- **Double Deep Q-Learning (DDQN):** Uses two identical ANN agents (two Q-tables) trained on different samples to avoid value overestimation, stabilizing and speeding learning. prereqs: DQN, Q-learning.
- **Multi-layer perceptron (MLP):** Feedforward network; data passes once forward, error propagates backward (backpropagation). prereqs: neural network.
- **init_net():** Function defining two identical MLPs (modelR, modelQ) for DDQN. prereqs: Keras, DDQN.
- **ANN input/output dimensions:** Input = state dimension; output = number of actions (buy, sell, hold = 3). prereqs: ANN, RL.
- **Sequential + Dense layers:** Three dense layers (input, hidden, output) in a sequential model. prereqs: Keras, MLP.
- **Softmax output activation:** Converts action scores to a probability distribution over actions. prereqs: activation functions, classification.
- **SGD optimizer (stochastic gradient descent):** Optimizer used to update weights; learning rate controls step size. prereqs: gradient descent, optimization.
- **Learning rate:** Multiplier for gradient steps; how fast the optimizer reaches an optimum. prereqs: optimization, hyperparameters.
- **Loss function (mse):** Quantifies how far predictions are from ground truth. prereqs: loss functions.
- **Activation function (relu):** Adds non-linearity for fitting complex curves. prereqs: activation functions.
- **HIDDEN_MULT:** Multiplier determining hidden layer size relative to input size. prereqs: ANN architecture, hyperparameters.
- **NUM_ACTIONS:** Number of actions the agent can take (buy, sell, hold). prereqs: RL, actions.
- **BATCH_SIZE:** Number of samples trained on at a time. prereqs: training, hyperparameters.
- **Resampling to 1h/1d:** Building hourly and daily bars from 5m data for the multi-granularity state. prereqs: resampling.
- **LKBK (lookback):** Number of bars used as lookback for training. prereqs: time series, hyperparameters.
- **START_IDX:** Initial index of the dataset where the agent starts learning. prereqs: RL, training.
---
## MODULE: Backtesting Implementation
### LESSON: Backtesting Implementation
- **Episode:** Each iteration of exploring the environment (one trade game). prereqs: RL.
- **Epsilon (exploration vs exploitation):** Probability of taking a random action vs the optimal (max Q-value) action; decays over episodes. prereqs: RL, exploration.
- **Epsilon decay (exponential):** epsilon = EPSILON^(log10(episode)) + EPS_MIN, decreasing exploration over time. prereqs: RL, exploration.
- **EPSILON / EPS_MIN:** Initial and minimum epsilon values. prereqs: RL, hyperparameters.
- **MAX_MEM:** Maximum length of the experience replay buffer. prereqs: RL, memory buffer.
- **DISCOUNT_RATE:** Tradeoff between reward and next-state Q-value. prereqs: RL, Bellman equation.
- **run() function:** Trains the agent in the Game environment: initializes env + ANNs + replay buffer, loops over episodes/states, selects actions via epsilon, stores experiences, computes target Q-values, and trains the Q-network. prereqs: RL, DQN, backtesting.
- **Action selection:** If random <= epsilon, pick a random action; else argmax of Q-network prediction. prereqs: RL, exploration.
- **Experience storage:** Adding [state_t, action, reward, state_tp1] to the replay buffer each step. prereqs: RL, memory buffer.
- **Target Q-value computation:** Using modelR and modelQ to compute targets for sampled experiences. prereqs: DDQN, Bellman equation.
- **r_network.set_weights(q_network.get_weights()):** Syncing the R-network weights to the Q-network when a game ends (UPDATE_QR). prereqs: DDQN.
- **Trade logs:** Recording current time, position, and episode for each step. prereqs: backtesting, logging.
- **Saving weights / trade logs / replay buffer:** Periodically persisting model weights, trade logs, and memory to disk. prereqs: serialization, checkpointing.
- **TEST_MODE:** Flag to stop training after a few trades for resource constraints; set False for full runs. prereqs: RL, training.
- **PRELOAD:** Flag to load pre-trained weights and replay memory from disk. prereqs: RL, checkpointing.
---
## MODULE: Performance Analysis_ Synthetic Data
### LESSON: Synthetic Time Series Patterns
- **Synthetic OHLCV:** Simulated price data based on a base signal plus random noise, used to test the RL model. prereqs: simulation, market data.
- **create_synth_ohlc():** Builds synthetic open/high/low/close/volume from a wave `y` plus noise (mult * randn); high/low ~1 unit away; volume fixed at 1000. prereqs: simulation, numpy.
- **Mean-reverting (sine) time series:** Base signal y = 10*sin(0.005*x)+100; tests the model on a mean-reverting pattern. prereqs: mean reversion, simulation.
- **Trending time series:** Base signal y = 0.01*x+100; tests the model on a trending pattern. prereqs: trend, simulation.
- **Mixed time series:** First half sine wave, second half trending; tests regime-shift behavior. prereqs: simulation, regime change.
- **Noise multiplier (mult):** Controls the amount of random noise added to the synthetic signal. prereqs: simulation.
### LESSON: Apply RL on Synthetic Mixed Wave Pattern
- **Running RL on synthetic data:** Applying the run() function to the mixed wave pattern to train the agent and observe strategy performance. prereqs: RL, backtesting.
- **trade_analytics():** Function that joins trade logs with price data, computes strategy returns, cumulative returns, drawdown, and Sharpe ratio. prereqs: performance analysis.
- **Strategy returns:** percent_change * position.shift(1). prereqs: returns, trading.
- **Cumulative strategy returns:** (1 + strategy_returns).cumprod(). prereqs: returns.
- **RL learns sine better than trend:** The model learns the mean-reverting (sine) regime remarkably well but crashes when the regime shifts to trending. prereqs: RL, regime change.
- **Synthetic performance caveat:** Huge synthetic returns (e.g. 2.5×10^5%) are unlikely on real price data. prereqs: backtesting, realism.
---
## MODULE: Performance Analysis_ Real World Price Data
### LESSON: RL Model on Real World Price Data
- **Applying RL to real price data:** Running the RL model on actual 5-minute price data and analyzing strategy performance. prereqs: RL, backtesting.
- **rl_config hyperparameters:** LEARNING_RATE, LOSS_FUNCTION, ACTIVATION_FUN, NUM_ACTIONS, HIDDEN_MULT, DISCOUNT_RATE, LKBK, BATCH_SIZE, MAX_MEM, EPSILON, EPS_MIN, START_IDX. prereqs: RL, hyperparameters.
- **Performance analysis:** Plotting returns and drawdown and computing metrics via trade_analytics(). prereqs: performance analysis.
- **Drawdown metrics:** Percentage decline from running maximum of cumulative returns; max drawdown reported. prereqs: performance metrics.
- **Sharpe ratio (5-min bars):** mean/std * sqrt(252*78) since 5-minute time steps. prereqs: Sharpe ratio, risk.
- **Portfolio return:** Final cumulative strategy return minus 1. prereqs: returns.
- **Model robustness to crashes:** The RL model handles market crashes (2019 flat, 2020 drawdown recovery) reasonably well. prereqs: RL, risk.
---
## MODULE: Capstone Project
### LESSON: Model Solution Template_ Building the RL Model
- **Capstone RL model template:** A structured template to build a reinforcement learning model for the capstone project; must be calibrated per underlying asset. prereqs: RL, project workflow.
- **Data sanity check:** Checking for missing values and outliers; fixing data or obtaining good-quality data. prereqs: data quality.
- **Input features (extendable):** Statistical (beta of high/low), overlap studies (EMA instead of SMA), volatility (ATR), and other-asset data (On Balance Volume). prereqs: feature engineering, technical analysis.
- **Average True Range (ATR):** Volatility indicator measuring average true range of price. prereqs: technical indicators.
- **On Balance Volume (OBV):** Volume-based indicator. prereqs: technical indicators.
- **Reward function selection:** Choosing/creating a reward function based on the desired outcome. prereqs: reward design.
- **Recency sampling vs uniform random sampling:** Sampling the N most recent experiences from the buffer (recency) as a baseline vs uniform random sampling; used to assess the impact of experience replay. prereqs: experience replay, sampling.
- **Backtesting function (run):** The run() function trains the RL agent on historical data. prereqs: RL, backtesting.
### LESSON: Model Solution_ Combining the Agents
- **Combining RL agents:** Running the RL algorithm multiple times to obtain several agents, then building a strategy by allocating portfolio weights based on recent performance. prereqs: RL, portfolio construction.
- **Loading trained agents:** Reading each agent's trade logs and computing its strategy returns. prereqs: backtesting, serialization.
- **Agent selection:** Selecting agents on performance parameters (Sharpe, drawdown) or by return correlation (least correlated). prereqs: portfolio construction.
- **Rolling performance:** Computing positive rolling returns (window e.g. 30000 bars); negative returns set to 0 to avoid incorrect weight allocation. prereqs: performance analysis.
- **Weight allocation:** Portfolio weight = agent rolling return / sum of all agents' rolling returns; updated every N bars (e.g. 1500). prereqs: portfolio construction.
- **Strategy returns:** Sum over agents of (agent returns * weight.shift(1)). prereqs: portfolio construction.
- **pyfolio tear sheet:** Generating performance metrics with `pf.create_simple_tear_sheet()`. prereqs: performance analysis.
- **Combination benefit:** A combination of agents performs better overall than selecting a single best agent. prereqs: portfolio construction, diversification.
---
## MODULE: data_modules (supporting module)
- **Reward functions:** get_pnl, reward_pos_log_pnl, reward_pure_pnl, reward_positive_pnl, reward_categorical_pnl, reward_positive_categorical_pnl, reward_exponential_pnl. prereqs: reward design.
- **Game class (module):** Full environment with _update_position, _assemble_state, _get_last_N_timebars, _get_reward, get_state, act, reset. prereqs: RL environment, OOP.
- **_assemble_state():** Builds the state from normalized candlesticks (5m/1h/1d), technical indicators (SMA diff, RSI, MOM, BOP, Aroon), time signature, and position. prereqs: feature engineering, RL.
- **_get_last_N_timebars():** Gets last N bars for 5m/1h/1d resolutions based on lookback. prereqs: time series.
- **_get_reward():** Computes reward via the reward function only when the game is over. prereqs: reward design.
- **act():** Updates position, computes unrealized/realized PnL, and returns (reward, game_over). prereqs: RL, trading.
- **reset():** Resets game state and resamples bars for a new trade. prereqs: RL episode.
- **init_net():** Creates two identical MLPs (modelQ, modelR) for DDQN. prereqs: Keras, DDQN.
- **ExperienceReplay class:** remember() + process() implementing the replay buffer and Bellman target computation. prereqs: RL, DQN.
- **run():** Full training/backtesting loop over episodes with epsilon-greedy action selection and Q-network updates. prereqs: RL, DQN.
- **drawdown_metrics():** Computes and plots drawdown; returns max drawdown. prereqs: performance metrics.
- **trade_analytics():** Computes strategy returns, cumulative returns, drawdown, portfolio return, and Sharpe ratio from trade logs. prereqs: performance analysis.
---
## Deep-Reinforcement-Learning-in-Trading — Section-based course structure
# — Deep Reinforcement Learning in Trading — Concept Inventory
**Track:** 5 — Artificial Intelligence in Trading (Advanced)
**Media note:** PDFs + resource/template zips only (no mp4s in folder).
**Overlap with D: notebooks:** the D: side carries a notebook-based treatment of the same RL trading pipeline (agent scaffolding via ANN, replay buffer, backtesting, capstone); this course is organised as an narrative walkthrough (RL foundations → ANN → backtest → automate → paper/live → capstone).
## COURSE
Build an end-to-end deep-Q reinforcement-learning trading agent: model a trading problem as an MDP-like (state → action → reward) Q-learning loop, construct and assemble a state from price/indicator data, define trade positions and reward, replay experiences to stabilise learning, express the value function as an **artificial neural network (deep Q network)**, define backtesting logic (price, transaction cost, execution), then move to paper/live trading and a capstone that swaps in your own asset/minute data.
## Course Prerequisite Map
- **Section 1 Introduction:** none (course map). Strongly consume prior ML/classification & Python-of-ML track courses.
- **Section 4 Q Learning :** (no prereqs) — foundation for all subsequent RL sections.
- **Section 5 State construction requires:** Section 4 (state concept) + feature/indicator engineering.
- **Section 6 Policies requires:** Section 4; π(state)→action mapping, exploration vs exploitation.
- **Section 9 Positions & Rewards requires:** Sections 5–6 (how the agent acts) + PnL.
- **Section 11 Construct/Assemble State requires:** Sections 5 & 9 + `talib` (installed). Deepens the state vector with indicators and returns.
- **Section 13 Experience Replay requires:** Section 4/5 (transition tuples) + replay-buffer concept.
- **Section 14 ANN Concepts requires:** Section 13 (DQN needs a learning target) + neural-network basics (gradient descent).
- **Section 15 ANN Implementation requires:** Section 14 + Keras/TensorFlow env.
- **Section 16 Backtesting Logic requires:** Sections 9–15 (a trained policy + reward to replay) + trade-level the logic needed to be modelled.
- **Section 17 Backtesting Implementation requires:** Section 16 + the ANN agent/model files.
- **Section 19 Performance Analysis requires:** Sections 11–17 (real price data + model rollout).
- **Section 20 Automated Trading requires:** Section 19 (minute data) + IBridgePy/broker connect.
- **Section 21 Paper & Live Trading requires:** Section 20 + template.
- **Section 22 Capstone requires:** all of the above (project on your own asset/minute data).
- **Section 23 Future Enhancements & 25 Summary:** no new prereqs.
---
### Section 1 — Introduction
- **CONCEPT:** Course structure — the RL-agent pipeline from Q-learning foundations through ANN-based DQN, backtesting, automation, and live deployment. prereqs: none.
### Section 4 — Q Learning
- **CONCEPT:** Q-learning — model-free RL where an agent learns an action-value `Q(s,a)` (expected future return of taking action a in state s) and updates it toward the best next-state value; the backbone for DQN/A3C-style algorithms and DeepMind breakthroughs. prereqs: RL MDP vocabulary, state/action/reward.
- **CONCEPT:** Bellman update / temporal difference — the Q-value update target relating current estimate to reward + discounted next-state maximum. prereqs: Section 4 Q-table.
### Section 5 — State Construction
- **CONCEPT:** State — data the agent uses to decide action; must contain all info needed for prediction, simplified from the raw market stream. prereqs: Section 4 + features.
- **CONCEPT:** Why state quality matters — the behavioural-IRL cautionary frame (individual investors underperform; sell winners/hold losers) motivating engineered features. prereqs: trading behaviour awareness, Section 5.
### Section 6 — Policies in Reinforcement Learning
- **CONCEPT:** Policy π — the mapping from state to action the agent follows; RL balances **exploration** (trying new actions) vs **exploitation** (using the current best policy) — the core RL trade-off. prereqs: Section 4/5.
### Section 9 — Positions and Rewards
- **CONCEPT:** Reward design — the scalar feedback the agent optimises; for trading often a PnL/aware-shape; reward should align with profitable behaviour. prereqs: Section 5–6, PnL.
- **CONCEPT:** Volatility-scaled rewards — position scaled by market volatility to make reward more stable for continuous futures/FX. prereqs: Section 9 + volatility.
### Section 11 — Construct and Assemble State
- **CONCEPT:** Assembling the state vector — gather price/indicator (ta-lib: technical indicator library) features into the state fed to the agent. **pip install TA-Lib** (/windows/mac) prerequisite reading. prereqs: Section 5 state + indicator definitions.
### Section 13 — Experience Replay
- **CONCEPT:** Experience replay — store (state, action, reward, next-state) transitions in a replay buffer and sample batches uniformly for training, decoupling data correlation. prereqs: Q-learning/transition tuples.
- **CONCEPT:** Replay capacity/pro-portions — the replay ratio (learning updates vs experience collected) and buffer size must be tuned; too large a buffer can hurt DQN performance. prereqs: Section 13 + batch training.
### Section 14 — Artificial Neural Network Concepts
- **CONCEPT:** The ANN as a value function — represents the Q/mode value approximated across states; training via **gradient descent** on a loss between predicted and target Q. prereqs: neural net basics + gradients.
- **CONCEPT:** Gradient descent — the algorithm that minimises the network loss by stepping against gradients; why GD is central to training a DQN. prereqs: calculus (derivative, chain rule), forward/backprop.
### Section 15 — Artificial Neural Network Implementation
- **CONCEPT:** ANN agent implementation — build the Q-network in Keras/TensorFlow (versions 2.2.4 / 1.12.0 pinned); setup requires Visual Studio on Windows; two Q-tables/Double DQN of moving targets & maximisation bias mitigation. prereqs: Section 14 + TF/Keras env.
- **CONCEPT:** DQN vs Double-DQN boundary — using two Q-value tables (target/online) to reduce maximisation bias. prereqs: Section 15.
### Section 16 — Backtesting Logic
- **CONCEPT:** Backtesting logic — the model-priced simulation step: iterate bars sequentially, decide position via the agent (get prediction from ANN), apply costs, and carry the PnL. (PDF `Backtesting Logic.pdf` describes this loop.) prereqs: trained policy + state + reward.
### Section 17 — Backtesting Implementation
- **CONCEPT:** Backtest the trained agent on historical data — replay historical price bars, let the agent make position decisions, with sanity checks; produces `indicator_model.h5` (ANN weights) + `replay_buffer.bz2`. prereqs: Section 16 logic + Section 15 model.
### Section 19 — Performance Analysis (Real-World Price Data)
- **CONCEPT:** Model rollout on live/real price data — evaluate the trained DQN on minutely/real data; compare equity/CAGR vs buy-and-hold; discusses asset-appropriate and data-source FAQ. prereqs: Section 17 + minute data.
### Section 20 — Automated Trading Strategy
- **CONCEPT:** Automated execution of trades — connect to a broker (Trader Workstation for IBKR, IBroute Py), load the algorithm, stream live data, generate signals, place orders — the live execution flow. prereqs: trained model + broker account/IBridgePy.
- **CONCEPT:** IBridgePy / automated paper account practice — placing orders in a demo/paper/live Interactive Brokers (or TD Ameritrade/Robinhood) account. prereqs: broker setup.
### Section 21 — Paper and Live Trading
### Section 22 — Capstone Project
- **CONCEPT:** Capstone problem statement — build an advanced DRL model for your own asset (minute data; FX pair sample given); data sanity checks, add input features in `assemble_state`, train, download template/capstone solution `.zip`. prereqs: all prior.
### Section 23 — Future Enhancements
- **CONCEPT:** Future directions — deep RL for asset allocation; RL survey; reward-free exploration paving ways beyond this course. prereqs: capstone.
### Section 25 — Course Summary
- **CONCEPT:** Resources recap — the full `Deep-Reinforcement-Learning-in-Trading-Resources.zip` (RL env, time, template) bringing the pipeline together. prereqs: entire course.