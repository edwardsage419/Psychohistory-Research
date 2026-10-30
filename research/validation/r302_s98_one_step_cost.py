#!/usr/bin/env python3
"""R302 S98: exact finite artificial posterior one-step opportunity costs."""
from __future__ import annotations
import argparse,csv,hashlib,itertools,json,math,unittest
from fractions import Fraction as F
from pathlib import Path

ROOT=Path(__file__).resolve().parent
WORLDS=list(itertools.product(range(3),repeat=4))
COLS=('world','A_success','A_failure','B_success','B_failure','posterior_mean_A','posterior_mean_B','thompson_prob_A','greedy_choice','greedy_reward','thompson_reward','uniform_reward','thompson_cost','uniform_cost')

def beta(a,b):
    return F(math.factorial(a-1)*math.factorial(b-1),math.factorial(a+b-1))

def superiority(a,b,c,d):
    n=c+d-1
    return sum((F(math.comb(n,j))*beta(a+j,b+n-j)/beta(a,b) for j in range(c,n+1)),F(0))

def evaluate(w):
    sa,fa,sb,fb=w
    a,b,c,d=sa+1,fa+1,sb+1,fb+1
    ma,mb=F(a,a+b),F(c,c+d)
    p=superiority(a,b,c,d)
    greedy=max(ma,mb)
    ts=p*ma+(1-p)*mb
    uniform=(ma+mb)/2
    result=dict(zip(COLS,(f'A={sa},{fa}|B={sb},{fb}',sa,fa,sb,fb,ma,mb,p,'A' if ma>=mb else 'B',greedy,ts,uniform,greedy-ts,greedy-uniform)))
    assert F(0)<p<F(1)
    assert result['thompson_cost']>=0 and result['uniform_cost']>=0
    return result

def rows():return [evaluate(w) for w in WORLDS]

def summarize(rs):
    costs=[r['thompson_cost'] for r in rs]
    maximum=max(costs)
    return {'scope':'E1_ARTIFICIAL_POSTERIOR_ONE_STEP_ONLY','worlds':len(rs),
        'mean_thompson_cost':str(sum(costs,F(0))/len(rs)),
        'mean_uniform_cost':str(sum((r['uniform_cost'] for r in rs),F(0))/len(rs)),
        'positive_thompson_cost_worlds':sum(x>0 for x in costs),
        'zero_thompson_cost_worlds':sum(x==0 for x in costs),
        'max_thompson_cost':str(maximum),
        'max_cost_worlds':[r['world'] for r in rs if r['thompson_cost']==maximum],
        'posterior_mean_tie_worlds':sum(r['posterior_mean_A']==r['posterior_mean_B'] for r in rs),
        'R073':'FROZEN','PESEN_v0_1':'FROZEN','new_human_E2':0,'new_historical_E3':0,
        'external_independent_replication':'NOT_RUN'}

def verify(rs):
    assert len(rs)==81 and len({r['world'] for r in rs})==81
    lookup={w:rs[i] for i,w in enumerate(WORLDS)}
    for w in WORLDS:
        r=lookup[w];rev=lookup[(w[2],w[3],w[0],w[1])]
        assert r['thompson_prob_A']+rev['thompson_prob_A']==1
        assert r['thompson_reward']==rev['thompson_reward']
        assert r['thompson_cost']==rev['thompson_cost']
        assert r['greedy_reward']>=r['thompson_reward']
        assert r['greedy_reward']>=r['uniform_reward']
        assert (r['thompson_cost']==0)==(r['posterior_mean_A']==r['posterior_mean_B'])
    assert lookup[(0,0,0,0)]['thompson_cost']==0
    assert lookup[(1,0,0,0)]['thompson_cost']==F(1,18)
    assert lookup[(2,0,0,2)]['thompson_cost']==F(1,40)
    return True

def emit(output):
    output.mkdir(parents=True,exist_ok=True)
    rs=rows();verify(rs)
    csvpath=output/'R302_S98_ALL_81_POSTERIOR_ONE_STEP_WORLDS.csv'
    with csvpath.open('w',encoding='utf-8',newline='') as f:
        wr=csv.DictWriter(f,fieldnames=COLS,lineterminator='\n');wr.writeheader()
        for row in rs:wr.writerow({k:str(row[k]) for k in COLS})
    result=summarize(rs)
    jpath=output/'R302_S98_EXACT_POSTERIOR_ONE_STEP_RESULTS.json'
    jpath.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    receipt={'csv_sha256':hashlib.sha256(csvpath.read_bytes()).hexdigest(),
             'json_sha256':hashlib.sha256(jpath.read_bytes()).hexdigest(),
             'worlds':81,'science':'E1_ONLY','external_replication':'NOT_RUN'}
    (output/'R302_S98_RECEIPT.json').write_text(json.dumps(receipt,indent=2)+'\n',encoding='utf-8')
    return result

class Tests(unittest.TestCase):
    def test_all(self):self.assertTrue(verify(rows()))
    def test_count(self):self.assertEqual(len(rows()),81)
    def test_tie(self):self.assertEqual(evaluate((0,0,0,0))['thompson_cost'],0)
    def test_reference(self):self.assertEqual(evaluate((1,0,0,0))['thompson_cost'],F(1,18))
    def test_strong(self):self.assertEqual(evaluate((2,0,0,2))['thompson_cost'],F(1,40))

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--emit',action='store_true');parser.add_argument('--out',type=Path,default=ROOT);args=parser.parse_args()
    if args.emit:print(json.dumps(emit(args.out),ensure_ascii=False,indent=2))
    else:unittest.main(argv=['r302_s98.py'])
