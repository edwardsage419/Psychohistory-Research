#!/usr/bin/env python3
"""R322 S118 independent exact oracle. Does not import R scorer or source generator."""
from collections import defaultdict
from fractions import Fraction as F
from itertools import product
import json

OBS=("behavior_full","behavior_partial","behavior_only","label_only","label_full")
STRATA=("all","r0","r1","gate_all")
EPS=(F(0),F(1,4),F(1,2))

def universe(policy):
    for h,a,y,d,r,w in product((0,1),repeat=6):
        if policy=="gated_intervention":
            active=int(h!=a and d==1 and r==1 and w==1)
            out=a if active else h
            label=active
        elif policy=="lookup_equivalent":
            out=h^((h^a)&d&r&w)
            label=0
        else:
            raise ValueError(policy)
        yield (h,a,y,d,r,w,out,label)

def select(t,s):
    h,a,y,d,r,w,out,label=t
    return s=="all" or (s=="r0" and r==0) or (s=="r1" and r==1) or (s=="gate_all" and d==r==w==1)

def observed(t,o,label):
    h,a,y,d,r,w,out,_=t
    if o=="behavior_full": return (h,a,d,r,w,out)
    if o=="behavior_partial": return (h,a,out)
    if o=="behavior_only": return (out,)
    if o=="label_only": return (out,label)
    if o=="label_full": return (h,a,d,r,w,out,label)
    raise ValueError(o)

def distribution(policy,o,eps,s):
    rows=[t for t in universe(policy) if select(t,s)]
    m=defaultdict(F)
    for t in rows:
        if o.startswith("behavior_"):
            m[observed(t,o,None)]+=F(1,len(rows))
        else:
            label=t[-1]
            m[observed(t,o,label)]+=(1-eps)/len(rows)
            m[observed(t,o,1-label)]+=eps/len(rows)
    if sum(m.values())!=1: raise ValueError("mass")
    return m

def compute():
    cells=[]
    for s in STRATA:
        for eps in EPS:
            for o in OBS:
                a=distribution("gated_intervention",o,eps,s)
                b=distribution("lookup_equivalent",o,eps,s)
                tv=sum((abs(a.get(k,0)-b.get(k,0)) for k in a.keys()|b.keys()),F(0))/2
                cells.append(dict(stratum=s,noise_flip=str(eps),observation=o,total_variation=str(tv),bayes_accuracy=str((1+tv)/2),support_gated=sum(bool(v) for v in a.values()),support_lookup=sum(bool(v) for v in b.values())))
    assert len(cells)==60
    assert all(c["total_variation"]=="0" for c in cells if c["observation"].startswith("behavior_") or c["stratum"]=="r0" or c["noise_flip"]=="1/2")
    return cells

if __name__=="__main__":
    print(json.dumps({"schema":"R322_S118_INDEPENDENT_ORACLE_v1","cells":compute()},indent=2))
