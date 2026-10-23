#!/usr/bin/env python3
"""R308 independent exact 4-bit gate enumeration for belief-vs-action-proxy E1, no main-model imports."""
from __future__ import annotations
import argparse,csv,hashlib,itertools,json,unittest
from fractions import Fraction as Q
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]/"research/R308"
CSV=ROOT/"R308_ALL_864_ORIGINAL_COLLECTIVE_EFFICACY_CHANNEL_SOURCES.csv"
RESULT=ROOT/"R308_EXACT_COLLECTIVE_EFFICACY_RESULTS.json"
RECEIPT=ROOT/"R308_MACHINE_RECEIPT.json"
Z,O=Q(0),Q(1)
PATTERNS={
 "NONE":(Z,Z,Z),"LOW_UNIFORM":(Q(1,2),Q(1,2),Q(1,2)),
 "HIGH_UNIFORM":(O,O,O),"ONE_STRONG_TWO_ZERO":(O,Z,Z),
 "ONE_WEAK_LINK":(O,O,Z),"SAME_MEAN_NO_ZERO":(O,Q(1,2),Q(1,2)),
 "HETEROGENEOUS":(O,Q(1,2),Z),"HALF_HALF_ZERO":(Q(1,2),Q(1,2),Z)}
AGGREGATORS=("MEAN","BOTTLENECK_MIN")
LEVELS=(Z,Q(1,2),O)
CHANNELS=("PERCEIVED_COLLECTIVE_BELIEF","RESOURCE_GATED_ACTION_PROXY")
WORLDS=tuple(itertools.product(PATTERNS,AGGREGATORS,LEVELS,LEVELS,LEVELS))
FIELDS=("belief_pattern","individual_member_beliefs","aggregation_rule",
   "social_cohesion_gate","willingness_to_intervene_gate","resource_availability_gate",
   "mean_member_belief","min_member_belief","perceived_collective_efficacy_belief",
   "cohesion_times_intervention_willingness","material_resource_gate",
   "hypothetical_action_propensity_proxy","belief_minus_action_proxy_gap",
   "observation_channel","channel_probability","no_real_intervention_or_violence_observed")

def obj(path):return json.loads(path.read_text(encoding="utf-8"))
def load():
    with CSV.open(newline="",encoding="utf-8") as f:return list(csv.DictReader(f))
def name(world):
    p,g,c,w,r=world
    return f"pattern={p}|aggregation={g}|cohesion={c}|willingness={w}|resources={r}"

def independently_enumerate(world):
    p,g,c,w,r=world
    individual=PATTERNS[p]
    avg=sum(individual,Z)/3
    minimum=sorted(individual)[0]
    belief=avg if g=="MEAN" else minimum
    # Enumerate Bernoulli outcomes for four separately specified toy gates
    # (belief, cohesion, willingness, resources), summing joint mass only if all succeed.
    action=Z
    for bits in itertools.product((0,1),repeat=4):
        mass=O
        for bit,prob in zip(bits,(belief,c,w,r)):
            mass*=prob if bit else O-prob
        if bits==(1,1,1,1):action+=mass
    return {"member_beliefs":individual,"mean":avg,"min":minimum,
      "belief":belief,"cohesion_willingness":c*w,"resources":r,
      "action":action,"gap":belief-action}

def expected_row(world,channel):
    p,g,c,w,r=world
    v=independently_enumerate(world)
    x={"belief_pattern":p,"individual_member_beliefs":";".join(str(z) for z in v["member_beliefs"]),
       "aggregation_rule":g,"social_cohesion_gate":c,"willingness_to_intervene_gate":w,
       "resource_availability_gate":r,"mean_member_belief":v["mean"],
       "min_member_belief":v["min"],"perceived_collective_efficacy_belief":v["belief"],
       "cohesion_times_intervention_willingness":v["cohesion_willingness"],
       "material_resource_gate":v["resources"],
       "hypothetical_action_propensity_proxy":v["action"],
       "belief_minus_action_proxy_gap":v["gap"],
       "observation_channel":channel,
       "channel_probability":v["belief"] if channel==CHANNELS[0] else v["action"],
       "no_real_intervention_or_violence_observed":True}
    return {k:str(x[k]) for k in FIELDS}

def verify(rows,results):
    if len(rows)!=864 or len(results["worlds"])!=432 or results["original_source_rows"]!=864:
        raise AssertionError("source universe must be complete")
    if results["synthetic_worlds"]!=432 or results["belief_patterns"]!=8:
        raise AssertionError("world count altered")
    universe={(world,channel) for world in WORLDS for channel in CHANNELS}
    seen={}
    for item in rows:
        try:
            world=(item["belief_pattern"],item["aggregation_rule"],
                   Q(item["social_cohesion_gate"]),Q(item["willingness_to_intervene_gate"]),
                   Q(item["resource_availability_gate"]))
            channel=item["observation_channel"]
        except (KeyError,ValueError,ZeroDivisionError) as e:raise AssertionError("bad source dimensions") from e
        key=(world,channel)
        if key not in universe or key in seen:raise AssertionError("duplicate/out of grid original source")
        if item["world"]!=name(world):raise AssertionError("wrong world ID")
        for k,v in expected_row(world,channel).items():
            if item[k]!=v:raise AssertionError("source tampering: "+k)
        seen[key]=item
    if set(seen)!=universe:raise AssertionError("missing source")
    for idx,world in enumerate(WORLDS):
        result=results["worlds"][idx]
        p,g,c,w,r=world
        v=independently_enumerate(world)
        expected={"world":name(world),"belief_pattern":p,
          "individual_member_beliefs":[str(x) for x in PATTERNS[p]],
          "aggregation_rule":g,"cohesion":str(c),"willingness":str(w),"resources":str(r),
          "perceived_collective_belief":str(v["belief"]),
          "cohesion_willingness_conjunction":str(v["cohesion_willingness"]),
          "hypothetical_action_proxy":str(v["action"]),
          "original_channel_source_rows":[expected_row(world,ch) for ch in CHANNELS]}
        if result!=expected:raise AssertionError("result JSON wrong or incomplete")
        if not Z<=v["action"]<=v["belief"]<=O:raise AssertionError("inequality error")
        if not c or not w or not r:
            if v["action"]!=Z:raise AssertionError("zero-gate false efficacy")
    reference={"high_belief_no_willingness_B":"1",
      "high_belief_no_willingness_action_proxy":"0",
      "high_belief_no_resources_action_proxy":"0",
      "one_weak_link_mean":"2/3",
      "same_mean_no_zero_mean":"2/3",
      "one_weak_link_bottleneck_proxy":"0",
      "same_mean_no_zero_bottleneck_proxy":"1/2",
      "all_high_gates_action_proxy":"1"}
    if results["frozen_reference"]!=reference:raise AssertionError("predefined contrast altered")
    return {"full_original_synthetic_rows":864,"artificial_worlds":432,
      "no_import_independent_4_Bernoulli_gate_enumeration":"PASS",
      "same_mean_bottleneck_difference_verified":True,
      "human_violence_or_teacher_achievement_E2":0,
      "historical_E3":0}

def audit():
    r,j=obj(RECEIPT),obj(RESULT)
    freeze="cf0f4894fba5acd22700cc6ea7cdc74e6ff80bed"
    if r["freeze_commit"]!=freeze or j["freeze_commit"]!=freeze:
        raise AssertionError("protocol freeze drift")
    if j["research_id"]!="R308" or j["original_catalogue_id"]!="03-018":
        raise AssertionError("wrong research original")
    if j["project_invented_probability_aggregators_and_intervention_proxy"] is not True:
        raise AssertionError("false original psychology equation")
    if j["real_Bandura_or_Sampson_or_Goddard_human_data_reanalyzed"] is not False:
        raise AssertionError("fictional real respondent source")
    if j["real_neighborhood_violence_or_school_achievement_predictions"] is not False:
        raise AssertionError("fictitious outcome prediction")
    if any(j[k]!=0 for k in ("new_real_human_E2","new_real_animal_E2","new_historical_E3")):
        raise AssertionError("synthetic counted empirical")
    if r["source_rows"]!=864 or r["new_real_E2"]!=0 or r["new_historical_E3"]!=0:
        raise AssertionError("receipt empirical promotion")
    if hashlib.sha256(CSV.read_bytes()).hexdigest()!=r["source_sha256"]:
        raise AssertionError("source byte SHA")
    if hashlib.sha256(RESULT.read_bytes()).hexdigest()!=r["results_sha256"]:
        raise AssertionError("result byte SHA")
    return {**verify(load(),j),"source_sha256":r["source_sha256"],"results_sha256":r["results_sha256"]}

class Tests(unittest.TestCase):
    def test_all(self):self.assertEqual(audit()["full_original_synthetic_rows"],864)
    def test_worlds(self):self.assertEqual(len(WORLDS),432)
    def test_high_all(self):self.assertEqual(independently_enumerate(("HIGH_UNIFORM","MEAN",O,O,O))["action"],O)
    def test_belief_not_action(self):self.assertEqual(independently_enumerate(("HIGH_UNIFORM","MEAN",O,Z,O))["belief"],O)
    def test_no_willingness(self):self.assertEqual(independently_enumerate(("HIGH_UNIFORM","MEAN",O,Z,O))["action"],Z)
    def test_no_resources(self):self.assertEqual(independently_enumerate(("HIGH_UNIFORM","MEAN",O,O,Z))["action"],Z)
    def test_means_same(self):self.assertEqual(independently_enumerate(("ONE_WEAK_LINK","MEAN",O,O,O))["belief"],independently_enumerate(("SAME_MEAN_NO_ZERO","MEAN",O,O,O))["belief"])
    def test_min_different(self):self.assertEqual(independently_enumerate(("SAME_MEAN_NO_ZERO","BOTTLENECK_MIN",O,O,O))["action"],Q(1,2))
    def test_missing(self):
        with self.assertRaises(AssertionError):verify(load()[:-1],obj(RESULT))
    def test_duplicate(self):
        rows=load();rows[1]=dict(rows[0])
        with self.assertRaises(AssertionError):verify(rows,obj(RESULT))
    def test_false_mean(self):
        rows=load();rows[1]=dict(rows[1]);rows[1]["mean_member_belief"]="99"
        with self.assertRaises(AssertionError):verify(rows,obj(RESULT))
    def test_false_belief(self):
        rows=load();rows[1]=dict(rows[1]);rows[1]["perceived_collective_efficacy_belief"]="99"
        with self.assertRaises(AssertionError):verify(rows,obj(RESULT))
    def test_false_resources(self):
        rows=load();rows[1]=dict(rows[1]);rows[1]["resource_availability_gate"]="1/3"
        with self.assertRaises(AssertionError):verify(rows,obj(RESULT))
    def test_false_action(self):
        rows=load();rows[1]=dict(rows[1]);rows[1]["hypothetical_action_propensity_proxy"]="99"
        with self.assertRaises(AssertionError):verify(rows,obj(RESULT))
    def test_false_channel(self):
        rows=load();rows[1]=dict(rows[1]);rows[1]["observation_channel"]="OBSERVED_VIOLENCE"
        with self.assertRaises(AssertionError):verify(rows,obj(RESULT))
    def test_result_tamper(self):
        j=obj(RESULT);j["worlds"][0]["hypothetical_action_proxy"]="9"
        with self.assertRaises(AssertionError):verify(load(),j)
    def test_reference_tamper(self):
        j=obj(RESULT);j["frozen_reference"]["one_weak_link_bottleneck_proxy"]="1"
        with self.assertRaises(AssertionError):verify(load(),j)
    def test_sha_tamper(self):
        self.assertNotEqual(hashlib.sha256(CSV.read_bytes()+b"x").hexdigest(),obj(RECEIPT)["source_sha256"])

if __name__=="__main__":
    p=argparse.ArgumentParser()
    g=p.add_mutually_exclusive_group(required=True)
    g.add_argument("--test",action="store_true");g.add_argument("--audit",action="store_true")
    a=p.parse_args()
    if a.test:unittest.main(argv=["R308 independent"],verbosity=1)
    else:print(json.dumps(audit(),ensure_ascii=False,indent=2))
