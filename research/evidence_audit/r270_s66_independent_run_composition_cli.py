#!/usr/bin/env python3
"""R270 S66 independent exact run-composition audit; Python standard library."""
import argparse
import json
from fractions import Fraction as F
from math import comb

PRIORS=((1,1),(2,2),(1,3))
THETAS=(F(1,4),F(1,2),F(3,4))
ALPHAS=(F(1,20),F(1,10),F(1,5))

def rising(x,n):
    p=1
    for j in range(n):p*=x+j
    return p

def comps(n,r):
    return comb(n-1,r-1) if n>=r>0 else int(n==0 and r==0)

def run_count(k,t):
    if k in (0,6):return int(t==5)
    r=6-t
    return sum(comps(k,(r+1)//2 if start else r//2)*
               comps(6-k,r//2 if start else (r+1)//2) for start in (0,1))

def lower(prior,obs):
    a,b=prior;K=obs.bit_count();A=a+K;B=b+6-K
    t=sum(((obs>>i)&1)==((obs>>(i+1))&1) for i in range(5))
    den=rising(A+B,6)
    return sum((F(run_count(k,j)*rising(A,k)*rising(B,6-k),den)
                for k in range(7) for j in range(t+1)),F(0))

def expected():
    tails={};alarms={}
    for a,b in PRIORS:
        key=f'{a},{b}'
        ps=[lower((a,b),i) for i in range(64)]
        tails[key]=[str(v) for v in ps]
        for theta in THETAS:
            for alpha in ALPHAS:
                chosen=[i for i,p in enumerate(ps) if p<=alpha]
                prob=sum((theta**i.bit_count()*(1-theta)**(6-i.bit_count()) for i in chosen),F(0))
                alarms[f'{key}|{theta}|{alpha}']={
                    'alarm_sequence_count':len(chosen),
                    'alarm_probability':str(prob),
                    'probability_minus_nominal':str(prob-alpha)}
    return tails,alarms

def check(data):
    if type(data) is not dict or set(data)!={'research','evidence','protocol',
            'observation_count_per_prior','replicates_per_observation',
            'priors','generating_thetas','thresholds','lower_tails','alarms'}:
        raise ValueError('schema')
    if data['research']!='R270_S66' or data['evidence']!='E1_ARTIFICIAL' or \
       data['protocol']!='R270_S66_PRIOR_PREDICTIVE_PPC_FALSE_ALARM_PRESCORE_FREEZE_2026-10-29.md':
        raise ValueError('identity')
    if type(data['observation_count_per_prior']) is not int or data['observation_count_per_prior']!=64 or \
       type(data['replicates_per_observation']) is not int or data['replicates_per_observation']!=64:
        raise ValueError('source count')
    if data['priors']!=['1,1','2,2','1,3'] or \
       data['generating_thetas']!=['1/4','1/2','3/4'] or \
       data['thresholds']!=['1/20','1/10','1/5']:
        raise ValueError('universe')
    tails,alarms=expected()
    if type(data['lower_tails']) is not dict or data['lower_tails']!=tails:
        raise ValueError('192 exact tail mismatch')
    if type(data['alarms']) is not dict or data['alarms']!=alarms:
        raise ValueError('27 exact alarm mismatch')
    return True

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--check')
    ap.add_argument('--selftest',action='store_true')
    args=ap.parse_args()
    assert sum(run_count(k,t) for k in range(7) for t in range(6))==64
    assert all(sum(run_count(k,t) for t in range(6))==comb(6,k) for k in range(7))
    if args.selftest:
        from copy import deepcopy
        tails,alarms=expected()
        good={'research':'R270_S66','evidence':'E1_ARTIFICIAL',
          'protocol':'R270_S66_PRIOR_PREDICTIVE_PPC_FALSE_ALARM_PRESCORE_FREEZE_2026-10-29.md',
          'observation_count_per_prior':64,'replicates_per_observation':64,
          'priors':['1,1','2,2','1,3'],'generating_thetas':['1/4','1/2','3/4'],
          'thresholds':['1/20','1/10','1/5'],'lower_tails':tails,'alarms':alarms}
        assert check(good)
        bad=[]
        x=deepcopy(good);x['alarms']['1,1|1/4|1/20']['alarm_probability']='999';bad.append(x)
        x=deepcopy(good);x['lower_tails']['1,1'].pop();bad.append(x)
        x=deepcopy(good);x['lower_tails']['1,1'].append('1');bad.append(x)
        x=deepcopy(good);x['evidence']='E2_HUMAN';bad.append(x)
        x=deepcopy(good);x['observation_count_per_prior']=False;bad.append(x)
        for i,v in enumerate(bad):
            try:check(v)
            except ValueError:continue
            raise AssertionError(f'negative control {i} accepted')
        print('PASS: run-count combinatorics, 192 tails, 27 alarms, 5 negative controls')
    if args.check:
        with open(args.check,encoding='utf8') as f:check(json.load(f))
        print('PASS: archived receipt 192 exact tails and 27 exact alarm probabilities')

if __name__=='__main__':main()
