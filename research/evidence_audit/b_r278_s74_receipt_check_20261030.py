#!/usr/bin/env python3
"""Independent R278 S74 analytic and persisted receipt checker; stdlib only."""
import argparse,csv,json
from fractions import Fraction as F
from math import comb
from pathlib import Path
PS=(F(1,4),F(1,2),F(3,4))
POL=('BMA_JOINT','BMA_PRODUCT','HARD_SELECT','FIXED_HALF','TRUTH_ORACLE')
ZS=('00','01','10','11')
def forecast(p,k,policy):
    w=F(3**(4-k),3**(4-k)+3**k)
    q=(3-2*w)/4
    if policy=='BMA_JOINT':return ((1+8*w)/16,F(3,16),F(3,16),(9-8*w)/16)
    if policy=='BMA_PRODUCT':return ((1-q)**2,q*(1-q),q*(1-q),q*q)
    if policy=='HARD_SELECT':q=F(1,4) if k<=2 else F(3,4)
    elif policy=='FIXED_HALF':q=F(1,2)
    elif policy=='TRUTH_ORACLE':q=p
    else:raise ValueError('policy')
    return ((1-q)**2,q*(1-q),q*(1-q),q*q)
def analytic():
    ans={}
    for p in PS:
        truth=((1-p)**2,p*(1-p),p*(1-p),p*p)
        for policy in POL:
            ans[(str(p),policy)]=sum((F(comb(4,k))*p**k*(1-p)**(4-k)*(1-2*sum((a*b for a,b in zip(forecast(p,k,policy),truth)),F(0))+sum((v*v for v in forecast(p,k,policy)),F(0))) for k in range(5)),F(0))
    return ans
def check(csvpath,jsonpath):
    data=json.loads(Path(jsonpath).read_text())
    if data['evidence']!='E1_ARTIFICIAL_NONBLIND_EXPLORATORY' or data['new_E2_predictions']!=0 or data['new_E3_predictions']!=0 or data['S74_freeze_commit']!='56b00cf6d016242e4d35c800c9b4a3162d01ea1e':raise ValueError('scope')
    expected=analytic();claims=data['world_results'];seen=set()
    if len(claims)!=15:raise ValueError('world count')
    for r in claims:
        key=(r['true_p'],r['policy'])
        if key in seen or key not in expected or F(r['expected_joint_brier'])!=expected[key]:raise ValueError('world risk')
        seen.add(key)
    if seen!=set(expected):raise ValueError('coverage')
    rows=list(csv.DictReader(open(csvpath,newline='')))
    if len(rows)!=960:raise ValueError('source count')
    keys=set();risk={key:F(0) for key in expected};mass={key:F(0) for key in expected}
    for r in rows:
        key=(r['true_p'],r['policy']);bits=r['full_sixbit']
        if key not in expected or len(bits)!=6 or set(bits)-{'0','1'} or (key,bits) in keys:raise ValueError('source identity')
        keys.add((key,bits));p=F(key[0]);k=bits[:4].count('1');y=bits[4:]
        if r['train_fourbit']!=bits[:4] or r['future_twobit']!=y or int(r['train_successes'])!=k:raise ValueError('time leakage')
        if F(r['posterior_low'])!=F(3**(4-k),3**(4-k)+3**k):raise ValueError('posterior')
        w=p**bits.count('1')*(1-p)**(6-bits.count('1'))
        if F(r['source_probability'])!=w:raise ValueError('source mass')
        pred=forecast(p,k,key[1]);stored=tuple(F(r['Q_'+z]) for z in ZS)
        if stored!=pred or sum(pred)!=1:raise ValueError('forecast')
        loss=sum(((v-int(z==y))**2 for z,v in zip(ZS,pred)),F(0))
        if F(r['joint_brier'])!=loss:raise ValueError('score')
        risk[key]+=w*loss;mass[key]+=w
    if len(keys)!=960 or any(v!=1 for v in mass.values()) or risk!=expected:raise ValueError('aggregate')
    return {'status':'PASS','worlds':15,'rows':960,'independent_route':'binomial K + four-class expected quadratic risk','scope':'E1 internal nonblind'}
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('csv');ap.add_argument('json');a=ap.parse_args()
    print(json.dumps(check(a.csv,a.json),indent=2))
