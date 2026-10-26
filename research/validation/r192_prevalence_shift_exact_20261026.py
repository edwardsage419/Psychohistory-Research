#!/usr/bin/env python3
"""R192 postscore E1: exact observable identification under class prevalence shift."""
from fractions import Fraction as F
from itertools import product
import json
from pathlib import Path

QS={"A":(F(3,4),F(5,6),F(3,4)),"B":(F(5,6),F(3,4),F(3,4))}
PIS=(F(1,4),F(1,2),F(3,4))

def pmf(j,pi,orientation):
    q=QS[orientation][:j]
    result={}
    for bits in product((0,1),repeat=j):
        high=F(1);low=F(1)
        for b,p in zip(bits,q):
            high*=p if b else 1-p
            low*=(1-p) if b else p
        result[''.join(map(str,bits))]=pi*high+(1-pi)*low
    assert sum(result.values())==1
    return result

def ordered_tv(p,q,n):
    keys=sorted(p);tv=F(0);states=0
    for tup in product(keys,repeat=n):
        pa=F(1);pb=F(1)
        for key in tup:
            pa*=p[key];pb*=q[key]
        tv+=abs(pa-pb);states+=1
    return tv/2,states

def run():
    rows=[];singles=[]
    for j in (2,3):
        for pi in PIS:
            pa=pmf(j,pi,'A');pb=pmf(j,pi,'B')
            for name,p in [('A',pa),('B',pb)]:
                singles.append({'J':j,'pi':str(pi),'orientation':name,'pmf':{k:str(v) for k,v in p.items()}})
            prev=None
            for n in (1,2,3):
                tv,states=ordered_tv(pa,pb,n)
                assert states==2**(j*n) and 0<=tv<=1
                assert prev is None or tv>=prev
                prev=tv
                j2tv,_=ordered_tv(pmf(2,pi,'A'),pmf(2,pi,'B'),n)
                if j==2:assert (tv==0)==(pi==F(1,2))
                else:assert tv>0 and tv>=j2tv
                rows.append({'J':j,'pi':str(pi),'n':n,'ordered_states':states,
                    'total_variation':str(tv),'equal_prior_optimal_error':str((1-tv)/2),
                    'projected_first_two_tv':str(j2tv)})
    assert len(rows)==18 and len(singles)==12
    assert ordered_tv(pmf(2,F(1,4),'A'),pmf(2,F(1,4),'A'),3)[0]==0
    for pi in PIS:
        for orientation in QS:
            p3=pmf(3,pi,orientation);p2=pmf(2,pi,orientation)
            assert all(sum(p3[k+b] for b in ('0','1'))==p2[k] for k in p2)
    return {'research_id':'R192','date':'2026-10-26','evidence':'E1_ARTIFICIAL_EXACT_POSTSCORE',
        'protocol':'protocols/R192_PREVALENCE_SHIFT_OBSERVABLE_IDENTIFICATION_THIRD_METHOD_FREEZE_2026-10-26.md',
        'fixed_prior_candidates':['A','B'],'world_count':18,
        'total_ordered_states':sum(x['ordered_states'] for x in rows),
        'rows':rows,'single_person_manifest_pmfs':singles,
        'negative_control_same_candidate_tv_zero':True,'coarsening_projection_identity':True,
        'new_E2':0,'new_E3':0,'external_independent_replication':0}

if __name__=='__main__':
    obj=run()
    target=Path(__file__).with_name('R192_PREVALENCE_SHIFT_18_EXACT_RECEIPT_2026-10-26.json')
    target.write_text(json.dumps(obj,ensure_ascii=False,indent=2,sort_keys=True)+'\n')
    for row in obj['rows']:
        print(row['J'],row['pi'],row['n'],row['total_variation'],row['equal_prior_optimal_error'])
    print('PASS',obj['world_count'],obj['total_ordered_states'])
