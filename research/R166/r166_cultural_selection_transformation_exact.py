"""R166 synthetic finite cultural selection versus biased transformation.

Original Mesoudi (2021) author R code uses continuous traits and EMG change.
This is an original discrete-two-token Markov identification counterexample.
No original human or archaeological observations are used.
"""
from __future__ import annotations
from fractions import Fraction as F
from functools import lru_cache
from itertools import product
from math import comb
import json

N_GRID=(4,8)
START_K=((0,1,2,4),(0,2,4,8))
REGIMES=(
    ("neutral",1,1,F(0),F(0)),
    ("toward_A",2,1,F(1,3),F(0)),
    ("toward_B",1,2,F(0),F(1,3)),
)
MECHANISMS=("selection","transformation")
HORIZON=4


def checked(n,k,regime,mechanism):
    if type(n) is not int or n not in N_GRID:
        raise ValueError("population must be frozen N=4 or N=8")
    if type(k) is not int or not 0<=k<=n:
        raise ValueError("A count must be an integer between 0 and N")
    if type(regime) is not int or not 0<=regime<len(REGIMES):
        raise ValueError("unknown culture-selection regime")
    if type(mechanism) is not str or mechanism not in MECHANISMS:
        raise ValueError("unknown cultural transmission mechanism")
    return n,k,regime,mechanism


def child_probability(n,k,regime,mechanism):
    n,k,regime,mechanism=checked(n,k,regime,mechanism)
    _,wA,wB,a,b=REGIMES[regime]
    p=F(k,n)
    if mechanism=="selection":
        return F(wA)*p/(F(wA)*p+F(wB)*(1-p))
    return p*(1-b)+(1-p)*a


def child_probability_oracle(n,k,regime,mechanism):
    """Independent channel arithmetic without referencing child_probability."""
    n,k,regime,mechanism=checked(n,k,regime,mechanism)
    _,wa,wb,forward,back=REGIMES[regime]
    if mechanism=="selection":
        # Total chance of weighted-urn A tickets.
        A=F(k*wa)
        B=F((n-k)*wb)
        return A/(A+B)
    # Separate four branches of copying + post-copy A/B transformation.
    previous_A=F(k,n)
    previous_B=F(n-k,n)
    AA=previous_A*(1-back)
    BA=previous_B*forward
    return AA+BA


@lru_cache(maxsize=None)
def kernel(n,regime,mechanism):
    checked(n,0,regime,mechanism)
    out=[]
    for k in range(n+1):
        q=child_probability(n,k,regime,mechanism)
        row=tuple(F(comb(n,j))*q**j*(1-q)**(n-j) for j in range(n+1))
        if sum(row,F(0))!=1:
            raise AssertionError("full transition row lost total probability")
        out.append(row)
    return tuple(out)


@lru_cache(maxsize=None)
def enumerated_kernel(n,regime,mechanism):
    """Enumerate all 2**N next-child configurations and branch probabilities."""
    checked(n,0,regime,mechanism)
    choices=tuple(product((0,1),repeat=n))
    out=[]
    for k in range(n+1):
        # Recompute model-channel q independently from the baseline formula.
        q=child_probability_oracle(n,k,regime,mechanism)
        row=[F(0) for _ in range(n+1)]
        for outcomes in choices:
            ones=sum(outcomes)
            chance=F(1)
            for value in outcomes:
                chance*=q if value else (1-q)
            row[ones]+=chance
        out.append(tuple(row))
    return tuple(out)


def path(n,k,regime,mechanism,t=HORIZON):
    checked(n,k,regime,mechanism)
    if type(t) is not int or t<0:
        raise ValueError("horizon must be nonnegative integer")
    matrix=kernel(n,regime,mechanism)
    state=tuple(F(int(j==k)) for j in range(n+1))
    result=[state]
    for _ in range(t):
        state=tuple(sum((state[i]*matrix[i][j] for i in range(n+1)),F(0))
                    for j in range(n+1))
        result.append(state)
    return tuple(result)


def independent_path(n,k,regime,mechanism,t=HORIZON):
    checked(n,k,regime,mechanism)
    if type(t) is not int or t<0:
        raise ValueError("horizon must be nonnegative integer")
    matrix=enumerated_kernel(n,regime,mechanism)
    state=[F(int(i==k)) for i in range(n+1)]
    result=[tuple(state)]
    for _ in range(t):
        new=[F(0)]*(n+1)
        for former in range(n+1):
            for later in range(n+1):
                new[later]+=state[former]*matrix[former][later]
        result.append(tuple(new))
        state=new
    return tuple(result)


def mean_frequency(distribution,n):
    if len(distribution)!=n+1 or sum(distribution,F(0))!=1:
        raise ValueError("probability distribution has wrong size or sum")
    return sum((F(j,n)*distribution[j] for j in range(n+1)),F(0))


def total_variation(a,b):
    if len(a)!=len(b):
        raise ValueError("TV distributions dimensions differ")
    if sum(a,F(0))!=1 or sum(b,F(0))!=1:
        raise ValueError("TV probabilities not normalized")
    return sum((abs(x-y) for x,y in zip(a,b)),F(0))/2


def result_document():
    matrices=[]
    for n in N_GRID:
        for ri in range(len(REGIMES)):
            for mechanism in MECHANISMS:
                a=kernel(n,ri,mechanism)
                b=enumerated_kernel(n,ri,mechanism)
                if a!=b: raise AssertionError("independent full kernel mismatch")
                matrices.append({
                    "N":n,"regime":REGIMES[ri][0],"mechanism":mechanism,
                    "rows":[[str(v) for v in row] for row in a]})
    worlds=[]
    for ni,n in enumerate(N_GRID):
        for ki,k in enumerate(START_K[ni]):
            for ri in range(len(REGIMES)):
                for mi,mechanism in enumerate(MECHANISMS):
                    a=path(n,k,ri,mechanism)
                    b=independent_path(n,k,ri,mechanism)
                    if a!=b: raise AssertionError("independent full path mismatch")
                    worlds.append({
                        "id":f"n{ni}_k{ki}_r{ri}_m{mi}",
                        "N":n,"starting_A_count":k,
                        "regime":REGIMES[ri][0],
                        "mechanism":mechanism,
                        "independent_exact_oracles_equal":True,
                        "points":[{"t":t,"count_probabilities":[str(z) for z in state],
                                   "expected_A_fraction":str(mean_frequency(state,n))}
                                  for t,state in enumerate(a)]
                    })
    if len(worlds)!=48 or len({x["id"] for x in worlds})!=48:
        raise AssertionError("frozen 48-case identities not met")
    ss=path(4,2,1,"selection")
    tt=path(4,2,1,"transformation")
    ssB=path(4,2,2,"selection")
    ttB=path(4,2,2,"transformation")
    tv=total_variation(ss[2],tt[2])
    if ss[1]!=tt[1] or ssB[1]!=ttB[1] or tv==0:
        raise AssertionError("prespecified identification boundary failed")
    return {
        "research_id":"R166",
        "evidence":"E1_PROJECT_BINARY_SELECTION_VS_DIRECTED_TRANSFORMATION",
        "original_Mesoudi_2021_EMG_model_reproduced":False,
        "R019_is_not_selection_theory":True,
        "original_human_cultural_data_used":False,
        "number_of_worlds":48,
        "timepoints_per_world":5,
        "total_kernel_count":12,
        "kernels":matrices,
        "worlds":worlds,
        "counterexamples":{
            "p_half_A_favored_both_one_step_q":"2/3",
            "p_half_B_favored_both_one_step_q":"1/3",
            "p_quarter_A_selection_one_step_q":str(child_probability(4,1,1,"selection")),
            "p_quarter_A_transformation_one_step_q":str(child_probability(4,1,1,"transformation")),
            "p_zero_A_selection_q":str(child_probability(4,0,1,"selection")),
            "p_zero_A_transformation_q":str(child_probability(4,0,1,"transformation")),
            "N4_half_A_t1_complete_kernel_equal":ss[1]==tt[1],
            "N4_half_A_t2_total_variation":str(tv),
            "N4_half_A_t2_selection_mean":str(mean_frequency(ss[2],4)),
            "N4_half_A_t2_transformation_mean":str(mean_frequency(tt[2],4)),
            "neutral_sel_and_trans_equal":all(
                kernel(n,0,"selection")==kernel(n,0,"transformation")
                for n in N_GRID),
        }
    }


def main():
    print(json.dumps(result_document(),sort_keys=True,indent=2,ensure_ascii=False))


if __name__=="__main__":
    main()
