#!/usr/bin/env python3
"""R262 S58 independent table-based exact oracle and negative controls."""
import argparse,itertools,json
from collections import Counter,defaultdict
from fractions import Fraction
from pathlib import Path
TABLES={'ABSORB_ZERO':'00000000','ABSORB_ONE':'11111111','IDENTITY':'11001100','SHIFT_RIGHT':'10101010','SHIFT_LEFT':'11110000','XOR_NEIGHBORS':'01011010','XOR_THREE':'10010110','RULE30':'00011110','RULE110':'01101110'}
PATTERNS=['111','110','101','100','011','010','001','000']
FEATURES=['F0','F1','F01','Ffull'];TARGETS=['Y_cell','Y_macro']
def table_step(state,world):
    table=dict(zip(PATTERNS,TABLES[world]))
    return tuple(int(table[''.join(str(state[(j+d)%7]) for d in (-1,0,1))]) for j in range(7))
def oracle():
    out=[]
    for world in TABLES:
        counts={t:{f:defaultdict(lambda:[0,0]) for f in FEATURES} for t in TARGETS}
        for bits in itertools.product((0,1),repeat=7):
            next_state=table_step(bits,world)
            future=table_step(next_state,world)
            keys={'F0':(), 'F1':(sum(next_state),),'F01':(sum(bits),sum(next_state)),'Ffull':next_state}
            labels={'Y_cell':future[0],'Y_macro':int(sum(future)>=4)}
            for t in TARGETS:
                for f in FEATURES:
                    v=counts[t][f][keys[f]];v[0]+=labels[t];v[1]+=1
        for t in TARGETS:
            for f in FEATURES:
                groups=counts[t][f]
                score=sum((Fraction(v[0]*(v[1]-v[0]),128*v[1]) for v in groups.values()),Fraction(0))
                out.append({'world':world,'target':t,'feature':f,'risk':str(score),'groups':len(groups)})
    return out
def verify(data):
    if data.get('evidence')!='E1_ARTIFICIAL' or data.get('new_E2')!=0 or data.get('new_E3')!=0 or data.get('R073')!='FROZEN' or data.get('PESEN_v0_1')!='FROZEN':raise ValueError('evidence scope changed')
    rows=data.get('risk_rows')
    if not isinstance(rows,list) or len(rows)!=72:raise ValueError('incomplete risk rows')
    actual={}
    for r in rows:
        if set(r)!={'world','target','feature','risk','groups'}:raise ValueError('unexpected risk schema')
        k=(r['world'],r['target'],r['feature'])
        if k in actual:raise ValueError('duplicate score key')
        actual[k]=(Fraction(r['risk']),r['groups'])
    expected={(r['world'],r['target'],r['feature']):(Fraction(r['risk']),r['groups']) for r in oracle()}
    if actual!=expected:raise ValueError('score or coverage mismatch')
    return len(expected)
def negatives(data):
    mutations=[]
    def duplicate(z):z['risk_rows'][1]=dict(z['risk_rows'][0])
    def tamper(z):z['risk_rows'][0]['risk']='999'
    def upgrade(z):z['evidence']='E2_HUMAN'
    def missing(z):z['risk_rows'].pop()
    for f in (duplicate,tamper,upgrade,missing):
        z=json.loads(json.dumps(data));f(z)
        try:verify(z)
        except (ValueError,KeyError,TypeError,ZeroDivisionError):mutations.append('REJECTED')
        else:raise AssertionError('negative control accepted')
    return mutations
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--receipt',required=True);a=ap.parse_args()
    data=json.loads(Path(a.receipt).read_text(encoding='utf-8'))
    print(json.dumps({'exact_comparisons':verify(data),'negative_controls':negatives(data),'scope':'NONBLIND_ORIGINAL_R262_RESULT_BLIND_S58_INTERNAL_E1'}))
