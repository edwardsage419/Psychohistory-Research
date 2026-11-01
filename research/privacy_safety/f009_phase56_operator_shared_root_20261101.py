#!/usr/bin/env python3
"""Finite synthetic witness independence and false-operator metadata model."""
from itertools import product
import json
SLOTS = (
    {'label':'ORG_A', 'root':'CLOUD_X'},
    {'label':'ORG_B', 'root':'CLOUD_X'},
    {'label':'ORG_C', 'root':'CLOUD_Y'},
    {'label':'ORG_D', 'root':'CLOUD_Z'},
)
def policy(states, authenticated=True, trust_map_fresh=True, actual_roots=None):
    if not authenticated or not trust_map_fresh:
        return 'UNKNOWN_QUARANTINE'
    if actual_roots is None:
        actual_roots = tuple(x['root'] for x in SLOTS)
    valid = [i for i, x in enumerate(states) if x == 'VALID']
    revoked = [i for i, x in enumerate(states) if x == 'REVOKED']
    if valid and revoked:
        return 'CONFLICT_QUARANTINE'
    if revoked:
        return 'REJECT'
    if len({actual_roots[i] for i in valid}) >= 3:
        return 'REVIEW_ONLY'
    return 'UNKNOWN_QUARANTINE'
def naive(states):
    return len([x for x in states if x == 'VALID']) >= 2 and 'REVOKED' not in states
def run():
    states_all = list(product(('VALID','REVOKED','MISSING'), repeat=4))
    counts = {x:0 for x in ('REVIEW_ONLY','REJECT','CONFLICT_QUARANTINE','UNKNOWN_QUARANTINE')}
    false_independent = 0
    for states in states_all:
        decision = policy(states)
        counts[decision] += 1
        if naive(states) and decision != 'REVIEW_ONLY':
            false_independent += 1
    checks = 0
    def check(c, msg):
        nonlocal checks
        assert c, msg
        checks += 1
    check(len(states_all)==81,'universe')
    check(sum(counts.values())==81,'partition')
    check(policy(('VALID','VALID','MISSING','MISSING'))=='UNKNOWN_QUARANTINE','shared root')
    check(policy(('VALID','MISSING','VALID','VALID'))=='REVIEW_ONLY','three roots')
    check(policy(('VALID','VALID','VALID','MISSING'))=='UNKNOWN_QUARANTINE','two roots')
    check(policy(('VALID','MISSING','VALID','REVOKED'))=='CONFLICT_QUARANTINE','split view')
    check(policy(('MISSING','REVOKED','MISSING','MISSING'))=='REJECT','revocation')
    check(policy(('VALID','MISSING','VALID','VALID'),authenticated=False)=='UNKNOWN_QUARANTINE','forged labels')
    check(policy(('VALID','MISSING','VALID','VALID'),trust_map_fresh=False)=='UNKNOWN_QUARANTINE','stale map')
    check(policy(('VALID','VALID','VALID','MISSING'),actual_roots=('X','Y','Z','W'))=='REVIEW_ONLY','mapping matters')
    check(false_independent>0,'false quorum cases')
    check(counts['REVIEW_ONLY']>0,'review possible')
    print(json.dumps({'status':'PASS_SYNTHETIC_E1','states':81,'assertions':checks,
        'outcomes':counts,'naive_false_independent_acceptances':false_independent,
        'automatic_high_impact_restorations':0}, sort_keys=True))
if __name__=='__main__':
    run()
