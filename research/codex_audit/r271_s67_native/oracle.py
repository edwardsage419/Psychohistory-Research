"""Nonblind S67 exact oracle: rolling run-length DP, disjoint complements.

Imports neither archived route; no source-string enumeration or inclusion-exclusion.
"""
from fractions import Fraction as F
from math import comb

def require(ok,message):
    if not ok:raise ValueError(message)

def risks():
    # Live states record trailing-success length 0..3; a run of four absorbs.
    # Integer path counts use all 2^(m+3) equiprobable bit histories.
    rolling={}
    for m in (1,2,3):
        live=[1,0,0,0];hit=0
        for _ in range(m+3):
            hit=2*hit+live[3]
            live=[sum(live),live[0],live[1],live[2]]
        rolling[m]=F(hit,2**(m+3))
    min_p=F(comb(4,4),2**4)
    out={}
    for m in (1,2,3):
        for design,union in (('IDENTICAL',min_p),('ROLLING',rolling[m]),('DISJOINT',1-(1-min_p)**m)):
            for policy in ('FROZEN_FIRST','FLEXIBLE_ANY','BONFERRONI_ANY'):
                risk=min_p if policy=='FROZEN_FIRST' else union
                if policy=='BONFERRONI_ANY' and min_p>F(1,8*m):risk=F(0)
                out[f'{design}_M{m}_{policy}']=risk
    return out

def verify_results(obj):
    require(type(obj) is dict,'result object')
    flags={'research_id':'R271_S67','original_model':'R271',
           'evidence':'E1_EXPLORATORY_ARTIFICIAL_NONBLIND','strict_blind_prescore_freeze':False,
           'real_human_E2':0,'real_historical_E3':0,'external_independent_replications':0,
           'original_R271_acceptance_unchanged':True,'R073':'FROZEN','PESEN_v0_1':'FROZEN',
           'world_count':27,'policy_labelled_source_count':13584}
    for key,value in flags.items():
        require(type(obj.get(key)) is type(value) and obj[key]==value,'result metadata '+key)
    require(type(obj.get('worlds')) is list and len(obj['worlds'])==27,'world list')
    expected=risks();seen=set();source_total=0
    for row in obj['worlds']:
        require(type(row) is dict,'world object')
        key=row.get('world');require(type(key) is str and key in expected and key not in seen,'duplicate/unknown world')
        seen.add(key);design,ms,policy=key.split('_',2);m=int(ms[1:])
        require(type(row.get('m')) is int and row['m']==m and row.get('design')==design and row.get('policy')==policy,'world identity')
        length=4 if design=='IDENTICAL' else m+3 if design=='ROLLING' else 4*m
        require(type(row.get('source_count')) is int and row['source_count']==2**length,'source count')
        require(type(row.get('exact_familywise_false_positive_risk')) is str and row['exact_familywise_false_positive_risk']==str(expected[key]),'exact risk')
        source_total+=row['source_count']
    require(set(expected)==seen and source_total==13584,'source universe')
    return {'status':'COMPLETE','worlds_verified':27,'policy_labelled_sources':source_total,
            'method':'rolling run-length DP; disjoint complement; no imports from R/B',
            'evidence':'NONBLIND_INTERNAL_ARTIFICIAL_E1','external_team_replications':0}
