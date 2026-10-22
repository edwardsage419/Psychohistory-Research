#!/usr/bin/env python3
"""R230 exact finite exploratory-factor covariance, rotations and oracle rank."""
from __future__ import annotations
import argparse,csv,hashlib,itertools,json,unittest
from collections import defaultdict
from fractions import Fraction as F
from pathlib import Path

HERE=Path(__file__).resolve().parent
ZERO=F(0);ONE=F(1)
FREEZE='63b7a6a05cfbd71bd49a59d559c8299256c3abf3'
BASE=((F(1),ZERO),(F(1),ZERO),(F(1),ZERO))
CROSS=((F(1),ZERO),(F(1),F(1)),(ZERO,F(1)))
ROT=((F(3,5),F(-4,5)),(F(4,5),F(3,5)))
WORLDS={
 'ONE_COMMON_TRAIT':(BASE,(1,1,1),'stable_shared_trait'),
 'COMMON_METHOD_ALIAS':(BASE,(1,1,1),'occasion_method_signal'),
 'TWO_FACTOR_BLOCK':(((1,0),(1,0),(0,1)),(1,1,1),'two_orthogonal_factors'),
 'CROSS_LOADING':(CROSS,(1,1,1),'cross_loading'),
 'NO_COMMON_FACTOR':(((0,0),(0,0),(0,0)),(1,1,1),'independent_error_only'),
 'BIPOLAR_LOADING':(((1,0),(-1,0),(1,0)),(1,1,1),'opposite_item_loading'),
 'ROTATED_CROSS_ALIAS':(CROSS,(1,1,1),'orthogonally_rotated_coordinates'),
 'HIGH_UNIQUENESS':(BASE,(2,2,2),'high_item_specific_noise')
}
EIGENS={
 'ONE_COMMON_TRAIT':(4,1,1),
 'COMMON_METHOD_ALIAS':(4,1,1),
 'TWO_FACTOR_BLOCK':(3,2,1),
 'CROSS_LOADING':(4,2,1),
 'NO_COMMON_FACTOR':(1,1,1),
 'BIPOLAR_LOADING':(4,1,1),
 'ROTATED_CROSS_ALIAS':(4,2,1),
 'HIGH_UNIQUENESS':(7,4,4)
}
RANK={
 'ONE_COMMON_TRAIT':1,'COMMON_METHOD_ALIAS':1,'TWO_FACTOR_BLOCK':2,
 'CROSS_LOADING':2,'NO_COMMON_FACTOR':0,'BIPOLAR_LOADING':1,
 'ROTATED_CROSS_ALIAS':2,'HIGH_UNIQUENESS':1
}
def dot(a,b):return sum((F(x)*F(y) for x,y in zip(a,b)),ZERO)
def reported_factors(world,u,v):
    if world not in WORLDS:raise ValueError('unfrozen factor world')
    if world=='ROTATED_CROSS_ALIAS':
        return (dot(ROT[0],(u,v)),dot(ROT[1],(u,v)))
    return (F(u),F(v))
def reported_loadings(world):
    if world not in WORLDS:raise ValueError('unfrozen factor world')
    load=WORLDS[world][0]
    if world=='ROTATED_CROSS_ALIAS':
        # L' = L Q^T. Q is the fixed 3/5,4/5 orthogonal rotation.
        return tuple((dot(row,ROT[0]),dot(row,ROT[1])) for row in load)
    return tuple(tuple(F(x) for x in row) for row in load)
def source_row(world,u,v,e1,e2,e3):
    if world not in WORLDS or any(a not in (-1,1) for a in (u,v,e1,e2,e3)):
        raise ValueError('source outside frozen independent support')
    f=reported_factors(world,u,v)
    L=reported_loadings(world)
    amp=WORLDS[world][1]
    x=tuple(dot(L[i],f)+F(amp[i]*(e1,e2,e3)[i]) for i in range(3))
    return dict(world=world,original_U=u,original_V=v,
                independent_E1=e1,independent_E2=e2,independent_E3=e3,
                reported_factor_F1=f[0],reported_factor_F2=f[1],
                observed_X1=x[0],observed_X2=x[1],observed_X3=x[2],
                original_source_probability=F(1,32))
def sources(world):
    return tuple(source_row(world,*bits) for bits in itertools.product((-1,1),repeat=5))
def source_covariance(world):
    data=sources(world)
    if len(data)!=32 or sum((r['original_source_probability'] for r in data),ZERO)!=ONE:
        raise AssertionError('source universe incomplete')
    mean=tuple(sum((r['original_source_probability']*r['observed_X'+str(j+1)] for r in data),ZERO) for j in range(3))
    cov=tuple(tuple(sum((r['original_source_probability']*
                  (r['observed_X'+str(i+1)]-mean[i])*(r['observed_X'+str(j+1)]-mean[j]) for r in data),ZERO)
                  for j in range(3)) for i in range(3))
    return mean,cov
def theoretical_covariance(world):
    L=reported_loadings(world)
    amp=WORLDS[world][1]
    return tuple(tuple(dot(L[i],L[j])+(F(amp[i]**2) if i==j else ZERO) for j in range(3)) for i in range(3))
def matrix_subtract_noise(cov,world):
    amp=WORLDS[world][1]
    return tuple(tuple(cov[i][j]-(F(amp[i]**2) if i==j else ZERO) for j in range(3)) for i in range(3))
def exact_rank(matrix):
    a=[list(row) for row in matrix]
    rank=0
    for j in range(len(a[0])):
        found=next((i for i in range(rank,len(a)) if a[i][j]!=0),None)
        if found is None:continue
        a[rank],a[found]=a[found],a[rank]
        pivot=a[rank][j]
        for k in range(j,len(a[rank])):a[rank][k]/=pivot
        for i in range(len(a)):
            if i!=rank:
                f=a[i][j]
                for k in range(j,len(a[i])):a[i][k]-=f*a[rank][k]
        rank+=1
        if rank==len(a):break
    return rank
def det3(a):
    return a[0][0]*(a[1][1]*a[2][2]-a[1][2]*a[2][1])-a[0][1]*(a[1][0]*a[2][2]-a[1][2]*a[2][0])+a[0][2]*(a[1][0]*a[2][1]-a[1][1]*a[2][0])
def spectral_invariants(matrix):
    tr=sum((matrix[i][i] for i in range(3)),ZERO)
    s2=sum((matrix[i][i]*matrix[j][j]-matrix[i][j]*matrix[j][i] for i in range(3) for j in range(i+1,3)),ZERO)
    return (tr,s2,det3(matrix))
def eigen_certificate(world,cov):
    roots=tuple(F(v) for v in EIGENS[world])
    assert spectral_invariants(cov)==(sum(roots,ZERO),
         roots[0]*roots[1]+roots[0]*roots[2]+roots[1]*roots[2],
         roots[0]*roots[1]*roots[2])
    return roots
def observed_joint(world):
    result=defaultdict(F)
    for row in sources(world):
        key=tuple(row['observed_X'+str(j+1)] for j in range(3))
        result[key]+=row['original_source_probability']
    return dict(sorted(result.items()))
def rotation_identity():
    assert all(dot(ROT[i],ROT[j])==(ONE if i==j else ZERO) for i in range(2) for j in range(2))
    for u,v in itertools.product((-1,1),repeat=2):
        a=reported_factors('ROTATED_CROSS_ALIAS',u,v)
        b=reported_loadings('ROTATED_CROSS_ALIAS')
        actual=[dot(row,a) for row in b]
        expected=[dot(row,(F(u),F(v))) for row in CROSS]
        assert actual==expected
    return True
def world_result(world):
    mean,cov=source_covariance(world)
    independent=theoretical_covariance(world)
    if cov!=independent:raise AssertionError('source and loading covariance differ')
    common=matrix_subtract_noise(cov,world)
    if exact_rank(common)!=RANK[world]:raise AssertionError('oracle common variance rank mismatch')
    roots=eigen_certificate(world,cov)
    d=WORLDS[world][1]
    return dict(world=world,original_source_atoms=32,original_probability_sum='1',
        factor_interpretation=WORLDS[world][2],
        reported_loadings=[[str(v) for v in row] for row in reported_loadings(world)],
        original_item_noise_amplitudes=list(d),
        expected_observable_scores_mean=[str(m) for m in mean],
        exact_population_covariance=[[str(x) for x in row] for row in cov],
        exact_eigenvalue_characteristic_polynomial_roots=[str(r) for r in roots],
        exact_eigenvalue_invariant_triplet=[str(v) for v in spectral_invariants(cov)],
        oracle_common_component_covariance=[[str(x) for x in row] for row in common],
        oracle_common_component_rank=exact_rank(common),
        oracle_item_communality_fraction=[str(common[i][i]/cov[i][i]) for i in range(3)],
        full_observable_joint={','.join(str(v) for v in key):str(mass) for key,mass in observed_joint(world).items()})
def generate():
    rotation_identity()
    if observed_joint('ONE_COMMON_TRAIT')!=observed_joint('COMMON_METHOD_ALIAS'):
        raise AssertionError('factor semantic alias broken')
    if observed_joint('CROSS_LOADING')!=observed_joint('ROTATED_CROSS_ALIAS'):
        raise AssertionError('rotation equivalence broken')
    out=dict(research_id='R230',original_catalogue_id='10-004',
        prescore_freeze_commit=FREEZE,scope='FINITE_ARTIFICIAL_E1_ONLY',
        original_worlds=8,original_full_source_rows=256,
        exact_two_full_observational_alias_pairs_verified=True,
        rotated_factor_covariance_identity=True,
        new_real_human_E2=0,new_real_historical_E3=0,
        R073='FROZEN',PESEN_v0_1='FROZEN',
        world_results=[world_result(w) for w in WORLDS])
    a=HERE/'R230_ALL_256_ORIGINAL_FACTOR_EXOGENOUS_SOURCES.csv'
    fields=list(source_row('ONE_COMMON_TRAIT',1,1,1,1,1))
    with a.open('w',newline='',encoding='utf-8') as f:
        wr=csv.DictWriter(f,fieldnames=fields,lineterminator='\n')
        wr.writeheader()
        for w in WORLDS:
            for row in sources(w):wr.writerow({k:str(v) for k,v in row.items()})
    b=HERE/'R230_EXACT_RESULTS.json'
    b.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    rec=dict(research_id='R230',original_catalogue_id='10-004',
        worlds=8,full_original_source_atoms=256,
        source_sha256=hashlib.sha256(a.read_bytes()).hexdigest(),
        results_sha256=hashlib.sha256(b.read_bytes()).hexdigest(),
        source_vs_load_covariance_exact=True,exact_polynomial_spectral_certificates=True,
        orthogonal_rotation_alias_certified=True,
        new_real_human_E2=0,new_real_historical_E3=0)
    (HERE/'R230_FINAL_MACHINE_ACCEPTANCE.json').write_text(json.dumps(rec,indent=2)+'\n',encoding='utf-8')
    return rec
class Tests(unittest.TestCase):
    def test_eight_worlds(self):self.assertEqual(len(WORLDS),8)
    def test_original_count(self):self.assertEqual(sum(len(sources(w)) for w in WORLDS),256)
    def test_method_alias(self):self.assertEqual(observed_joint('ONE_COMMON_TRAIT'),observed_joint('COMMON_METHOD_ALIAS'))
    def test_rotation_alias(self):self.assertEqual(observed_joint('CROSS_LOADING'),observed_joint('ROTATED_CROSS_ALIAS'))
    def test_rotation_sourcewise(self):self.assertTrue(rotation_identity())
    def test_one_eigens(self):self.assertEqual(eigen_certificate('ONE_COMMON_TRAIT',source_covariance('ONE_COMMON_TRAIT')[1]),(4,1,1))
    def test_two_eigens(self):self.assertEqual(eigen_certificate('TWO_FACTOR_BLOCK',source_covariance('TWO_FACTOR_BLOCK')[1]),(3,2,1))
    def test_cross_eigens(self):self.assertEqual(eigen_certificate('CROSS_LOADING',source_covariance('CROSS_LOADING')[1]),(4,2,1))
    def test_noise(self):self.assertEqual(eigen_certificate('HIGH_UNIQUENESS',source_covariance('HIGH_UNIQUENESS')[1]),(7,4,4))
    def test_rank_zero(self):self.assertEqual(world_result('NO_COMMON_FACTOR')['oracle_common_component_rank'],0)
    def test_communality(self):
        self.assertEqual(world_result('ONE_COMMON_TRAIT')['oracle_item_communality_fraction'],['1/2']*3)
        self.assertEqual(world_result('HIGH_UNIQUENESS')['oracle_item_communality_fraction'],['1/5']*3)
    def test_bad_world(self):
        with self.assertRaises(ValueError):source_row('NOPE',1,1,1,1,1)
def _case(world,kind):
    def t(self):
        ss=sources(world)
        if kind=='mass':self.assertEqual(sum((s['original_source_probability'] for s in ss),ZERO),ONE)
        elif kind=='source_keys':self.assertEqual(len({(s['original_U'],s['original_V'],s['independent_E1'],s['independent_E2'],s['independent_E3']) for s in ss}),32)
        elif kind=='mean_zero':self.assertEqual(source_covariance(world)[0],(ZERO,)*3)
        elif kind=='cov':self.assertEqual(source_covariance(world)[1],theoretical_covariance(world))
        elif kind=='spectrum':self.assertEqual(tuple(map(int,eigen_certificate(world,source_covariance(world)[1]))),EIGENS[world])
        elif kind=='rank':self.assertEqual(exact_rank(matrix_subtract_noise(source_covariance(world)[1],world)),RANK[world])
        else:raise AssertionError('bad test')
    return t
for _world in WORLDS:
    for _kind in ('mass','source_keys','mean_zero','cov','spectrum','rank'):
        setattr(Tests,'test_'+_world.lower()+'_'+_kind,_case(_world,_kind))
if __name__=='__main__':
    parser=argparse.ArgumentParser()
    group=parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--test',action='store_true')
    group.add_argument('--emit',action='store_true')
    opts=parser.parse_args()
    if opts.test:unittest.main(argv=['r230'],verbosity=2)
    else:print(json.dumps(generate(),indent=2))
