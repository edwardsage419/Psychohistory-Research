#!/usr/bin/env python3
"""Independent nonblind S86 binomial-marginal exact audit; no R imports.
Usage: python b_r290_s86_independent_binomial_oracle.py R290_S86_EXACT_RESULTS.json
"""
import json
import math
import sys
from fractions import Fraction as Q

DISTRIBUTIONS = {
    'MONOTONE': ((8,6,4,2,1),(1,2,4,6,8),21),
    'CENTERED': ((8,2,1,2,8),(1,3,13,3,1),21),
    'IDENTICAL': ((1,2,3,2,1),(1,2,3,2,1),9),
}

def binomial(m,k,p):
    return Q(math.comb(m,k)) * p**k * (1-p)**(m-k)

def expected_risk(name, pi, fp, fn, m):
    nn, ss, den = DISTRIBUTIONS[name]
    total = Q(0)
    for x in range(5):
        pn, ps = Q(nn[x],den), Q(ss[x],den)
        signal_probability = Q(0)
        for kn in range(m+1):
            for ks in range(m+1):
                p = binomial(m,kn,pn)*binomial(m,ks,ps)
                signal_probability += p * int(pi*fn*(ks+1) > (1-pi)*fp*(kn+1))
        total += (1-pi)*fp*pn*signal_probability + pi*fn*ps*(1-signal_probability)
    return total

def verify(doc):
    assert doc['evidence']=='E1_ARTIFICIAL_ONLY' and doc['new_E2']==doc['new_E3']==0
    assert doc['R073']=='FROZEN' and doc['PESEN']=='FROZEN'
    assert len(doc['results'])==24
    keys=set()
    for row in doc['results']:
        key=(row['world'],row['m'])
        if key in keys: raise ValueError('duplicate world and sample size')
        keys.add(key)
        name,tail=row['world'].split('_PI')
        prior_s, costs_s=tail.split('_FP')
        pi=Q(*map(int,prior_s.split('of')))
        fp_s,fn_s=costs_s.split('_FN')
        fp,fn=int(fp_s),int(fn_s)
        m=row['m']
        assert m in (1,2) and name in DISTRIBUTIONS
        if row['sources'] != 5**(2*m) or row['training_mass']!='1':
            raise ValueError('training coverage or mass')
        v=expected_risk(name,pi,fp,fn,m)
        if Q(row['expected_heldout_risk']) != v:
            raise ValueError('independent binomial risk mismatch '+str(key))
        if Q(row['regret']) != v-Q(row['oracle_risk']) or Q(row['regret'])<0:
            raise ValueError('regret or oracle')
    assert len(keys)==24
    return len(keys)

def negatives(doc):
    import copy
    cases=[]
    for label, change in [
        ('duplicate', lambda d: d['results'].__setitem__(1,copy.deepcopy(d['results'][0]))),
        ('missing',lambda d: d['results'].pop()),
        ('risk',lambda d: d['results'][0].__setitem__('expected_heldout_risk','999')),
        ('mass',lambda d: d['results'][0].__setitem__('training_mass','1/2')),
        ('class_swap',lambda d: d['results'][0].__setitem__('expected_heldout_risk','0')),
        ('E2_upgrade',lambda d: d.__setitem__('evidence','E2_HUMAN')),
        ('regret',lambda d: d['results'][0].__setitem__('regret','-1')),
    ]:
        bad=copy.deepcopy(doc);change(bad)
        try: verify(bad)
        except (ValueError,AssertionError):cases.append(label)
        else: raise AssertionError('mutation accepted '+label)
    return cases

if __name__=='__main__':
    with open(sys.argv[1],encoding='utf-8') as f: doc=json.load(f)
    print(json.dumps({'status':'PASS','world_sample_combinations':verify(doc),'rejected_mutations':negatives(doc)},indent=2))
