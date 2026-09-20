from pathlib import Path
import pandas as pd
from scripts.run_strategy_002_cross_sectional_residual import load, START, VALIDATION_START

def test_load_slices_exploratory_only(tmp_path: Path):
    p=tmp_path/"NSE_TEST_5minute.csv"
    ts=pd.date_range("2025-09-18 09:15",periods=4,freq="5min",tz="Asia/Kolkata")
    pd.DataFrame({"timestamp":ts,"open":[1,2,3,4],"high":[2,3,4,5],"low":[1,2,3,4],"close":[1.5,2.5,3.5,4.5],"volume":[1,1,1,1]}).to_csv(p,index=False)
    out=load(p)
    assert out.timestamp.max()<VALIDATION_START
    assert out.timestamp.min()>=START
