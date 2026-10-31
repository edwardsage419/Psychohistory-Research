#!/usr/bin/env python3
"""Independent nonblind E1 audit. Does not import the R320 S116 generator."""
import copy
import json
import sys
import unittest
from collections import defaultdict
from fractions import Fraction as F
from pathlib import Path

GRID=[(4,F(1,4)),(4,F(1,2)),(4,F(3,4)),(6,F(1,4)),(6,F(1,2)),(6,F(3,4))]
KEYS={'schema','prescore_freeze_commit','original_source_path','original_source_git_blob',
      'original_paths','world_count','evidence_class','human_E2','historical_E3','worlds'}
WKEYS={'world_id','upper_bound','start','p_up','eventual_upper','eventual_lower',
       'expected_eventual_steps','six_step_upper','six_step_lower','six_step_survival',
       'residual_upper','residual_lower','upper_given_survival',
       'expected_truncated_six_steps','six_step_cells'}

def gaussian(A,b):
    n=len(b)
    m=[list(row)+[b[i]] for i,row in enumerate(A)]
    for k in range(n):
        pivot=next(i for i in range(k,n) if m[i][k])
        m[k],m[pivot]=m[pivot],m[k]
        div=m[k][k]
        m[k]=[x/div for x in m[k]]
        for i in range(n):
            if i!=k:
                factor=m[i][k]
                m[i]=[v-factor*w for v,w in zip(m[i],m[k])]
    return [row[-1] for row in m]

def oracle(a,p):
    q=1-p
    n=a-1
    mat=[]
    upper_rhs=[]
    time_rhs=[]
    for state in range(1,a):
        row=[F(int(j==state)) for j in range(1,a)]
        if state>1:row[state-2]-=q
        if state<a-1:row[state]-=p
        mat.append(row)
        upper_rhs.append(p if state==a-1 else F(0))
        time_rhs.append(F(1))
    upper=gaussian(mat,upper_rhs)[a//2-1]
    mean=gaussian(mat,time_rhs)[a//2-1]
    live={a//2:F(1)}
    cells=[]
    trunc=F(0)
    for t in range(1,7):
        trunc+=sum(live.values(),F(0))
        next_live=defaultdict(F)
        hit_l=hit_u=F(0)
        for x,mass in live.items():
            for y,prob in ((x-1,q),(x+1,p)):
                if y==0:hit_l+=mass*prob
                elif y==a:hit_u+=mass*prob
                else:next_live[y]+=mass*prob
        live=dict(next_live)
        cells.append(dict(time=t,lower=str(hit_l),upper=str(hit_u)))
    survival=sum(live.values(),F(0))
    return upper,mean,cells,survival,trunc

def check(doc):
    if set(doc)!=KEYS:raise ValueError('root schema mismatch')
    if doc['schema']!='r320_s116_eventual_absorption_e1_v1':raise ValueError('schema mismatch')
    if doc['prescore_freeze_commit']!='2664cca07f969b0e753f3c70886f9ec623b84f58':raise ValueError('freeze mismatch')
    if doc['original_source_git_blob']!='ec0f3702f956e0075444d1d3efafef0bced1d7a2':raise ValueError('source mismatch')
    if doc['original_paths']!=384 or doc['world_count']!=6 or len(doc['worlds'])!=6:raise ValueError('universe mismatch')
    if doc['evidence_class']!='E1_SYNTHETIC_ONLY' or doc['human_E2']!=0 or doc['historical_E3']!=0:raise ValueError('evidence upgrade')
    for idx,(a,p) in enumerate(GRID):
        w=doc['worlds'][idx]
        if set(w)!=WKEYS:raise ValueError('world schema mismatch')
        if (w['world_id'],w['upper_bound'],w['start'],w['p_up'])!=(idx,a,a//2,str(p)):raise ValueError('world identity mismatch')
        u,mean,cells,survival,trunc=oracle(a,p)
        u6=sum((F(x['upper']) for x in cells),F(0))
        l6=sum((F(x['lower']) for x in cells),F(0))
        expected=dict(eventual_upper=u,eventual_lower=1-u,expected_eventual_steps=mean,
            six_step_upper=u6,six_step_lower=l6,six_step_survival=survival,
            residual_upper=u-u6,residual_lower=1-u-l6,
            upper_given_survival=(u-u6)/survival,expected_truncated_six_steps=trunc)
        for k,v in expected.items():
            if w[k]!=str(v):raise ValueError(f'world {idx} {k} mismatch')
        if w['six_step_cells']!=cells:raise ValueError('first hit cells mismatch')
    return True

class AuditTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.doc=json.loads(Path(sys.argv[1] if len(sys.argv)>1 else 'R320_S116_EXACT_EVENTUAL_RESULTS.json').read_text())
    def test_01_positive(self):self.assertTrue(check(self.doc))
    def mutate(self,fn):
        d=copy.deepcopy(self.doc)
        fn(d)
        with self.assertRaises(ValueError):check(d)
    def test_02_missing_world(self):self.mutate(lambda d:d['worlds'].pop())
    def test_03_duplicate_world(self):self.mutate(lambda d:d['worlds'].__setitem__(1,d['worlds'][0]))
    def test_04_p_change(self):self.mutate(lambda d:d['worlds'][0].__setitem__('p_up','1/2'))
    def test_05_eventual_up(self):self.mutate(lambda d:d['worlds'][0].__setitem__('eventual_upper','1/9'))
    def test_06_mean(self):self.mutate(lambda d:d['worlds'][1].__setitem__('expected_eventual_steps','5'))
    def test_07_survival(self):self.mutate(lambda d:d['worlds'][2].__setitem__('six_step_survival','1/2'))
    def test_08_residual(self):self.mutate(lambda d:d['worlds'][3].__setitem__('residual_upper','0'))
    def test_09_e2(self):self.mutate(lambda d:d.__setitem__('human_E2',1))
    def test_10_cell(self):self.mutate(lambda d:d['worlds'][4]['six_step_cells'][2].__setitem__('upper','1/4'))
    def test_11_original_blob(self):self.mutate(lambda d:d.__setitem__('original_source_git_blob','bad'))

if __name__=='__main__':
    path=sys.argv[1] if len(sys.argv)>1 else 'R320_S116_EXACT_EVENTUAL_RESULTS.json'
    sys.argv=[sys.argv[0],path]
    unittest.main(argv=[sys.argv[0]],verbosity=2)
