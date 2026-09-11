# Phase 0 — India Retail Quant Trading & Regulatory Specification

**Status:** Research specification — verified against publicly available SEBI, NSE and Zerodha material on 11 September 2026.

> This document is a project-control document, not legal, tax, investment, or regulatory advice. Rules can change. Before any live order is automated, re-check the current SEBI/NSE/BSE and Zerodha requirements and the account-specific broker terms.

## 1. Objective

The project must be capable of moving from historical research to paper trading and, only if justified, to controlled personal live validation while respecting the Indian retail trading and broker/API framework.

The project must therefore distinguish three activities:

1. **Research:** historical data, event studies, statistical analysis and backtesting.
2. **Signal generation:** producing a buy/sell/hold decision without automatically submitting an order.
3. **Automated execution:** software sending orders to the broker/exchange without manual order entry.

The third category requires additional controls and regulatory/broker checks. We will not treat a backtest or signal generator as automatically equivalent to a permitted live execution system.

## 2. Current regulatory baseline

SEBI issued Circular **SEBI/HO/MIRSD/MIRSD-PoD/P/CIR/2025/0000013** on 4 February 2025, titled **Safer participation of retail investors in Algorithmic trading**. SEBI subsequently issued extensions concerning implementation timelines. The framework allocates responsibilities across retail investors, stock brokers, algo providers/vendors and market infrastructure institutions.

NSE subsequently published implementation standards and FAQs for retail algorithmic trading. NSE's current public material states that API orders from clients are treated as algo orders and must receive the appropriate algo tagging. For client-generated algos below the exchange threshold, the framework provides a route without exchange registration; the initial Threshold Order Per Second (TOPS) is 10 orders/second. Above that threshold, registration requirements apply.

**Project implication:** order automation must be designed as a broker/API-compliant client-generated algo, not as an unrestricted script that happens to call an order endpoint.

## 3. Zerodha/Kite constraints relevant to this project

Current Zerodha material states that:

- Kite Connect provides order-management APIs and market-data APIs.
- API-based order placement requires a whitelisted static IP under the current framework.
- Zerodha currently enforces a maximum of **10 order requests per second per client account**; requests beyond the limit are rejected.
- WebSocket market data and non-order APIs can be accessed without the order-placement static-IP restriction.
- Zerodha's current API offering distinguishes free order/account-management access from the paid Connect tier for real-time/historical market data.

**Important:** the repository must not hard-code an assumption that the user can automatically place orders from an ordinary dynamic home connection. Before live API execution, the infrastructure must satisfy the current broker requirements.

## 4. Execution architecture for this project

We will use the following progression:

```text
Historical research
      ↓
Signal generation only
      ↓
Backtest with costs/slippage
      ↓
Walk-forward / out-of-sample validation
      ↓
Paper / shadow trading
      ↓
Broker integration test without unintended order submission
      ↓
Controlled personal live validation, if justified
```

The default development mode should be **signal-only**. Automatic order submission should require an explicit live-trading configuration and multiple safety gates.

## 5. Required live-trading safety gates

Before enabling automated orders, the system must have:

- explicit `LIVE_TRADING` opt-in;
- paper/shadow mode as the default;
- instrument allow-list;
- maximum position size;
- maximum gross exposure;
- maximum orders per day;
- maximum daily loss / kill switch;
- duplicate-order protection;
- stale-data detection;
- broker connectivity/error handling;
- order acknowledgement/reconciliation;
- open-position reconciliation;
- trading-session/time-window checks;
- logging of every signal, order request, broker response and resulting position;
- emergency disable mechanism;
- no credential storage in source control.

No strategy should be permitted to bypass these controls merely because its backtest is attractive.

## 6. Order-type policy

The strategy layer must be independent of the broker execution layer. A strategy should emit an abstract instruction such as:

```text
BUY / SELL / EXIT
instrument
quantity
limit/reference price
stop/risk information
signal timestamp
strategy identifier
```

The execution layer decides whether and how that instruction can be submitted under current broker/exchange rules.

We should not assume that every order type available through a manual trading interface is permitted for every API/algo workflow. In particular, current NSE retail-algo FAQs identify restrictions on market/IOC orders in specified algo contexts. The execution implementation must therefore validate allowed order types rather than defaulting to market orders.

## 7. Market/data universe policy

The first NIFTYBEES dataset remains a **pipeline validation instrument**. It is not automatically the final strategy instrument.

The research universe will be selected using:

- instrument eligibility;
- liquidity;
- price level and capital feasibility;
- historical data availability;
- spread/execution feasibility;
- corporate-action/data-quality considerations;
- short-selling feasibility where relevant;
- transaction-cost burden;
- strategy-specific turnover;
- broker/API support;
- robustness across multiple instruments.

We will initially prioritize NSE cash equities and ETFs because they avoid some of the additional expiry/margin/contract-roll complexity of derivatives.

## 8. Capital policy

The user's available account capital is approximately **₹30,000**. This is a hard research constraint, not a requirement to deploy all capital.

The project must separately track:

- total account capital;
- strategy-allocated capital;
- maximum capital at risk per trade;
- maximum gross exposure;
- reserve cash;
- estimated transaction costs;
- realized/unrealized P&L.

No strategy will be judged solely on percentage returns. A strategy that requires unrealistic capital, leverage, turnover, or execution quality is not considered feasible for this project.

## 9. Tax and cost policy

The backtest must treat transaction costs and taxes/levies as configurable inputs rather than hard-coded permanent constants.

At minimum, the research model should be able to represent:

- brokerage, where applicable;
- STT;
- exchange transaction charges;
- GST;
- SEBI charges;
- stamp duty;
- bid/ask spread;
- market impact/slippage.

Tax treatment depends on the nature of the activity and the taxpayer's circumstances. The project will document assumptions and direct the user to verify final tax treatment with current official guidance or a qualified tax professional.

## 10. Compliance checklist before live deployment

The following must all be true:

- [ ] Current SEBI retail-algo framework re-checked.
- [ ] Current NSE/BSE implementation standards re-checked for the intended segment.
- [ ] Current Zerodha API terms and order-placement requirements re-checked.
- [ ] Static IP configured and verified if required.
- [ ] API account/application configuration verified.
- [ ] Allowed order types verified.
- [ ] Instrument eligibility verified.
- [ ] TOPS/order-rate limits respected.
- [ ] Position/exposure limits implemented.
- [ ] Kill switch tested.
- [ ] Paper/shadow results reviewed.
- [ ] Backtest includes realistic costs and slippage.
- [ ] Out-of-sample/walk-forward evidence exists.
- [ ] Live capital allocation explicitly approved by the user.

## 11. Primary sources

- SEBI — Safer participation of retail investors in Algorithmic trading: https://www.sebi.gov.in/legal/circulars/feb-2025/safer-participation-of-retail-investors-in-algorithmic-trading_91614.html
- SEBI — September 2025 implementation-timeline extension: https://www.sebi.gov.in/legal/circulars/sep-2025/extension-of-timeline-for-implementation-of-sebi-circular-dated-february-04-2025-on-safer-participation-of-retail-investors-in-algorithmic-trading-_96979.html
- NSE — Decision Support Tools / Algorithms trading: https://www.nseindia.com/static/trade/platform-services-non-neat-decision-support-tools-algorithm-trading
- NSE — Retail Algo FAQ (November 2025): https://nsearchives.nseindia.com/web/sites/default/files/inline-files/FAQ_Retail%20Algo_03112025_NSE.pdf
- Zerodha — Kite Connect: https://zerodha.com/products/api
- Zerodha — Kite Connect FAQ: https://support.zerodha.com/category/trading-and-markets/general-kite/kite-api/articles/kite-connect-api-faqs
- Zerodha — Static IP requirements: https://support.zerodha.com/category/trading-and-markets/general-kite/kite-api/articles/static-ip

**Last verified:** 2026-09-11.
