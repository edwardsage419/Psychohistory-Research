#!/usr/bin/env python3
"""R215 S11: exhaustive artificial three-period DiD pretrend selection audit.
Frozen source: research/R215/r215_exact_three_period_did.py, Git blob
f2a4f26bddcb5c97d3d3168cbea0d3e8a7a657fa. No external dependencies.
"""
import itertools, json
from fractions import Fraction as F

# Original 12 structural worlds: bT,bC,sT,sC,qT,qC,anticip,tau.
W = {
 'PARALLEL_NULL': (3,0,1,1,0,0,0,0),
 'PARALLEL_TAU_TWO': (3,0,1,1,0,0,0,2),
 'PARALLEL_NEGATIVE': (3,0,1,1,0,0,0,-2),
 'LEVEL_GAP_ONLY': (10,0,1,1,0,0,0,0),
 'DIFFERENTIAL_SLOPE_FALSE': (3,0,2,1,0,0,0,0),
 'DIFFERENTIAL_SLOPE_TAU_TWO': (3,0,2,1,0,0,0,2),
 'POST_SHOCK_FALSE': (3,0,1,1,2,0,0,0),
 'POST_SHOCK_WITH_TAU_MINUS_ONE': (3,0,1,1,3,0,0,-1),
 'ANTICIPATION_TAU_TWO': (3,0,1,1,0,0,1,2),
 'ANTICIPATION_NULL': (3,0,1,1,0,0,1,0),
 'CONTROL_POST_SHOCK': (3,0,1,1,0,2,0,0),
 'LARGE_DIFF_SLOPE': (3,0,3,0,0,0,0,0),
}
H=(1,2,4)
def obs(w,eps):
 bT,bC,sT,sC,qT,qC,a,tau=w
 base=(bT-sT,bT+a,bT+sT+qT+tau,bC-sC,bC,bC+sC+qC)
 return tuple(x+e for x,e in zip(base,eps))
def scores(y):
 tm,t0,tp,cm,c0,cp=y
 d=(tp-cp)-(t0-c0)
 p=(t0-c0)-(tm-cm)
 return d,p,d-p

def moments(vals,tau):
 n=len(vals)
 if not n:return None
 out={}
 for name,ix in (('D',0),('C',2)):
  x=[F(v[ix]) for v in vals]
  m=sum(x,F(0))/n
  var=sum(((z-m)**2 for z in x),F(0))/n
  mse=sum(((z-tau)**2 for z in x),F(0))/n
  out[name]={'mean':str(m),'variance':str(var),'mse_ATT':str(mse)}
 return out

def main():
 rows=[]; checks=0
 for name,w in W.items():
  tau=F(w[-1]); source=[]
  for eps in itertools.product((-1,1),repeat=6):
   y=obs(w,eps);d,p,c=scores(y)
   assert c==d-p
   # Invariance to a common level shift.
   assert scores(tuple(z+19 for z in y))==(d,p,c)
   checks+=2
   source.append((d,p,c))
  full=moments(source,tau)
  assert full['D']['variance']=='4' and full['C']['variance']=='12'
  checks+=2
  for h in H:
   selected=[s for s in source if abs(s[1])<=h]
   assert selected
   m=moments(selected,tau)
   record={'world':name,'threshold':h,'true_ATT':str(tau),
           'accepted_source_count':len(selected),
           'accept_probability':str(F(len(selected),64)),
           'D':m['D'],'C':m['C'],
           'D_mean_shift_from_full':str(F(m['D']['mean'])-F(full['D']['mean'])),
           'C_mean_shift_from_full':str(F(m['C']['mean'])-F(full['C']['mean'])),
           'D_MSE_change_from_full':str(F(m['D']['mse_ATT'])-F(full['D']['mse_ATT'])),
           'C_MSE_change_from_full':str(F(m['C']['mse_ATT'])-F(full['C']['mse_ATT']))}
   rows.append(record)
   checks+=1
  # Negative controls: full inclusion and intentionally incorrect C.
  assert len(source)==64 and moments(source,tau)==full
  assert any((d+p)!=(d-p) for d,p,c in source)
  checks+=2
 assert len(rows)==36
 assert any(F(r['D_MSE_change_from_full'])>0 for r in rows)
 assert any(F(r['D_MSE_change_from_full'])<0 for r in rows)
 assert any(F(r['D_mean_shift_from_full'])!=0 for r in rows)
 # Wrong complement selection changes acceptance for at least one case.
 assert any(sum(abs(scores(obs(w,e))[1])>1 for e in itertools.product((-1,1),repeat=6)) !=
            sum(abs(scores(obs(w,e))[1])<=1 for e in itertools.product((-1,1),repeat=6)) for w in W.values())
 checks+=5
 summary={'status':'BOUNDED_SYNTHETIC_E1_INTERNAL','worlds':12,
          'original_panels':768,'thresholds':list(H),'world_threshold_combinations':36,
          'evaluation_slots':2304,'checks':checks,
          'D_MSE_increased':sum(F(r['D_MSE_change_from_full'])>0 for r in rows),
          'D_MSE_decreased':sum(F(r['D_MSE_change_from_full'])<0 for r in rows),
          'D_MSE_equal':sum(F(r['D_MSE_change_from_full'])==0 for r in rows),
          'D_conditional_mean_shift_nonzero':sum(F(r['D_mean_shift_from_full'])!=0 for r in rows),
          'E2':0,'E3':0,'external_replications':0}
 return {'summary':summary,'rows':rows}
if __name__=='__main__':print(json.dumps(main(),ensure_ascii=False,sort_keys=True,indent=2))
