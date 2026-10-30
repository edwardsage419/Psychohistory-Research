#!/usr/bin/env python3
"""R283 S79: exact finite-sample Cochran Q artificial E1 replay.
Usage: python R283_S79_EXACT_Q_REPLAY.py --output-dir /tmp/r283_s79
"""
import argparse
import csv
import itertools
import json
from collections import defaultdict
from fractions import Fraction as F
from pathlib import Path

FREEZE = 'd6a072305ed28a12d987cf148f5f53b3eaeb3262'
THRESHOLD = F(6)
WORLDS = {
    'HOMOGENEOUS': ((F(3,4), F(1,4)),) * 3,
    'BALANCED_HETEROGENEITY': ((F(3,4),F(1,4)), (F(1,2),F(1,2)), (F(1,4),F(3,4))),
    'ONE_REVERSAL': ((F(3,4),F(1,4)), (F(3,4),F(1,4)), (F(1,4),F(3,4))),
}
EXPECTED_MEANS = {'HOMOGENEOUS':F(2), 'BALANCED_HETEROGENEITY':F(10,3), 'ONE_REVERSAL':F(34,9)}

def exact_q(studies, ds):
    weights = [1 / (t*(1-t)+c*(1-c)) for t,c in studies]
    pooled = sum((w*d for w,d in zip(weights,ds)),F()) / sum(weights)
    return sum((w*(d-pooled)**2 for w,d in zip(weights,ds)),F())

def calculate():
    records=[]
    results=[]
    for name,studies in WORLDS.items():
        pmf=defaultdict(F)
        seen=set()
        for bits in itertools.product((0,1),repeat=6):
            source=''.join(map(str,bits))
            assert source not in seen
            seen.add(source)
            probability=F(1)
            ds=[]
            for i,(t,c) in enumerate(studies):
                a,b=bits[2*i:2*i+2]
                probability *= (t if a else 1-t) * (c if b else 1-c)
                ds.append(a-b)
            q=exact_q(studies,ds)
            pmf[q]+=probability
            records.append((name,source,str(probability),';'.join(map(str,ds)),str(q),str(int(q>=THRESHOLD))))
        assert len(seen)==64 and sum(pmf.values(),F())==1
        expected_q=sum((q*p for q,p in pmf.items()),F())
        assert expected_q==EXPECTED_MEANS[name]
        results.append({'regime':name,'source_count':64,'pmf_support':len(pmf),
            'p_q_zero':str(pmf[F(0)]),'p_q_at_least_6':str(sum((p for q,p in pmf.items() if q>=THRESHOLD),F())),
            'expected_q':str(expected_q),'min_q':str(min(pmf)),'max_q':str(max(pmf)),
            'pmf':[{'q':str(q),'mass':str(pmf[q])} for q in sorted(pmf)]})
    assert len(records)==192
    return records,results

def main(output_dir):
    records,results=calculate()
    output_dir.mkdir(parents=True,exist_ok=True)
    with (output_dir/'R283_S79_ALL_192_Q_SOURCES.csv').open('w',newline='',encoding='utf-8') as f:
        writer=csv.writer(f,lineterminator='\n')
        writer.writerow(('regime','source_T1C1T2C2T3C3','source_mass','study_differences','Q','alert_Q_ge_6'))
        writer.writerows(records)
    receipt={'research_id':'R283','extension':'S79','freeze_commit':FREEZE,'evidence':'E1_ARTIFICIAL_NONBLIND',
        'threshold_Q':str(THRESHOLD),'complete_source_rows':len(records),'R073':'FROZEN','PESEN_v0_1':'FROZEN',
        'results':results}
    (output_dir/'R283_S79_EXACT_Q_RESULTS.json').write_text(json.dumps(receipt,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
    print(json.dumps(receipt,indent=2,ensure_ascii=False))

if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--output-dir',type=Path,required=True)
    args=parser.parse_args()
    main(args.output_dir)
