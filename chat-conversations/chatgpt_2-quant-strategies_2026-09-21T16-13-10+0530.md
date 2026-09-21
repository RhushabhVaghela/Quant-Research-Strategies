---
title: "2 - Quant Strategies"
tags: []
author: chatgpt
count: 17
exporter: 3.1.0
date: 2026-09-21T16-13-10+0530
url: https://chatgpt.com/c/6aabafb0-989c-83ee-937f-f1aa9741bfa8
---

# 2 - Quant Strategies

## Table of Contents

- [1: so we will continue our chat conversation now, please refer to the pre…](#chat-1)
- [2: also just to be clear, we are using our approach the same way as this…](#chat-2)
- [3: Pasted text.txt Document](#chat-3)
- [4: Pasted text.txt Document](#chat-4)
- [5: okay proceed now with the next steps, make sure to create/update the f…](#chat-5)
- [6: fix the warnings and errors, update the files necessary so I can pull](#chat-6)
- [7: fix the warnings okay proceed now with the next steps, make sure to cr…](#chat-7)
- [8: okay proceed now with the next steps, make sure to create/update the f…](#chat-8)
- [9: also fix the warnings, okay proceed now with the next steps, make sure…](#chat-9)
- [10: Pasted text.txt Document](#chat-10)
- [11: okay proceed now with the next steps, make sure to create/update the f…](#chat-11)
- [12: okay proceed now with the next steps, make sure to create/update the f…](#chat-12)
- [13: okay proceed now with the next steps, make sure to create/update the f…](#chat-13)
- [14: okay proceed now with the next steps, make sure to create/update the f…](#chat-14)
- [15: D:\\Quant\-Research\-Strategies\\scripts\\run\\\_strategy\\\_002\\\_validation.py…](#chat-15)
- [16: fix the warnings and proceed now with the next steps, make sure to cre…](#chat-16)
- [17: D:\\Quant\-Research\-Strategies\\scripts\\run\_strategy\_002\_turnover\_decompo…](#chat-17)

## chat-1

> so we will continue our chat conversation now, please refer to the previous chat context for your reference.
> 
> Note - this chat context along with all the files is already in my github repo (same one we are using for this conversation), so if the files expire just retrieve from there whenever you want to refer them

Absolutely. We can continue from here as a continuation of the **Quant Strategies** conversation.

I’ve reviewed the uploaded conversation context, so I have the current state of the project. 

chatgpt_quant-stategies_2026-09…

### Where we currently stand

Our project is **not starting from scratch**. We have already:

- Set up the Zerodha/Kite API workflow.

- Chosen **Strategy 001 — GoldBeES mean reversion** as our first strategy.

- Built the research/diagnostic pipeline.

- Progressed through **001A → 001H**.

- Frozen the historical strategy rather than continuously optimizing it.

- Performed robustness/replay work.

- Built **001I prospective OOS paper/shadow trading**.

- Added validation and tests.

- Reached **72 tests passing** after the warning fixes.

- Established **17 September 2026, 09:15 IST** as the prospective activation boundary. chatgpt_quant-stategies_2026-09…

- The 001I collector is **paper/shadow only** and does not place orders. chatgpt_quant-stategies_2026-09…

And importantly, we've already recognized that **one day of paper trading isn't sufficient**. The purpose of 001I is to accumulate genuinely unseen prospective observations, with the eventual evaluation based on the number and quality of trades rather than an arbitrary "one week/month" rule. 

chatgpt_quant-stategies_2026-09…

### The bigger research philosophy we're following

We also changed our approach from:

> Pick one random asset → test one strategy → if it looks profitable, move on.

to a more defensible **quant research process**:

> Define a hypothesis → define the universe → screen appropriately → test systematically → diagnose → backtest → account for costs → robustness/OOS testing → prospective paper trading → evaluate → only then consider controlled deployment.

That matters because we don't want to accidentally discover a strategy that "works" only because we happened to test it on an asset where it looked good.

And we are **not going to force Strategy 001 to succeed**. If the evidence says the GoldBeES strategy doesn't survive costs or prospective testing, the correct research outcome is to document that and move to the next hypothesis.

### Current immediate task

We're now effectively in the **001I prospective observation phase**.

The next useful thing is therefore **not to change the strategy**. We should let the frozen 001I process collect data, then audit the resulting:

```
data/prospective/strategy_001i/
├── bars.csv
├── signals.csv
├── outcomes.csv
└── run_manifest.json
```

Once we have enough observations, we'll compare the prospective results against the historical 001D/001H expectations and make the next research decision.

And yes — **if we need something from the previous conversation that isn't in the uploaded context, we can retrieve the relevant material from the GitHub repository rather than making you resend everything.**

So we're fully synced. **Let's continue from wherever you want to pick up.**

___
###### [top](#table-of-contents)
## chat-2

> also just to be clear, we are using our approach the same way as this document (this document is also in the github so you can fetch from there and refer to it whenever you want), right?

Yes — **that is exactly the framework we are trying to follow.** In fact, the document you just uploaded is a very good description of the philosophy behind the way we have been restructuring the project.

The important distinction is:

> **We are not claiming that our current Strategy 001 has completed every institutional step in the document. We are building the project so that we move through those steps in the same research order, as far as is practical for an individual research project.**

The document itself explicitly says that serious quant research is not simply _“download data → train model → get high Sharpe → deploy”_; the process is about establishing whether a signal is economically sensible, statistically robust, operationally feasible, and profitable after costs. 

How does a Quant Researcher act…

### How our process maps to the document

| Document's process | What we're doing |
|---|---|
| 1. Economic / market hypothesis | Mean reversion hypothesis for GoldBeES |
| 2. Define prediction target | Defined the event/signal and subsequent return/outcome rather than just looking at price charts |
| 3. Point-in-time data | Historical research with attention to what information was actually available at each point |
| 4. Clean & validate data | Data validation, universe checks, timestamp/session handling, tests |
| 5. Engineer meaningful features | Rolling statistics, z-score, deviations, event characteristics, etc. |
| 6. Simple baseline | We deliberately started with a simple rule-based mean-reversion strategy rather than ML |
| 7. Statistical significance / stability | Event studies, dependence diagnostics, robustness analysis, parameter sensitivity, etc. |
| 8. Proper OOS testing | Chronological holdout / robustness work and now prospective OOS |
| 9. Neutralize unwanted exposures | Not fully developed yet — this is a later research layer |
| 10. Portfolio-level value | Returns, Sharpe, drawdown, turnover/trades, costs, slippage/economic viability |
| 11. Stress testing | 001H robustness work |
| 12. Combine with existing alphas | Not applicable yet — we don't have an alpha library/portfolio yet |
| 13. Paper/shadow trading | 001I, currently running through Zerodha real-time data with no orders |
| 14. Production deployment | Not yet — intentionally |

This is remarkably close to the document's own pipeline:

**Economic hypothesis → point-in-time data → cleaning → feature engineering → signal → statistical testing → OOS validation → risk/factor analysis → costs/capacity → portfolio construction → paper trading → production → monitoring.** 

How does a Quant Researcher act…

### And this explains some of the decisions we've already made

For example, when you previously asked:

> _“Why aren't we just taking the code from the resource and applying it to a random asset?”_

the answer is precisely what this document is warning against.

A historical pattern appearing profitable isn't enough. The document specifically says that a historical relationship without an economic/behavioral/structural explanation may simply be coincidence. 

How does a Quant Researcher act…

Likewise, when you proposed testing a **basket of assets** rather than randomly picking one, that fits the broader research philosophy much better. We need to be careful, though, because testing hundreds of assets and selecting only the winners can itself create **selection bias / multiple-testing problems**. The document explicitly warns that when thousands of features are tested, some will appear successful purely by chance. 

How does a Quant Researcher act…

So we'll eventually need to distinguish:

**Research universe → predefined screening → analysis → selection based on predefined criteria**

from:

**Try everything → find what worked → declare that the strategy works.**

That distinction is extremely important.

## One thing I particularly want us to preserve

The document says:

> **“The real job is to determine whether that pattern contains information that is economically explainable, statistically reliable, stable out of sample, distinct from existing factors, profitable after transaction costs, scalable, compatible with portfolio constraints, and robust enough to survive changing markets.”** 
> 
> How does a Quant Researcher act…

That is basically the **standard we should use for this entire GitHub project**.

So our goal isn't:

> **“Find a strategy that makes money.”**

It is:

> **“Investigate a trading hypothesis rigorously enough that we can determine whether it contains a genuine, repeatable, economically meaningful edge.”**

And sometimes the conclusion will be:

> **Reject the hypothesis.**

That is a perfectly valid quant-research result.

### Where Strategy 001 currently sits

We're approximately here:

```
Economic hypothesis
       ↓
Historical data
       ↓
Data validation
       ↓
Feature / signal construction
       ↓
Diagnostics / event study
       ↓
Baseline strategy
       ↓
Historical backtest
       ↓
Robustness / decomposition
       ↓
Chronological OOS / holdout
       ↓
Transaction-cost analysis
       ↓
[ WE ARE HERE ]
       ↓
001I Prospective OOS / Shadow Trading
       ↓
Evaluate accumulated unseen observations
       ↓
Decision:
   ├── Reject
   ├── Research modification → new version
   └── Advance toward controlled deployment
```

And **only after that** would real capital become relevant.

The document itself describes shadow trading as a way to discover problems that historical backtesting cannot reveal — delayed feeds, missing observations, production/research discrepancies, slippage, execution feasibility, etc. 

How does a Quant Researcher act…

 That's exactly why we built 001I rather than simply declaring the historical backtest successful.

So yes: **from this point forward, I will treat this document as one of the governing research frameworks for our Quant-Research-Strategies project**, alongside the actual evidence and methodology we've already established in the repository.

And importantly, **I won't shortcut the process just because we want to get to another strategy or live trading faster.** If Strategy 001 fails a research gate, we'll document why and then use that information to design Strategy 002 rather than quietly changing the rules until 001 works.

___
###### [top](#table-of-contents)
## chat-3

> Pasted text.txt
> Document

## chat-4

> Pasted text.txt
> Document

## chat-5

> okay proceed now with the next steps, make sure to create/update the files and documents accordingly as necessary

## chat-6

> fix the warnings and errors, update the files necessary so I can pull

## chat-7

> fix the warnings
> 
> okay proceed now with the next steps, make sure to create/update the files and documents accordingly as necessary

## chat-8

> okay proceed now with the next steps, make sure to create/update the files and documents accordingly as necessary

## chat-9

> also fix the warnings, okay proceed now with the next steps, make sure to create/update the files and documents accordingly as necessary

## chat-10

> Pasted text.txt
> Document

## chat-11

> okay proceed now with the next steps, make sure to create/update the files and documents accordingly as necessary

## chat-12

> okay proceed now with the next steps, make sure to create/update the files and documents accordingly as necessary

## chat-13

> okay proceed now with the next steps, make sure to create/update the files and documents accordingly as necessary

## chat-14

> okay proceed now with the next steps, make sure to create/update the files and documents accordingly as necessary

## chat-15

> D:\Quant-Research-Strategies\scripts\run\_strategy\_002\_validation.py:105: DeprecationWarning: The 'generic' unit for NumPy timedelta is deprecated, and will raise an error in the future. This includes implicit conversion of bare integers (e.g. + 1). Please use a specific unit instead.
> next\_ts = ts + pd.Timedelta(minutes=5)
> Included instruments: 19
> Excluded instruments: 1
> Validation portfolios: 3699
> Outputs: data\reports\strategy\_002\_validation
> (.venv) D:\Quant-Research-Strategies>

Proceeding with the next step, I’ve now updated the repository on **`main`**.

### What I added

**1. Turnover/execution protocol**

```
research/journal/002_turnover_execution_decomposition_protocol.md
```

This locks down exactly what we are measuring and, importantly, explicitly protects the final holdout.

**2. Turnover decomposition implementation**

```
scripts/run_strategy_002_turnover_decomposition.py
```

It will measure, using **only 2026-06-10 → 2026-08-19**:

- portfolio observations

- long/short counts

- target portfolio weights

- gross/net exposure

- one-way turnover

- opened positions

- closed positions

- flipped positions

- unchanged positions

- turnover distribution

- 95th-percentile turnover

- validation-period portfolio churn

The frozen Strategy 002 signal itself has **not** been changed.

**3. Tests**

```
tests/test_strategy_002_turnover_decomposition.py
```

These check:

- market-neutral weight construction

- turnover calculation

- first-observation handling

**4. Updated Strategy Registry**

Strategy 002 is now explicitly recorded as:

> **Development diagnostic; frozen baseline not promotable, holdout locked**

rather than "active validation."

**5. Updated validation findings**

`research/journal/002_validation_findings.md` now records that the turnover/execution decomposition is the next diagnostic and that no lower-turnover conclusion has yet been made.

### One important point

I have **not fabricated or pre-filled turnover results**. The repository currently contains the implementation and protocol, but the actual output needs to be generated against your local Strategy 002 market-data files.

So the next thing for you to run locally is:

```cmd
pytest -q
```

Then:

```cmd
python scripts/run_strategy_002_turnover_decomposition.py <YOUR_STRATEGY_002_DATA_DIRECTORY>
```

Use the **same data directory you used for `run_strategy_002_validation.py`**.

The expected output directory is:

```
data\reports\strategy_002_turnover_decomposition
```

After it completes, send me:

```cmd
type data\reports\strategy_002_turnover_decomposition\turnover_summary.csv
```

and, if possible:

```cmd
type data\reports\strategy_002_turnover_decomposition\turnover_by_rebalance.csv
```

Then we'll make the actual methodological decision.

**We are still not touching the final holdout.**

The sequence is now:

```
Strategy 002 frozen baseline
        ↓
Validation failed cost-resilience gate
        ↓
Turnover/execution decomposition   ← WE ARE HERE
        ↓
      ┌───────────────┴───────────────┐
      ↓                               ↓
Economically hopeless          Credible lower-turnover
      ↓                         expression identified
Close Strategy 002                    ↓
                              New development experiment
                                      ↓
                              Development testing
                                      ↓
                              New candidate freeze
                                      ↓
                              Chronological validation
                                      ↓
                              ONLY THEN holdout
```

This keeps the research clean while still giving us one legitimate opportunity to determine whether **Strategy 002's underlying residual-reversal phenomenon is being destroyed primarily by the way we are implementing it**, rather than prematurely throwing away the entire mechanism.

___
###### [top](#table-of-contents)
## chat-16

> fix the warnings and proceed now with the next steps, make sure to create/update the files and documents accordingly as necessary

Done. I continued the Strategy 002 work and updated **`main`** directly.

### What I fixed

I corrected the turnover diagnostic so it distinguishes two things that were previously easy to conflate:

- **Target-weight turnover** — how much the hypothetical target portfolio changes from one signal to the next.

- **Actual executed turnover** — what the frozen strategy really trades.

This matters because Strategy 002 is a **one-bar strategy**: it enters the portfolio at the next bar's open and closes it at that bar's close.

Therefore, with normalized 100% gross exposure:

> **1.0× entry + 1.0× exit = 2.0× executed round-trip turnover per trade.**

The code and protocol now explicitly account for this.

I also made the pandas typing explicit in the weight construction and tightened timestamp/boundary handling to eliminate the likely warning sources rather than simply suppressing warnings.

### Files updated

- `scripts/run_strategy_002_turnover_decomposition.py`

- `tests/test_strategy_002_turnover_decomposition.py`

- `research/journal/002_turnover_execution_decomposition_protocol.md`

- `research/journal/002_validation_findings.md`

- `research/journal/strategy_registry.md`

- `README.md`

- `research/README.md`

The README files had stale text saying Strategy 002 was still in the initial exploratory/no-hypothesis phase. That is now synchronized with the actual research state.

## I also proceeded to the next research step

The turnover analysis gives us a very clear methodological question:

> **Can the residual-reversal signal be expressed with materially lower turnover while retaining enough of the effect to survive costs?**

Rather than modifying the frozen baseline, I registered a **new Strategy 002 development experiment**.

### New experiment

`research/journal/002_turnover_reduction_development_experiment.md`

The experiment is deliberately narrow and pre-registered:

| Variant | Holding period |
|---|---|
| H1 | Original 1 bar |
| H2 | 2 bars / 10 min |
| H3 | 3 bars / 15 min |
| H6 | 6 bars / 30 min |

The experiment:

- uses exactly the same leave-one-out residual signal;

- does not change the universe;

- does not change the long/short construction;

- does not optimize thresholds;

- does not rebalance while a position is active;

- does not carry positions overnight;

- uses non-overlapping trades;

- only changes the predetermined holding period.

This is economically motivated because the original research showed the reversal effect was strongest at short horizons and weakened later. We're therefore testing a **small nearby set**, rather than searching hundreds of holding periods.

### New implementation

```
scripts/run_strategy_002_turnover_reduction_development.py
tests/test_strategy_002_turnover_reduction_development.py
```

It is restricted to:

**Development:**  

`2025-09-18 → 2026-06-09`

and explicitly excludes:

**Validation:**  

`2026-06-10 → 2026-08-19`

**Holdout:**  

`2026-08-20 → 2026-09-17`

So we are **not contaminating the existing validation or final holdout** while trying to improve the implementation.

It will evaluate:

- gross return

- median return

- win rate

- drawdown

- trade count

- holding duration

- executed turnover

- return per unit of turnover

- 0 / 2 / 5 / 10 bps cost sensitivities

- chronological stability within the development sample

No result has been selected yet.

### One limitation

I could not actually execute the repository's full pytest suite or the market-data experiment from this environment because the repository's raw market-data directory is local to your machine and the execution environment here cannot clone the GitHub repository.

So I have **not claimed a test count or numerical H2/H3/H6 results that I haven't actually run**.

The code has been committed directly to `main`, and the repository is currently at commit:

`a65a6125ca6e6e9240541ee630a71c96f345ff63`

### Your next local run

Pull the changes:

```cmd
git pull origin main
```

Then run the focused tests:

```cmd
pytest -q tests/test_strategy_002_turnover_decomposition.py tests/test_strategy_002_turnover_reduction_development.py
```

Then run the turnover diagnostic:

```cmd
python scripts/run_strategy_002_turnover_decomposition.py <YOUR_STRATEGY_002_DATA_DIRECTORY>
```

And finally the new development experiment:

```cmd
python scripts/run_strategy_002_turnover_reduction_development.py <YOUR_STRATEGY_002_DATA_DIRECTORY>
```

Once those finish, send me the two summary files:

```cmd
type data\reports\strategy_002_turnover_decomposition\turnover_summary.csv
type data\reports\strategy_002_turnover_reduction_development\turnover_reduction_summary.csv
```

Then we'll evaluate H2/H3/H6 **systematically**, freeze at most one candidate, and only after that decide whether the existing validation period can be legitimately reopened for that frozen candidate. The final holdout remains untouched.

___
###### [top](#table-of-contents)
## chat-17

> D:\Quant-Research-Strategies\scripts\run_strategy_002_turnover_decomposition.py:168: DeprecationWarning: The 'generic' unit for NumPy timedelta is deprecated, and will raise an error in the future. This includes implicit conversion of bare integers (e.g. + 1). Please use a specific unit instead.
> next_ts = pd.Timestamp(ts) + pd.Timedelta(minutes=5)
> D:\Quant-Research-Strategies\scripts\run_strategy_002_turnover_decomposition.py:168: DeprecationWarning: The 'generic' unit for NumPy timedelta is deprecated, and will raise an error in the future. This includes implicit conversion of bare integers (e.g. + 1). Please use a specific unit instead.
> next_ts = pd.Timestamp(ts) + pd.Timedelta(minutes=5)
> Included instruments: 19
> Excluded instruments: 1
> Validation portfolios: 3699
> Outputs: data\reports\strategy_002_turnover_decomposition
> (.venv) D:\Quant-Research-Strategies>python scripts/run_strategy_002_turnover_reduction_development.py data/raw/strategy_002_universe
> Included instruments: 19
> Excluded instruments: 1
> Development variants: [2, 3, 6]
> Outputs: data\reports\strategy_002_turnover_reduction_development
> (.venv) D:\Quant-Research-Strategies>type data\reports\strategy_002_turnover_decomposition\turnover_summary.csv
> validation_start,validation_end_exclusive,included_instruments,excluded_instruments,portfolio_observations,target_turnover_observations,mean_one_way_target_turnover_pct,median_one_way_target_turnover_pct,p95_one_way_target_turnover_pct,mean_long_count,median_long_count,mean_short_count,median_short_count,mean_gross_exposure,mean_net_exposure,mean_executed_round_trip_turnover_pct,daily_executed_round_trip_turnover_multiple,median_holding_bars,mean_holding_minutes,holdout_used,optimization_performed
> 2026-06-10 00:00:00+05:30,2026-08-20 00:00:00+05:30,"['AXISBANK', 'BANKBEES', 'BHARTIARTL', 'GOLDBEES', 'HCLTECH', 'HDFCBANK', 'ICICIBANK', 'INFY', 'ITBEES', 'ITC', 'KOTAKBANK', 'LT', 'M&M', 'MARUTI', 'NIFTYBEES', 'RELIANCE', 'SBIN', 'SUNPHARMA', 'TATASTEEL']","[{'symbol': 'HINDUNILVR', 'reason': 'failed structural universe audit'}]",3699,3698,57.97866361475865,58.33333333333333,78.4090909090909,9.518788861854555,10.0,9.327115436604487,9.0,1.0,4.352050245218916e-19,200.0,147.96,1.0,5.0,False,False
> (.venv) D:\Quant-Research-Strategies>type data\reports\strategy_002_turnover_reduction_development\turnover_reduction_summary.csv
> holding_variant,holding_bars,cost_round_trip_bps,trades,mean_gross_return_bps,median_gross_return_bps,gross_win_rate,compounded_return_pct,max_drawdown_pct,mean_executed_turnover_per_trade,gross_return_per_turnover_bps,development_start,development_end_exclusive
> H2,2,0.0,4403,0.19211052872352435,0.21389593140164298,0.5275948217124687,8.78504196469294,-1.4277212449604115,2.0,0.09605526436176218,2025-09-18 00:00:00+05:30,2026-06-10 00:00:00+05:30
> H2,2,2.0,4403,-1.8078894712764755,-1.786104068598357,0.28367022484669546,-54.90810408755552,-54.93291810648996,2.0,0.09605526436176218,2025-09-18 00:00:00+05:30,2026-06-10 00:00:00+05:30
> H2,2,5.0,4403,-4.807889471276475,-4.786104068598357,0.08357937769702475,-87.97046090941417,-87.96921536825162,2.0,0.09605526436176218,2025-09-18 00:00:00+05:30,2026-06-10 00:00:00+05:30
> H2,2,10.0,4403,-9.807889471276477,-9.786104068598357,0.014535543947308653,-98.67122856947921,-98.66976101271355,2.0,0.09605526436176218,2025-09-18 00:00:00+05:30,2026-06-10 00:00:00+05:30
> H3,3,0.0,3171,0.2120660293152607,0.2556110201809942,0.5320088300220751,6.902150946518493,-1.4889957210576843,2.0,0.10603301465763035,2025-09-18 00:00:00+05:30,2026-06-10 00:00:00+05:30
> H3,3,2.0,3171,-1.7879339706847392,-1.744388979819006,0.3270261747082939,-43.306262134693675,-43.31561592628043,2.0,0.10603301465763035,2025-09-18 00:00:00+05:30,2026-06-10 00:00:00+05:30
> H3,3,5.0,3171,-4.7879339706847395,-4.744388979819006,0.13024282560706402,-78.10954780812934,-78.10413505258002,2.0,0.10603301465763035,2025-09-18 00:00:00+05:30,2026-06-10 00:00:00+05:30
> H3,3,10.0,3171,-9.78793397068474,-9.744388979819007,0.026174708293913593,-95.52102740745102,-95.51767819659223,2.0,0.10603301465763035,2025-09-18 00:00:00+05:30,2026-06-10 00:00:00+05:30
> H6,6,0.0,1761,-0.156390831117498,0.035842595433929744,0.5048268029528676,-2.7766476788879224,-6.790661438654688,2.0,-0.078195415558749,2025-09-18 00:00:00+05:30,2026-06-10 00:00:00+05:30
> H6,6,2.0,1761,-2.156390831117498,-1.9641574045660701,0.36740488358886997,-31.641224103729538,-31.620135472620237,2.0,-0.078195415558749,2025-09-18 00:00:00+05:30,2026-06-10 00:00:00+05:30
> H6,6,5.0,1761,-5.156390831117498,-4.96415740456607,0.18852924474730268,-59.70302766005835,-59.6760309582138,2.0,-0.078195415558749,2025-09-18 00:00:00+05:30,2026-06-10 00:00:00+05:30
> H6,6,10.0,1761,-10.156390831117497,-9.964157404566071,0.055650198750709826,-83.30513748946443,-83.28559006805492,2.0,-0.078195415558749,2025-09-18 00:00:00+05:30,2026-06-10 00:00:00+05:30
> (.venv) D:\Quant-Research-Strategies>
> 
> please fix the issues and commit it so I can sync locally and proceed now with the next steps, make sure to create/update the files and documents accordingly as necessary

Done. I fixed the warning and updated the research record based on the results you just ran.

### What was fixed

- Fixed the NumPy/Pandas timedelta deprecation in `run_strategy_002_turnover_decomposition.py`.

- The code now converts the timestamp to a native Python datetime before adding 5 minutes, so that specific deprecation warning should disappear.

- Clarified the turnover accounting:

    - target-weight turnover ≠ executed turnover;

    - one completed 100%-gross round trip = **2.0 normalized units** of executed turnover;

    - longer holding reduces trade frequency, but not turnover per completed trade.

### Strategy 002 decision

The H2/H3/H6 experiment is now formally **closed**.

| Variant | Gross mean/trade | At 2 bps cost | Decision |
|---|---|---|---|
| H2 | +0.1921 bps | -1.8079 bps | ❌ |
| H3 | +0.2121 bps | -1.7879 bps | ❌ |
| H6 | -0.1564 bps | -2.1564 bps | ❌ |

So there is no defensible reason to reopen the protected validation period for any of these variants.

The final holdout **2026-08-20 → 2026-09-17 remains untouched**.

This closes the **tested Strategy 002 executable research line**, not the claim that every possible residual-reversal phenomenon is impossible.

### Documents updated

I updated:

- `README.md`

- `research/README.md`

- `research/journal/strategy_registry.md`

- `research/journal/002_validation_findings.md`

- `research/journal/002_turnover_execution_decomposition_protocol.md`

- `research/journal/002_turnover_reduction_development_experiment.md`

Created:

- `research/journal/002_turnover_reduction_development_findings.md`

And fixed:

- `scripts/run_strategy_002_turnover_decomposition.py`

### Commit

Latest commit on **main**:

`2db1bfae922cdf63b7c4eb29e6876431d9c6d122`

There are **no GitHub Actions/CI runs configured for this commit**, so I cannot honestly claim that the modified code passed pytest remotely. The scripts you ran before the warning fix did execute successfully; the warning fix itself has not been executed by me in your local environment.

### Sync locally

Use Windows CMD:

```cmd
cd /d D:\Quant-Research-Strategies
git pull origin main
```

Then verify the warning fix and repository tests:

```cmd
pytest -q
```

And, if you want to rerun the decomposition just to confirm the warning is gone:

```cmd
python scripts/run_strategy_002_turnover_decomposition.py data/raw/strategy_002_universe
```

You should no longer see the `generic unit for NumPy timedelta` warning.

### What we do next

**Strategy 002 is finished. We should not squeeze another parameter search out of it.**

The next research cycle should be **Strategy 003**, with a genuinely different economic mechanism and preferably a different asset class, rather than another variation of residual reversal.

The repository is now documented accordingly: Strategy 003 is the next open slot, while the Strategy 002 validation and final holdout evidence remain preserved.

___
###### [top](#table-of-contents)

