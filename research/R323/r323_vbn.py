#!/usr/bin/env python3
"""R323: project-constructed finite VBN mediation counterexample, artificial E1."""
from __future__ import annotations
import argparse,csv,io,itertools,json,unittest
from fractions import Fraction as F
from pathlib import Path
HERE=Path(__file__).resolve().parent
CSV=HERE/"R323_ALL_128_ORIGINAL_VBN_STATES.csv"
JSON=HERE/"R323_EXACT_FOUR_VBN_WORLDS.json"
POLICIES=("vbn_cascade","direct_product","unconstrained_norm","value_feasible")
FIELDS=("world_id","policy","V","T","R","E","C","weight","latent_norm","action")
STATES=tuple(itertools.product((0,1),repeat=5))
def decide(policy,V,T,R,E,C):
    if policy not in POLICIES or any(x not in (0,1) for x in (V,T,R,E,C)):raise ValueError("invalid state")
    if policy=="vbn_cascade":
        n=V*T*R*E;return n,n*C
    if policy=="direct_product":return 0,V*T*R*E*C
    if policy=="unconstrained_norm":
        n=V*T*R*E;return n,n
    return V,V*C
def generate():
    rows=[];worlds=[]
    for i,policy in enumerate(POLICIES):
        norms=acts=c0=0
        for V,T,R,E,C in STATES:
            n,a=decide(policy,V,T,R,E,C)
            norms+=n;acts+=a;c0+=int(C==0 and a==1)
            rows.append(dict(zip(FIELDS,map(str,(i,policy,V,T,R,E,C,F(1,32),n,a)))))
        worlds.append({"world_id":i,"policy":policy,"state_count":32,
            "personal_norm_positive_count":norms,"action_positive_count":acts,
            "personal_norm_rate":str(F(norms,32)),"action_rate":str(F(acts,32)),
            "action_when_C_zero_count":c0})
    pairs={}
    for i,p in enumerate(POLICIES):
        for q in POLICIES[i+1:]:
            pairs[p+"|"+q]=sum(decide(p,*s)[1]!=decide(q,*s)[1] for s in STATES)
    return rows,{"schema":"r323_schematic_vbn_mediation_e1_v1","original_catalogue_id":"01-015",
        "artificial_schematic_only":True,"original_source_rows":128,"worlds":worlds,
        "pairwise_action_disagreement_counts":pairs}
def csv_text(rows):
    f=io.StringIO(newline="");w=csv.DictWriter(f,fieldnames=FIELDS,lineterminator="\n")
    w.writeheader();w.writerows(rows);return f.getvalue()
def json_text(o):return json.dumps(o,indent=2,ensure_ascii=False)+"\n"
def verify_source(c,j):
    rows,obj=generate()
    if c!=csv_text(rows):raise AssertionError("original state bytes differ")
    if json.loads(j)!=obj:raise AssertionError("world results differ")
    return True
def replay():return verify_source(CSV.read_text(encoding="utf-8"),JSON.read_text(encoding="utf-8"))
def world(p):return next(w for w in generate()[1]["worlds"] if w["policy"]==p)
class Tests(unittest.TestCase):
    def test_01_policies(self):self.assertEqual(len(POLICIES),4)
    def test_02_states(self):self.assertEqual(len(STATES),32)
    def test_03_rows(self):self.assertEqual(len(generate()[0]),128)
    def test_04_unique(self):self.assertEqual(len({tuple(r[x] for x in FIELDS[:7]) for r in generate()[0]}),128)
    def test_05_mass(self):
        for i in range(4):self.assertEqual(sum((F(r["weight"]) for r in generate()[0] if r["world_id"]==str(i)),F(0)),1)
    def test_06_uniform(self):self.assertTrue(all(r["weight"]=="1/32" for r in generate()[0]))
    def test_07_cascade_norm(self):self.assertEqual(world("vbn_cascade")["personal_norm_positive_count"],2)
    def test_08_cascade_action(self):self.assertEqual(world("vbn_cascade")["action_positive_count"],1)
    def test_09_direct_norm(self):self.assertEqual(world("direct_product")["personal_norm_positive_count"],0)
    def test_10_direct_action(self):self.assertEqual(world("direct_product")["action_positive_count"],1)
    def test_11_unconstrained_action(self):self.assertEqual(world("unconstrained_norm")["action_positive_count"],2)
    def test_12_value_action(self):self.assertEqual(world("value_feasible")["action_positive_count"],8)
    def test_13_cascade_constraint(self):self.assertEqual(world("vbn_cascade")["action_when_C_zero_count"],0)
    def test_14_unconstrained_c0(self):self.assertEqual(world("unconstrained_norm")["action_when_C_zero_count"],1)
    def test_15_direct_equal(self):
        for s in STATES:self.assertEqual(decide("vbn_cascade",*s)[1],decide("direct_product",*s)[1])
    def test_16_norm_difference(self):self.assertEqual(sum(decide("vbn_cascade",*s)[0]!=decide("direct_product",*s)[0] for s in STATES),2)
    def test_17_pair_equiv(self):self.assertEqual(generate()[1]["pairwise_action_disagreement_counts"]["vbn_cascade|direct_product"],0)
    def test_18_pair_unconstrained(self):self.assertEqual(generate()[1]["pairwise_action_disagreement_counts"]["vbn_cascade|unconstrained_norm"],1)
    def test_19_pair_value(self):self.assertEqual(generate()[1]["pairwise_action_disagreement_counts"]["vbn_cascade|value_feasible"],7)
    def test_20_pair_count(self):self.assertEqual(len(generate()[1]["pairwise_action_disagreement_counts"]),6)
    def test_21_all_zero(self):
        for p in POLICIES:self.assertEqual(decide(p,0,0,0,0,0)[1],0)
    def test_22_all_one(self):
        for p in POLICIES:self.assertEqual(decide(p,1,1,1,1,1)[1],1)
    def test_23_norm_when_C0(self):self.assertEqual(decide("vbn_cascade",1,1,1,1,0),(1,0))
    def test_24_direct_when_C0(self):self.assertEqual(decide("direct_product",1,1,1,1,0),(0,0))
    def test_25_value_only(self):self.assertEqual(decide("value_feasible",1,0,0,0,1),(1,1))
    def test_26_invalid(self):
        with self.assertRaises(ValueError):decide("other",1,1,1,1,1)
    def test_27_replay(self):self.assertTrue(replay())
    def test_28_corrupt(self):
        c=csv_text(generate()[0]);j=json_text(generate()[1])
        with self.assertRaises(AssertionError):verify_source(c.replace("1/32","1/16",1),j)
    def test_29_binary(self):self.assertTrue(all(r["action"] in ("0","1") for r in generate()[0]))
    def test_30_meta(self):self.assertEqual(generate()[1]["original_catalogue_id"],"01-015")
if __name__=="__main__":
    p=argparse.ArgumentParser();p.add_argument("--write",action="store_true")
    p.add_argument("--test",action="store_true");p.add_argument("--audit",action="store_true")
    a=p.parse_args()
    if a.write:
        r,o=generate();CSV.write_text(csv_text(r),encoding="utf-8");JSON.write_text(json_text(o),encoding="utf-8");print("WROTE",len(r))
    elif a.audit:print("R323_REPLAY_PASS",replay())
    elif a.test:unittest.main(argv=["r323"],verbosity=2)
    else:p.print_help()
