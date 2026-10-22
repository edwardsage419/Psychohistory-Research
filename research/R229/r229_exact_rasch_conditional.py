#!/usr/bin/env python3
"""R229 eight frozen finite Rasch worlds; full exact artificial CML audit."""
from __future__ import annotations
import argparse,csv,hashlib,itertools,json,unittest
from collections import defaultdict
from fractions import Fraction as F
from functools import lru_cache
from pathlib import Path
HERE=Path(__file__).resolve().parent
ZERO=F(0); ONE=F(1)
PATS=tuple(itertools.product((0,1),repeat=3))
FULL=((1,1,1),)*3
PART=((1,1,0),(1,1,0),(0,0,1))
FREEZE='93dd2e7f3dfd76342c3deaff2487edc676160a91'
WORLDS={
'BASE_RASCH':((-1,0,1),(-1,0,1),(1,1,1),False,FULL),
'SHIFT_ALIAS':((0,1,2),(0,1,2),(1,1,1),False,FULL),
'ABILITY_SPREAD_RASCH':((-2,0,2),(-1,0,1),(1,1,1),False,FULL),
'ITEM_STRETCH_RASCH':((-1,0,1),(-2,0,2),(1,1,1),False,FULL),
'TWO_PARAMETER_NONRASCH':((-1,0,1),(-1,0,1),(1,2,1),False,FULL),
'LOCAL_DEPENDENT_CLONE':((-1,0,1),(-1,0,-1),(1,1,1),True,FULL),
'ITEM_DIF_PERSON3':((-1,0,1),(-1,0,1),(1,1,1),False,FULL),
'DISCONNECTED_ITEM3':((-1,0,1),(-1,0,1),(1,1,1),False,PART)}
RASCH=('BASE_RASCH','SHIFT_ALIAS','ABILITY_SPREAD_RASCH',
'ITEM_STRETCH_RASCH','ITEM_DIF_PERSON3','DISCONNECTED_ITEM3')
def p2(x):
    v=F(2)**x
    return v/(1+v)
def diff(world,i):
    theta,b,a,clone,masks=WORLDS[world]
    return (b[0],b[1],b[2]+1) if world=='ITEM_DIF_PERSON3' and i==2 else b
def likelihood(world,i,y):
    if world not in WORLDS or i not in range(3) or y not in PATS:raise ValueError('unfrozen source')
    theta,b,a,clone,masks=WORLDS[world]
    bs=diff(world,i)
    ps=tuple(p2(a[j]*(theta[i]-bs[j])) for j in range(3))
    if clone:
        if y[2]!=y[0]:return ZERO
        return (ps[0] if y[0] else ONE-ps[0])*(ps[1] if y[1] else ONE-ps[1])
    out=ONE
    for bit,pr in zip(y,ps):out*=pr if bit else ONE-pr
    return out
def observable(pattern,mask):return tuple(x if mask[j] else -1 for j,x in enumerate(pattern))
def score(y):return sum(v for v in y if v>=0)
def key(y):return ''.join('?' if v<0 else str(v) for v in y)
@lru_cache(None)
def sources(world):
    if world not in WORLDS:raise ValueError('unknown world')
    masks=WORLDS[world][-1]
    out=[]
    for mats in itertools.product(PATS,repeat=3):
        pr=ONE
        for i in range(3):pr*=likelihood(world,i,mats[i])
        obs=tuple(observable(mats[i],masks[i]) for i in range(3))
        out.append(dict(world=world,
        original_full_nine_bit_matrix=''.join(''.join(map(str,x)) for x in mats),
        actual_observed_matrix='|'.join(key(x) for x in obs),
        observation_mask='|'.join(''.join(map(str,x)) for x in masks),
        observed_person_row_scores=''.join(str(score(x)) for x in obs),
        original_probability=pr,structural_zero=int(pr==0)))
    assert len(out)==512 and sum((x['original_probability'] for x in out),ZERO)==ONE
    return tuple(out)
def local_weights(world,i):
    result=defaultdict(F)
    mask=WORLDS[world][-1][i]
    for p in PATS:result[observable(p,mask)]+=likelihood(world,i,p)
    assert sum(result.values(),ZERO)==ONE
    return dict(result)
def source_weights(world,i):
    result=defaultdict(F)
    for x in sources(world):
        part=x['actual_observed_matrix'].split('|')[i]
        y=tuple(-1 if c=='?' else int(c) for c in part)
        result[y]+=x['original_probability']
    assert sum(result.values(),ZERO)==ONE
    return dict(result)
def conditional(weight):
    den=defaultdict(F)
    for y,p in weight.items():den[score(y)]+=p
    return {y:p/den[score(y)] for y,p in weight.items() if den[score(y)]>0}
def rasch_formula(world,i):
    theta,b,a,clone,masks=WORLDS[world]
    if clone or len(set(a))!=1:return None
    cols=[j for j,c in enumerate(masks[i]) if c]
    bs=diff(world,i)
    w={}
    for bits in itertools.product((0,1),repeat=len(cols)):
        pat=[-1]*3
        for j,v in zip(cols,bits):pat[j]=v
        k=tuple(pat)
        w[k]=F(2)**(-a[0]*sum(bs[j]*pat[j] for j in cols))
    den=defaultdict(F)
    for y,p in w.items():den[score(y)]+=p
    return {y:p/den[score(y)] for y,p in w.items()}
def observed_joint(world):
    out=defaultdict(F)
    for x in sources(world):out[x['actual_observed_matrix']]+=x['original_probability']
    return dict(sorted(out.items()))
def analytic_joint(world):
    # Independent product of three local observed marginals, not 512 matrix atoms.
    d=[local_weights(world,i) for i in range(3)]
    out={}
    for a,pa in d[0].items():
        for b,pb in d[1].items():
            for c,pc in d[2].items():out['|'.join((key(a),key(b),key(c)))]=pa*pb*pc
    return out
def odds(world,i,j,k):
    mask=WORLDS[world][-1][i]
    if not mask[j] or not mask[k]:return None
    out=local_weights(world,i)
    blank=[0 if m else -1 for m in mask]
    a=list(blank);b=list(blank)
    a[j]=1;b[k]=1
    num=out.get(tuple(a),ZERO);den=out.get(tuple(b),ZERO)
    return num/den if den>0 else None
def world_result(world):
    assert observed_joint(world)==analytic_joint(world)
    rows=sources(world)
    rr=[]
    for i in range(3):
        loc=local_weights(world,i)
        assert loc==source_weights(world,i)
        cond=conditional(loc)
        formula=rasch_formula(world,i)
        if world in RASCH:assert cond==formula
        a,b=odds(world,i,0,1),odds(world,i,1,2)
        rr.append(dict(person_index=i,observed_item_count=sum(WORLDS[world][-1][i]),
                       observed_pattern_count=len(loc),
                       Rasch_conditional_formula_matches=(formula is not None and cond==formula),
                       score_one_item0_over_item1=None if a is None else str(a),
                       score_one_item1_over_item2=None if b is None else str(b),
                       score_one_conditional_patterns={key(z):str(p) for z,p in cond.items() if score(z)==1}))
    if world=='TWO_PARAMETER_NONRASCH':assert [x['score_one_item0_over_item1'] for x in rr]==['4','2','1']
    if world=='ITEM_DIF_PERSON3':assert [x['score_one_item1_over_item2'] for x in rr]==['2','2','4']
    if world=='DISCONNECTED_ITEM3':assert rr[2]['observed_item_count']==1 and rr[2]['score_one_item1_over_item2'] is None
    return dict(world=world,complete_original_matrix_count=len(rows),
                positive_probability_sources=sum(x['original_probability']>0 for x in rows),
                original_probability_mass='1',observed_joint_support=len(observed_joint(world)),
                masked_answers_per_matrix=sum(9-sum(m) for m in WORLDS[world][-1]),
                individual_conditional_odds=rr,
                observed_matrix_probability_signature={key:str(val) for key,val in observed_joint(world).items()})
def generate():
    worlds=[world_result(w) for w in WORLDS]
    assert observed_joint('BASE_RASCH')==observed_joint('SHIFT_ALIAS')
    assert observed_joint('BASE_RASCH')!=observed_joint('ABILITY_SPREAD_RASCH')
    for i in range(3):
        assert conditional(local_weights('BASE_RASCH',i))==conditional(local_weights('ABILITY_SPREAD_RASCH',i))
    assert set(rasch_formula('DISCONNECTED_ITEM3',2).values())=={ONE}
    result=dict(research_id='R229',catalogue_id='10-003',scope='FINITE_ARTIFICIAL_E1_ONLY',
        prescore_freeze_commit=FREEZE,worlds=8,original_complete_matrix_atoms=4096,
        true_observation_alias_base_vs_shift=True,conditional_ability_invariance=True,
        disconnected_item3_conditional_nonidentification=True,
        new_real_human_E2=0,new_real_historical_E3=0,
        R073='FROZEN',PESEN_v0_1='FROZEN',world_results=worlds)
    a=HERE/'R229_ALL_4096_ORIGINAL_3X3_MATRIX_SOURCES.csv'
    with a.open('w',newline='',encoding='utf-8') as f:
        fieldnames=list(sources('BASE_RASCH')[0])
        wr=csv.DictWriter(f,fieldnames=fieldnames,lineterminator='\n');wr.writeheader()
        for w in WORLDS:
            for r in sources(w):wr.writerow({k:str(v) for k,v in r.items()})
    b=HERE/'R229_EXACT_RESULTS.json'
    b.write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
    receipt=dict(research_id='R229',catalogue_id='10-003',
      worlds=8,all_structural_matrix_source_rows=4096,
      source_sha256=hashlib.sha256(a.read_bytes()).hexdigest(),
      results_sha256=hashlib.sha256(b.read_bytes()).hexdigest(),
      independent_source_and_local_marginals_agree=True,
      original_observed_alias=True,new_real_human_E2=0,new_real_historical_E3=0)
    (HERE/'R229_FINAL_MACHINE_ACCEPTANCE.json').write_text(json.dumps(receipt,indent=2)+'\n',encoding='utf-8')
    return receipt
class Tests(unittest.TestCase):
    def test_worlds(self):self.assertEqual(len(WORLDS),8)
    def test_original_atoms(self):self.assertEqual(sum(len(sources(w)) for w in WORLDS),4096)
    def test_shift(self):self.assertEqual(observed_joint('BASE_RASCH'),observed_joint('SHIFT_ALIAS'))
    def test_spread(self):self.assertNotEqual(observed_joint('BASE_RASCH'),observed_joint('ABILITY_SPREAD_RASCH'))
    def test_base_odds(self):self.assertEqual(odds('BASE_RASCH',0,0,1),2)
    def test_stretch_odds(self):self.assertEqual(odds('ITEM_STRETCH_RASCH',0,0,1),4)
    def test_twopl_odds(self):self.assertEqual([str(odds('TWO_PARAMETER_NONRASCH',i,0,1)) for i in range(3)],['4','2','1'])
    def test_dif_odds(self):self.assertEqual(odds('ITEM_DIF_PERSON3',2,1,2),4)
    def test_clone_zeros(self):self.assertEqual(sum(x['original_probability']>0 for x in sources('LOCAL_DEPENDENT_CLONE')),64)
    def test_disconnect_mask(self):self.assertEqual(sum(sum(m) for m in WORLDS['DISCONNECTED_ITEM3'][-1]),5)
    def test_no_odds(self):self.assertIsNone(odds('DISCONNECTED_ITEM3',2,1,2))
    def test_invalid(self):
        with self.assertRaises(ValueError):sources('missing')
def _case(world,kind):
    def t(self):
        s=sources(world)
        if kind=='mass':self.assertEqual(sum((r['original_probability'] for r in s),ZERO),ONE)
        elif kind=='size':self.assertEqual(len(s),512)
        elif kind=='unique':self.assertEqual(len({r['original_full_nine_bit_matrix'] for r in s}),512)
        elif kind=='source_vs_local':
            for i in range(3):self.assertEqual(source_weights(world,i),local_weights(world,i))
        elif kind=='joint':self.assertEqual(observed_joint(world),analytic_joint(world))
        elif kind=='conditional':
            if world in RASCH:
                for i in range(3):self.assertEqual(conditional(local_weights(world,i)),rasch_formula(world,i))
            else:self.assertIsNone(rasch_formula(world,0))
        elif kind=='positive':self.assertGreater(sum(r['original_probability']>0 for r in s),0)
        else:raise AssertionError('unknown test')
    return t
for _w in WORLDS:
    for _kind in ('mass','size','unique','source_vs_local','joint','conditional','positive'):
        setattr(Tests,'test_'+_w.lower()+'_'+_kind,_case(_w,_kind))
if __name__=='__main__':
    p=argparse.ArgumentParser()
    g=p.add_mutually_exclusive_group(required=True)
    g.add_argument('--test',action='store_true');g.add_argument('--emit',action='store_true')
    args=p.parse_args()
    if args.test:unittest.main(argv=['r229'],verbosity=2)
    else:print(json.dumps(generate(),indent=2))
