#!/usr/bin/env python3
"""Independent implementation of Ohtsuki-Iwasa 2004 linear public H-score model.
Exploratory continuation of R135; no modifications to the frozen protocol or results.
"""
import argparse
from functools import lru_cache
import json
from math import sqrt
import time

ME = 0.02
P = tuple(tuple((v >> j)&1 for j in (3,2,1,0)) for v in range(16))
D = tuple(tuple((v >> j)&1 for j in (7,6,5,4,3,2,1,0)) for v in range(256))

def help_prob(a, own, recipient):
    return (a[0]*own*recipient + a[1]*own*(1-recipient)
            +a[2]*(1-own)*recipient +a[3]*(1-own)*(1-recipient))

def transitions(d,p,ma,me=ME):
    z = []
    for k in range(4):
        cooperation,defection=d[2*k],d[2*k+1]
        observed = (1-me)*cooperation+me*defection if p[k] else defection
        z.append(ma+(1-2*ma)*observed)
    return z

def resident_reputation(t, tol_iters=55):
    lo,hi=0.0,1.0
    for _ in range(tol_iters):
        m=(lo+hi)/2
        f=(t[0]*m*m+(t[1]+t[2])*m*(1-m)+t[3]*(1-m)*(1-m))
        if f>m: lo=m
        else: hi=m
    return (lo+hi)/2

def mutant_reputation(tm, hr):
    t_g=tm[0]*hr+tm[1]*(1-hr)
    t_b=tm[2]*hr+tm[3]*(1-hr)
    return t_b/(1-t_g+t_b)

def mirror_pair(d,p):
    return (tuple(1-d[2*(3-i)+c] for i in range(4) for c in range(2)), p[::-1])

def scan_one(ma,b=2,c=1,margin=1e-12,break_when_failed=True):
    n_strict=0
    n_alld=0
    cooperative=[]
    minimum_margin=1e9
    allD_noncoop_wins=0
    maximum_coop_allD_loss= -1e9
    for di,d in enumerate(D):
        for pi,p in enumerate(P):
            tp=transitions(d,p,ma)
            hr=resident_reputation(tp)
            hpr=help_prob(p,hr,hr)
            wr=(b-c)*hpr
            strict=True
            smallest=1e9
            for mi,m in enumerate(P):
                if mi==pi: continue
                tm=transitions(d,m,ma)
                hm=mutant_reputation(tm,hr)
                theta_rm=help_prob(p,hr,hm)
                theta_mr=help_prob(m,hm,hr)
                gap=wr-(b*theta_rm-c*theta_mr)
                if gap<smallest:smallest=gap
                if mi==0 and pi!=0:
                    if gap < -margin: allD_noncoop_wins+=1
                    maximum_coop_allD_loss=max(maximum_coop_allD_loss,-gap)
                if gap <= margin:
                    strict=False
                    if break_when_failed:
                        # Continue all mutant comparisons only for mode all, so stop
                        # after we have seen AllD (mi==0 first) if pi>0.
                        break
            if strict:
                n_strict+=1
                minimum_margin=min(minimum_margin,smallest)
                if pi==0:n_alld+=1
                else:cooperative.append((di,pi,smallest,hr))
    # Mirroring gives exact two-member orbits except for self-mirror members
    coop_idx=set((n,p) for n,p,*_ in cooperative)
    cfix=sum(mirror_pair(D[n],P[p])==(D[n],P[p]) for n,p in coop_idx)
    return {"ma":ma,"b":b,"raw_strict":n_strict,"raw_alld":n_alld,
            "raw_cooperative":len(cooperative),"cooperative_mirror_orbits":(len(cooperative)+cfix)//2,
            "min_positive_margin":minimum_margin,"cooperative":cooperative}

def main():
    import sys
    start=time.time()
    for ma in (.02,.08,.12,.2,.3,.4,.45,.49,.5):
        res=scan_one(ma)
        print(ma,{k:v for k,v in res.items() if k!='cooperative'},'seconds',round(time.time()-start,2),flush=True)
if __name__ == '__main__': main()
