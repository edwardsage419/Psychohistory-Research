#!/usr/bin/env python3
"""Independent exhaustive segmentation auditor for R301 S97, imports no R code."""
import argparse,csv,hashlib,itertools,json,math,unittest,os
from fractions import Fraction as F
from pathlib import Path

H=(F(0),F(1,4),F(1,2))
S=tuple(''.join(x) for x in itertools.product('01',repeat=4))
COLS=('true_hazard','assumed_hazard','history','future_outcome','true_history_mass','true_conditional_one','assumed_conditional_one','joint_mass','brier_loss','weighted_brier')

def evidence(h,bits):
    n=len(bits)
    total=F(0)
    for boundaries in itertools.product((0,1),repeat=n-1):
        weight=h**sum(boundaries)*(1-h)**(n-1-sum(boundaries))
        start=0
        for i,change in enumerate(boundaries,1):
            if change:
                segment=bits[start:i];k=segment.count('1');weight*=F(math.factorial(k)*math.factorial(len(segment)-k),math.factorial(len(segment)+1));start=i
        segment=bits[start:];k=segment.count('1');weight*=F(math.factorial(k)*math.factorial(len(segment)-k),math.factorial(len(segment)+1))
        total+=weight
    return total

def oracle(h,bits):
    prior=evidence(h,bits)
    p=evidence(h,bits+'1')/prior
    if evidence(h,bits+'0')+evidence(h,bits+'1')!=prior:raise ValueError('partition identity')
    return prior,p

def check(rows,results):
    if len(rows)!=288 or len(results['pairs'])!=9:raise ValueError('count')
    if results['evidence']!='E1_SYNTHETIC_ONLY' or results['real_E2']!=0 or results['historical_E3']!=0:raise ValueError('evidence class')
    if results['R073']!='FROZEN' or results['PESEN_v0_1']!='FROZEN':raise ValueError('freeze')
    expected={(str(t),str(a),s,str(y)) for t in H for a in H for s in S for y in (0,1)}
    actual={(r['true_hazard'],r['assumed_hazard'],r['history'],r['future_outcome']) for r in rows}
    if len(actual)!=288 or actual!=expected:raise ValueError('universe')
    grouped={(t,a):F(0) for t in H for a in H}
    for r in rows:
        t,a,s,y=F(r['true_hazard']),F(r['assumed_hazard']),r['history'],int(r['future_outcome'])
        mass,p=oracle(t,s);_,q=oracle(a,s)
        joint=mass*(p if y else 1-p);loss=(q-y)**2
        values=(mass,p,q,joint,loss,joint*loss)
        for key,value in zip(COLS[4:],values):
            if F(r[key])!=value:raise ValueError('wrong '+key)
        grouped[t,a]+=joint*loss
    seen=set()
    for r in results['pairs']:
        t,a=F(r['true_hazard']),F(r['assumed_hazard'])
        if (t,a) in seen or (t,a) not in grouped:raise ValueError('pair universe')
        seen.add((t,a))
        oracle_risk=grouped[t,t]
        excess=sum((oracle(t,s)[0]*(oracle(a,s)[1]-oracle(t,s)[1])**2 for s in S),F(0))
        if any((F(r['risk'])!=grouped[t,a],F(r['oracle_risk'])!=oracle_risk,F(r['excess_risk'])!=excess,F(r['constant_half_baseline'])!=F(1,4))):raise ValueError('risk summary')
        if grouped[t,a]-oracle_risk!=excess:raise ValueError('proper score identity')
    if len(seen)!=9:raise ValueError('missing pair')
    return True

def load(folder):
    folder=Path(folder)
    with (folder/'R301_S97_ALL_288_HELDOUT_ATOMS.csv').open(newline='',encoding='utf8') as f:
        rd=csv.DictReader(f)
        if tuple(rd.fieldnames)!=COLS:raise ValueError('header')
        rows=list(rd)
    result=json.loads((folder/'R301_S97_EXACT_HELDOUT_RESULTS.json').read_text(encoding='utf8'))
    receipt=json.loads((folder/'R301_S97_RECEIPT.json').read_text(encoding='utf8'))
    for name,meta in receipt['files'].items():
        data=(folder/name).read_bytes()
        if len(data)!=meta['bytes'] or hashlib.sha256(data).hexdigest()!=meta['sha256']:raise ValueError('receipt')
    return rows,result

class Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.rows,cls.res=load(os.environ.get('R301_S97_FOLDER',str(Path(__file__).resolve().parents[1]/'validation')))
    def test_complete(self):self.assertTrue(check(self.rows,self.res))
    def _reject(self,rows=None,res=None):
        with self.assertRaises(ValueError):check(self.rows if rows is None else rows,self.res if res is None else res)
    def test_duplicate(self):self._reject(self.rows[:-1]+[self.rows[0].copy()])
    def test_missing(self):self._reject(self.rows[:-1])
    def test_joint_mutation(self):
        x=[r.copy() for r in self.rows];x[0]['joint_mass']='0';self._reject(x)
    def test_candidate_mutation(self):
        x=[r.copy() for r in self.rows];x[1]['assumed_conditional_one']='0';self._reject(x)
    def test_outcome_mutation(self):
        x=[r.copy() for r in self.rows];x[0]['future_outcome']='1';self._reject(x)
    def test_risk_mutation(self):
        z=json.loads(json.dumps(self.res));z['pairs'][0]['risk']='0';self._reject(res=z)
    def test_evidence_promotion(self):
        z=json.loads(json.dumps(self.res));z['real_E2']=1;self._reject(res=z)
    def test_segmentation_normalization(self):
        for h in H:
            self.assertEqual(sum((evidence(h,s) for s in S),F(0)),1)

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--folder',default=str(Path(__file__).resolve().parents[1]/'validation'));p.add_argument('--test',action='store_true');a=p.parse_args()
    if a.test:
        suite=unittest.defaultTestLoader.loadTestsFromTestCase(Tests)
        outcome=unittest.TextTestRunner(verbosity=2).run(suite)
        if not outcome.wasSuccessful():raise SystemExit(1)
    else:
        rows,res=load(a.folder);print(json.dumps({'audit':'PASS' if check(rows,res) else 'FAIL','rows':len(rows),'pairs':len(res['pairs']),'method':'independent full segmentation'},indent=2))
