#!/usr/bin/env python3
"""R251 S47 independent Fraction reconstruction from frozen map equations.
Usage: python b_r251_s47_independent_fraction_20261029.py [R_receipt.json]
No dependencies; no R-track source CSV or JS imports.
"""
import json
import sys
from fractions import Fraction as F
from pathlib import Path

INITIALS = tuple(map(F, ('-1/2','-1/4','-1/12','-1/24','0','1/24','1/12','1/4','1/2')))
WORLDS = ('HALF_CONTRACTION','NEGATIVE_HALF_CONTRACTION','ZERO_MAP',
          'DOUBLE_EXPANSION','IDENTITY_NEUTRAL','SIGN_FLIP_NEUTRAL',
          'CUBIC_LOCAL_INWARD','CUBIC_OUTWARD','LOGISTIC_R3_CENTERED')

def step(w,x):
    if w == 'HALF_CONTRACTION': return x/2
    if w == 'NEGATIVE_HALF_CONTRACTION': return -x/2
    if w == 'ZERO_MAP': return F(0)
    if w == 'DOUBLE_EXPANSION': return 2*x
    if w == 'IDENTITY_NEUTRAL': return x
    if w == 'SIGN_FLIP_NEUTRAL': return -x
    if w == 'CUBIC_LOCAL_INWARD': return x-x**3
    if w == 'CUBIC_OUTWARD': return x+x**3
    if w == 'LOGISTIC_R3_CENTERED': return -x-3*x**2
    raise ValueError(w)

def sgn(x):
    return '+' if x>0 else '-' if x<0 else '0'

def independent():
    output=[]
    for w in WORLDS:
        counts={'negative':0,'zero':0,'positive':0}
        net={'shrink':0,'equal':0,'grow':0}
        local={'count':0,'strict4':0,'net4_shrink':0}
        cohorts=[]
        strict=0
        for initial in INITIALS:
            trajectory=[initial]
            for _ in range(5): trajectory.append(step(w,trajectory[-1]))
            for t in range(5):
                dv=trajectory[t+1]**2-trajectory[t]**2
                counts[{'-':'negative','0':'zero','+':'positive'}[sgn(dv)]]+=1
            if initial==0: continue
            signs=''.join(sgn(trajectory[t+1]**2-trajectory[t]**2) for t in range(4))
            is_strict=signs=='----'
            strict+=int(is_strict)
            cls='shrink' if abs(trajectory[4])<abs(initial) else 'grow' if abs(trajectory[4])>abs(initial) else 'equal'
            net[cls]+=1
            if abs(initial)<=F(1,12):
                local['count']+=1
                local['strict4']+=int(is_strict)
                local['net4_shrink']+=int(cls=='shrink')
            cohorts.append({'x0':str(initial),'delta_signs_t0_t3':signs,'strict4':is_strict,'net4':cls})
        output.append({'world':w,'source_rows':45,'delta_sign_counts':counts,
                       'strict4_cohorts':strict,'net4_cohorts':net,'local':local,'cohorts':cohorts})
    return {'research_id':'R251_S47','source_rows':405,'independent_cohorts':72,'worlds':output}

def compare(receipt):
    other=independent()
    for key in ('research_id','source_rows','independent_cohorts','worlds'):
        if receipt.get(key)!=other[key]:
            raise AssertionError('independent formula mismatch: '+key)
    return len(WORLDS)*5+len(WORLDS)*8*4

def main():
    result=independent()
    assert len(result['worlds'])==9
    assert sum(sum(w['delta_sign_counts'].values()) for w in result['worlds'])==405
    assert sum(sum(w['net4_cohorts'].values()) for w in result['worlds'])==72
    assert next(w for w in result['worlds'] if w['world']=='ZERO_MAP')['strict4_cohorts']==0
    assert next(w for w in result['worlds'] if w['world']=='LOGISTIC_R3_CENTERED')['local']['net4_shrink']==4
    if len(sys.argv)>1:
        receipt=json.loads(Path(sys.argv[1]).read_text(encoding='utf-8'))
        checks=compare(receipt)
        mutant=json.loads(json.dumps(receipt))
        mutant['worlds'][0]['strict4_cohorts']+=1
        try: compare(mutant)
        except AssertionError: pass
        else: raise AssertionError('mutant was accepted')
        print(json.dumps({'status':'PASS','worlds':9,'cohorts':72,'source_atoms_reconstructed':405,
                          'cross_route_comparisons':checks,'mutation_rejected':True}))
    else: print(json.dumps(result,ensure_ascii=False,indent=2))

if __name__=='__main__': main()
