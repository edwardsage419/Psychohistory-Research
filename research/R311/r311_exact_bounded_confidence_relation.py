#!/usr/bin/env python3
"""R311 common threshold-confidence adjacency geometry, artificial exact E1. No opinion updates."""
from __future__ import annotations
import argparse,csv,hashlib,itertools,json,unittest
from fractions import Fraction as F
from pathlib import Path
ROOT=Path(__file__).resolve().parent
FREEZE="98f463acd827ab9535ae134c4d22bbe3235da837"
V=(F(0),F(1,2),F(1));E=(F(0),F(1,4),F(1,2),F(1))
PAIRS=tuple(itertools.combinations(range(4),2))
WORLDS=tuple((x,eps) for x in itertools.product(V,repeat=4) for eps in E)
CSVNAME="R311_ALL_1944_ORIGINAL_CONFIDENCE_DYAD_SOURCES.csv"
JSONNAME="R311_EXACT_BOUNDED_CONFIDENCE_GRAPH_RESULTS.json"
RECEIPT="R311_MACHINE_RECEIPT.json"
FIELDS=("world","initial_opinions","confidence_radius","source_i","source_j",
 "opinion_i","opinion_j","absolute_distance","is_confidence_dyad",
 "component_of_i","component_of_j","confidence_edge_count","connected_component_count",
 "fully_pairwise_confident","graph_connected","nontransitive_confidence_witness")
def wid(x,eps):return "opinion="+",".join(map(str,x))+"|epsilon="+str(eps)
def graph(x,eps):
    if (x,eps) not in WORLDS:raise ValueError("outside frozen confidence grid")
    positive={(i,j) for i,j in PAIRS if abs(x[i]-x[j])<=eps}
    # No library graph routines; compute components with BFS.
    unseen=set(range(4));membership=[-1]*4;components=[]
    while unseen:
        first=min(unseen);frontier=[first];component=set()
        while frontier:
            a=frontier.pop()
            if a in component:continue
            component.add(a)
            for i,j in positive:
                if i==a and j not in component:frontier.append(j)
                if j==a and i not in component:frontier.append(i)
        unseen.difference_update(component)
        for i in component:membership[i]=min(component)
        components.append(tuple(sorted(component)))
    witness=any(((min(a,b),max(a,b)) in positive and (min(b,c),max(b,c)) in positive
        and (min(a,c),max(a,c)) not in positive)
        for a,b,c in itertools.permutations(range(4),3))
    return {"edges":positive,"component_membership":tuple(membership),
      "components":tuple(components),"confidence_edge_count":len(positive),
      "connected_component_count":len(components),
      "fully_pairwise_confident":len(positive)==len(PAIRS),
      "graph_connected":len(components)==1,
      "nontransitive_confidence_witness":witness}
def source(x,eps,i,j):
    if (i,j) not in PAIRS:raise ValueError("need frozen unordered distinct dyad")
    g=graph(x,eps)
    return {"world":wid(x,eps),"initial_opinions":";".join(map(str,x)),
        "confidence_radius":eps,"source_i":i,"source_j":j,
        "opinion_i":x[i],"opinion_j":x[j],
        "absolute_distance":abs(x[i]-x[j]),
        "is_confidence_dyad":(i,j) in g["edges"],
        "component_of_i":g["component_membership"][i],
        "component_of_j":g["component_membership"][j],
        "confidence_edge_count":g["confidence_edge_count"],
        "connected_component_count":g["connected_component_count"],
        "fully_pairwise_confident":g["fully_pairwise_confident"],
        "graph_connected":g["graph_connected"],
        "nontransitive_confidence_witness":g["nontransitive_confidence_witness"]}
def all_sources():return tuple(source(x,e,i,j) for x,e in WORLDS for i,j in PAIRS)
def verify():
    assert len(WORLDS)==324 and len(all_sources())==1944
    for x in itertools.product(V,repeat=4):
        previous=set();previous_components=4
        for eps in E:
            g=graph(x,eps)
            assert previous.issubset(g["edges"])
            assert g["connected_component_count"]<=previous_components
            assert g["fully_pairwise_confident"]<=g["graph_connected"]
            assert sum(len(k) for k in g["components"])==4
            assert len(set(g["component_membership"]))==g["connected_component_count"]
            if eps==F(0):
                assert all(((i,j) in g["edges"])==(x[i]==x[j]) for i,j in PAIRS)
            if eps==F(1):
                assert g["confidence_edge_count"]==6 and g["graph_connected"]
            previous=set(g["edges"]);previous_components=g["connected_component_count"]
    ref=(F(0),F(1,2),F(1),F(1))
    assert [graph(ref,e)["confidence_edge_count"] for e in E]==[1,1,4,6]
    assert [graph(ref,e)["connected_component_count"] for e in E]==[3,3,1,1]
    assert graph(ref,F(1,2))["nontransitive_confidence_witness"] is True
    assert graph(ref,F(1,2))["fully_pairwise_confident"] is False
    assert graph(ref,F(1))["fully_pairwise_confident"] is True
    return True
def emit():
    verify();csvpath=ROOT/CSVNAME
    with csvpath.open("w",encoding="utf-8",newline="") as f:
        w=csv.DictWriter(f,fieldnames=FIELDS,lineterminator="\n")
        w.writeheader()
        for x,e in WORLDS:
            for i,j in PAIRS:
                cell=source(x,e,i,j)
                w.writerow({k:str(cell[k]) for k in FIELDS})
    data={"research_id":"R311","original_catalogue_id":"04-011","freeze_commit":FREEZE,
      "scope":"E1_EXACT_ARTIFICIAL_COMMON_BOUNDED_CONFIDENCE_RELATION_GEOMETRY_NO_HK_OR_DEFFUANT_DYNAMICS",
      "artificial_worlds":324,"full_labeled_original_dyad_sources":1944,"agents_per_world":4,
      "distinct_dyads_per_world":6,"real_human_E2":0,"historical_E3":0,
      "R066_existing_HK_and_FJ_unchanged":True,
      "R073":"FROZEN","PESEN_v0_1":"FROZEN",
      "reference":{"example_opinions":["0","1/2","1","1"],
        "edges_by_epsilon":[1,1,4,6],"component_counts_by_epsilon":[3,3,1,1],
        "at_epsilon_half_connected_not_clique":True,"at_epsilon_half_nontransitive":True},
      "worlds":[]}
    for x,eps in WORLDS:
        g=graph(x,eps)
        data["worlds"].append({"world":wid(x,eps),"opinions":[str(i) for i in x],
           "epsilon":str(eps),"edges":[list(pair) for pair in PAIRS if pair in g["edges"]],
           "component_membership":list(g["component_membership"]),
           "components":[list(k) for k in g["components"]],
           "confidence_edge_count":g["confidence_edge_count"],
           "connected_component_count":g["connected_component_count"],
           "fully_pairwise_confident":g["fully_pairwise_confident"],
           "graph_connected":g["graph_connected"],
           "nontransitive_confidence_witness":g["nontransitive_confidence_witness"],
           "six_original_dyad_sources":[{k:str(source(x,eps,i,j)[k]) for k in FIELDS if k!="world"} for i,j in PAIRS]})
    resultpath=ROOT/JSONNAME
    resultpath.write_text(json.dumps(data,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    receipt={"research_id":"R311","freeze_commit":FREEZE,"original_sources":1944,
      "source_sha256":hashlib.sha256(csvpath.read_bytes()).hexdigest(),
      "result_sha256":hashlib.sha256(resultpath.read_bytes()).hexdigest(),
      "new_real_E2":0,"new_historical_E3":0}
    (ROOT/RECEIPT).write_text(json.dumps(receipt,indent=2)+"\n",encoding="utf-8")
    return receipt
class Tests(unittest.TestCase):
    def test_complete(self):self.assertTrue(verify())
    def test_worlds(self):self.assertEqual(len(WORLDS),324)
    def test_pairs(self):self.assertEqual(len(PAIRS),6)
    def test_sources(self):self.assertEqual(len(all_sources()),1944)
    def test_example_edges(self):self.assertEqual(graph((F(0),F(1,2),F(1),F(1)),F(1,2))["confidence_edge_count"],4)
    def test_example_components(self):self.assertEqual(graph((F(0),F(1,2),F(1),F(1)),F(1,2))["connected_component_count"],1)
    def test_nontransitive(self):self.assertTrue(graph((F(0),F(1,2),F(1),F(1)),F(1,2))["nontransitive_confidence_witness"])
    def test_not_clique(self):self.assertFalse(graph((F(0),F(1,2),F(1),F(1)),F(1,2))["fully_pairwise_confident"])
    def test_inclusive_boundary(self):self.assertTrue(source((F(0),F(1,2),F(1),F(1)),F(1,2),0,1)["is_confidence_dyad"])
    def test_zero_eps(self):self.assertFalse(source((F(0),F(1,2),F(1),F(1)),F(0),0,1)["is_confidence_dyad"])
    def test_complete_eps(self):self.assertTrue(graph((F(0),)*4,F(1))["fully_pairwise_confident"])
    def test_bad_world(self):
        with self.assertRaises(ValueError):graph((F(0),F(0),F(0),F(1,4)),F(1,2))
    def test_bad_dyad(self):
        with self.assertRaises(ValueError):source((F(0),)*4,F(0),0,0)
def generated(x,e,i,j,k):
    def check(self):
        d=source(x,e,i,j);g=graph(x,e)
        if k=="dist":self.assertEqual(d["absolute_distance"],abs(x[i]-x[j]))
        elif k=="edge":self.assertEqual(d["is_confidence_dyad"],(i,j) in g["edges"])
        elif k=="comp":self.assertEqual(d["component_of_i"],g["component_membership"][i])
        else:raise AssertionError(k)
    return check
for a,(x,e) in enumerate(WORLDS):
    for i,j in PAIRS:
        for k in ("dist","edge","comp"):
            setattr(Tests,f"test_world{a}_dyad{i}_{j}_{k}",generated(x,e,i,j,k))
if __name__=="__main__":
    p=argparse.ArgumentParser();g=p.add_mutually_exclusive_group(required=True)
    g.add_argument("--test",action="store_true");g.add_argument("--emit",action="store_true")
    a=p.parse_args()
    if a.test:unittest.main(argv=["R311"],verbosity=1)
    else:print(json.dumps(emit(),indent=2))
