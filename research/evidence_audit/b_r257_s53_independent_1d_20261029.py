#!/usr/bin/env python3
"""Independent 1D active-set oracle for R257 S53; stdlib only."""
from fractions import Fraction as F
import json, sys

WORLD_PARAMS={
 'INTERIOR_OFF_GRID':('1','3/5','1/5'),
 'BINDING_SUM_BOTH':('1','3/4','3/4'),
 'LOWER_X_ACTIVE':('1','-1/2','1/2'),
 'LOWER_Y_ACTIVE':('1','1/2','-1/2'),
 'VERTEX_ORIGIN':('1','-1/2','-1/2'),
 'VERTEX_RIGHT':('1','2','1/4'),
 'VERTEX_UPPER':('1','1/4','2'),
 'CAPACITY_TWO_SLACK':('2','3/4','3/4'),
}

def bound(z, lo, hi): return min(hi,max(lo,z))

def one_dimensional_oracle(C,a,b):
    # Minimize in y for each x. The resulting convex piecewise quadratic
    # changes form at x=C-b and at x=0,C. Check both quadratic vertices.
    candidates={F(0),C,bound(a,F(0),C),bound(C-b,F(0),C),
                bound((C+a-b)/2,F(0),C)}
    vals=[]
    for x in candidates:
        y=bound(b,F(0),C-x)
        vals.append(((x-a)**2+(y-b)**2,x,y))
    v=min(z[0] for z in vals)
    pts={(x,y) for q,x,y in vals if q==v}
    assert len(pts)==1
    return v,next(iter(pts))

def compare(receipt):
    checked=0
    for w in receipt['worlds']:
        C0,a,b=map(F,WORLD_PARAMS[w['world']]);assert str(C0)==w['baseline_capacity']
        for row in w['perturbations']:
            v,p=one_dimensional_oracle(F(row['capacity']),a,b)
            assert v==F(row['minimum'])
            assert [str(z) for z in p]==row['point']
            checked+=1
        v,p=one_dimensional_oracle(C0,a,b)
        assert v==F(w['baseline_minimum'])
        for sec in w['secants']:
            h=F(sec['step']);lv=one_dimensional_oracle(C0-h,a,b)[0]
            rv=one_dimensional_oracle(C0+h,a,b)[0]
            assert (v-lv)/h==F(sec['left_secant'])
            assert (rv-v)/h==F(sec['right_secant'])
            checked+=2
    return checked

if __name__=='__main__':
    data=json.load(open(sys.argv[1],encoding='utf-8'))
    n=compare(data)
    assert n==72
    corrupted=json.loads(json.dumps(data))
    corrupted['worlds'][0]['perturbations'][0]['minimum']='999'
    try:
        compare(corrupted)
        raise AssertionError('corruption undetected')
    except AssertionError as e:
        if str(e)=='corruption undetected':raise
    print(json.dumps({'independent_method':'one_dimensional_piecewise_quadratic',
       'exact_checks_passed':n,'intentional_mutation_rejected':True,
       'external_research_team_replications':0},indent=2))
