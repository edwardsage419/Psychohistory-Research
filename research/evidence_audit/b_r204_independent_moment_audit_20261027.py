#!/usr/bin/env python3
"""B-track independent finite convolution audit. No imports from R-track script.
Usage: python b_r204_independent_moment_audit_20261027.py RECEIPT.json
"""
import json,sys
from collections import defaultdict
from fractions import Fraction as F
from itertools import product
P={'IID':[[int(i==j) for i in range(5)] for j in range(5)],'CONSTANT':[[1]*5],'ALTERNATING':[[1,-1,1,-1,1]],'LINEAR':[[-2,-1,0,1,2]]}
S={'EXTRAPOLATION':([0,1,2],[3,4]),'INTERPOLATION':([0,2,4],[1,3]),'GAP':([0,1,4],[2,3])}
def convolution(features):
 d={(0,0,0,0,0):F(1)}
 for v in features:
  nxt=defaultdict(F)
  for f,p in d.items():
   for z in (-1,1):nxt[tuple(f[i]+z*v[i] for i in range(5))]+=p/2
  d=nxt
 return d
def independent_moments(k,train,test):
 mass=defaultdict(F);first=defaultdict(lambda:[F(0),F(0)]);second=defaultdict(lambda:[F(0),F(0)])
 for f,p in convolution(P[k]).items():
  for e in product((-1,1),repeat=3):
   y=tuple(f[i]+e[j] for j,i in enumerate(train));weight=p/8
   mass[y]+=weight
   for j,t in enumerate(test):
    first[y][j]+=weight*f[t];second[y][j]+=weight*f[t]*f[t]
 risk=sum((sum((second[y][j]-first[y][j]**2/mass[y] for j in range(2)),F(0))/2 for y in mass),F(0))
 assert sum(mass.values(),F(0))==1
 return risk,len(mass)
def main(path):
 j=json.load(open(path,encoding='utf-8'));assert len(j['worlds'])==12
 checks=0
 for w in j['worlds']:
  tr,te=S[w['split']];risk,distinct=independent_moments(w['true_kernel'],tr,te)
  assert risk==F(w['risk_exact']['bayes']);checks+=1
  assert distinct==w['distinct_observed_y'];checks+=1
  for k in ('gp_true','gp_selected','zero'):
   assert F(w['risk_exact'][k])>=risk;checks+=1
   assert F(w['risk_exact'][k])-risk==F(w['excess_over_discrete_bayes_exact'][k]);checks+=1
 positive=sum(F(w['risk_exact']['bayes'])>0 for w in j['worlds'])
 assert positive==9
 assert all(F(w['risk_exact']['bayes'])==F(1,8) for w in j['worlds'] if w['true_kernel']=='CONSTANT')
 print(json.dumps({'result':'PASS','worlds':12,'exact_cross_algorithm_field_checks':checks,'discrepancies':0,'lookahead_oracle_leakage_negative_control_positive_worlds':positive,'false_zero_noise_negative_control_constant_worlds':3,'external_independent_replication':False},indent=2))
if __name__=='__main__':main(sys.argv[1])
