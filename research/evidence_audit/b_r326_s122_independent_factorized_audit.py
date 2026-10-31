#!/usr/bin/env python3
"""Independent no-import exact R326 S122 audit. Standard library only, nonblind E1."""
from __future__ import annotations
import argparse
import csv
import hashlib
import io
import itertools
import json
from fractions import Fraction as Q
from pathlib import Path

FROZEN_CSV_BLOB = '3d2481365160c33fabbba7f8be6c3a9ff78e5121'
THETA = (Q(1,4),Q(3,4))
COLUMNS = ('law','history_id','h11','h12','h21','h22','h31','h32',
           'target_group','next_y','joint_mass','hier_prediction',
           'independent_prediction','constant_prediction',
           'hier_squared_loss','independent_squared_loss','constant_squared_loss',
           'hier_weighted_brier','independent_weighted_brier','constant_weighted_brier')

def likelihood(t, obs):
    x = Q(1)
    for bit in obs:
        x *= t if bit else (1-t)
    return x

def group_moments(obs, z=None):
    """Factorized per-group evidence and success-weighted evidence."""
    hi = Q(1,2) if z is None else (Q(3,4) if z else Q(1,4))
    terms = ((1-hi)*likelihood(THETA[0],obs),hi*likelihood(THETA[1],obs))
    return sum(terms),sum(t*w for t,w in zip(THETA,terms))

def atom(h,g,y,law):
    groups = [h[j:j+2] for j in (0,2,4)]
    if law == 'I':
        moms = [group_moments(x) for x in groups]
        mass = Q(1)
        for j,(m,u) in enumerate(moms):
            mass *= (u if y else m-u) if j==g else m
        return mass
    if law == 'H':
        total = Q(0)
        for z in (0,1):
            moms = [group_moments(x,z) for x in groups]
            mass = Q(1,2)
            for j,(m,u) in enumerate(moms):
                mass *= (u if y else m-u) if j==g else m
            total += mass
        return total
    raise ValueError('law')

def make_expected():
    records = []
    sums = {(law,k):Q(0) for law in ('H','I') for k in range(3)}
    for ident,h in enumerate(itertools.product((0,1),repeat=6)):
        for g in range(3):
            mass = {law:[atom(h,g,y,law) for y in (0,1)] for law in ('H','I')}
            pred = [mass['H'][1]/sum(mass['H']),mass['I'][1]/sum(mass['I']),Q(1,2)]
            for law in ('H','I'):
                for y in (0,1):
                    w = mass[law][y]
                    losses = [(p-y)**2 for p in pred]
                    weighted = [w*x for x in losses]
                    records.append([law,str(ident),*(str(x) for x in h),str(g+1),str(y),str(w),
                                    *(str(x) for x in pred),*(str(x) for x in losses),
                                    *(str(x) for x in weighted)])
                    for k in range(3):
                        sums[law,k] += weighted[k]/3
    return records,sums

def check_records(rows):
    if len(rows)!=768:
        raise ValueError('wrong number of records')
    expected,sums=make_expected()
    seen=set()
    for i,(actual,correct) in enumerate(zip(rows,expected)):
        if set(actual)!=set(COLUMNS):
            raise ValueError('schema mismatch')
        key=(actual['law'],actual['history_id'],actual['target_group'],actual['next_y'])
        if key in seen:raise ValueError('duplicate')
        seen.add(key)
        if [actual[c] for c in COLUMNS]!=correct:
            raise ValueError('wrong atom %d'%i)
    if len(seen)!=768:raise ValueError('incomplete key set')
    for law in ('H','I'):
        for g in range(1,4):
            if sum(Q(r['joint_mass']) for r in rows if r['law']==law and int(r['target_group'])==g)!=1:
                raise ValueError('mass')
    return sums

def check_summary(s,sums):
    if s['schema']!='r326_s122_exact_predictive_brier_v1' or s['atoms']!=768 or s['artificial_only'] is not True:
        raise ValueError('summary scope')
    if s['scope']!='E1_ONLY_NO_HUMAN_E2_NO_HISTORICAL_E3':raise ValueError('grade')
    for law in ('H','I'):
        for k,label in enumerate(('hierarchical','independent','constant')):
            if Q(s['losses'][law][label])!=sums[law,k]:raise ValueError('summary loss')
    if Q(s['contrasts']['H_independent_minus_hierarchical'])!=sums['H',1]-sums['H',0]:raise ValueError('H contrast')
    if Q(s['contrasts']['I_hierarchical_minus_independent'])!=sums['I',0]-sums['I',1]:raise ValueError('I contrast')
    if not all(s['checks'].values()):raise ValueError('missing source check')

def mutations(rows,s):
    import copy
    rejected=[]
    for label,change in [
        ('delete',lambda a:a.pop()),
        ('duplicate',lambda a:a.__setitem__(1,dict(a[0]))),
        ('law',lambda a:a[0].__setitem__('law','I')),
        ('mass',lambda a:a[0].__setitem__('joint_mass','1/64')),
        ('predict',lambda a:a[0].__setitem__('hier_prediction','1/2')),
        ('weighted',lambda a:a[0].__setitem__('hier_weighted_brier','0')),
    ]:
        a=copy.deepcopy(rows)
        change(a)
        try:check_records(a)
        except ValueError:rejected.append(label)
    bad=copy.deepcopy(s);bad['scope']='E2_HUMAN'
    try:check_summary(bad,check_records(rows))
    except ValueError:rejected.append('grade')
    bad=copy.deepcopy(s);bad['losses']['H']['hierarchical']='0'
    try:check_summary(bad,check_records(rows))
    except ValueError:rejected.append('summary')
    if len(rejected)!=8:raise AssertionError('mutation acceptance: '+str(rejected))
    return rejected

def git_blob(data):
    return hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()

def run(csv_path,summary_path):
    with open(csv_path,newline='',encoding='utf-8') as f:
        reader=csv.DictReader(f)
        if tuple(reader.fieldnames)!=COLUMNS:raise ValueError('CSV header')
        rows=list(reader)
    s=json.loads(Path(summary_path).read_text(encoding='utf-8'))
    sums=check_records(rows)
    check_summary(s,sums)
    rejected=mutations(rows,s)
    print(json.dumps({'status':'PASS_INTERNAL_NONBLIND_E1','atoms':len(rows),
          'losses':{law:[str(sums[law,k]) for k in range(3)] for law in ('H','I')},
          'mutations_rejected':rejected,
          'csv_git_blob':git_blob(Path(csv_path).read_bytes()),
          'json_git_blob':git_blob(Path(summary_path).read_bytes())},indent=2))

if __name__=='__main__':
    p=argparse.ArgumentParser()
    p.add_argument('csv')
    p.add_argument('summary')
    args=p.parse_args()
    run(args.csv,args.summary)
