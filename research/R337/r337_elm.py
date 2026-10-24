"""R337 finite constructed route gating versus additive cue model."""
import argparse
import csv
import io
import json
import unittest
from itertools import product
from pathlib import Path
ROOT=Path(__file__).resolve().parent
SOURCE=ROOT/"R337_ALL_64_ARTIFICIAL_ARGUMENT_CUE_ATOMS.csv"
RESULT=ROOT/"R337_EXACT_32_CONDITIONS.json"
HEADER=["involvement","ability","argument_quality","source_cue","cue_visible","policy","central_gate","score"]
EXPECTED={"worlds":32,"rows":64,"central_worlds":8,"other_worlds":24,"low_no_cue_zero":12,"quality_pairs_central":4,"quality_pairs_low":12,"cue_pairs_central":2,"cue_pairs_low":6,"agreement":2,"disagreement":30}
def build():
    rows,worlds=[],[]
    checks={k:0 for k in EXPECTED}
    for i,b,q,e,c in product((0,1),(0,1),(-1,1),(-1,1),(0,1)):
        g=i*b
        route=2*q if g else c*e
        fixed=q+c*e
        worlds.append(dict(involvement=i,ability=b,argument_quality=q,source_cue=e,cue_visible=c,central_gate=g,route_score=route,fixed_score=fixed))
        rows.extend([[i,b,q,e,c,"ROUTE_GATE",g,route],[i,b,q,e,c,"FIXED_ADDITIVE",g,fixed]])
        checks["worlds"]+=1
        checks["rows"]+=2
        checks["central_worlds"]+=g
        checks["other_worlds"]+=1-g
        checks["low_no_cue_zero"]+=int(not g and not c and route==0)
        checks["quality_pairs_central"]+=int(q==1 and bool(g))
        checks["quality_pairs_low"]+=int(q==1 and not g)
        checks["cue_pairs_central"]+=int(e==1 and c==1 and bool(g))
        checks["cue_pairs_low"]+=int(e==1 and c==1 and not g)
        checks["agreement"]+=int(route==fixed)
        checks["disagreement"]+=int(route!=fixed)
    return rows,{"schema":"R337_frozen_binary_route_gate_v1","conditions":worlds,"checks":checks}
def render():
    rows,obj=build()
    stream=io.StringIO(newline="")
    writer=csv.writer(stream,lineterminator="\n")
    writer.writerow(HEADER)
    writer.writerows(rows)
    return stream.getvalue().encode(),(json.dumps(obj,indent=2,ensure_ascii=True)+"\n").encode()
def audit():
    a,b=render()
    assert SOURCE.read_bytes()==a,"source byte mismatch"
    assert RESULT.read_bytes()==b,"results byte mismatch"
    assert build()[1]["checks"]==EXPECTED
class Tests(unittest.TestCase):
    def test_counts(self):self.assertEqual(build()[1]["checks"],EXPECTED)
    def test_unique_worlds(self):
        w=build()[1]["conditions"]
        self.assertEqual(len({(x["involvement"],x["ability"],x["argument_quality"],x["source_cue"],x["cue_visible"]) for x in w}),32)
    def test_central_cue_invariance(self):
        w=build()[1]["conditions"]
        self.assertTrue(all(x["route_score"]==2*x["argument_quality"] for x in w if x["central_gate"]))
    def test_low_argument_invariance(self):
        w=build()[1]["conditions"]
        self.assertTrue(all(x["route_score"]==x["cue_visible"]*x["source_cue"] for x in w if not x["central_gate"]))
    def test_exact_pairs(self):
        w=build()[1]["conditions"]
        get=lambda i,b,q,e,c:next(x["route_score"] for x in w if (x["involvement"],x["ability"],x["argument_quality"],x["source_cue"],x["cue_visible"])==(i,b,q,e,c))
        self.assertEqual((get(1,1,1,1,1)-get(1,1,-1,1,1),get(0,1,1,1,1)-get(0,1,-1,1,1)),(4,0))
        self.assertEqual((get(1,1,1,1,1)-get(1,1,1,-1,1),get(0,1,1,1,1)-get(0,1,1,-1,1)),(0,2))
    def test_byte_replay(self):audit()
if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--test",action="store_true")
    p.add_argument("--audit",action="store_true")
    args=p.parse_args()
    if args.test:
        r=unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(Tests))
        if not r.wasSuccessful():raise SystemExit(1)
    if args.audit:
        audit()
        print("R337 PRODUCTION_REPLAY_PASS 64 artificial atoms 32 worlds")
