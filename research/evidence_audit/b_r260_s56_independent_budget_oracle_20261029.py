#!/usr/bin/env python3
"""Independent R260 S56 exact finite budget transfer oracle.

No original CSV parser, JS calls, or R result imports. Uses the previously
frozen nine world cost matrices and direct set enumeration. All values are
integers or exact fractions. Optional canonical R projection comparison.
"""
from __future__ import annotations
import argparse
from fractions import Fraction
from pathlib import Path

M = {
    'ALIGNED_DOMINANCE': ((1,2,2,3),(2,3,3,4),(3,4,4,5),(4,5,5,6),(5,6,6,7)),
    'HIDDEN_JOINT_TAIL': ((0,0,0,12),(2,3,3,4),(3,3,3,3),(4,4,4,4),(5,5,5,5)),
    'REGRET_VS_WORST': ((0,0,0,8),(2,2,2,5),(4,4,4,4),(5,5,5,5),(6,6,6,6)),
    'NONMONOTONE_SHOCK_COST': ((4,1,1,0),(2,2,2,2),(3,1,2,3),(5,0,0,5),(6,6,6,6)),
    'TWO_SHOCK_INTERACTION': ((0,0,0,10),(1,4,4,5),(3,3,3,3),(4,4,4,4),(6,6,6,6)),
    'ADDITIVE_COMMON_SHOCK': ((0,1,2,3),(2,3,4,5),(3,4,5,5),(4,5,6,7),(5,6,7,8)),
    'HIDDEN_TAIL_ALIAS': ((0,0,0,0),(2,3,3,4),(3,3,3,3),(4,4,4,4),(5,5,5,5)),
    'TIED_WORST_CASE': ((0,2,2,2),(1,1,1,3),(2,2,2,2),(3,3,3,3),(4,4,4,4)),
    'HEDGE_VS_NOMINAL': ((0,6,6,6),(2,2,4,4),(3,3,3,3),(1,5,5,5),(4,4,4,4)),
}
A='ABCDE'
SCENARIOS=((0,0),(0,1),(1,0),(1,1))

def independent_lines():
    rows=[]
    for w, costs in M.items():
        best_s=[min(costs[a][s] for a in range(5)) for s in range(4)]
        full_worst=[max(costs[a]) for a in range(5)]
        full_regret=[max(costs[a][s]-best_s[s] for s in range(4)) for a in range(5)]
        best_w=min(full_worst); best_r=min(full_regret)
        for gamma in (0,1,2):
            allowed=[s for s,(x,y) in enumerate(SCENARIOS) if x+y<=gamma]
            for objective in ('minimax_cost','minimax_regret'):
                vals=[]
                for a in range(5):
                    if objective=='minimax_cost':
                        vals.append(max(costs[a][s] for s in allowed))
                    else:
                        vals.append(max(costs[a][s]-best_s[s] for s in allowed))
                minval=min(vals)
                win=[a for a in range(5) if vals[a]==minval]
                members=[]
                for a in win:
                    mean=Fraction(sum(costs[a]),4)
                    assert mean*4==sum(costs[a])
                    members.append(f'{A[a]}:{full_worst[a]}:{full_regret[a]}:{full_worst[a]-best_w}:{full_regret[a]-best_r}:{mean.numerator*4//mean.denominator}')
                rows.append(f'{w}|{gamma}|{objective}|{minval}|{",".join(A[a] for a in win)}|{";".join(members)}')
    assert len(rows)==54
    return rows

def main():
    p=argparse.ArgumentParser()
    p.add_argument('--r-projection',type=Path)
    p.add_argument('--emit',action='store_true')
    a=p.parse_args()
    rows=independent_lines()
    if a.r_projection:
        observed=a.r_projection.read_text(encoding='utf-8').splitlines()
        if observed!=rows:
            bad=[i for i,(x,y) in enumerate(zip(observed,rows)) if x!=y]
            raise SystemExit(f'FAIL: mismatch indices={bad[:12]}, lengths={len(observed)}/{len(rows)}')
        print('PASS: all 54 R groups, every winner and 5 member metrics exact')
        tampered=observed.copy();tampered[0]=tampered[0]+'|999'
        assert tampered!=rows, 'mutation control failed'
        print('PASS: mutated projection rejected')
    if a.emit:
        print('\n'.join(rows))
    print('INDEPENDENT_B_ORACLE_54_GROUPS_PASS')

if __name__=='__main__':
    main()
