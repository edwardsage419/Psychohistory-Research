"""R165 finite synthetic cultural drift with exact Fraction, no real people/data."""
from fractions import Fraction as F
from itertools import product
from functools import lru_cache
from math import comb
import json

NS=(4,6,8)
STARTS=((0,1,2,4),(0,1,3,6),(0,1,4,8))
MUS=(F(0),F(1,16),F(1,8),F(1,4))
HORIZON=4

def validate(n,k,mu):
    if type(n) is not int or n not in NS: raise ValueError("invalid N")
    if type(k) is not int or not 0<=k<=n: raise ValueError("invalid k")
    if type(mu) is bool or not isinstance(mu,(int,F)) or F(mu) not in MUS:
        raise ValueError("invalid innovation")
    return n,k,F(mu)

def prob(n,k,mu):
    n,k,mu=validate(n,k,mu)
    return (1-mu)*F(k,n)+mu/2

@lru_cache(None)
def kernel(n,mu):
    n,_,mu=validate(n,0,mu)
    return tuple(tuple(F(comb(n,j))*prob(n,k,mu)**j*
        (1-prob(n,k,mu))**(n-j) for j in range(n+1))
        for k in range(n+1))

@lru_cache(None)
def enumerate_kernel(n,mu):
    n,_,mu=validate(n,0,mu)
    rows=[]
    for k in range(n+1):
        q=(1-mu)*F(k,n)+mu/2
        row=[F(0)]*(n+1)
        for bits in product((0,1),repeat=n):
            j=sum(bits)
            row[j]+=q**j*(1-q)**(n-j)
        rows.append(tuple(row))
    return tuple(rows)

def path_binomial(n,k,mu,t=HORIZON):
    n,k,mu=validate(n,k,mu)
    if type(t) is not int or t<0: raise ValueError("invalid horizon")
    P=kernel(n,mu)
    a=tuple(F(int(i==k)) for i in range(n+1))
    result=[a]
    for _ in range(t):
        a=tuple(sum((a[i]*P[i][j] for i in range(n+1)),F(0))
                for j in range(n+1))
        result.append(a)
    return tuple(result)

def path_enumerated(n,k,mu,t=HORIZON):
    n,k,mu=validate(n,k,mu)
    if type(t) is not int or t<0: raise ValueError("invalid horizon")
    P=enumerate_kernel(n,mu)
    a=[F(int(i==k)) for i in range(n+1)]
    result=[tuple(a)]
    for _ in range(t):
        b=[F(0)]*(n+1)
        for i in range(n+1):
            for j in range(n+1): b[j]+=a[i]*P[i][j]
        a=b
        result.append(tuple(a))
    return tuple(result)

def solve(A,y):
    n=len(A)
    if len(y)!=n or any(len(row)!=n for row in A):
        raise ValueError("non-square equation system")
    a=[[F(x) for x in A[i]]+[F(y[i])] for i in range(n)]
    for j in range(n):
        k=next((i for i in range(j,n) if a[i][j]),None)
        if k is None: raise ValueError("singular system")
        a[j],a[k]=a[k],a[j]
        pivot=a[j][j]
        a[j]=[x/pivot for x in a[j]]
        for i in range(n):
            if i!=j:
                f=a[i][j]
                if f: a[i]=[x-f*z for x,z in zip(a[i],a[j])]
    return tuple(a[i][-1] for i in range(n))

@lru_cache(None)
def absorption(n):
    n,_,_=validate(n,0,0)
    P=kernel(n,F(0))
    A=[[F(int(i==j))-P[i+1][j+1] for j in range(n-1)]
       for i in range(n-1)]
    t=(F(0),)+solve(A,[F(1)]*(n-1))+(F(0),)
    assert all(t[i]==1+sum((P[i][j]*t[j] for j in range(n+1)),F(0))
               for i in range(1,n))
    return t

@lru_cache(None)
def stationary(n,mu):
    n,_,mu=validate(n,0,mu)
    if mu==0: raise ValueError("nonunique stationary distribution")
    P=kernel(n,mu)
    A=[[P[i][j]-F(int(i==j)) for i in range(n+1)] for j in range(n)]
    pi=solve(A+[[F(1)]*(n+1)],[F(0)]*n+[F(1)])
    assert sum(pi)==1 and all(x>0 for x in pi)
    assert all(pi[j]==sum((pi[i]*P[i][j] for i in range(n+1)),F(0))
               for j in range(n+1))
    return pi

def mean(dist,n):
    if len(dist)!=n+1 or sum(dist)!=1: raise ValueError("bad distribution")
    return sum((F(i,n)*dist[i] for i in range(n+1)),F(0))

def heterogeneity(dist,n):
    if len(dist)!=n+1 or sum(dist)!=1: raise ValueError("bad distribution")
    return sum((F(2*i,n)*(1-F(i,n))*dist[i] for i in range(n+1)),F(0))

def mean_formula(n,k,mu,t):
    n,k,mu=validate(n,k,mu)
    if type(t) is not int or t<0: raise ValueError("bad time")
    return F(1,2)+(1-mu)**t*(F(k,n)-F(1,2))

def document():
    kernels=[]
    for n in NS:
        for mu in MUS:
            P=kernel(n,mu)
            if P!=enumerate_kernel(n,mu): raise AssertionError("kernel disagreement")
            pi=stationary(n,mu) if mu>0 else None
            tau=absorption(n) if mu==0 else None
            kernels.append({"N":n,"mu":str(mu),
                "rows":[[str(v) for v in row] for row in P],
                "stationary":None if pi is None else [str(v) for v in pi],
                "absorption_time":None if tau is None else [str(v) for v in tau]})
    worlds=[]
    for ni,n in enumerate(NS):
        for ki,k in enumerate(STARTS[ni]):
            for mi,mu in enumerate(MUS):
                a=path_binomial(n,k,mu)
                b=path_enumerated(n,k,mu)
                if a!=b: raise AssertionError("exact trajectory disagreement")
                h0=2*F(k,n)*(1-F(k,n))
                points=[]
                for t,dist in enumerate(a):
                    assert sum(dist)==1 and all(v>=0 for v in dist)
                    E=mean(dist,n);H=heterogeneity(dist,n)
                    assert E==mean_formula(n,k,mu,t)
                    if mu==0: assert H==h0*(1-F(1,n))**t
                    points.append({"t":t,"counts":[str(x) for x in dist],
                                   "mean":str(E),"heterogeneity":str(H)})
                worlds.append({"id":f"n{ni}_k{ki}_m{mi}","N":n,"k0":k,
                    "mu":str(mu),"oracles_equal":True,
                    "absorption_time":None if mu>0 else str(absorption(n)[k]),
                    "points":points})
    assert len(worlds)==48 and len({x["id"] for x in worlds})==48
    return {"research_id":"R165",
        "evidence":"E1_SYNTHETIC_TWO_TOKEN_FINITE_NEUTRAL_DRIFT",
        "original_multi_allele_model_reproduced":False,
        "empirical_name_pottery_patent_data_used":False,
        "historical_predictions_made":False,
        "world_count":48,"timepoints":5,"kernels":kernels,"worlds":worlds,
        "controls":{"N4_half_one_step_variance":"1/16",
                    "N8_half_one_step_variance":"1/32",
                    "N4_half_absorption_time":str(absorption(4)[2]),
                    "N8_half_absorption_time":str(absorption(8)[4]),
                    "positive_innovation_stationary_mean_half":all(
                      mean(stationary(n,mu),n)==F(1,2) for n in NS for mu in MUS[1:])}}

if __name__=="__main__":
    print(json.dumps(document(),indent=2,sort_keys=True,ensure_ascii=False))
