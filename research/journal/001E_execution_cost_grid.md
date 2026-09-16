# Strategy 001E — Execution Cost Grid

This file defines the cost grid **before inspecting the audit output**.

| Transaction cost / side | Slippage / side |
|---:|---:|
| 0 bps | 0, 1, 2, 3, 5 bps |
| 1 bps | 0, 1, 2, 3, 5 bps |
| 2 bps | 0, 1, 2, 3, 5 bps |
| 3 bps | 0, 1, 2, 3, 5 bps |
| 4 bps | 0, 1, 2, 3, 5 bps |
| 5 bps | 0, 1, 2, 3, 5 bps |
| 7.5 bps | 0, 1, 2, 3, 5 bps |
| 10 bps | 0, 1, 2, 3, 5 bps |

For a round trip, the simplified friction represented by a row is:

`2 × (transaction_cost_bps_per_side + slippage_bps_per_side)`.

This grid is a sensitivity analysis, not an estimate of the user's actual Zerodha/NSE costs. Actual paper/live execution assumptions will be established separately using current broker/exchange documentation and observed execution data.

No cell may be selected as the preferred result merely because it produces the most attractive historical performance.
