#!/usr/bin/env python3
"""Independent R298 source-level planner and cached-value audit, never imports main model."""
from __future__ import annotations
import argparse,csv,hashlib,itertools,json,unittest
from collections import defaultdict
from fractions import Fraction as Q
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]/"research/R298"
SOURCE=ROOT/"R298_ALL_64_ORIGINAL_REVALUATION_ACTION_SOURCES.csv"
RESULT=ROOT/"R298_EXACT_MODEL_BASED_REVALUATION_RESULTS.json"
RECEIPT=ROOT/"R298_MACHINE_RECEIPT.json"
SCENARIOS=("BASELINE","REWARD_SHIFT","TRANSITION_SWAP","BOTH")
GAMMAS=(Q(1,2),Q(1))
INFO=(0,1)
CONTROLLERS=("MODEL_BASED_PLANNER","CACHED_VALUES")
ACTIONS=("LEFT","RIGHT")
WORLDS=list(itertools.product(SCENARIOS,GAMMAS,INFO,CONTROLLERS))
ZERO=Q(0)

def obj(path):return json.loads(path.read_text(encoding="utf-8"))
def load():
    with SOURCE.open(newline="",encoding="utf-8") as f:return list(csv.DictReader(f))
def ident(world):
    s,g,n,c=world
    return f"scenario={s}|gamma={g}|notified={n}|controller={c}"

def elementary_model(scenario):
    # Independently list both alternate reward and transition factors.
    transitions={"LEFT":"S1","RIGHT":"S2"}
    rewards={"S1":2,"S2":1}
    if scenario=="REWARD_SHIFT":
        rewards={"S1":0,"S2":3}
    elif scenario=="TRANSITION_SWAP":
        transitions={"LEFT":"S2","RIGHT":"S1"}
    elif scenario=="BOTH":
        transitions={"LEFT":"S2","RIGHT":"S1"}
        rewards={"S1":0,"S2":3}
    elif scenario!="BASELINE":raise AssertionError("unfrozen model")
    return transitions,rewards

def independent_world(w):
    scenario,gamma,notification,controller=w
    actual_trans,actual_reward=elementary_model(scenario)
    reported=scenario if notification==1 and controller=="MODEL_BASED_PLANNER" else "BASELINE"
    known_trans,known_reward=elementary_model(reported)
    actual={a:gamma*actual_reward[actual_trans[a]] for a in ACTIONS}
    estimated={a:gamma*known_reward[known_trans[a]] for a in ACTIONS}
    proposed=max(ACTIONS,key=lambda a:(estimated[a],-ACTIONS.index(a)))
    optimal=max(ACTIONS,key=lambda a:(actual[a],-ACTIONS.index(a)))
    regret=max(actual.values())-actual[proposed]
    return {"assumed":reported,"true_transition":actual_trans,"true_reward":actual_reward,
      "known_transition":known_trans,"known_reward":known_reward,
      "actual_Q":actual,"predicted_Q":estimated,"chosen":proposed,"optimal":optimal,
      "regret":regret,"agreement":proposed==optimal}

def verify(rows,results):
    if len(rows)!=64 or len(results["worlds"])!=32:raise AssertionError("complete universe missing")
    if results["original_full_labeled_action_sources"]!=64 or results["synthetic_worlds"]!=32:raise AssertionError("metadata count invalid")
    found=defaultdict(dict)
    for r in rows:
        try:world=(r["scenario"],Q(r["gamma"]),int(r["notified"]),r["controller"])
        except (KeyError,ValueError,ZeroDivisionError) as ex:raise AssertionError("source parameters malformed") from ex
        action=r["action"]
        if world not in WORLDS or action not in ACTIONS:raise AssertionError("unfrozen source")
        if action in found[world]:raise AssertionError("duplicate action")
        if r["world"]!=ident(world):raise AssertionError("world label mismatch")
        expected=independent_world(world)
        if r["assumed_environment_scenario"]!=expected["assumed"]:raise AssertionError("assumed model mismatch")
        if r["actual_successor"]!=expected["true_transition"][action]:raise AssertionError("true successor mismatch")
        if r["assumed_successor"]!=expected["known_transition"][action]:raise AssertionError("announced successor mismatch")
        if Q(r["actual_successor_terminal_reward"])!=expected["true_reward"][expected["true_transition"][action]]:raise AssertionError("actual reward mismatch")
        if Q(r["assumed_successor_terminal_reward"])!=expected["known_reward"][expected["known_transition"][action]]:raise AssertionError("assumed reward mismatch")
        if Q(r["actual_Q"])!=expected["actual_Q"][action] or Q(r["predicted_Q"])!=expected["predicted_Q"][action]:raise AssertionError("action value mismatch")
        if r["chosen_action"]!=expected["chosen"] or r["actual_optimal_action"]!=expected["optimal"]:raise AssertionError("policy choice mismatch")
        if r["oracle_agreement"]!=str(expected["agreement"]):raise AssertionError("agreement value wrong")
        if Q(r["regret_against_actual_model"])!=expected["regret"]:raise AssertionError("true model regret mismatch")
        found[world][action]=expected
    if set(found)!=set(WORLDS):raise AssertionError("world incomplete")
    agree=0
    for i,world in enumerate(WORLDS):
        if set(found[world])!=set(ACTIONS):raise AssertionError("missing action")
        v=independent_world(world)
        s,g,n,c=world
        x=results["worlds"][i]
        if x["world"]!=ident(world) or x["scenario"]!=s or x["gamma"]!=str(g) or x["notified"]!=n or x["controller"]!=c:raise AssertionError("world results mislabeled")
        if x["assumed_environment_scenario"]!=v["assumed"]:raise AssertionError("stored belief mismatch")
        if x["predicted_action_Q"]!={a:str(v["predicted_Q"][a]) for a in ACTIONS}:raise AssertionError("stored predicted value mismatch")
        if x["true_environment_action_Q"]!={a:str(v["actual_Q"][a]) for a in ACTIONS}:raise AssertionError("stored true value mismatch")
        if x["chosen_action"]!=v["chosen"] or x["actual_optimal_action"]!=v["optimal"]:raise AssertionError("stored policy wrong")
        if x["oracle_agreement"]!=v["agreement"] or x["regret_against_actual_model"]!=str(v["regret"]):raise AssertionError("stored regret wrong")
        if x["original_source_rows"]!=2:raise AssertionError("wrong row count")
        agree+=int(v["agreement"])
    if agree!=20 or results["oracle_agreement_count"]!=20 or results["oracle_disagreement_count"]!=12:raise AssertionError("summary mismatch")
    return {"original_action_sources":64,"world_count":32,"oracle_optimal_agreement":20,"oracle_disagreement":12,
      "independent_planning_and_information_audit":"PASS","human_E2_added":0,"animal_E2_added":0,"historical_E3_added":0}

def audit():
    receipt,res=obj(RECEIPT),obj(RESULT)
    freeze="24cdb3119991c7233ee02fdad271d74881ab8825"
    if receipt["freeze_commit"]!=freeze or res["freeze_commit"]!=freeze:raise AssertionError("not original freeze")
    if res["original_catalogue_id"]!="02-004":raise AssertionError("wrong original 239 candidate")
    if res["new_real_human_E2"]!=0 or res["new_real_animal_E2"]!=0 or res["new_historical_E3"]!=0:raise AssertionError("false human/animal/historical")
    if res["model_transition_learning_performed"] is not False or res["no_new_direct_experience_after_revaluation"] is not True:raise AssertionError("unwarranted learning")
    if receipt["new_E2"]!=0 or receipt["new_E3"]!=0 or receipt["source_action_rows"]!=64:raise AssertionError("receipt metadata wrong")
    if hashlib.sha256(SOURCE.read_bytes()).hexdigest()!=receipt["source_sha256"]:raise AssertionError("CSV digest")
    if hashlib.sha256(RESULT.read_bytes()).hexdigest()!=receipt["results_sha256"]:raise AssertionError("JSON digest")
    return {**verify(load(),res),"source_sha256":receipt["source_sha256"],"results_sha256":receipt["results_sha256"]}

class Tests(unittest.TestCase):
    def test_full(self):self.assertEqual(audit()["original_action_sources"],64)
    def test_world_count(self):self.assertEqual(len(WORLDS),32)
    def test_reward_change(self):self.assertEqual(independent_world(("REWARD_SHIFT",Q(1),1,"MODEL_BASED_PLANNER"))["chosen"],"RIGHT")
    def test_transition_change(self):self.assertEqual(independent_world(("TRANSITION_SWAP",Q(1),1,"MODEL_BASED_PLANNER"))["chosen"],"RIGHT")
    def test_two_changes_cancel(self):self.assertEqual(independent_world(("BOTH",Q(1),1,"MODEL_BASED_PLANNER"))["chosen"],"LEFT")
    def test_no_notice(self):self.assertEqual(independent_world(("REWARD_SHIFT",Q(1),0,"MODEL_BASED_PLANNER"))["chosen"],"LEFT")
    def test_cached_notified(self):self.assertEqual(independent_world(("REWARD_SHIFT",Q(1),1,"CACHED_VALUES"))["chosen"],"LEFT")
    def test_missing_row(self):
        with self.assertRaises(AssertionError):verify(load()[:-1],obj(RESULT))
    def test_duplicate_action(self):
        x=load();x[1]=dict(x[0])
        with self.assertRaises(AssertionError):verify(x,obj(RESULT))
    def test_wrong_successor(self):
        x=load();x[0]=dict(x[0]);x[0]["actual_successor"]="S4"
        with self.assertRaises(AssertionError):verify(x,obj(RESULT))
    def test_wrong_reward(self):
        x=load();x[0]=dict(x[0]);x[0]["actual_successor_terminal_reward"]="42"
        with self.assertRaises(AssertionError):verify(x,obj(RESULT))
    def test_wrong_predicted(self):
        x=load();x[0]=dict(x[0]);x[0]["predicted_Q"]="100"
        with self.assertRaises(AssertionError):verify(x,obj(RESULT))
    def test_wrong_notification(self):
        x=load();x[0]=dict(x[0]);x[0]["notified"]="7"
        with self.assertRaises(AssertionError):verify(x,obj(RESULT))
    def test_wrong_choice(self):
        x=load();x[0]=dict(x[0]);x[0]["chosen_action"]="WRONG"
        with self.assertRaises(AssertionError):verify(x,obj(RESULT))
    def test_wrong_regret(self):
        x=load();x[0]=dict(x[0]);x[0]["regret_against_actual_model"]="1"
        with self.assertRaises(AssertionError):verify(x,obj(RESULT))
    def test_result_tamper(self):
        x=obj(RESULT);x["worlds"][0]["predicted_action_Q"]["LEFT"]="100"
        with self.assertRaises(AssertionError):verify(load(),x)
    def test_digest_tamper(self):self.assertNotEqual(hashlib.sha256(SOURCE.read_bytes()+b"x").hexdigest(),obj(RECEIPT)["source_sha256"])

if __name__=="__main__":
    ap=argparse.ArgumentParser()
    g=ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--test",action="store_true")
    g.add_argument("--audit",action="store_true")
    args=ap.parse_args()
    if args.test:unittest.main(argv=["R298audit"],verbosity=1)
    else:print(json.dumps(audit(),indent=2))
