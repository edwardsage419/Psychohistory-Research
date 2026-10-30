#!/usr/bin/env python3
"""Independent 27-cell audit for R283 S79. No import of R route."""
import argparse,csv,json,itertools,copy
from collections import defaultdict
from fractions import Fraction as F
from pathlib import Path
W={'HOMOGENEOUS':((F(3,4),F(1,4)),)*3,
   'BALANCED_HETEROGENEITY':((F(3,4),F(1,4)),(F(1,2),F(1,2)),(F(1,4),F(3,4))),
   'ONE_REVERSAL':((F(3,4),F(1,4)),(F(3,4),F(1,4)),(F(1,4),F(3,4)))}

def oracle(studies):
    w=[1/(t*(1-t)+c*(1-c)) for t,c in studies]
    out=defaultdict(F)
    for d in itertools.product((-1,0,1),repeat=3):
        prob=F(1)
        for (t,c),x in zip(studies,d):
            prob*={-1:(1-t)*c,0:t*c+(1-t)*(1-c),1:t*(1-c)}[x]
        m=sum((wi*di for wi,di in zip(w,d)),F())/sum(w)
        q=sum((wi*(di-m)**2 for wi,di in zip(w,d)),F())
        out[q]+=prob
    return out

def verify(rows,result):
    if result['evidence']!='E1_ARTIFICIAL_NONBLIND' or result['threshold_Q']!='6':raise ValueError('evidence or threshold mismatch')
    if result['freeze_commit']!='d6a072305ed28a12d987cf148f5f53b3eaeb3262':raise ValueError('freeze mismatch')
    if len(rows)!=192 or len({(r['regime'],r['source_T1C1T2C2T3C3']) for r in rows})!=192:raise ValueError('source coverage')
    for name,studies in W.items():
        subset=[r for r in rows if r['regime']==name]
        if len(subset)!=64 or {r['source_T1C1T2C2T3C3'] for r in subset}!={''.join(x) for x in itertools.product('01',repeat=6)}:raise ValueError('universe')
        o=oracle(studies)
        found=defaultdict(F)
        for r in subset:
            bits=[int(x) for x in r['source_T1C1T2C2T3C3']]
            ds=[bits[2*i]-bits[2*i+1] for i in range(3)]
            if r['study_differences']!=';'.join(map(str,ds)):raise ValueError('d mismatch')
            prob=F(1)
            for i,(t,c) in enumerate(studies):
                prob*=(t if bits[2*i] else 1-t)*(c if bits[2*i+1] else 1-c)
            if F(r['source_mass'])!=prob:raise ValueError('mass mismatch')
            w=[1/(t*(1-t)+c*(1-c)) for t,c in studies]
            m=sum((wi*di for wi,di in zip(w,ds)),F())/sum(w)
            q=sum((wi*(di-m)**2 for wi,di in zip(w,ds)),F())
            if F(r['Q'])!=q or int(r['alert_Q_ge_6'])!=int(q>=6):raise ValueError('Q mismatch')
            found[q]+=prob
        if dict(found)!=dict(o):raise ValueError('PMF mismatch')
        rr=next(x for x in result['results'] if x['regime']==name)
        if {F(x['q']):F(x['mass']) for x in rr['pmf']}!=dict(o):raise ValueError('receipt PMF mismatch')
        if F(rr['p_q_at_least_6'])!=sum((v for k,v in o.items() if k>=6),F()):raise ValueError('tail mismatch')
        if F(rr['p_q_zero'])!=o[F(0)] or F(rr['expected_q'])!=sum((k*v for k,v in o.items()),F()):raise ValueError('summary mismatch')
    return True

def main(root):
    with (root/'R283_S79_ALL_192_Q_SOURCES.csv').open(newline='') as f: rows=list(csv.DictReader(f))
    result=json.loads((root/'R283_S79_EXACT_Q_RESULTS.json').read_text())
    assert verify(rows,result)
    tests=[]
    def reject(name,changed_rows,changed_result):
        try:verify(changed_rows,changed_result)
        except (ValueError,KeyError,IndexError):tests.append(name);return
        raise AssertionError('mutation accepted: '+name)
    reject('duplicate',rows+[rows[0]],result)
    reject('missing',rows[:-1],result)
    a=copy.deepcopy(rows);a[0]['source_mass']='1';reject('mass',a,result)
    a=copy.deepcopy(rows);a[1]['Q']='999';reject('Q',a,result)
    a=copy.deepcopy(result);a['evidence']='E3_HISTORICAL';reject('grade',rows,a)
    a=copy.deepcopy(result);a['results'][0]['p_q_at_least_6']='0';reject('tail',rows,a)
    print('PASS: 192 source rows; 3 independent 27-cell PMFs; 6/6 mutations rejected:',','.join(tests))

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('root',type=Path);a=p.parse_args();main(a.root)
