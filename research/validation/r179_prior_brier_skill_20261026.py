"""R179 postacceptance E1: exact Brier skill of Beta posterior vs prior-only forecast.

Fixed 90-world grid from R179. Method A uses source count variance;
Method B enumerates source count PMFs without using Method A's variance.
No human or historical observations. Python standard library only.
"""
from fractions import Fraction as F
from itertools import product
from math import comb
from collections import Counter
import json
from pathlib import Path

NS = (4, 8, 12)
PS = (F(1, 4), F(1, 2))
SOURCES = ('IID_BIN', 'CLUSTERED_BB_C2', 'CLUSTERED_BB_C8', 'INACTIVE_ZIB_Z1_8', 'INACTIVE_ZIB_Z1_4')
PRIORS = (('U', 1, 1), ('S', 2, 2), ('A', 1, 3))


def source_variance(name, n, p):
    base = n * p * (1 - p)
    if name == 'IID_BIN':
        return base
    if name.startswith('CLUSTERED_BB_'):
        c = int(name.rsplit('C', 1)[1])
        return base * F(c + n, c + 1)
    z = F(1, 8) if name.endswith('1_8') else F(1, 4)
    return base + z / (1 - z) * n * (n - 1) * p**2


def rising(v, k):
    out = F(1)
    for i in range(k):
        out *= v + i
    return out


def source_pmf(name, n, p):
    if name == 'IID_BIN':
        return [F(comb(n, k)) * p**k * (1-p)**(n-k) for k in range(n+1)]
    if name.startswith('CLUSTERED_BB_'):
        c = int(name.rsplit('C', 1)[1])
        return [F(comb(n, k)) * rising(p*c, k) * rising((1-p)*c, n-k) / rising(F(c), n) for k in range(n+1)]
    z = F(1, 8) if name.endswith('1_8') else F(1, 4)
    q = p / (1-z)
    return [(z if k == 0 else F(0)) + (1-z)*comb(n,k)*q**k*(1-q)**(n-k) for k in range(n+1)]


def compute():
    records = []
    summary = Counter()
    for n,p,source,(prior,a,b) in product(NS,PS,SOURCES,PRIORS):
        weights = source_pmf(source,n,p)
        assert len(weights)==n+1 and sum(weights,F(0))==1 and min(weights)>=0
        v = source_variance(source,n,p)
        assert sum((F(k)-n*p)**2*w for k,w in enumerate(weights)) == v
        risk = (v + (a-(a+b)*p)**2) / (a+b+n)**2
        risk_b = sum(w*(F(a+k,a+b+n)-p)**2 for k,w in enumerate(weights))
        assert risk == risk_b
        prior_risk = (F(a,a+b)-p)**2
        half_risk = (F(1,2)-p)**2
        dprior = prior_risk-risk
        dhalf = half_risk-risk
        assert F(0)<=risk<=1
        assert (p*(1-p)+risk)-(p*(1-p)+prior_risk)==-dprior
        assert (p*(1-p)+risk)-(p*(1-p)+half_risk)==-dhalf
        sign = 'positive' if dprior>0 else 'negative' if dprior<0 else 'zero'
        summary[sign]+=1
        summary[f'{source}:{sign}']+=1
        summary[f'{prior}:{sign}']+=1
        records.append({'n':n,'p':str(p),'source':source,'prior':prior,'a':a,'b':b,
                        'source_variance':str(v),'posterior_mse':str(risk),
                        'prior_only_mse':str(prior_risk),'neutral_half_mse':str(half_risk),
                        'brier_skill_vs_prior':str(dprior),'brier_skill_vs_half':str(dhalf),
                        'posterior_expected_brier':str(p*(1-p)+risk),'sign_vs_prior':sign})
    assert len(records)==90
    n,p,source,prior,a,b=8,F(1,4),'CLUSTERED_BB_C2','U',1,1
    weights=source_pmf(source,n,p)
    wrong=sum(w*(F(a+k,a+b+n+1)-p)**2 for k,w in enumerate(weights))
    right=next(F(x['posterior_mse']) for x in records if (x['n'],x['p'],x['source'],x['prior'])==(n,str(p),source,prior))
    assert wrong!=right
    return {'research_id':'R179','date':'2026-10-26','evidence':'E1_SYNTHETIC_ONLY',
            'source_grid':'R179 fixed 90 posterior worlds','prior_baseline_sign_counts':{k:summary[k] for k in ('positive','zero','negative')},
            'by_prior':{x:{k:summary[f'{x}:{k}'] for k in ('positive','zero','negative')} for x,_,_ in PRIORS},
            'by_source':{x:{k:summary[f'{x}:{k}'] for k in ('positive','zero','negative')} for x in SOURCES},
            'selected_n8_p_quarter':[x for x in records if x['n']==8 and x['p']=='1/4'],
            'full_90_worlds':records,'independent_pmf_and_variance_routes_equal':True,
            'mutated_posterior_denominator_detected':True,'new_E2':0,'new_E3':0}


if __name__=='__main__':
    result=compute()
    with Path(__file__).with_name('R179_PRIOR_BRIER_SKILL_EXACT_RECEIPT_2026-10-26.json').open('w', encoding='utf-8') as f:
        json.dump(result,f,indent=2,ensure_ascii=False,sort_keys=True)
        f.write('\n')
    print(json.dumps({'counts':result['prior_baseline_sign_counts'],'by_prior':result['by_prior'],'by_source':result['by_source'],'selected':result['selected_n8_p_quarter']},ensure_ascii=False,indent=2))
