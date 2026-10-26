#!/usr/bin/env python3
"""B independent R193 E1 audit: Bernoulli DP plus unordered multinomial histograms."""
from fractions import Fraction as F
from math import factorial
from pathlib import Path
import json

SOURCES={'S':((F(1,2),F(1,4)),(F(1,2),F(3,4))),
         'A':((F(9,13),F(1,3)),(F(4,13),F(7,8)))}

def bernoulli_dp(n,q):
    a=[F(1)]
    for _ in range(n):
        b=[F(0)]*(len(a)+1)
        for k,p in enumerate(a):b[k]+=p*(1-q);b[k+1]+=p*q
        a=b
    return a

def dist(n,source,channel):
    a=[F(0)]*(n+1)
    for w,q in SOURCES[source]:
        for k,p in enumerate(bernoulli_dp(n,q)):a[k]+=w*p
    return a if channel=='full_K' else [sum(a[:-1],F(0)),a[-1]]

def hist(k,m):
    if k==1:yield (m,)
    else:
        for i in range(m+1):
            for tail in hist(k-1,m-i):yield (i,)+tail

def exact(n,m,channel):
    p=dist(n,'S',channel);q=dist(n,'A',channel)
    assert sum(p)==sum(q)==1
    total=F(0);configs=0;sequences=0
    for counts in hist(len(p),m):
        configs+=1;weight=factorial(m);a=b=F(1)
        for t,x,y in zip(counts,p,q):
            weight//=factorial(t);a*=x**t;b*=y**t
        total+=weight*abs(a-b);sequences+=weight
    assert sequences==len(p)**m
    return total/2,configs

def main():
    path=Path(__file__).with_name('R193_COARSENING_16_EXACT_RECEIPT_2026-10-27.json')
    rows=json.loads(path.read_text(encoding='utf-8'))['rows']
    details=[];checked=0;configs=0
    for r in rows:
        n,m,c=r['n'],r['m'],r['channel']
        tv,h=exact(n,m,c)
        assert tv==F(r['TV'])
        assert (1-tv)/2==F(r['bayes_error'])
        assert [str(x) for x in dist(n,'S',c)]==r['S_pmf']
        assert [str(x) for x in dist(n,'A',c)]==r['A_pmf']
        checked+=4;configs+=h
        details.append({'n':n,'m':m,'channel':c,'histograms':h,'TV':str(tv)})
    alias=exact(2,1,'full_K')[0];full=exact(3,1,'full_K')[0]
    binary=exact(3,1,'all_success_binary')[0]
    assert alias==0 and full>0 and alias!=full
    assert binary<full
    result={'research_id':'R193','status':'PASS_BOUNDED_INTERNAL_E1_DIFFERENT_ALGORITHM',
            'rows_checked':len(rows),'exact_field_comparisons':checked,
            'unordered_histogram_configurations':configs,
            'n2_alias_negative_control_detected':True,
            'coarsening_strict_loss_negative_control_detected':True,
            'details':details,'external_independent_replications':0,'new_E2':0,'new_E3':0}
    out=Path(__file__).with_name('B_R193_HISTOGRAM_DP_AUDIT_RECEIPT_2026-10-27.json')
    out.write_text(json.dumps(result,sort_keys=True,indent=2)+'\n',encoding='utf-8')
    print('B_R193 PASS',len(rows),checked,configs)

if __name__=='__main__':main()
