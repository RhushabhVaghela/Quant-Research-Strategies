# Algo Trading with Zerodha (Kite Connect) — Concept Inventory
## COURSE: AlgoTradingZerodhaResources
A () course on building automated trading systems in Python against the Zerodha Kite Connect API (and KiteTicker WebSocket). Covers authentication/session management, instrument lists, market quotes (LTP/OHLC/full quote), API rate limiting & batching, historical data & resampling, derivatives/Open Interest, order types (regular, stop-loss SL/SL-M, cover CO, GTT, AMO, Iceberg), order management, positions & holdings, WebSocket live streaming, SMA/crossover trading signals, a low-frequency polling system, and a full end-to-end automated trading system.
Notebooks enumerated (20): `KiteConnect Authentication`, `Storing and Reusing the Access Token`, `Fetching Full Instrument Lists`, `Fetching Live Quotes with Kite Connect`, `API Rate Limiting and Optimization Strategies`, `Fetching and Resampling Historical Data`, `Access Historical Derivatives Data and Analysing Open Interest`, `Streaming Live Market Data`, `Calculation of SMA Using Websockets`, `Trading Signal`, `Placing Your First Trade with Kite Connect`, `Monitoring and Managing Orders`, `Stop-Loss Orders`, `Cover Orders`, `GTT and AMO`, `Iceberg Orders`, `Managing Trading Positions with KiteConnect`, `Managing Portfolio Holdings with KiteConnect`, `Low Frequency Trading System`, `A Complete Automated Trading System`.
No local Python modules — relies on the external `kiteconnect` package (`KiteConnect`, `KiteTicker`) plus `pandas`, `matplotlib`.
---
## MODULE: API Login and Session Management
### LESSON: KiteConnect Authentication
- **KiteConnect API** — Zerodha's REST-like API giving programmatic access to a trading account (historical data, portfolio/funds, live order placement). prereqs: none.
- **`kiteconnect` Python package** — abstraction over HTTP calls; JSON responses returned as native Python structures. prereqs: none.
- **Installation** — `pip install kiteconnect`. prereqs: pip.
- **API key & API secret** — credentials from a developer-account app; treat like passwords (environment variables / config, never hardcoded). prereqs: none.
- **`login_url()`** — generates the manual-login URL. prereqs: KiteConnect init.
- **`request_token`** — one-time token captured from the redirect URL query string after browser login (User ID + Password + TOTP). prereqs: login_url.
- **`kite.generate_session(request_token)`** — exchanges `request_token` for the `access_token` used for all subsequent API calls. prereqs: request_token.
- **Authentication flow** — API key → login URL → request_token → session → access_token. prereqs: all above.
### LESSON: Storing and Reusing the Access Token
- **`access_token` lifetime** — valid for the full trading day; reusing avoids repeated manual logins. prereqs: access_token.
- **Storing the access token** — save `access_token` to a local file (e.g. `access_token.txt`) in the notebook folder for reuse. prereqs: access_token.
- **Reuse with fallback** — on run, load the saved token; on failure/expiry fall back to full manual login. prereqs: access_token.
- **`kite.profile()`** — fetches account profile details using the stored token. prereqs: authenticated kite object.
- **`kite.margins('equity')`** — fetches funds and margins data for a segment. prereqs: authenticated kite object.
- **`kite.logout()`** — invalidates the current access_token and ends the programmatic session; subsequent calls fail with auth errors. prereqs: access_token.
## MODULE: Fetching Market Quotes
### LESSON: Fetching Full Instrument Lists
- **Instrument master** — the full list of all tradable instruments (stocks, indices, commodities, derivatives) via a single API call. prereqs: none.
- **`kite.instruments()`** — downloads the complete instrument list (list of dicts). prereqs: authenticated kite object.
- **Instruments to DataFrame** — load the list into a pandas DataFrame for querying. prereqs: pandas.
- **`instrument_token`** — unique numeric id needed for orders, historical data, and live subscriptions (found from the instrument list). prereqs: instrument master.
- **Filtering by exchange** — filter the `exchange` column for NSE (equities), NFO (futures & options), MCX (commodities). prereqs: instrument DataFrame.
- **KiteAuth helper class** — reusable class wrapping the manual login (URL → request_token → access_token). prereqs: authentication.
### LESSON: Fetching Live Quotes with Kite Connect
- **Instrument symbol format** — `EXCHANGE:TRADINGSYMBOL` (e.g. `NSE:INFY`). prereqs: instrument master.
- **LTP (Last Traded Price)** — quickest price call; `kite.ltp()` returns dict of `instrument_token` + `last_price`. prereqs: authenticated kite object.
- **OHLC quotes** — day's open, high, low, and previous close; `kite.ohlc()`. prereqs: LTP.
- **Full quote** — comprehensive packet (OHLC, LTP, volume, average traded price, market depth of top-5 bids/asks); `kite.quote()`. prereqs: OHLC.
- **Market depth** — top-5 pending bids/asks used for limit-vs-market order decisions and liquidity assessment. prereqs: full quote.
- **When to use each format** — LTP for dashboards/watchlists; OHLC for daily/candlestick analysis; full quote for order-placement logic. prereqs: quote formats.
- **Polling vs streaming** — quote functions are polling-based; tick-by-tick needs the WebSocket API. prereqs: quote formats.
### LESSON: API Rate Limiting and Optimization Strategies
- **API rate limits** — servers cap requests/second for stability & fair use; Kite limits ~10 requests/second, exceeding triggers errors (HTTP 429 / `TokenException`). prereqs: none.
- **Consequences of ignoring limits** — requests get blocked and the application breaks. prereqs: rate limits.
- **Batch processing** — request multiple instruments in one call (`ltp`, `ohlc`, `quote` all support it); the single most effective optimization. prereqs: quote functions.
- **Throttling** — introduce `time.sleep()` delays between polling calls to stay within the rate limit. prereqs: polling.
- **Prefer WebSockets for high frequency** — streams push data instead of repeated polls. prereqs: streaming.
## MODULE: Historical Data Analysis
### LESSON: Fetching and Resampling Historical Data
- **Historical OHLCV data** — foundation for backtesting, analysis, and signal generation; per-instrument across timeframes. prereqs: none.
- **`kite.historical_data(instrument_token, from, to, interval)`** — fetches historical data, requires token not symbol. prereqs: instrument_token.
- **Interval data limits** — e.g. 1-min 60 days, 3/5/10-min 100 days, 15/30-min 200 days, 60-min 400 days, day 2000 days. prereqs: historical_data.
- **Resampling** — converting a time series from one frequency to another. prereqs: pandas.
- **`.resample(freq).agg()`** — aggregate OHLCV when converting to a lower frequency. prereqs: pandas.
- **Setting index for resampling** — set the `date` column as the DataFrame index first. prereqs: resampling.
- **Verifying resampled data** — plot close prices of multiple frequencies to confirm logic. prereqs: matplotlib.
### LESSON: Access Historical Derivatives Data and Analysing Open Interest
- **Open Interest (OI)** — total outstanding (unsettled) derivative contracts; one buyer pairs with one seller. prereqs: derivatives.
- **Expired futures via continuous data** — use the `instrument_token` of a live contract + `continuous=True` to get stitched historical futures data. prereqs: historical_data.
- **Expired options data unavailable** — historical candlestick data for specific expired options not offered by Kite Connect. prereqs: historical_data.
- **`oi=True`** — include Open Interest in the historical response. prereqs: historical_data.
- **OI + price sentiment signals** — Price↑ / OI↑ = long buildup (bullish); Price↓ / OI↑ = short buildup (bearish); Price↑ / OI↓ = short covering; Price↓ / OI↓ = long unwinding. prereqs: Open Interest.
- **Dual-axis price vs OI plot** — visualise trend conviction & exhaustion. prereqs: matplotlib.
## MODULE: Streaming Data
### LESSON: Streaming Live Market Data
- **WebSocket / KiteTicker** — persistent connection for streaming every price tick (push, vs polling pull). prereqs: none.
- **`KiteTicker(api_key, access_token)`** — the WebSocket streaming class. prereqs: kiteconnect.
- **Callback functions** — event-driven handlers: `on_ticks` (every tick), `on_connect` (connection established), `on_close` (disconnected). prereqs: KiteTicker.
- **Assigning callbacks** — set handler functions on the `kws` `on_` attributes. prereqs: callbacks.
- **Subscribing instruments** — subscribe to instrument tokens (e.g. Reliance) to receive their updates. prereqs: instrument_token.
- **`kws.connect()`** — blocking call that listens forever until closed. prereqs: KiteTicker.
- **Streaming modes** — `ws.MODE_LTP`, `ws.MODE_QUOTE` change the data payload size (data-use optimization). prereqs: KiteTicker.
- **Reconnect logic** — call `connect()` again from `on_close` to make the script robust. prereqs: on_close.
### LESSON: Calculation of SMA Using Websockets
- **Parsing live ticks** — extract Last Traded Price (LTP) from each incoming tick. prereqs: on_ticks.
- **Stateful price history** — a `ltp_history` list stores recent prices. prereqs: streaming.
- **Fixed-size history** — trim the list to the SMA period (e.g. 10) by dropping the oldest price. prereqs: price history.
- **Live Simple Moving Average (SMA)** — recompute SMA of the window on every new tick when enough data has accumulated. prereqs: SMA, streaming.
- **Real-time indicator bridge** — going from receiving data to processing it into an indicator. prereqs: history, SMA.
### LESSON: Trading Signal
- **Crossover strategy** — classic SMA-crossover buys on bullish, sells on bearish crossover. prereqs: SMA.
- **State (memory) variable** — `position_status` remembers whether price was previously above (`BULL`) or below (`BEAR`) the SMA. prereqs: live SMA.
- **Why state is needed** — checking price-vs-SMA alone would signal every tick; only the *moment of crossing* matters. prereqs: crossover.
- **Bullish crossover signal** — price > SMA AND previous state was BEAR → BUY. prereqs: state, crossover.
- **Bearish crossover signal** — price < SMA AND previous state was BULL → SELL. prereqs: state, crossover.
- **Preventing repeated signals** — update `position_status` immediately after generating a signal. prereqs: state.
- **Signal→execution gap** — completes Data Feed → Analysis → Signals; execution comes next. prereqs: signals.
## MODULE: Order Execution
### LESSON: Placing Your First Trade with Kite Connect
- **`kite.place_order()`** — sends an order; parameters map to web-platform fields. prereqs: authenticated kite object.
- **Order parameters** — `variety`, `exchange`, `tradingsymbol`, `transaction_type`, `quantity`, `product`, `order_type`, `price`. prereqs: none.
- **Varieties** — `VARIETY_REGULAR`, `VARIETY_AMO` (after-market), `VARIETY_CO` (cover), plus GTT/Iceberg later. prereqs: place_order.
- **Transaction types** — `TRANSACTION_TYPE_BUY` / `TRANSACTION_TYPE_SELL`. prereqs: place_order.
- **Product types** — `PRODUCT_CNC` (delivery equity), `PRODUCT_MIS` (intraday), `PRODUCT_NRML` (overnight F&O). prereqs: place_order.
- **Order types (basic)** — `ORDER_TYPE_MARKET` (best available price) vs `ORDER_TYPE_LIMIT` (specific price or better; `price` param required). prereqs: place_order.
- **BUY vs SELL orders** — sell order identical except `transaction_type`. prereqs: place_order.
- **Other order types preview** — stop-loss limit/market, AMO, CO, GTT, Iceberg covered in later sections. prereqs: order types.
### LESSON: Monitoring and Managing Orders
- **`kite.orders()`** — fetches all of the day's orders; format into a pandas table. prereqs: authenticated kite object.
- **Order statuses** — OPEN, TRIGGER PENDING, COMPLETE, CANCELLED, REJECTED etc. (see Kite docs). prereqs: orders.
- **`kite.modify_order(order_id, ...)`** — change parameters of a pending order (e.g. price). prereqs: orders, order_id.
- **`kite.cancel_order(order_id)`** — cancel a pending order. prereqs: order_id.
- **`kite.order_history(order_id)`** — full lifecycle of a specific order (status changes). prereqs: order_id.
- **`kite.trades()`** — the trade book: only orders actually filled. prereqs: orders.
- **Postback / webhooks** — public-URL notifications for reliable order updates irrespective of timing. prereqs: order management.
## MODULE: Order Placement and Stop Loss Orders
### LESSON: Stop-Loss Orders
- **Stop-loss order** — risk-management instruction to auto-exit a trade at a predetermined level. prereqs: order placement.
- **Stop-Loss Market (SL-M)** — single trigger price; on hit, exit at next available market price; guaranteed execution but slippage-prone; API: `ORDER_TYPE_SLM`, `price=0`. prereqs: order types.
- **Stop-Loss Limit (SL)** — trigger price + limit price (worst acceptable); `ORDER_TYPE_SL`, limit `price` set; price control but execution not guaranteed if market gaps past limit. prereqs: order types.
- **Trigger price** — the price that activates the exit order. prereqs: stop-loss.
- **Exiting an existing buy position** — the protective exit order is a SELL with quantity matching the open position. prereqs: transaction type, stop-loss.
- **Slippage vs fill certainty trade-off** — SL-M guarantees close, SL caps price. prereqs: SL, SL-M.
### LESSON: Cover Orders
- **Cover Order (CO)** — special intraday order type (`product='MIS'`) combining entry + compulsory stop-loss into one automated command. prereqs: stop-loss, mas.
- **`variety=kite.VARIETY_CO`** — marks the order as a Cover Order. prereqs: place_order.
- **Two-legged structure** — initial Market/Limit entry + compulsory SL-M leg. prereqs: CO, order types.
- **Mandatory risk definition** — cannot place CO without defining maximum risk (trigger) upfront; enforces discipline. prereqs: CO.
- **`trigger_price`** — the stop-loss trigger of the CO entry. prereqs: CO.
- **`try...except` error handling** — wraps order placement so failures (insufficient margin, bad trigger) are reported, not crashed. prereqs: python exceptions.
### LESSON: GTT and AMO
- **Good Till Triggered (GTT)** — a standing instruction active up to one year; when the trigger price is met, Zerodha places a Limit order. prereqs: order types.
- **`place_gtt()`** — special method (not `place_order`) for placing GTTs. prereqs: GTT.
- **Single-leg GTT** — one trigger for one action (e.g. buy 5 TCS if price ≤ ₹3000). prereqs: GTT.
- **One-Cancels-Other (OCO) GTT** — two triggers on a holding (target above, stop-loss below); if one fires, the other auto-cancels; like a long-term bracket order. prereqs: GTT.
- **After Market Order (AMO)** — place orders after market close; broker sends to exchange at next open; `variety='amo'` in `place_order`. prereqs: order types.
### LESSON: Iceberg Orders
- **Iceberg order** — a large parent order split into several smaller child legs shown to the market; only one leg active at a time. prereqs: order types.
- **Purpose** — discreetly execute large quantities, minimizing market impact and hiding true size. prereqs: Iceberg.
- **`variety=kite.VARIETY_ICEBERG`** — marks the order as Iceberg. prereqs: place_order.
- **`iceberg_legs` & `iceberg_quantity`** — `iceberg_quantity = total_quantity / iceberg_legs`. prereqs: Iceberg.
- **Typical parameters** — limit `price`, `ORDER_TYPE_LIMIT`, `PRODUCT_CNC` for delivery, quantity = grand total. prereqs: place_order, product types.
- **Order placement & confirmation** — `place_order` returns parent `order_id`. prereqs: Iceberg.
## MODULE: Trading Positions
### LESSON: Managing Trading Positions with KiteConnect
- **`kite.positions()`** — returns current positions, split into Net (actual current) and Day (taken during the day). prereqs: authenticated kite object.
- **Position data fields** — `quantity` (positive long / negative short), `average_price`, `pnl`, `m2m` (mark-to-market unrealized P&L). prereqs: positions.
- **Mark-to-Market P&L** — unrealized P&L for current-day trades. prereqs: positions.
- **`kite.convert_position()`** — convert an intraday (MIS) position to overnight (CNC/NRML) or vice versa. prereqs: positions, margins.
- **Margin constraint on conversion** — conversion requires sufficient margin, else rejected. prereqs: convert_position.
- **Exiting a position** — place a counter order. prereqs: positions, order placement.
## MODULE: Portfolio Holdings
### LESSON: Managing Portfolio Holdings with KiteConnect
- **Holdings vs positions** — holdings are long-term delivery (CNC) investments in demat; positions are active day/net trades. prereqs: positions.
- **`kite.holdings()`** — fetches the list of all delivery instruments in the account. prereqs: authenticated kite object.
- **Holdings fields** — `tradingsymbol`, `quantity`, `t1_quantity` (T+1 not-yet-delivered), `average_price`, `last_price`, `pnl`. prereqs: holdings.
- **Settlement concepts** — T+1 shares, final (T+2 settled) quantity, realised/used/opening quantity. prereqs: holdings.
- **Pledge / collateral & e-authorisation** — collateral_quantity/type, authorised_quantity/date (eDIS) for selling. prereqs: holdings.
- **MTF (Margin Trading Facility)** — mtf.quantity, used, average_price, value, initial_margin. prereqs: holdings.
- **`kite.mf_holdings()`** — fetch mutual fund holdings (fund name, folio, quantity, average/last price, P&L). prereqs: holdings.
- **Portfolio-level totals** — compute invested value, current market value, and overall P&L. prereqs: holdings.
## MODULE: Low Frequency Trading System
### LESSON: Low Frequency Trading System
- **Polling architecture** — periodic pull (wake → fetch → calculate → sleep → repeat) instead of WebSocket push. prereqs: none.
- **Polling vs WebSocket fit** — polling for low-frequency swing/positional (hourly/daily) strategies; WebSockets for intraday reaction strategies. prereqs: streaming.
- **`fetch_data_and_calculate_sma`** — function fetching latest historical data and computing e.g. 200-day SMA. prereqs: historical_data, SMA.
- **`main_trading_loop`** — infinite `while True` that calls the data/analysis function, runs a trading-logic placeholder, then `time.sleep()`s to set frequency. prereqs: polling.
- **`if __name__ == "__main__":`** — guard so the loop only runs on direct script execution. prereqs: python.
- **Efficiency** — saves bandwidth/compute vs tick-reactive systems. prereqs: polling.
## MODULE: A Complete Automated Trading System
### LESSON: A Complete Automated Trading System
- **End-to-end system** — integrates KiteTicker (live data + signals) with KiteConnect (order execution) into one autonomous loop. prereqs: streaming, order placement.
- **`place_market_order` function** — dedicated, reusable order-placement function with error handling. prereqs: place_order.
- **Position state variable (`current_position`)** — `None` / `'LONG'` prevents duplicate orders. prereqs: state, signals.
- **Crossover + state gating in `on_ticks`** — calls `place_market_order` only on crossover when no open position. prereqs: crossover, positions.
- **`on_order_update` callback** — executed on every order update; prints order id, symbol, status, filled qty, average price, timestamp for real-time monitoring. prereqs: callbacks, orders.
- **Margin check** — `kite.order_margins()` computes requirement (span, exposure, option premium, additional, bo, cash, var, pnl) for large/spread orders before placing. prereqs: margins.
- **Postback (webhook) updates** — reliable arbitrary order updates (COMPLETE, CANCEL, REJECTED, UPDATE, partial fills) anytime. prereqs: order management.
- **Going live & risk disclaimer** — the script can place real trades; sequence: listen → analyze → signal → execute automatically. prereqs: all modules.
- **Extensions** — stop-loss/take-profit, position sizing by risk, RSI/MACD combo, reconnect logic, backtesting before live. prereqs: system.
---
## COURSE-LEVEL PREREQUISITE GRAPH
- Authentication (access_token) is the gateway for every subsequent notebook.
- Instrument master (token lookup) → quotes (LTP/OHLC/full) → historical data & derivatives/OI; rate-limit + batching applies to all polling calls.
- WebSockets (KiteTicker, callbacks) → live SMA → crossover trading signals → order execution integration.
- Order placement basics → stop-loss (SL/SL-M) → Cover Orders / GTT / AMO / Iceberg; order management after placement.
- Positions & holdings follow order execution.
- Two architecture patterns for the final system: WebSocket push (intraday) and polling (low-frequency).
- Out of scope (covered elsewhere): machine-learning signal generation (see *Python for Machine Learning*) and ARIMA/ARCH/GARCH statistical forecasting (see *Financial Time Series Analysis for Trading*).