#!/usr/bin/env python3
"""R135 exploratory mathematical certificate for AllD invasion above a*=2401/8502.
Uses exclusively Python Fraction for the finite parameter covering certificate.
It adds a bounded R135 scientific result; no historical frozen artefact is rewritten.
"""
from fractions import Fraction as F
from itertools import product
from hashlib import sha256
from math import sqrt
import json
import time
from pathlib import Path

A0=F(2401,8502)
B=2
ME=F(1,50)
RESIDENTS=[tuple((v>>shift)&1 for shift in (3,2,1,0)) for v in range(16)]
NORMS=[tuple((v>>shift)&1 for shift in (7,6,5,4,3,2,1,0)) for v in range(256)]
EXCEPTIONS={(152,10),(154,10),(184,10),(186,10),(81,5),(89,5),(209,5),(217,5)}
N_INTERVALS=48
BISECTION=10
LIPSCHITZ_A=F(19)
LIPSCHITZ_H=F(6)


def source_t(norm,strat,ma):
    factor=1-2*ma
    out=[]
    for j,act in enumerate(strat):
        c,d=norm[2*j],norm[2*j+1]
        expected = (1-ME)*c+ME*d if act else F(d)
        out.append(ma+factor*expected)
    return tuple(out)


def hr_bracket(t,steps=BISECTION):
    lo,hi=F(0),F(1)
    for _ in range(steps):
        x=(lo+hi)/2
        y=t[0]*x*x+(t[1]+t[2])*x*(1-x)+t[3]*(1-x)*(1-x)
        if y>x:
            lo=x
        else:
            hi=x
    return lo,hi


def help_prob(p,own,opp):
    return (p[0]*own*opp+p[1]*own*(1-opp)
            +p[2]*(1-own)*opp+p[3]*(1-own)*(1-opp))


def allD_resident_margin(norm, p, a, x, tm=None):
    if tm is None:tm=source_t(norm,RESIDENTS[0],a)
    tg=tm[0]*x+tm[1]*(1-x)
    tb=tm[2]*x+tm[3]*(1-x)
    hm=tb/(1-tg+tb)
    return help_prob(p,x,x)-2*help_prob(p,x,hm)


def main():
    start=time.monotonic()
    interval=(F(1,2)-A0)/N_INTERVALS
    halfwidth=interval/2
    huncert=LIPSCHITZ_H/F(2**(BISECTION+1))
    auncert=LIPSCHITZ_A*halfwidth
    max_upper=None
    max_mid=None
    max_where=None
    entries=0
    for k in range(N_INTERVALS):
        a=A0+(k*2+1)*interval/2
        for norm_i,norm in enumerate(NORMS):
            tm=source_t(norm,RESIDENTS[0],a)
            for pi in range(1,16):
                if (norm_i,pi) in EXCEPTIONS: continue
                p=RESIDENTS[pi]
                t=source_t(norm,p,a)
                lo,hi=hr_bracket(t)
                x=(lo+hi)/2
                gap=allD_resident_margin(norm,p,a,x,tm)
                upper=gap+huncert+auncert
                entries+=1
                if max_upper is None or upper>max_upper:
                    max_upper=upper;max_mid=gap;max_where=(k,norm_i,pi)
        if (k+1)%12==0:
            print('interval',k+1,'of',N_INTERVALS,'best upper bound',float(max_upper),'runtime',round(time.monotonic()-start,2),flush=True)
    if max_upper is None or max_upper>=0:
        raise RuntimeError(('Global interval certification failed',max_upper,max_where))
    result={
      'project':'R135 postfreeze AllD invasion interval certificate',
      'evidence':'math E1; not a new human/animal source or a change to prior frozen score',
      'first_party_equations':'Ohtsuki Iwasa (2004) JTB 231:107-120 Eq 3-10',
      'parameters':{'b':2,'c':1,'execution_error':'1/50','assignment_error_range':['2401/8502','1/2']},
      'mathematical_competing_inequality':'Gap = resident-intended payoff - AllD-intended payoff = theta(p,h,h)-2*theta(p,h,h_m)',
      'exceptional_equality_pairs':sorted([{'norm':n,'resident_strategy':p} for n,p in EXCEPTIONS],key=lambda d:(d['norm'],d['resident_strategy'])),
      'exceptional_algebraic_resultant':'a*(2*a-1)^2*(8502*a-2401)/1250',
      'candidate_exact_threshold':'2401/8502',
      'input_complete_norm_count':256,
      'input_cooperative_strategy_count':15,
      'sampled_intervals':N_INTERVALS,
      'nonexception_pairs_per_interval':256*15-len(EXCEPTIONS),
      'exact_fraction_evaluations':entries,
      'resident_root_bracket_bisections':BISECTION,
      'x_root_enclosure_max_halfwidth':str(F(1,2**(BISECTION+1))),
      'uniform_abs_derivative_in_a_bound':str(LIPSCHITZ_A),
      'uniform_abs_derivative_in_h_bound':str(LIPSCHITZ_H),
      'uniform_parameter_halfwidth':str(halfwidth),
      'a_midpoint_extension_error_bound':str(auncert),
      'h_bracket_error_bound':str(huncert),
      'maximum_certified_upper_resident_margin':str(max_upper),
      'maximum_certified_upper_resident_margin_approx':float(max_upper),
      'maximum_raw_midpoint_margin':str(max_mid),
      'maximum_upper_location':{'interval':max_where[0], 'norm':max_where[1], 'strategy':max_where[2]},
      'all_remaining_cooperative_residents_are_beaten_by_AllD_on_interval':max_upper<0,
      'note':'Eight exceptional pairs require the separate symbolic-resultant argument and endpoint evaluation; this finite certificate excludes them.'
    }
    print(json.dumps(result,indent=2),flush=True)
    with Path(__file__).with_name('R135_THRESHOLD_INTERVAL_CERTIFICATE_20261113.json').open('w') as f:
        json.dump(result,f,indent=2)

if __name__=='__main__':main()
