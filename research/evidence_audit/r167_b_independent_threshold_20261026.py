"""R167 independent audit. Pure Python Fraction and direct normalized weights.

No calls to the R167 primary solver. Fixed grid copied from the original
2026-10-21 protocol; this is internal algorithmic cross-check, not external replication.
"""
from fractions import Fraction as F
import json

PAIRS = [(F(1,4),F(3,4)), (F(1,3),F(2,3)), (F(1,5),F(4,5)), (F(1,2),F(1,2))]
HIGH = [F(1,2), F(3,4)]
DELTA = [F(-1,4), F(0), F(1,4)]
KAPPA = [0,1,2]

def next_total(a,b,high,delta,kappa):
    """Directly normalize post-reweighting group masses and new local rates."""
    low = 1-high
    q_a = a-delta*a*(1-a)
    q_b = b-delta*b*(1-b)
    low_mass = low*(1+kappa*a)
    high_mass = high*(1+kappa*b)
    after = (low_mass*q_a+high_mass*q_b)/(low_mass+high_mass)
    before = low*a+high*b
    return after-before

def find_threshold(a,b,high,delta):
    """Solve direct normalized inequality without the primary covariance formula."""
    low=1-high
    before=low*a+high*b
    q_a=a-delta*a*(1-a)
    q_b=b-delta*b*(1-b)
    # Difference after-before has numerator intercept+ kappa*slope.
    intercept=low*q_a+high*q_b-before
    slope=low*a*q_a+high*b*q_b-before*(low*a+high*b)
    if slope <= 0:
        return None
    return -intercept/slope

def main():
    records=[]
    boundaries=0
    positive=0
    finite=0
    impossible=0
    sign_checks=0
    controls=0
    for pi,(a,b) in enumerate(PAIRS):
        for wi,high in enumerate(HIGH):
            for di,delta in enumerate(DELTA):
                for ki,kappa in enumerate(KAPPA):
                    ident=f'p{pi}_w{wi}_d{di}_k{ki}'
                    change=next_total(a,b,high,delta,F(kappa))
                    threshold=None
                    if delta>0:
                        sign_checks+=1
                        threshold=find_threshold(a,b,high,delta)
                        if threshold is None:
                            impossible+=1
                            assert change<0,ident
                        else:
                            finite+=1
                            assert (change>0)==(F(kappa)>threshold),ident
                            assert (change==0)==(F(kappa)==threshold),ident
                            for scale,expected in [(threshold/2,-1),(threshold,0),(threshold+1,1)]:
                                actual=next_total(a,b,high,delta,scale)
                                assert (actual>0)-(actual<0)==expected,(ident,scale,actual)
                                boundaries+=1
                    if delta>0 and change>0:
                        positive+=1
                    if kappa==0:
                        assert change==-delta*((1-high)*a*(1-a)+high*b*(1-b))
                        controls+=1
                    if a==b:
                        assert change==-delta*a*(1-a)
                        controls+=1
                    records.append({'id':ident,'net':str(change),'critical_kappa':str(threshold) if threshold is not None else None})
    assert len(records)==72
    assert (sign_checks,finite,impossible,positive,boundaries,controls)==(24,12,12,5,36,42)
    example=[str(next_total(F(1,4),F(3,4),F(1,2),F(1,4),F(k))) for k in [1,F(6,5),2]]
    assert example==['-1/192','0','1/64'],example
    return {'evidence':'INTERNAL_INDEPENDENT_PYTHON_FRACTION','worlds':len(records),
            'delta_positive_worlds':sign_checks,'finite_threshold_worlds':finite,
            'impossible_threshold_worlds':impossible,'positive_reversal_worlds':positive,
            'boundary_tests':boundaries,'controls':controls,'example_nets':example,
            'records':records,'status':'PASS_BOUNDED_E1'}

if __name__=='__main__':
    print(json.dumps(main(),indent=2,ensure_ascii=False))
