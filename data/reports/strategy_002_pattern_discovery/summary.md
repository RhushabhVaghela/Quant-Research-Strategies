# Strategy 002 — Exploratory Pattern Discovery Summary

**Status:** descriptive/exploratory only. No hypothesis or strategy selected.

## Research controls

- Exploratory window: 2025-09-18 00:00:00+05:30 through 2026-06-09 23:59:59+05:30
- Instruments included: 19
- Instruments excluded: 1
- Holdout used: **false**
- Strategy P&L calculated: **false**

## 1. Return dynamics

The table below describes the cross-instrument distribution of autocorrelation diagnostics. It does not identify a preferred lag or instrument.

| Lag | Median return ACF | Q25 | Q75 | Median absolute-return ACF | Q25 | Q75 |
|---:|---:|---:|---:|---:|---:|---:|
| 1 | -0.011094 | -0.030339 | -0.006030 | 0.145156 | 0.135973 | 0.172495 |
| 2 | -0.000197 | -0.003764 | 0.004547 | 0.100819 | 0.090348 | 0.114448 |
| 3 | -0.003181 | -0.014339 | 0.003000 | 0.093351 | 0.087710 | 0.121573 |
| 6 | 0.009059 | 0.000053 | 0.015952 | 0.097934 | 0.087860 | 0.107933 |
| 12 | 0.013995 | 0.006996 | 0.019560 | 0.059745 | 0.049073 | 0.065668 |
| 24 | 0.010619 | 0.005987 | 0.015181 | 0.026425 | 0.017335 | 0.037807 |

## 2. Forward-horizon behavior

Conditional forward-return distributions are shown by state and horizon. Differences here are exploratory and are not entry/exit rules.

| State | Bucket | Horizon | Median forward return | Q25 | Q75 | Sign counts |
|---|---|---:|---:|---:|---:|---|
| all | ALL | 1 | -0.00000571 | -0.00001433 | 0.00000701 | positive=7, negative=12, zero=0 |
| all | ALL | 2 | -0.00001152 | -0.00002897 | 0.00001386 | positive=7, negative=12, zero=0 |
| all | ALL | 3 | -0.00001731 | -0.00004368 | 0.00002065 | positive=6, negative=13, zero=0 |
| all | ALL | 6 | -0.00003461 | -0.00008785 | 0.00004117 | positive=6, negative=13, zero=0 |
| all | ALL | 12 | -0.00006936 | -0.00017599 | 0.00008182 | positive=6, negative=13, zero=0 |
| prior_6_return_negative | ALL | 1 | 0.00001324 | -0.00000168 | 0.00001997 | positive=13, negative=6, zero=0 |
| prior_6_return_negative | ALL | 2 | 0.00000418 | -0.00002218 | 0.00001809 | positive=10, negative=9, zero=0 |
| prior_6_return_negative | ALL | 3 | -0.00000730 | -0.00003714 | 0.00002259 | positive=9, negative=10, zero=0 |
| prior_6_return_negative | ALL | 6 | -0.00006632 | -0.00012434 | 0.00002613 | positive=6, negative=13, zero=0 |
| prior_6_return_negative | ALL | 12 | -0.00017971 | -0.00030433 | -0.00000029 | positive=5, negative=14, zero=0 |
| prior_6_return_positive | ALL | 1 | -0.00001657 | -0.00003099 | -0.00001139 | positive=4, negative=15, zero=0 |
| prior_6_return_positive | ALL | 2 | -0.00002384 | -0.00004469 | -0.00000071 | positive=5, negative=14, zero=0 |
| prior_6_return_positive | ALL | 3 | -0.00001899 | -0.00005757 | 0.00001307 | positive=6, negative=13, zero=0 |
| prior_6_return_positive | ALL | 6 | -0.00001138 | -0.00006833 | 0.00005625 | positive=7, negative=12, zero=0 |
| prior_6_return_positive | ALL | 12 | 0.00002825 | -0.00007525 | 0.00012457 | positive=11, negative=8, zero=0 |
| prior_abs_return_quartile | Q1 | 1 | -0.00000001 | -0.00001258 | 0.00001857 | positive=9, negative=10, zero=0 |
| prior_abs_return_quartile | Q1 | 2 | 0.00000726 | -0.00002051 | 0.00002598 | positive=12, negative=7, zero=0 |
| prior_abs_return_quartile | Q1 | 3 | -0.00000293 | -0.00003618 | 0.00002320 | positive=8, negative=11, zero=0 |
| prior_abs_return_quartile | Q1 | 6 | -0.00000718 | -0.00008903 | 0.00003098 | positive=9, negative=10, zero=0 |
| prior_abs_return_quartile | Q1 | 12 | -0.00008282 | -0.00020038 | 0.00006285 | positive=8, negative=11, zero=0 |
| prior_abs_return_quartile | Q2 | 1 | -0.00002394 | -0.00003384 | -0.00001260 | positive=3, negative=16, zero=0 |
| prior_abs_return_quartile | Q2 | 2 | -0.00001619 | -0.00003298 | -0.00000637 | positive=4, negative=15, zero=0 |
| prior_abs_return_quartile | Q2 | 3 | -0.00002392 | -0.00006818 | -0.00000150 | positive=5, negative=14, zero=0 |
| prior_abs_return_quartile | Q2 | 6 | -0.00007368 | -0.00012219 | 0.00000434 | positive=5, negative=14, zero=0 |
| prior_abs_return_quartile | Q2 | 12 | -0.00011629 | -0.00025033 | 0.00006452 | positive=6, negative=13, zero=0 |
| prior_abs_return_quartile | Q3 | 1 | -0.00000885 | -0.00001945 | 0.00001834 | positive=8, negative=11, zero=0 |
| prior_abs_return_quartile | Q3 | 2 | -0.00001952 | -0.00003368 | 0.00000291 | positive=6, negative=13, zero=0 |
| prior_abs_return_quartile | Q3 | 3 | -0.00002740 | -0.00005012 | 0.00001931 | positive=7, negative=12, zero=0 |
| prior_abs_return_quartile | Q3 | 6 | -0.00004475 | -0.00010625 | 0.00002367 | positive=5, negative=14, zero=0 |
| prior_abs_return_quartile | Q3 | 12 | -0.00005946 | -0.00021900 | 0.00012020 | positive=7, negative=12, zero=0 |
| prior_abs_return_quartile | Q4 | 1 | 0.00001031 | -0.00000138 | 0.00002415 | positive=14, negative=5, zero=0 |
| prior_abs_return_quartile | Q4 | 2 | 0.00000901 | -0.00001984 | 0.00001997 | positive=12, negative=7, zero=0 |
| prior_abs_return_quartile | Q4 | 3 | 0.00000730 | -0.00003441 | 0.00003807 | positive=11, negative=8, zero=0 |
| prior_abs_return_quartile | Q4 | 6 | 0.00000979 | -0.00003767 | 0.00007693 | positive=11, negative=8, zero=0 |
| prior_abs_return_quartile | Q4 | 12 | 0.00002779 | -0.00009877 | 0.00011806 | positive=11, negative=8, zero=0 |
| prior_return_negative | ALL | 1 | 0.00002889 | 0.00000785 | 0.00003504 | positive=16, negative=3, zero=0 |
| prior_return_negative | ALL | 2 | 0.00002881 | 0.00000617 | 0.00003721 | positive=16, negative=3, zero=0 |
| prior_return_negative | ALL | 3 | 0.00001167 | -0.00001116 | 0.00003861 | positive=12, negative=7, zero=0 |
| prior_return_negative | ALL | 6 | -0.00000923 | -0.00004673 | 0.00007338 | positive=9, negative=10, zero=0 |
| prior_return_negative | ALL | 12 | -0.00009777 | -0.00019572 | 0.00007424 | positive=7, negative=12, zero=0 |
| prior_return_positive | ALL | 1 | -0.00003165 | -0.00004047 | -0.00002009 | positive=1, negative=18, zero=0 |
| prior_return_positive | ALL | 2 | -0.00004066 | -0.00006621 | -0.00002009 | positive=2, negative=17, zero=0 |
| prior_return_positive | ALL | 3 | -0.00003676 | -0.00006323 | -0.00000586 | positive=4, negative=15, zero=0 |
| prior_return_positive | ALL | 6 | -0.00005213 | -0.00011307 | 0.00000756 | positive=6, negative=13, zero=0 |
| prior_return_positive | ALL | 12 | -0.00004775 | -0.00015013 | 0.00011651 | positive=6, negative=13, zero=0 |

## 3. Cross-sectional dependence

- 5-minute pair correlations: 171 directional-free pairs.
- Daily pair correlations: 171 pairs.

| Diagnostic | Median | Q25 | Q75 | Min | Max |
|---|---:|---:|---:|---:|---:|
| 5-minute correlation | 0.310677 | 0.211052 | 0.457939 | 0.001699 | 0.861167 |
| Daily correlation | 0.274782 | 0.152280 | 0.496321 | -0.037230 | 0.918193 |

## 4. Lead-lag diagnostics

These are directional dependence diagnostics only. They are not treated as arbitrage evidence.

| Lag | Median correlation | Q25 | Q75 | Min | Max |
|---:|---:|---:|---:|---:|---:|
| 1 | 0.002750 | -0.006031 | 0.010682 | -0.031820 | 0.047395 |
| 2 | 0.001236 | -0.005120 | 0.007183 | -0.025475 | 0.029010 |
| 3 | -0.003646 | -0.011671 | 0.003018 | -0.032677 | 0.025115 |
| 6 | 0.005205 | -0.002215 | 0.011718 | -0.035142 | 0.030829 |
| 12 | 0.009009 | -0.000917 | 0.015779 | -0.018269 | 0.033329 |
| 24 | 0.004983 | 0.000441 | 0.009698 | -0.021177 | 0.025837 |

## 5. PCA/common-factor structure

| Component | Explained variance | Cumulative explained variance |
|---:|---:|---:|
| 1 | nan | nan |

## Interpretation guardrails

- This summary does not rank instruments or declare a winning pattern.
- No parameter, threshold, holding period, or strategy rule is selected here.
- Any potentially interesting pattern must be characterized for breadth, stability, economic mechanism, and execution implications before a hypothesis is written.
- Development validation and the final chronological holdout remain untouched.
