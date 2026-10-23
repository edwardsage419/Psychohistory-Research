#!/usr/bin/env python3
"""R322 finite schematic default/intervention and observational equivalence E1."""
from __future__ import annotations
import argparse,csv,io,itertools,json,unittest
from fractions import Fraction as F
from pathlib import Path
HERE=Path(__file__).resolve().parent
CSV=HERE/"R322_ALL_256_ORIGINAL_BINARY_STATES.csv"
JSON=HERE/"R322_EXACT_FOUR_POLICY_WORLDS.json"
POLICIES=("default_only","gated_intervention","analytic_only","lookup_equivalent")
FIELDS=("world_id","policy","h","a","y","d","r","w","weight","output","correct","intervention")
STATES=tuple(itertools.product((0,1),repeat=6))
def choose(policy,h,a,d,r,w):
    if policy not in POLICIES or any(v not in (0,1) for v in (h,a,d,r,w)):
        raise ValueError("outside frozen state")
    if policy=="default_only":return h,0
    if policy=="analytic_only":return a,1
    if policy=="gated_intervention":
        gate=int(h!=a and d==r==w==1)
        return (a if gate else h),gate
    return h^((h^a)&d&r&w),0
def generate():
    rows=[];worlds=[]
    for wid,policy in enumerate(POLICIES):
        correct=changed=intervened=0
        for h,a,y,d,r,w in STATES:
            out,intervention=choose(policy,h,a,d,r,w)
            correct+=int(out==y);changed+=int(out!=h);intervened+=intervention
            rows.append(dict(zip(FIELDS,map(str,(wid,policy,h,a,y,d,r,w,
                F(1,64),out,int(out==y),intervention)))))
        worlds.append({"world_id":wid,"policy":policy,"state_count":64,
            "correct_count":correct,"changed_from_default_count":changed,
            "intervention_count":intervened,"correct_fraction":str(F(correct,64)),
            "changed_fraction":str(F(changed,64)),"intervention_fraction":str(F(intervened,64))})
    pairwise={}
    for i,p in enumerate(POLICIES):
        for q in POLICIES[i+1:]:
            pairwise[p+"|"+q]=sum(choose(p,h,a,d,r,w)[0]!=choose(q,h,a,d,r,w)[0]
                for h,a,y,d,r,w in STATES)
    return rows,{"schema":"r322_schematic_default_intervention_e1_v1",
        "original_catalogue_id":"01-012","artificial_schematic_only":True,
        "original_source_rows":256,"state_count_per_policy":64,
        "worlds":worlds,"pairwise_output_disagreement_counts":pairwise}
def csv_text(rows):
    f=io.StringIO(newline="");w=csv.DictWriter(f,fieldnames=FIELDS,lineterminator="\n")
    w.writeheader();w.writerows(rows);return f.getvalue()
def json_text(obj):return json.dumps(obj,indent=2,ensure_ascii=False)+"\n"
def verify_source(c,j):
    r,o=generate()
    if c!=csv_text(r):raise AssertionError("original states differ")
    if json.loads(j)!=o:raise AssertionError("results differ")
    return True
def replay():return verify_source(CSV.read_text(encoding="utf-8"),JSON.read_text(encoding="utf-8"))
def world(p):return next(x for x in generate()[1]["worlds"] if x["policy"]==p)
class Tests(unittest.TestCase):
    def test_01_policies(self):self.assertEqual(len(POLICIES),4)
    def test_02_states(self):self.assertEqual(len(STATES),64)
    def test_03_rows(self):self.assertEqual(len(generate()[0]),256)
    def test_04_unique(self):self.assertEqual(len({tuple(r[x] for x in FIELDS[:8]) for r in generate()[0]}),256)
    def test_05_correct_half(self):
        for p in POLICIES:self.assertEqual(world(p)["correct_fraction"],"1/2")
    def test_06_gated_changed(self):self.assertEqual(world("gated_intervention")["changed_from_default_count"],4)
    def test_07_analytic_changed(self):self.assertEqual(world("analytic_only")["changed_from_default_count"],32)
    def test_08_default_changed(self):self.assertEqual(world("default_only")["changed_from_default_count"],0)
    def test_09_lookup_changed(self):self.assertEqual(world("lookup_equivalent")["changed_from_default_count"],4)
    def test_10_gated_interventions(self):self.assertEqual(world("gated_intervention")["intervention_count"],4)
    def test_11_lookup_no_interventions(self):self.assertEqual(world("lookup_equivalent")["intervention_count"],0)
    def test_12_analytic_interventions(self):self.assertEqual(world("analytic_only")["intervention_count"],64)
    def test_13_output_equivalence(self):
        for h,a,y,d,r,w in STATES:self.assertEqual(choose("gated_intervention",h,a,d,r,w)[0],choose("lookup_equivalent",h,a,d,r,w)[0])
    def test_14_label_non_equivalence(self):self.assertNotEqual(choose("gated_intervention",0,1,1,1,1)[1],choose("lookup_equivalent",0,1,1,1,1)[1])
    def test_15_conditional(self):
        selected=[s for s in STATES if s[1]==s[2] and s[0]!=s[1]]
        self.assertEqual(len(selected),16)
        self.assertEqual(sum(choose("gated_intervention",s[0],s[1],s[3],s[4],s[5])[1] for s in selected),2)
    def test_16_pair_equiv(self):self.assertEqual(generate()[1]["pairwise_output_disagreement_counts"]["gated_intervention|lookup_equivalent"],0)
    def test_17_pair_default(self):self.assertEqual(generate()[1]["pairwise_output_disagreement_counts"]["default_only|gated_intervention"],4)
    def test_18_pair_analytic(self):self.assertEqual(generate()[1]["pairwise_output_disagreement_counts"]["default_only|analytic_only"],32)
    def test_19_binary_outputs(self):self.assertTrue(all(r["output"] in ("0","1") for r in generate()[0]))
    def test_20_uniform_weights(self):self.assertTrue(all(r["weight"]=="1/64" for r in generate()[0]))
    def test_21_mass(self):
        for i in range(4):self.assertEqual(sum((F(r["weight"]) for r in generate()[0] if r["world_id"]==str(i)),F(0)),1)
    def test_22_default(self):self.assertEqual(choose("default_only",1,0,1,1,1),(1,0))
    def test_23_analytic(self):self.assertEqual(choose("analytic_only",1,0,0,0,0),(0,1))
    def test_24_gated_yes(self):self.assertEqual(choose("gated_intervention",0,1,1,1,1),(1,1))
    def test_25_gated_no_resource(self):self.assertEqual(choose("gated_intervention",0,1,1,0,1),(0,0))
    def test_26_no_conflict(self):self.assertEqual(choose("gated_intervention",1,1,1,1,1),(1,0))
    def test_27_invalid(self):
        with self.assertRaises(ValueError):choose("other",0,1,1,1,1)
    def test_28_replay(self):self.assertTrue(replay())
    def test_29_corruption(self):
        c=csv_text(generate()[0]);j=json_text(generate()[1])
        with self.assertRaises(AssertionError):verify_source(c.replace("1/64","1/32",1),j)
    def test_30_meta(self):self.assertEqual(generate()[1]["original_catalogue_id"],"01-012")
    def test_31_output_counterexample(self):
        self.assertEqual(choose("gated_intervention",0,1,1,1,1)[0],1)
        self.assertEqual(choose("gated_intervention",1,0,1,1,1)[0],0)
    def test_32_pair_count(self):self.assertEqual(len(generate()[1]["pairwise_output_disagreement_counts"]),6)
if __name__=="__main__":
    p=argparse.ArgumentParser();p.add_argument("--write",action="store_true")
    p.add_argument("--test",action="store_true");p.add_argument("--audit",action="store_true")
    a=p.parse_args()
    if a.write:
        r,o=generate();CSV.write_text(csv_text(r),encoding="utf-8");JSON.write_text(json_text(o),encoding="utf-8")
        print("WROTE",len(r),"states")
    elif a.audit:print("R322_REPLAY_PASS",replay())
    elif a.test:unittest.main(argv=["r322"],verbosity=2)
    else:p.print_help()
