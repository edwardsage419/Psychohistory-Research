#!/usr/bin/env python3
"""R297 S93 exact finite-horizon oracle-regret audit of frozen E1 Q-learning states.

Usage: python research/validation/r297_s93_finite_policy_regret_20261031.py --emit
       python research/validation/r297_s93_finite_policy_regret_20261031.py --check
       python research/validation/r297_s93_finite_policy_regret_20261031.py --test
"""
from __future__ import annotations
import argparse, csv, hashlib, io, itertools, json, unittest
from collections import defaultdict
from fractions import Fraction as F
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT/'R297/R297_ALL_120_ORIGINAL_Q_LEARNING_Q_VECTOR_SOURCES.csv'
OUT = ROOT/'validation/R297_S93_ALL_120_FINITE_POLICY_REGRET_ROWS.csv'
RES = ROOT/'validation/R297_S93_EXACT_POLICY_REGRET_RESULTS.json'
EXPECTED_SHA = 'da5f8af83a4ab28421732e0e6b365b6c9fd99f8de2c85de5270d3a0470cecbc6'
GAMMAS=(F(0),F(1,2),F(1)); ALPHAS=(F(1,2),F(1))
COV=('FULL','GOOD_MISSING'); BACK=('OFF_POLICY_MAX','BEHAVIOR_BAD')
COLS=('world','gamma','alpha','coverage','backup_rule','epoch','Q_S0_SAFE','Q_S0_EXPLORE','chosen_S0','oracle_best_S0','Q_gap','regret','error')

def expected_worlds():
    return tuple(itertools.product(GAMMAS,ALPHAS,COV,BACK))

def wid(g,a,c,b):return f'gamma={g}|alpha={a}|coverage={c}|bootstrap={b}'

def load_rows(raw:bytes):
    if hashlib.sha256(raw).hexdigest()!=EXPECTED_SHA:raise ValueError('pinned original source SHA mismatch')
    rows=list(csv.DictReader(io.StringIO(raw.decode('utf-8'))))
    if len(rows)!=120:raise ValueError('source count')
    expected={(wid(*args),t) for args in expected_worlds() for t in range(5)}
    keys=[(r['world'],int(r['epoch'])) for r in rows]
    if len(set(keys))!=120 or set(keys)!=expected:raise ValueError('duplicate/missing source key')
    return rows

def compute(rows):
    keys=[(r['world'],int(r['epoch'])) for r in rows]
    expected={(wid(*args),t) for args in expected_worlds() for t in range(5)}
    if len(keys)!=120 or len(set(keys))!=120 or set(keys)!=expected:
        raise ValueError('incomplete or duplicate source coverage')
    indexed={(r['world'],int(r['epoch'])):r for r in rows}
    detail=[]; summaries=[]
    for g,a,c,b in expected_worlds():
        world=wid(g,a,c,b); qsafe=qexplore=qgood=qbad=F(0); values=[]
        for t in range(5):
            row=indexed[world,t]
            if (F(row['gamma']),F(row['alpha']),row['coverage'],row['backup_rule'])!=(g,a,c,b):raise ValueError('world factor mismatch')
            if t:
                if c=='FULL':qgood+=a*(F(3)-qgood)
                qbad+=a*(F(0)-qbad)
                qsafe+=a*(F(1)-qsafe)
                target=g*(max(qgood,qbad) if b=='OFF_POLICY_MAX' else qbad)
                qexplore+=a*(target-qexplore)
            else:target=F(0)
            for field,v in {'Q_S0_SAFE':qsafe,'Q_S0_EXPLORE':qexplore,'Q_S1_GOOD':qgood,'Q_S1_BAD':qbad,'target_S0_EXPLORE':target,'oracle_Qstar_S0_SAFE':F(1),'oracle_Qstar_S0_EXPLORE':3*g}.items():
                if F(row[field])!=v:raise ValueError(f'original recurrence/oracle mismatch {world} {t} {field}')
            chosen='EXPLORE' if qexplore>qsafe else 'SAFE'
            oracle='EXPLORE' if 3*g>1 else 'SAFE'
            if row['chosen_S0']!=chosen or row['oracle_best_S0']!=oracle or row['oracle_action_agreement']!=str(chosen==oracle):raise ValueError('action/oracle mismatch')
            regret=max(F(1),3*g)-(F(1) if chosen=='SAFE' else 3*g)
            if regret<0:raise ValueError('negative regret')
            d={'world':world,'gamma':str(g),'alpha':str(a),'coverage':c,'backup_rule':b,'epoch':t,'Q_S0_SAFE':str(qsafe),'Q_S0_EXPLORE':str(qexplore),'chosen_S0':chosen,'oracle_best_S0':oracle,'Q_gap':str(qexplore-qsafe),'regret':str(regret),'error':int(regret>0)}
            detail.append(d);values.append(d)
        correct=[r['error']==0 for r in values]
        first=next((t for t in range(5) if correct[t]),None)
        sustained=next((t for t in range(5) if all(correct[t:])),None)
        summaries.append({'world':world,'gamma':str(g),'alpha':str(a),'coverage':c,'backup_rule':b,'error_epochs_0_4':sum(r['error'] for r in values),'regret_epochs_0_4':str(sum((F(r['regret']) for r in values),F(0))),'regret_epochs_1_4':str(sum((F(r['regret']) for r in values[1:]),F(0))),'first_correct_epoch':first if first is not None else 'NONE','sustained_correct_epoch':sustained if sustained is not None else 'NONE','final_error':values[-1]['error']})
    if len(detail)!=120 or len(summaries)!=24 or sum(r['final_error'] for r in summaries)!=12:raise ValueError('R297 original final split mismatch')
    by_epoch=[]
    for t in range(5):
        s=[r for r in detail if r['epoch']==t]
        by_epoch.append({'epoch':t,'world_count':len(s),'error_worlds':sum(r['error'] for r in s),'total_regret':str(sum((F(r['regret']) for r in s),F(0)))})
    res={'research_id':'R297','extension':'S93-v1','evidence':'E1_ARTIFICIAL_ONLY','original_csv_sha256':EXPECTED_SHA,'original_source_rows':120,'world_count':24,'epochs':5,'human_E2':0,'historical_E3':0,'R073':'FROZEN','PESEN_v0_1':'FROZEN','objective':'unrestricted_continuation_oracle_counterfactual_not_fixed_BAD_behavioral_value','worlds':summaries,'by_epoch':by_epoch,'total_regret_epochs_0_4':str(sum((F(r['regret']) for r in detail),F(0))),'total_regret_epochs_1_4':str(sum((F(r['regret']) for r in detail if r['epoch']>0),F(0)))}
    return detail,res

def csv_bytes(rows):
    out=io.StringIO(newline='');w=csv.DictWriter(out,fieldnames=COLS,lineterminator='\n');w.writeheader();w.writerows(rows);return out.getvalue().encode('utf-8')

def json_bytes(result):return (json.dumps(result,indent=2,ensure_ascii=False)+'\n').encode('utf-8')

def main(mode):
    rows=load_rows(SRC.read_bytes());details,result=compute(rows)
    cb=csv_bytes(details);jb=json_bytes(result)
    if mode=='emit':OUT.write_bytes(cb);RES.write_bytes(jb)
    if mode=='check':
        if OUT.read_bytes()!=cb or RES.read_bytes()!=jb:raise ValueError('persisted S93 output mismatch')
    print(json.dumps({'status':'PASS','mode':mode,'rows':len(details),'worlds':len(result['worlds']),'csv_sha256':hashlib.sha256(cb).hexdigest(),'json_sha256':hashlib.sha256(jb).hexdigest(),'by_epoch':result['by_epoch'],'total_regret_epochs_0_4':result['total_regret_epochs_0_4']}))

class Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.raw=SRC.read_bytes();cls.rows=load_rows(cls.raw)
    def test_original_identity(self):self.assertEqual(hashlib.sha256(self.raw).hexdigest(),EXPECTED_SHA)
    def test_grid(self):self.assertEqual(len(self.rows),120)
    def test_recurrence(self):self.assertEqual(len(compute(self.rows)[1]['worlds']),24)
    def test_sha_reject(self):
        with self.assertRaises(ValueError):load_rows(self.raw+b'\n')
    def test_duplicate_reject(self):
        a=self.rows.copy();a[-1]=a[0]
        with self.assertRaises(ValueError):compute(a)
    def test_missing_reject(self):
        with self.assertRaises(ValueError):compute(self.rows[:-1])
    def test_action_reject(self):
        a=[dict(r) for r in self.rows];a[6]['chosen_S0']='EXPLORE'
        with self.assertRaises(ValueError):compute(a)
    def test_q_reject(self):
        a=[dict(r) for r in self.rows];a[1]['Q_S0_SAFE']='100'
        with self.assertRaises(ValueError):compute(a)
    def test_oracle_reject(self):
        a=[dict(r) for r in self.rows];a[1]['oracle_Qstar_S0_EXPLORE']='99'
        with self.assertRaises(ValueError):compute(a)

if __name__=='__main__':
    p=argparse.ArgumentParser();g=p.add_mutually_exclusive_group(required=True)
    for n in ('emit','check','test'):g.add_argument('--'+n,action='store_true')
    a=p.parse_args()
    if a.test:unittest.main(argv=['S93'],verbosity=1)
    else:main('emit' if a.emit else 'check')
