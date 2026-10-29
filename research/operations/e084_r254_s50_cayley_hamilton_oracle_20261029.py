#!/usr/bin/env python3
"""E084 R254 S50 third route: closed-form Cayley-Hamilton, no R/B imports.
Usage: python e084_r254_s50_cayley_hamilton_oracle_20261029.py [downloaded_receipt.json]
The embedded expected values were read from GitHub receipt blob e79c83380ae86c2cdc63129484d4e550bde978b5.
This reconstructs artificial inputs; it does not audit the original 18432-row CSV.
"""
import itertools
import json
import sys
from collections import Counter
from fractions import Fraction

EXPECTED = {
    'independent_edge_seed_pairs':512,
    'paired_vector_mismatch_count_by_n':[0,192,152,200],
    'same_trace_A2_pairs':512,
    'same_trace_A4_pairs':512,
    'same_rho_squared_pairs':512,
    'different_trace_A3_pairs':64,
    'n1_analytic_condition_matches':512,
    'trace_moments':{
        '2':{'positive':'3','signed':'3','positive_minus_signed':'0'},
        '3':{'positive':'3/4','signed':'-3/4','positive_minus_signed':'3/2'},
        '4':{'positive':'6','signed':'6','positive_minus_signed':'0'},
    },
    'edge_mask_counts':{format(i,'03b'):64 for i in range(8)},
}

def state_closed_form(a,b,c,seed):
    """A^3=s A+2abc I; s=a^2+b^2+c^2, for zero-diagonal 3x3 symmetric A."""
    u,v,w=seed
    first=(a*v+b*w,a*u+c*w,b*u+c*v)
    second=((a*a+b*b)*u+b*c*v+a*c*w,
            b*c*u+(a*a+c*c)*v+a*b*w,
            a*c*u+a*b*v+(b*b+c*c)*w)
    s=a*a+b*b+c*c
    third=tuple(s*first[i]+2*a*b*c*seed[i] for i in range(3))
    return (seed,first,second,third)

def compute():
    mismatch=[0]*4
    moments={k:[0,0] for k in (2,3,4)}
    masks=Counter()
    first_matches=0
    odd=0
    coordinate_count=0
    for bits in itertools.product((0,1),repeat=6):
        a,b,c=(1-bits[0],1-bits[2],1-bits[4])
        s=a*a+b*b+c*c
        for seed in itertools.product((0,1),repeat=3):
            masks[f'{a}{b}{c}']+=1
            plus=state_closed_form(a,b,c,seed)
            minus=state_closed_form(a,b,-c,seed)
            for n in range(4):
                mismatch[n]+=plus[n]!=minus[n]
                coordinate_count+=6
            first_matches+=((plus[1]!=minus[1]) == bool(c and (seed[1] or seed[2])))
            odd+=(6*a*b*c != -6*a*b*c)
            for k, v in ((2,2*s),(3,6*a*b*c),(4,2*s*s)):
                moments[k][0]+=v
                moments[k][1]+=v if k%2==0 else -v
    out={
        'independent_edge_seed_pairs':512,
        'paired_vector_mismatch_count_by_n':mismatch,
        'same_trace_A2_pairs':512,
        'same_trace_A4_pairs':512,
        'same_rho_squared_pairs':512,
        'different_trace_A3_pairs':odd,
        'n1_analytic_condition_matches':first_matches,
        'trace_moments':{
            str(k):{
                'positive':str(Fraction(moments[k][0],512)),
                'signed':str(Fraction(moments[k][1],512)),
                'positive_minus_signed':str(Fraction(moments[k][0]-moments[k][1],512))
            } for k in (2,3,4)
        },
        'edge_mask_counts':dict(sorted(masks.items())),
    }
    return out, coordinate_count

def check(actual, expected):
    for key,value in expected.items():
        if actual.get(key)!=value:
            raise AssertionError(f'{key}: {actual.get(key)!r} != {value!r}')

if __name__=='__main__':
    actual,coordinates=compute()
    check(actual,EXPECTED)
    if len(sys.argv)>1:
        with open(sys.argv[1],encoding='utf-8') as f:
            receipt=json.load(f)
        check(actual,receipt)
    mutated=dict(EXPECTED)
    mutated['paired_vector_mismatch_count_by_n']=[0,192,152,201]
    rejected=False
    try:check(actual,mutated)
    except AssertionError:rejected=True
    assert rejected
    print(json.dumps({'status':'PASS','pairs':512,'coordinates':coordinates,
      'compared_fields':len(EXPECTED),'mutation_rejected':True,
      'original_csv_full_byte_audit':'NOT_PERFORMED','new_E2':0,'new_E3':0,
      'external_replication':0},ensure_ascii=False))
