#!/usr/bin/env python3
"""R250 finite three-node bond percolation response, NOT a critical phase transition.

Nine structural graph/probability worlds, each with six original fair bits
(three independent 2-bit potential edge draws) and 64 complete source atoms,
576 total. Source BFS is checked against independent closed-form cluster-size
polynomials and Bernoulli edge-mask product probabilities. The graph has
only three vertices: no infinite cluster, no thermodynamic singularity.
"""
from __future__ import annotations
import argparse,csv,hashlib,itertools,json,unittest
from collections import defaultdict
from fractions import Fraction as F
from functools import lru_cache
from pathlib import Path

HERE=Path(__file__).resolve().parent
FREEZE="f511d8390c4d7439ad14a5315447b335af9df26c"
ZERO=F(0);ONE=F(1)
EDGES=((0,1),(0,2),(1,2))
EDGE_NAMES=("01","02","12")
BITS=(0,1)
EXOG=tuple(itertools.product(BITS,repeat=6))
WORLD_CONFIG={
 "CHAIN_P_QUARTER":("CHAIN",F(1,4)),
 "CHAIN_P_HALF":("CHAIN",F(1,2)),
 "CHAIN_P_THREE_QUARTER":("CHAIN",F(3,4)),
 "TRIANGLE_P_ZERO":("TRIANGLE",ZERO),
 "TRIANGLE_P_QUARTER":("TRIANGLE",F(1,4)),
 "TRIANGLE_P_HALF":("TRIANGLE",F(1,2)),
 "TRIANGLE_P_THREE_QUARTER":("TRIANGLE",F(3,4)),
 "TRIANGLE_P_ONE":("TRIANGLE",ONE),
 "TRIANGLE_STATIC_TRUE_GRAPH_REPORT_ALIAS":("TRIANGLE",F(1,2))
}
WORLDS=tuple(WORLD_CONFIG)
ALIAS="TRIANGLE_STATIC_TRUE_GRAPH_REPORT_ALIAS"

def require(world):
    if world not in WORLD_CONFIG:raise ValueError("unfrozen graph mechanism")

def edge_report(world,bits):
    require(world)
    if len(bits)!=6 or any(v not in BITS for v in bits):
        raise ValueError("not six independent original edge draw bits")
    topology,p=WORLD_CONFIG[world]
    result=[]
    for i,name in enumerate(EDGE_NAMES):
        if topology=="CHAIN" and name=="02":
            result.append(0)
        else:
            r=2*bits[2*i]+bits[2*i+1]
            result.append(int(F(r)<4*p))
    return tuple(result)

def bfs_root_component_size(edges):
    if len(edges)!=3 or any(x not in BITS for x in edges):
        raise ValueError("not observed edge configuration")
    seen={0}
    pending=[0]
    while pending:
        node=pending.pop()
        for (a,b),opened in zip(EDGES,edges):
            if opened:
                if a==node and b not in seen:
                    seen.add(b);pending.append(b)
                if b==node and a not in seen:
                    seen.add(a);pending.append(a)
    return len(seen)

def source_atom(world,bits):
    y=edge_report(world,bits)
    true=(0,0,0) if world==ALIAS else y
    out={"world":world,
         "observed_graph_topology":WORLD_CONFIG[world][0],
         "frozen_edge_open_probability":WORLD_CONFIG[world][1]}
    for i,e in enumerate(EDGE_NAMES):
        out["oracle_original_edge_R"+e+"a"]=bits[2*i]
        out["oracle_original_edge_R"+e+"b"]=bits[2*i+1]
        out["observed_reported_edge_Y"+e]=y[i]
        out["oracle_true_hidden_edge_H"+e]=true[i]
    out["observed_root_component_size"]=bfs_root_component_size(y)
    out["oracle_true_root_component_size"]=bfs_root_component_size(true)
    out["original_full_edge_source_probability"]=F(1,64)
    return out

@lru_cache(maxsize=None)
def sources(world):
    require(world)
    rows=tuple(source_atom(world,bits) for bits in EXOG)
    if len(rows)!=64 or sum((r["original_full_edge_source_probability"] for r in rows),ZERO)!=ONE:
        raise AssertionError("64 complete six-bit source universe absent")
    return rows

def observed_edge_joint(world):
    result=defaultdict(F)
    for r in sources(world):
        mask=tuple(r["observed_reported_edge_Y"+e] for e in EDGE_NAMES)
        result[mask]+=r["original_full_edge_source_probability"]
    return dict(sorted(result.items()))

def root_size_joint(world):
    result=defaultdict(F)
    for r in sources(world):
        result[r["observed_root_component_size"]]+=r["original_full_edge_source_probability"]
    return dict(sorted(result.items()))

def independent_bernoulli_edge_joint(world):
    """Product law over all 8 masks: NO source or BFS access."""
    require(world)
    topology,p=WORLD_CONFIG[world]
    out={}
    for mask in itertools.product(BITS,repeat=3):
        if topology=="CHAIN" and mask[1]!=0:continue
        mass=ONE
        for i,(edge,edgeval) in enumerate(zip(EDGE_NAMES,mask)):
            if topology=="CHAIN" and edge=="02":continue
            mass*=p if edgeval else (ONE-p)
        if mass:out[mask]=mass
    return dict(sorted(out.items()))

def independent_root_size_distribution(world):
    """Closed analytic P(Croot=1,2,3); no original source or BFS."""
    require(world)
    topology,p=WORLD_CONFIG[world]
    if topology=="CHAIN":
        return {k:v for k,v in ((1,ONE-p),(2,p*(ONE-p)),(3,p*p)) if v}
    result=((1,(ONE-p)**2),(2,2*p*(ONE-p)**2),
            (3,3*p*p-2*p*p*p))
    return {k:v for k,v in result if v}

def independent_mean_and_slope(world):
    topology,p=WORLD_CONFIG[world]
    if topology=="CHAIN":
        return ONE+p+p*p,ONE+2*p
    return ONE+2*p+2*p*p-2*p*p*p,2+4*p-6*p*p

def world_result(world):
    src=sources(world)
    joint=observed_edge_joint(world)
    size=root_size_joint(world)
    if joint!=independent_bernoulli_edge_joint(world):
        raise AssertionError("source observed edge joint differs product Bernoulli law")
    if size!=independent_root_size_distribution(world):
        raise AssertionError("BFS source cluster differs closed-form root size polynomial")
    mean=sum((F(k)*v for k,v in size.items()),ZERO)
    independent_mean,slope=independent_mean_and_slope(world)
    if mean!=independent_mean:raise AssertionError("root cluster mean differs analytic polynomial")
    return dict(
      world=world,finite_graph_topology=WORLD_CONFIG[world][0],
      exact_bernoulli_edge_probability=str(WORLD_CONFIG[world][1]),
      complete_original_six_bit_edge_atoms=64,
      observed_root_size_distribution={str(k):str(v) for k,v in size.items()},
      observed_full_three_edge_mask_joint={
          "".join(map(str,k)):str(v) for k,v in joint.items()},
      exact_root_expected_component_size=str(mean),
      exact_root_component_size3_probability=str(size.get(3,ZERO)),
      derivative_expected_root_component_vs_p=str(slope),
      actual_true_hidden_component_size_sourcewise=[
          r["oracle_true_root_component_size"] for r in src],
      independent_finite_Bernoulli_edge_product_formula_verified=True,
      independent_finite_root_component_polynomial_verified=True,
      strictly_finite_no_genuine_critical_point=True
    )

def baseline_claims():
    expect={
       "CHAIN_P_HALF":(F(7,4),F(1,4)),
       "TRIANGLE_P_QUARTER":(F(51,32),F(5,32)),
       "TRIANGLE_P_HALF":(F(9,4),F(1,2)),
       "TRIANGLE_P_THREE_QUARTER":(F(89,32),F(27,32)),
       "TRIANGLE_P_ZERO":(ONE,ZERO),
       "TRIANGLE_P_ONE":(F(3),ONE)
    }
    for world,expected in expect.items():
        actual=independent_mean_and_slope(world)[0],root_size_joint(world).get(3,ZERO)
        if actual!=expected:raise AssertionError(f"{world} exact root connectivity mismatch {actual} vs {expected}")
    ref="TRIANGLE_P_HALF"
    if observed_edge_joint(ref)!=observed_edge_joint(ALIAS):raise AssertionError("report sensor full edge distribution alias broken")
    if root_size_joint(ref)!=root_size_joint(ALIAS):raise AssertionError("root-size observation distribution alias broken")
    for bits in EXOG:
        a=source_atom(ref,bits)
        b=source_atom(ALIAS,bits)
        for edge in EDGE_NAMES:
            if a["observed_reported_edge_Y"+edge]!=b["observed_reported_edge_Y"+edge]:
                raise AssertionError("sourcewise observed edge alias broken")
            if b["oracle_true_hidden_edge_H"+edge]!=0:
                raise AssertionError("hidden physical graph must be empty")
        if a["observed_root_component_size"]!=b["observed_root_component_size"]:
            raise AssertionError("root observation alias not sourcewise")
        if b["oracle_true_root_component_size"]!=1:
            raise AssertionError("root real true component must be singleton")
    for world in WORLDS:
        m,_=independent_mean_and_slope(world)
        if not (ONE<=m<=F(3)):raise AssertionError("finite root cluster incorrectly unbounded")
    return True

def generate():
    baseline_claims()
    data=dict(research_id="R250",original_catalogue_id="11-010",
       prescore_freeze_commit=FREEZE,
       scientific_scope="FINITE_ARTIFICIAL_E1_THREE_NODE_BOND_PERCOLATION_POLYNOMIAL_NO_TRUE_PHASE_TRANSITION",
       finite_vertices=3,finite_possible_edges=3,
       frozen_worlds=9,original_complete_six_bit_sources=576,
       true_thermodynamic_critical_phase_transition_verified=False,
       finite_polynomials_are_continuous_and_smooth=True,
       chain_analytic_mean_polynomial="1+p+p^2",
       triangle_analytic_mean_polynomial="1+2p+2p^2-2p^3",
       chain_P_full_root_component="p^2",
       triangle_P_full_root_component="3p^2-2p^3",
       sourcewise_report_vs_true_empty_graph_alias=[
          "TRIANGLE_P_HALF","TRIANGLE_STATIC_TRUE_GRAPH_REPORT_ALIAS"],
       new_real_human_E2=0,new_real_historical_E3=0,
       R073="FROZEN",PESEN_v0_1="FROZEN",
       world_results=[world_result(w) for w in WORLDS])
    p=HERE/"R250_ALL_576_ORIGINAL_THREE_NODE_EDGE_SOURCE_ATOMS.csv"
    keys=list(sources("CHAIN_P_QUARTER")[0])
    with p.open("w",newline="",encoding="utf-8") as f:
        wr=csv.DictWriter(f,fieldnames=keys,lineterminator="\n");wr.writeheader()
        for w in WORLDS:
            for r in sources(w):wr.writerow({k:str(r[k]) for k in keys})
    res=HERE/"R250_EXACT_RESULTS.json"
    res.write_text(json.dumps(data,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    receipt=dict(
       research_id="R250",original_catalogue_id="11-010",
       frozen_worlds=9,complete_original_edge_source_atoms=576,
       no_true_phase_transition_in_three_node_finite_graph=True,
       exact_finite_root_cluster_distribution_by_polynomials=True,
       independent_full_edge_bernoulli_mask_distribution=True,
       sourcewise_sensor_alias_vs_true_empty_graph=True,
       source_sha256=hashlib.sha256(p.read_bytes()).hexdigest(),
       results_sha256=hashlib.sha256(res.read_bytes()).hexdigest(),
       new_real_human_E2=0,new_real_historical_E3=0)
    (HERE/"R250_FINAL_MACHINE_ACCEPTANCE.json").write_text(json.dumps(receipt,indent=2)+"\n",encoding="utf-8")
    return receipt

class Tests(unittest.TestCase):
    def test_nine_finite_worlds(self):self.assertEqual(len(WORLDS),9)
    def test_576_total_complete(self):self.assertEqual(sum(len(sources(w)) for w in WORLDS),576)
    def test_all_fixed_claims(self):self.assertTrue(baseline_claims())
    def test_chain_half(self):
        self.assertEqual(independent_mean_and_slope("CHAIN_P_HALF")[0],F(7,4))
    def test_triangle_half(self):
        self.assertEqual(independent_mean_and_slope("TRIANGLE_P_HALF")[0],F(9,4))
    def test_triangle_quarter(self):
        self.assertEqual(independent_root_size_distribution("TRIANGLE_P_QUARTER")[3],F(5,32))
    def test_triangle_three_quarter(self):
        self.assertEqual(independent_root_size_distribution("TRIANGLE_P_THREE_QUARTER")[3],F(27,32))
    def test_endpoints(self):
        self.assertEqual(root_size_joint("TRIANGLE_P_ZERO"),{1:ONE})
        self.assertEqual(root_size_joint("TRIANGLE_P_ONE"),{3:ONE})
    def test_triangle_half_derivative(self):
        self.assertEqual(independent_mean_and_slope("TRIANGLE_P_HALF")[1],F(5,2))
    def test_chain_half_derivative(self):
        self.assertEqual(independent_mean_and_slope("CHAIN_P_HALF")[1],F(2))
    def test_static_physical_graph(self):
        self.assertEqual(set(r["oracle_true_root_component_size"] for r in sources(ALIAS)),{1})
    def test_unknown_world(self):
        with self.assertRaises(ValueError):sources("UNKNOWN_WORLD")

def _case(world,kind):
    def t(self):
        rows=sources(world)
        if kind=="mass":
            self.assertEqual(sum((r["original_full_edge_source_probability"] for r in rows),ZERO),ONE)
        elif kind=="unique":
            names=[("oracle_original_edge_R"+edge+suffix) for edge in EDGE_NAMES for suffix in ("a","b")]
            self.assertEqual(len({tuple(r[k] for k in names) for r in rows}),64)
        elif kind=="positive":
            self.assertTrue(all(r["original_full_edge_source_probability"]==F(1,64) for r in rows))
        elif kind=="edges":
            self.assertEqual(observed_edge_joint(world),independent_bernoulli_edge_joint(world))
        elif kind=="clusters":
            self.assertEqual(root_size_joint(world),independent_root_size_distribution(world))
        elif kind=="source":
            for r in rows:
                mask=tuple(r["observed_reported_edge_Y"+e] for e in EDGE_NAMES)
                self.assertEqual(bfs_root_component_size(mask),r["observed_root_component_size"])
        elif kind=="bounds":
            self.assertTrue(all(ONE<=r["observed_root_component_size"]<=F(3) for r in rows))
        elif kind=="report":
            self.assertEqual(world_result(world)["complete_original_six_bit_edge_atoms"],64)
        else:raise AssertionError("not frozen test")
    return t

for _w in WORLDS:
    for _kind in ("mass","unique","positive","edges","clusters","source","bounds","report"):
        setattr(Tests,"test_"+_w.lower()+"_"+_kind,_case(_w,_kind))

if __name__=="__main__":
    ap=argparse.ArgumentParser()
    g=ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--test",action="store_true")
    g.add_argument("--emit",action="store_true")
    a=ap.parse_args()
    if a.test:unittest.main(argv=["r250"],verbosity=2)
    else:print(json.dumps(generate(),indent=2))
