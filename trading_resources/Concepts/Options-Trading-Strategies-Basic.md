# Options Trading Strategies in Python — Basic (Concept Inventory)
Data module(s): `data_modules/apple_stock_data.csv` (Apple adjusted close prices). No standalone Python modules; all code is embedded in the notebooks.
Key libraries used across the course: `numpy`, `pandas`, `matplotlib.pyplot` (payoff plotting and rolling volatility).
---
## MODULE: Know Your Options!
### LESSON: Call Option Payoff.ipynb
- **Call option (long)** — buying a call gives the right, not the obligation, to buy the underlying at the strike; payoff depends on where spot sits relative to strike at expiry. prereqs: none (entry-level)
- **Call payoff formula** — via `np.where`: profit = `spot - strike` when spot > strike, else `0`, then minus premium. prereqs: numpy.where
- **Call buyer risk/reward** — loss capped at premium paid; profit rises linearly and is unlimited above the strike; must first recover premium (break-even region). prereqs: call payoff
- **Call seller payoff** — exact mirror (multiply buyer payoff by −1); max profit = premium; loss is open-ended as spot rises. prereqs: call payoff
- **Selling a call** — appropriate only when the view is that the underlying will not rally beyond the strike. prereqs: call payoff
- **Payoff plotting** — matplotlib plotting with a zero-moved spine to show profit/loss regions. prereqs: matplotlib
### LESSON: Put Option Payoff.ipynb
- **Put option (long)** — buying a put gives the right to sell the underlying at the strike; payoff depends on spot vs strike at expiry. prereqs: none
- **Put payoff formula** — profit = `strike - spot` when spot < strike, else `0`, then debit the premium. prereqs: numpy.where
- **Put buyer risk/reward** — limited risk (premium), potentially large (near-linear, capped at strike) profit as underlying falls. prereqs: put payoff
- **Put seller payoff** — mirror image: max profit = premium received; losses accrue as the underlying falls below the break-even. prereqs: put payoff
- **Selling a put** — appropriate only when the view is that the underlying will not fall below the strike. prereqs: put payoff
## MODULE: Options Trading Strategies
### LESSON: Bull Call Spread Payoff.ipynb
- **Bull call spread** — long a lower-strike call + simultaneous short of a higher-strike call on the same underlying/expiry. prereqs: call option payoff, premium/debit concept
- **Strategy objective** — profit from small positive (moderately bullish) moves; ceiling placed on both profit and loss. prereqs: bull call spread
- **Payoff assembly** — add long-leg payoff and −1× short-leg call payoff; `max()`/`min()` give capped max profit (strike width − net debit) and max loss (net debit). prereqs: call payoff, numpy
- **Worked example** — long 920C / short 940C on Infosys → max profit ₹15, max loss ₹5. prereqs: bull call spread
- **numpy.arange** — used to build the stock-price-at-expiry range. prereqs: numpy
### LESSON: Bear Put Spread Payoff.ipynb
- **Bear put spread** — long a higher-strike put + simultaneous short of a lower-strike put. prereqs: put option payoff, spread mechanics
- **Strategy objective** — benefit from small negative (moderately bearish) price moves. prereqs: bear put spread
- **Combined payoff** — long put payoff + short put payoff, giving capped max profit (strike width − net debit) and bounded max loss (net debit). prereqs: put payoff
- **Worked example** — long 880P / short 860P on Infosys → max profit ₹15, max loss ₹5. prereqs: bear put spread
- **max()/min() on combined array** — reading off max profit/min loss. prereqs: numpy
### LESSON: Covered Call Payoff.ipynb
- **Covered call** — long (own) stock + simultaneous short call on that stock → a "neutral" view strategy. prereqs: long stock payoff, call payoff
- **Capped upside** — profit ceiling ≈ call premium received; unlimited downside exposure scaled by the long stock position. prereqs: covered call
- **Payoff** — stock payoff (`spot - purchase price`) + short-call payoff. prereqs: stock payoff, call payoff
- **Worked example** — Wipro at ₹300, short 300C → max profit capped at ₹10, max loss proportional to the fall below ₹300. prereqs: covered call
### LESSON: Protective Put Payoff.ipynb
- **Protective put** — long stock + long put on the same underlying ("insurance" against adverse moves). prereqs: stock payoff, put payoff
- **Downside capped** — max loss ≈ put premium; upside remains unlimited. prereqs: protective put
- **Payoff** — long stock payoff + long put payoff. prereqs: stock payoff, put payoff
- **Worked example** — Auro Pharma 700P strike premium ₹20 → max loss bounded to ₹20. prereqs: protective put
## MODULE: Types of Volatility
### LESSON: Historical Volatility Calculation.ipynb
- **Historical (realized) volatility** — gauges past price fluctuations of the underlying over a fixed look-back period. prereqs: volatility concept
- **Daily log returns** — `np.log(Adj_Close / Adj_Close.shift(1))`. prereqs: pandas, log-return math
- **20-day historical volatility** — rolling standard deviation of log returns, annualized-scaled (× `sqrt(window)`), expressed as a percentage. prereqs: standard deviation, annualization scaling
- **Volatility time-series plot** — visualization with matplotlib. prereqs: matplotlib
## Prerequisite chain across the course
- Payoff fundamentals (Call/Put) → every spread strategy (Bull Call, Bear Put, Covered Call, Protective Put).
- Historical volatility lays groundwork for the Intermediate course's volatility skew / smile / forward-volatility modules.
---
## Options-Trading-Strategies-Basic — Section-based course structure (full lesson-by-lesson view)
# Concept Inventory — Options Trading Strategies In Python : Basic
> **5 sections on disk** (Sections 1–4, 6; no Section 5).
## COURSE — Options Trading Strategies In Python : Basic
**Purpose:** Foundational options skill course — understand call/put options, terminology, nomenclature, moneyness, put-call parity, open interest & volume, volatility (realized/historical, implied, forward), pricing inputs, and build simple directional, hedging and neutral option strategies with payoff diagrams in Python.
### Section: Section 1 - Know Your Options!
- **CONCEPT:** Introduction — why options; rights vs obligations, asymmetrical payoff. prereqs: none.
- **CONCEPT:** Options terminology — underlying, premium, strike price, expiration date, style (European/American/Bermudan), ITM/ATM/OTM, intrinsic vs time value. prereqs: none.
- **CONCEPT:** Call options — the right (not obligation) to BUY the underlying at strike; bullish; payoff diagram. prereqs: terminology.
- **CONCEPT:** Put options — the right (not obligation) to SELL the underlying at strike; bearish; payoff diagram. prereqs: terminology.
### Section: Section 2 - Options Nomenclature
- **CONCEPT:** Types of options — classification by exercisability (European/American/Bermudan), tradability (exchange-traded vs OTC), underlying (equity/index/commodity/futures/currency); plain-vanilla vs exotic (Asian average, Binary, Barrier). prereqs: calls & puts.
- **CONCEPT:** Moneyness — ITM/ATM/OTM for calls and puts; drives intrinsic and time value. prereqs: nomenclature.
- **CONCEPT:** Open interest and volume — OI = number of open contracts; Volume = number traded; joint interpretation for market activity. prereqs: payment.
- **CONCEPT:** Put-call parity (PCP) — relationship C + K·e^(-rt) = P + S linking call/put prices; deviation implies arbitrage; used to price/screen. prereqs: calls, puts, moneyness, arbitrage.
- **CONCEPT:** Arbitrage & risk-free profit — exploit mispricing across markets/contracts to lock near-riskless gain (PCP enforcement). prereqs: PCP.
### Section: Section 3 - Types of Volatility
- **CONCEPT:** Normal probability distribution — bell curve, mean (expected value, drift), standard deviation (risk/volatility); assumption that asset returns are normally distributed. prereqs: basic statistics.
- **CONCEPT:** Historical (realized) volatility — annualized σ computed from observed daily returns; measure of realized price dispersion. prereqs: normal distribution, standard deviation.
- **CONCEPT:** Implied volatility (IV) — expected future volatility back-solved from an option's market price (Black-Scholes-Merton); market's consensus forecast. prereqs: normal distribution, option pricing input.
- **CONCEPT:** Forward volatility — future expected volatility over an upcoming horizon implied from term of IVs. prereqs: implied volatility.
### Section: Section 4 - Options Trading Strategies
- **CONCEPT:** Delta trading strategies — directional sensitivity; using delta to express/protect directional (bull/bear) bias. prereqs: moneyness, options pricing.
- **CONCEPT:** Hedging with options — protective put, covered call to reduce downside / enhance yield, insurance-style payoffs. prereqs: call & put payoffs.
- **CONCEPT:** Bull call spread — buy low-strike call, sell higher-strike call (same expiry); limited-risk bullish bet. prereqs: call payoff, spread mechanics.
- **CONCEPT:** Bear put spread — buy high-strike put, sell lower-strike put; limited-risk bearish bet. prereqs: put payoff, spread mechanics.
- **CONCEPT:** Iron Condor (neutral) — short strangle + outer long wings = bull put spread + bear call spread; high-prob small profit when price stays range-bound, limited loss. prereqs: bull put, bear call spread.
### Section: Section 6 - Wrapping Up!
- **CONCEPT:** Course summary — recaps payoff/PCP, historical volatility, bull-call, bear-put, covered call, protective put, iron condor; ability to compute payoffs in Python. prereqs: all course.
- **CONCEPT:** Backtesting & live trading next steps — beyond course scope; resources for data fetching, backtesting tools, broker APIs (IBridgePy/Blueshift). prereqs: all course.
## Course Prerequisite Map
- Terminology → Calls & Puts → Nomenclature (Types, Moneyness, OI/Volume, PCP)
- Normal Distribution → Historical Volatility; IV needed for pricing-based strategies.
- Calls/Puts + Moneyness → Bull Call Spread / Bear Put Spread → Iron Condor (combines spreads).
- Hedging (Protective Put, Covered Call) is built directly from call & put payoff foundations.
- PCP + OI/Volume + Payoffs feed all strategy construction; Wrapping Up consolidates and points to the Intermediate / Python resources.