"""Run hypothesis-free cross-sectional residual pattern discovery for Strategy 002."""
from __future__ import annotations
import argparse
from pathlib import Path
import numpy as np
import pandas as pd

START = pd.Timestamp("2025-09-18", tz="Asia/Kolkata")
END = pd.Timestamp("2026-06-09 23:59:59", tz="Asia/Kolkata")
VALIDATION_START = pd.Timestamp("2026-06-10", tz="Asia/Kolkata")
HORIZONS = (1, 2, 3, 6, 12)

def args():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("directory",type=Path)
    p.add_argument("--audit-report",type=Path,default=Path("data/reports/strategy_002_universe_audit.csv"))
    p.add_argument("--output-dir",type=Path,default=Path("data/reports/strategy_002_cross_sectional_residual"))
    return p.parse_args()

def load(path):
    df=pd.read_csv(path,parse_dates=["timestamp"])
    req={"timestamp","open","high","low","close","volume"}
    if not req.issubset(df.columns): raise ValueError(f"{path}: missing columns")
    ts=pd.DatetimeIndex(df["timestamp"])
    if ts.tz is None: raise ValueError(f"{path}: timestamps must be timezone-aware")
    df["timestamp"]=ts.tz_convert("Asia/Kolkata")
    df=df.sort_values("timestamp")
    if df["timestamp"].duplicated().any() or not df["timestamp"].is_monotonic_increasing:
        raise ValueError(f"{path}: invalid timestamps")
    for c in ["open","high","low","close","volume"]: df[c]=pd.to_numeric(df[c],errors="coerce")
    if df[["open","high","low","close"]].isna().any().any() or (df[["open","high","low","close"]]<=0).any().any():
        raise ValueError(f"{path}: invalid OHLC")
    if df["volume"].isna().any() or (df["volume"]<0).any(): raise ValueError(f"{path}: invalid volume")
    out=df.loc[(df.timestamp>=START)&(df.timestamp<=END),["timestamp","close"]].copy()
    if out.empty: raise ValueError(f"{path}: no exploratory observations")
    if out.timestamp.max()>=VALIDATION_START: raise AssertionError(f"{path}: crossed validation boundary")
    return out

def main():
    a=args(); a.output_dir.mkdir(parents=True,exist_ok=True)
    audit=pd.read_csv(a.audit_report)
    eligible=set(audit.loc[(audit.unexpected_interval_count==0)&(audit.zero_volume_rows==0),"symbol"].astype(str))
    series={}
    excluded=[]
    for path in sorted(a.directory.glob("*_5minute.csv")):
        symbol=path.name.removeprefix("NSE_").removesuffix("_5minute.csv")
        if symbol not in eligible: excluded.append({"symbol":symbol,"reason":"failed structural universe audit"}); continue
        try:
            d=load(path); series[symbol]=d.set_index("timestamp")["close"]
        except (ValueError,AssertionError) as e: excluded.append({"symbol":symbol,"reason":str(e)})
    if len(series)<3: raise SystemExit("Need at least three eligible instruments")
    panel=pd.DataFrame(series).sort_index()
    returns=panel.pct_change(fill_method=None)
    market=returns.mean(axis=1,skipna=True)
    residual=returns.sub(market,axis=0)
    rows=[]
    for h in HORIZONS:
        future=residual.shift(-h)
        for state,mask in {
            "prior_negative": residual<0,
            "prior_positive": residual>0,
        }.items():
            x=future.where(mask)
            for symbol in residual.columns:
                vals=x[symbol].dropna()
                rows.append({"symbol":symbol,"state":state,"horizon_bars":h,"observations":len(vals),"mean":vals.mean(),"median":vals.median(),"positive_fraction":(vals>0).mean() if len(vals) else np.nan})
        mag=residual.abs()
        q=pd.DataFrame({c:pd.qcut(mag[c].dropna(),4,labels=["Q1","Q2","Q3","Q4"],duplicates="drop").reindex(mag.index) for c in mag})
        for state,signmask in {"negative":residual<0,"positive":residual>0}.items():
            for quart in ["Q1","Q2","Q3","Q4"]:
                mask=signmask & (q==quart)
                vals=future.where(mask)
                for symbol in residual.columns:
                    z=vals[symbol].dropna()
                    rows.append({"symbol":symbol,"state":f"prior_{state}_abs_{quart}","horizon_bars":h,"observations":len(z),"mean":z.mean(),"median":z.median(),"positive_fraction":(z>0).mean() if len(z) else np.nan})
    detail=pd.DataFrame(rows)
    breadth=(detail.groupby(["state","horizon_bars"],as_index=False).agg(
        instruments=("symbol","nunique"),median_instrument_mean=("mean","median"),
        q25_instrument_mean=("mean",lambda x:x.quantile(.25)),
        q75_instrument_mean=("mean",lambda x:x.quantile(.75)),
        positive_instrument_fraction=("mean",lambda x:(x>0).mean())))
    stability=[]
    time_index=pd.Series(residual.index.astype("int64"),index=residual.index)
    periods=pd.qcut(time_index,4,labels=["Q1_time","Q2_time","Q3_time","Q4_time"],duplicates="drop")
    for period in periods.cat.categories:
        idx=periods==period
        sub=residual.loc[idx]
        for lag in [1,2,3,6,12,24]:
            for symbol in residual.columns:
                x=sub[symbol].dropna()
                ac=x.autocorr(lag=lag) if len(x)>lag else np.nan
                stability.append({"period":str(period),"symbol":symbol,"lag":lag,"residual_return_acf":ac})
    detail.to_csv(a.output_dir/"per_instrument_residual_patterns.csv",index=False)
    breadth.to_csv(a.output_dir/"residual_pattern_breadth.csv",index=False)
    pd.DataFrame(stability).to_csv(a.output_dir/"residual_temporal_stability.csv",index=False)
    pd.DataFrame({"timestamp":market.index,"cross_sectional_mean_return":market.values}).to_csv(a.output_dir/"cross_sectional_market_return.csv",index=False)
    pd.DataFrame(excluded).to_csv(a.output_dir/"excluded_instruments.csv",index=False)
    manifest={"exploratory_start":str(START),"exploratory_end":str(END),"validation_start":str(VALIDATION_START),"included_instruments":sorted(series),"excluded_instruments":excluded,"holdout_used":False,"strategy_pnl_calculated":False}
    pd.Series(manifest,dtype="object").to_json(a.output_dir/"run_manifest.json",indent=2)
    print(f"Included instruments: {len(series)}")
    print(f"Excluded instruments: {len(excluded)}")
    print(f"Outputs: {a.output_dir}")

if __name__=="__main__": main()
