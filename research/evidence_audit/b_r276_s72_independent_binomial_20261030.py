#!/usr/bin/env python3
"""Independent nonblind R276 S72 binomial-count audit; stdlib only."""
from fractions import Fraction as F
from math import comb
from itertools import product
import json
M=('PARAM_A','PARAM_B','PARAM_C')
T=(F(1,2),F(1,4),F(1))

def count_route(m):
    conf=[[F(0) for _ in M] for _ in M]
    for k in range(m+1):
        likelihoods=[t**k*(1-t)**(m-k) for t in T]
        winner=next(i for i,x in enumerate(likelihoods) if x==max(likelihoods))
        for i,t in enumerate(T):
            conf[i][winner]+=comb(m,k)*t**k*(1-t)**(m-k)
    assert all(sum(r)==1 for r in conf)
    return conf

def independent_ordered_route(m):
    conf=[[F(0) for _ in M] for _ in M]
    for seq in product((0,1),repeat=m):
        k=sum(seq)
        like=[t**k*(1-t)**(m-k) for t in T]
        w=next(i for i,x in enumerate(like) if x==max(like))
        for i in range(3): conf[i][w]+=like[i]
    return conf

if __name__=='__main__':
    out=[]
    for m in range(9):
        c=count_route(m)
        assert c==independent_ordered_route(m)
        a=sum(c[i][i] for i in range(3))/3
        out.append({'m':m,'macro_accuracy':str(a),'conditional_accuracy':[str(c[i][i]) for i in range(3)],'confusion':[[str(x) for x in row] for row in c]})
    assert out[0]['macro_accuracy']=='1/3'
    assert out[2]['macro_accuracy']=='11/16'
    print(json.dumps(out,indent=2))
