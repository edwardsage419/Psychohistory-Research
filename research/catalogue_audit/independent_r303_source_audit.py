#!/usr/bin/env python3
"""Independent R303 synthetic social learning acquisition/expression exact enumeration; NO production imports."""
from __future__ import annotations
import argparse,csv,hashlib,itertools,json,unittest
from fractions import Fraction as Q
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]/"research/R303"
SOURCE=ROOT/"R303_ALL_486_ORIGINAL_OBSERVATIONAL_SOURCE_PHASES.csv"
RESULT=ROOT/"R303_EXACT_ACQUISITION_VS_EXPRESSION_RESULTS.json"
RECEIPT=ROOT/"R303_MACHINE_RECEIPT.json"
LEVELS=(Q(0),Q(1,2),Q(1))
CONSEQUENCE={"REWARDED":Q(1),"NO_CONSEQUENCE":Q(1,2),"PUNISHED":Q(1,4)}
PHASES=("SPONTANEOUS","INCENTIVIZED")
WORLDS=list((a,r,p,m,c) for a,r,p,m in itertools.product(LEVELS,repeat=4) for c in CONSEQUENCE)
ZERO,ONE=Q(0),Q(1)

def obj(p):return json.loads(p.read_text(encoding="utf-8"))
def load():
    with SOURCE.open(newline="",encoding="utf-8") as f:return list(csv.DictReader(f))
def wid(w):
    a,r,p,m,c=w
    return f"attention={a}|retention={r}|production={p}|motivation={m}|model_consequence={c}"

def independently_enumerate(w):
    # Enumerate five independent Bernoulli gates: attention, retention,
    # production, own baseline motivation, model vicarious consequence.
    a,r,p,m,c=w
    parameters=(a,r,p,m,CONSEQUENCE[c])
    acquired=available=spontaneous=prompted=ZERO
    for switches in itertools.product((0,1),repeat=5):
        mass=ONE
        for bit,prob in zip(switches,parameters):
            mass*=prob if bit==1 else ONE-prob
        observed=switches[0] and switches[1]
        reproduced=observed and switches[2]
        spontaneous_on=reproduced and switches[3] and switches[4]
        if observed:acquired+=mass
        if reproduced:
            available+=mass
            prompted+=mass
        if spontaneous_on:spontaneous+=mass
    return {"latent_acquisition_probability":acquired,
       "production_available_probability":available,
       "spontaneous_expression_factor":m*CONSEQUENCE[c],
       "spontaneous_response_probability":spontaneous,
       "incentivized_response_probability":prompted,
       "gap":prompted-spontaneous,
       "consequence_factor":CONSEQUENCE[c]}

def verify(rows,result):
    if len(rows)!=486 or len(result["worlds"])!=243:
        raise AssertionError("incomplete full source worlds")
    if result["synthetic_worlds"]!=243 or result["original_phase_source_rows"]!=486:
        raise AssertionError("frozen science universe count violated")
    universe={(w,phase) for w in WORLDS for phase in PHASES}
    seen={}
    for s in rows:
        try:
            w=tuple(Q(s[z]) for z in ("attention","retention","motor_production","baseline_motivation"))+(s["model_consequence"],)
            phase=s["phase"]
        except (ValueError,KeyError,ZeroDivisionError) as err:raise AssertionError("bad parameters") from err
        key=(w,phase)
        if key not in universe or key in seen:raise AssertionError("source missing/duplicate/out-of-grid")
        if s["world"]!=wid(w):raise AssertionError("wrong original world ID")
        expected=independently_enumerate(w)
        if Q(s["consequence_factor"])!=expected["consequence_factor"]:raise AssertionError("consequence tampering")
        if Q(s["latent_acquisition_probability"])!=expected["latent_acquisition_probability"]:raise AssertionError("acquisition tampering")
        if Q(s["production_available_probability"])!=expected["production_available_probability"]:raise AssertionError("reproduction tampering")
        e=expected["spontaneous_expression_factor"] if phase=="SPONTANEOUS" else ONE
        if Q(s["expression_factor"])!=e:raise AssertionError("expression factor tampering")
        imitation=expected["spontaneous_response_probability"] if phase=="SPONTANEOUS" else expected["incentivized_response_probability"]
        if Q(s["imitative_response_probability"])!=imitation:raise AssertionError("phase response tampering")
        if Q(s["no_observation_baseline_probability"])!=ZERO:raise AssertionError("no-observation control tampering")
        if Q(s["incentive_minus_spontaneous_probability"])!=expected["gap"]:raise AssertionError("performance gap tampering")
        seen[key]=s
    if set(seen)!=universe:raise AssertionError("sources do not cover every original phase")
    strict=0
    for ix,w in enumerate(WORLDS):
        a,r,p,m,c=w
        v=independently_enumerate(w)
        item=result["worlds"][ix]
        if item["world"]!=wid(w) or item["model_consequence"]!=c:
            raise AssertionError("result world identity wrong")
        for field,val in (("attention",a),("retention",r),("motor_production",p),("baseline_motivation",m)):
            if item[field]!=str(val):raise AssertionError("gate result tamper")
        for field,expected in (("latent_acquisition_probability",v["latent_acquisition_probability"]),
            ("production_available_probability",v["production_available_probability"]),
            ("spontaneous_expression_factor",v["spontaneous_expression_factor"]),
            ("spontaneous_imitation_probability",v["spontaneous_response_probability"]),
            ("incentivized_imitation_probability",v["incentivized_response_probability"]),
            ("incentive_performance_gap",v["gap"])):
            if item[field]!=str(expected):raise AssertionError("world value differs: "+field)
        if item["original_phases"]!=2:raise AssertionError("phase result count wrong")
    for a,r,p,m in itertools.product(LEVELS,repeat=4):
        values=[independently_enumerate((a,r,p,m,c)) for c in CONSEQUENCE]
        if len({v["latent_acquisition_probability"] for v in values})!=1:raise AssertionError("acquisition changes spuriously")
        if len({v["incentivized_response_probability"] for v in values})!=1:raise AssertionError("incentive failed to equalize")
        if a>ZERO and r>ZERO and p>ZERO and m>ZERO:
            strict+=1
            if not values[0]["spontaneous_response_probability"]>values[1]["spontaneous_response_probability"]>values[2]["spontaneous_response_probability"]:
                raise AssertionError("spontaneous consequence ordering")
    if strict!=16:raise AssertionError("positive-gates grid count wrong")
    reference={"fully_attending_retaining_producing_motivation_half_acquired":"1",
      "fully_attending_retaining_producing_motivation_half_REWARDED_spontaneous":"1/2",
      "fully_attending_retaining_producing_motivation_half_NEUTRAL_spontaneous":"1/4",
      "fully_attending_retaining_producing_motivation_half_PUNISHED_spontaneous":"1/8",
      "all_three_incentivized":"1","strong_spontaneous_order_gate_tuples":16}
    if result["reference_case"]!=reference:raise AssertionError("preregistered case mismatch")
    return {"R303_independent_five_binary_gate_enumeration":"PASS",
      "full_original_phase_rows":486,"synthetic_worlds":243,
      "strictly_ordered_spontaneous_gate_tuples":16,
      "author_original_quantitative_formula_replicated":False,
      "new_real_human_animal_E2":0,"historical_E3":0}

def audit():
    receipt,result=obj(RECEIPT),obj(RESULT)
    freeze="5adc32ae7c91c150fe82bb16f99a059d2a62e991"
    if receipt["freeze_commit"]!=freeze or result["freeze_commit"]!=freeze:raise AssertionError("not frozen first")
    if result["research_id"]!="R303" or result["original_catalogue_id"]!="03-001":raise AssertionError("wrong research original")
    if result["research_project_custom_multiplicative_probability_equations_not_bandura_original"] is not True:
        raise AssertionError("false author equation")
    if result["Bandura_original_1965_child_behavior_data_reanalyzed"] is not False:
        raise AssertionError("fictitious Bandura real results")
    if result["Najar_R063_social_value_learning_human_data_reused"] is not False:
        raise AssertionError("R063 real data reused falsely")
    if any(result[k]!=0 for k in ("new_real_human_E2","new_real_animal_E2","new_historical_E3")):
        raise AssertionError("synthetic task counted empirical")
    if receipt["source_rows"]!=486 or receipt["new_real_E2"]!=0 or receipt["new_historical_E3"]!=0:
        raise AssertionError("receipt metadata changed")
    if hashlib.sha256(SOURCE.read_bytes()).hexdigest()!=receipt["source_sha256"]:raise AssertionError("source sha mismatch")
    if hashlib.sha256(RESULT.read_bytes()).hexdigest()!=receipt["results_sha256"]:raise AssertionError("result sha mismatch")
    return {**verify(load(),result),"source_sha256":receipt["source_sha256"],"results_sha256":receipt["results_sha256"]}

class Tests(unittest.TestCase):
    def test_all(self):self.assertEqual(audit()["full_original_phase_rows"],486)
    def test_worlds(self):self.assertEqual(len(WORLDS),243)
    def test_sample_reward(self):self.assertEqual(independently_enumerate((ONE,ONE,ONE,Q(1,2),"REWARDED"))["spontaneous_response_probability"],Q(1,2))
    def test_sample_no_consequence(self):self.assertEqual(independently_enumerate((ONE,ONE,ONE,Q(1,2),"NO_CONSEQUENCE"))["spontaneous_response_probability"],Q(1,4))
    def test_sample_punished(self):self.assertEqual(independently_enumerate((ONE,ONE,ONE,Q(1,2),"PUNISHED"))["spontaneous_response_probability"],Q(1,8))
    def test_same_incentive(self):self.assertEqual(independently_enumerate((ONE,ONE,ONE,Q(1,2),"PUNISHED"))["incentivized_response_probability"],ONE)
    def test_knowledge_without_production(self):
        v=independently_enumerate((ONE,ONE,ZERO,ONE,"REWARDED"))
        self.assertEqual(v["latent_acquisition_probability"],ONE)
        self.assertEqual(v["incentivized_response_probability"],ZERO)
    def test_no_motivation_incentive_possible(self):
        v=independently_enumerate((ONE,ONE,ONE,ZERO,"REWARDED"))
        self.assertEqual(v["spontaneous_response_probability"],ZERO)
        self.assertEqual(v["incentivized_response_probability"],ONE)
    def test_missing(self):
        with self.assertRaises(AssertionError):verify(load()[:-1],obj(RESULT))
    def test_duplicate(self):
        rows=load();rows[1]=dict(rows[0])
        with self.assertRaises(AssertionError):verify(rows,obj(RESULT))
    def test_wrong_consequence(self):
        rows=load();rows[0]=dict(rows[0]);rows[0]["consequence_factor"]="1/8"
        with self.assertRaises(AssertionError):verify(rows,obj(RESULT))
    def test_wrong_acquisition(self):
        rows=load();rows[0]=dict(rows[0]);rows[0]["latent_acquisition_probability"]="1"
        with self.assertRaises(AssertionError):verify(rows,obj(RESULT))
    def test_wrong_phase(self):
        rows=load();rows[0]=dict(rows[0]);rows[0]["phase"]="LEARNED"
        with self.assertRaises(AssertionError):verify(rows,obj(RESULT))
    def test_wrong_expression(self):
        rows=load();rows[0]=dict(rows[0]);rows[0]["imitative_response_probability"]="1"
        with self.assertRaises(AssertionError):verify(rows,obj(RESULT))
    def test_incentive_gap(self):
        rows=load();rows[0]=dict(rows[0]);rows[0]["incentive_minus_spontaneous_probability"]="1"
        with self.assertRaises(AssertionError):verify(rows,obj(RESULT))
    def test_result_tamper(self):
        j=obj(RESULT);j["worlds"][0]["spontaneous_imitation_probability"]="9"
        with self.assertRaises(AssertionError):verify(load(),j)
    def test_digest_tamper(self):
        self.assertNotEqual(hashlib.sha256(SOURCE.read_bytes()+b"x").hexdigest(),obj(RECEIPT)["source_sha256"])

if __name__=="__main__":
    p=argparse.ArgumentParser();g=p.add_mutually_exclusive_group(required=True)
    g.add_argument("--test",action="store_true");g.add_argument("--audit",action="store_true")
    a=p.parse_args()
    if a.test:unittest.main(argv=["R303 audit"],verbosity=1)
    else:print(json.dumps(audit(),ensure_ascii=False,indent=2))
