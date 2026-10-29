#!/usr/bin/env python3
"""Independent K-count audit of R275 S71 persisted CSV and JSON.
Usage: python b_r275_s71_independent_gate.py results.json rows.csv
Standard library only. Does not call the R source enumerator.
"""
import csv
import json
import sys
from fractions import Fraction as F
from math import comb

M = ('IID_PAIR', 'COPY_PAIR', 'FLIP_PAIR')
E = (F(0), F(1,8), F(1,4), F(1,2))

def oracle(e):
    conf = {m: {n: F(0) for n in M} for m in M}
    decisions = []
    for k in range(5):
        p = (F(1,16), (1-e)**k*e**(4-k), e**k*(1-e)**(4-k))
        decision = M[p.index(max(p))]
        decisions.append(decision)
        for i,m in enumerate(M):
            conf[m][decision] += comb(4,k)*p[i]
    assert all(sum(row.values()) == 1 for row in conf.values())
    avg = sum(conf[m][m] for m in M)/3
    return conf, avg, decisions

def check(result_path, csv_path):
    data=json.load(open(result_path, encoding='utf-8'))
    assert data['research_id']=='R275_S71'
    assert data['evidence']=='E1_ARTIFICIAL_NONBLIND'
    assert data['source_rows']==3072 and data['new_E2']==data['new_E3']==0
    assert len(data['summary'])==4
    observed=set(); counts={(str(e),m):0 for e in E for m in M}
    with open(csv_path, newline='', encoding='utf-8') as f:
        reader=csv.DictReader(f)
        expected={'epsilon','true_mechanism','pair_code','equal_pair_count','true_source_probability','MAP_selected','correct','posterior_IID','posterior_COPY','posterior_FLIP'}
        assert set(reader.fieldnames)==expected
        for row in reader:
            e=F(row['epsilon']);true=row['true_mechanism'];code=row['pair_code']
            assert e in E and true in M and len(code)==4 and all(c in '0123' for c in code)
            key=(str(e),true,code)
            assert key not in observed,'duplicate source';observed.add(key)
            counts[(str(e),true)]+=1
            k=sum(c in '03' for c in code)
            assert int(row['equal_pair_count'])==k
            p=(F(1,16),(1-e)**k*e**(4-k),e**k*(1-e)**(4-k))
            q=tuple(x/F(16) for x in p)
            assert F(row['true_source_probability'])==q[M.index(true)]
            choice=M[p.index(max(p))]
            assert row['MAP_selected']==choice and int(row['correct'])==int(choice==true)
            post=[F(row['posterior_IID']),F(row['posterior_COPY']),F(row['posterior_FLIP'])]
            assert sum(post)==1 and post==[x/sum(p) for x in p]
    assert len(observed)==3072 and all(n==256 for n in counts.values())
    for s,e in zip(data['summary'],E):
        conf,avg,labels=oracle(e)
        assert F(s['epsilon'])==e and F(s['average_MAP_correct'])==avg
        assert s['K_decisions']==labels
        for m in M:
            for n in M:assert F(s['confusion'][m][n])==conf[m][n]
    assert oracle(F(0))[1]==F(23,24)
    assert oracle(F(1,2))[1]==F(1,3)
    return {'source_rows':len(observed),'epsilons':4,'confusion_cells':36,'MAP_values':4,'status':'PASS'}

if __name__=='__main__':
    if len(sys.argv)!=3:raise SystemExit('usage: gate.py results.json rows.csv')
    print(json.dumps(check(sys.argv[1],sys.argv[2])))
