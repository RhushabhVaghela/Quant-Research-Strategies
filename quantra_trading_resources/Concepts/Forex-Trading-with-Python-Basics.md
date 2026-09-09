# Concept Inventory: Forex Trading using Python - Basics
> Inventory source: 1 PDF (` Blueshift Utility Functions.pdf`), 1 Python strategy (`forex_basic_code.py`). No section subfolders exist in this course folder — course content is flat (single unit).
## COURSE
Introductory course on building & backtesting a simple algorithmic forex trading (currency-pair rebalancing) strategy on the Blueshift platform, which is built on **Zipline**. Focus is on the Blueshift API function set (initialize / scheduling / data fetching / order placement) and a working momentum-style multi-currency-pair rebalance strategy. The content corresponds to roughly the first unit of a larger forex algorithmic-trading stream.
### Section: (Course unit) — Blueshift Utility Functions (platform API)
Source: ` Blueshift Utility Functions.pdf` • Course code: `forex_core.py`
- Blueshift is built on Zipline (Pythonic algorithmic trading/backtesting library).
- `zipline.api` basic functions underpin every strategy on the platform.
- **Initialize function**
 - `initialize(context)` called once before strategy start; passed a `context` object.
 - `context` is a persistent namespace for storing variables accessible from anywhere in the algorithm (lookback, currency list, etc.).
- **Optional functions**
 - `before_trading_start(context, data)` — called before the market opens (pre-market setup).
 - `handle_data(context, data)` — called **every minute**; receives current trading bar OHLC + volume for all currency pairs.
 - `schedule_function(...)` — schedule a named function to run on chosen days/times.
 - `date_rules`: `every_day`, `week_start`, `week_end`, `month_start`, `month_end`; supports `days_offset`.
 - `time_rules`: `market_open`, `market_close`; supports `hours` / `minutes` offsets.
 - `set_account_currency('USD')` — set base/PnL currency.
 - `get_datetime()` — current strategy datetime.
- **Data fetching — `data.history(...)`**
 - `assets` = currency-pair symbol or iterable of symbols (string notational).
 - `fields` = 'price', 'open', 'high', 'low', 'close', 'volume'.
 - `bar_count` = integer number of bars/sub-sample.
 - `frequency` = '1m' (minute) or '1d' (daily); for other frequencies use pandas `resample`.
 - Returns a pandas Series / DataFrame / Panel indexed by date.
 - 'price' field is forward-filled (last known price, else NaN).
- **Order placement**
 - `order_target_percent(symbol, target_pct)` — rebalance a currency pair to a target portfolio weight (supports long/short via +/- percentages; 0 = flat entry).
- **Strategy logic (from `forex_cross.py`)**
 - Currency pairs list: AUD/USD, EUR/USD, GBP/USD, NZD/USD, USD/CHF, USD/CAD, USD/JPY.
 - `context.lookback = 50` days; fetch daily 'close' bars.
 - Compute returns over lookback = `iloc[-1]/iloc[0] - 1`; sort descending by return.
 - **Long** the top-3 pairs (weight 1/6 each), **Short** the bottom-3 pairs (weight -1/6 each), flat (0) the middle (4th) pair — a simple momentum/reversal rebalance.
 - Rebalance weekly at `week_start`, market_open +15min.
### Prerequisites (for this unit)
- Basic familiarity with Zipline OR willingness to learn its API surface.
- Working knowledge of pandas DataFrame indexing/slicing (`iloc`), pandas resample.
- Understanding of currency-pair symbols (FX convention AUD/USD etc.).
- Basic Python function definitions and module imports.
## Course Prerequisite Map
- **Python fundamentals** → pandas data structures (Series/DataFrame) → `data.history` return shapes.
- **Zipline/event-loop model** → initialize/before_trading_start/handle_data lifecycle.
- **Portfolio/weight math incl. MPT & position sizing concepts (Track 7 / Track 1 level)** → `order_target_percent` rebalancing weights per pair.
- **Forex market basics** → currency pair ticks, bid/ask/OHLC, '1d' vs '1m' frequency, pricing marks.
- No formal folder-level prerequisite chain exists in this course (single unit).
---
*Notes on D (duplicate/overlap) with other tracks*: Blueshift/Zipline API concepts overlap with Track 1 (Algorithmic Trading for Beginners) strategy skeleton material; momentum/reversal pair rebalancing overlaps Track 3 and Track 6 (Value Strategy in Forex) weight-selection logic.