#!/usr/bin/env python3
"""MKT130 artificial exact demonstration. Python standard library only."""
from fractions import Fraction as F
from math import comb
import json

N = 8
P = F(1, 20)
TRUTH = F(1)


def binomial_mass(n, k, p):
    if not isinstance(n, int) or isinstance(n, bool) or n < 0:
        raise ValueError('n must be a nonnegative integer')
    if not isinstance(k, int) or isinstance(k, bool) or k < 0 or k > n:
        raise ValueError('invalid k')
    if not isinstance(p, F) or not (F(0) <= p <= F(1)):
        raise ValueError('invalid probability')
    return comb(n, k) * p**k * (1 - p)**(n-k)


def percentile_quantile(n, p, level):
    """Smallest k whose binomial CDF >= level, inclusive quantile."""
    if not isinstance(level, F) or not F(0) < level < F(1):
        raise ValueError('invalid quantile')
    cumulative = F(0)
    for k in range(n+1):
        cumulative += binomial_mass(n, k, p)
        if cumulative >= level:
            return k
    raise AssertionError('probabilities do not sum to one')


def compute():
    rows = []
    coverage = F(0)
    no_rare = (1-P)**N
    direct_mean = crossfit_mean = F(0)
    direct_second = crossfit_second = F(0)
    for k in range(N+1):
        mass = binomial_mass(N,k,P)
        # Unique IDs. Same-row nuisance memorizes Y when A=1; else predicts 0.
        # In-sample DR contribution = A. Held-out nuisance predicts 0;
        # cross-fitted DR contribution = A/P. Both are algebraic counterexamples.
        same_row_dr = F(k,N)
        heldout_dr = F(k,N)/P
        direct_mean += mass*same_row_dr
        crossfit_mean += mass*heldout_dr
        direct_second += mass*same_row_dr**2
        crossfit_second += mass*heldout_dr**2
        # Ordinary nonparametric row bootstrap, conditional on observed k.
        # Each bootstrap draw includes a rare action with probability k/N.
        lo_k = percentile_quantile(N,F(k,N),F(1,40))
        hi_k = percentile_quantile(N,F(k,N),F(39,40))
        lower = F(lo_k,N)/P
        upper = F(hi_k,N)/P
        contains = lower <= TRUTH <= upper
        if contains:
            coverage += mass
        rows.append(dict(k=k,source_mass=str(mass),bootstrap_low=str(lower),
                         bootstrap_high=str(upper),contains_truth=contains))
    assert sum((binomial_mass(N,k,P) for k in range(N+1)),F(0)) == 1
    assert direct_mean == P
    assert crossfit_mean == TRUTH
    assert direct_second-direct_mean**2 == P*(1-P)/N
    assert crossfit_second-crossfit_mean**2 == (1-P)/(N*P)
    assert rows[0]['bootstrap_low']=='0' and rows[0]['bootstrap_high']=='0'
    assert rows[0]['contains_truth'] is False
    assert coverage < F(1,2)
    assert coverage == sum((binomial_mass(N,k,P) for k in (1,2)),F(0))
    for bad in [True, -1, F(1,2)]:
        try:
            binomial_mass(bad,0,P)
        except ValueError:
            pass
        else:
            raise AssertionError('bad n accepted')
    for bad in [F(-1,2),F(3,2),0.5]:
        try:
            binomial_mass(8,0,bad)
        except ValueError:
            pass
        else:
            raise AssertionError('bad probability accepted')
    return dict(research='MKT130',evidence='E1_ARTIFICIAL',n=N,rare_probability=str(P),
                true_target_value=str(TRUTH),same_row_dr_mean=str(direct_mean),
                same_row_dr_variance=str(direct_second-direct_mean**2),
                crossfit_dr_mean=str(crossfit_mean),
                crossfit_dr_variance=str(crossfit_second-crossfit_mean**2),
                probability_no_rare=str(no_rare),
                bootstrap_percentile_nominal='19/20',
                exact_unconditional_bootstrap_coverage=str(coverage),
                by_k=rows,tests='PASS')


if __name__ == '__main__':
    print(json.dumps(compute(),ensure_ascii=False,indent=2))
