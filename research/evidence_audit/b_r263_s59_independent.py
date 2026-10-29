#!/usr/bin/env python3
"""R263 S59 B oracle. Independent parent-pair × operator distribution, exact fractions.
Usage: python b_r263_s59_independent.py R263_S59_GLOBAL_PEAK_RESULTS.json
"""
from fractions import Fraction
from collections import Counter, defaultdict
from itertools import product
import json, sys

CONFIG = {
 'CLONAL_ONEMAX':(0,0,0,0),'CROSS_ONEMAX':(1,0,0,0),
 'MUTATE_ONEMAX':(0,1,0,0),'CROSS_MUTATE_ONEMAX':(1,1,0,0),
 'ELITE_CLONAL_ONEMAX':(0,0,1,0),'ELITE_CROSS_ONEMAX':(1,0,1,0),
 'ELITE_MUTATE_ONEMAX':(0,1,1,0),'ELITE_CROSS_MUTATE_ONEMAX':(1,1,1,0),
 'ELITE_CROSS_MUTATE_TRAP':(1,1,1,1)
}

def event(a,b,ops,config):
    cross,mutation,elite,trap=config
    flag,cut,flip0,flip1=ops
    if cross and flag:
        low=3 if cut==0 else 1
        c=(a & ~low)|(b & low)
        d=(b & ~low)|(a & low)
    else:
        c,d=a,b
    if mutation and flip0: c^=4
    if mutation and flip1: d^=1
    score=lambda x: 4 if trap and x==0 else x.bit_count()
    if elite:
        choices=(a,b,c,d)
        rank=sorted(range(4),key=lambda i:(-score(choices[i]),choices[i],i))
        c,d=choices[rank[0]],choices[rank[1]]
    return int(max(score(c),score(d))==(4 if trap else 3))

def oracle(world):
    flags=CONFIG[world]
    groups=[defaultdict(Counter) for _ in range(5)]
    seen=set()
    positives=0
    for a in range(8):
        for b in range(8):
            for ops in product((0,1),repeat=4):
                identity=(a,b,*ops)
                if identity in seen: raise AssertionError('duplicate')
                seen.add(identity)
                y=event(a,b,ops,flags)
                positives+=y
                score=lambda x: 4 if flags[3] and x==0 else x.bit_count()
                keys=((),(max(score(a),score(b)),),(a,b),(a,b,ops[0]),identity)
                for i,k in enumerate(keys): groups[i][k][y]+=1
    if len(seen)!=1024: raise AssertionError('missing')
    output=[]
    for g in groups:
        risk=sum((Fraction(v[0]*v[1],v[0]+v[1]) for v in g.values()),Fraction(0))/1024
        output.append(dict(risk=str(risk),groups=len(g),
                           mixed_groups=sum(v[0]>0 and v[1]>0 for v in g.values())))
    return positives,output

def verify(receipt):
    if receipt.get('evidence')!='E1' or receipt.get('R073')!='FROZEN' or receipt.get('PESEN_v0_1')!='FROZEN': raise AssertionError('scope')
    if receipt.get('all_atoms')!=9216 or receipt.get('exact_risks')!=45: raise AssertionError('coverage')
    results=receipt.get('results',[])
    if [r.get('world') for r in results]!=list(CONFIG): raise AssertionError('world order or duplicate')
    for row in results:
        if row.get('source_atoms')!=1024: raise AssertionError('source count')
        positive,values=oracle(row['world'])
        if row.get('global_peak_positive')!=positive: raise AssertionError('target count')
        for key,actual in zip(('F0','FB','FP','FPC','FF'),values):
            if row.get(key)!=actual: raise AssertionError(row['world']+' '+key)
    return 45

if __name__=='__main__':
    receipt=json.load(open(sys.argv[1],encoding='utf8'))
    print('independent exact fields:',verify(receipt))
    for case in ('duplicate','score','scope','missing'):
        changed=json.loads(json.dumps(receipt))
        if case=='duplicate': changed['results'].append(changed['results'][0])
        elif case=='score': changed['results'][0]['F0']['risk']='999'
        elif case=='scope': changed['evidence']='E2'
        elif case=='missing': changed['results'][0]['source_atoms']=1023
        try: verify(changed)
        except AssertionError: print('negative rejected:',case)
        else: raise AssertionError('false acceptance '+case)
