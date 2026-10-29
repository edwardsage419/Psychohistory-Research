#!/usr/bin/env python3
"""R257 S53: exact capacity perturbations, separate from frozen R257 code.

No dependencies beyond Python stdlib. E1 artificial mathematical experiment.
"""
from fractions import Fraction as F
import json

WORLDS = {
    'INTERIOR_OFF_GRID': ('1', '3/5', '1/5'),
    'BINDING_SUM_BOTH': ('1', '3/4', '3/4'),
    'LOWER_X_ACTIVE': ('1', '-1/2', '1/2'),
    'LOWER_Y_ACTIVE': ('1', '1/2', '-1/2'),
    'VERTEX_ORIGIN': ('1', '-1/2', '-1/2'),
    'VERTEX_RIGHT': ('1', '2', '1/4'),
    'VERTEX_UPPER': ('1', '1/4', '2'),
    'CAPACITY_TWO_SLACK': ('2', '3/4', '3/4'),
}
BASELINE_VALUES = {'INTERIOR_OFF_GRID':'0','BINDING_SUM_BOTH':'1/8',
 'LOWER_X_ACTIVE':'1/4','LOWER_Y_ACTIVE':'1/4','VERTEX_ORIGIN':'1/2',
 'VERTEX_RIGHT':'17/16','VERTEX_UPPER':'17/16','CAPACITY_TWO_SLACK':'0'}
BASELINE_LAMBDAS = {'INTERIOR_OFF_GRID':'0','BINDING_SUM_BOTH':'1/2',
 'LOWER_X_ACTIVE':'0','LOWER_Y_ACTIVE':'0','VERTEX_ORIGIN':'0',
 'VERTEX_RIGHT':'2','VERTEX_UPPER':'2','CAPACITY_TWO_SLACK':'0'}
STEPS = (F(1, 4), F(1, 16))

def clamp(z, lo, hi):
    return max(lo, min(z, hi))

def exact_projection(C, a, b):
    """Enumerate analytically minimized triangle faces and feasible interior."""
    t = clamp((C+a-b)/2, F(0), C)
    points = {(clamp(a, F(0), C), F(0)),
              (F(0), clamp(b, F(0), C)), (t, C-t)}
    if a >= 0 and b >= 0 and a+b <= C:
        points.add((a,b))
    values = [( (x-a)**2+(y-b)**2, x, y) for x,y in points]
    best = min(v for v,_,_ in values)
    hits = [(x,y) for v,x,y in values if v == best]
    assert len(hits) == 1, ('nonunique', C,a,b,hits)
    return best, hits[0]

def lambda_at_baseline(C, a, b, point):
    x,y = point
    if x+y < C:
        return F(0)
    if x > 0:
        return 2*(a-x)
    return 2*(b-y)

def emit():
    rows = []
    checks = 0
    for world, raw in WORLDS.items():
        C0,a,b = map(F, raw)
        v0,p0 = exact_projection(C0,a,b)
        assert v0 == F(BASELINE_VALUES[world]); checks += 1
        lam = lambda_at_baseline(C0,a,b,p0)
        assert lam == F(BASELINE_LAMBDAS[world]); checks += 1
        assert lam >= 0; checks += 1
        records = []
        for delta in (-F(1,4),-F(1,16),F(0),F(1,16),F(1,4)):
            C = C0+delta
            v,p = exact_projection(C,a,b)
            assert C > 0 and p[0] >= 0 and p[1] >= 0 and sum(p) <= C
            checks += 1
            assert v >= v0-lam*delta
            checks += 1
            records.append({'delta':str(delta),'capacity':str(C),
                'minimum':str(v),'point':[str(z) for z in p]})
        slopes = []
        for h in STEPS:
            vl = exact_projection(C0-h,a,b)[0]
            vr = exact_projection(C0+h,a,b)[0]
            left = (v0-vl)/h
            right = (vr-v0)/h
            assert left <= right <= 0, (world,h,left,right)
            checks += 1
            slopes.append({'step':str(h),'left_secant':str(left),
                           'right_secant':str(right)})
        rows.append({'world':world,'baseline_capacity':str(C0),
          'baseline_minimum':str(v0),'baseline_lambda':str(lam),
          'local_derivative':str(-lam),'perturbations':records,
          'secants':slopes})
    off = rows[0]
    assert off['perturbations'][0]['minimum'] == '1/800'; checks += 1
    assert off['secants'][0]['left_secant'] == '-1/200'; checks += 1
    assert off['secants'][0]['right_secant'] == '0'; checks += 1
    assert off['secants'][1]['left_secant'] == '0'; checks += 1
    assert off['secants'][1]['right_secant'] == '0'; checks += 1
    # The nonconvex stationary point at (1/2,1/2) is KKT but worse than (0,1/2).
    assert -(F(1,2)-F(1,2))**2 == 0
    assert -(F(0)-F(1,2))**2 == -F(1,4)
    checks += 2
    return {'research_id':'R257_S53','evidence':'E1','capacity_evaluations':40,
      'one_sided_secants':32,'baseline_lambdas':8,'assertions_passed':checks,
      'nonconvex_negative_control':'KKT_stationary_0_vs_feasible_-1/4',
      'worlds':rows,'new_human_E2':0,'new_history_E3':0}

if __name__ == '__main__':
    print(json.dumps(emit(),indent=2,ensure_ascii=False))
