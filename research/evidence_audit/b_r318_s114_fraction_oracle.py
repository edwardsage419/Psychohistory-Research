#!/usr/bin/env python3
"""Independent, nonblind exact finite R318 S114 oracle, no R program imports."""
from fractions import Fraction as Q
from itertools import combinations
from collections import Counter

X=(-2,-1,1,2)
PS=(Q(1,4),Q(1,2),Q(3,4))
LOT=[(a,b,p) for a,b in combinations(X,2) for p in PS]

def transform(p,kind):
    if kind=='identity': return p
    return p*p/(p*p+2*(1-p)*(1-p))

def val(z):return z if z>0 else 2*z

def cdf(l,t):
    a,b,p=l
    return (p if a<=t else Q(0))+(1-p if b<=t else Q(0))

def calc(l,k,normalize=False):
    a,b,p=l
    if b<0: weights=(transform(p,k),1-transform(p,k))
    elif a>0: weights=(1-transform(1-p,k),transform(1-p,k))
    else: weights=(transform(p,k),transform(1-p,k))
    result=weights[0]*val(a)+weights[1]*val(b)
    return result/sum(weights) if normalize and a<0<b else result

def sign(z):return (z>0)-(z<0)

def main():
    assert len(LOT)==18
    summary={}
    signs={}
    for k in ('identity','quadratic_asymmetric_noncanonical'):
        d=Counter()
        for i,a in enumerate(LOT):
            for j,b in enumerate(LOT):
                if i==j:continue
                dom=all(cdf(a,t)<=cdf(b,t) for t in X) and any(cdf(a,t)<cdf(b,t) for t in X)
                delta=calc(a,k)-calc(b,k)
                ndelta=calc(a,k,True)-calc(b,k,True)
                d['rows']+=1
                if dom:
                    d['fosd']+=1
                    if delta<=0:d['fosd_bad']+=1
                    if ndelta<=0:d['normalized_fosd_bad']+=1
                if sign(delta)!=sign(ndelta):d['normalized_sign_differences_ordered']+=1
                if i<j:signs[(k,i,j)]=sign(delta)
        summary[k]=dict(d)
    d=Counter()
    for i in range(18):
        for j in range(i+1,18):
            a=signs[('identity',i,j)];b=signs[('quadratic_asymmetric_noncanonical',i,j)]
            if a*b==-1:d['strict_reversals']+=1
            if a==0 or b==0:d['ties_any']+=1
            if a!=b:d['sign_disagreement']+=1
    print(summary)
    print(dict(d))
    assert all(x['rows']==306 for x in summary.values())

if __name__=='__main__':main()
