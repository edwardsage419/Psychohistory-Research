#!/usr/bin/env python3
"""Independent R245 S41 16-gap probability-law route. Python standard library."""
from fractions import Fraction as F
from itertools import product
import json
WORLDS=('IID_FAIR','IID_SHORT_3OF4','IID_LONG_1OF4','DETERMINISTIC_UNIT','DETERMINISTIC_TWO','LATENT_RATE_MIXTURE','ALTERNATING_RATE','COMMON_GAP_SHOCK','STATIC_HIDDEN_EVENT_SENSOR_ALIAS')
FEATURES=((),(3,),(2,3),(1,2,3))
NAMES=('F0','F3','F23','F123')
def pshort(w,i,u):
 if w in ('IID_FAIR','COMMON_GAP_SHOCK','STATIC_HIDDEN_EVENT_SENSOR_ALIAS'):return F(1,2)
 if w=='IID_SHORT_3OF4':return F(3,4)
 if w=='IID_LONG_1OF4':return F(1,4)
 if w=='DETERMINISTIC_UNIT':return F(1)
 if w=='DETERMINISTIC_TWO':return F(0)
 if w=='LATENT_RATE_MIXTURE':return F(3,4) if u==0 else F(1,4)
 if w=='ALTERNATING_RATE':return F(3,4) if i%2 else F(1,4)
 raise ValueError(w)
def gaplaw(w,gaps):
 if w=='COMMON_GAP_SHOCK':return F(1,2) if gaps in ((1,)*4,(2,)*4) else F(0)
 def prod(u):
  v=F(1)
  for i,g in enumerate(gaps,1):
   p=pshort(w,i,u);v*=p if g==1 else 1-p
  return v
 return (prod(0)+prod(1))/2 if w=='LATENT_RATE_MIXTURE' else prod(0)
def path(gaps):
 s=0;arrival=[]
 for g in gaps:s+=g;arrival.append(s)
 return tuple(sum(x<=t for x in arrival) for t in range(5))
def calculate():
 result=[];checks=0
 for w in WORLDS:
  paths={}
  for gaps in product((1,2),repeat=4):
   p=gaplaw(w,gaps);checks+=1
   if p:
    y=path(gaps);paths[y]=paths.get(y,F(0))+p
  assert sum(paths.values(),F(0))==1
  risk={}
  for name,features in zip(NAMES,FEATURES):
   groups={}
   for y,p in paths.items():
    key=tuple(y[i] for i in features);total,yes=groups.get(key,(F(0),F(0)))
    groups[key]=(total+p,yes+(p if y[4]>y[3] else 0));checks+=1
   risk[name]=sum((yes*(total-yes)/total for total,yes in groups.values()),F(0));checks+=len(groups)
  assert all(risk[NAMES[i]]>=risk[NAMES[i+1]] for i in range(3))
  assert all(F(0)<=x<=F(1,4) for x in risk.values())
  result.append({'world':w,'risks':{k:str(v) for k,v in risk.items()},'gain_F0_F123':str(risk['F0']-risk['F123']),'gain_F3_F123':str(risk['F3']-risk['F123'])})
  checks+=7
 assert result[0]['risks']==result[-1]['risks']
 return {'audit':'R245_S41_B_16_GAP_INDEPENDENT_LAW','worlds':9,'checks':checks,'failed':0,'results':result,'evidence':'E1 synthetic oracle only'}
if __name__=='__main__':print(json.dumps(calculate(),indent=2))
