#!/usr/bin/env python3
"""R264 S60 independent four-outcome Fraction oracle; internal nonblind E1 only."""
import argparse
import copy
import json
from fractions import Fraction as F
from pathlib import Path

WORLD = {
 'IID_GRADIENT':('123','123'),
 'COMPLEMENTARY_GRADIENT':('123','321'),
 'REVERSED_COMPLEMENT':('321','123'),
 'FIRST_ONLY_INFORMATIVE':('123','222'),
 'SECOND_ONLY_INFORMATIVE':('222','123'),
 'NO_SIGNAL':('222','222'),
 'DETERMINISTIC_ENDS':('024','420'),
 'NONMONOTONE_IID':('132','132'),
 'FIRST_WITH_SECOND_QUARTER':('123','111')
}
KINDS=('FULL_HAMMING','COUNT_SUM','FIRST_COMPONENT')
GOALS=('NEXT_Y1','NEXT_Y2','THETA_EQ_2')
FIELDS=('exact_event_probability','abc_event_probability','signed_probability_bias',
        'excess_expected_brier','expected_brier','oracle_expected_brier')
PROTOCOL='4d400965d1c50b4af6ed67ec8b52d7b07b27db05'

def normalize(v):
    z=sum(v)
    if z<=0:raise ValueError('zero posterior')
    return tuple(x/z for x in v)

def discrepancy(kind,a,b):
    if kind=='FULL_HAMMING':return int(a!=1)+int(b!=0)
    if kind=='COUNT_SUM':return int(a+b!=1)
    if kind=='FIRST_COMPONENT':return int(a!=1)
    raise ValueError('invalid distance')

def analytic():
    result={}
    for world,(a,b) in WORLD.items():
        q1=tuple(F(int(x),4) for x in a)
        q2=tuple(F(int(x),4) for x in b)
        exact=normalize([q1[t]*(1-q2[t]) for t in range(3)])
        for kind in KINDS:
            for eps in (0,1,2):
                likelihood=[]
                for t in range(3):
                    likelihood.append(sum(
                        (q1[t] if y1 else 1-q1[t])*(q2[t] if y2 else 1-q2[t])
                        for y1 in (0,1) for y2 in (0,1)
                        if discrepancy(kind,y1,y2)<=eps))
                abc=normalize(likelihood)
                for goal in GOALS:
                    g=q1 if goal=='NEXT_Y1' else q2 if goal=='NEXT_Y2' else (F(0),F(0),F(1))
                    true=sum(exact[t]*g[t] for t in range(3))
                    pred=sum(abc[t]*g[t] for t in range(3))
                    bias=pred-true
                    base=true*(1-true)
                    result[(world,kind,eps,goal)]=(true,pred,bias,bias*bias,base+bias*bias,base)
    assert len(result)==243
    return result

def compare(j):
    if j.get('prescore_protocol_commit')!=PROTOCOL:raise ValueError('protocol')
    if j.get('evidence')!='E1_SYNTHETIC_EXACT_CONDITIONAL_RISK':raise ValueError('evidence')
    if j.get('new_real_human_E2')!=0 or j.get('new_historical_E3')!=0:raise ValueError('E2/E3')
    if j.get('R073')!='FROZEN' or j.get('PESEN_v0_1')!='FROZEN':raise ValueError('freeze')
    reference=analytic()
    rows=j.get('results')
    if type(rows) is not list or len(rows)!=243:raise ValueError('coverage')
    seen=set()
    for row in rows:
        if type(row['epsilon']) is not int:raise ValueError('epsilon type')
        if any(type(row[f]) is not str for f in FIELDS):raise ValueError('fraction type')
        if set(row)!={'world','discrepancy','epsilon','target',*FIELDS}:raise ValueError('fields')
        key=(row['world'],row['discrepancy'],row['epsilon'],row['target'])
        if key in seen or key not in reference:raise ValueError('identity')
        seen.add(key)
        if tuple(F(row[f]) for f in FIELDS)!=reference[key]:raise ValueError('metric '+str(key))
    if seen!=set(reference):raise ValueError('missing')
    return len(seen)*len(FIELDS)

def negatives(j):
    cases=[]
    x=copy.deepcopy(j);x['results'][1]=copy.deepcopy(x['results'][0]);cases.append(('duplicate',x))
    x=copy.deepcopy(j);x['results'][0]['expected_brier']='999';cases.append(('metric',x))
    x=copy.deepcopy(j);x['evidence']='E2_HUMAN';cases.append(('evidence',x))
    x=copy.deepcopy(j);x['results'].pop();cases.append(('missing',x))
    x=copy.deepcopy(j);x['results'][0]['epsilon']=False;cases.append(('bool_epsilon',x))
    passed=[]
    for name,bad in cases:
        try:compare(bad)
        except (ValueError,TypeError,KeyError,ZeroDivisionError):passed.append(name)
        else:raise AssertionError('false PASS: '+name)
    return passed

if __name__=='__main__':
    p=argparse.ArgumentParser()
    p.add_argument('receipt',type=Path)
    args=p.parse_args()
    data=json.loads(args.receipt.read_text(encoding='utf-8'))
    print(json.dumps({'fraction_fields_verified':compare(data),
                      'negative_controls_rejected':negatives(data),
                      'scope':'INTERNAL_NONBLIND_E1_ONLY'},indent=2))
