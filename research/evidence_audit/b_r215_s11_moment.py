#!/usr/bin/env python3
"""Independent B: combinatorial conditional-moment audit of R215 S11.
No import from R code, no use of R computed results. Frozen original-world
structural mean tuples transcribed from R215-3P original parameters.
"""
import json
from fractions import Fraction as F
from math import comb

# Frozen-world structure: (true_ATT, mu_D, mu_P), derived from original 3P W.
WORLD={
 'PARALLEL_NULL':(0,0,0),
 'PARALLEL_TAU_TWO':(2,2,0),
 'PARALLEL_NEGATIVE':(-2,-2,0),
 'LEVEL_GAP_ONLY':(0,0,0),
 'DIFFERENTIAL_SLOPE_FALSE':(0,1,1),
 'DIFFERENTIAL_SLOPE_TAU_TWO':(2,3,1),
 'POST_SHOCK_FALSE':(0,2,0),
 'POST_SHOCK_WITH_TAU_MINUS_ONE':(-1,2,0),
 'ANTICIPATION_TAU_TWO':(2,1,1),
 'ANTICIPATION_NULL':(0,-1,1),
 'CONTROL_POST_SHOCK':(0,-2,0),
 'LARGE_DIFF_SLOPE':(0,3,3),
}

def cond(tau,muD,muP,h):
 muC=muD-muP
 atoms=[(F(2*k-4),F(comb(4,k),16)) for k in range(5)]
 included=[(s,p) for s,p in atoms if h is None or abs(muP+s)<=h]
 z=sum((p for s,p in included),F(0))
 assert z>0
 out={'accept_probability':str(z),'accepted_source_count':str(64*z)}
 for label,mu,slope,quadratic in (('D',muD,F(-1,2),F(1,6)),('C',muC,F(-3,2),F(13,6))):
  mean=sum((p*(mu+slope*s) for s,p in included),F(0))/z
  second=sum((p*(mu*mu+2*mu*slope*s+F(10,3)+quadratic*s*s) for s,p in included),F(0))/z
  var=second-mean*mean
  mse=second-2*tau*mean+tau*tau
  out[label]={'mean':str(mean),'variance':str(var),'mse_ATT':str(mse)}
 return out

def main():
 rows=[];baseline={};checks=0
 for name,(t,d,p) in WORLD.items():
  full=cond(F(t),F(d),F(p),None)
  assert full['accept_probability']=='1'
  assert full['D']['variance']=='4'
  assert full['C']['variance']=='12'
  baseline[name]=full
  checks+=3
  for h in (1,2,4):
   row=cond(F(t),F(d),F(p),F(h))
   row.update({'world':name,'threshold':h,'true_ATT':str(t)})
   for key in ('D','C'):
    row[key+'_mean_shift_from_full']=str(F(row[key]['mean'])-F(full[key]['mean']))
    row[key+'_MSE_change_from_full']=str(F(row[key]['mse_ATT'])-F(full[key]['mse_ATT']))
   rows.append(row)
   checks+=7
 assert len(rows)==36
 return {'summary':{'worlds':12,'threshold_combinations':36,'baseline_checks':36,'analytic_field_checks':252,'total_internal_checks':checks},'rows':rows,'baseline':baseline}
if __name__=='__main__':print(json.dumps(main(),ensure_ascii=False,sort_keys=True,indent=2))
