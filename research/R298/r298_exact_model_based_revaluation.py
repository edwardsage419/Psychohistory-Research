#!/usr/bin/env python3
"""R298 deterministic one-step model-based planning vs frozen cached values, artificial E1."""
from __future__ import annotations
import argparse,csv,hashlib,itertools,json,unittest
from fractions import Fraction as F
from pathlib import Path

ROOT=Path(__file__).resolve().parent
FREEZE="24cdb3119991c7233ee02fdad271d74881ab8825"
SCENARIOS=("BASELINE","REWARD_SHIFT","TRANSITION_SWAP","BOTH")
GAMMAS=(F(1,2),F(1))
NOTIFIED=(0,1)
CONTROLLERS=("MODEL_BASED_PLANNER","CACHED_VALUES")
ACTIONS=("LEFT","RIGHT")
WORLDS=tuple(itertools.product(SCENARIOS,GAMMAS,NOTIFIED,CONTROLLERS))
CSV_NAME="R298_ALL_64_ORIGINAL_REVALUATION_ACTION_SOURCES.csv"
RESULT_NAME="R298_EXACT_MODEL_BASED_REVALUATION_RESULTS.json"
RECEIPT_NAME="R298_MACHINE_RECEIPT.json"

def model(scenario):
    if scenario not in SCENARIOS:raise ValueError("unfrozen scenario")
    swap=scenario in ("TRANSITION_SWAP","BOTH")
    changed=scenario in ("REWARD_SHIFT","BOTH")
    transition={"LEFT":"S2","RIGHT":"S1"} if swap else {"LEFT":"S1","RIGHT":"S2"}
    reward={"S1":0,"S2":3} if changed else {"S1":2,"S2":1}
    return transition,reward

def assumed_model(scenario,notify,controller):
    if (scenario,notify,controller) not in tuple(itertools.product(SCENARIOS,NOTIFIED,CONTROLLERS)):
        raise ValueError("unfrozen information/controller")
    belief=scenario if notify==1 and controller=="MODEL_BASED_PLANNER" else "BASELINE"
    return belief,*model(belief)

def worldid(scenario,gamma,notify,controller):
    return f"scenario={scenario}|gamma={gamma}|notified={notify}|controller={controller}"

def calculate(scenario,gamma,notify,controller):
    if (scenario,gamma,notify,controller) not in WORLDS:raise ValueError("unfrozen world")
    actual_transition,actual_reward=model(scenario)
    belief,assumed_transition,assumed_reward=assumed_model(scenario,notify,controller)
    actual_q={action:gamma*actual_reward[actual_transition[action]] for action in ACTIONS}
    predicted_q={action:gamma*assumed_reward[assumed_transition[action]] for action in ACTIONS}
    chosen="RIGHT" if predicted_q["RIGHT"]>predicted_q["LEFT"] else "LEFT"
    oracle="RIGHT" if actual_q["RIGHT"]>actual_q["LEFT"] else "LEFT"
    loss=max(actual_q.values())-actual_q[chosen]
    return {"belief_scenario":belief,"actual_transition":actual_transition,
       "actual_terminal_reward":actual_reward,
       "assumed_transition":assumed_transition,
       "assumed_terminal_reward":assumed_reward,
       "actual_Q":actual_q,"predicted_Q":predicted_q,
       "chosen_action":chosen,"actual_optimal_action":oracle,
       "regret_against_actual_model":loss,"oracle_agreement":chosen==oracle}

def source_row(scenario,gamma,notify,controller,action):
    if action not in ACTIONS:raise ValueError("unfrozen action")
    result=calculate(scenario,gamma,notify,controller)
    return {"world":worldid(scenario,gamma,notify,controller),
      "scenario":scenario,"gamma":gamma,"notified":notify,"controller":controller,
      "action":action,"assumed_environment_scenario":result["belief_scenario"],
      "actual_successor":result["actual_transition"][action],
      "actual_successor_terminal_reward":result["actual_terminal_reward"][result["actual_transition"][action]],
      "assumed_successor":result["assumed_transition"][action],
      "assumed_successor_terminal_reward":result["assumed_terminal_reward"][result["assumed_transition"][action]],
      "actual_Q":result["actual_Q"][action],"predicted_Q":result["predicted_Q"][action],
      "chosen_action":result["chosen_action"],"actual_optimal_action":result["actual_optimal_action"],
      "oracle_agreement":result["oracle_agreement"],"regret_against_actual_model":result["regret_against_actual_model"]}

def sources():
    return tuple(source_row(*world,action) for world in WORLDS for action in ACTIONS)

def verify():
    assert len(WORLDS)==32 and len(sources())==64
    assert len(set((x["world"],x["action"]) for x in sources()))==64
    last=[]
    for scenario,gamma,notify,controller in WORLDS:
        info=calculate(scenario,gamma,notify,controller)
        assert info["regret_against_actual_model"]>=0
        assert info["regret_against_actual_model"]==(0 if info["oracle_agreement"] else (
            gamma*3 if scenario=="REWARD_SHIFT" else gamma if scenario=="TRANSITION_SWAP" else F(0)))
        assert info["predicted_Q"]=={
          k:gamma*info["assumed_terminal_reward"][info["assumed_transition"][k]] for k in ACTIONS}
        assert info["actual_Q"]=={
          k:gamma*info["actual_terminal_reward"][info["actual_transition"][k]] for k in ACTIONS}
        if scenario in ("BASELINE","BOTH"):
            assert info["oracle_agreement"]
        if notify and controller=="MODEL_BASED_PLANNER":
            assert info["oracle_agreement"] and info["belief_scenario"]==scenario
        if not notify or controller=="CACHED_VALUES":
            assert info["belief_scenario"]=="BASELINE" and info["chosen_action"]=="LEFT"
        last.append(info)
    assert sum(x["oracle_agreement"] for x in last)==20
    assert sum(not x["oracle_agreement"] for x in last)==12
    for gamma in GAMMAS:
        assert calculate("REWARD_SHIFT",gamma,1,"MODEL_BASED_PLANNER")["chosen_action"]=="RIGHT"
        assert calculate("TRANSITION_SWAP",gamma,1,"MODEL_BASED_PLANNER")["chosen_action"]=="RIGHT"
        assert calculate("BOTH",gamma,1,"MODEL_BASED_PLANNER")["chosen_action"]=="LEFT"
        assert calculate("BOTH",gamma,0,"CACHED_VALUES")["chosen_action"]=="LEFT"
        assert calculate("REWARD_SHIFT",gamma,0,"MODEL_BASED_PLANNER")["chosen_action"]=="LEFT"
        assert calculate("REWARD_SHIFT",gamma,1,"CACHED_VALUES")["chosen_action"]=="LEFT"
    return True

def emit():
    verify()
    fields=("world","scenario","gamma","notified","controller","action",
         "assumed_environment_scenario","actual_successor","actual_successor_terminal_reward",
         "assumed_successor","assumed_successor_terminal_reward",
         "actual_Q","predicted_Q","chosen_action","actual_optimal_action",
         "oracle_agreement","regret_against_actual_model")
    file=ROOT/CSV_NAME
    with file.open("w",encoding="utf-8",newline="") as f:
        w=csv.DictWriter(f,fieldnames=fields,lineterminator="\n")
        w.writeheader()
        for row in sources():w.writerow({key:str(row[key]) for key in fields})
    output={"research_id":"R298","original_catalogue_id":"02-004","freeze_commit":FREEZE,
      "scope":"E1_SYNTHETIC_KNOWN_MODEL_PLANNING_AFTER_EXOGENOUS_NOTIFICATION_NOT_WORLD_MODEL_LEARNING",
      "synthetic_worlds":len(WORLDS),"original_full_labeled_action_sources":len(sources()),
      "no_new_direct_experience_after_revaluation":True,
      "model_transition_learning_performed":False,
      "new_real_human_E2":0,"new_real_animal_E2":0,"new_historical_E3":0,
      "R073":"FROZEN","PESEN_v0_1":"FROZEN",
      "worlds":[]}
    for w in WORLDS:
        scenario,gamma,notify,controller=w
        data=calculate(*w)
        output["worlds"].append({"world":worldid(*w),"scenario":scenario,
         "gamma":str(gamma),"notified":notify,"controller":controller,
         "assumed_environment_scenario":data["belief_scenario"],
         "predicted_action_Q":{a:str(data["predicted_Q"][a]) for a in ACTIONS},
         "true_environment_action_Q":{a:str(data["actual_Q"][a]) for a in ACTIONS},
         "chosen_action":data["chosen_action"],"actual_optimal_action":data["actual_optimal_action"],
         "oracle_agreement":data["oracle_agreement"],
         "regret_against_actual_model":str(data["regret_against_actual_model"]),
         "original_source_rows":2})
    output["oracle_agreement_count"]=sum(w["oracle_agreement"] for w in output["worlds"])
    output["oracle_disagreement_count"]=sum(not w["oracle_agreement"] for w in output["worlds"])
    resultp=ROOT/RESULT_NAME
    resultp.write_text(json.dumps(output,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    receipt={"research_id":"R298","freeze_commit":FREEZE,"source_action_rows":64,
       "source_sha256":hashlib.sha256(file.read_bytes()).hexdigest(),
       "results_sha256":hashlib.sha256(resultp.read_bytes()).hexdigest(),
       "new_E2":0,"new_E3":0}
    (ROOT/RECEIPT_NAME).write_text(json.dumps(receipt,indent=2)+"\n",encoding="utf-8")
    return receipt

class Tests(unittest.TestCase):
    def test_all(self):self.assertTrue(verify())
    def test_worlds(self):self.assertEqual(len(WORLDS),32)
    def test_sources(self):self.assertEqual(len(sources()),64)
    def test_reward_shifts(self):self.assertEqual(calculate("REWARD_SHIFT",F(1),1,"MODEL_BASED_PLANNER")["chosen_action"],"RIGHT")
    def test_transition_swap(self):self.assertEqual(calculate("TRANSITION_SWAP",F(1),1,"MODEL_BASED_PLANNER")["chosen_action"],"RIGHT")
    def test_both_is_negative_control(self):self.assertEqual(calculate("BOTH",F(1),1,"MODEL_BASED_PLANNER")["chosen_action"],"LEFT")
    def test_cached_after_notification(self):self.assertEqual(calculate("REWARD_SHIFT",F(1),1,"CACHED_VALUES")["chosen_action"],"LEFT")
    def test_planner_without_notification(self):self.assertEqual(calculate("REWARD_SHIFT",F(1),0,"MODEL_BASED_PLANNER")["chosen_action"],"LEFT")
    def test_regret_reward(self):self.assertEqual(calculate("REWARD_SHIFT",F(1,2),0,"CACHED_VALUES")["regret_against_actual_model"],F(3,2))
    def test_regret_transition(self):self.assertEqual(calculate("TRANSITION_SWAP",F(1,2),0,"CACHED_VALUES")["regret_against_actual_model"],F(1,2))
    def test_bad_scenario(self):
        with self.assertRaises(ValueError):model("MISSING")
    def test_bad_discount(self):
        with self.assertRaises(ValueError):calculate("BASELINE",F(3,4),1,"MODEL_BASED_PLANNER")
    def test_bad_action(self):
        with self.assertRaises(ValueError):source_row("BASELINE",F(1),1,"MODEL_BASED_PLANNER","INVALID")

def case(world,action,kind):
    def check(self):
        r=source_row(*world,action)
        values=calculate(*world)
        if kind=="source":self.assertEqual(r["predicted_Q"],values["predicted_Q"][action])
        elif kind=="actual":self.assertEqual(r["actual_Q"],values["actual_Q"][action])
        elif kind=="choice":self.assertEqual(r["chosen_action"],values["chosen_action"])
        elif kind=="loss":self.assertEqual(r["regret_against_actual_model"],values["regret_against_actual_model"])
        else:raise AssertionError(kind)
    return check
for i,w in enumerate(WORLDS):
    for action in ACTIONS:
        for k in ("source","actual","choice","loss"):
            setattr(Tests,f"test_world{i}_{action.lower()}_{k}",case(w,action,k))
if __name__=="__main__":
    p=argparse.ArgumentParser()
    m=p.add_mutually_exclusive_group(required=True)
    m.add_argument("--test",action="store_true")
    m.add_argument("--emit",action="store_true")
    a=p.parse_args()
    if a.test:unittest.main(argv=["R298"],verbosity=1)
    else:print(json.dumps(emit(),indent=2))
