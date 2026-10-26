#!/usr/bin/env python3
"""R193 E1 exact S/A mixture Bayes error under count coarsening. Standard library only."""
from fractions import Fraction as F
from itertools import product
from math import comb
from pathlib import Path
import json

SOURCES={'S':((F(1,2),F(1,4)),(F(1,2),F(3,4))),
         'A':((F(9,13),F(1,3)),(F(4,13),F(7,8)))}

def pmf(n,source):
    return tuple(sum((w*comb(n,k)*q**k*(1-q)**(n-k) for w,q in SOURCES[source]),F(0)) for k in range(n+1))

def dist(n,source,channel):
    p=pmf(n,source)
    return p if channel=='full_K' else (sum(p[:-1],F(0)),p[-1])

def run(n,m,channel):
    p=dist(n,'S',channel);q=dist(n,'A',channel)
    assert sum(p)==sum(q)==1
    total=F(0)
    for sequence in product(range(len(p)),repeat=m):
        a=b=F(1)
        for k in sequence:a*=p[k];b*=q[k]
        total+=abs(a-b)
    tv=total/2
    return {'n':n,'m':m,'channel':channel,'alphabet_size':len(p),
            'ordered_sequences':len(p)**m,'S_pmf':[str(x) for x in p],
            'A_pmf':[str(x) for x in q],'TV':str(tv),
            'bayes_error':str((1-tv)/2)}

def main():
    rows=[run(n,m,c) for n in (2,3) for m in (1,2,3,4)
          for c in ('full_K','all_success_binary')]
    for row in rows:
        n,m,c=row['n'],row['m'],row['channel']
        tv=F(row['TV'])
        assert 0<=tv<=1
        assert 0<=F(row['bayes_error'])<=F(1,2)
        if n==2:assert tv==0
        if c=='all_success_binary':
            full=next(x for x in rows if x['n']==n and x['m']==m and x['channel']=='full_K')
            assert tv<=F(full['TV'])
        if m>1:
            prev=next(x for x in rows if x['n']==n and x['m']==m-1 and x['channel']==c)
            assert tv>=F(prev['TV'])
    assert F(next(x['TV'] for x in rows if x['n']==3 and x['m']==1 and x['channel']=='full_K'))>0
    out={'research_id':'R193','date':'2026-10-27',
         'scope':'E1 artificial exact postscore addendum',
         'protocol':'protocols/R193_S_A_OBSERVATION_COARSENING_BAYES_ERROR_THIRD_METHOD_FREEZE_2026-10-27.md',
         'rows':rows,'worlds':len(rows),
         'ordered_sequences_total':sum(x['ordered_sequences'] for x in rows),
         'all_prespecified_invariants_pass':True,'new_E2':0,'new_E3':0,
         'external_independent_replications':0}
    path=Path(__file__).with_name('R193_COARSENING_16_EXACT_RECEIPT_2026-10-27.json')
    path.write_text(json.dumps(out,sort_keys=True,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
    print('R193 PASS',len(rows),out['ordered_sequences_total'])
    for x in rows:print(x['n'],x['m'],x['channel'],x['TV'],x['bayes_error'])

if __name__=='__main__':main()
