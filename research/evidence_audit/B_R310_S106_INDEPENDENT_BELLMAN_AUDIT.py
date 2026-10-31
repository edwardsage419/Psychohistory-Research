#!/usr/bin/env python3
"""Nonblind, no-import R310 S106 audit. Checks exact Bellman equations and 8 mutants."""
import argparse
import csv
from collections import Counter
from fractions import Fraction as F
from itertools import combinations, product
from pathlib import Path

GRAPH={
 'PATH4': {(0,1),(1,2),(2,3)},
 'CYCLE4': {(0,1),(1,2),(2,3),(0,3)},
 'COMPLETE4': set(combinations(range(4),2)),
}
STATES=[''.join(map(str,x)) for x in product((0,1),repeat=4)]
FIELDS={'graph','bits','p_absorb_ones','expected_steps'}

def check(rows):
    if len(rows)!=48:
        raise ValueError('wrong row count')
    if any(set(x)!=FIELDS for x in rows):
        raise ValueError('wrong fields')
    bykey={}
    for row in rows:
        key=(row['graph'],row['bits'])
        if key in bykey:
            raise ValueError('duplicate world')
        bykey[key]=row
    if set(bykey)!={(g,b) for g in GRAPH for b in STATES}:
        raise ValueError('missing or foreign world')
    for g,edges in GRAPH.items():
        neighbor={i:set() for i in range(4)}
        for u,v in edges:
            neighbor[u].add(v)
            neighbor[v].add(u)
        degree={i:len(neighbor[i]) for i in range(4)}
        for bits in STATES:
            r=bykey[g,bits]
            try:
                q=F(r['p_absorb_ones'])
                t=F(r['expected_steps'])
            except (ValueError,ZeroDivisionError) as exc:
                raise ValueError('bad fraction') from exc
            if not F(0)<=q<=F(1) or t<0:
                raise ValueError('out-of-range q/t')
            expected_weighted=F(sum(int(bits[i])*degree[i] for i in range(4)),sum(degree.values()))
            if q!=expected_weighted:
                raise ValueError('weighted fixation identity')
            if bits in ('0000','1111'):
                if q!=int(bits=='1111') or t!=0:
                    raise ValueError('wrong consensus boundary')
            elif t<=0:
                raise ValueError('nonpositive transient time')
            qnext=F(0)
            tnext=F(0)
            prob=F(0)
            for target in range(4):
                for peer in neighbor[target]:
                    after=list(bits)
                    after[target]=bits[peer]
                    nxt=''.join(after)
                    p=F(1,4*degree[target])
                    qnext+=p*F(bykey[g,nxt]['p_absorb_ones'])
                    tnext+=p*F(bykey[g,nxt]['expected_steps'])
                    prob+=p
            if prob!=1 or q!=qnext:
                raise ValueError('transition or fixation Bellman mismatch')
            if bits not in ('0000','1111') and t!=1+tnext:
                raise ValueError('time Bellman mismatch')
    return {'worlds':48,'transient_equations':42,'mutation_rejections':8,'mode':'NONBLIND_INTERNAL_E1'}

def mutations(rows):
    original=[dict(x) for x in rows]
    tests=[]
    def attempt(fn):
        x=[dict(z) for z in original]
        fn(x)
        try:
            check(x)
        except (ValueError,KeyError):
            tests.append(True)
        else:
            tests.append(False)
    attempt(lambda x:x.append(dict(x[0])))
    attempt(lambda x:x.pop(0))
    attempt(lambda x:x[8].__setitem__('p_absorb_ones','1/3'))
    attempt(lambda x:x[8].__setitem__('expected_steps','7'))
    attempt(lambda x:x[8].__setitem__('graph','STAR4'))
    attempt(lambda x:x[8].__setitem__('bits','2222'))
    attempt(lambda x:x[0].__setitem__('p_absorb_ones','1'))
    attempt(lambda x:x[15].__setitem__('expected_steps','1'))
    if len(tests)!=8 or not all(tests):
        raise ValueError('mutation rejection failure')
    return len(tests)

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('csv_path',type=Path)
    args=parser.parse_args()
    with args.csv_path.open(newline='',encoding='utf-8') as f:
        rows=list(csv.DictReader(f))
    receipt=check(rows)
    receipt['mutations_rejected']=mutations(rows)
    print(receipt)

if __name__=='__main__':
    main()
