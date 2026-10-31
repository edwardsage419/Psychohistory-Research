#!/usr/bin/env python3
"""R320 S116 frozen E1 eventual absorption. Python standard library only."""
import json
import sys
from fractions import Fraction as F
from itertools import product
from pathlib import Path

WORLDS = [(4,F(1,4)),(4,F(1,2)),(4,F(3,4)),(6,F(1,4)),(6,F(1,2)),(6,F(3,4))]
T = 6

def f(x): return str(x)

def finite(a,p):
    z=a//2
    cells={(t,s):F(0) for t in range(1,T+1) for s in ('lower','upper')}
    censored=F(0)
    for bits in product((0,1),repeat=T):
        prob=p**sum(bits)*(1-p)**(T-sum(bits))
        x=z
        for t,b in enumerate(bits,1):
            x+=2*b-1
            if x in (0,a):
                cells[t,'upper' if x==a else 'lower']+=prob
                break
        else: censored+=prob
    return cells,censored

def solve(a,p):
    z=a//2
    if p==F(1,2):
        upper=F(z,a)
        expected=F(z*(a-z))
    else:
        r=(1-p)/p
        upper=(1-r**z)/(1-r**a)
        expected=(a*upper-z)/(2*p-1)
    return upper,expected

def generate():
    records=[]
    for i,(a,p) in enumerate(WORLDS):
        cells,survival=finite(a,p)
        u6=sum((cells[t,'upper'] for t in range(1,T+1)),F(0))
        l6=sum((cells[t,'lower'] for t in range(1,T+1)),F(0))
        upper,expected=solve(a,p)
        residual_upper=upper-u6
        residual_lower=(1-upper)-l6
        trunc=sum((t*(cells[t,'upper']+cells[t,'lower']) for t in range(1,T+1)),F(0))+T*survival
        assert upper+(1-upper)==1 and u6+l6+survival==1
        assert residual_upper>=0 and residual_lower>=0
        assert residual_upper+residual_lower==survival
        assert expected>=trunc
        records.append(dict(world_id=i,upper_bound=a,start=a//2,p_up=f(p),
            eventual_upper=f(upper),eventual_lower=f(1-upper),
            expected_eventual_steps=f(expected),six_step_upper=f(u6),
            six_step_lower=f(l6),six_step_survival=f(survival),
            residual_upper=f(residual_upper),residual_lower=f(residual_lower),
            upper_given_survival=f(residual_upper/survival),
            expected_truncated_six_steps=f(trunc),
            six_step_cells=[dict(time=t,lower=f(cells[t,'lower']),upper=f(cells[t,'upper'])) for t in range(1,T+1)]))
    for i,j in ((0,2),(3,5)):
        x,y=records[i],records[j]
        assert x['eventual_upper']==y['eventual_lower']
        assert x['residual_upper']==y['residual_lower']
    return dict(schema='r320_s116_eventual_absorption_e1_v1',
        prescore_freeze_commit='2664cca07f969b0e753f3c70886f9ec623b84f58',
        original_source_path='research/R320/R320_EXACT_6_FIRST_HIT_WORLDS.json',
        original_source_git_blob='ec0f3702f956e0075444d1d3efafef0bced1d7a2',
        original_paths=384,world_count=6,evidence_class='E1_SYNTHETIC_ONLY',
        human_E2=0,historical_E3=0,worlds=records)

if __name__=='__main__':
    result=generate()
    if len(sys.argv)>1 and sys.argv[1]=='--emit':
        Path(sys.argv[2]).write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    elif len(sys.argv)>1 and sys.argv[1]=='--audit':
        assert json.loads(Path(sys.argv[2]).read_text(encoding='utf-8'))==result
        print('R320_S116_PRIMARY_REPLAY_PASS 6_WORLDS')
    else: print(json.dumps(result,indent=2))
