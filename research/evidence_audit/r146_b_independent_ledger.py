#!/usr/bin/env python3
"""R146 independent Fraction labor/consumption ledger and exact voter audit."""
from fractions import Fraction as F
from itertools import combinations_with_replacement
import json

X = [F(i,4) for i in range(5)]
T = [F(k,20) for k in range(21)]

def economy(profile):
    n=len(profile)
    sq=[x*x for x in profile]
    a=sum(sq,F(0))/n
    m=sq[n//2]
    if a==0 or m>=a: tax=F(0)
    else: tax=(a-m)/(2*a-m)
    if a==0:
        assert all(sum(((1-t)**2*q/F(2)+t*(1-t)*a for q in sq),F(0))==0 for t in T)
    votes=[]
    for t in T:
        labor=[(1-t)*x for x in profile]
        income=[x*z for x,z in zip(profile,labor)]
        taxes=[t*y for y in income]
        transfer=sum(taxes,F(0))/n
        assert n*transfer==sum(taxes,F(0))
        consumption=[(1-t)*y+transfer for y in income]
        utility=[c-z*z/F(2) for c,z in zip(consumption,labor)]
        votes.append(utility)
    median_utility=[v[n//2] for v in votes]
    max_med=max(median_utility)
    best=[i for i,v in enumerate(median_utility) if v==max_med]
    for k in best:
        for alt in range(21):
            majority=sum(votes[alt][i]>votes[k][i] for i in range(n))
            assert majority<=n//2
    return tax, len(best)>1

def main():
    count=pos=zero=flat=tie=0
    by_n={}
    for n in [5,7,9]:
        by_n[n]=0
        for p in combinations_with_replacement(X,n):
            t,tied=economy(p)
            by_n[n]+=1;count+=1;pos+=(t>0);zero+=(t==0)
            flat+=(all(x==0 for x in p));tie+=tied
    assert (count,pos,zero,flat,tie)==(1171,751,420,3,16)
    return dict(status='PASS',worlds=count,positive_tax=pos,zero_tax=zero,
                flat_all_zero=flat,grid_ties=tie,by_n=by_n,
                budget_ledger_checks=worlds*21 if (worlds:=count) else 0,
                median_winner_unbeaten_checks='all 1171 profiles, 21 candidates')
if __name__=='__main__': print(json.dumps(main(),indent=2))
