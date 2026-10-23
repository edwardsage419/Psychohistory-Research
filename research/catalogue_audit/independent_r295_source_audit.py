#!/usr/bin/env python3
"""R295 independent original 180-source / 90-pair adversarial audit; no production imports."""
from __future__ import annotations
import argparse,csv,hashlib,itertools,json,unittest
from collections import defaultdict
from fractions import Fraction as Q
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]/"research"/"R295"
SOURCE=ROOT/"R295_ALL_180_ORIGINAL_HABIT_CUE_REVALUATION_STATES.csv"
RESULT=ROOT/"R295_EXACT_HABIT_CUE_AND_DEVALUATION_RESULTS.json"
RECEIPT=ROOT/"R295_MACHINE_RECEIPT.json"
RATES=(Q(0),Q(1,2),Q(1))
SHARES=RATES
CUES=(0,1)
OUTCOMES=(0,1)
DATES=tuple(range(5))
FROZEN=list(itertools.product(RATES,SHARES,CUES,OUTCOMES,DATES))
PAIR_KEYS=list(itertools.product(RATES,SHARES,CUES,DATES))
Z,O=Q(0),Q(1)

def obj(path):return json.loads(path.read_text(encoding="utf-8"))
def sources():
    with SOURCE.open(encoding="utf-8",newline="") as f:return list(csv.DictReader(f))
def independently_learned(alpha,n):
    h=Z
    for _ in range(n):
        h+=alpha*(O-h)
    return h
def reconstruct(key):
    alpha,lamb,cue,value,n=key
    h=independently_learned(alpha,n)
    g=(O-lamb)*value
    p=lamb*cue*h
    score=g+p
    return {"world":f"alpha={alpha}|lambda={lamb}|cue={cue}|value={value}",
      "learned_habit_strength":h,"goal_component":g,"habit_component":p,
      "action_A_score":score,"alternative_B_score":Q(1,2),
      "exact_tie":str(score==Q(1,2)),"selected":"A" if score>Q(1,2) else "B"}

def verify(original,results):
    if len(original)!=180:raise AssertionError("180 complete labeled sources required")
    if results["world_count"]!=36 or results["fully_labeled_source_rows"]!=180 or results["matched_devaluation_pairs"]!=90:raise AssertionError("wrong output metadata")
    seen={}
    for r in original:
        try:
            a=Q(r["alpha"]);l=Q(r["habit_share_lambda"]);c=int(r["same_context_cue"])
            v=int(r["current_outcome_value"]);n=int(r["training_repetitions_n"])
        except (KeyError,ValueError,ZeroDivisionError) as ex:raise AssertionError("unreadable source") from ex
        key=(a,l,c,v,n)
        if key not in FROZEN or key in seen:raise AssertionError("source out of frozen universe or duplicated")
        expected=reconstruct(key)
        for field in ("world","exact_tie","selected"):
            if r[field]!=expected[field]:raise AssertionError("source mismatch "+field)
        for field in ("learned_habit_strength","goal_component","habit_component","action_A_score","alternative_B_score"):
            if Q(r[field])!=expected[field]:raise AssertionError("source score mismatch "+field)
        seen[key]=expected
    if len(seen)!=180 or set(seen)!=set(FROZEN):raise AssertionError("missing source states")
    pairs=results["complete_matched_pair_results"]
    if len(pairs)!=90:raise AssertionError("incomplete valuation comparisons")
    totals=defaultdict(lambda:{"comparisons":0,"devaluation_sensitive":0})
    for pos,(a,l,c,n) in enumerate(PAIR_KEYS):
        valued=seen[(a,l,c,1,n)]
        devalued=seen[(a,l,c,0,n)]
        if valued["action_A_score"]<devalued["action_A_score"]:raise AssertionError("devaluation falsely increases score")
        if valued["selected"]=="B" and devalued["selected"]=="A":raise AssertionError("wrong devaluation reversal direction")
        sensitivity=valued["selected"]=="A" and devalued["selected"]=="B"
        expected={"alpha":str(a),"habit_share_lambda":str(l),"same_context_cue":str(c),
          "training_repetitions_n":str(n),"valued_choice":valued["selected"],
          "devalued_choice":devalued["selected"],"valuation_sensitive_A_to_B":str(sensitivity),
          "valued_A_score":str(valued["action_A_score"]), "devalued_A_score":str(devalued["action_A_score"])}
        if pairs[pos]!=expected:raise AssertionError("paired report or ordering incorrect")
        totals[str(l)]["comparisons"]+=1
        totals[str(l)]["devaluation_sensitive"]+=int(sensitivity)
    if dict(totals)!=results["habit_share_group_sensitivity_counts"]:raise AssertionError("controller group counts mismatch")
    for n in DATES:
        if results["learning_curve_half_rate"][str(n)]!=str(independently_learned(Q(1,2),n)):raise AssertionError("learning curve corrupted")
    special=results["artificial_special_cases"]
    if special!={"habit_half_rate_four_repetitions":"15/16",
      "same_cue_habit_only_valued_choice":"A","same_cue_habit_only_devalued_choice":"A",
      "changed_cue_habit_only_choice":"B","mixed_same_cue_valued_A_score":"31/32",
      "mixed_same_cue_devalued_A_score":"15/32"}:raise AssertionError("special negative control mismatch")
    return {"complete_original_sources":180,"matched_outcome_devaluation_comparisons":90,
      "full_training_worlds":36,"independent_habit_and_goal_score_reconstruction":"PASS",
      "sensitivity_by_controller":dict(totals),"human_E2_added":0,"historical_E3_added":0}

def audit():
    receipt,result=obj(RECEIPT),obj(RESULT)
    freeze="638948a4fb2fdcc370dbbc2c2f9f634f4d61a57b"
    if receipt["freeze_commit"]!=freeze or result["freeze_commit"]!=freeze:raise AssertionError("wrong prospective freeze")
    if result["original_catalogue_id"]!="01-019":raise AssertionError("wrong catalogue ID")
    if result["new_real_human_E2"]!=0 or result["new_historical_E3"]!=0 or receipt["new_real_human_E2"]!=0 or receipt["new_historical_E3"]!=0:raise AssertionError("scope promotion")
    if hashlib.sha256(SOURCE.read_bytes()).hexdigest()!=receipt["source_sha256"]:raise AssertionError("original CSV SHA256 failure")
    if hashlib.sha256(RESULT.read_bytes()).hexdigest()!=receipt["results_sha256"]:raise AssertionError("results SHA256 failure")
    return {**verify(sources(),result),"source_sha256":receipt["source_sha256"],"results_sha256":receipt["results_sha256"]}

class Tests(unittest.TestCase):
    def test_all(self):self.assertEqual(audit()["complete_original_sources"],180)
    def test_worlds(self):self.assertEqual(len(FROZEN),180)
    def test_pair_count(self):self.assertEqual(len(PAIR_KEYS),90)
    def test_half_rate(self):self.assertEqual(independently_learned(Q(1,2),4),Q(15,16))
    def test_devaluation_habit_only(self):self.assertEqual(reconstruct((Q(1,2),O,1,0,4))["selected"],"A")
    def test_goal_devaluation(self):self.assertEqual(reconstruct((Q(1,2),Z,1,0,4))["selected"],"B")
    def test_context_disruption(self):self.assertEqual(reconstruct((Q(1,2),O,0,1,4))["selected"],"B")
    def test_reject_missing(self):
        with self.assertRaises(AssertionError):verify(sources()[:-1],obj(RESULT))
    def test_reject_duplicates(self):
        bad=sources();bad[1]=dict(bad[0])
        with self.assertRaises(AssertionError):verify(bad,obj(RESULT))
    def test_reject_wrong_utility(self):
        bad=sources();bad[0]=dict(bad[0]);bad[0]["action_A_score"]="99"
        with self.assertRaises(AssertionError):verify(bad,obj(RESULT))
    def test_reject_cue(self):
        bad=sources();bad[0]=dict(bad[0]);bad[0]["same_context_cue"]="7"
        with self.assertRaises(AssertionError):verify(bad,obj(RESULT))
    def test_reject_pair_sensitivity(self):
        out=obj(RESULT);out["complete_matched_pair_results"][0]["valuation_sensitive_A_to_B"]="FAKE"
        with self.assertRaises(AssertionError):verify(sources(),out)
    def test_reject_group_count(self):
        out=obj(RESULT);out["habit_share_group_sensitivity_counts"]["0"]["devaluation_sensitive"]=-1
        with self.assertRaises(AssertionError):verify(sources(),out)
    def test_tamper_sha(self):self.assertNotEqual(hashlib.sha256(SOURCE.read_bytes()+b"change").hexdigest(),obj(RECEIPT)["source_sha256"])

if __name__=="__main__":
    p=argparse.ArgumentParser()
    g=p.add_mutually_exclusive_group(required=True)
    g.add_argument("--test",action="store_true");g.add_argument("--audit",action="store_true")
    args=p.parse_args()
    if args.test:unittest.main(argv=["R295 independent"],verbosity=1)
    else:print(json.dumps(audit(),indent=2))
