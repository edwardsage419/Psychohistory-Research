#!/usr/bin/env python3
"""Independent nonblind exact oracle for R314 S110, no R code imports."""
import argparse
import csv
import json
from collections import defaultdict
from copy import deepcopy
from fractions import Fraction as Q
from pathlib import Path

SEED_DEGREES={'P3':(1,2,1),'K3':(2,2,2),'S4':(3,1,1,1)}
SEED_EDGES={'P3':((0,1),(1,2)),'K3':((0,1),(0,2),(1,2)),'S4':((0,1),(0,2),(0,3))}
OBS=('O0_path','O1_labeled_degree','O2_sorted_degree','O3_max_degree')
KEYS=('seed','first_target','second_target','ba_probability','uniform_probability','final_edges','labeled_degrees','sorted_degrees','maximum_degree','likelihood_ratio')

def expected():
    answer={}
    for name,d in SEED_DEGREES.items():
        n=len(d); D=sum(d)
        for i in range(n):
            for j in range(n+1):
                ds=list(d)+[1,1]
                ds[i]+=1
                ds[j]+=1
                edges=tuple(sorted(SEED_EDGES[name]+((i,n),(j,n+1))))
                second_degree=(d[j]+int(j==i)) if j<n else 1
                ba=Q(d[i],D)*Q(second_degree,D+2)
                uniform=Q(1,n*(n+1))
                answer[(name,i,j)]={
                    'seed':name,'first_target':str(i),'second_target':str(j),
                    'ba_probability':str(ba),'uniform_probability':str(uniform),
                    'final_edges':';'.join(f'{a}-{b}' for a,b in edges),
                    'labeled_degrees':','.join(map(str,ds)),
                    'sorted_degrees':','.join(map(str,sorted(ds))),
                    'maximum_degree':str(max(ds)),'likelihood_ratio':str(ba/uniform)}
    if len(answer)!=44: raise RuntimeError('oracle universe mismatch')
    return answer

def observation(row,kind):
    if kind=='O0_path':return row['first_target']+','+row['second_target']
    if kind=='O1_labeled_degree':return row['labeled_degrees']
    if kind=='O2_sorted_degree':return row['sorted_degrees']
    if kind=='O3_max_degree':return row['maximum_degree']
    raise ValueError('bad observation')

def oracle_summary(rows):
    z=[]
    for name in SEED_DEGREES:
        for kind in OBS:
            cells=defaultdict(lambda:[Q(0),Q(0)])
            for row in rows:
                if row['seed']!=name:continue
                pair=cells[observation(row,kind)]
                pair[0]+=Q(row['ba_probability']);pair[1]+=Q(row['uniform_probability'])
            if sum(x[0] for x in cells.values())!=1 or sum(x[1] for x in cells.values())!=1:
                raise ValueError('mass check')
            tv=sum((abs(x[0]-x[1]) for x in cells.values()),Q(0))/2
            z.append({'seed':name,'observation':kind,'cells':len(cells),'tv':str(tv),
                      'equal_prior_accuracy':str((1+tv)/2),'equal_prior_error':str((1-tv)/2)})
    return z

def validate(rows, summary):
    if summary.get('evidence')!='SYNTHETIC_E1_ONLY':raise ValueError('grade escalation')
    if summary.get('source_paths')!=44:raise ValueError('count declaration')
    if summary.get('schema')!='r314_s110_ba_vs_uniform_3seeds_2arrivals_4_observations_e1_v1':raise ValueError('schema')
    if summary.get('k3_first_target_tv')!='0':raise ValueError('negative control')
    if len(rows)!=44:raise ValueError('missing or extra path')
    model=expected(); seen=set()
    for r in rows:
        if set(r)!=set(KEYS):raise ValueError('column identity')
        try:key=(r['seed'],int(r['first_target']),int(r['second_target']))
        except Exception as e:raise ValueError('bad path key') from e
        if key in seen:raise ValueError('duplicate path')
        seen.add(key)
        if key not in model or r!=model[key]:raise ValueError('path or probability differs from oracle')
    if seen!=set(model):raise ValueError('path universe')
    if summary.get('seed_results')!=oracle_summary(rows):raise ValueError('observation TV summary mismatch')
    return True

def mutations(rows,summary):
    tests=[]
    def reject(name,mutator):
        r=deepcopy(rows);s=deepcopy(summary);mutator(r,s)
        try:validate(r,s)
        except (ValueError,KeyError,TypeError,ZeroDivisionError):tests.append((name,'REJECTED'));return
        raise RuntimeError('MUTATION ACCEPTED: '+name)
    reject('duplicate_path',lambda r,s:r.__setitem__(1,deepcopy(r[0])))
    reject('missing_path',lambda r,s:r.pop())
    reject('ba_probability',lambda r,s:r[0].__setitem__('ba_probability','1/99'))
    reject('uniform_probability',lambda r,s:r[0].__setitem__('uniform_probability','1/99'))
    reject('labeled_degrees',lambda r,s:r[0].__setitem__('labeled_degrees','0,0,0'))
    reject('coarsened_observation',lambda r,s:r[0].__setitem__('sorted_degrees','1,1'))
    reject('tv_summary',lambda r,s:s['seed_results'][0].__setitem__('tv','0'))
    reject('evidence_grade',lambda r,s:s.__setitem__('evidence','REAL_HUMAN_E2'))
    return tests

def main():
    p=argparse.ArgumentParser();p.add_argument('--csv',type=Path,required=True);p.add_argument('--json',type=Path,required=True)
    p.add_argument('--mutations',action='store_true');a=p.parse_args()
    with a.csv.open(newline='',encoding='utf-8') as h: rows=list(csv.DictReader(h))
    summary=json.loads(a.json.read_text(encoding='utf-8'))
    validate(rows,summary)
    print('PASS exact nonimporting oracle 44 paths and 12 observation summaries')
    if a.mutations:
        for name,status in mutations(rows,summary):print(name,status)

if __name__=='__main__':main()
