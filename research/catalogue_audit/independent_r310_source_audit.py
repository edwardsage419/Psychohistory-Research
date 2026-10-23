#!/usr/bin/env python3
"""No-import independent exact directed-site stochastic voter audit across path/cycle/complete graph."""
from __future__ import annotations
import argparse,csv,hashlib,itertools,json,unittest
from collections import defaultdict
from fractions import Fraction as Q
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]/"research/R310"
SOURCE=ROOT/"R310_ALL_416_ORIGINAL_VOTER_DIRECTED_UPDATE_SOURCES.csv"
RESULT=ROOT/"R310_EXACT_NETWORK_VOTER_MODEL_RESULTS.json"
RECEIPT=ROOT/"R310_MACHINE_RECEIPT.json"
ZERO,ONE=Q(0),Q(1)
N=4
EDGE_SETS={
  "PATH4":{frozenset((0,1)),frozenset((1,2)),frozenset((2,3))},
  "CYCLE4":{frozenset((0,1)),frozenset((1,2)),frozenset((2,3)),frozenset((0,3))},
  "COMPLETE4":{frozenset(pair) for pair in itertools.combinations(range(N),2)}}
# These 4-tuples and edge sets are authored independently of R310 production implementation.
BITS=tuple(itertools.product((0,1),repeat=N))
WORLDS=[(name,b) for name in EDGE_SETS for b in BITS]
FIELDS=("graph","undirected_edges","degree_vector","initial_bits","target_node",
       "copied_neighbor_node","neighbor_prior_bit","original_target_bit","next_bits",
       "directed_update_probability","initial_unweighted_density","next_unweighted_density",
       "initial_degree_weighted_density","next_degree_weighted_density","target_opinion_changed")

def obj(path):return json.loads(path.read_text(encoding="utf-8"))
def read():
    with SOURCE.open(newline="",encoding="utf-8") as f:return list(csv.DictReader(f))
def sorted_edges(g):
    return tuple(sorted(tuple(sorted(e)) for e in EDGE_SETS[g]))
def neighbors(g,v):
    return tuple(sorted((next(iter(e-{v})) for e in EDGE_SETS[g] if v in e)))
def degree(g):return tuple(len(neighbors(g,v)) for v in range(N))
def world_id(g,b):return g+"|bits="+",".join(map(str,b))
def plain(b):return Q(sum(b),4)
def weight(g,b):
    deg=degree(g)
    return Q(sum(x*d for x,d in zip(b,deg)),sum(deg))
def row(g,b,i,j):
    if j not in neighbors(g,i):raise ValueError("invalid arc")
    after=list(b);after[i]=b[j];after=tuple(after)
    d=degree(g)
    x={
      "graph":g,
      "undirected_edges":";".join(f"{u}-{v}" for u,v in sorted_edges(g)),
      "degree_vector":";".join(map(str,d)),
      "initial_bits":";".join(map(str,b)),
      "target_node":i,"copied_neighbor_node":j,
      "neighbor_prior_bit":b[j],"original_target_bit":b[i],
      "next_bits":";".join(map(str,after)),
      "directed_update_probability":Q(1,4*d[i]),
      "initial_unweighted_density":plain(b),"next_unweighted_density":plain(after),
      "initial_degree_weighted_density":weight(g,b),"next_degree_weighted_density":weight(g,after),
      "target_opinion_changed":b[i]!=b[j]}
    return {k:str(x[k]) for k in FIELDS}
def arcs(g):
    return tuple((i,j) for i in range(N) for j in neighbors(g,i))
def aggregate(g,b):
    events=[row(g,b,i,j) for i,j in arcs(g)]
    def expect(k):
        return sum((Q(e["directed_update_probability"])*Q(e[k]) for e in events),ZERO)
    return {"expected_next_unweighted_density":expect("next_unweighted_density"),
      "expected_next_degree_weighted_density":expect("next_degree_weighted_density"),
      "transition_probability_total":expect("directed_update_probability") if False else sum((Q(e["directed_update_probability"]) for e in events),ZERO),
      "change_probability":sum((Q(e["directed_update_probability"]) for e in events if e["target_opinion_changed"]=="True"),ZERO)}

def verify(originals,results):
    if len(originals)!=416 or len(results["worlds"])!=48 or results["full_original_directed_update_rows"]!=416:
        raise AssertionError("wrong full directed update universe")
    universe={(g,b,i,j) for g,b in WORLDS for i,j in arcs(g)}
    found={}
    for item in originals:
        try:
            graph=item["graph"]
            b=tuple(int(x) for x in item["initial_bits"].split(";"))
            i,j=int(item["target_node"]),int(item["copied_neighbor_node"])
            k=(graph,b,i,j)
        except (KeyError,ValueError) as e:raise AssertionError("bad original source") from e
        if k not in universe or k in found:raise AssertionError("unfrozen duplicate/missing source")
        if item["world"]!=world_id(graph,b):raise AssertionError("world source ID error")
        for key,value in row(graph,b,i,j).items():
            if item[key]!=value:raise AssertionError("directed update source corrupted "+key)
        found[k]=item
    if set(found)!=universe:raise AssertionError("original source key set incomplete")
    for ix,(g,b) in enumerate(WORLDS):
        z=results["worlds"][ix]
        if z["world"]!=world_id(g,b) or z["graph"]!=g or z["initial_bits"]!=";".join(map(str,b)):
            raise AssertionError("result identity mismatch")
        if z["degree_vector"]!=";".join(map(str,degree(g))):raise AssertionError("degree vector wrong")
        m=aggregate(g,b)
        if z["original_source_event_count"]!=len(arcs(g)):raise AssertionError("world source count wrong")
        if z["initial_plain_density"]!=str(plain(b)) or z["initial_weighted_density"]!=str(weight(g,b)):
            raise AssertionError("initial density wrong")
        for k in ("expected_next_unweighted_density","expected_next_degree_weighted_density","transition_probability_total","change_probability"):
            if z[k]!=str(m[k]):raise AssertionError("aggregate mismatch "+k)
        if z["events"]!=[row(g,b,i,j) for i,j in arcs(g)]:raise AssertionError("nested source mismatch")
        if m["expected_next_degree_weighted_density"]!=weight(g,b):raise AssertionError("degree-weighted martingale false")
        if g!="PATH4" and m["expected_next_unweighted_density"]!=plain(b):
            raise AssertionError("regular graph plain martingale false")
        if b in ((0,0,0,0),(1,1,1,1)) and m["change_probability"]!=ZERO:
            raise AssertionError("absorbing consensus false")
    references={
      "PATH4_1000_original_plain":"1/4",
      "PATH4_1000_expected_plain":"7/32",
      "PATH4_1000_original_degree_weighted":"1/6",
      "PATH4_1000_expected_degree_weighted":"1/6",
      "CYCLE4_1000_expected_plain":"1/4",
      "COMPLETE4_1000_expected_plain":"1/4",
      "all_48_degree_weighted_expectation_conserved":True,
      "all_regular_graph_unweighted_expectation_conserved":True,
      "both_consensus_configurations_absorbing":True}
    if results["frozen_reference"]!=references:raise AssertionError("preregistered counterexample mutated")
    return {"worlds":48,"all_original_voter_event_sources":416,
      "independent_directed_graph_transition_replay":"PASS",
      "degree_weighted_martingale_all_topologies":"PASS",
      "irregular_path_unweighted_nonmartingale":"PASS",
      "real_elections_or_human_behavior_E2":0,"historical_E3":0}

def audit():
    r,j=obj(RECEIPT),obj(RESULT)
    freeze="782990a1cae101a3c0fd5ba37f89dc8ed9c2078c"
    if r["freeze_commit"]!=freeze or j["freeze_commit"]!=freeze:raise AssertionError("protocol not frozen")
    if j["research_id"]!="R310" or j["original_catalogue_id"]!="04-008":raise AssertionError("wrong research")
    if j["original_Clifford_Sudbury_1973_human_political_votes_reanalyzed"] is not False:raise AssertionError("human original falsely attributed")
    if j["real_human_animal_E2"]!=0 or j["new_historical_E3"]!=0 or r["new_real_E2"]!=0 or r["new_historical_E3"]!=0:
        raise AssertionError("synthetic evidence promoted")
    if r["source_rows"]!=416:raise AssertionError("incorrect source count")
    if hashlib.sha256(SOURCE.read_bytes()).hexdigest()!=r["source_sha256"]:raise AssertionError("source SHA")
    if hashlib.sha256(RESULT.read_bytes()).hexdigest()!=r["results_sha256"]:raise AssertionError("results SHA")
    return {**verify(read(),j),"source_sha256":r["source_sha256"],"results_sha256":r["results_sha256"]}

class Tests(unittest.TestCase):
    def test_all(self):self.assertEqual(audit()["all_original_voter_event_sources"],416)
    def test_universe(self):self.assertEqual(len(WORLDS),48)
    def test_degrees(self):self.assertEqual(degree("PATH4"),(1,2,2,1))
    def test_martingale(self):self.assertEqual(aggregate("PATH4",(1,0,0,0))["expected_next_degree_weighted_density"],Q(1,6))
    def test_path_nonmartingale(self):self.assertEqual(aggregate("PATH4",(1,0,0,0))["expected_next_unweighted_density"],Q(7,32))
    def test_cycle(self):self.assertEqual(aggregate("CYCLE4",(1,0,0,0))["expected_next_unweighted_density"],Q(1,4))
    def test_complete(self):self.assertEqual(aggregate("COMPLETE4",(1,0,0,0))["expected_next_unweighted_density"],Q(1,4))
    def test_absorbing(self):self.assertEqual(aggregate("COMPLETE4",(1,1,1,1))["change_probability"],ZERO)
    def test_arc_not_allowed(self):
        with self.assertRaises(ValueError):row("PATH4",(1,0,0,0),0,3)
    def test_missing(self):
        with self.assertRaises(AssertionError):verify(read()[:-1],obj(RESULT))
    def test_duplicate(self):
        data=read();data[1]=dict(data[0])
        with self.assertRaises(AssertionError):verify(data,obj(RESULT))
    def test_probability_tamper(self):
        data=read();data[1]=dict(data[1]);data[1]["directed_update_probability"]="1"
        with self.assertRaises(AssertionError):verify(data,obj(RESULT))
    def test_next_bits_tamper(self):
        data=read();data[1]=dict(data[1]);data[1]["next_bits"]="1;1;1;1"
        with self.assertRaises(AssertionError):verify(data,obj(RESULT))
    def test_degree_tamper(self):
        data=read();data[1]=dict(data[1]);data[1]["degree_vector"]="2;2;2;2"
        with self.assertRaises(AssertionError):verify(data,obj(RESULT))
    def test_result_tamper(self):
        data=obj(RESULT);data["worlds"][0]["expected_next_unweighted_density"]="9"
        with self.assertRaises(AssertionError):verify(read(),data)
    def test_reference_tamper(self):
        data=obj(RESULT);data["frozen_reference"]["PATH4_1000_expected_plain"]="1/4"
        with self.assertRaises(AssertionError):verify(read(),data)
    def test_SHA_tamper(self):self.assertNotEqual(hashlib.sha256(SOURCE.read_bytes()+b"x").hexdigest(),obj(RECEIPT)["source_sha256"])
if __name__=="__main__":
    p=argparse.ArgumentParser()
    g=p.add_mutually_exclusive_group(required=True)
    g.add_argument("--test",action="store_true");g.add_argument("--audit",action="store_true")
    x=p.parse_args()
    if x.test:unittest.main(argv=["R310 independent"],verbosity=1)
    else:print(json.dumps(audit(),ensure_ascii=False,indent=2))
