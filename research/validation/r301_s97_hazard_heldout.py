#!/usr/bin/env python3
"""Frozen R301 S97 finite E1 held-out fifth-bit evaluation. Standard library only."""
import argparse, csv, hashlib, itertools, json, unittest
from fractions import Fraction as F
from pathlib import Path

HAZARDS = (F(0), F(1,4), F(1,2))
HISTORIES = tuple(''.join(z) for z in itertools.product('01',repeat=4))
COLUMNS = ('true_hazard','assumed_hazard','history','future_outcome','true_history_mass','true_conditional_one','assumed_conditional_one','joint_mass','brier_loss','weighted_brier')
FREEZE = 'b18d1cd4e149a60ebfe3732f38f09f1cb6d94e7a'

def filter_history(h, bits):
    if h not in HAZARDS or not bits or any(b not in '01' for b in bits):
        raise ValueError('outside frozen universe')
    w={1:F(1,2)}
    for t in range(2,len(bits)+1):
        new={1:h*sum(w.values(),F(0))/2}
        for l,m in w.items():
            seg=bits[t-1-l:t-1]
            p1=F(seg.count('1')+1,len(seg)+2)
            p=p1 if bits[t-1]=='1' else 1-p1
            new[l+1]=(1-h)*m*p
        w=new
    evidence=sum(w.values(),F(0))
    if evidence<=0:raise AssertionError('nonpositive evidence')
    p1=h/2+(1-h)*sum((m/evidence)*F(bits[-l:].count('1')+1,l+2) for l,m in w.items())
    return evidence,p1

def evaluate():
    rows=[]; pairs=[]
    for true in HAZARDS:
        oracle=sum((filter_history(true,s)[0]*filter_history(true,s)[1]*(1-filter_history(true,s)[1]) for s in HISTORIES),F(0))
        for assumed in HAZARDS:
            risk=F(0);regret=F(0);total=F(0)
            for s in HISTORIES:
                pm,p=filter_history(true,s)
                _,q=filter_history(assumed,s)
                regret+=pm*(q-p)**2
                for y in (0,1):
                    joint=pm*(p if y else 1-p)
                    loss=(q-y)**2
                    rows.append(dict(zip(COLUMNS,map(str,(true,assumed,s,y,pm,p,q,joint,loss,joint*loss)))))
                    risk+=joint*loss
                    total+=joint
            if total!=1 or risk-oracle!=regret:raise AssertionError('frozen Brier identity')
            if assumed==true and regret!=0:raise AssertionError('oracle mismatch')
            pairs.append(dict(true_hazard=str(true),assumed_hazard=str(assumed),risk=str(risk),oracle_risk=str(oracle),excess_risk=str(regret),constant_half_baseline='1/4'))
    if len(rows)!=288 or len(pairs)!=9:raise AssertionError('source universe')
    return rows,pairs

def emit(out):
    out=Path(out);out.mkdir(parents=True,exist_ok=True)
    rows,pairs=evaluate()
    csv_path=out/'R301_S97_ALL_288_HELDOUT_ATOMS.csv'
    with csv_path.open('w',encoding='utf8',newline='') as f:
        writer=csv.DictWriter(f,fieldnames=COLUMNS,lineterminator='\n');writer.writeheader();writer.writerows(rows)
    result=dict(research_id='R301',extension='S97',freeze_commit=FREEZE,evidence='E1_SYNTHETIC_ONLY',real_E2=0,historical_E3=0,external_team_replication=False,history_length=4,heldout_length=1,source_atoms=288,distinct_true_atoms=96,pairs=pairs,R073='FROZEN',PESEN_v0_1='FROZEN')
    json_path=out/'R301_S97_EXACT_HELDOUT_RESULTS.json'
    json_path.write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n',encoding='utf8')
    receipt=dict(freeze_commit=FREEZE,files={p.name:dict(bytes=len(p.read_bytes()),sha256=hashlib.sha256(p.read_bytes()).hexdigest()) for p in (csv_path,json_path)})
    (out/'R301_S97_RECEIPT.json').write_text(json.dumps(receipt,indent=2)+'\n',encoding='utf8')
    return receipt

class Tests(unittest.TestCase):
    def test_source_count(self):self.assertEqual(len(evaluate()[0]),288)
    def test_pair_count(self):self.assertEqual(len(evaluate()[1]),9)
    def test_unique_atoms(self):
        r,_=evaluate();self.assertEqual(len({(x['true_hazard'],x['assumed_hazard'],x['history'],x['future_outcome']) for x in r}),288)
    def test_all_masses(self):
        for h in HAZARDS:
            self.assertEqual(sum((filter_history(h,s)[0] for s in HISTORIES),F(0)),1)
    def test_r301_frozen_cases(self):
        self.assertEqual(filter_history(F(1,4),'0000'),(F(757,5120),F(1717,6056)))
        self.assertEqual(filter_history(F(1,4),'0001'),(F(323,5120),F(1301,2584)))
    def test_oracle_regret(self):
        _,p=evaluate();self.assertTrue(all(F(x['excess_risk'])>=0 for x in p));self.assertTrue(all(F(x['excess_risk'])==0 for x in p if x['true_hazard']==x['assumed_hazard']))
    def test_constant_baseline(self):
        for h in HAZARDS:
            self.assertEqual(sum((filter_history(h,s)[0] for s in HISTORIES),F(0)),1)
    def test_probability_bounds(self):
        for h in HAZARDS:
            for s in HISTORIES:
                m,p=filter_history(h,s);self.assertTrue(0<m<=1 and 0<=p<=1)

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--emit');p.add_argument('--test',action='store_true');a=p.parse_args()
    if a.test:
        suite=unittest.defaultTestLoader.loadTestsFromTestCase(Tests)
        outcome=unittest.TextTestRunner(verbosity=2).run(suite)
        if not outcome.wasSuccessful():raise SystemExit(1)
    if a.emit:print(json.dumps(emit(a.emit),indent=2))
