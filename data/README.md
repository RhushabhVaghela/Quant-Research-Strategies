# Data

Local market data belongs here.

Raw CSV/Parquet files are ignored by Git by default. Do not commit private account
data or credentials. The instrument master should be refreshed locally rather than
relying on hard-coded instrument tokens.

## Strategy 001J U1

The active Strategy 001J experiment uses a point-in-time Nifty 100 equity universe.

Required local inputs:

```text
data/
├── universe/
│   ├── strategy_001j_u1_membership.csv
│   └── strategy_001j_u1_membership_metadata.json
└── raw/
    └── strategy_001j_u1/
        ├── SYMBOL1.csv
        ├── SYMBOL2.csv
        └── ...
```

The membership file must contain effective-date intervals. Do not populate it with
the current Nifty 100 constituent list for the full historical period.

Each 5-minute symbol file must contain:

```text
timestamp,open,high,low,close,volume
```

Before backtesting 001J, run:

```powershell
python scripts/validate_strategy_001j_u1_membership.py
python scripts/audit_strategy_001j_u1_data.py
```

Only after both gates pass should the frozen-001D transfer baseline be run.
