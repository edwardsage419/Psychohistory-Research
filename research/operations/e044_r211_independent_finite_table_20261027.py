#!/usr/bin/env python3
"""R211 independent finite-table audit. Python 3 standard library only."""
from itertools import product, combinations
from fractions import Fraction
from collections import Counter
import json
TYPES=list(product((0,1),repeat=2))
PAIRS=list(combinations(range(4),2))
POLICIES=('FULL','FIXED_02','ARM_FAVORABLE')
EXPECTED={
'FULL':(1536,{0:1536},6144,1536,1536,0,0,102,96,0),
'FIXED_02':(1536,{2:1536},9216,1536,1024,512,0,60,256,186),
'ARM_FAVORABLE':(1536,{0:96,1:384,2:576,3:384,4:96},9216,1536,864,672,1728,246,864,220)}
def run():
    res={p:dict(rows=0,missing_hist=Counter(),width_quarters_sum=0,covered=0,cc_defined=0,cc_undefined=0,cc_diff_halves_sum=0,zero_ate_cc_positive=0,cc_equals_one=0,worlds_cc_mean_differs_from_true=0) for p in POLICIES}
    checks=0
    for s in product(TYPES,repeat=4):
        truth=sum(y1-y0 for y0,y1 in s)
        for policy in POLICIES:
            cc=[]
            for pair in PAIRS:
                lo=hi=m=0
                tr=[];co=[]
                for i,(y0,y1) in enumerate(s):
                    z=int(i in pair)
                    y=y1 if z else y0
                    response=(policy=='FULL' or (policy=='FIXED_02' and i in (0,2)) or (policy=='ARM_FAVORABLE' and ((z and y==1) or (not z and y==0))))
                    if response:
                        if z:lo+=y-1;hi+=y;tr.append(y)
                        else:lo-=y;hi+=1-y;co.append(y)
                    else:m+=1;lo-=1;hi+=1
                a=res[policy];a['rows']+=1;a['missing_hist'][m]+=1;a['width_quarters_sum']+=hi-lo;a['covered']+=int(lo<=truth<=hi)
                assert hi-lo==4+m
                assert 2**(4+m)>0
                assert lo<=truth<=hi
                checks+=3
                if tr and co:
                    diff=Fraction(sum(tr),len(tr))-Fraction(sum(co),len(co))
                    assert (diff*2).denominator==1
                    h=int(diff*2)
                    a['cc_defined']+=1;a['cc_diff_halves_sum']+=h;cc.append(diff)
                    a['zero_ate_cc_positive']+=int(truth==0 and diff>0)
                    a['cc_equals_one']+=int(diff==1)
                    if policy=='ARM_FAVORABLE':assert diff==1;checks+=1
                else:a['cc_undefined']+=1
            if cc and sum(cc,Fraction(0))/len(cc)!=Fraction(truth,4):res[policy]['worlds_cc_mean_differs_from_true']+=1
    keys=('rows','missing_hist','width_quarters_sum','covered','cc_defined','cc_undefined','cc_diff_halves_sum','zero_ate_cc_positive','cc_equals_one','worlds_cc_mean_differs_from_true')
    for p,expected in EXPECTED.items():
        for k,v in zip(keys,expected):
            assert res[p][k]==v,(p,k,res[p][k],v)
            checks+=1
    assert checks==14718
    return dict(checks=checks,failures=0,source_schedules=256,rows=4608,policies={p:{**d,'missing_hist':dict(d['missing_hist'])} for p,d in res.items()},evidence='INTERNAL_SYNTHETIC_E1_ONLY')
if __name__=='__main__':print(json.dumps(run(),ensure_ascii=False,sort_keys=True,indent=2))
