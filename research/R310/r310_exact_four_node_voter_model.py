#!/usr/bin/env python3
"""R310 asynchronous site-update voter model on three exact four-node synthetic graph topologies."""
from __future__ import annotations
import argparse,csv,hashlib,itertools,json,unittest
from fractions import Fraction as F
from pathlib import Path
ROOT=Path(__file__).resolve().parent
FREEZE="782990a1cae101a3c0fd5ba37f89dc8ed9c2078c"
N=4;Z,O=F(0),F(1)
GRAPHS={
  "PATH4":((0,1),(1,2),(2,3)),
  "CYCLE4":((0,1),(1,2),(2,3),(0,3)),
  "COMPLETE4":tuple(itertools.combinations(range(N),2))}
BITS=tuple(itertools.product((0,1),repeat=N))
WORLDS=tuple((graph,bits) for graph in GRAPHS for bits in BITS)
SOURCE_NAME="R310_ALL_416_ORIGINAL_VOTER_DIRECTED_UPDATE_SOURCES.csv"
RESULT_NAME="R310_EXACT_NETWORK_VOTER_MODEL_RESULTS.json"
RECEIPT_NAME="R310_MACHINE_RECEIPT.json"

def adj(name):
    if name not in GRAPHS:raise ValueError("graph not frozen")
    return tuple(tuple(sorted(j if i==v else i for i,j in GRAPHS[name] if i==v or j==v)) for v in range(N))
def degree(name):return tuple(len(x) for x in adj(name))
def identifier(name,bits):return name+"|bits="+",".join(map(str,bits))
def plain(bits):return F(sum(bits),N)
def weighted(graph,bits):
    d=degree(graph)
    return F(sum(v*k for v,k in zip(bits,d)),sum(d))
def source(graph,bits,target,neighbor):
    if (graph,bits) not in WORLDS or target not in range(N) or neighbor not in adj(graph)[target]:raise ValueError("not frozen source")
    nxt=list(bits);nxt[target]=bits[neighbor];nxt=tuple(nxt)
    d=degree(graph)
    return {"world":identifier(graph,bits),"graph":graph,
       "undirected_edges":";".join(f"{i}-{j}" for i,j in GRAPHS[graph]),
       "degree_vector":";".join(map(str,d)),
       "initial_bits":";".join(map(str,bits)),
       "target_node":target,"copied_neighbor_node":neighbor,
       "neighbor_prior_bit":bits[neighbor],"original_target_bit":bits[target],
       "next_bits":";".join(map(str,nxt)),
       "directed_update_probability":F(1,N*d[target]),
       "initial_unweighted_density":plain(bits),
       "next_unweighted_density":plain(nxt),
       "initial_degree_weighted_density":weighted(graph,bits),
       "next_degree_weighted_density":weighted(graph,nxt),
       "target_opinion_changed":bits[target]!=bits[neighbor]}
def rows(graph,bits):
    return tuple(source(graph,bits,i,j) for i,neighbors in enumerate(adj(graph)) for j in neighbors)
def moments(graph,bits):
    rr=rows(graph,bits)
    return {"expected_next_unweighted_density":sum((r["directed_update_probability"]*r["next_unweighted_density"] for r in rr),Z),
      "expected_next_degree_weighted_density":sum((r["directed_update_probability"]*r["next_degree_weighted_density"] for r in rr),Z),
      "transition_probability_total":sum((r["directed_update_probability"] for r in rr),Z),
      "change_probability":sum((r["directed_update_probability"] for r in rr if r["target_opinion_changed"]),Z)}
def originals():return tuple(r for g,b in WORLDS for r in rows(g,b))
def verify():
    assert len(BITS)==16 and len(WORLDS)==48 and len(originals())==416
    assert tuple(degree(x) for x in GRAPHS)==((1,2,2,1),(2,2,2,2),(3,3,3,3))
    assert len({(r["world"],r["target_node"],r["copied_neighbor_node"]) for r in originals()})==416
    for g,b in WORLDS:
        m=moments(g,b)
        assert m["transition_probability_total"]==O
        assert m["expected_next_degree_weighted_density"]==weighted(g,b)
        if g!="PATH4":assert m["expected_next_unweighted_density"]==plain(b)
        if b in ((0,)*N,(1,)*N):
            assert m["change_probability"]==Z
            assert all(not r["target_opinion_changed"] for r in rows(g,b))
        for r in rows(g,b):
            assert r["next_unweighted_density"]>=Z and r["next_unweighted_density"]<=O
            before=tuple(int(x) for x in r["initial_bits"].split(";"))
            after=tuple(int(x) for x in r["next_bits"].split(";"))
            assert sum(u!=v for u,v in zip(before,after))<=1
    p=("PATH4",(1,0,0,0))
    assert plain(p[1])==F(1,4)
    assert moments(*p)["expected_next_unweighted_density"]==F(7,32)
    assert weighted(*p)==F(1,6)
    assert moments(*p)["expected_next_degree_weighted_density"]==F(1,6)
    assert moments("CYCLE4",p[1])["expected_next_unweighted_density"]==F(1,4)
    assert moments("COMPLETE4",p[1])["expected_next_unweighted_density"]==F(1,4)
    return True
def emit():
    verify()
    cols=("world","graph","undirected_edges","degree_vector","initial_bits","target_node",
       "copied_neighbor_node","neighbor_prior_bit","original_target_bit","next_bits",
       "directed_update_probability","initial_unweighted_density","next_unweighted_density",
       "initial_degree_weighted_density","next_degree_weighted_density","target_opinion_changed")
    spath=ROOT/SOURCE_NAME
    with spath.open("w",encoding="utf-8",newline="") as f:
        w=csv.DictWriter(f,fieldnames=cols,lineterminator="\n");w.writeheader()
        for x in originals():w.writerow({k:str(x[k]) for k in cols})
    j={"research_id":"R310","original_catalogue_id":"04-008","freeze_commit":FREEZE,
       "scope":"E1_PROJECT_FINITE_FOUR_NODE_ASYNCHRONOUS_SITE_UPDATE_VOTER_GRAPH_COPYING",
       "synthetic_worlds":48,"full_original_directed_update_rows":416,
       "synthetic_graph_count":3,"artificial_node_count":4,
       "original_Clifford_Sudbury_1973_human_political_votes_reanalyzed":False,
       "model_stochastic_copying_not_real_political_elections":True,
       "real_human_animal_E2":0,"new_historical_E3":0,
       "R073":"FROZEN","PESEN_v0_1":"FROZEN","worlds":[]}
    for g,b in WORLDS:
        m=moments(g,b)
        j["worlds"].append({"world":identifier(g,b),"graph":g,
          "initial_bits":";".join(map(str,b)),
          "degree_vector":";".join(map(str,degree(g))),
          "original_source_event_count":len(rows(g,b)),
          "initial_plain_density":str(plain(b)),
          "initial_weighted_density":str(weighted(g,b)),
          "expected_next_unweighted_density":str(m["expected_next_unweighted_density"]),
          "expected_next_degree_weighted_density":str(m["expected_next_degree_weighted_density"]),
          "transition_probability_total":str(m["transition_probability_total"]),
          "change_probability":str(m["change_probability"]),
          "events":[{k:str(r[k]) for k in cols if k!="world"} for r in rows(g,b)]})
    j["frozen_reference"]={
      "PATH4_1000_original_plain":"1/4",
      "PATH4_1000_expected_plain":"7/32",
      "PATH4_1000_original_degree_weighted":"1/6",
      "PATH4_1000_expected_degree_weighted":"1/6",
      "CYCLE4_1000_expected_plain":"1/4",
      "COMPLETE4_1000_expected_plain":"1/4",
      "all_48_degree_weighted_expectation_conserved":True,
      "all_regular_graph_unweighted_expectation_conserved":True,
      "both_consensus_configurations_absorbing":True}
    rpath=ROOT/RESULT_NAME
    rpath.write_text(json.dumps(j,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    rec={"research_id":"R310","freeze_commit":FREEZE,"source_rows":416,
       "source_sha256":hashlib.sha256(spath.read_bytes()).hexdigest(),
       "results_sha256":hashlib.sha256(rpath.read_bytes()).hexdigest(),
       "new_real_E2":0,"new_historical_E3":0}
    (ROOT/RECEIPT_NAME).write_text(json.dumps(rec,indent=2)+"\n",encoding="utf-8")
    return rec

class Tests(unittest.TestCase):
    def test_all(self):self.assertTrue(verify())
    def test_worlds(self):self.assertEqual(len(WORLDS),48)
    def test_source_universe(self):self.assertEqual(len(originals()),416)
    def test_path_degree(self):self.assertEqual(degree("PATH4"),(1,2,2,1))
    def test_cycle_degree(self):self.assertEqual(degree("CYCLE4"),(2,2,2,2))
    def test_complete_degree(self):self.assertEqual(degree("COMPLETE4"),(3,3,3,3))
    def test_path_unweighted_nonmartingale(self):self.assertNotEqual(moments("PATH4",(1,0,0,0))["expected_next_unweighted_density"],F(1,4))
    def test_path_degree_martingale(self):self.assertEqual(moments("PATH4",(1,0,0,0))["expected_next_degree_weighted_density"],F(1,6))
    def test_consensus(self):self.assertEqual(moments("PATH4",(0,0,0,0))["change_probability"],Z)
    def test_regular(self):self.assertEqual(moments("COMPLETE4",(1,0,0,0))["expected_next_unweighted_density"],F(1,4))
    def test_invalid_graph(self):
        with self.assertRaises(ValueError):degree("STAR4")
    def test_invalid_neighbor(self):
        with self.assertRaises(ValueError):source("PATH4",(1,0,0,0),0,3)
    def test_invalid_bits(self):
        with self.assertRaises(ValueError):source("PATH4",(1,0,0,2),0,1)
    def test_undirected_pair_reverses(self):self.assertIn(0,adj("PATH4")[1])
def generated(world,target,neighbor,kind):
    def f(self):
        g,b=world
        z=source(g,b,target,neighbor)
        if kind=="prob":self.assertEqual(z["directed_update_probability"],F(1,4*degree(g)[target]))
        elif kind=="next":self.assertEqual(z["neighbor_prior_bit"],b[neighbor])
        elif kind=="weighted":self.assertEqual(z["initial_degree_weighted_density"],weighted(g,b))
        else:raise AssertionError(kind)
    return f
for w in WORLDS:
    for i,near in enumerate(adj(w[0])):
        for j in near:
            for kind in ("prob","next","weighted"):
                setattr(Tests,f"test_{w[0]}_{''.join(map(str,w[1]))}_{i}_{j}_{kind}",generated(w,i,j,kind))
if __name__=="__main__":
    p=argparse.ArgumentParser()
    m=p.add_mutually_exclusive_group(required=True)
    m.add_argument("--test",action="store_true");m.add_argument("--emit",action="store_true")
    x=p.parse_args()
    if x.test:unittest.main(argv=["R310"],verbosity=1)
    else:print(json.dumps(emit(),indent=2))
