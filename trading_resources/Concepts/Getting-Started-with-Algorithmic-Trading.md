## COURSE: Getting Started with Algorithmic Trading
### MODULE: Introduction to Python
#### NOTEBOOK: My First Jupyter Notebook
- **Programming** — The task of telling a machine (computer/phone) what to do by writing software; synonymous with coding/developing. prereqs: none
- **Jupyter Notebook** — An interactive document combining markdown text and runnable code cells for learning/analysis. prereqs: none
- **Code cells & Markdown cells** — Two cell types in a notebook; markdown holds explanatory text, code holds executable Python. prereqs: Jupyter Notebook
- **Shift+Enter to run a cell** — The keyboard shortcut that executes the current notebook cell. prereqs: Jupyter Notebook
- **Simple Python syntax** — Python reads like English, prioritising coding productivity and readability; portable across platforms. prereqs: none
- **Code comments (#)** — Non-executable notes prefixed with `#` that explain code and are ignored when run; anything after `#` is commented out. prereqs: Python syntax
- **Multi-line comments (triple quotes)** — Text wrapped in `"""..."""` is not executed and serves as a multi-line comment. prereqs: Python syntax
- **Print statement** — `print("...")` outputs text/values to the console. prereqs: Python syntax
- **Variables** — Named storage of values that can be reused; Python variables can hold different data types. prereqs: Programming
- **Assignment `=` semantics** — The `=` sign means "is set to", not "equal to". prereqs: Variables
- **Integer (int)** — A whole number data type, positive or negative; `type()` returns `int`. prereqs: Variables
- **Float** — A real-number (decimal) data type; defined as `5.0` or via `float(5)`. prereqs: Variables
- **String** — A data type for text (alphabets, numbers, special chars) wrapped in single or double quotes. prereqs: Variables
- **Case sensitivity** — Python distinguishes variable names differing only by case (e.g. `gold_price` vs `Gold_Price`). prereqs: Variables
- **type() function** — Built-in that returns the data type of a value/object. prereqs: Variables
- **Indentation** — Python requires consistent indentation (spaces) for block structure; inconsistent indents raise `IndentationError`. prereqs: Python syntax
- **Exponentiation operator `**`** — Raises a number to a power (e.g. `3**2 == 9`). prereqs: Python basics
- **Simple returns** — Percentage change in price over a period: `(Final/Initial - 1) * 100`. prereqs: Variables, arithmetic
- **Log returns** — Natural log of `final/initial`, computed with `math.log(price_2/price_1)`. prereqs: Simple returns, math import
- **import math** — Bringing in the standard `math` library to use functions like `log()`. prereqs: Functions, libraries
#### NOTEBOOK: Operations and Functions in Python
- **Arithmetic operators** — Basic operations `+ - * /` performed on numbers/variables. prereqs: Python basics
- **Exponentiation operator `**`** — Computes a number raised to a power. prereqs: Arithmetic
- **Modulo operator `%`** — Returns the remainder of a division (e.g. `15 % 4 == 3`). prereqs: Arithmetic
- **Built-in math functions** — `abs()`, `round()`, `max()`, `min()`, `sum()` operated on numbers. prereqs: Python basics
- **import keyword** — Loads a library (`import math`) so its functions become available. prereqs: Python basics
- **math package constants/functions** — `math.pi` (π), `math.e` (Euler's constant), `math.cos()`. prereqs: import math
- **Comparison (relational) operators** — `==`, `!=`, `<`, `>`, `<=`, `>=` return booleans `True`/`False`. prereqs: Python basics
- **Boolean results** — Logical/comparison operations evaluate to `True` or `False`. prereqs: Comparison operators
- **Logical operators** — `not` (negation), `and` (both true), `or` (either true); combined per a truth table. prereqs: Booleans
- **Equality `==`** — Compares two values, returning `True` if equal, `False` otherwise. prereqs: Comparison operators
- **Functions** — Reusable blocks of code defined with `def` that can be called repeatedly for clean, modular code. prereqs: Python syntax
- **Function definition & call** — `def name():` begins a function; calling `name()` executes its body. prereqs: Functions
- **Function parameters** — Input values placed inside parentheses in the definition, separated by commas, used by the function body. prereqs: Functions
- **return statement** — Exits a function and hands a value back to the caller for storage in an outer variable. prereqs: Functions
- **Variable scope** — The region of code where a variable is accessible; variables defined inside a function are local to it. prereqs: Functions
- **Scope error (NameError)** — Referencing a function-local variable outside raises `NameError: name not defined`. prereqs: Variable scope
#### NOTEBOOK: DataFrame and Basic Functionality
- **DataFrame** — pandas' tabular/spreadsheet-like structure storing data in named rows and columns. prereqs: Pandas
- **import pandas as pd** — Importing the pandas library under the alias `pd`. prereqs: Python
- **pd.DataFrame() constructor** — Creates a DataFrame from data (e.g. a dict of lists), optionally with index. prereqs: pandas
- **Columns & index** — Columns are named fields; the index is the row-label sequence (default 0..n). prereqs: DataFrame
- **set_index()** — Assigns a column's values as the DataFrame's index for label-based access. prereqs: DataFrame
- **pd.read_csv()** — Loads a CSV file into a DataFrame; `index_col` sets an index column. prereqs: pandas
- **head() / tail()** — Display the first/last n rows (default 5) to preview data. prereqs: DataFrame
- **loc[]** — Label-based row/index access; both start and stop labels are included. prereqs: pandas indexing
- **iloc[]** — Position-based row access by integer position (0-indexed); the stop index is excluded. prereqs: pandas indexing
- **Boolean indexing** — Filtering a DataFrame with a boolean condition (e.g. `df[df.quantity > 5000]`). prereqs: DataFrame
- **Accessing columns** — Reference a column by its name via `df["colname"]`. prereqs: DataFrame
- **drop()** — Removes rows (by index position) or columns (`axis=1`), optionally saving in place. prereqs: DataFrame
- **axis parameter** — Specifies whether to operate along rows (0/"index") or columns (1/"columns"). prereqs: pandas
- **Adding a column** — `df["new_col"] = expression` creates a computed field, e.g. a moving average. prereqs: DataFrame
- **rolling() + mean()** — The `.rolling(window=N).mean()` construct computes an N-period simple moving average. prereqs: pandas, DataFrame columns
- **Simple Moving Average (SMA)** — The mean of the last N observations at each point in a time series. prereqs: rolling()
### MODULE: Financial Market Data and Visualisation
#### NOTEBOOK: Importing Time Series Data
- **yfinance** — A Python package for fetching financial data from Yahoo Finance. prereqs: pip, Python
- **pip install** — The tool/command that installs and manages Python packages. prereqs: none
- **yf.download(ticker, start, end)** — Downloads OHLCV data for a ticker between given dates into a DataFrame. prereqs: yfinance
- **Ticker** — The exchange symbol identifying a stock/asset (e.g. 'KO' for Coca Cola). prereqs: yfinance
- **auto_adjust parameter** — When `True`, yfinance returns split/dividend-adjusted price data (default `False`). prereqs: yf.download
- **Adjusted close price** — Closing price restated for corporate actions (splits/dividends). prereqs: adjusted data
- **CSV file** — A Comma-Separated-Value text file storing tabular data; readable via `pd.read_csv()`. prereqs: pandas
- **Financial time series data** — Ordered daily price data (open/high/low/close/volume) indexed by date. prereqs: CSV
- **pd.to_datetime()** — Converts a date column/index to datetime type for easier date operations. prereqs: pandas
- **Datetime index** — Using a parsed datetime column as the DataFrame index enables time-series operations. prereqs: pd.to_datetime
#### NOTEBOOK: Data Visualisation
- **Data visualisation** — Graphical representation (charts/graphs) of data to draw insights. prereqs: none
- **matplotlib** — The Python plotting library; commonly imported as `matplotlib.pyplot as plt`. prereqs: Python
- **%matplotlib inline** — Magic command rendering graphs inline within a notebook. prereqs: matplotlib
- **plt.style.use()** — Sets a global plotting style (e.g. 'seaborn-v0_8-darkgrid'); options in `plt.style.available`. prereqs: matplotlib
- **Line graph** — A plot of a continuous series; in pandas via `dataframe.column.plot(figsize, color)`. prereqs: matplotlib
- **Plot decorators** — `plt.title()`, `plt.xlabel()`, `plt.ylabel()`, and `plt.show()` label and display a chart. prereqs: matplotlib
- **figsize & color params** — Control plot dimensions (x,y) and line colour. prereqs: line graph
- **Scatter plot** — `plt.scatter(x, y)` plots two variables against each other to study relationships. prereqs: matplotlib
- **Histogram** — `data["col"].plot(kind='hist')` shows the frequency distribution of a numeric column. prereqs: pandas plot
- **Insights from charts** — Reading ranges, co-movement, and distribution shape from plotted data. prereqs: line/scatter/hist
### MODULE: Moving Average Crossover Strategy
#### NOTEBOOK: Moving Average Crossover Strategy
- **Momentum** — Persistence of a trend/returns in a particular direction in an asset's price. prereqs: none
- **numpy (np) & pandas (pd)** — Core numerical and dataframe libraries used in strategy work. prereqs: Python
- **warnings.filterwarnings('ignore')** — Suppresses warning messages during analysis. prereqs: Python
- **Slicing data columns** — Retaining only desired columns (e.g. `data[['Adj Close']]`). prereqs: DataFrame
- **rolling()/mean() for SMA** — Computes short- and long-term moving averages with window sizes. prereqs: pandas rolling
- **Short-term vs long-term window** — Window sizes (40 and 70 days) defining fast vs slow averages. prereqs: rolling()
- **Moving-average crossover logic** — Buy when the short-term average rises above the long-term average; sell when it falls back. prereqs: moving averages
- **np.where(condition, if_true, if_false)** — Element-wise array selection assigning signal values (1 buy / −1 sell). prereqs: numpy
- **shift() to lag signals** — Shifting the signal forward one day so the trade executes the next day, avoiding lookahead. prereqs: pandas
- **Replace NaN with 0** — `series.replace(np.nan, 0)` cleans the first-day missing signal value. prereqs: pandas
- **pct_change()** — Computes the daily percentage change `(today - yesterday)/yesterday`. prereqs: pandas
- **Strategy returns** — Daily strategy return = signal (previous day) × daily price change. prereqs: pct_change
- **Trading cost / commission** — Charging a fixed commission on position changes: `0.001*|signal - shifted-signal|`. prereqs: strategy returns
- **Buy & hold strategy** — Simply purchasing and holding the asset; used as a comparison baseline. prereqs: none
- **Cumulative returns** — Running product of `(1+return)` via `.cumprod()`, showing total growth over time. prereqs: strategy returns
- **prod()** — Multiplicative product of all elements, giving the final cumulative growth factor. prereqs: cumprod
- **Yearly annualisation (252)** — Multiplying daily stats by `sqrt(252)` to annualise to ≈ number of trading days/year. prereqs: Sharpe ratio
- **Standard deviation (risk)** — Measures average dispersion/movement of prices; proxies uncertainty/risk. prereqs: statistics
- **Sharpe ratio** — Average excess return per unit of risk: `(mean / std) * sqrt(252)`. prereqs: mean, std, annualisation
- **Drawdown** — Decline of cumulative returns from a previous running peak, quoted as a percentage drop. prereqs: cumulative returns
- **Cumulative maximum** — `np.maximum.accumulate()` tracks the running maximum of a series (peak). prereqs: numpy
- **Maximum drawdown** — The deepest peak-to-trough percentage loss of the equity curve. prereqs: drawdown
- **plt.fill_between()** — Shading the area under a drawdown curve to visualise loss regions. prereqs: matplotlib
---
## Getting-Started-with-Algorithmic-Trading — Section-based course structure
# Concept Inventory — Getting Started with Algorithmic Trading
## COURSE: Getting Started with Algorithmic Trading
### Section: Section 1 - Introduction
- **Introduction / course structure:** overview of what algorithmic trading is and how the course is organised. prereqs: none.
### Section: Section 2 - What is Algorithmic Trading
- **What is algorithmic trading:** using automated programs executing trades based on predefined rules. prereqs: none.
- **Direct Market Access (DMA):** connecting directly to an exchange to place orders with reduced latency. prereqs: algo trading.
- **What is high-frequency trading (HFT):** ultra-fast automated trading exploiting small latency advantages. prereqs: algo trading; DMA.
### Section: Section 3 - Why Algorithmic Trading
- **Why go algo (parts 1–3):** benefits — speed, discipline, backtestability, removal of human emotion. prereqs: what is algo.
- **How to start algorithmic trading:** practical first steps (learning, platforms, small strategies). prereqs: why algo.
### Section: Section 4 - Available Platforms & Languages
- **Available platforms & languages:** Python, C++, R, broker APIs, backtesting libraries. prereqs: what is algo.
### Section: Section 5 - Strategy Paradigms
- **Types of algorithmic trading strategies:** broad taxonomy. prereqs: what is algo.
- **Market making strategy:** posting bids/asks to profit from the spread. prereqs: strategy types.
- **Momentum based strategies:** trading on trend/momentum signals. prereqs: strategy types.
- **Statistical arbitrage:** exploiting statistical mispricings between related instruments. prereqs: strategy types.
- **Machine-readable news & ML:** using news & machine learning in strategies. prereqs: strategy types.
### Section: Section 6 - Algorithmic Trading Platform
- **Algorithmic Trading Platform (ATP):** three core functions — receive data, analyse/decide, place orders. prereqs: what is algo.
- **Server:** core hardware/software infra of an ATP. prereqs: ATP.
- **Market Data Adapter (MDA):** handles incoming exchange data feeds. prereqs: ATP; server.
- **Complex Event Processing (CEP) Engine:** real-time analysis/decision engine. prereqs: ATP.
- **Order Routing/Management System (OMS):** routes and manages orders to exchange. prereqs: ATP; server.
### Section: Section 8 - Financial Market Data and Visualisation
- **Importing data:** fetching price/volume/fundamental data via Python APIs. (Financial Market Data) prereqs: Python basics.
- **Market data & analysis in Python:** working with price, volume, fundamental data. prereqs: importing data.
- **Data cleaning basics:** handling incomplete/erroneous data. prereqs: importing data.
- **Data sources:** free vs paid market data APIs; fundamental & sentiment feeds. prereqs: importing data.
### Section: Section 9 - Moving Average Crossover Strategy
- **Moving average crossover strategy:** long/short on short-period MA crossing long-period MA. prereqs: market data; strategy paradigms.
### Section: Section 12 - Regulations & Compliance (Optional Section)
- **Regulations & compliance (SEBI, India):** audit requirements, order limits (>20/s penalised), India-routed orders, approved IDs. prereqs: algo trading foundations.
- **Global regulation snapshots:** EU, US algo/commodity (CFTC/CME) regulations. prereqs: regulations.
### Section: Section 14 - Summary
- **Summary / course recap:** recap of all concepts, trading desk FAQ. prereqs: all sections.
- **Setting up a trading desk (FAQs):** capital, licensing, infrastructure, human-resource skills (stats, programming, markets, compliance). prereqs: summary.
- **Handbook:** × MCX intro reference. prereqs: none (annexure).
## Course Prerequisite Map
- Foundations: *What is Algo → DMA → HFT; Why Algo → How to start.*
- Platforms: *Available Platforms → Strategy Paradigms → Moving Average Crossover (needs returns + MA).*
- Infrastructure: *What is Algo → ATP (Server → MDA/CEP/OMS).*
- Data: *Python basics → Importing Data → Market Analysis → Visualisation.*
- Compliance is optional and standalone (after fundamentals).
- Course flow: **Intro → What is Algo/DMA/HFT → Why → Platforms → Strategy Paradigms → Platform Architecture → Market Data → MA Crossover → [Regulations] → Summary/Handbook.**
- FunPath basics feeding this course: Python for trading, return calculation, moving averages, basic market structure.