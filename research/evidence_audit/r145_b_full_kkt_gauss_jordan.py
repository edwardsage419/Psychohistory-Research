#!/usr/bin/env python3
"""R145 independent full KKT linear-system recomputation, Python standard library."""
from fractions import Fraction as F
import itertools
import json

MODELS = {
    'base': (['3/4','1/4'], ['1/4','3/4']),
    'redundant': (['3/8','3/8','1/8','1/8'], ['1/8','1/8','3/8','3/8']),
    'informative': (['1/2','1/4','1/16','3/16'], ['1/16','3/16','1/4','1/2']),
}
COSTS = ['0','1/8','1/4','3/8']

def solve_linear(matrix, rhs):
    """Independent row-pivot Gauss Jordan solver over exact rational numbers."""
    n = len(rhs)
    a = [[F(x) for x in row] + [F(y)] for row, y in zip(matrix, rhs)]
    for j in range(n):
        pivot = next((i for i in range(j, n) if a[i][j] != 0), None)
        if pivot is None:
            raise ValueError('singular KKT matrix')
        a[j], a[pivot] = a[pivot], a[j]
        scale = a[j][j]
        a[j] = [x / scale for x in a[j]]
        for i in range(n):
            if i != j:
                scale = a[i][j]
                a[i] = [x - scale*y for x,y in zip(a[i],a[j])]
    return [row[-1] for row in a]

def audit(model, effort_cost, perm=None):
    h0,l0 = MODELS[model]
    if perm is None:
        perm = range(len(h0))
    h = [F(h0[i]) for i in perm]
    l = [F(l0[i]) for i in perm]
    d = [x-y for x,y in zip(h,l)]
    c = F(effort_cost)
    b0 = F(1,2) + c
    n = len(h)
    matrix = []
    rhs = []
    for i in range(n):
        row = [F(0)]*(n+2)
        row[i] = 2*h[i]
        row[n] = -h[i]
        row[n+1] = -d[i]
        matrix.append(row)
        rhs.append(F(0))
    matrix.extend([h+[F(0),F(0)],d+[F(0),F(0)]])
    rhs.extend([b0,c])
    solution = solve_linear(matrix,rhs)
    v = solution[:n]
    lam,mu = solution[n:]
    assert min(v) >= 0 and lam >= 0 and mu >= 0
    assert sum((x*y for x,y in zip(h,v)),F(0)) == b0
    assert sum((x*y for x,y in zip(d,v)),F(0)) == c
    assert all(2*h[i]*v[i] == lam*h[i]+mu*d[i] for i in range(n))
    cost = sum((h[i]*v[i]**2 for i in range(n)),F(0))
    return {'model':model,'c':effort_cost,'v':list(map(str,v)),'cost':str(cost),
            'lambda':str(lam),'mu':str(mu)}

def main():
    rows = [audit(m,c) for m in MODELS for c in COSTS]
    expected = {('base','1/4'):'39/64',('redundant','1/4'):'39/64',
                ('informative','1/4'):'5505/9104'}
    assert all(next(r['cost'] for r in rows if (r['model'],r['c'])==k)==v
               for k,v in expected.items())
    perm_checks = 0
    for m in ('redundant','informative'):
        for perm in itertools.permutations(range(4)):
            for c in COSTS:
                r = audit(m,c,perm)
                assert r['cost'] == next(x['cost'] for x in rows
                                         if x['model']==m and x['c']==c)
                perm_checks += 1
    assert perm_checks == 192
    return {'status':'PASS','method':'independent full KKT Gaussian elimination',
            'exact_cases':len(rows),'permutation_checks':perm_checks,'rows':rows}

if __name__ == '__main__':
    print(json.dumps(main(),ensure_ascii=False,indent=2))
