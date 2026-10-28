#!/usr/bin/env python3
"""Independent R254 S50 B oracle: direct path enumeration and closed walks.
Does not import the R script or call its matrix multiplication/trajectory code.
"""
import itertools, json, sys
from collections import Counter
from fractions import Fraction
from pathlib import Path

HERE=Path(__file__).resolve().parent

def signed_edges(bits,sign):
    on=[(bits[2*i],bits[2*i+1]) in ((0,0),(0,1)) for i in range(3)]
    return (int(on[0]),int(on[1]),sign*int(on[2]))

def weight(edges,i,j):
    if i==j:return 0
    return edges[{(0,1):0,(0,2):1,(1,2):2}[tuple(sorted((i,j)))]]

def path_coordinate(edges,seed,start,n):
    if n==0:return seed[start]
    total=0
    for path in itertools.product(range(3),repeat=n):
        vertices=(start,)+path
        product=seed[path[-1]]
        for j in range(n):product*=weight(edges,vertices[j],vertices[j+1])
        total+=product
    return total

def closed_walk_trace(edges,n):
    return sum(
        __import__('math').prod(weight(edges,v[j],v[j+1]) for j in range(n))
        for v0 in range(3)
        for suffix in itertools.product(range(3),repeat=n-1)
        for v in [(v0,)+suffix+(v0,)]
    )

def calculate():
    moments={k:[0,0] for k in (2,3,4)}
    mismatch=[0,0,0,0]
    odd_count=0; even_matches=0; checks=0; masks=Counter()
    for bits in itertools.product((0,1),repeat=6):
        p=signed_edges(bits,1);q=signed_edges(bits,-1)
        assert p[:2]==q[:2] and p[2]==-q[2]
        tp={k:closed_walk_trace(p,k) for k in (2,3,4)}
        tq={k:closed_walk_trace(q,k) for k in (2,3,4)}
        assert tp[3]==6*p[0]*p[1]*p[2]
        assert tq[3]==6*q[0]*q[1]*q[2]
        for seed in itertools.product((0,1),repeat=3):
            masks[''.join(str(abs(x)) for x in p)]+=1
            odd_count+=tp[3]!=tq[3]
            even_matches+=tp[2]==tq[2] and tp[4]==tq[4]
            for k in (2,3,4):
                moments[k][0]+=tp[k]
                moments[k][1]+=tq[k]
            for n in range(4):
                sp=tuple(path_coordinate(p,seed,i,n) for i in range(3))
                sq=tuple(path_coordinate(q,seed,i,n) for i in range(3))
                mismatch[n]+=sp!=sq
                checks+=6
    return {
       'independent_edge_seed_pairs':512,
       'same_trace_A2_pairs':even_matches,
       'same_trace_A4_pairs':even_matches,
       'different_trace_A3_pairs':odd_count,
       'paired_vector_mismatch_count_by_n':mismatch,
       'trace_moments':{str(k):{'positive':str(Fraction(v[0],512)),'signed':str(Fraction(v[1],512)),
        'positive_minus_signed':str(Fraction(v[0]-v[1],512))} for k,v in moments.items()},
       'edge_mask_counts':dict(sorted(masks.items())),
       'independently_calculated_state_coordinates':checks
    }

def compare(actual,receipt):
    for k,v in actual.items():
        if k=='independently_calculated_state_coordinates':continue
        if receipt.get(k)!=v:raise AssertionError(f'independent oracle mismatch: {k}')

if __name__=='__main__':
    receipt=json.loads((HERE.parent/'validation'/'R254_S50_PAIRED_SIGNED_TRACE_RECEIPT_2026-10-29.json').read_text())
    actual=calculate()
    compare(actual,receipt)
    bad=dict(receipt);bad['paired_vector_mismatch_count_by_n']=[0,192,152,999]
    mutation_rejected=False
    try:compare(actual,bad)
    except AssertionError:mutation_rejected=True
    assert mutation_rejected
    print(json.dumps({'status':'INTERNAL_INDEPENDENT_WALK_ORACLE_PASS',
        'paired_cases':512,'coordinates_calculated':actual['independently_calculated_state_coordinates'],
        'verified_fields':len(actual)-1,'mutation_rejected':mutation_rejected,
        'source_full_byte_audit':'NOT_PERFORMED','external_replication':0},indent=2))
