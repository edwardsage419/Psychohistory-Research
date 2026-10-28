#!/usr/bin/env python3
"""R250 S46 independent exact symbolic audit. No original CSV or R code imports."""
import json
from fractions import Fraction as Q
WORLDS = [
 ('CHAIN_P_QUARTER','CHAIN',Q(1,4)),('CHAIN_P_HALF','CHAIN',Q(1,2)),
 ('CHAIN_P_THREE_QUARTER','CHAIN',Q(3,4)),('TRIANGLE_P_ZERO','TRIANGLE',Q(0)),
 ('TRIANGLE_P_QUARTER','TRIANGLE',Q(1,4)),('TRIANGLE_P_HALF','TRIANGLE',Q(1,2)),
 ('TRIANGLE_P_THREE_QUARTER','TRIANGLE',Q(3,4)),('TRIANGLE_P_ONE','TRIANGLE',Q(1)),
 ('TRIANGLE_STATIC_TRUE_GRAPH_REPORT_ALIAS','TRIANGLE',Q(1,2))
]
def solve():
 out=[]
 for name,top,p in WORLDS:
  if top=='CHAIN':
   t=p*p
   q0,q1=Q(0),p
   f01=p*p*(1-p)
   gain=p**3*(1-p)
   support=1 if p in (0,1) else 4
  else:
   t=3*p*p-2*p**3
   q0,q1=p*p,2*p-p*p
   f01=p*q1*(1-q1)+(1-p)*q0*(1-q0)
   gain=4*p**3*(1-p)**3
   support=1 if p in (0,1) else 8
  f0=t*(1-t)
  assert f0-f01==gain and 0<=f01<=f0
  out.append(dict(world=name,f0=str(f0),f01=str(f01),fall='0',gain=str(gain),
   remaining=str(f01),target_rate=str(t),q0=str(q0),q1=str(q1),
   support_f0=1,support_f01=1 if p in (0,1) else 2,support_fall=support,
   oracle_true_target_rate='0' if name.endswith('ALIAS') else str(t)))
 return out
if __name__=='__main__':
 print(json.dumps({'research_id':'R250_S46','method':'independent_Fraction_closed_form','worlds':solve()},indent=2))
