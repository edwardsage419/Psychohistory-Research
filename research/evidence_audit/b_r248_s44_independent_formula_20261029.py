#!/usr/bin/env python3
"""Independent R248 S44 exact Fraction audit, no R CSV or JavaScript imports."""
from collections import Counter
from fractions import Fraction as F
import json
import sys

INITIALS = tuple(map(F, ('-1/2','-1/4','0','1/4','1/2','2/3','3/4','1','5/4')))
ROOTS = {
 'AFFINE_CONTRACT_ZERO':F(0), 'AFFINE_CONTRACT_ONE':F(1),
 'AFFINE_ALTERNATE_CONTRACT':F(0), 'AFFINE_EXPAND_ZERO':F(0),
 'IDENTITY_EVERY_POINT_FIXED':F(0), 'LOGISTIC_R2':F('1/2'),
 'LOGISTIC_R3_BORDER':F('2/3'), 'LOGISTIC_R4_REPELLER':F('3/4'),
 'CUBIC_NONHYPERBOLIC_ATTRACTOR':F(0)}

def orbit(world, initial):
    x = initial
    seq = [x]
    for _ in range(4):
        if world == 'AFFINE_CONTRACT_ZERO': x = x/2
        elif world == 'AFFINE_CONTRACT_ONE': x = (x+1)/2
        elif world == 'AFFINE_ALTERNATE_CONTRACT': x = -x/2
        elif world == 'AFFINE_EXPAND_ZERO': x = 2*x
        elif world == 'IDENTITY_EVERY_POINT_FIXED': x = x
        elif world in ('LOGISTIC_R2','LOGISTIC_R3_BORDER','LOGISTIC_R4_REPELLER'):
            r = {'LOGISTIC_R2':2,'LOGISTIC_R3_BORDER':3,'LOGISTIC_R4_REPELLER':4}[world]
            x = r*x*(1-x)
        elif world == 'CUBIC_NONHYPERBOLIC_ATTRACTOR': x = x*(1-x*x)
        else: raise AssertionError('unknown map')
        seq.append(x)
    return seq

def audit():
    results, summaries = [], {}
    for world, root in ROOTS.items():
        labels = Counter()
        for initial in INITIALS:
            d = [abs(z-root) for z in orbit(world,initial)]
            label = ('AT_FIXED_EXCLUDED' if d[0]==0 else
                     'SHRINK' if d[4]<d[0] else
                     'TIE' if d[4]==d[0] else 'EXPAND')
            labels[label] += 1
            results.append(dict(world=world,x0=str(initial),label=label,distances=list(map(str,d))))
        summaries[world] = {k:labels[k] for k in ('SHRINK','TIE','EXPAND','AT_FIXED_EXCLUDED')}
    assert len(results)==81
    assert next(x for x in results if x['world']=='LOGISTIC_R4_REPELLER' and x['x0']=='1/4')['label']=='SHRINK'
    assert all(x['label']=='TIE' for x in results if x['world']=='IDENTITY_EVERY_POINT_FIXED' and x['x0']!='0')
    assert all(x['label']=='EXPAND' for x in results if x['world']=='AFFINE_EXPAND_ZERO' and x['x0']!='0')
    return dict(research_id='R248_S44',method='INDEPENDENT_PYTHON_FRACTION_DIRECT_FORMULA',
                worlds=9,trajectories=81,points=405,summary=summaries,rows=results,failures=0)

def verify(independent, source_receipt):
    actual = {(r['world'],r['x0']):r for r in independent['rows']}
    expected = {(r['world'],r['x0']):r for r in source_receipt['rows']}
    if set(actual)!=set(expected): raise AssertionError('different cohort universe')
    comparisons = 0
    for key, row in actual.items():
        ref = expected[key]
        if row['label']!=ref['label']: raise AssertionError('label mismatch '+str(key))
        comparisons += 1
        for a,b in zip(row['distances'],ref['distances']):
            if F(a)!=F(b): raise AssertionError('distance mismatch '+str(key))
            comparisons += 1
    return comparisons

if __name__ == '__main__':
    data=audit()
    if len(sys.argv)>1:
        with open(sys.argv[1],encoding='utf-8') as f:
            source=json.load(f)
        data['cross_runtime_comparisons']=verify(data,source)
    print(json.dumps(data,ensure_ascii=False,indent=2))
