#!/usr/bin/env python3
"""B independent, nonblind closed-form R297 S93 audit; no R-script imports.
Usage: python research/evidence_audit/b_r297_s93_independent_closedform_20261031.py
"""
import csv,hashlib,itertools,json
from collections import defaultdict
from fractions import Fraction as F
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
SOURCE=ROOT/'R297/R297_ALL_120_ORIGINAL_Q_LEARNING_Q_VECTOR_SOURCES.csv'
ROWS=ROOT/'validation/R297_S93_ALL_120_FINITE_POLICY_REGRET_ROWS.csv'
RESULT=ROOT/'validation/R297_S93_EXACT_POLICY_REGRET_RESULTS.json'
PIN='da5f8af83a4ab28421732e0e6b365b6c9fd99f8de2c85de5270d3a0470cecbc6'
PARAMS=tuple(itertools.product((F(0),F(1,2),F(1)),(F(1,2),F(1)),('FULL','GOOD_MISSING'),('OFF_POLICY_MAX','BEHAVIOR_BAD')))
def wid(g,a,c,b):return f'gamma={g}|alpha={a}|coverage={c}|bootstrap={b}'

def verify(src,rows,res):
    keys=[(r['world'],int(r['epoch'])) for r in rows]
    wanted={(wid(*p),t) for p in PARAMS for t in range(5)}
    if len(rows)!=120 or len(set(keys))!=120 or set(keys)!=wanted:raise ValueError('source coverage')
    skeys=[(r['world'],int(r['epoch'])) for r in src]
    if len(src)!=120 or len(set(skeys))!=120 or set(skeys)!=wanted:raise ValueError('original coverage')
    orig={k:v for k,v in zip(skeys,src)}
    byworld=defaultdict(list)
    for row in rows:
        g,a,c,b=next((p for p in PARAMS if wid(*p)==row['world']), (None,)*4)
        if g is None:raise ValueError('unknown world')
        t=int(row['epoch']);remain=(1-a)**t
        safe=1-remain;good=3*(1-remain) if c=='FULL' else F(0)
        explore=3*g*(1-remain-a*t*remain) if c=='FULL' and b=='OFF_POLICY_MAX' else F(0)
        action='EXPLORE' if explore>safe else 'SAFE'
        oracle='EXPLORE' if 3*g>1 else 'SAFE'
        regret=max(F(1),3*g)-(F(1) if action=='SAFE' else 3*g)
        expected={'Q_S0_SAFE':str(safe),'Q_S0_EXPLORE':str(explore),'chosen_S0':action,'oracle_best_S0':oracle,'Q_gap':str(explore-safe),'regret':str(regret),'error':str(int(regret>0)),'gamma':str(g),'alpha':str(a),'coverage':c,'backup_rule':b}
        for k,v in expected.items():
            if row[k]!=v:raise ValueError(f'S93 tamper {k} {row["world"]} {t}')
        old=orig[row['world'],t]
        for k in ('Q_S0_SAFE','Q_S0_EXPLORE','chosen_S0','oracle_best_S0','gamma','alpha','coverage','backup_rule'):
            if old[k]!=row[k]:raise ValueError('original parity '+k)
        if F(old['Q_S1_GOOD'])!=good:raise ValueError('original GOOD mismatch')
        byworld[row['world']].append(row)
    if res.get('original_csv_sha256')!=PIN or res.get('evidence')!='E1_ARTIFICIAL_ONLY' or res.get('human_E2')!=0 or res.get('historical_E3')!=0 or res.get('R073')!='FROZEN' or res.get('PESEN_v0_1')!='FROZEN':raise ValueError('scope or lineage tamper')
    worlds=res.get('worlds',[])
    if len(worlds)!=24 or len(set(w['world'] for w in worlds))!=24 or set(w['world'] for w in worlds)!=set(byworld):raise ValueError('summary coverage')
    for w in worlds:
        rr=sorted(byworld[w['world']],key=lambda z:int(z['epoch']))
        correct=[int(z['error'])==0 for z in rr]
        first=next((i for i in range(5) if correct[i]),'NONE')
        sustained=next((i for i in range(5) if all(correct[i:])),'NONE')
        expected={'error_epochs_0_4':sum(int(z['error']) for z in rr),'regret_epochs_0_4':str(sum((F(z['regret']) for z in rr),F(0))),'regret_epochs_1_4':str(sum((F(z['regret']) for z in rr[1:]),F(0))),'first_correct_epoch':first,'sustained_correct_epoch':sustained,'final_error':int(rr[-1]['error'])}
        for k,v in expected.items():
            if w[k]!=v:raise ValueError('summary mismatch '+k)
    epochs=res.get('by_epoch',[])
    if len(epochs)!=5:raise ValueError('epoch coverage')
    for t,e in enumerate(epochs):
        subset=[r for r in rows if int(r['epoch'])==t]
        if e!={'epoch':t,'world_count':24,'error_worlds':sum(int(z['error']) for z in subset),'total_regret':str(sum((F(z['regret']) for z in subset),F(0)))}:raise ValueError('epoch summary mismatch')
    if res.get('total_regret_epochs_0_4')!=str(sum((F(z['regret']) for z in rows),F(0))):raise ValueError('total regret tamper')
    if res.get('total_regret_epochs_1_4')!=str(sum((F(z['regret']) for z in rows if int(z['epoch'])>0),F(0))):raise ValueError('total regret 1..4 tamper')
    return True

def main():
    if hashlib.sha256(SOURCE.read_bytes()).hexdigest()!=PIN:raise ValueError('original SHA mismatch')
    with SOURCE.open(newline='') as f:src=list(csv.DictReader(f))
    with ROWS.open(newline='') as f:rows=list(csv.DictReader(f))
    res=json.loads(RESULT.read_text())
    assert verify(src,rows,res)
    mutations=[]
    def fail(name,s,r,j):
        try:verify(s,r,j)
        except (ValueError,KeyError,TypeError):mutations.append(name);return
        raise AssertionError('false acceptance: '+name)
    def rcopy():return [dict(z) for z in rows]
    z=rcopy();z[-1]=dict(z[0]);fail('duplicate',src,z,res)
    fail('omission',src,rows[:-1],res)
    z=rcopy();z[70]['chosen_S0']='SAFE' if z[70]['chosen_S0']=='EXPLORE' else 'EXPLORE';fail('action',src,z,res)
    z=rcopy();z[1]['Q_S0_SAFE']='999';fail('Q',src,z,res)
    z=rcopy();z[1]['oracle_best_S0']='EXPLORE';fail('oracle',src,z,res)
    z=rcopy();z[80]['regret']='-1';fail('regret',src,z,res)
    j=json.loads(json.dumps(res));j['worlds'][0]['regret_epochs_0_4']='999';fail('summary',src,rows,j)
    j=json.loads(json.dumps(res));j['human_E2']=1;fail('E2 promotion',src,rows,j)
    print(json.dumps({'status':'INDEPENDENT_NONBLIND_PASS','rows':len(rows),'worlds':len(res['worlds']),'original_sha256':PIN,'mutations_rejected':len(mutations),'mutations':mutations,'regret_total':res['total_regret_epochs_0_4']}))

if __name__=='__main__':main()
