#!/usr/bin/env python3
"""R254 3x3 finite random signed symmetric adjacency matrices, exact spectra.
Six fair edge bits, three fair vector bits and four time labels: 2048 full
source types per frozen world, 18432 total. Never infer infinite-dimensional
random-matrix laws or real network diffusion from these artificial sources.
"""
from __future__ import annotations
import argparse,csv,hashlib,itertools,json,unittest
from fractions import Fraction as F
from functools import lru_cache
from collections import defaultdict
from pathlib import Path
HERE=Path(__file__).resolve().parent
FREEZE="74740c27108b2a203c5860824f6862a0866d69d3"
ZERO=F(0);ONE=F(1)
EDGE_NAMES=("01","02","12")
EDGE_BITS=tuple(itertools.product((0,1),repeat=6))
SEEDS=tuple(itertools.product((0,1),repeat=3))
TIMES=(0,1,2,3)
CONFIG={
 "EMPTY_P0":("ALL",F(0),1),
 "EDGE_01_P1":("01",F(1),1),
 "PATH_01_12_P1":("01_12",F(1),1),
 "TRIANGLE_P1":("ALL",F(1),1),
 "ER_TRIANGLE_P_QUARTER":("ALL",F(1,4),1),
 "ER_TRIANGLE_P_HALF":("ALL",F(1,2),1),
 "ER_TRIANGLE_P_THREE_QUARTER":("ALL",F(3,4),1),
 "SIGNED_ER_TRIANGLE_P_HALF":("ALL",F(1,2),-1),
 "SIGNED_TRIANGLE_P1":("ALL",F(1),-1)
}
WORLDS=tuple(CONFIG)
def check(w):
    if w not in CONFIG:raise ValueError("unfrozen random matrix world")
def enabled(w,e):
    topo=CONFIG[w][0]
    return topo=="ALL" or (topo=="01" and e=="01") or (topo=="01_12" and e in ("01","12"))
def edges_from_original(w,bits):
    check(w)
    if len(bits)!=6 or any(x not in (0,1) for x in bits):
        raise ValueError("six original fair edge bits required")
    _,p,sign=CONFIG[w]
    a=[]
    for i,e in enumerate(EDGE_NAMES):
        r=2*bits[2*i]+bits[2*i+1]
        open_edge=int(enabled(w,e) and F(r)<4*p)
        a.append(open_edge*(sign if e=="12" else 1))
    return tuple(a)
def matrix_from_edges(e):
    a,b,c=e
    return ((0,a,b),(a,0,c),(b,c,0))
def mv(A,v):
    return tuple(sum(A[i][k]*v[k] for k in range(3)) for i in range(3))
def matrix_product(A,B):
    return tuple(tuple(sum(A[i][k]*B[k][j] for k in range(3)) for j in range(3)) for i in range(3))
def identity():
    return ((1,0,0),(0,1,0),(0,0,1))
def direct_state(e,seed,n):
    if seed not in SEEDS or n not in TIMES:raise ValueError("unfrozen seed/time")
    A=matrix_from_edges(e)
    v=seed
    for _ in range(n):v=mv(A,v)
    return v
def independent_walk_sum(e,seed,n):
    """All vertex walks expanded directly; no matvec, no recurrence."""
    if seed not in SEEDS or n not in TIMES:raise ValueError("unfrozen seed/time")
    A=matrix_from_edges(e)
    if not n:return seed
    ans=[]
    for i in range(3):
        val=0
        for walk in itertools.product(range(3),repeat=n):
            prod=A[i][walk[0]]
            for k in range(n-1):prod*=A[walk[k]][walk[k+1]]
            val+=prod*seed[walk[-1]]
        ans.append(val)
    return tuple(ans)
def determinant_three_by_three(M):
    a,b,c=M[0];d,e,f=M[1];g,h,i=M[2]
    return a*(e*i-f*h)-b*(d*i-f*g)+c*(d*h-e*g)
def char_coefficients(e):
    """det(lambda I-A)=lambda^3+c2 lambda²+c1 lambda+c0."""
    A=matrix_from_edges(e)
    trace=sum(A[i][i] for i in range(3))
    trA2=sum(A[i][j]*A[j][i] for i in range(3) for j in range(3))
    c2=-trace
    c1=(trace*trace-trA2)//2
    c0=-determinant_three_by_three(A)
    return (1,c2,c1,c0)
def exact_spectrum(e):
    a,b,c=e
    m=a*a+b*b+c*c
    prod=a*b*c
    assert char_coefficients(e)==(1,0,-m,-2*prod)
    # exact eigenvalue multiset string and max eigen in Q + Q sqrt(2)
    if m==0:return {"eigen":["0","0","0"],"rho2":0,"lambda_a":0,"lambda_sqrt2":0}
    if m==1:return {"eigen":["-1","0","1"],"rho2":1,"lambda_a":1,"lambda_sqrt2":0}
    if m==2:return {"eigen":["-sqrt(2)","0","sqrt(2)"],"rho2":2,"lambda_a":0,"lambda_sqrt2":1}
    if prod==1:return {"eigen":["-1","-1","2"],"rho2":4,"lambda_a":2,"lambda_sqrt2":0}
    if prod==-1:return {"eigen":["-2","1","1"],"rho2":4,"lambda_a":1,"lambda_sqrt2":0}
    raise AssertionError("wrong signed triangle classification")
def independent_bernoulli_edge_masks(w):
    check(w)
    _,p,sign=CONFIG[w]
    joint={}
    for mask in itertools.product((0,1),repeat=3):
        if any(mask[i] and not enabled(w,e) for i,e in enumerate(EDGE_NAMES)):
            continue
        mass=ONE
        for v,e in zip(mask,EDGE_NAMES):
            if enabled(w,e):mass*=p if v else ONE-p
        if mass:
            signed=(mask[0],mask[1],mask[2]*sign)
            joint[signed]=mass
    return dict(sorted(joint.items()))
def source_atom(w,bits,seed,n):
    e=edges_from_original(w,bits)
    spec=exact_spectrum(e)
    state=direct_state(e,seed,n)
    if state!=independent_walk_sum(e,seed,n):
        raise AssertionError("matvec and independent walk index enumeration disagree")
    row={"world":w}
    for i,name in enumerate(EDGE_NAMES):
        row["oracle_original_edge_R"+name+"a"]=bits[2*i]
        row["oracle_original_edge_R"+name+"b"]=bits[2*i+1]
        row["observed_edge_weight_w"+name]=e[i]
    for i in range(3):
        row["oracle_original_initial_seed_S"+str(i)]=seed[i]
        row["observed_initial_seed_v"+str(i)]=seed[i]
        row["observed_state_x"+str(i)+"_at_n"]=state[i]
    row["observed_time_step_n"]=n
    row["oracle_spectral_radius_squared"]=spec["rho2"]
    row["oracle_largest_eigenvalue_rational_coefficient"]=spec["lambda_a"]
    row["oracle_largest_eigenvalue_sqrt2_coefficient"]=spec["lambda_sqrt2"]
    row["original_complete_source_mass"]=F(1,2048)
    return row
@lru_cache(None)
def sources(w):
    check(w)
    data=tuple(source_atom(w,b,s,n) for b in EDGE_BITS for s in SEEDS for n in TIMES)
    assert len(data)==2048 and sum((r["original_complete_source_mass"] for r in data),ZERO)==ONE
    return data
def source_edge_joint(w):
    d=defaultdict(F)
    for row in sources(w):
        e=tuple(row["observed_edge_weight_w"+name] for name in EDGE_NAMES)
        d[e]+=row["original_complete_source_mass"]
    return dict(sorted(d.items()))
def source_spectral_expectations(w):
    ar=ZERO;bs=ZERO;rho2=ZERO
    for r in sources(w):
        p=r["original_complete_source_mass"]
        rho2+=p*r["oracle_spectral_radius_squared"]
        ar+=p*r["oracle_largest_eigenvalue_rational_coefficient"]
        bs+=p*r["oracle_largest_eigenvalue_sqrt2_coefficient"]
    return rho2,ar,bs
def independent_spectral_expectations(w):
    r=ZERO;a=ZERO;b=ZERO
    for edge,p in independent_bernoulli_edge_masks(w).items():
        sp=exact_spectrum(edge)
        r+=p*sp["rho2"]
        a+=p*sp["lambda_a"]
        b+=p*sp["lambda_sqrt2"]
    return r,a,b
def cayley_hamilton(e):
    A=matrix_from_edges(e)
    A2=matrix_product(A,A);A3=matrix_product(A2,A)
    a,b,c=e;m=a*a+b*b+c*c;prod=a*b*c
    return all(A3[i][j]==m*A[i][j]+(2*prod if i==j else 0)
               for i in range(3) for j in range(3))
def locked_claims():
    for w in WORLDS:
        assert source_edge_joint(w)==independent_bernoulli_edge_masks(w)
        assert source_spectral_expectations(w)==independent_spectral_expectations(w)
        for e in independent_bernoulli_edge_masks(w):
            assert cayley_hamilton(e)
    locked={
     "EMPTY_P0":(0,0,0),
     "EDGE_01_P1":(1,1,0),
     "PATH_01_12_P1":(2,0,1),
     "TRIANGLE_P1":(4,2,0),
     "ER_TRIANGLE_P_QUARTER":(F(49,64),F(29,64),F(9,64)),
     "ER_TRIANGLE_P_HALF":(F(13,8),F(5,8),F(3,8)),
     "ER_TRIANGLE_P_THREE_QUARTER":(F(171,64),F(63,64),F(27,64)),
     "SIGNED_ER_TRIANGLE_P_HALF":(F(13,8),F(1,2),F(3,8)),
     "SIGNED_TRIANGLE_P1":(4,1,0)
    }
    for w,expected in locked.items():
        actual=source_spectral_expectations(w)
        if actual!=tuple(F(x) for x in expected):
            raise AssertionError(f"{w}: spectral source expectations {actual} vs locked {expected}")
    # On identical original edge bits signed and unsigned, rho2 exactly same,
    # and lambda_max differs only for fully-open odd signed triangle (1 unit).
    plus="ER_TRIANGLE_P_HALF";minus="SIGNED_ER_TRIANGLE_P_HALF"
    for bits in EDGE_BITS:
        e1=edges_from_original(plus,bits);e2=edges_from_original(minus,bits)
        s1=exact_spectrum(e1);s2=exact_spectrum(e2)
        assert s1["rho2"]==s2["rho2"]
        assert s1["lambda_a"]-s2["lambda_a"]==(1 if all(e1) else 0)
    assert source_spectral_expectations(plus)[1]-source_spectral_expectations(minus)[1]==F(1,8)
    return True
def result_world(w):
    joint=source_edge_joint(w)
    rho2,a,b=source_spectral_expectations(w)
    return {
       "world":w,"frozen_topology":CONFIG[w][0],"edge_open_probability":str(CONFIG[w][1]),
       "negative_sign_on_open_edge12":CONFIG[w][2]==-1,
       "complete_original_ninebit_and_time_atoms":2048,
       "complete_sixbit_edge_weight_joint":{"".join("+" if t>0 else "-" if t<0 else "0" for t in e):str(p) for e,p in joint.items()},
       "exact_expected_spectral_radius_squared":str(rho2),
       "exact_expected_largest_algebraic_eigenvalue":{
           "rational":str(a),"sqrt2_coefficient":str(b)},
       "all_observed_matrix_charpolynomials_and_cayley_hamilton_verified":True,
       "all_source_vectors_direct_matvec_vs_independent_walks_verified":True,
       "exact_independent_bernoulli_edge_mask_probability_parity":True}
def emit():
    locked_claims()
    result=dict(research_id="R254",original_catalogue_id="11-014",
        prescore_freeze_commit=FREEZE,
        scientific_scope="FINITE_ARTIFICIAL_E1_SIGNED_RANDOM_THREE_NODE_SPECTRAL_METHODS",
        frozen_worlds=9,complete_original_source_atoms=18432,
        original_independent_edge_and_seed_bits_per_world=9,
        number_time_observations_per_bit_source=4,
        no_infinite_random_matrix_theory_or_real_diffusion_replicated=True,
        unsigned_er_p_half_expected_rho2="13/8",
        signed_er_p_half_expected_rho2="13/8",
        unsigned_er_p_half_expected_lmax="5/8+(3/8)sqrt(2)",
        signed_er_p_half_expected_lmax="1/2+(3/8)sqrt(2)",
        same_rho2_but_lmax_difference="1/8",
        new_real_human_E2=0,new_real_historical_E3=0,
        R073="FROZEN",PESEN_v0_1="FROZEN",
        world_results=[result_world(w) for w in WORLDS])
    src=HERE/"R254_ALL_18432_ORIGINAL_SIGNED_SPECTRAL_SOURCES.csv"
    keys=list(sources(WORLDS[0])[0])
    with src.open("w",encoding="utf-8",newline="") as f:
        wr=csv.DictWriter(f,fieldnames=keys,lineterminator="\n");wr.writeheader()
        for w in WORLDS:
            for row in sources(w):wr.writerow({k:str(row[k]) for k in keys})
    res=HERE/"R254_EXACT_RESULTS.json"
    res.write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    receipt=dict(research_id="R254",original_catalogue_id="11-014",
        full_original_signed_matrix_seed_time_atoms=18432,frozen_worlds=9,
        signed_spectral_radius_alias_but_largest_eigen_diff_certified=True,
        independent_walk_expansion_and_charpolynomial_verified=True,
        source_sha256=hashlib.sha256(src.read_bytes()).hexdigest(),
        results_sha256=hashlib.sha256(res.read_bytes()).hexdigest(),
        new_real_human_E2=0,new_real_historical_E3=0)
    (HERE/"R254_FINAL_MACHINE_ACCEPTANCE.json").write_text(json.dumps(receipt,indent=2)+"\n",encoding="utf-8")
    return receipt
class Tests(unittest.TestCase):
    def test_nine(self):self.assertEqual(len(WORLDS),9)
    def test_source_count(self):self.assertEqual(sum(len(sources(w)) for w in WORLDS),18432)
    def test_locked_claims(self):self.assertTrue(locked_claims())
    def test_rho2_signed_alias(self):
        self.assertEqual(source_spectral_expectations("ER_TRIANGLE_P_HALF")[0],
                         source_spectral_expectations("SIGNED_ER_TRIANGLE_P_HALF")[0])
    def test_lmax_signed_difference(self):
        self.assertEqual(source_spectral_expectations("ER_TRIANGLE_P_HALF")[1]-
                         source_spectral_expectations("SIGNED_ER_TRIANGLE_P_HALF")[1],F(1,8))
    def test_path_eigen(self):self.assertEqual(exact_spectrum((1,0,1))["rho2"],2)
    def test_triangle_spectrum(self):self.assertEqual(exact_spectrum((1,1,1))["eigen"],["-1","-1","2"])
    def test_negative_triangle(self):self.assertEqual(exact_spectrum((1,1,-1))["eigen"],["-2","1","1"])
    def test_cayley(self):
        self.assertTrue(cayley_hamilton((1,1,-1)))
        self.assertTrue(cayley_hamilton((1,0,1)))
    def test_direct_seed_path(self):
        self.assertEqual(direct_state((1,1,1),(1,0,0),2),(2,1,1))
    def test_unknown(self):
        with self.assertRaises(ValueError):sources("UNFROZEN_MATRIX")
def _case(w,kind):
    def t(self):
        data=sources(w)
        if kind=="mass":
            self.assertEqual(sum((r["original_complete_source_mass"] for r in data),ZERO),ONE)
        elif kind=="unique":
            keys=[f"oracle_original_edge_R{e}{s}" for e in EDGE_NAMES for s in ("a","b")]+[f"oracle_original_initial_seed_S{i}" for i in range(3)]+["observed_time_step_n"]
            self.assertEqual(len({tuple(r[k] for k in keys) for r in data}),2048)
        elif kind=="positive":self.assertTrue(all(r["original_complete_source_mass"]==F(1,2048) for r in data))
        elif kind=="law":self.assertEqual(source_edge_joint(w),independent_bernoulli_edge_masks(w))
        elif kind=="spectrum":self.assertEqual(source_spectral_expectations(w),independent_spectral_expectations(w))
        elif kind=="cayley":
            for edge in independent_bernoulli_edge_masks(w):self.assertTrue(cayley_hamilton(edge))
        elif kind=="walks":
            for edge in independent_bernoulli_edge_masks(w):
                for s in SEEDS:
                    for n in TIMES:self.assertEqual(direct_state(edge,s,n),independent_walk_sum(edge,s,n))
        elif kind=="report":self.assertEqual(result_world(w)["complete_original_ninebit_and_time_atoms"],2048)
        else:raise AssertionError("unfrozen test")
    return t
for w in WORLDS:
    for kind in ("mass","unique","positive","law","spectrum","cayley","walks","report"):
        setattr(Tests,"test_"+w.lower()+"_"+kind,_case(w,kind))
if __name__=="__main__":
    p=argparse.ArgumentParser();g=p.add_mutually_exclusive_group(required=True)
    g.add_argument("--test",action="store_true");g.add_argument("--emit",action="store_true")
    a=p.parse_args()
    if a.test:unittest.main(argv=["r254"],verbosity=2)
    else:print(json.dumps(emit(),indent=2))
