#!/usr/bin/env python3
"""R295 finite artificial cue/action habit and devaluation, no real human data."""
from __future__ import annotations
import argparse,csv,hashlib,itertools,json,unittest
from fractions import Fraction as F
from pathlib import Path

ROOT=Path(__file__).resolve().parent
FREEZE="638948a4fb2fdcc370dbbc2c2f9f634f4d61a57b"
Z,O=F(0),F(1)
ALPHAS=(Z,F(1,2),O)
LAMBDAS=(Z,F(1,2),O)
CONTEXTS=(0,1)
VALUES=(0,1)
STAGES=tuple(range(5))
WORLDS=tuple(itertools.product(ALPHAS,LAMBDAS,CONTEXTS,VALUES))
PAIR_IDS=tuple(itertools.product(ALPHAS,LAMBDAS,CONTEXTS,STAGES))
CSV_NAME="R295_ALL_180_ORIGINAL_HABIT_CUE_REVALUATION_STATES.csv"
RESULT_NAME="R295_EXACT_HABIT_CUE_AND_DEVALUATION_RESULTS.json"
RECEIPT_NAME="R295_MACHINE_RECEIPT.json"

def habit(alpha,n):
    if alpha not in ALPHAS or n not in STAGES:raise ValueError("unfrozen learning parameter")
    return O-(O-alpha)**n

def world_id(alpha,lamb,cue,value):
    return f"alpha={alpha}|lambda={lamb}|cue={cue}|value={value}"

def record(alpha,lamb,cue,value,n):
    if (alpha,lamb,cue,value) not in WORLDS or n not in STAGES:raise ValueError("unfrozen source")
    h=habit(alpha,n)
    goal=(O-lamb)*value
    associative=lamb*cue*h
    action=goal+associative
    alternative=F(1,2)
    return {"world":world_id(alpha,lamb,cue,value),"alpha":alpha,"habit_share_lambda":lamb,
      "same_context_cue":cue,"current_outcome_value":value,"training_repetitions_n":n,
      "learned_habit_strength":h,"goal_component":goal,"habit_component":associative,
      "action_A_score":action,"alternative_B_score":alternative,
      "exact_tie":action==alternative,"selected":"A" if action>alternative else "B"}

def rows():
    return tuple(record(a,l,c,v,n) for a,l,c,v in WORLDS for n in STAGES)

def paired(alpha,lamb,cue,n):
    x=record(alpha,lamb,cue,1,n)
    y=record(alpha,lamb,cue,0,n)
    if y["action_A_score"]>x["action_A_score"]:raise AssertionError("valuation reversal")
    if y["selected"]=="A" and x["selected"]=="B":raise AssertionError("devaluation makes A newly preferred")
    return {"alpha":alpha,"habit_share_lambda":lamb,"same_context_cue":cue,
        "training_repetitions_n":n,"valued_choice":x["selected"],
        "devalued_choice":y["selected"],
        "valuation_sensitive_A_to_B":x["selected"]=="A" and y["selected"]=="B",
        "valued_A_score":x["action_A_score"],"devalued_A_score":y["action_A_score"]}

def pairs():return tuple(paired(*key) for key in PAIR_IDS)

def validate():
    assert len(WORLDS)==36 and len(rows())==180 and len(pairs())==90
    assert len(set((r["world"],r["training_repetitions_n"]) for r in rows()))==180
    for a in ALPHAS:
        for n in STAGES:
            h=habit(a,n)
            assert Z<=h<=O and h==O-(O-a)**n
            if n<4:assert habit(a,n+1)-h==a*(O-h)
    assert habit(F(1,2),4)==F(15,16)
    for r in rows():
        assert r["goal_component"]+r["habit_component"]==r["action_A_score"]
        assert r["selected"]==("A" if r["action_A_score"]>F(1,2) else "B")
        assert r["exact_tie"]==(r["action_A_score"]==F(1,2))
        a,l,c,v,n=(r[x] for x in ("alpha","habit_share_lambda","same_context_cue","current_outcome_value","training_repetitions_n"))
        if l==0:assert r["selected"]==("A" if v==1 else "B")
        if l==1 and c==0:assert r["selected"]=="B"
        if l==1 and a==0:assert r["selected"]=="B"
    for v in VALUES:
        assert record(F(1,2),O,1,v,4)["selected"]=="A"
        assert record(F(1,2),O,0,v,4)["selected"]=="B"
    assert record(F(1,2),F(1,2),1,1,4)["action_A_score"]==F(31,32)
    assert record(F(1,2),F(1,2),1,0,4)["action_A_score"]==F(15,32)
    assert record(F(1,2),F(1,2),1,1,4)["selected"]=="A"
    assert record(F(1,2),F(1,2),1,0,4)["selected"]=="B"
    for p in pairs():
        if p["habit_share_lambda"]==0:assert p["valuation_sensitive_A_to_B"]
        if p["habit_share_lambda"]==1:assert not p["valuation_sensitive_A_to_B"]
    return True

def emit():
    validate()
    csv_file=ROOT/CSV_NAME
    fields=("world","alpha","habit_share_lambda","same_context_cue","current_outcome_value",
      "training_repetitions_n","learned_habit_strength","goal_component","habit_component",
      "action_A_score","alternative_B_score","exact_tie","selected")
    with csv_file.open("w",encoding="utf-8",newline="") as f:
        writer=csv.DictWriter(f,fieldnames=fields,lineterminator="\n")
        writer.writeheader()
        for r in rows():writer.writerow({key:str(r[key]) for key in fields})
    group_counts={}
    for l in LAMBDAS:
        chunk=[p for p in pairs() if p["habit_share_lambda"]==l]
        group_counts[str(l)]={"comparisons":len(chunk),
            "devaluation_sensitive":sum(p["valuation_sensitive_A_to_B"] for p in chunk)}
    result={"research_id":"R295","original_catalogue_id":"01-019","freeze_commit":FREEZE,
       "scope":"SYNTHETIC_FINITE_E1_CUE_ASSOCIATION_AND_OUTCOME_DEVALUATION_NOT_REAL_HABIT_VALIDATION",
       "world_count":len(WORLDS),"fully_labeled_source_rows":len(rows()),"matched_devaluation_pairs":len(pairs()),
       "outcome_value_noncausal_habit_controller_by_definition":True,
       "complete_matched_pair_results":[{k:str(v) for k,v in p.items()} for p in pairs()],
       "habit_share_group_sensitivity_counts":group_counts,
       "learning_curve_half_rate":{str(n):str(habit(F(1,2),n)) for n in STAGES},
       "artificial_special_cases":{
         "habit_half_rate_four_repetitions":"15/16",
         "same_cue_habit_only_valued_choice":record(F(1,2),O,1,1,4)["selected"],
         "same_cue_habit_only_devalued_choice":record(F(1,2),O,1,0,4)["selected"],
         "changed_cue_habit_only_choice":record(F(1,2),O,0,1,4)["selected"],
         "mixed_same_cue_valued_A_score":"31/32",
         "mixed_same_cue_devalued_A_score":"15/32"},
       "new_real_human_E2":0,"new_historical_E3":0,"R073":"FROZEN","PESEN_v0_1":"FROZEN"}
    result_file=ROOT/RESULT_NAME
    result_file.write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    receipt={"research_id":"R295","freeze_commit":FREEZE,"original_source_rows":180,
       "source_sha256":hashlib.sha256(csv_file.read_bytes()).hexdigest(),
       "results_sha256":hashlib.sha256(result_file.read_bytes()).hexdigest(),
       "new_real_human_E2":0,"new_historical_E3":0}
    (ROOT/RECEIPT_NAME).write_text(json.dumps(receipt,indent=2)+"\n",encoding="utf-8")
    return receipt

class Tests(unittest.TestCase):
    def test_validate(self):self.assertTrue(validate())
    def test_universe(self):self.assertEqual(len(rows()),180)
    def test_pairs(self):self.assertEqual(len(pairs()),90)
    def test_half_rate(self):self.assertEqual(habit(F(1,2),4),F(15,16))
    def test_goal_devaluation(self):self.assertEqual(paired(F(1,2),Z,1,4)["valuation_sensitive_A_to_B"],True)
    def test_habit_no_devaluation(self):self.assertEqual(paired(F(1,2),O,1,4)["valuation_sensitive_A_to_B"],False)
    def test_context_switch(self):self.assertEqual(record(F(1,2),O,0,1,4)["selected"],"B")
    def test_mixture_remains_sensitive(self):self.assertTrue(paired(F(1,2),F(1,2),1,4)["valuation_sensitive_A_to_B"])
    def test_bad_alpha(self):
        with self.assertRaises(ValueError):habit(F(1,3),4)
    def test_bad_stage(self):
        with self.assertRaises(ValueError):habit(F(1,2),5)
    def test_bad_world(self):
        with self.assertRaises(ValueError):record(Z,Z,2,1,2)
def generated(a,l,c,v,n,kind):
    def fn(self):
        r=record(a,l,c,v,n)
        if kind=="H":self.assertEqual(r["learned_habit_strength"],O-(O-a)**n)
        elif kind=="goal":self.assertEqual(r["goal_component"],(O-l)*v)
        elif kind=="associative":self.assertEqual(r["habit_component"],l*c*r["learned_habit_strength"])
        elif kind=="choice":self.assertEqual(r["selected"],"A" if r["action_A_score"]>F(1,2) else "B")
        else:raise AssertionError(kind)
    return fn
for j,(a,l,c,v) in enumerate(WORLDS):
    for n in STAGES:
        for kind in ("H","goal","associative","choice"):
            setattr(Tests,f"test_finite_world{j}_n{n}_{kind}",generated(a,l,c,v,n,kind))
if __name__=="__main__":
    ap=argparse.ArgumentParser()
    m=ap.add_mutually_exclusive_group(required=True)
    m.add_argument("--test",action="store_true")
    m.add_argument("--emit",action="store_true")
    a=ap.parse_args()
    if a.test:unittest.main(argv=["R295"],verbosity=1)
    else:print(json.dumps(emit(),indent=2))
