"""R168 synthetic cultural-skill frontier under copying and innovation.

No original Derex experimental rows or author evolutionary equations are used.
The group records the highest of m independent anonymous skill attempts; this
is an E1 counterexample to equating group maximum with individual learning.
"""
from __future__ import annotations
from fractions import Fraction as F
from functools import lru_cache
import json

GROUP_SIZES=(2,4,8,16)
FIDELITIES=(F(1,2),F(3,4))
INNOVATIONS=(F(0),F(1,8))
MODES=("full_pool","single_channel")
INITIAL_LEVELS=(0,2)
HORIZON=4


def checked(n,f,u,mode,level=0):
    if type(n) is not int or n not in GROUP_SIZES:
        raise ValueError("N must be a frozen population size")
    if isinstance(f,bool) or not isinstance(f,(F,int)) or F(f) not in FIDELITIES:
        raise ValueError("individual fidelity outside frozen grid")
    if isinstance(u,bool) or not isinstance(u,(F,int)) or F(u) not in INNOVATIONS:
        raise ValueError("innovation probability outside frozen grid")
    if type(mode) is not str or mode not in MODES:
        raise ValueError("invalid effective cultural sample access")
    if type(level) is not int or level not in (0,1,2):
        raise ValueError("invalid cultural frontier level")
    return n,F(f),F(u),mode,level


def individual_distribution(level,f,u):
    if type(level) is not int or level not in (0,1,2):
        raise ValueError("invalid starting shared-skill frontier")
    if isinstance(f,bool) or not isinstance(f,(int,F)) or F(f) not in FIDELITIES:
        raise ValueError("invalid fidelity")
    if isinstance(u,bool) or not isinstance(u,(int,F)) or F(u) not in INNOVATIONS:
        raise ValueError("invalid innovation")
    f=F(f);u=F(u)
    if level==0: return (1-u,u,F(0))
    if level==1: return ((1-u)*(1-f),(1-u)*f,u)
    return (F(0),1-f,f)


def independent_child_distribution(level,f,u):
    """Separate branching oracle, independent of individual_distribution."""
    if type(level) is not int or level not in (0,1,2):
        raise ValueError("bad level")
    if isinstance(f,bool) or not isinstance(f,(F,int)) or F(f) not in FIDELITIES:
        raise ValueError("bad f")
    if isinstance(u,bool) or not isinstance(u,(F,int)) or F(u) not in INNOVATIONS:
        raise ValueError("bad u")
    f=F(f);u=F(u)
    outcomes=[F(0),F(0),F(0)]
    if level==0:
        outcomes[0]+=F(1)-u
        outcomes[1]+=u
    elif level==1:
        outcomes[0]+= (F(1)-u)*(F(1)-f)
        outcomes[1]+= (F(1)-u)*f
        outcomes[2]+=u
    else:
        outcomes[1]+= F(1)-f
        outcomes[2]+=f
    return tuple(outcomes)


@lru_cache(None)
def cumulative_kernel(n,f,u,mode):
    n,f,u,mode,_=checked(n,f,u,mode)
    draws=n if mode=="full_pool" else 1
    rows=[]
    for level in (0,1,2):
        a,b,c=individual_distribution(level,f,u)
        low=a**draws
        mid=(a+b)**draws-low
        top=F(1)-(a+b)**draws
        row=(low,mid,top)
        if sum(row,F(0))!=1 or any(x<0 for x in row):
            raise AssertionError("invalid cumulative-maximum probability")
        rows.append(row)
    return tuple(rows)


@lru_cache(None)
def max_dynamic_program_kernel(n,f,u,mode):
    """Independent sequential maximum DP, no powered CDF formula used."""
    n,f,u,mode,_=checked(n,f,u,mode)
    draws=n if mode=="full_pool" else 1
    rows=[]
    for level in (0,1,2):
        child=independent_child_distribution(level,f,u)
        distribution=[F(1),F(0),F(0)]
        for _ in range(draws):
            after=[F(0),F(0),F(0)]
            for old,old_probability in enumerate(distribution):
                for new,new_probability in enumerate(child):
                    after[max(old,new)]+=old_probability*new_probability
            distribution=after
        rows.append(tuple(distribution))
    return tuple(rows)


def analytic_path(n,f,u,mode,start,horizon=HORIZON):
    n,f,u,mode,start=checked(n,f,u,mode,start)
    if type(horizon) is not int or horizon<0:
        raise ValueError("horizon must be nonnegative integer")
    M=cumulative_kernel(n,f,u,mode)
    current=tuple(F(int(i==start)) for i in range(3))
    path=[current]
    for _ in range(horizon):
        current=tuple(sum((current[i]*M[i][j] for i in range(3)),F(0))
                      for j in range(3))
        path.append(current)
    return tuple(path)


def independent_path(n,f,u,mode,start,horizon=HORIZON):
    n,f,u,mode,start=checked(n,f,u,mode,start)
    if type(horizon) is not int or horizon<0:
        raise ValueError("horizon must be nonnegative integer")
    M=max_dynamic_program_kernel(n,f,u,mode)
    current=[F(int(i==start)) for i in range(3)]
    out=[tuple(current)]
    for _ in range(horizon):
        next_state=[F(0),F(0),F(0)]
        for old in range(3):
            for new in range(3):
                next_state[new]+=current[old]*M[old][new]
        current=next_state
        out.append(tuple(current))
    return tuple(out)


def linear_fraction(A,b):
    if len(A)!=len(b) or any(len(row)!=len(b) for row in A):
        raise ValueError("malformed square system")
    n=len(b)
    c=[[F(x) for x in A[i]]+[F(b[i])] for i in range(n)]
    for j in range(n):
        pivot=next((i for i in range(j,n) if c[i][j]),None)
        if pivot is None:raise ValueError("singular probability balance")
        c[j],c[pivot]=c[pivot],c[j]
        d=c[j][j]
        c[j]=[z/d for z in c[j]]
        for i in range(n):
            if i==j:continue
            t=c[i][j]
            if t:c[i]=[a-t*b for a,b in zip(c[i],c[j])]
    return tuple(c[i][-1] for i in range(n))


@lru_cache(None)
def stationary(n,f,u,mode):
    n,f,u,mode,_=checked(n,f,u,mode)
    if u==0:raise ValueError("zero innovation has absorbing zero frontier")
    M=cumulative_kernel(n,f,u,mode)
    A=[[M[i][j]-F(int(i==j)) for i in range(3)] for j in range(2)]
    pi=linear_fraction(A+[[F(1)]*3],[F(0),F(0),F(1)])
    if sum(pi,F(0))!=1 or any(v<=0 for v in pi):
        raise AssertionError("unexpected stationary support")
    for j in range(3):
        if pi[j]!=sum((pi[i]*M[i][j] for i in range(3)),F(0)):
            raise AssertionError("nonzero stationarity residual")
    return pi


def mean_frontier(state):
    if len(state)!=3 or sum(state,F(0))!=1 or any(x<0 for x in state):
        raise ValueError("not a valid probability vector")
    return state[1]+2*state[2]


def expected_loss_time(n,f,u,mode,start):
    n,f,u,mode,start=checked(n,f,u,mode,start)
    if u!=0:raise ValueError("no absorbing-zero hit-time formula under innovation")
    effective=n if mode=="full_pool" else 1
    return F(start)/(F(1)-f)**effective


def document():
    matrices=[]
    for n in GROUP_SIZES:
        for f in FIDELITIES:
            for u in INNOVATIONS:
                for mode in MODES:
                    a=cumulative_kernel(n,f,u,mode)
                    b=max_dynamic_program_kernel(n,f,u,mode)
                    if a!=b:raise AssertionError("exact CDF and dynamic oracles differ")
                    eq=None if u==0 else stationary(n,f,u,mode)
                    matrices.append({"N":n,"f":str(f),"u":str(u),"mode":mode,
                         "kernel":[[str(x) for x in row] for row in a],
                         "stationary":None if eq is None else [str(x) for x in eq]})
    worlds=[]
    for ni,n in enumerate(GROUP_SIZES):
        for fi,f in enumerate(FIDELITIES):
            for ui,u in enumerate(INNOVATIONS):
                for mi,mode in enumerate(MODES):
                    for li,start in enumerate(INITIAL_LEVELS):
                        a=analytic_path(n,f,u,mode,start)
                        b=independent_path(n,f,u,mode,start)
                        if a!=b:raise AssertionError("independent complete path differs")
                        worlds.append({
                          "id":f"n{ni}_f{fi}_u{ui}_m{mi}_l{li}",
                          "N":n,"f":str(f),"u":str(u),"access_mode":mode,
                          "initial_frontier":start,
                          "exact_independent_paths_equal":True,
                          "mean_loss_time_to_zero_if_u0":None if u>0 else str(expected_loss_time(n,f,u,mode,start)),
                          "points":[{"t":t,"frontier_0_1_2_probabilities":[str(z) for z in p],
                                     "expected_group_max_skill_level":str(mean_frontier(p))}
                                     for t,p in enumerate(a)]})
    if len(worlds)!=64 or len(set(w["id"] for w in worlds))!=64:
        raise AssertionError("frozen 64-world grid identities mismatch")
    same=analytic_path(2,F(1,2),0,"full_pool",2)[1][2]
    alt=analytic_path(16,F(3,4),0,"single_channel",2)[1][2]
    if same!=F(3,4) or alt!=same:raise AssertionError("group-level confound failed")
    return {
      "research_id":"R168",
      "evidence":"E1_SYNTHETIC_GROUP_MAXIMUM_ONLY",
      "source_nature2013_original_XLS_acquired":False,
      "derex2015_original_XLSX_acquired":False,
      "external_real_human_rows_scored":0,
      "original_author_model_reproduced":False,
      "2014_criticism_resolved":False,
      "world_count":64,"timepoints_per_world":5,
      "kernel_count":32,"kernels":matrices,"worlds":worlds,
      "predeclared_controls":{
         "N2_full_pool_fhalf_top_retention":str(same),
         "N16_single_channel_fthreequarters_top_retention":str(alt),
         "N16_full_pool_fhalf_top_retention":str(analytic_path(16,F(1,2),0,"full_pool",2)[1][2]),
         "N2_full_pool_fhalf_top_retention":str(analytic_path(2,F(1,2),0,"full_pool",2)[1][2]),
         "zero_innovation_no_spontaneous_recovery":all(
             analytic_path(n,f,0,mode,0)==((F(1),F(0),F(0)),)*5
             for n in GROUP_SIZES for f in FIDELITIES for mode in MODES),
         "one_generation_cannot_jump_from_zero_to_level_two":all(
             analytic_path(n,f,F(1,8),mode,0)[1][2]==0
             for n in GROUP_SIZES for f in FIDELITIES for mode in MODES),
         "two_generations_allow_level_two_after_innovation":all(
             analytic_path(n,f,F(1,8),mode,0)[2][2]>0
             for n in GROUP_SIZES for f in FIDELITIES for mode in MODES),
         "full_pool_fhalf_level2_absorption_N2":str(expected_loss_time(2,F(1,2),0,"full_pool",2)),
         "full_pool_fhalf_level2_absorption_N16":str(expected_loss_time(16,F(1,2),0,"full_pool",2)),
         "single_channel_any_N_identical":all(
             cumulative_kernel(n,F(1,2),F(1,8),"single_channel")==
             cumulative_kernel(2,F(1,2),F(1,8),"single_channel") for n in GROUP_SIZES),
      }
    }


if __name__=="__main__":
    print(json.dumps(document(),sort_keys=True,indent=2,ensure_ascii=False))
