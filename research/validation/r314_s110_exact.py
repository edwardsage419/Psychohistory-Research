#!/usr/bin/env python3
"""R314 S110 frozen two-arrival BA versus uniform attachment; E1 only."""
import argparse
import csv
import io
import json
from collections import defaultdict
from fractions import Fraction as F
from pathlib import Path

SEEDS = {
    'P3': ((0,1),(1,2)),
    'K3': ((0,1),(0,2),(1,2)),
    'S4': ((0,1),(0,2),(0,3)),
}
FIELDS = ['seed','first_target','second_target','ba_probability','uniform_probability',
          'final_edges','labeled_degrees','sorted_degrees','maximum_degree','likelihood_ratio']

def deg(edges, n):
    out=[0]*n
    for a,b in edges:
        if not (0<=a<b<n): raise ValueError('edge out of range')
        out[a]+=1;out[b]+=1
    return tuple(out)

def attach(edges,n,target):
    if target not in range(n): raise ValueError('invalid target')
    return tuple(sorted((*edges,(target,n))))

def make_rows():
    rows=[]
    for seed,base in SEEDS.items():
        n=max(max(e) for e in base)+1
        d0=deg(base,n)
        for i in range(n):
            first=attach(base,n,i)
            d1=deg(first,n+1)
            for j in range(n+1):
                last=attach(first,n+1,j)
                d2=deg(last,n+2)
                p=F(d0[i],sum(d0))*F(d1[j],sum(d1))
                q=F(1,n*(n+1))
                rows.append(dict(seed=seed,first_target=i,second_target=j,
                    ba_probability=str(p),uniform_probability=str(q),
                    final_edges=';'.join(f'{a}-{b}' for a,b in last),
                    labeled_degrees=','.join(map(str,d2)),
                    sorted_degrees=','.join(map(str,sorted(d2))),
                    maximum_degree=max(d2),likelihood_ratio=str(p/q)))
    if len(rows)!=44: raise ValueError('path universe incorrect')
    return rows

def summarize(rows):
    ans=[]
    for seed in SEEDS:
        subset=[r for r in rows if r['seed']==seed]
        for name,key in [('O0_path',lambda r:f"{r['first_target']},{r['second_target']}"),
                         ('O1_labeled_degree',lambda r:r['labeled_degrees']),
                         ('O2_sorted_degree',lambda r:r['sorted_degrees']),
                         ('O3_max_degree',lambda r:str(r['maximum_degree']))]:
            dist=defaultdict(lambda:[F(0),F(0)])
            for r in subset:
                a=dist[key(r)]
                a[0]+=F(r['ba_probability']);a[1]+=F(r['uniform_probability'])
            if sum(v[0] for v in dist.values())!=1 or sum(v[1] for v in dist.values())!=1:
                raise ValueError('mass != 1')
            tv=sum((abs(a-b) for a,b in dist.values()),F(0))/2
            ans.append(dict(seed=seed,observation=name,cells=len(dist),tv=str(tv),
                            equal_prior_accuracy=str((1+tv)/2),equal_prior_error=str((1-tv)/2)))
        z=[F(x['tv']) for x in ans[-4:]]
        if not all(z[i]>=z[i+1] for i in range(3)): raise ValueError('data processing violation')
    if len(ans)!=12: raise ValueError('summary length incorrect')
    return {'schema':'r314_s110_ba_vs_uniform_3seeds_2arrivals_4_observations_e1_v1',
            'evidence':'SYNTHETIC_E1_ONLY','source_paths':44,'seed_results':ans,
            'k3_first_target_tv':'0'}

def csv_bytes(rows):
    s=io.StringIO(newline='')
    w=csv.DictWriter(s,fieldnames=FIELDS,lineterminator='\n')
    w.writeheader();w.writerows(rows)
    return s.getvalue().encode()

def json_bytes(summary):
    return (json.dumps(summary,indent=2,ensure_ascii=False)+'\n').encode()

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,required=True)
    args=ap.parse_args();args.out.mkdir(parents=True,exist_ok=True)
    rows=make_rows();summary=summarize(rows)
    (args.out/'R314_S110_ALL_44_PATHS_BA_VS_UNIFORM.csv').write_bytes(csv_bytes(rows))
    (args.out/'R314_S110_12_OBSERVATION_TV_SUMMARY.json').write_bytes(json_bytes(summary))
    print(json.dumps(summary,ensure_ascii=False))

if __name__=='__main__':main()
