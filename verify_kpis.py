# Recomputes the dashboard's headline KPIs from the CSV to check the dashboard math.
import pandas as pd

df = pd.read_csv('sales_leads_synthetic.csv')
n = len(df)
ev = df.evaluation_completed.sum()
ps = df.evaluation_result.isin(['Employment', 'WC', 'Both']).sum()
sg = (df.emp_retainer_signed | df.wc_retainer_signed).sum()
ia = (df.emp_intake_completed | df.wc_intake_completed).sum()
ie = df.emp_intake_completed.sum()
iw = df.wc_intake_completed.sum()
ib = (df.emp_intake_completed & df.wc_intake_completed).sum()

print(dict(leads=n, evaluations=ev, passes=ps, retainers=sg, any_intakes=ia, emp_intakes=ie, wc_intakes=iw, dual_intakes=ib))
print('Employment conversion', ie / n, '| WC conversion', iw / n, '| Dual-case', ib / n, '| Any-case', ia / n)
steps = [ev / n, ps / ev, sg / ps, ia / sg]
print('Supporting KPIs', steps, '| product', steps[0] * steps[1] * steps[2] * steps[3])
print(df.groupby('agent').emp_intake_completed.mean().sort_values())
