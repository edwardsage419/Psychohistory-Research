#!/usr/bin/env python3
"""R308 project-original synthetic collective efficacy belief ≠ intervention propensity, exact Fraction E1."""
from __future__ import annotations
import argparse,csv,hashlib,itertools,json,unittest
from fractions import Fraction as F
from pathlib import Path
ROOT=Path(__file__).resolve().parent
FREEZE="cf0f4894fba5acd22700cc6ea7cdc74e6ff80bed"
ZERO,ONE=F(0),F(1)
PATTERNS={
 "NONE":(ZERO,ZERO,ZERO),
 "LOW_UNIFORM":(F(1,2),F(1,2),F(1,2)),
 "HIGH_UNIFORM":(ONE,ONE,ONE),
 "ONE_STRONG_TWO_ZERO":(ONE,ZERO,ZERO),
 "ONE_WEAK_LINK":(ONE,ONE,ZERO),
 "SAME_MEAN_NO_ZERO":(ONE,F(1,2),F(1,2)),
 "HETEROGENEOUS":(ONE,F(1,2),ZERO),
 "HALF_HALF_ZERO":(F(1,2),F(1,2),ZERO)}
AGGREGATORS=("MEAN","BOTTLENECK_MIN")
LEVELS=(ZERO,F(1,2),ONE)
CHANNELS=("PERCEIVED_COLLECTIVE_BELIEF","RESOURCE_GATED_ACTION_PROXY")
WORLDS=tuple(itertools.product(PATTERNS,AGGREGATORS,LEVELS,LEVELS,LEVELS))
CSV_NAME="R308_ALL_864_ORIGINAL_COLLECTIVE_EFFICACY_CHANNEL_SOURCES.csv"
RESULT_NAME="R308_EXACT_COLLECTIVE_EFFICACY_RESULTS.json"
RECEIPT_NAME="R308_MACHINE_RECEIPT.json"

def worldid(pattern,aggregator,cohesion,willingness,resources):
    return f"pattern={pattern}|aggregation={aggregator}|cohesion={cohesion}|willingness={willingness}|resources={resources}"

def evaluate(pattern,aggregator,cohesion,willingness,resources):
    if (pattern,aggregator,cohesion,willingness,resources) not in WORLDS:
        raise ValueError("not in frozen collective efficacy finite universe")
    individual=PATTERNS[pattern]
    mean=sum(individual,ZERO)/3
    bottleneck=min(individual)
    collective_belief=mean if aggregator=="MEAN" else bottleneck
    cohesion_intervention=cohesion*willingness
    proxy=collective_belief*cohesion_intervention*resources
    if not ZERO<=proxy<=collective_belief<=ONE:raise AssertionError("not a valid toy probability")
    return {"member_beliefs":individual,"mean_personal_belief":mean,
      "bottleneck_personal_belief":bottleneck,
      "perceived_collective_efficacy":collective_belief,
      "cohesion_willingness_conjunction":cohesion_intervention,
      "material_resource_gate":resources,"hypothetical_action_propensity_proxy":proxy,
      "belief_minus_action_proxy_gap":collective_belief-proxy}

def source(pattern,aggregator,cohesion,willingness,resources,channel):
    if channel not in CHANNELS:raise ValueError("unfrozen channel")
    v=evaluate(pattern,aggregator,cohesion,willingness,resources)
    return {"world":worldid(pattern,aggregator,cohesion,willingness,resources),
       "belief_pattern":pattern,
       "individual_member_beliefs":";".join(str(x) for x in v["member_beliefs"]),
       "aggregation_rule":aggregator,"social_cohesion_gate":cohesion,
       "willingness_to_intervene_gate":willingness,"resource_availability_gate":resources,
       "mean_member_belief":v["mean_personal_belief"],
       "min_member_belief":v["bottleneck_personal_belief"],
       "perceived_collective_efficacy_belief":v["perceived_collective_efficacy"],
       "cohesion_times_intervention_willingness":v["cohesion_willingness_conjunction"],
       "material_resource_gate":v["material_resource_gate"],
       "hypothetical_action_propensity_proxy":v["hypothetical_action_propensity_proxy"],
       "belief_minus_action_proxy_gap":v["belief_minus_action_proxy_gap"],
       "observation_channel":channel,
       "channel_probability":v["perceived_collective_efficacy"] if channel==CHANNELS[0] else v["hypothetical_action_propensity_proxy"],
       "no_real_intervention_or_violence_observed":True}

def originals():return tuple(source(*world,channel) for world in WORLDS for channel in CHANNELS)

def verify():
    assert len(PATTERNS)==8 and len(WORLDS)==432 and len(originals())==864
    assert len({(r["world"],r["observation_channel"]) for r in originals()})==864
    assert len(set(PATTERNS.values()))==8
    for pattern,agg,c,w,r in WORLDS:
        v=evaluate(pattern,agg,c,w,r)
        assert v["cohesion_willingness_conjunction"]==c*w
        assert v["hypothetical_action_propensity_proxy"]==v["perceived_collective_efficacy"]*c*w*r
        assert v["perceived_collective_efficacy"] in (v["mean_personal_belief"],v["bottleneck_personal_belief"])
        if c==ZERO or w==ZERO or r==ZERO:assert v["hypothetical_action_propensity_proxy"]==ZERO
        if agg=="BOTTLENECK_MIN":assert v["perceived_collective_efficacy"]<=evaluate(pattern,"MEAN",c,w,r)["perceived_collective_efficacy"]
        if c==ZERO:assert v["perceived_collective_efficacy"]==evaluate(pattern,agg,ONE,w,r)["perceived_collective_efficacy"]
        if c<ONE:assert v["hypothetical_action_propensity_proxy"]<=evaluate(pattern,agg,ONE,w,r)["hypothetical_action_propensity_proxy"]
        if w<ONE:assert v["hypothetical_action_propensity_proxy"]<=evaluate(pattern,agg,c,ONE,r)["hypothetical_action_propensity_proxy"]
        if r<ONE:assert v["hypothetical_action_propensity_proxy"]<=evaluate(pattern,agg,c,w,ONE)["hypothetical_action_propensity_proxy"]
    assert evaluate("HIGH_UNIFORM","MEAN",ONE,ONE,ONE)["hypothetical_action_propensity_proxy"]==ONE
    assert evaluate("HIGH_UNIFORM","MEAN",ONE,ZERO,ONE)["perceived_collective_efficacy"]==ONE
    assert evaluate("HIGH_UNIFORM","MEAN",ONE,ZERO,ONE)["hypothetical_action_propensity_proxy"]==ZERO
    assert evaluate("HIGH_UNIFORM","MEAN",ONE,ONE,ZERO)["hypothetical_action_propensity_proxy"]==ZERO
    assert evaluate("ONE_WEAK_LINK","MEAN",ONE,ONE,ONE)["perceived_collective_efficacy"]==F(2,3)
    assert evaluate("SAME_MEAN_NO_ZERO","MEAN",ONE,ONE,ONE)["perceived_collective_efficacy"]==F(2,3)
    assert evaluate("ONE_WEAK_LINK","BOTTLENECK_MIN",ONE,ONE,ONE)["hypothetical_action_propensity_proxy"]==ZERO
    assert evaluate("SAME_MEAN_NO_ZERO","BOTTLENECK_MIN",ONE,ONE,ONE)["hypothetical_action_propensity_proxy"]==F(1,2)
    return True

def emit():
    verify()
    cols=("world","belief_pattern","individual_member_beliefs","aggregation_rule",
      "social_cohesion_gate","willingness_to_intervene_gate","resource_availability_gate",
      "mean_member_belief","min_member_belief","perceived_collective_efficacy_belief",
      "cohesion_times_intervention_willingness","material_resource_gate",
      "hypothetical_action_propensity_proxy","belief_minus_action_proxy_gap",
      "observation_channel","channel_probability",
      "no_real_intervention_or_violence_observed")
    spath=ROOT/CSV_NAME
    with spath.open("w",newline="",encoding="utf-8") as f:
        out=csv.DictWriter(f,fieldnames=cols,lineterminator="\n");out.writeheader()
        for item in originals():out.writerow({key:str(item[key]) for key in cols})
    results={"research_id":"R308","original_catalogue_id":"03-018","freeze_commit":FREEZE,
       "scope":"E1_NEW_PROJECT_COLLECTIVE_EFFICACY_BELIEF_VS_WILLINGNESS_AND_RESOURCE_GATED_ACTION_PROXY",
       "synthetic_worlds":432,"original_source_rows":864,"belief_patterns":8,
       "aggregation_rules":2,"social_gate_level_count":3,
       "project_invented_probability_aggregators_and_intervention_proxy":True,
       "real_Bandura_or_Sampson_or_Goddard_human_data_reanalyzed":False,
       "real_neighborhood_violence_or_school_achievement_predictions":False,
       "new_real_human_E2":0,"new_real_animal_E2":0,"new_historical_E3":0,
       "R073":"FROZEN","PESEN_v0_1":"FROZEN",
       "frozen_reference":{"high_belief_no_willingness_B":"1",
          "high_belief_no_willingness_action_proxy":"0",
          "high_belief_no_resources_action_proxy":"0",
          "one_weak_link_mean":"2/3",
          "same_mean_no_zero_mean":"2/3",
          "one_weak_link_bottleneck_proxy":"0",
          "same_mean_no_zero_bottleneck_proxy":"1/2",
          "all_high_gates_action_proxy":"1"},
       "worlds":[]}
    for world in WORLDS:
        pattern,agg,c,w,r=world;values=evaluate(*world)
        results["worlds"].append({"world":worldid(*world),
          "belief_pattern":pattern,"individual_member_beliefs":[str(x) for x in PATTERNS[pattern]],
          "aggregation_rule":agg,"cohesion":str(c),"willingness":str(w),"resources":str(r),
          "perceived_collective_belief":str(values["perceived_collective_efficacy"]),
          "cohesion_willingness_conjunction":str(values["cohesion_willingness_conjunction"]),
          "hypothetical_action_proxy":str(values["hypothetical_action_propensity_proxy"]),
          "original_channel_source_rows":[{key:str(source(*world,channel)[key]) for key in cols if key!="world"} for channel in CHANNELS]})
    rpath=ROOT/RESULT_NAME
    rpath.write_text(json.dumps(results,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    receipt={"research_id":"R308","freeze_commit":FREEZE,"source_rows":864,
       "source_sha256":hashlib.sha256(spath.read_bytes()).hexdigest(),
       "results_sha256":hashlib.sha256(rpath.read_bytes()).hexdigest(),
       "new_real_E2":0,"new_historical_E3":0}
    (ROOT/RECEIPT_NAME).write_text(json.dumps(receipt,indent=2)+"\n",encoding="utf-8")
    return receipt

class Tests(unittest.TestCase):
    def test_all(self):self.assertTrue(verify())
    def test_worlds(self):self.assertEqual(len(WORLDS),432)
    def test_sources(self):self.assertEqual(len(originals()),864)
    def test_no_willingness(self):self.assertEqual(evaluate("HIGH_UNIFORM","MEAN",ONE,ZERO,ONE)["hypothetical_action_propensity_proxy"],ZERO)
    def test_no_resources(self):self.assertEqual(evaluate("HIGH_UNIFORM","MEAN",ONE,ONE,ZERO)["hypothetical_action_propensity_proxy"],ZERO)
    def test_all_gates(self):self.assertEqual(evaluate("HIGH_UNIFORM","MEAN",ONE,ONE,ONE)["hypothetical_action_propensity_proxy"],ONE)
    def test_equal_mean(self):self.assertEqual(evaluate("ONE_WEAK_LINK","MEAN",ONE,ONE,ONE)["perceived_collective_efficacy"],evaluate("SAME_MEAN_NO_ZERO","MEAN",ONE,ONE,ONE)["perceived_collective_efficacy"])
    def test_bottleneck_diff(self):self.assertEqual(evaluate("SAME_MEAN_NO_ZERO","BOTTLENECK_MIN",ONE,ONE,ONE)["hypothetical_action_propensity_proxy"],F(1,2))
    def test_belief_not_resource(self):self.assertEqual(evaluate("HIGH_UNIFORM","MEAN",ONE,ONE,ZERO)["perceived_collective_efficacy"],ONE)
    def test_zero_cohesion(self):self.assertEqual(evaluate("HIGH_UNIFORM","MEAN",ZERO,ONE,ONE)["hypothetical_action_propensity_proxy"],ZERO)
    def test_no_human(self):self.assertTrue(source("HIGH_UNIFORM","MEAN",ONE,ONE,ONE,CHANNELS[0])["no_real_intervention_or_violence_observed"])
    def test_bad_pattern(self):
        with self.assertRaises(ValueError):evaluate("UNKNOWN","MEAN",ONE,ONE,ONE)
    def test_bad_aggregation(self):
        with self.assertRaises(ValueError):evaluate("HIGH_UNIFORM","HARMONIC",ONE,ONE,ONE)
    def test_bad_gate(self):
        with self.assertRaises(ValueError):evaluate("HIGH_UNIFORM","MEAN",F(1,4),ONE,ONE)
    def test_bad_channel(self):
        with self.assertRaises(ValueError):source("HIGH_UNIFORM","MEAN",ONE,ONE,ONE,"OBSERVED_CRIME")

def generated(world,channel,kind):
    def check(self):
        row=source(*world,channel)
        v=evaluate(*world)
        if kind=="belief":self.assertEqual(row["perceived_collective_efficacy_belief"],v["perceived_collective_efficacy"])
        elif kind=="action":self.assertEqual(row["hypothetical_action_propensity_proxy"],v["hypothetical_action_propensity_proxy"])
        elif kind=="response":self.assertEqual(row["channel_probability"],v["perceived_collective_efficacy"] if channel==CHANNELS[0] else v["hypothetical_action_propensity_proxy"])
        else:raise AssertionError(kind)
    return check
for i,world in enumerate(WORLDS):
    for channel in CHANNELS:
        for kind in ("belief","action","response"):
            setattr(Tests,f"test_world{i}_{channel.lower()}_{kind}",generated(world,channel,kind))

if __name__=="__main__":
    p=argparse.ArgumentParser();m=p.add_mutually_exclusive_group(required=True)
    m.add_argument("--test",action="store_true");m.add_argument("--emit",action="store_true")
    args=p.parse_args()
    if args.test:unittest.main(argv=["R308"],verbosity=1)
    else:print(json.dumps(emit(),indent=2))
