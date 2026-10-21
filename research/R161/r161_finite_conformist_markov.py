"""R161 finite-population cultural conformity as a synthetic exact Markov chain.

Finite isolated groups N=5/7 only. Labels A/B are arbitrary, not actual people.
Binomial kernel versus full 2**N indicator enumeration are independent oracles.
"""
from __future__ import annotations

import json
import math
from fractions import Fraction as F
from itertools import product

POPULATIONS=(5,7)
INITIAL_STATES=((0,1,2,3,4,5),(0,1,2,5,6,7))
CONFORMITY=(F(0),F(1,4),F(1,2),F(1))
HORIZON=4


def unit(x, name):
    if isinstance(x,bool) or not isinstance(x,(int,F)):
        raise ValueError(f"{name} should be exact int or Fraction")
    v=F(x)
    if not 0<=v<=1:
        raise ValueError(f"{name} must be in unit interval")
    return v


def checked_n(n):
    if isinstance(n,bool) or not isinstance(n,int) or n not in POPULATIONS:
        raise ValueError("population size must be one of frozen 5,7")
    return n


def checked_k(n,k):
    n=checked_n(n)
    if isinstance(k,bool) or not isinstance(k,int) or not 0<=k<=n:
        raise ValueError("initial group count outside range")
    return k


def copying_target(n,k,h):
    n=checked_n(n); k=checked_k(n,k); h=unit(h,"conformity strength")
    p=F(k,n)
    majority=3*p*p-2*p*p*p
    return (1-h)*p+h*majority


def binomial_kernel(n,h):
    n=checked_n(n);h=unit(h,"conformity strength")
    rows=[]
    for k in range(n+1):
        q=copying_target(n,k,h)
        row=tuple(F(math.comb(n,j))*q**j*(1-q)**(n-j) for j in range(n+1))
        if sum(row,F(0))!=1:
            raise AssertionError("binomial transition row not normalized")
        rows.append(row)
    return tuple(rows)


def binary_enumerated_kernel(n,h):
    """Independent explicit enumeration, no call to binomial_kernel."""
    n=checked_n(n);h=unit(h,"conformity strength")
    rows=[]
    for k in range(n+1):
        prevalence=F(k,n)
        q=(1-h)*prevalence+h*(prevalence**3 + 3*prevalence**2*(1-prevalence))
        values=[F(0) for _ in range(n+1)]
        for outcome in product((0,1),repeat=n):
            positives=sum(outcome)
            values[positives]+=q**positives*(1-q)**(n-positives)
        rows.append(tuple(values))
    return tuple(rows)


def distribution_path_formula(n,k,h,horizon=HORIZON):
    n=checked_n(n);k=checked_k(n,k);h=unit(h,"conformity strength")
    if isinstance(horizon,bool) or not isinstance(horizon,int) or horizon<0:
        raise ValueError("negative or invalid horizon")
    kernel=binomial_kernel(n,h)
    distribution=tuple(F(int(j==k)) for j in range(n+1))
    out=[distribution]
    for _ in range(horizon):
        distribution=tuple(sum((distribution[i]*kernel[i][j] for i in range(n+1)),F(0))
                           for j in range(n+1))
        out.append(distribution)
    return tuple(out)


def distribution_path_enumerated(n,k,h,horizon=HORIZON):
    n=checked_n(n);k=checked_k(n,k);h=unit(h,"conformity strength")
    if isinstance(horizon,bool) or not isinstance(horizon,int) or horizon<0:
        raise ValueError("negative or invalid horizon")
    transition=binary_enumerated_kernel(n,h)
    current=[F(int(state==k)) for state in range(n+1)]
    distributions=[tuple(current)]
    for _ in range(horizon):
        updated=[F(0) for _ in range(n+1)]
        for from_state in range(n+1):
            for to_state in range(n+1):
                updated[to_state]+=current[from_state]*transition[from_state][to_state]
        distributions.append(tuple(updated))
        current=updated
    return tuple(distributions)


def fixation_probabilities(n,h):
    """Pure-Fraction Gaussian elimination for all-A absorption probabilities."""
    n=checked_n(n);h=unit(h,"conformity strength")
    P=binomial_kernel(n,h)
    m=n-1
    system=[[F(int(i==j))-P[i+1][j+1] for j in range(m)]+[P[i+1][n]]
            for i in range(m)]
    for pivot in range(m):
        nonzero=next((i for i in range(pivot,m) if system[i][pivot]!=0),None)
        if nonzero is None:
            raise ValueError("noninvertible absorbing transient matrix")
        system[pivot],system[nonzero]=system[nonzero],system[pivot]
        factor=system[pivot][pivot]
        system[pivot]=[x/factor for x in system[pivot]]
        for i in range(m):
            if i!=pivot:
                weight=system[i][pivot]
                if weight:
                    system[i]=[x-weight*y for x,y in zip(system[i],system[pivot])]
    result=(F(0),)+tuple(system[i][-1] for i in range(m))+(F(1),)
    if any(not 0<=x<=1 for x in result):
        raise AssertionError("invalid absorption probability")
    if any(result[k]!=sum((P[k][j]*result[j] for j in range(n+1)),F(0))
           for k in range(1,n)):
        raise AssertionError("harmonic exact residual nonzero")
    return result


def expected_frequency(distribution,n):
    if len(distribution)!=n+1:
        raise ValueError("distribution has wrong dimension")
    if sum(distribution,F(0))!=1:
        raise ValueError("distribution not normalized")
    return sum((F(j,n)*distribution[j] for j in range(n+1)),F(0))


def results_document():
    worlds=[]
    kernels={}
    fixation={}
    for n in POPULATIONS:
        for hi,h in enumerate(CONFORMITY):
            a=binomial_kernel(n,h)
            b=binary_enumerated_kernel(n,h)
            if a!=b:
                raise AssertionError("independent enumerated kernel mismatch")
            fx=fixation_probabilities(n,h)
            kernels[(n,hi)]=a
            fixation[(n,hi)]=fx
            if h==0 and fx!=tuple(F(i,n) for i in range(n+1)):
                raise AssertionError("neutral fixation must be k/N")
    for ni,n in enumerate(POPULATIONS):
        for ki,k in enumerate(INITIAL_STATES[ni]):
            for hi,h in enumerate(CONFORMITY):
                a=distribution_path_formula(n,k,h)
                b=distribution_path_enumerated(n,k,h)
                if a!=b:
                    raise AssertionError("independent full distribution paths differ")
                worlds.append({
                    "id":f"n{ni}_k{ki}_h{hi}",
                    "N":n,"initial_A_count":k,"h":str(h),
                    "two_independent_paths_equal":True,
                    "ultimate_all_A_fixation_probability":str(fixation[(n,hi)][k]),
                    "probability_distributions":[
                        {"t":t,"state_k_probabilities":[str(x) for x in row],
                         "expected_A_fraction":str(expected_frequency(row,n))}
                        for t,row in enumerate(a)]
                })
    if len(worlds)!=48 or len({w['id'] for w in worlds})!=48:
        raise AssertionError("frozen experiment case mismatch")
    n=5;h=F(1)
    first=distribution_path_formula(n,2,h)
    p=F(2,5)
    deterministic_second=(1-h)*copying_target(n,2,h)+h*(3*copying_target(n,2,h)**2-2*copying_target(n,2,h)**3)
    second_expected=expected_frequency(first[2],n)
    return {
        "research_id":"R161",
        "evidence":"E1_SYNTHETIC_FINITE_POPULATION_MARKOV_ONLY",
        "author_original_models_reproduced":False,
        "original_behavioral_data_used":False,
        "group_causal_prediction_claimed":False,
        "number_of_frozen_worlds":48,
        "periods_per_world":5,
        "worlds":worlds,
        "kernel_receipts":[
            {"N":n,"h":str(h),
             "kernel_rows":[[str(x) for x in row] for row in kernels[(n,hi)]],
             "all_A_fixation_by_initial_count":[str(x) for x in fixation[(n,hi)]]}
            for n in POPULATIONS for hi,h in enumerate(CONFORMITY)],
        "counterexamples":{
            "N5_h1_k2_first_expected":str(copying_target(5,2,1)),
            "N5_h1_k3_first_expected":str(copying_target(5,3,1)),
            "N5_h1_k1_fixation":str(fixation[(5,3)][1]),
            "N5_h1_k4_fixation":str(fixation[(5,3)][4]),
            "N5_h1_k2_second_expected":str(second_expected),
            "N5_h1_k2_second_deterministic_iterate":str(deterministic_second),
            "finite_stochastic_vs_infinite_deterministic_t2_difference":str(second_expected-deterministic_second)
        }
    }


def main():
    print(json.dumps(results_document(),sort_keys=True,indent=2,ensure_ascii=False))


if __name__=="__main__":
    main()
