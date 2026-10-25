"""Independent R155 E1 audit by coefficient matching of the Bass ODE."""
from fractions import Fraction as Q
import json
import sys

P=(Q(0),Q(1,200),Q(1,50),Q(2,25),Q(1,5))
R=(Q(0),Q(1,50),Q(1,10),Q(2,5),Q(4,5))
M=(100,1000,10000)

def serial(x):
    return str(x.numerator) if x.denominator==1 else f"{x.numerator}/{x.denominator}"

def series_jet(p,q,m):
    # F=a1*t+a2*t**2+a3*t**3+O(t**4).
    # Match coefficients in F'=p+(q-p)F-qF**2.
    a1=p
    a2=(q-p)*a1/2
    a3=((q-p)*a2-q*a1*a1)/3
    return (m*a1, 2*m*a2, 6*m*a3)

def audit(expected):
    lookup={r['id']:r for r in expected['rows']}
    checked=0
    mutant_detected=0
    positive=0
    zero=0
    for i,p in enumerate(P):
        for j,q in enumerate(R):
            for k,m in enumerate(M):
                key=f"p{i}_q{j}_m{k}"
                s0,s1,s2=series_jet(p,q,m)
                assert [serial(z) for z in (s0,s1,s2)]==[lookup[key][z] for z in ('S0','S1','S2')]
                if p:
                    positive+=1
                    d=s1/s0
                    h=(d*d-s2/s0)/2
                    assert h==p*q and d==q-p
                    assert p*p+d*p==h and m==s0/p
                else:
                    zero+=1
                    assert s0==s1==s2==0
                if p and q:
                    wrong_s2=m*p*(q-p)**2  # drops the nonlinear term -q*F**2
                    assert wrong_s2!=s2
                    mutant_detected+=1
                checked+=1
    assert (checked,positive,zero,mutant_detected)==(75,60,15,48)
    return {"method":"independent_Taylor_coefficient_matching", "evidence":"E1_INTERNAL_ONLY", "compared_rows":checked,"positive_p_inversions":positive,"zero_p_blocked":zero,"nonlinear_term_deletion_mutants_detected":mutant_detected,"row_mismatches":0,"external_replication":False}

if __name__=='__main__':
    path=sys.argv[1] if len(sys.argv)>1 else 'R155_INITIAL_JET_IDENTIFICATION_EXACT_RECEIPT_2026-10-25.json'
    with open(path,encoding='utf-8') as f: expected=json.load(f)
    print(json.dumps(audit(expected),indent=2,sort_keys=True))
