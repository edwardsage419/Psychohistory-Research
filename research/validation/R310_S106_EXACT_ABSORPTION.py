#!/usr/bin/env python3
"""R310 S106: exact finite voter consensus probability and absorption time.
Frozen before scoring at commit 2d44da5a1d40582674cdf11cdb05233b13794476.
Standard library only; no external data or billed computation.
"""
import argparse
import csv
import io
from collections import defaultdict
from fractions import Fraction as Q
from itertools import combinations, product
from pathlib import Path

EDGES = {
    'PATH4': ((0,1),(1,2),(2,3)),
    'CYCLE4': ((0,1),(1,2),(2,3),(0,3)),
    'COMPLETE4': tuple(combinations(range(4),2)),
}
STATES = tuple(product((0,1), repeat=4))
COLUMNS = ('graph','bits','p_absorb_ones','expected_steps')


def solve_exact(matrix, rhs):
    """Fraction Gauss Jordan elimination with explicit singularity failure."""
    n = len(rhs)
    a = [list(matrix[i]) + [rhs[i]] for i in range(n)]
    for k in range(n):
        pivot = next((i for i in range(k,n) if a[i][k]), None)
        if pivot is None:
            raise ArithmeticError('singular transient system')
        a[k],a[pivot] = a[pivot],a[k]
        d = a[k][k]
        a[k] = [z/d for z in a[k]]
        for i in range(n):
            if i == k:
                continue
            c = a[i][k]
            if c:
                a[i] = [x-c*y for x,y in zip(a[i],a[k])]
    return [a[i][-1] for i in range(n)]


def exact_results():
    records=[]
    for graph, edges in EDGES.items():
        nbr=[[] for _ in range(4)]
        for a,b in edges:
            nbr[a].append(b)
            nbr[b].append(a)
        deg=tuple(len(x) for x in nbr)
        p=[]
        for bits in STATES:
            row=defaultdict(Q)
            for i in range(4):
                for j in nbr[i]:
                    nxt=list(bits)
                    nxt[i]=bits[j]
                    row[tuple(nxt)]+=Q(1,4*deg[i])
            p.append(tuple(row[s] for s in STATES))
        transient=tuple(range(1,15))
        matrix=[[Q(int(i==j))-p[i][j] for j in transient] for i in transient]
        q=[Q(0)]+solve_exact(matrix,[p[i][15] for i in transient])+[Q(1)]
        t=[Q(0)]+solve_exact(matrix,[Q(1) for _ in transient])+[Q(0)]
        for i,bits in enumerate(STATES):
            if sum(p[i]) != 1:
                raise AssertionError('transition normalization')
            weighted=Q(sum(x*d for x,d in zip(bits,deg)),sum(deg))
            if q[i] != weighted or not Q(0)<=q[i]<=Q(1):
                raise AssertionError('fixation probability')
            if t[i]<0 or (i in transient and t[i]==0):
                raise AssertionError('absorption time')
            if q[i] != sum((p[i][j]*q[j] for j in range(16)),Q(0)):
                raise AssertionError('fixation recurrence')
            expected=Q(0) if i in (0,15) else Q(1)+sum((p[i][j]*t[j] for j in range(16)),Q(0))
            if t[i]!=expected:
                raise AssertionError('time recurrence')
            records.append(dict(graph=graph,bits=''.join(map(str,bits)),
                                p_absorb_ones=str(q[i]),expected_steps=str(t[i])))
    if len(records)!=48:
        raise AssertionError('world universe')
    return records


def as_csv(records):
    f=io.StringIO(newline='')
    w=csv.DictWriter(f,fieldnames=COLUMNS,lineterminator='\n')
    w.writeheader()
    w.writerows(records)
    return f.getvalue()


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--emit',action='store_true')
    parser.add_argument('--check',type=Path)
    args=parser.parse_args()
    data=as_csv(exact_results())
    if args.check:
        if args.check.read_bytes()!=data.encode('utf-8'):
            raise SystemExit('FAIL: archived results mismatch')
        print('PASS: 48 worlds, exact q/t and full archived CSV identity')
    elif args.emit:
        print(data,end='')
    else:
        print('PASS: 48 worlds, 42 transient states, exact recurrences')


if __name__=='__main__':
    main()
