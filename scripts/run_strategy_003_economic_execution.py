"""Evaluate the frozen Strategy 003 signal under fixed executable economics."""
from __future__ import annotations
import argparse, json
from pathlib import Path
import numpy as np
import pandas as pd

BROKER_RATE=0.0003; BROKER_CAP=20.0; STT_RATE=0.00025; NSE_TX_RATE=0.0000307; STAMP_RATE=0.00003; SEBI_RATE=0.000001; GST_RATE=0.18
FRICTIONS={'fee_floor':(0.0,0.0),'low':(0.00005,0.00005),'base':(0.00010,0.00005),'stress':(0.00020,0.00010)}

def parse_args():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('directory',type=Path,nargs='?',default=Path('data/raw/strategy_002_universe'))
    p.add_argument('--validation-dir',type=Path,default=Path('data/reports/strategy_003_protected_validation'))
    p.add_argument('--output-dir',type=Path,default=Path('data/reports/strategy_003_economic_execution'))
    return p.parse_args()

def brokerage(turnover): return np.minimum(BROKER_CAP,BROKER_RATE*turnover)

def fee_breakdown(orders):
    buy=orders.loc[orders.side=='buy','notional'].sum(); sell=orders.loc[orders.side=='sell','notional'].sum(); total=orders.notional.sum()
    broker=brokerage(orders.notional).sum(); tx=NSE_TX_RATE*total; stt=STT_RATE*sell; stamp=STAMP_RATE*buy; sebi=SEBI_RATE*total; gst=GST_RATE*(broker+tx+sebi)
    return {'brokerage':broker,'stt':stt,'stamp_duty':stamp,'sebi':sebi,'gst':gst,'fee_total':broker+stt+stamp+sebi+gst}

def main():
    a=parse_args(); a.output_dir.mkdir(parents=True,exist_ok=True)
    s=pd.read_csv(a.validation_dir/'protected_validation_scored_observations.csv',parse_dates=['timestamp'])
    s['timestamp']=pd.DatetimeIndex(s.timestamp).tz_convert('Asia/Kolkata')
    s['quintile']=s.groupby('timestamp').prediction.rank(method='first',pct=True).map(lambda x:min(5,int(np.ceil(x*5))))
    rows=[]
    for ts,g in s.groupby('timestamp',sort=True):
        long=g[g.quintile==5]; short=g[g.quintile==1]
        if len(long)!=3 or len(short)!=3: continue
        # Dollar-neutral return; the common cross-sectional mean cancels.
        gross=0.5*long.target_excess_1bar.mean()-0.5*short.target_excess_1bar.mean()
        rows.append({'timestamp':ts,'gross_return':gross})
    bars=pd.DataFrame(rows)
    if bars.empty: raise ValueError('No complete Q1/Q5 portfolios')
    orders=pd.DataFrame([{'timestamp':ts,'side':side,'notional':1/6} for ts in bars.timestamp for side in ('buy','sell') for _ in range(6)])
    fees=fee_breakdown(orders); total_gross=bars.gross_return.sum()
    out=[]
    for name,(spread,impact) in FRICTIONS.items():
        extra=(spread+impact)*2*len(bars)
        total_cost=fees['fee_total']+extra; net=total_gross-total_cost
        out.append({'scenario':name,'timestamps':len(bars),'gross_cumulative_return':total_gross,'fee_only_cost':fees['fee_total'],'additional_execution_friction':extra,'total_cost':total_cost,'net_cumulative_return':net,'mean_gross_bps':bars.gross_return.mean()*1e4,'mean_net_bps_per_bar':net/len(bars)*1e4})
    pd.DataFrame(out).to_csv(a.output_dir/'economic_scenario_summary.csv',index=False)
    pd.DataFrame([fees]).to_csv(a.output_dir/'fee_breakdown.csv',index=False)
    bars.to_csv(a.output_dir/'gross_portfolio_bars.csv',index=False)
    manifest={'experiment':'003_economic_execution','status':'executed_on_frozen_validation_signal','portfolio':'top_Q5_long_bottom_Q1_short_equal_notional_50_50_gross','holding_bars':1,'gross_exposure':1.0,'net_exposure':0.0,'final_holdout_used':False,'feature_search':False,'threshold_search':False,'holding_period_search':False,'universe_search':False,'cost_search':False}
    (a.output_dir/'run_manifest.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
    print('Strategy 003 economic execution test complete'); print(f'Portfolio timestamps: {len(bars)}'); print(f'Outputs: {a.output_dir}')

if __name__=='__main__': main()