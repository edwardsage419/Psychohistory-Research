"""R174 original artificial 4-node diffusion versus independent invention benchmark.

Two entirely separate Fraction transition algorithms: analytical hazards and
enumerated per-node/per-edge Bernoulli events. Only synthetic E1 evidence.
"""
from __future__ import annotations

from collections import defaultdict
from fractions import Fraction as F
from hashlib import sha256
from itertools import product
from pathlib import Path
import json
import sys
import unittest
import zipfile

HERE=Path(__file__).resolve().parent
PROTO=HERE.parent.parent/"protocols/R174_DIFFUSION_VS_INVENTION_72_4NODE_FINITE_MARKOV_WORLDS_PRESCORE_FREEZE_2026-10-21.md"
OUT=HERE/"R174_EXACT_RESULTS.json"
ACCEPT=HERE/"R174_FINAL_MACHINE_ACCEPTANCE.json"
ARCH=HERE/"R174_Diffusion_Invention_72_Worlds_Exact_Archive.zip"
EDGES={
 "star":((0,1),(0,2),(0,3)),
 "path":((0,1),(1,2),(2,3)),
 "cycle":((0,1),(1,2),(2,3),(3,0)),
 "complete":tuple((i,j) for i in range(4) for j in range(i+1,4)),
}
SEEDS=(0,1)
RATES=(F(1,4),F(1,2),F(3,4))
MECHANISMS=("invention","diffusion","mixed")
STATES=tuple(range(16))


def parameters(kind,a):
    return {"invention":(a,F(0)), "diffusion":(F(0),a),
            "mixed":(F(1,4),a)}[kind]


def adopted_neighbours(edges,state,node):
    return sum((state>>other)&1 for i,j in edges
               for other in ([j] if i==node else [i] if j==node else []))


def analytical_row(edges,state,mu,beta):
    """Algorithm A: local complement-product hazards and joint node events."""
    dist={state:F(1)}
    for node in range(4):
        if state>>node&1:continue
        m=adopted_neighbours(edges,state,node)
        h=1-(1-mu)*(1-beta)**m
        res=defaultdict(F)
        for mask,p in dist.items():
            res[mask]+=p*(1-h)
            res[mask|(1<<node)]+=p*h
        dist=dict(res)
    return {k:v for k,v in dist.items() if v}


def enumerated_row(edges,state,mu,beta):
    """Algorithm B: exhaustive independent innovation/edge-event coins.

    This independent route intentionally never calls analytical_row or its
    shared hazard helper: it enumerates physical independent trigger events.
    """
    events=[]
    for node in range(4):
        if state>>node&1:continue
        if mu:events.append((node,mu))
        for a,b in edges:
            other=b if node==a else a if node==b else None
            if other is not None and (state>>other)&1 and beta:
                events.append((node,beta))
    out=defaultdict(F)
    for coins in product((0,1),repeat=len(events)):
        p=F(1)
        target=state
        for (node,prob),event in zip(events,coins):
            p*=prob if event else 1-prob
            if event:target|=1<<node
        if p:out[target]+=p
    return dict(out)


def step(dist,edges,mu,beta,method):
    nextdist=defaultdict(F)
    for mask,weight in dist.items():
        transition=method(edges,mask,mu,beta)
        for target,p in transition.items():
            if target&mask!=mask:raise AssertionError("adoption reversed")
            nextdist[target]+=weight*p
    result={k:v for k,v in sorted(nextdist.items()) if v}
    if sum(result.values(),F(0))!=1:
        raise AssertionError("transition not normalized")
    return result


def sequence(edges,seed,mu,beta,method):
    dist={1<<seed:F(1)}
    series=[dist]
    for _ in range(4):
        dist=step(dist,edges,mu,beta,method)
        series.append(dist)
    return series


def tv(p,q):
    return sum((abs(p.get(x,F(0))-q.get(x,F(0))) for x in STATES),F(0))/2


def worlds():
    for name in ("star","path","cycle","complete"):
        for seed in SEEDS:
            for a in RATES:
                for kind in MECHANISMS:
                    yield name,seed,a,kind


def run():
    rows=[]
    bykey={}
    for name,seed,a,kind in worlds():
        mu,beta=parameters(kind,a)
        edges=EDGES[name]
        primary=sequence(edges,seed,mu,beta,analytical_row)
        independently=sequence(edges,seed,mu,beta,enumerated_row)
        if primary!=independently:
            raise AssertionError(f"independent method mismatch: {name} {seed} {a} {kind}")
        key=(name,seed,a,kind)
        bykey[key]=primary
        rows.append({
          "graph":name,"seed":seed,"rate":str(a),"mechanism":kind,
          "independent_full_distribution_agreement":True,
          "time_distributions":[{f"{mask:04b}":str(states.get(mask,F(0))) for mask in STATES}
                                for states in primary],
          "mean_total_adopters":[str(sum((F(mask.bit_count())*pr
                                        for mask,pr in d.items()),F(0)))
                                 for d in primary],
        })
    contrasts=[]
    for graph in ("star","path","cycle","complete"):
        for seed in SEEDS:
            for a in RATES:
                i=bykey[(graph,seed,a,"invention")]
                d=bykey[(graph,seed,a,"diffusion")]
                contrast=[tv(ii,dd) for ii,dd in zip(i,d)]
                contrasts.append({
                  "graph":graph,"seed":seed,"rate":str(a),
                  "TV_by_period":[str(x) for x in contrast],
                })
    assert len(rows)==72 and len(contrasts)==24
    star_center=[c for c in contrasts if c["graph"]=="star" and c["seed"]==0]
    assert len(star_center)==3
    assert all(c["TV_by_period"]==["0"]*5 for c in star_center)
    path_middle=[c for c in contrasts if c["graph"]=="path" and c["seed"]==1]
    assert all(F(c["TV_by_period"][1])>0 for c in path_middle)
    result={
       "research_id":"R174",
       "stage":"BOUNDED_ARTIFICIAL_EXACT_FINITE_MARKOV_E1",
       "catalog_id":"07-016",
       "states":16,"worlds":len(rows),"periods_per_world":5,
       "graph_edges":{k:[list(edge) for edge in v] for k,v in EDGES.items()},
       "rates":[str(x) for x in RATES],
       "mechanisms":list(MECHANISMS),
       "cases":rows,"invention_vs_diffusion_TV":contrasts,
       "primary_nonidentification":"star center-seeded invention and diffusion have identical full joint 0..4 distributions",
       "primary_identification_control":"path seed1, unexposed node3 initially cannot adopt under pure diffusion",
       "real_independent_invention_or_diffusion_verified":False,
       "new_E2":0,"new_E3":0
    }
    OUT.write_text(json.dumps(result,ensure_ascii=False,sort_keys=True,indent=2)+"\n",encoding="utf-8")
    acceptance={
       "research_id":"R174","status":"E1_ARTIFICIAL_EXACT_FINITE_MECHANISM_CLOSED_BOUNDED",
       "original_real_human_data_scored":False,
       "original_Bass_empirical_model_reproduced":False,
       "graphs":len(EDGES),"worlds":len(rows),"time_distributions":len(rows)*5,
       "state_probability_cells":len(rows)*5*16,
       "independent_transition_algorithms":"all 72 worlds x 5 periods x 16 state cells exact Fraction equality",
       "star_center_seed_observational_equivalence":True,
       "path_initially_unexposed_adoption_difference":True,
       "exact_results_sha256":sha256(OUT.read_bytes()).hexdigest(),
       "new_E2":0,"new_E3":0
    }
    ACCEPT.write_text(json.dumps(acceptance,ensure_ascii=False,sort_keys=True,indent=2)+"\n",encoding="utf-8")
    print("R174_FULL_ARTIFICIAL_ACCEPTANCE",json.dumps(acceptance,sort_keys=True))
    print("R174_TV_PATH_SEED1",json.dumps([x for x in contrasts if x["graph"]=="path" and x["seed"]==1],sort_keys=True))
    return result


def archive():
    names=[
      "r174_diffusion_invention_exact.py",
      "R174_EXACT_RESULTS.json",
      "R174_FINAL_MACHINE_ACCEPTANCE.json",
    ]
    with zipfile.ZipFile(ARCH,"w",compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
        for name in names:
            zi=zipfile.ZipInfo(name,date_time=(2026,10,21,0,0,0))
            zi.compress_type=zipfile.ZIP_DEFLATED
            zi.external_attr=0o644<<16
            z.writestr(zi,(HERE/name).read_bytes())
        zi=zipfile.ZipInfo(PROTO.name,date_time=(2026,10,21,0,0,0))
        zi.compress_type=zipfile.ZIP_DEFLATED
        zi.external_attr=0o644<<16
        z.writestr(zi,PROTO.read_bytes())
    print("R174_ARCHIVE_SHA256",sha256(ARCH.read_bytes()).hexdigest())


class TestIndependentTransitionMechanics(unittest.TestCase):
    def test_world_count(self):
        self.assertEqual(len(list(worlds())),72)
    def test_graph_sizes(self):
        self.assertEqual([len(EDGES[x]) for x in ("star","path","cycle","complete")],[3,3,4,6])
    def test_mixed_rule(self):
        self.assertEqual(parameters("mixed",F(3,4)),(F(1,4),F(3,4)))
    def test_initial_state(self):
        self.assertEqual(sequence(EDGES["star"],0,F(1,4),F(0),analytical_row)[0],{1:F(1)})
    def test_no_initial_adopters_under_pure_diffusion(self):
        self.assertEqual(analytical_row(EDGES["path"],0,F(0),F(1,2)),{0:F(1)})
    def test_analytic_vs_event_counter_example(self):
        x=analytical_row(EDGES["path"],2,F(1,4),F(1,2))
        y=enumerated_row(EDGES["path"],2,F(1,4),F(1,2))
        self.assertEqual(x,y)
    def test_same_graph_all_edge_cases(self):
        for edges in EDGES.values():
            for s in STATES:
                for mu,beta in ((F(0),F(0)),(F(1,4),F(1,2)),(F(1),F(1))):
                    self.assertEqual(analytical_row(edges,s,mu,beta),
                                     enumerated_row(edges,s,mu,beta))
    def test_all_adopted_is_absorbing(self):
        for edges in EDGES.values():
            self.assertEqual(analytical_row(edges,15,F(1,2),F(1,2)),{15:F(1)})
    def test_star_center_full_process_identical(self):
        for a in RATES:
            self.assertEqual(sequence(EDGES["star"],0,a,F(0),analytical_row),
                             sequence(EDGES["star"],0,F(0),a,enumerated_row))
    def test_path_unexposed_node_differs(self):
        for a in RATES:
            inv=analytical_row(EDGES["path"],2,a,F(0))
            dif=analytical_row(EDGES["path"],2,F(0),a)
            self.assertEqual(sum((v for k,v in dif.items() if k&8),F(0)),0)
            self.assertEqual(sum((v for k,v in inv.items() if k&8),F(0)),a)
    def test_tv_zero_for_same_distribution(self):
        self.assertEqual(tv({1:F(1,2),3:F(1,2)},{1:F(1,2),3:F(1,2)}),0)
    def test_tv_one_for_disjoint(self):
        self.assertEqual(tv({1:F(1)},{2:F(1)}),1)
    def test_t0_no_data_separation(self):
        for g in EDGES:
            a=sequence(EDGES[g],1,F(1,4),F(0),analytical_row)
            b=sequence(EDGES[g],1,F(0),F(1,4),analytical_row)
            self.assertEqual(a[0],b[0])
    def test_no_adoption_reversal(self):
        for edges in EDGES.values():
            for s in STATES:
                row=enumerated_row(edges,s,F(1,4),F(1,2))
                self.assertTrue(all(mask&s==s for mask in row))
    def test_each_source_distribution_normalized(self):
        for name,seed,a,kind in worlds():
            mu,beta=parameters(kind,a)
            seq=sequence(EDGES[name],seed,mu,beta,analytical_row)
            self.assertTrue(all(sum(v.values(),F(0))==1 for v in seq))
    def test_negative_probability_absent(self):
        for g in EDGES:
            self.assertTrue(all(v>=0 for v in enumerated_row(EDGES[g],3,F(1,4),F(1,2)).values()))


if __name__=="__main__":
    if sys.argv[1:]==["--run-and-archive"]:run();archive()
    elif sys.argv[1:]==["--self-test"]:unittest.main(argv=[sys.argv[0]],verbosity=2)
    else:raise SystemExit("Use --self-test or --run-and-archive")
