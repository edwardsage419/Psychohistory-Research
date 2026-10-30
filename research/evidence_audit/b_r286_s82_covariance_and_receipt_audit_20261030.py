#!/usr/bin/env python3
"""Independent nonblind R286 S82 covariance oracle and strict receipt gate.
Usage: python b_r286_s82_covariance_and_receipt_audit_20261030.py CSV JSON
"""
import csv
import json
import sys
from collections import defaultdict
from copy import deepcopy
from fractions import Fraction as F
from pathlib import Path

POLICIES = ('TD0_ONLINE_CORRECT','MC_COMPLETE_RETURN','B_THEN_A_UPDATED_BOOTSTRAP')
COEFF = {
    POLICIES[0]: (F(1,8),F(3,16),F(1,4),F(1,4),F(0)),
    POLICIES[1]: (F(1,32),F(1,16),F(1,8),F(1,4),F(1,2)),
    POLICIES[2]: (F(5,64),F(1,8),F(3,16),F(1,4),F(1,4)),
}
STAYS = (F(1,4),F(1,2),F(3,4))
COLS = ('stay_probability','rho','policy','source_6bits','training_5bits',
        'future_Y6','source_mass','VA5','heldout_Brier')

def risk_by_moments(s, policy):
    rho = 2*s-1
    c = COEFF[policy]
    second = sum((c[i]*c[j]*rho**abs(i-j) for i in range(5)
                  for j in range(5)),F(0))
    cross = sum((c[i]*rho**(5-i) for i in range(5)),F(0))
    return F(1,4)+(1-sum(c))**2/4+second/4-cross/2

def audit(rows, result):
    if len(rows) != 576 or len(result.get('results',[])) != 9:
        raise ValueError('full row/world coverage')
    if tuple(rows[0].keys()) != COLS:
        raise ValueError('exact columns')
    if result.get('scope') != 'INTERNAL_NONBLIND_ARTIFICIAL_E1_MARKOV_REWARD_DEPENDENCE':
        raise ValueError('E1 scope')
    if result.get('R073') != 'FROZEN' or result.get('PESEN_v0_1') != 'FROZEN':
        raise ValueError('freeze identity')
    if result.get('new_E2_predictions') != 0 or result.get('new_E3_predictions') != 0:
        raise ValueError('E2/E3 overclaim')
    seen=set();mass=defaultdict(lambda:F(0));score=defaultdict(lambda:F(0))
    for row in rows:
        s=F(row['stay_probability']);p=row['policy'];seq=row['source_6bits']
        if s not in STAYS or p not in POLICIES or len(seq)!=6 or set(seq)-{'0','1'}:
            raise ValueError('unfrozen world or source')
        key=(s,p,seq)
        if key in seen: raise ValueError('duplicate source')
        seen.add(key)
        bits=tuple(map(int,seq))
        same=sum(a==b for a,b in zip(bits,bits[1:]))
        weight=F(1,2)*s**same*(1-s)**(5-same)
        value=sum((COEFF[p][i]*bits[i] for i in range(5)),F(0))
        loss=(bits[5]-value)**2
        if (row['training_5bits']!=seq[:5] or int(row['future_Y6'])!=bits[5]
            or F(row['rho'])!=2*s-1 or F(row['source_mass'])!=weight
            or F(row['VA5'])!=value or F(row['heldout_Brier'])!=loss):
            raise ValueError('source, probability, future, or score mismatch')
        mass[s,p]+=weight
        score[s,p]+=weight*loss
    expected={(s,p,format(i,'06b')) for s in STAYS for p in POLICIES for i in range(64)}
    if seen!=expected: raise ValueError('incomplete source universe')
    actual={(F(x['stay_probability']),x['policy']):x for x in result['results']}
    if set(actual)!={(s,p) for s in STAYS for p in POLICIES}:
        raise ValueError('missing or duplicate summary world')
    for (s,p),item in actual.items():
        oracle=risk_by_moments(s,p)
        if (mass[s,p]!=1 or score[s,p]!=oracle or F(item['exact_heldout_Brier'])!=oracle
            or F(item['independent_covariance_Brier'])!=oracle
            or F(item['delta_vs_constant_half'])!=oracle-F(1,4)
            or item['constant_half_baseline_Brier']!='1/4'
            or item['complete_sources']!=64):
            raise ValueError('mass, summary, or covariance oracle mismatch')
    return len(seen),len(actual)

def mutations(rows, obj):
    failures=0
    def must_reject(r,o):
        nonlocal failures
        try:audit(r,o)
        except (ValueError,KeyError,TypeError,AssertionError):failures+=1
        else:raise AssertionError('mutation falsely accepted')
    r=deepcopy(rows);r[1]=deepcopy(r[0]);must_reject(r,obj)
    r=deepcopy(rows);r.pop();must_reject(r,obj)
    r=deepcopy(rows);r[0]['source_mass']='1/2';must_reject(r,obj)
    r=deepcopy(rows);r[0]['heldout_Brier']='999';must_reject(r,obj)
    r=deepcopy(rows);r[0]['VA5']='999';must_reject(r,obj)
    o=deepcopy(obj);o['results'][0]['exact_heldout_Brier']='999';must_reject(rows,o)
    o=deepcopy(obj);o['new_E2_predictions']=1;must_reject(rows,o)
    o=deepcopy(obj);o['R073']='ADOPTED';must_reject(rows,o)
    return failures

if __name__=='__main__':
    if len(sys.argv)!=3:raise SystemExit('usage: audit.py CSV JSON')
    with Path(sys.argv[1]).open(newline='',encoding='utf-8') as f:
        rows=list(csv.DictReader(f))
    obj=json.loads(Path(sys.argv[2]).read_text(encoding='utf-8'))
    sources,worlds=audit(rows,obj)
    print(json.dumps(dict(pass_audit=True,sources=sources,worlds=worlds,
                          mutations_rejected=mutations(rows,obj),
                          evidence='INTERNAL_NONBLIND_E1',external_replication='NOT_RUN')))
