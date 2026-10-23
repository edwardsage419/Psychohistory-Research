#!/usr/bin/env python3
"""R255 exact finite three-node random graph Laplacian and lazy consensus.

For each of nine frozen worlds: six independent random edge bits, three
independent binary opinion seeds, four time indices -> 2048 complete
original artificial atoms. Exact Fraction source propagation is compared
with a separate time-index walk sum, closed graph spectral classes,
independent Bernoulli-mask laws and variance dissipation.
"""
from __future__ import annotations
import argparse,csv,hashlib,itertools,json,unittest
from collections import defaultdict
from fractions import Fraction as F
from functools import lru_cache
from pathlib import Path
HERE=Path(__file__).resolve().parent
FREEZE="1b5b16feb1291a017c1ab01b7dd1deda87ae138f"
ZERO=F(0);ONE=F(1)
EDGE_NAMES=("01","02","12")
EDGE_BITS=tuple(itertools.product((0,1),repeat=6))
SEEDS=tuple(itertools.product((0,1),repeat=3))
TIMES=(0,1,2,3)
ALIAS="STATIC_EMPTY_TRUE_GRAPH_OBS_REPORT_HALF"
CONFIG={
"EMPTY_P0":("ALL",ZERO),
"EDGE01_P1":("01",ONE),
"EDGE12_P1":("12",ONE),
"PATH_01_12_P1":("01_12",ONE),
"TRIANGLE_P1":("ALL",ONE),
"ER_TRIANGLE_P_QUARTER":("ALL",F(1,4)),
"ER_TRIANGLE_P_HALF":("ALL",F(1,2)),
"ER_TRIANGLE_P_THREE_QUARTER":("ALL",F(3,4)),
ALIAS:("ALL",F(1,2))}
WORLDS=tuple(CONFIG)
def check(w):
    if w not in WORLDS:raise ValueError("unfrozen Laplacian world")
def enabled(w,e):
    t=CONFIG[w][0]
    return t=="ALL" or (t=="01" and e=="01") or (t=="12" and e=="12") or (t=="01_12" and e in ("01","12"))
def observed_edges(w,bits):
    check(w)
    if len(bits)!=6 or any(x not in (0,1) for x in bits):
        raise ValueError("expected six fair original bits")
    p=CONFIG[w][1]
    return tuple(int(enabled(w,e) and F(2*bits[2*i]+bits[2*i+1])<4*p)
                 for i,e in enumerate(EDGE_NAMES))
def adjacency(edge):
    a,b,c=edge
    return ((0,a,b),(a,0,c),(b,c,0))
def laplacian(edge):
    A=adjacency(edge)
    deg=[sum(A[i]) for i in range(3)]
    return tuple(tuple((deg[i] if i==j else 0)-A[i][j] for j in range(3)) for i in range(3))
def transition(edge):
    L=laplacian(edge)
    return tuple(tuple((ONE if i==j else ZERO)-F(L[i][j],4) for j in range(3)) for i in range(3))
def multiply(M,v):
    return tuple(sum((M[i][j]*v[j] for j in range(3)),ZERO) for i in range(3))
def product(M,N):
    return tuple(tuple(sum((M[i][k]*N[k][j] for k in range(3)),ZERO) for j in range(3)) for i in range(3))
def determinant(M):
    a,b,c=M[0];d,e,f=M[1];g,h,i=M[2]
    return a*(e*i-f*h)-b*(d*i-f*g)+c*(d*h-e*g)
def char_poly_laplacian(edge):
    L=laplacian(edge)
    tr=sum(L[i][i] for i in range(3))
    traceL2=sum(L[i][j]*L[j][i] for i in range(3) for j in range(3))
    return (1,-tr,(tr*tr-traceL2)//2,-determinant(L))
def components(edge):
    A=adjacency(edge)
    seen=set();count=0
    for i in range(3):
        if i in seen:continue
        count+=1;queue=[i];seen.add(i)
        while queue:
            v=queue.pop()
            for j in range(3):
                if A[v][j] and j not in seen:seen.add(j);queue.append(j)
    return count
def analytic_laplacian_spectrum(edge):
    m=sum(edge)
    if m==0:eig=(0,0,0);coeff=(1,0,0,0)
    elif m==1:eig=(0,0,2);coeff=(1,-2,0,0)
    elif m==2:eig=(0,1,3);coeff=(1,-4,3,0)
    elif m==3:eig=(0,3,3);coeff=(1,-6,9,0)
    else:raise AssertionError("not a simple three-node graph")
    if char_poly_laplacian(edge)!=coeff:
        raise AssertionError("independent determinant does not match predicted Laplacian eigenvalues")
    if components(edge)!=eig.count(0):
        raise AssertionError("zero eigenvalue count not connected components")
    return {"eigenvalues":eig,"lambda2":eig[1],"zero_multiplicity":eig.count(0),
            "connected":int(eig[1]>0)}
def direct_state(edge,seed,n):
    if seed not in SEEDS or n not in TIMES:raise ValueError("unfrozen seed time")
    v=tuple(F(x) for x in seed)
    W=transition(edge)
    for _ in range(n):v=multiply(W,v)
    return v
def independent_walk_sum(edge,seed,n):
    """No matrix multiplication or source trajectory call: sum walks directly."""
    if seed not in SEEDS or n not in TIMES:raise ValueError("unfrozen seed time")
    if n==0:return tuple(F(x) for x in seed)
    W=transition(edge)
    result=[]
    for i in range(3):
        total=ZERO
        for path in itertools.product(range(3),repeat=n):
            mass=W[i][path[0]]
            for j in range(n-1):mass*=W[path[j]][path[j+1]]
            total+=mass*seed[path[-1]]
        result.append(total)
    return tuple(result)
def mean_opinion(v):return sum(v,ZERO)/3
def variance_opinion(v):
    mu=mean_opinion(v)
    return sum(((x-mu)**2 for x in v),ZERO)
def source_atom(w,bits,seed,n):
    edge=observed_edges(w,bits)
    true_edge=(0,0,0) if w==ALIAS else edge
    sp=analytic_laplacian_spectrum(edge)
    state=direct_state(edge,seed,n)
    if state!=independent_walk_sum(edge,seed,n):
        raise AssertionError("direct W iteration and independent path sum disagree")
    nxt=multiply(transition(edge),state)
    v=variance_opinion(state);nextv=variance_opinion(nxt)
    if nextv>v:raise AssertionError("symmetric averaging violates squared deviation monotonicity")
    if sum(state,ZERO)!=F(sum(seed)):
        raise AssertionError("mean preserving consensus transition violated")
    out={"world":w}
    for j,e in enumerate(EDGE_NAMES):
        out["oracle_original_edge_R"+e+"a"]=bits[2*j]
        out["oracle_original_edge_R"+e+"b"]=bits[2*j+1]
        out["observed_reported_edge_Y"+e]=edge[j]
        out["oracle_true_hidden_edge_H"+e]=true_edge[j]
    for j in range(3):
        out["oracle_original_initial_opinion_S"+str(j)]=seed[j]
        out["observed_opinion_x"+str(j)+"_at_n"]=state[j]
        out["observed_next_opinion_x"+str(j)]=nxt[j]
    out["observed_time_index_n"]=n
    out["observed_squared_deviation_Vn"]=v
    out["observed_next_squared_deviation_V"]=nextv
    out["oracle_observed_graph_lambda2"]=sp["lambda2"]
    out["oracle_observed_graph_zero_eigenvalue_multiplicity"]=sp["zero_multiplicity"]
    out["oracle_true_graph_connected_components"]=components(true_edge)
    out["original_complete_source_mass"]=F(1,2048)
    return out
@lru_cache(None)
def sources(w):
    check(w)
    rows=tuple(source_atom(w,b,seed,n) for b in EDGE_BITS for seed in SEEDS for n in TIMES)
    assert len(rows)==2048 and sum((r["original_complete_source_mass"] for r in rows),ZERO)==ONE
    return rows
def source_edge_joint(w):
    out=defaultdict(F)
    for r in sources(w):
        mask=tuple(r["observed_reported_edge_Y"+e] for e in EDGE_NAMES)
        out[mask]+=r["original_complete_source_mass"]
    return dict(sorted(out.items()))
def independent_bernoulli_masks(w):
    check(w);p=CONFIG[w][1]
    out={}
    for mask in itertools.product((0,1),repeat=3):
        if any(v and not enabled(w,e) for v,e in zip(mask,EDGE_NAMES)):continue
        probability=ONE
        for v,e in zip(mask,EDGE_NAMES):
            if enabled(w,e):probability*=p if v else ONE-p
        if probability:out[mask]=probability
    return dict(sorted(out.items()))
def source_laplacian_stats(w):
    gap=ZERO;linked=ZERO;comp=ZERO
    for r in sources(w):
        p=r["original_complete_source_mass"]
        gap+=p*r["oracle_observed_graph_lambda2"]
        linked+=p*int(r["oracle_observed_graph_lambda2"]>0)
        comp+=p*r["oracle_observed_graph_zero_eigenvalue_multiplicity"]
    return gap,linked,comp
def independent_laplacian_stats(w):
    gap=ZERO;linked=ZERO;comp=ZERO
    for edge,p in independent_bernoulli_masks(w).items():
        s=analytic_laplacian_spectrum(edge)
        gap+=p*s["lambda2"];linked+=p*s["connected"];comp+=p*s["zero_multiplicity"]
    return gap,linked,comp
def locked_claims():
    locked={
     "EMPTY_P0":(0,0,3),
     "EDGE01_P1":(0,0,2),
     "EDGE12_P1":(0,0,2),
     "PATH_01_12_P1":(1,1,1),
     "TRIANGLE_P1":(3,1,1),
     "ER_TRIANGLE_P_QUARTER":(F(3,16),F(5,32),F(145,64)),
     "ER_TRIANGLE_P_HALF":(F(3,4),F(1,2),F(13,8)),
     "ER_TRIANGLE_P_THREE_QUARTER":(F(27,16),F(27,32),F(75,64)),
     ALIAS:(F(3,4),F(1,2),F(13,8))}
    for w,want in locked.items():
        a=source_laplacian_stats(w)
        b=independent_laplacian_stats(w)
        assert source_edge_joint(w)==independent_bernoulli_masks(w)
        if a!=b or a!=tuple(F(x) for x in want):
            raise AssertionError(f"{w} disconnected spectral mean {a} vs {b} vs {want}")
    base="ER_TRIANGLE_P_HALF"
    assert source_edge_joint(base)==source_edge_joint(ALIAS)
    for b in EDGE_BITS:
        assert observed_edges(base,b)==observed_edges(ALIAS,b)
        for s in SEEDS:
            for n in TIMES:assert direct_state(observed_edges(base,b),s,n)==direct_state(observed_edges(ALIAS,b),s,n)
    assert all(r["oracle_true_graph_connected_components"]==3 for r in sources(ALIAS))
    return True
def world_result(w):
    gap,conn,comps=source_laplacian_stats(w)
    return dict(world=w,complete_original_ninebit_time_source_atoms=2048,
        frozen_topology=CONFIG[w][0],
        frozen_edge_open_probability=str(CONFIG[w][1]),
        complete_observed_edge_joint={"".join(map(str,e)):str(p) for e,p in source_edge_joint(w).items()},
        exact_expected_algebraic_connectivity_lambda2=str(gap),
        observed_graph_connected_probability=str(conn),
        exact_expected_number_connected_components=str(comps),
        true_hidden_graph_always_empty_for_sensor_alias=(w==ALIAS),
        exact_full_source_direct_matrix_vs_independent_walks=True,
        exact_independent_closed_edge_mask_law=True,
        graph_L_eigenvalue_zero_multiplicity_equals_BFS_components=True,
        all_complete_source_opinion_variances_nonincreasing=True)
def emit():
    locked_claims()
    data=dict(research_id="R255",original_catalogue_id="11-015",
        prescore_freeze_commit=FREEZE,
        scientific_scope="FINITE_ARTIFICIAL_E1_THREE_NODE_RANDOM_LAPLACIAN_AND_LAZY_CONSENSUS",
        frozen_worlds=9,complete_original_source_atoms=18432,
        no_real_social_consensus_or_large_network_spectral_claim=True,
        three_node_random_graph_expected_lambda2_formula="3p^2",
        three_node_connected_probability_formula="3p^2-2p^3",
        three_node_expected_components_formula="3-3p+p^3",
        sourcewise_hidden_empty_graph_vs_observed_ER_half_alias=[ALIAS,"ER_TRIANGLE_P_HALF"],
        new_real_human_E2=0,new_real_historical_E3=0,
        R073="FROZEN",PESEN_v0_1="FROZEN",
        world_results=[world_result(w) for w in WORLDS])
    out=HERE/"R255_ALL_18432_ORIGINAL_LAPLACIAN_CONSENSUS_SOURCE_ATOMS.csv"
    fields=list(sources(WORLDS[0])[0])
    with out.open("w",encoding="utf-8",newline="") as f:
        wr=csv.DictWriter(f,fieldnames=fields,lineterminator="\n");wr.writeheader()
        for w in WORLDS:
            for r in sources(w):wr.writerow({k:str(r[k]) for k in fields})
    result=HERE/"R255_EXACT_RESULTS.json"
    result.write_text(json.dumps(data,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    receipt=dict(research_id="R255",original_catalogue_id="11-015",
        all_original_graph_seed_time_source_atoms=18432,frozen_worlds=9,
        independent_laplacian_spectra_and_component_count_proven=True,
        all_source_consensus_variance_nonincreasing=True,
        sourcewise_fake_graph_vs_true_graph_alias=True,
        source_sha256=hashlib.sha256(out.read_bytes()).hexdigest(),
        results_sha256=hashlib.sha256(result.read_bytes()).hexdigest(),
        new_real_human_E2=0,new_real_historical_E3=0)
    (HERE/"R255_FINAL_MACHINE_ACCEPTANCE.json").write_text(json.dumps(receipt,indent=2)+"\n",encoding="utf-8")
    return receipt
class Tests(unittest.TestCase):
    def test_nine_worlds(self):self.assertEqual(len(WORLDS),9)
    def test_original_18432_sources(self):self.assertEqual(sum(len(sources(w)) for w in WORLDS),18432)
    def test_frozen_theorem(self):self.assertTrue(locked_claims())
    def test_path_eigen(self):self.assertEqual(analytic_laplacian_spectrum((1,0,1))["eigenvalues"],(0,1,3))
    def test_triangle_eigen(self):self.assertEqual(analytic_laplacian_spectrum((1,1,1))["eigenvalues"],(0,3,3))
    def test_single_edge(self):self.assertEqual(analytic_laplacian_spectrum((1,0,0))["eigenvalues"],(0,0,2))
    def test_zero_multiplicity(self):self.assertEqual(analytic_laplacian_spectrum((0,0,0))["zero_multiplicity"],3)
    def test_half_expected_gap(self):self.assertEqual(source_laplacian_stats("ER_TRIANGLE_P_HALF")[0],F(3,4))
    def test_signed_not_allowed(self):
        with self.assertRaises(AssertionError):analytic_laplacian_spectrum((1,1,-1))
    def test_mean_preservation(self):
        s=direct_state((1,1,1),(1,0,0),3)
        self.assertEqual(sum(s,ZERO),ONE)
    def test_fake_hidden_graph(self):
        self.assertTrue(all(x["oracle_true_graph_connected_components"]==3 for x in sources(ALIAS)))
    def test_invalid_world(self):
        with self.assertRaises(ValueError):sources("BAD_GRAPH")
def _case(w,kind):
    def t(self):
        data=sources(w)
        if kind=="mass":self.assertEqual(sum((r["original_complete_source_mass"] for r in data),ZERO),ONE)
        elif kind=="unique":
            keys=[f"oracle_original_edge_R{e}{s}" for e in EDGE_NAMES for s in ("a","b")]+[f"oracle_original_initial_opinion_S{i}" for i in range(3)]+["observed_time_index_n"]
            self.assertEqual(len({tuple(r[k] for k in keys) for r in data}),2048)
        elif kind=="positive":self.assertTrue(all(r["original_complete_source_mass"]==F(1,2048) for r in data))
        elif kind=="law":self.assertEqual(source_edge_joint(w),independent_bernoulli_masks(w))
        elif kind=="laplacian":self.assertEqual(source_laplacian_stats(w),independent_laplacian_stats(w))
        elif kind=="walks":
            for edge in independent_bernoulli_masks(w):
                for seed in SEEDS:
                    for n in TIMES:self.assertEqual(direct_state(edge,seed,n),independent_walk_sum(edge,seed,n))
        elif kind=="dissipation":
            self.assertTrue(all(r["observed_next_squared_deviation_V"]<=r["observed_squared_deviation_Vn"] for r in data))
        elif kind=="report":self.assertEqual(world_result(w)["complete_original_ninebit_time_source_atoms"],2048)
        else:raise AssertionError("invalid type")
    return t
for w in WORLDS:
    for k in ("mass","unique","positive","law","laplacian","walks","dissipation","report"):
        setattr(Tests,"test_"+w.lower()+"_"+k,_case(w,k))
if __name__=="__main__":
    p=argparse.ArgumentParser();g=p.add_mutually_exclusive_group(required=True)
    g.add_argument("--test",action="store_true");g.add_argument("--emit",action="store_true")
    a=p.parse_args()
    if a.test:unittest.main(argv=["r255"],verbosity=2)
    else:print(json.dumps(emit(),indent=2))
