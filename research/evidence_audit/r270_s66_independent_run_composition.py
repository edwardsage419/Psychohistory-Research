#!/usr/bin/env python3
"""Independent run-composition route for R270 S66, E1 artificial only."""
import json
from fractions import Fraction as F
from math import comb
from itertools import product
from collections import defaultdict

PRIORS=((1,1),(2,2),(1,3))
THETAS=(F(1,4),F(1,2),F(3,4))
ALPHAS=(F(1,20),F(1,10),F(1,5))

def rising(x,n):
    p=1
    for i in range(n):p*=x+i
    return p

def compositions(n,r):
    if r==0:return int(n==0)
    if n<r or n<=0:return 0
    return comb(n-1,r-1)

def count_k_t(k,t):
    if k in (0,6):return int(t==5)
    r=6-t
    out=0
    for start in (0,1):
        ones=(r+1)//2 if start==1 else r//2
        zeros=r-ones
        out+=compositions(k,ones)*compositions(6-k,zeros)
    return out

def p_lower(prior,obs):
    a,b=prior
    K=sum(obs)
    A=a+K;B=b+6-K
    t=sum(obs[i]==obs[i+1] for i in range(5))
    den=rising(A+B,6)
    return sum((F(count_k_t(k,j)*rising(A,k)*rising(B,6-k),den)
                for k in range(7) for j in range(t+1)),F(0))

def calculate():
    result={}
    for prior in PRIORS:
        ps=[]
        for obs in product((0,1),repeat=6):
            ps.append(p_lower(prior,obs))
        assert len(ps)==64
        for theta in THETAS:
            for alpha in ALPHAS:
                indices=[i for i,p in enumerate(ps) if p<=alpha]
                risk=sum((theta**(i.bit_count())*(1-theta)**(6-i.bit_count()) for i in indices),F(0))
                key=f'{prior[0]},{prior[1]}|{theta}|{alpha}'
                result[key]=(len(indices),str(risk),str(risk-alpha))
    return result

if __name__=='__main__':
    assert sum(count_k_t(k,t) for k in range(7) for t in range(6))==64
    for k in range(7):assert sum(count_k_t(k,t) for t in range(6))==comb(6,k)
    out=calculate()
    assert len(out)==27
    with open('/mnt/data/r270_s66/b_oracle.json','w') as f:json.dump(out,f,indent=2)
    print(json.dumps(out,ensure_ascii=False,indent=2))
