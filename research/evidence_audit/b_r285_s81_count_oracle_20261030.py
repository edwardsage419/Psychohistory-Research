#!/usr/bin/env python3
"""Independent nonblind count-distribution oracle for R285 S81, Python stdlib only.
No access to original ordered-source enumerator. Prints exact rational metrics.
"""
import json
from fractions import Fraction as F

REGIMES = {'BOTH_NULL': (F(1, 2), F(1, 2)),
           'ONE_SIGNAL': (F(3, 4), F(1, 2))}
COUPLINGS = ('INDEPENDENT', 'COMONOTONE', 'COUNTERMONOTONE')
POLICIES = ('RAW_UNADJUSTED', 'HOLM_FWER', 'BH_FDR')
PV = [F(1), F(15, 16), F(11, 16), F(5, 16), F(1, 16)]

def pair_probabilities(a, b, mode):
    both = {'INDEPENDENT': a*b, 'COMONOTONE': min(a,b),
            'COUNTERMONOTONE': max(F(0),a+b-1)}[mode]
    return {(0,0): 1-a-b+both, (0,1): b-both,
            (1,0): a-both, (1,1): both}

def count_distribution(a,b,mode):
    pairs = pair_probabilities(a,b,mode)
    dist = {(0,0): F(1)}
    for _ in range(4):
        new = {}
        for (i,j),p in dist.items():
            for (u,v),q in pairs.items():
                key = (i+u,j+v)
                new[key] = new.get(key,F(0)) + p*q
        dist = new
    assert len(dist) == 25 and sum(dist.values()) == 1
    from math import comb
    for i in range(5):
        assert sum(p for (k,_),p in dist.items() if k==i) == F(comb(4,i))*a**i*(1-a)**(4-i)
        assert sum(p for (_,k),p in dist.items() if k==i) == F(comb(4,i))*b**i*(1-b)**(4-i)
    return dist

def decisions(k1,k2,policy):
    vals = [PV[k1],PV[k2]]
    order = sorted(range(2), key=lambda i: (vals[i],i))
    mask = [0,0]
    if policy == 'RAW_UNADJUSTED':
        return tuple(int(x <= F(1,2)) for x in vals)
    if policy == 'HOLM_FWER':
        for rank,idx in enumerate(order):
            if vals[idx] <= F(1,2)/(2-rank):
                mask[idx] = 1
            else:
                break
    elif policy == 'BH_FDR':
        top = 0
        for rank,idx in enumerate(order,1):
            if vals[idx] <= F(rank,4):
                top = rank
        for idx in order[:top]: mask[idx] = 1
    else: raise ValueError(policy)
    return tuple(mask)

def run():
    results = []
    for regime,(a,b) in REGIMES.items():
        for mode in COUPLINGS:
            dist = count_distribution(a,b,mode)
            for policy in POLICIES:
                sums = [F(0)]*6
                for (k1,k2),mass in dist.items():
                    m = decisions(k1,k2,policy)
                    r = sum(m)
                    v = (m[0] if a==F(1,2) else 0) + (m[1] if b==F(1,2) else 0)
                    s = r-v
                    obs = (int(v>0), F(v,max(r,1)),v,s,r,int(r==0))
                    sums = [x+mass*y for x,y in zip(sums,obs)]
                assert F(0)<=sums[1]<=sums[0]<=F(1)
                if regime=='BOTH_NULL': assert sums[0]==sums[1]
                results.append(dict(regime=regime,coupling=mode,policy=policy,
                                    FWER=str(sums[0]),FDR=str(sums[1]),
                                    EV=str(sums[2]),ES=str(sums[3]),
                                    ER=str(sums[4]),P_R0=str(sums[5])))
    assert len(results)==18
    return results

if __name__ == '__main__':
    print(json.dumps(run(),indent=2))
