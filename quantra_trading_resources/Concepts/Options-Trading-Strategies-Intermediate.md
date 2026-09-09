# Options Trading Strategies in Python — Intermediate (Concept Inventory)
Data modules (`data_modules/`): `Nifty.csv`, `nifty_futures_data_2022.csv`, `nifty_options_data_2022.csv`, `Option_data_NIFTY.csv`, `spx_options_raw_data/*.7z` (SPX option quotes; 481,630 rows × 33 cols).
Key conventions: `mibian` (open-source Black–Scholes pricing + Greeks library) is the central tool; the futures price is used as the underlying with `interest_rate = 0`.
---
## MODULE: Option Greeks: Delta
### LESSON: Greeks Calculator.ipynb
- **Option Greeks set** — Delta, Gamma, Vega, Theta, Rho for both calls and puts via `mibian.BS`. prereqs: call/put payoff
- **mibian BS signature** — `BS([underlying, strike, rate, days_to_expiry], volatility=iv, ...)` returning call/put price, deltas, thetas, rhos, vega, gamma. prereqs: implied volatility
- **Numeric interpretation** — (S=340.3, K=350, 29d, IV=30%): call Δ +0.386, put Δ −0.614, gamma +0.013, vega +0.367, theta −0.19/day, rho call (+) vs put (−). prereqs: Greeks
- **BS theoretical vs market** — theoretical prices should approximate observed market prices. prereqs: Black–Scholes
## MODULE: Option Greeks: Gamma
### LESSON: Option Price Using Delta and Gamma.ipynb
- **Delta-gamma approximation** — first-order (Delta) + second-order (Gamma) Taylor-series: `Price ≈ Initial + Δ·(ΔS) + ½·Γ·(ΔS)²`. prereqs: Greeks calculator, calculus (Taylor series)
- **Approximation accuracy** — approximated call price 5.5680 vs BS true 5.5679; residual from higher-order Greeks. prereqs: delta-gamma approximation
- **Gamma as curvature** — the linear Delta term alone is insufficient; quadratic (Gamma) correction matters for larger moves. prereqs: gamma
## MODULE: Option Greeks: Vega
### LESSON: Option Price Using Vega.ipynb
- **Vega sensitivity** — sensitivity of option price to a 1-point (1%) change in implied volatility: `Price ≈ Initial + Vega × (ΔIV×100)`. prereqs: implied volatility, pricing models
- **Vega approximation accuracy** — approximated price at IV 31% ≈ 4.0923 vs BS true 4.0923. prereqs: vega
- **Vega links price to volatility** — core tool for volatility trading. prereqs: vega, implied volatility
## MODULE: Options Pricing Models
### LESSON: Theoretical Price of Option.ipynb
- **Black–Scholes in mibian** — build the model and compute theoretical call/put prices. prereqs: option pricing fundamentals
- **BS inputs** — underlying price, strike, risk-free rate (0 when futures used), days-to-expiry, implied volatility. prereqs: Black–Scholes
- **Reading outputs** — via `callPrice`/`putPrice` attributes. prereqs: mibian
- **Parameter sensitivity** — vary parameters and observe how option prices change. prereqs: Black–Scholes
## MODULE: Options Trading Strategies
### LESSON: Calculate Calendar Spread Payoff.ipynb
- **Calendar (time/horizontal) spread** — same underlying, same strike, different expiries; sell front-month (short-dated), buy back-month (long-dated). prereqs: call payoff, Black-Scholes
- **Payoff estimation** — one month guesstimated with Black–Scholes for both legs at front-month expiry, holding IV and rates constant. prereqs: calendar spread
- **Profit sources** — time decay (theta) and/or rise in implied volatility; each leg's IV recovered with `impliedVolatility`. prereqs: theta, implied volatility
- **Max profit/loss** — max profit when underlying is at strike at front-month expiry; loss grows deep ITM/OTM. prereqs: calendar spread
- **Worked example** — Nifty: short Nov-28 call ₹50.50, long Dec-30 call ₹148.50. prereqs: calendar spread
## MODULE: Sourcing Options Data
### LESSON: Options Data Storing.ipynb
- **Bulk options data sourcing** — unpackaging tick-rate options (SPX, 2010–2014). prereqs: pandas I/O, ZIP/7z handling
- **py7zr.extractall** — extraction of `.7z` bundles. prereqs: py7zr
- **File plumbing** — `os.listdir`/`os.remove`; concatenating monthly CSV blocks into one master `options_data` frame with `pd.concat`. prereqs: pandas
- **Raw quote schema** — UNIX timestamps, DTE, strike distance, per-leg Δ Γ V Θ ρ, IV, volume. prereqs: options data
## MODULE: Volatility Skew
### LESSON: Strategy Using Volatility Skew.ipynb
- **Volatility skew** — difference between implied volatilities of OTM puts and OTM calls at equal distance from ATM. prereqs: implied volatility, ATM/OTM
- **ATM strike computation** — `strike_difference × round(underlying/strike_difference)`; OTM call = ATM + 2·diff, OTM put = ATM − 2·diff. prereqs: skew, numpy
- **Per-contract IV** — via `mibian.BS(...).impliedVolatility` with call/put branch and guards for `days_to_expiry == 0` / `LTP == 0`. prereqs: mibian, implied volatility
- **Normalized skew** — `(OTM Put IV − OTM Call IV) / ATM IV`. prereqs: skew
- **Skew interpretation** — positive skew ⇒ put IV > call IV ⇒ market expects a fall; negative skew ⇒ call IV > put IV ⇒ rally expected. prereqs: skew
- **Rule-based strategy** — long entry when skew < −5% threshold; short entry when skew > +10%; exit on reversal. prereqs: skew, signal construction
- **Performance metrics** — compounded returns (≈1.12×), Sharpe ≈ 2.37, max drawdown ≈ −3.39% (rolling cummax). prereqs: Sharpe, max-drawdown math
## MODULE: Volatility Trading Strategies
### LESSON: Strategy Using Forward Volatility.ipynb
- **Forward (term) volatility** — future value of an option's implied volatility extrapolated from near- and far-month contracts. prereqs: implied volatility, options data
- **Time-scaled variance** — `IV² · (tau/365)`; take far−near variance, divide by forward (gap) days, then square root → forward-vol estimate. prereqs: variance vs volatility math
- **Signal rule** — forward-vol > near-month IV (far-month "expensive") → short (signal −1); else far-month "cheap" → long (signal +1). prereqs: forward volatility
- **PnL computation** — day-over-day far-month vs near-month LTP differences, scaled by prior-day signal. prereqs: pandas
- **Worked example** — Nifty 2017 (near expiry 2017-09-28, far 2017-10-26); profitable off option mispricing. prereqs: forward volatility
### LESSON: Strategy Using Volatility Smile.ipynb
- **Volatility smile** — U-shaped curve of IV across strikes for same-expiry options; anomalies ("bumps") are exploitable. prereqs: implied-option IV
- **Bump detection** — identify a single-strike bump where IV exceeds neighbour by 1.5, respecting moneyness (ITM/OTM, same-day). prereqs: smile, pandas data manipulation
- **Butterfly to trade the bump** — long two outer money calls, sell 2× middle(at-bump) calls to capture overpriced IV. prereqs: butterfly construction
- **Signals & PnL** — open (buy) when smile has a bump (signal=1), accumulate cost ≈ `2×LTP − neighbouring LTPs`; exit when bump recedes; track PNL/MTM and cumulative PNL. prereqs: butterfly, signal construction
- **Worked example** — Nifty Dec-29 2017 expiry — cumulative PnL ≈ ₹5.8. prereqs: volatility smile
## Course-level prerequisite map
- Greeks + pricing notebooks (1–4) build the quantitative toolkit.
- Sourcing notebook (6) supplies options data/plumbing for strategy notebooks (5, 7–9).
- Strategies in notebooks 5, 7–9 rely on Black-Scholes for IV and payoff computation.
- Volatility modules (skew, smile, forward) form the Intermediate "volatility trading" theme.
- This course feeds into the Advanced course (dispersion, risk management, exotic options, ML).
---
## Options-Trading-Strategies-Intermediate — Section-based course structure (full lesson-by-lesson view)
# Concept Inventory — Options Trading Strategies In Python : Intermediate
> **12 sections on disk** (numbering gaps: sections 9 and 12 absent).
## COURSE — Options Trading Strategies In Python : Intermediate
**Purpose:** Intermediate options engineering — price options with the Black-Scholes & Merton models (and evolved Derman-Kani / Heston models), master the Greeks (first, second, third order) and their sensitivities, and build intermediate multi-leg strategies (arbitrage/box, calendar spread, earnings IV trades) with volatility trading (smile, skew, forward volatility) and paper/live trading via IBridgePy.
### Section: Section 1 - Options Pricing Models
- **CONCEPT:** Course introduction & structure — roadmap onto pricing models, Greeks, and strategies. prereqs: none.
- **CONCEPT:** Analogy to pricing a call option (dice game) — intuition for expected-payoff valuation and how option price derives from underlying uncertainty. prereqs: call options, expected value.
- **CONCEPT:** Intuitive explanation of the Black-Scholes-Merton (BSM) model — continuous-time closed-form formula pricing European options using S, K, r, σ, T. prereqs: pricing analogy, normal distribution, risk-free rate.
- **CONCEPT:** Black-Scholes inputs & assumptions — underlying, strike, interest rate, days to expiry, volatility; lognormal underlying, no early exercise. prereqs: BSM model.
- **CONCEPT:** Mibian Python package — implementing BSM (and Garman-Kohlhagen, Merton) to compute call/put price, Greeks, implied volatility, and put-call-parity. prereqs: BSM, Python.
### Section: Section 2 - Option Type and Applicability
- **CONCEPT:** Option type & applicability — course methods apply to European-style options (US index options SPX/RUT/DJX, NSE India equities/index); NOT American single-stock options (early-assignment risk). prereqs: European/American options.
- **CONCEPT:** Sourcing US options data — retrieving/laying-out options chain data (OptionsDX) for pricing and Greek analysis. prereqs: option type, data structure.
- **CONCEPT:** Data vendors for options — reliable sources of historical options & IV data. prereqs: data sourcing.
### Section: Section 3 - Evolved Options Pricing Model
- **CONCEPT:** Derman-Kani model — implied binomial tree calibrated to observed option prices to price other options consistent with the market. prereqs: BSM, implied volatility.
- **CONCEPT:** Heston model — stochastic-volatility model with mean-reverting volatility to better fit implied-volatility surface. prereqs: Derman-Kani, advanced stochastics.
- **CONCEPT:** Other options pricing models — Lattice models (Binomial Cox-Ross-Rubinstein, Trinomial), Monte Carlo option pricing, Finite Difference method (for American-style options and complex payoffs). prereqs: BSM, lattice/Monte Carlo concepts.
### Section: Section 4 - Options Greeks - Delta
- **CONCEPT:** Greeks primer — Δ,Γ,Θ,ν as first-order sensitivities of option price to underlying, time, and volatility. prereqs: BSM pricing.
- **CONCEPT:** Delta (Δ) — change in option price per unit change in underlying; call Δ ∈ [0,1], put Δ ∈ [-1,0]; also approx. prob. of ITM at expiry. prereqs: Greeks primer.
- **CONCEPT:** Delta with respect to underlying price — how Δ varies across ITM/ATM/OTM (S-curve). prereqs: delta.
- **CONCEPT:** Delta with respect to time to expiry — how Δ changes toward 0/1 as expiry approaches. prereqs: delta.
- **CONCEPT:** Delta with respect to volatility — Δ flattens toward 0.5 with high IV (less directional certainty). prereqs: delta, volatility.
### Section: Section 5 - Option Greeks - Gamma
- **CONCEPT:** Gamma (Γ) — rate of change of Δ per unit underlying move; "acceleration"; largest for ATM, smallest for ITM/OTM; with respect to time to expiry and volatility. prereqs: delta, BSM.
- **CONCEPT:** Gamma sensitivity — rebalancing frequency, delta-hedged portfolio convexity/risk. prereqs: gamma, delta hedging.
### Section: Section 6 - Option Greeks - Vega
- **CONCEPT:** Vega (ν) — change in option price per 1% change in implied volatility; positive for long options. prereqs: implied volatility, BSM.
- **CONCEPT:** Vega with respect to time to expiry and volatility — vega peaks for longer-dated & ATM options; vol-sensitivity dynamics. prereqs: vega.
### Section: Section 7 - Option Greeks - Theta and Rho
- **CONCEPT:** Theta (Θ) — time decay; negative for long options, positive for short options; with respect to time & moneyness. prereqs: BSM, time value.
- **CONCEPT:** Rho (ρ) — interest-rate sensitivity; call ρ positive, put ρ negative; sensitive to time to expiry and moneyness. prereqs: theta, interest rates.
- **CONCEPT:** Advanced Greeks (2nd/3rd order) — Vanna, Charm, Veta, Vomma/Volga, Vera, and third-order Color, Speed, Zomma, Ultima; refine risk measurement. prereqs: first-order Greeks.
### Section: Section 8 - Options Trading Strategies
- **CONCEPT:** Arbitrage strategy — exploit mispricing / violation of no-arbitrage relationships to lock riskless profit; Box spread as synthetic risk-free. prereqs: PCP, moneyness.
- **CONCEPT:** Box trading — combining a bull call spread + bear put spread → synthetic forward / box arbitrage. prereqs: arbitrage strategy.
- **CONCEPT:** Calendar spread — same strike, different expirations (sell near, buy far); monetizes time decay and IV term structure. prereqs: theta, implied volatility.
- **CONCEPT:** Implied volatility in earnings strategy — buy a strangle before an earnings announcement to sell the post-announcement IV collapse. prereqs: strangle, IV crush.
- **CONCEPT:** Stock price movement in earnings strategy — ATM bull-call (bullish) or bear-put (bearish) spreads to profit from the post-earnings price move while limiting IV-crush damage. prereqs: bull call / bear put spread, IV.
- **CONCEPT:** Multi-leg strategy mechanics — payoff and risk profile construction from component legs. prereqs: spread mechanics, Greeks.
### Section: Section 10 - Volatility Trading Strategies
- **CONCEPT:** Forward volatility — expected future volatility over a target forward horizon (derived from the IV term structure) used for forward-start/calendar vol trades. prereqs: implied volatility, volatility term structure.
- **CONCEPT:** Volatility smile — IV varies by strike (not constant as BSM assumes); observed smile shape. prereqs: implied volatility, moneyness.
### Section: Section 11 - Volatility Skew
- **CONCEPT:** Predicting market movement via volatility skew — higher OTM put IV (reverse skew) signals fear/negative-return expectations; skew as a sentiment/hedging signal. prereqs: volatility smile.
- **CONCEPT:** Volatility skew strategy logic — building trades from the skew curve (reverse & forward skew). prereqs: volatility skew concept.
- **CONCEPT:** Reverse vs forward skew & market implication — additional reading on skew behavior and jump-risk interpretation. prereqs: volatility skew strategy.
### Section: Section 13 - Paper and Live Trading
- **CONCEPT:** IBridgePy options automation — template and IBridgePyOPTIONSINT resources for paper/live options trading. prereqs: full tested strategy, broker integration.
- **CONCEPT:** Broker/gateway setup and order flow — connecting broker API, placing multi-leg options orders. prereqs: IBridgePy automation.
### Section: Section 14 - Wrapping Up!
- **CONCEPT:** Summary & resources — recap of pricing models, Greeks, strategies, volatility trading; OTSIResources package. prereqs: all course.
## Course Prerequisite Map
- Options pricing (BSM) ← Dice-game intuition + normal distribution; Mibian implements BSM for Greeks.
- Pricing models (BSM) → Evolved Models (Derman-Kani, Heston, lattice/Monte Carlo/Finite-Difference).
- Greeks build on pricing: Delta → Gamma (rate of change of delta) → Vega (vol sensitivity) → Theta/Rho (time/rates) → Advanced 2nd/3rd order Greeks.
- Strategies combine Greeks + volatility: Arbitrage/Box (PCP enforcement) ← PCP; Calendar spread ← Theta & IV term; Earnings trades ← IV crush & underlying move.
- Volatility path: Implied Vol → Forward Volatility → Volatility Smile → Volatility Skew → Skew strategies.
- Paper/Live (IBridgePy) depends on a complete, back-tested strategy; Wrapping Up consolidates all blocks.