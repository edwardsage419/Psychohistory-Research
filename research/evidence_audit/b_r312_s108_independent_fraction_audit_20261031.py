#!/usr/bin/env python3
"""Independent nonblind R312 S108 Fraction midpoint audit. No generator import."""
import argparse
import csv
import io
import json
from collections import Counter
from fractions import Fraction as F
from pathlib import Path
from itertools import combinations

PROFILES = {
    'A': (0,0,0,0), 'B': (0,0,0,F(1,2)),
    'C': (0,0,F(1,2),1), 'D': (0,F(1,2),F(1,2),1),
    'E': (0,0,1,1), 'F': (0,F(1,2),1,1),
    'G': (F(1,2),F(1,2),F(1,2),1), 'H': (1,1,1,1)
}
EPS=(F(0),F(1,2),F(1)); MUS=(F(1,4),F(1,2)); PAIRS=tuple(combinations(range(4),2))
HEADER='world,profile,epsilon,mu,first_i,first_j,second_i,second_j,first_eligible,second_eligible,initial_opinions,after_first,after_second,D0,D1_path,D2_path'

def fmt(x): return str(x)
def vec(x): return ';'.join(map(fmt,x))
def dispersion(x):
    m=sum(x,F(0))/4
    return sum(((z-m)**2 for z in x),F(0))
def midpoint_step(x,eps,mu,p):
    i,j=p
    if abs(x[i]-x[j])>eps: return tuple(x)
    midpoint=(x[i]+x[j])/2
    half_gap=(1-2*mu)*(x[i]-x[j])/2
    y=list(x);y[i]=midpoint+half_gap;y[j]=midpoint-half_gap
    if sum(y)!=sum(x): raise ValueError('conservation failure')
    return tuple(y)

def independent_reconstruction():
    rows=[HEADER]; worlds=[]; changed=0; strict1=0; strict2=0; zero2=0
    min_states=100;max_states=0
    for p,initial in PROFILES.items():
        x=tuple(map(F,initial))
        for eps in EPS:
            for mu in MUS:
                world=f'profile={p}|eps={eps}|mu={mu}'
                one=[midpoint_step(x,eps,mu,pair) for pair in PAIRS]
                d0=dispersion(x)
                ed1=sum((dispersion(v) for v in one),F(0))/6
                ends=[]; ds=[]
                for a,pair1 in enumerate(PAIRS):
                    for pair2 in PAIRS:
                        first=one[a]
                        last=midpoint_step(first,eps,mu,pair2)
                        ends.append(last);ds.append(dispersion(last))
                        cells=[world,p,str(eps),str(mu),str(pair1[0]),str(pair1[1]),str(pair2[0]),str(pair2[1]),str(abs(x[pair1[0]]-x[pair1[1]])<=eps).lower(),str(abs(first[pair2[0]]-first[pair2[1]])<=eps).lower(),vec(x),vec(first),vec(last),str(d0),str(dispersion(first)),str(dispersion(last))]
                        rows.append(','.join(cells))
                ed2=sum(ds,F(0))/36
                if not d0>=ed1>=ed2: raise ValueError('monotonicity failure')
                strict1+=d0>ed1;strict2+=ed1>ed2;zero2+=ed1==ed2
                cnt=sum(midpoint_step(one[a],eps,mu,PAIRS[b])!=midpoint_step(one[b],eps,mu,PAIRS[a]) for a in range(6) for b in range(a+1,6))
                changed+=cnt
                nstates=len(set(ends));min_states=min(min_states,nstates);max_states=max(max_states,nstates)
                worlds.append({'world':world,'D0':str(d0),'E_D1':str(ed1),'E_D2':str(ed2),'distinct_terminal_states':nstates,'order_sensitive_of_15':cnt})
    if len(rows)!=1729 or len(worlds)!=48:raise ValueError('universe mismatch')
    return '\n'.join(rows)+'\n',{'worlds':worlds,'ordered_paths':len(rows)-1,'order_sensitive_contrasts':changed,'strict_reduction_step1_worlds':strict1,'strict_reduction_step2_worlds':strict2,'zero_reduction_step2_worlds':zero2,'distinct_terminal_min':min_states,'distinct_terminal_max':max_states}

def audit(csv_text,expected_csv):
    if not isinstance(csv_text,str) or csv_text!=expected_csv:raise ValueError('complete byte/field identity mismatch')
    records=list(csv.DictReader(io.StringIO(csv_text)))
    if len(records)!=1728:raise ValueError('row count mismatch')
    keys=[(r['world'],r['first_i'],r['first_j'],r['second_i'],r['second_j']) for r in records]
    if len(set(keys))!=1728:raise ValueError('duplicate path')
    counts=Counter(r['world'] for r in records)
    if len(counts)!=48 or set(counts.values())!={36}:raise ValueError('world coverage')
    return True

def mutations(expected):
    lines=expected.splitlines(keepends=True)
    variants=[
        ''.join(lines[:-1]),
        ''.join(lines+[lines[1]]),
        ''.join(lines[:2]+[lines[1]]+lines[3:]),
        expected.replace('profile=B|eps=1/2|mu=1/4','profile=B|eps=0|mu=1/4',1),
        expected.replace('1/8;0;0;3/8','1/4;0;0;1/4',1),
        expected.replace(',true,true,',',false,true,',1),
        expected.replace(',3/16,',',999,',1),
        expected.replace('first_i,first_j','first_j,first_i',1)
    ]
    if any(v==expected for v in variants):raise ValueError('mutation no-op')
    return variants

def main():
    p=argparse.ArgumentParser();p.add_argument('--csv',required=True);p.add_argument('--summary',required=True);p.add_argument('--write-reconstruction');a=p.parse_args()
    expected,stats=independent_reconstruction()
    actual=Path(a.csv).read_text(encoding='utf-8')
    audit(actual,expected)
    summary=json.loads(Path(a.summary).read_text(encoding='utf-8'))
    for k in ('ordered_paths','order_sensitive_contrasts','strict_reduction_step1_worlds','strict_reduction_step2_worlds','zero_reduction_step2_worlds','distinct_terminal_min','distinct_terminal_max'):
        if type(summary.get(k)) is not int or summary[k]!=stats[k]:raise ValueError('summary '+k)
    for row,expected_row in zip(summary['worlds'],stats['worlds'],strict=True):
        for k,v in expected_row.items():
            if row.get(k)!=v:raise ValueError('world summary '+k)
    rejected=0
    for variant in mutations(expected):
        try:audit(variant,expected)
        except ValueError:rejected+=1
    if rejected!=8:raise ValueError('mutation controls failed')
    if a.write_reconstruction:Path(a.write_reconstruction).write_text(expected,encoding='utf-8',newline='')
    print(json.dumps({'status':'PASS','audit_type':'INTERNAL_NONBLIND_E1','paths':1728,'worlds':48,'order_sensitive':stats['order_sensitive_contrasts'],'strict1':stats['strict_reduction_step1_worlds'],'strict2':stats['strict_reduction_step2_worlds'],'mutations_rejected':rejected},sort_keys=True))
if __name__=='__main__':main()
