#!/usr/bin/env python3
"""R311 independent union-find exact source proof; does not import project model."""
import argparse,csv,hashlib,itertools,json,unittest
from fractions import Fraction as Q
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]/"research/R311"
CSV=ROOT/"R311_ALL_1944_ORIGINAL_CONFIDENCE_DYAD_SOURCES.csv"
RESULT=ROOT/"R311_EXACT_BOUNDED_CONFIDENCE_GRAPH_RESULTS.json"
RECEIPT=ROOT/"R311_MACHINE_RECEIPT.json"
VAL=(Q(0),Q(1,2),Q(1));EPS=(Q(0),Q(1,4),Q(1,2),Q(1))
PAIRS=list(itertools.combinations(range(4),2))
WORLDS=list((x,e) for x in itertools.product(VAL,repeat=4) for e in EPS)
def obj(p):return json.loads(p.read_text(encoding="utf-8"))
def load():
    with CSV.open(encoding="utf-8",newline="") as f:return list(csv.DictReader(f))
def wid(x,e):return "opinion="+",".join(map(str,x))+"|epsilon="+str(e)
def independent(x,e):
    parents=list(range(4));edges=[]
    def root(i):
        while i!=parents[i]:i=parents[i]
        return i
    for i,j in PAIRS:
        if abs(x[i]-x[j])<=e:
            edges.append((i,j))
            a,b=root(i),root(j)
            if a!=b:parents[max(a,b)]=min(a,b)
    groups={}
    for i in range(4):groups.setdefault(root(i),[]).append(i)
    components=tuple(tuple(g) for g in sorted(groups.values(),key=min))
    belongs=tuple(min(next(g for g in components if i in g)) for i in range(4))
    edge_set=set(edges)
    witness=any((min(a,b),max(a,b)) in edge_set and
        (min(b,c),max(b,c)) in edge_set and
        (min(a,c),max(a,c)) not in edge_set
        for a,b,c in itertools.permutations(range(4),3))
    return edges,components,belongs,witness
def source(x,e,i,j):
    edges,groups,belongs,wit=independent(x,e)
    d={"world":wid(x,e),"initial_opinions":";".join(map(str,x)),
     "confidence_radius":e,"source_i":i,"source_j":j,
     "opinion_i":x[i],"opinion_j":x[j],"absolute_distance":abs(x[i]-x[j]),
     "is_confidence_dyad":(i,j) in edges,
     "component_of_i":belongs[i],"component_of_j":belongs[j],
     "confidence_edge_count":len(edges),"connected_component_count":len(groups),
     "fully_pairwise_confident":len(edges)==6,
     "graph_connected":len(groups)==1,
     "nontransitive_confidence_witness":wit}
    return {k:str(v) for k,v in d.items()}
def verify(rows,j):
    if len(rows)!=1944 or len(j["worlds"])!=324:raise AssertionError("count")
    expected={(x,e,i,h) for x,e in WORLDS for i,h in PAIRS}
    seen=set()
    for r in rows:
        x=tuple(Q(v) for v in r["initial_opinions"].split(";"))
        e=Q(r["confidence_radius"]);i,h=int(r["source_i"]),int(r["source_j"])
        key=(x,e,i,h)
        if key not in expected or key in seen:raise AssertionError("identity")
        if r!=source(x,e,i,h):raise AssertionError("source")
        seen.add(key)
    if seen!=expected:raise AssertionError("missing")
    for k,(x,e) in enumerate(WORLDS):
        z=j["worlds"][k];edges,groups,belong,wit=independent(x,e)
        if z["world"]!=wid(x,e) or z["opinions"]!=list(map(str,x)) or z["epsilon"]!=str(e):raise AssertionError("world")
        if z["edges"]!=[list(t) for t in edges] or z["components"]!=[list(t) for t in groups] or z["component_membership"]!=list(belong):raise AssertionError("graph")
        if z["confidence_edge_count"]!=len(edges) or z["connected_component_count"]!=len(groups):raise AssertionError("counts")
        if z["graph_connected"]!=(len(groups)==1) or z["fully_pairwise_confident"]!=(len(edges)==6) or z["nontransitive_confidence_witness"]!=wit:raise AssertionError("property")
        if z["six_original_dyad_sources"]!=[{key:value for key,value in source(x,e,i,h).items() if key!="world"} for i,h in PAIRS]:raise AssertionError("world sources")
    for x in itertools.product(VAL,repeat=4):
        previous=set();previous_n=4
        for e in EPS:
            edges,groups,_,_=independent(x,e)
            if not previous.issubset(edges) or len(groups)>previous_n:raise AssertionError("threshold monotonicity")
            previous=set(edges);previous_n=len(groups)
    return {"worlds":324,"full_original_sources":1944,"independent_union_find":"PASS","new_E2":0,"new_E3":0}
def audit():
    receipt,j=obj(RECEIPT),obj(RESULT)
    if receipt["freeze_commit"]!="98f463acd827ab9535ae134c4d22bbe3235da837":raise AssertionError("freeze")
    if j["research_id"]!="R311" or j["original_catalogue_id"]!="04-011":raise AssertionError("catalogue")
    if receipt["original_sources"]!=1944 or j["full_labeled_original_dyad_sources"]!=1944 or receipt["new_real_E2"]!=0:raise AssertionError("scope")
    if hashlib.sha256(CSV.read_bytes()).hexdigest()!=receipt["source_sha256"]:raise AssertionError("csv digest")
    if hashlib.sha256(RESULT.read_bytes()).hexdigest()!=receipt["result_sha256"]:raise AssertionError("json digest")
    return verify(load(),j)
class Tests(unittest.TestCase):
    def test_all(self):self.assertEqual(audit()["full_original_sources"],1944)
    def test_ref0(self):self.assertEqual(len(independent((Q(0),Q(1,2),Q(1),Q(1)),Q(0))[0]),1)
    def test_refhalf(self):self.assertEqual(len(independent((Q(0),Q(1,2),Q(1),Q(1)),Q(1,2))[0]),4)
    def test_nontransitive(self):self.assertTrue(independent((Q(0),Q(1,2),Q(1),Q(1)),Q(1,2))[3])
    def test_connected_not_clique(self):
        e,c,_,_=independent((Q(0),Q(1,2),Q(1),Q(1)),Q(1,2))
        self.assertEqual((len(e),len(c)),(4,1))
    def test_missing(self):
        with self.assertRaises(AssertionError):verify(load()[:-1],obj(RESULT))
    def test_duplicate(self):
        rows=load();rows[1]=dict(rows[0])
        with self.assertRaises(AssertionError):verify(rows,obj(RESULT))
    def test_edge_change(self):
        rows=load();rows[0]=dict(rows[0]);rows[0]["is_confidence_dyad"]="incorrect"
        with self.assertRaises(AssertionError):verify(rows,obj(RESULT))
    def test_id_change(self):
        rows=load();rows[0]=dict(rows[0]);rows[0]["source_j"]="0"
        with self.assertRaises(AssertionError):verify(rows,obj(RESULT))
    def test_distance_change(self):
        rows=load();rows[0]=dict(rows[0]);rows[0]["absolute_distance"]="3"
        with self.assertRaises(AssertionError):verify(rows,obj(RESULT))
    def test_graph_change(self):
        j=obj(RESULT);j["worlds"][0]["connected_component_count"]=5
        with self.assertRaises(AssertionError):verify(load(),j)
    def test_digest(self):self.assertNotEqual(hashlib.sha256(CSV.read_bytes()+b"x").hexdigest(),obj(RECEIPT)["source_sha256"])
if __name__=="__main__":
    p=argparse.ArgumentParser();g=p.add_mutually_exclusive_group(required=True)
    g.add_argument("--test",action="store_true");g.add_argument("--audit",action="store_true")
    a=p.parse_args()
    if a.test:unittest.main(argv=["R311 audit"],verbosity=1)
    else:print(json.dumps(audit(),indent=2))
