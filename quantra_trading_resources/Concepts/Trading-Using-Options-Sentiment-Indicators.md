# Trading Using Options Sentiment Indicators — Concept Inventory
> This course has **no notebooks**. Content lives in an ebook (`TUOSI-ebook.pdf`) plus three standalone Python strategy modules (`.py`). The accompanying `.txt` files are readable copies of each `.py`.
Course flow (ebook TOC): sentiment trading intro → market sentiment → greed/fear & bubbles → breadth measures (TRIN) → TRIN strategy → option trading measures (volume/open interest/PCR) → PCR strategy → volatility measures (hist vol/implied vol/VIX) → VIX strategy → risks → conclusion.
---
## eBook — `TUOSI-ebook.pdf` (course theory)
### 1. Introduction to Sentiment Trading
- **Sentiment / fear–greed driven markets** — markets priced by intrinsic value + market sentiment; overvaluation from greed, undervaluation from fear; the 2008 real-estate bubble as the canonical greed→bubble→fear cycle. *Prereq: market mechanics.
- **Contrarian trading** — profit by taking positions against crowd behavior on exploitable mispricing. *Prereq: sentiment signals.
- **Algorithmic trading** — pre-defined rules place orders automatically (no per-trade discretion). *Prereq: Python, order logic.
### 2. Market Sentiment
- **Market sentiment definition** — investors' perception of current/future price; bullish (buying, prices rise) vs bearish (selling, prices fall).
- **Volume as sentiment strength gauge** — high volatility + high volume = strong sentiment; high vol + low volume = weak.
- **Mispricing & intrinsic value** — separating drift caused by fundamentals vs. sentiment; the target of sentiment trading.
### 3. Breadth Measures
- **Market breadth** — number/volume of advancing vs declining stocks in an index; breadth & volume gauge sentiment strength and direction.
- **Importance of volume** — volume spikes mark support/resistance and bull/bear strength.
- **High/Low measures** — today's/52-wk/all-time highs/lows; range = stock's spread; trades near highs = bullish, near lows = bearish.
- **New High/Low ratio** — (today's new highs)/(today's new lows); >2 strong new high, <0.5 strong new low; divergences flag unsustainable trends; derived % new highs/lows, % high-low, cumulative new high-low line.
- **Advance/Decline ratio & line** — # advancing / # declining; AD line = cumulative (adv−decl); AD ratio 1.25–2 = bullish band.
- **TRIN (Arms Index / Short-Term TRading INdex)** — `TRIN = (advancing stocks/declining stocks) / (advancing vol / declining vol)`; spikes = bearish/sell days, troughs = bullish/buy days; >1 bearish, <1 bullish, ~1 neutral.
- **Making TRIN trade-able** — log transform to de-lopside the ratio; Bollinger bands (moving avg ± k·σ, usually 2σ) to detect oversold/overbought; market thrust component to resolve volume contradictions.
- *Prereq:* stocks/index breadth data, moving averages, standard deviation, Bollinger bands.
### 4. TRIN Strategy
- **Log-TRIN + SMA(22)** normalization, then **Bollinger bands** (k=1.5σ) and stop-loss bands (additional l=2σ).
- **Contrarian entry** — TRIN crossing the **Upper Bollinger Band** = oversold → **BUY** S&P futures; crossing the **Lower Bollinger Band** = overbought → **SELL**.
- **Exit (take profit)** — TRIN reverts to the moving average → close the open position.
- **Two stop-loss exits** — (1) TRIN crosses the stop-loss band (further away than entry), (2) absolute S&P 500 move of 25 points → book loss.
- **Single-position discipline** — no new position while one is open; flag matrix for open/close tracking.
- *Prereq:* TRIN indicator, Bollinger bands, stop-loss/take-profit order types, futures contracts, flag state machine.
### 5. Option Trading Measures — Volume & Open Interest
- **Options basics** — call/put contracts, long (right to buy/sell) vs short (obligation), strike price, premium, exercise date; unbounded long payoff vs capped short premium.
- **Volume** — number of option contracts traded (not direction-specific); each option contract has a buyer and seller.
- **Open Interest (OI)** — contracts traded but not yet liquidated; OI increases / unchanged / decreases depending on new vs offsetting positions and delivery.
- *Prereq:* options contract mechanics, order execution.
### 6. Put Call Ratio (PCR)
- **PCR definition** — (traded volume of put options)/(traded volume of call options); >1 = bearish (more puts), <1 = bullish (more calls).
- **Three PCR types** — Equity PCR, Index PCR, Total PCR (equity + index put volume / equity + index call volume).
- **PCR interpretation as sentiment** — extreme high PCR = oversold (favor long), extreme low PCR = overbought (favor short); use short-term moving-average trends.
- *Prereq:* volume, open interest, calls/pures, sentiment interpretation.
### 7. PCR Strategy
- **SMA(20)** of PCR + **Bollinger bands** (k=1σ) and stop-loss bands (l=1σ more).
- **Contrarian entry** — PCR crossing the **Upper Band** = oversold → **BUY**; crossing **Lower Band** = overbought → **SELL**.
- **Exits** — reversion to moving average = mechanical take profit; stop-loss band or absolute S&P move (5 points) = exit at loss.
- Same single-position / flag discipline as TRIN.
- *Prereq:* PCR indicator, Bollinger bands, order types, futures.
### 8. Volatility Measures — Historical & Implied
- **Volatility as dispersion** — variance = avg squared deviation from mean; standard deviation = sqrt(variance); annualized historical vol = daily σ × √(trading days/yr ~254).
- **Historical volatility** — annualized std of past returns; an imperfect guide to future move.
- **Moneyness** — in / at / out-of-the-money for calls vs puts.
- **Option price = intrinsic + extrinsic value**; **Black-Scholes-Merton** 5 inputs (S, X, t, r, σ) price the option.
- **Implied volatility** — back out σ from market option premiums (all else fixed & the only unknown being vol); forward-looking, reflects demand/supply and time-to-expiry.
- *Prereq:* underlying option pricing, standard deviation, BSM.
### 9. VIX (Volatility Index)
- **VIX definition** — CBOE's implied-volatility estimate for S&P 500 index options over next ~30 days; from a kernel-smoothed variance of first two months' option premiums (outside money); σ × 100.
- **Reading VIX** — quoted in % (e.g. 20 = expected ±20% annualized at 1σ); high VIX = high uncertainty/fear/falls; low VIX = calm sure; >30 high-fear, <20 calm.
- **VIX variants & instruments** — VXN (NASD), VXD (DJIA), India VIX, etc.; VIX futures/options; "fear/index".
- *Prereq: implied volatility, options pricing, sqrt rule.
### 10. VIX Strategy
- **Threshold trigger** — VIX crosses threshold (e.g. **22**) → oversold/fear → **BUY** S&P futures.
- **Take-profit** — sell when futures rise **5%** above the buy price.
- **Stop-loss** — sell when futures fall **5%** below buy price (absolute value).
- **Recurring structure of the contrarian no-position-while-open logic, flag-based** (buy_flag/sell_flag 0/1).
- *Prereq:* VIX indicator, take-profit/stop-loss, futures.
### 11. Risks in Trading
- **Risk itself** — uncertainty of realized vs expected return; std of returns as measure; conservative vs aggressive investors.
- **Specific/unsystematic risk** — company/sector-specific (fire, strike, etc.); diversified away (MPT ~30 names).
- **Systematic/market risk** — affects entire market (2008 crisis); not diversifiable; measured by **Beta** (β=1 market risk).
- **Systemic risk** — failure of a "too-big/too-interconnected" firm triggers sector/market collapse (Lehman→AIG).
- **Price risk** — loss from price fall; reduced by **hedging** (futures price lock; natural long → sell futures).
- **Execution risk** — order fails to execute at desired price (slippage); market vs limit orders trade-off.
- **Model risk** — errors in your own trading model's inputs/complexity; mitigate via model averaging, sensitivity.
- *Prereq:* risk/return, diversification, hedging, order types.
### 12. Conclusion & extension
- Use **multiple sentiment indicators** with the fundamentals/rationality, not in isolation; combine TRIN + PCR + VIX + breadth signals; extend with more indicators (polling, margin debt, short interest, new equity issuance). *Prereq:* all indicator modules above.
---
## Python Strategy Modules
### 1. `Breadth Measures/TRIN.py` (also `TRIN.txt`)
- **TRIN computation from breadth data** — merges advancing/declining stock counts & volumes, forms [(adv/decl) / (adv_vol/decl_vol)], applies **log transform**, and joins S&P 500 futures 'Last' as the trade instrument.
- **Bollinger/stop-loss bands** — SMA(22) of TRIN; lower/upper Bollinger bands (k=1.5σ); stop-loss bands (l=2σ); custom `variance_calculator` (rolling squared-deviation with (n-1)).
- **Trade state machine** — UBB-crossover → **BUY**, LBB-crossover → **SELL**; take-profit on reversion to cleaned moving average (mAvg crossover); exit on stop-loss bands or absolute SL (25 S&P points).
- **Trade-report artifacts** — placed orders, cumulative PnL/cash, per-trade cause/stoploss columns; `.xlsx` output; plots TRIN with bands.
- *Prereq:* TRIN strategy theory, pandas rolling windows, flags.
### 2. `Option Trading Measures/PCR.py` (also `PCR.txt`)
- **PCR input & bands** — reads S&P PUT-CALL RATIO series + S&P futures; SMA(20); Bollinger bands (k=1σ), stop-loss bands (l=1σ); custom variance solver.
- **Trade machine** — UBB-crossover → **BUY**, LBB-crossover → **SELL**; close at moving-average reversion (TP) or on band/absolute SL (5 S&P points); single-active-position flag logic.
- **Account/analytics output** — placed orders, per-trade PnL, mark-to-market, cumulative account, `.xlsx` export, PCR/Band plot.
- *Prereq:* PCR strategy, Bollinger, pandas.
### 3. `Volatility Measures/VIX.py` (also `VIX.txt`)
- **VIX threshold entry** — reads VIX close series + S&P futures; when VIX ≥ threshold (22) → **BUY** (interpreted as fear/oversold). *Prereq:* VIX indicator, futures.
- **Take-profit / sticky-loss** — sell when futures rise **5%** (TP) or fall **5%** (SL) from buy price; c_1/c_2 multiplier by.
- **Position flags & accounting** — buy_flag/sell_flag state; mark-to-market, cumulative account, per-trade profit, `.xlsx` output, PnL plot. *Prereq:* VIX strategy, order types.
## Non-code support
- `ReadMe.html`, `Folder Structure...html` — setup/execution instructions.
- Breadth/option/volatility measure `.csv` input datasets (`advancing.csv`, `declining.csv`, `adv_vol.csv`, `dec_vol.csv`, `local_data.csv`, `local_future.csv`, `VIX_data.csv`, `Data1.csv`).
## Order of concept prerequisites (flow)
sentiment/market breadth → TRIN → TRIN strategy; then option-basics → volume/OI → PCR → PCR strategy; then volatility → historical/implied vol → VIX → VIX strategy; cap with risks; use multiple indicators in combination.