#!/usr/bin/env python3
"""Independent R192 E1 audit: Walsh coefficients and unordered multinomial histograms."""
from fractions import Fraction as F
from itertools import product,combinations
from math import factorial
import json
from pathlib import Path

PARAMS={'A':(F(3,4),F(5,6),F(3,4)),'B':(F(5,6),F(3,4),F(3,4))}

def walsh_pmf(j,pi,orientation,disable_odd=False):
    delta=[2*x-1 for x in PARAMS[orientation][:j]]
    values=[]
    for bits in product((0,1),repeat=j):
        sign=[2*b-1 for b in bits]
        expansion=F(1)
        for r in range(1,j+1):
            for ids in combinations(range(j),r):
                weight=F(1) if r%2==0 else (F(0) if disable_odd else 2*pi-1)
                term=weight
                for i in ids:term*=delta[i]*sign[i]
                expansion+=term
        values.append(expansion/(2**j))
    assert sum(values)==1
    return values

def histograms(total,bins):
    if bins==1:yield (total,)
    else:
        for x in range(total+1):
            for tail in histograms(total-x,bins-1):
                yield (x,)+tail

def hist_tv(pa,pb,n):
    result=F(0);count=0
    for counts in histograms(n,len(pa)):
        multiplicity=factorial(n);a=F(1);b=F(1)
        for k,x in enumerate(counts):
            multiplicity//=factorial(x)
            a*=pa[k]**x;b*=pb[k]**x
        result+=multiplicity*abs(a-b);count+=1
    return result/2,count

def run():
    source=json.loads((Path(__file__).parent.parent/'validation'/'R192_PREVALENCE_SHIFT_18_EXACT_RECEIPT_2026-10-26.json').read_text())
    matched=0;pmfmatched=0;hist_total=0;entries=[]
    for row in source['rows']:
        j=row['J'];pi=F(row['pi']);n=row['n']
        pa=walsh_pmf(j,pi,'A');pb=walsh_pmf(j,pi,'B')
        tv,h=hist_tv(pa,pb,n)
        assert tv==F(row['total_variation'])
        assert (1-tv)/2==F(row['equal_prior_optimal_error'])
        hist_total+=h;matched+=2
        entries.append({'J':j,'pi':str(pi),'n':n,'histograms':h,'total_variation':str(tv)})
    for single in source['single_person_manifest_pmfs']:
        calc=walsh_pmf(single['J'],F(single['pi']),single['orientation'])
        assert [str(v) for v in calc]==list(single['pmf'].values())
        pmfmatched+=len(calc)
    incorrect_tv,_=hist_tv(walsh_pmf(2,F(1,4),'A',True),walsh_pmf(2,F(1,4),'B',True),1)
    actual_tv,_=hist_tv(walsh_pmf(2,F(1,4),'A'),walsh_pmf(2,F(1,4),'B'),1)
    assert incorrect_tv==0 and actual_tv==F(1,24)
    dropped,_=hist_tv(walsh_pmf(2,F(1,2),'A'),walsh_pmf(2,F(1,2),'B'),1)
    full,_=hist_tv(walsh_pmf(3,F(1,2),'A'),walsh_pmf(3,F(1,2),'B'),1)
    assert dropped==0 and full==F(1,24)
    result={'research_id':'R192','audit':'INTERNAL_DIFFERENT_ALGORITHM_E1','worlds':len(entries),
        'tv_and_error_exact_field_checks':matched,'single_person_exact_pmf_field_checks':pmfmatched,
        'unordered_histograms_evaluated':hist_total,'odd_moment_suppression_negative_control_detected':True,
        'third_indicator_drop_negative_control_detected':True,'entries':entries,'external_independent_replication':0}
    Path(__file__).with_name('B_R192_WALSH_HISTOGRAM_AUDIT_RECEIPT_2026-10-26.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    return result

if __name__=='__main__':
    result=run()
    print('PASS',result['worlds'],result['tv_and_error_exact_field_checks'],
          result['single_person_exact_pmf_field_checks'],result['unordered_histograms_evaluated'])
