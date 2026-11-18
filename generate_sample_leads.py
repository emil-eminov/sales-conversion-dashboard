# Generates 6,000 synthetic leads (Nov 2025 to Oct 2026) for the sales dashboard homework.
# Output: sales_leads_synthetic.csv
import numpy as np, pandas as pd
rng=np.random.default_rng(42)
N=6000
start=pd.Timestamp('2025-11-01'); end=pd.Timestamp('2026-10-31')
days=(end-start).days+1
dates=start+pd.to_timedelta(rng.integers(0,days,N),unit='D')
agents={'A. Ramirez':1.10,'B. Chen':1.05,'C. Okafor':1.00,'D. Patel':0.97,'E. Novak':0.93,'F. Brooks':0.85,'G. Haddad':1.02,'H. Lindqvist':0.80}
channels={'Phone':(0.38,1.10),'Web Form':(0.34,0.85),'Live Chat':(0.16,0.95),'SMS':(0.12,0.75)}
sources={'Google Ads':(0.30,1.00),'Facebook Ads':(0.22,0.78),'Organic Search':(0.15,1.10),'TV':(0.13,0.90),'Referral Partner':(0.12,1.30),'Radio':(0.08,0.85)}
ag=rng.choice(list(agents),N)
ch=rng.choice(list(channels),N,p=[v[0] for v in channels.values()])
src=rng.choice(list(sources),N,p=[v[0] for v in sources.values()])
am=np.array([agents[a] for a in ag]); cm=np.array([channels[c][1] for c in ch]); sm=np.array([sources[s][1] for s in src])
# mild seasonality / trend
mi=((dates.year-2025)*12+dates.month-11).values
trend=1+0.012*mi
def p(base,mult): return np.clip(base*mult,0,0.98)
eval_done=rng.random(N)<p(0.70,cm**0.6*am**0.5)
# evaluation result among completed
qual=sm**0.8*trend
r=rng.random(N)
pe=np.clip(0.30*qual,0,0.5); pw=np.clip(0.22*qual,0,0.4); pb=np.clip(0.08*qual,0,0.15)
res=np.where(r<pe,'Employment',np.where(r<pe+pw,'WC',np.where(r<pe+pw+pb,'Both','Neither')))
res=np.where(eval_done,res,'')
emp_pass=np.isin(res,['Employment','Both']); wc_pass=np.isin(res,['WC','Both'])
sign_p=p(0.62,am**1.6*sm**0.4)
emp_ret=emp_pass&(rng.random(N)<sign_p); wc_ret=wc_pass&(rng.random(N)<p(0.68,am**1.6*sm**0.4))
intake_p=p(0.82,am**0.8*cm**0.3)
emp_int=emp_ret&(rng.random(N)<intake_p); wc_int=wc_ret&(rng.random(N)<p(0.86,am**0.8*cm**0.3))
df=pd.DataFrame({'lead_id':[f'L{100000+i}' for i in range(N)],'lead_date':dates.strftime('%Y-%m-%d'),
 'agent':ag,'channel':ch,'source':src,'evaluation_completed':eval_done,'evaluation_result':res,
 'emp_retainer_signed':emp_ret,'wc_retainer_signed':wc_ret,'emp_intake_completed':emp_int,'wc_intake_completed':wc_int}).sort_values('lead_date').reset_index(drop=True)
df.to_csv('sales_leads_synthetic.csv',index=False)
print(df.head()); print(df.evaluation_result.value_counts())
