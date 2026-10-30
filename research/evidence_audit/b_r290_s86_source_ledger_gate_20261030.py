#!/usr/bin/env python3
"""Strict independent 1950-row training ledger gate, no R imports.
Usage: python b_r290_s86_source_ledger_gate.py R290_S86_ALL_1950_TRAINING_SOURCES.csv
"""
import csv
import io
import json
import sys
from collections import defaultdict
from fractions import Fraction as F
from itertools import product

DGP = {'MONOTONE':((8,6,4,2,1),(1,2,4,6,8),21),
       'CENTERED':((8,2,1,2,8),(1,3,13,3,1),21),
       'IDENTICAL':((1,2,3,2,1),(1,2,3,2,1),9)}
FIELDS = ['dgp','m','noise_draws','signal_draws','probability']

def check(rows):
    seen=set();mass=defaultdict(lambda:F(0));counts=defaultdict(int)
    for row in rows:
        if set(row)!=set(FIELDS):raise ValueError('schema mismatch')
        name=row['dgp']
        if name not in DGP or row['m'] not in ('1','2'):raise ValueError('world or m')
        m=int(row['m']);a=row['noise_draws'];b=row['signal_draws']
        if len(a)!=m or len(b)!=m or any(ch not in '01234' for ch in a+b):raise ValueError('invalid sequence')
        key=(name,m,a,b)
        if key in seen:raise ValueError('duplicate source')
        seen.add(key)
        n,s,d=DGP[name]
        p=F(1)
        for ch in a:p*=F(n[int(ch)],d)
        for ch in b:p*=F(s[int(ch)],d)
        if F(row['probability'])!=p:raise ValueError('source mass mismatch')
        mass[(name,m)]+=p;counts[(name,m)]+=1
    if len(rows)!=1950 or len(seen)!=1950:raise ValueError('incomplete source universe')
    for name in DGP:
        for m in (1,2):
            if counts[(name,m)]!=5**(2*m) or mass[(name,m)]!=1:
                raise ValueError('source count or probability total')
            expected={(name,m,''.join(map(str,a)),''.join(map(str,b))) for a in product(range(5),repeat=m) for b in product(range(5),repeat=m)}
            if not expected.issubset(seen):raise ValueError('missing source key')
    return len(seen)

def mutations(rows):
    import copy
    tests=[('duplicate',lambda r:r.__setitem__(1,copy.deepcopy(r[0]))),
           ('missing',lambda r:r.pop()),
           ('probability',lambda r:r[0].__setitem__('probability','0')),
           ('sequence',lambda r:r[0].__setitem__('noise_draws','4')),
           ('world',lambda r:r[0].__setitem__('dgp','UNKNOWN'))]
    rejected=[]
    for label,mut in tests:
        bad=copy.deepcopy(rows);mut(bad)
        try:check(bad)
        except (ValueError,AssertionError):rejected.append(label)
        else:raise AssertionError('accepted corruption '+label)
    return rejected

if __name__=='__main__':
    with open(sys.argv[1],newline='',encoding='utf-8') as f:rows=list(csv.DictReader(f))
    print(json.dumps({'status':'PASS','verified_sources':check(rows),'rejected_mutations':mutations(rows)},indent=2))
