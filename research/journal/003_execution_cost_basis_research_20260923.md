# Strategy 003 — Execution-Cost Basis Research (23 September 2026)

## Purpose

Before deciding whether to expose Strategy 003 to protected validation, the project needs a defensible economic basis for the transaction-cost sensitivity used in prior research.

The repository previously used **5 bps per completed round trip** as a predefined sensitivity in Strategy 001J and related economic gates. That number was explicitly described as a sensitivity rather than a broker-fee quote. The question here is whether 5 bps is a sensible *current NSE cash-equity intraday cost basis*.

This review uses current/recent official exchange, regulator, and broker pricing information available on 23 September 2026.

## 1. Current mandatory/retail cost components

For NSE equity intraday, current published charges include:

- STT: **0.025% = 2.5 bps**, sell side only.
- NSE equity transaction charge: **0.00307% = 0.307 bps**, on buy and sell turnover.
- Stamp duty: **0.003% = 0.3 bps**, buy side.
- SEBI turnover fee: **₹10/crore**, equivalent to 0.001 bps per side.
- GST: **18%** on applicable brokerage + transaction + SEBI charges.

Zerodha's current published equity-intraday brokerage is **0.03% or ₹20 per executed order, whichever is lower**. Upstox and Angel One also publish ₹20-or-percentage intraday brokerage structures. Groww publishes ₹20 or 0.1% for intraday. These broker schedules show that the statutory charges are not eliminated by choosing a low-cost broker.

Sources:
- NSE: https://www.nseindia.com/static/invest/first-time-investor-sebi-turnover-fees-stt-other-levies
- Zerodha: https://zerodha.com/charges
- Upstox: https://upstox.com/brokerage-charges/
- Groww: https://groww.in/pricing
- Angel One: https://www.angelone.in/exchange-transaction-charges

## 2. What the fixed charges imply

Using Zerodha's published ₹20/order cap and the current NSE rates, the approximate **round-trip statutory + brokerage cost**, before bid/ask spread or market impact, is approximately:

| Round-trip notional | Approx. cost |
|---:|---:|
| ₹50,000 | **10.6 bps** |
| ₹1,00,000 | **8.3 bps** |
| ₹2,50,000 | **5.4 bps** |
| ₹5,00,000 | **4.5 bps** |
| ₹10,00,000 | **4.0 bps** |
| ₹50,00,000 | **3.6 bps** |

These are calculated from the published rates and are **not execution estimates**. They exclude spread, slippage, market impact, and any order-specific effects.

This immediately shows an important limitation of a blanket 5-bps assumption:

> **5 bps can be below or only barely above the unavoidable broker/statutory cost for ordinary retail-sized intraday trades, even before execution friction.**

At larger notionals, brokerage becomes less important and the statutory floor approaches roughly 3.5–4 bps, but spread and impact remain.

## 3. Market-impact evidence

NSE explicitly defines impact cost as the price degradation associated with executing a specified order size relative to the ideal mid-price. It varies by stock, order size, and the live order book; NSE states that it is a more practical measure of execution cost than the quoted bid-ask spread alone.

NSE's stock categorisation methodology uses **₹1 lakh order size** for its mean-impact-cost calculation, using four order-book snapshots across fixed intraday windows. This makes the ₹1 lakh reference particularly relevant when thinking about a retail/individual execution-cost baseline.

Current NSE quote pages provide concrete examples:

- **RELIANCE**, which is in the Strategy 003 universe, showed current impact cost of **0.01% = 1 bp** and traded value above ₹1,000 crore on 23 September 2026.
- **TCS** showed impact cost of **0.02% = 2 bps** in the available NSE quote data.
- **TECHM** showed impact cost of **0.03% = 3 bps** in the available NSE quote data.

These figures are stock-level liquidity indicators, not guaranteed slippage for our strategy. They demonstrate why a cost model cannot stop at statutory fees.

Sources:
- NSE impact-cost methodology: https://www.nseindia.com/static/products-services/indices-impact-cost
- NSE equity categorisation methodology: https://www.nseindia.com/static/products-services/equity-market-categorisation-stocks-imposition-of-margins
- NSE RELIANCE quote: https://www.nseindia.com/get-quote/equity/747RIL31/Reliance-Industries-Limited
- NSE TCS quote: https://www.nseindia.com/get-quotes/equity?symbol=TCS
- NSE TECHM quote: https://www.nseindia.com/get-quote/equity/TECHM/Tech-Mahindra

## 4. Why 5 bps is not a sufficient single execution assumption

There are three separate quantities that should not be conflated:

1. **Statutory/broker cost**
2. **Spread/slippage**
3. **Market impact**

The previous 5-bps sensitivity was useful as an early economic stress test, but it should not be interpreted as a complete current retail execution-cost estimate.

For example, around ₹1 lakh notional, published charges alone are roughly 8.3 bps round trip before spread/impact. A ₹1 lakh order can additionally experience liquidity cost. NSE's published impact-cost methodology explicitly measures that component separately.

Therefore:

**5 bps should be treated as a historical lower-bound sensitivity, not as our current realistic all-in base-case cost.**

## 5. What this means for Strategy 003

The current Strategy 003 diagnostic is not a strategy P&L number. The latest development decomposition produced:

- close-location-only: **+2.358 bps Q1–Q5**;
- additive 003H core: **+1.780 bps Q1–Q5**;
- interaction: **+1.871 bps Q1–Q5**.

These are cross-sectional next-bar diagnostic spreads, not realized portfolio returns.

That distinction is critical.

It would be methodologically incorrect to say:

> 1.78 bps < 5 bps, therefore Strategy 003 fails.

The Q1–Q5 spread is not necessarily the same quantity as a fully specified strategy's gross return or turnover-adjusted return.

However, the economic comparison is still highly informative:

> A next-5-minute cross-sectional effect whose observed development separation is only around 1.8–2.4 bps is **small relative to current unavoidable cash-equity trading costs**, and the cost problem becomes harder rather than easier once spread, slippage, impact, turnover, and portfolio construction are included.

## 6. Decision before protected validation

The correct conclusion is **not** to kill Strategy 003 solely because 5 bps was an arbitrary sensitivity.

The correct conclusion is:

### 5 bps was too weak a basis to serve as the project's realistic all-in cost model.

But this does **not** justify opening another exploratory research branch.

The research has already completed the development gates. Therefore the next step should be a **frozen economic viability test**, not more alpha discovery:

- freeze the two-variable additive 003H explanatory form;
- define a concrete portfolio construction and execution rule;
- use current statutory charges exactly;
- model spread/slippage/impact separately;
- evaluate several **pre-registered cost scenarios** rather than selecting one convenient number;
- use the already-protected validation period;
- do not tune the strategy after seeing validation performance.

A sensible scenario framework is:

- **Floor:** statutory/broker charges only;
- **Low-friction:** statutory + modest execution friction;
- **Base:** statutory + realistic spread/slippage;
- **Stress:** base + additional impact/slippage.

The exact execution assumptions must be specified before validation and should be tied to order size and the actual 15-stock universe rather than a universal arbitrary bps number.

## 7. Current recommendation for the research process

The cost research **does not justify another discovery cycle**.

It actually strengthens the case for moving to the protected validation/economic gate, because the question is now much sharper:

> **Does the frozen 003H information survive outside development, and is the resulting executable economics large enough to overcome real NSE cash-equity implementation costs?**

If it fails, close Strategy 003.

If it survives prediction-wise but fails economically, close the current executable form.

If it survives both, then and only then proceed to prospective paper/shadow testing.

## 8. Important methodological correction

The repository should no longer describe 5 bps as if it were the project's universal "realistic cost".

Use this terminology instead:

> **5 bps round-trip sensitivity — historical stress-test threshold, not a broker-fee or all-in execution-cost estimate.**

The next cost model should be execution-aware and tied to notional, turnover, spread, and impact.

## Bottom line

**5 bps was not a bad research sensitivity. It was a reasonable early stress threshold, but it is not a defensible universal current all-in cost basis for NSE intraday cash equities.**

For the current Strategy 003 effect size, that distinction matters: the observed ~1.8–2.4 bps diagnostic separation is already small relative to the current fee floor for many practical order sizes, before liquidity costs.

Therefore, **continue only into the frozen protected-validation + economic-viability gate. Do not continue searching for more features.**


## 9. Current published economics — verified 23 September 2026

The current official schedules were rechecked on 23 September 2026. NSE publishes STT of 0.025% on intraday equity sales, stamp duty of 0.003% on non-delivery security transactions on the buy side, SEBI turnover fees of ₹10/crore, and 18% GST on broker services. Zerodha publishes NSE equity transaction charges of 0.00307% and intraday brokerage of ₹20 or 0.03%, whichever is lower. Upstox publishes the same 0.00307% NSE transaction charge and ₹20-or-0.1% intraday brokerage. Angel One publishes ₹20-or-0.1% intraday brokerage (minimum ₹5), and Groww publishes ₹20-or-0.1% intraday brokerage subject to its published minimum-brokerage rules.

The fee-only round-trip reference remains:

| Round-trip notional | Approx. broker + statutory cost |
|---:|---:|
| ₹50,000 | **10.6 bps** |
| ₹1,00,000 | **8.3 bps** |
| ₹2,50,000 | **5.4 bps** |
| ₹5,00,000 | **4.5 bps** |
| ₹10,00,000 | **4.0 bps** |
| ₹50,00,000 | **3.6 bps** |

These are before spread, slippage and market impact. They are a reference calculation, not a historical execution estimate.

### Official sources

- NSE — SEBI turnover fees, STT and other levies: https://www.nseindia.com/static/invest/first-time-investor-sebi-turnover-fees-stt-other-levies
- Zerodha — charges: https://zerodha.com/charges
- Upstox — brokerage charges: https://upstox.com/brokerage-charges/
- Groww — pricing: https://groww.in/pricing
- Angel One — transaction charges: https://www.angelone.in/exchange-transaction-charges

The research terminology remains: **5 bps round-trip sensitivity — historical stress-test threshold, not a broker-fee or all-in execution-cost estimate.**
