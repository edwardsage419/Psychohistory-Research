#!/usr/bin/env python3
"""R303 Bandura 1965-inspired (NOT author-parameterized) synthetic E1 observational acquisition/expression."""
from __future__ import annotations
import argparse,csv,hashlib,itertools,json,unittest
from fractions import Fraction as F
from pathlib import Path

ROOT=Path(__file__).resolve().parent
FREEZE="5adc32ae7c91c150fe82bb16f99a059d2a62e991"
Z,O=F(0),F(1)
LEVELS=(Z,F(1,2),O)
CONSEQUENCE_FACTOR={"REWARDED":O,"NO_CONSEQUENCE":F(1,2),"PUNISHED":F(1,4)}
CONSEQUENCES=tuple(CONSEQUENCE_FACTOR)
PHASES=("SPONTANEOUS","INCENTIVIZED")
WORLDS=tuple(itertools.product(LEVELS,repeat=4))
CONDITIONS=tuple((a,r,p,m,c) for (a,r,p,m) in WORLDS for c in CONSEQUENCES)
CSV_NAME="R303_ALL_486_ORIGINAL_OBSERVATIONAL_SOURCE_PHASES.csv"
RESULT_NAME="R303_EXACT_ACQUISITION_VS_EXPRESSION_RESULTS.json"
RECEIPT_NAME="R303_MACHINE_RECEIPT.json"

def world_id(a,r,p,m,c):
    return f"attention={a}|retention={r}|production={p}|motivation={m}|model_consequence={c}"

def evaluate(a,r,p,m,c):
    if (a,r,p,m,c) not in CONDITIONS:raise ValueError("outside frozen grid")
    learned=a*r
    available=learned*p
    c_factor=CONSEQUENCE_FACTOR[c]
    spontaneous_expression=m*c_factor
    spontaneous=available*spontaneous_expression
    prompted=available
    return {"acquired_trace_probability":learned,
      "production_available_probability":available,
      "consequence_factor":c_factor,
      "spontaneous_expression_factor":spontaneous_expression,
      "spontaneous_imitation_probability":spontaneous,
      "incentivized_imitation_probability":prompted,
      "incentive_performance_gap":prompted-spontaneous}

def row(a,r,p,m,c,phase):
    if phase not in PHASES:raise ValueError("invalid phase")
    values=evaluate(a,r,p,m,c)
    return {"world":world_id(a,r,p,m,c),"attention":a,"retention":r,
      "motor_production":p,"baseline_motivation":m,"model_consequence":c,
      "consequence_factor":values["consequence_factor"],"phase":phase,
      "latent_acquisition_probability":values["acquired_trace_probability"],
      "production_available_probability":values["production_available_probability"],
      "expression_factor":values["spontaneous_expression_factor"] if phase=="SPONTANEOUS" else O,
      "imitative_response_probability":values["spontaneous_imitation_probability"] if phase=="SPONTANEOUS" else values["incentivized_imitation_probability"],
      "no_observation_baseline_probability":Z,
      "incentive_minus_spontaneous_probability":values["incentive_performance_gap"]}

def sources():
    return tuple(row(*condition,phase) for condition in CONDITIONS for phase in PHASES)

def validate():
    assert len(WORLDS)==81 and len(CONDITIONS)==243 and len(sources())==486
    assert len({(r["world"],r["phase"]) for r in sources()})==486
    strict=0
    for a,r,p,m in WORLDS:
        vs=[evaluate(a,r,p,m,c) for c in CONSEQUENCES]
        assert len(set(x["acquired_trace_probability"] for x in vs))==1
        assert len(set(x["incentivized_imitation_probability"] for x in vs))==1
        assert vs[0]["spontaneous_imitation_probability"]>=vs[1]["spontaneous_imitation_probability"]>=vs[2]["spontaneous_imitation_probability"]
        if all(x>Z for x in (a,r,p,m)):
            strict+=1
            assert vs[0]["spontaneous_imitation_probability"]>vs[1]["spontaneous_imitation_probability"]>vs[2]["spontaneous_imitation_probability"]
    assert strict==16
    for condition in CONDITIONS:
        v=evaluate(*condition)
        assert all(Z<=x<=O for x in v.values())
        assert v["incentivized_imitation_probability"]>=v["spontaneous_imitation_probability"]
        assert v["acquired_trace_probability"]==condition[0]*condition[1]
        assert v["production_available_probability"]==condition[0]*condition[1]*condition[2]
        assert v["spontaneous_imitation_probability"]==condition[0]*condition[1]*condition[2]*condition[3]*CONSEQUENCE_FACTOR[condition[4]]
        for phase in PHASES:
            s=row(*condition,phase)
            assert s["imitative_response_probability"]==(v["spontaneous_imitation_probability"] if phase=="SPONTANEOUS" else v["incentivized_imitation_probability"])
    for cons,expected,gap in (("REWARDED",F(1,2),F(1,2)),("NO_CONSEQUENCE",F(1,4),F(3,4)),("PUNISHED",F(1,8),F(7,8))):
        v=evaluate(O,O,O,F(1,2),cons)
        assert (v["acquired_trace_probability"],v["incentivized_imitation_probability"])==(O,O)
        assert v["spontaneous_imitation_probability"]==expected and v["incentive_performance_gap"]==gap
    assert evaluate(Z,O,O,O,"REWARDED")["incentivized_imitation_probability"]==Z
    assert evaluate(O,O,Z,O,"REWARDED")["acquired_trace_probability"]==O
    assert evaluate(O,O,Z,O,"REWARDED")["incentivized_imitation_probability"]==Z
    assert evaluate(O,O,O,Z,"PUNISHED")["spontaneous_imitation_probability"]==Z
    assert evaluate(O,O,O,Z,"PUNISHED")["incentivized_imitation_probability"]==O
    return True

def emit():
    validate()
    cols=("world","attention","retention","motor_production","baseline_motivation",
      "model_consequence","consequence_factor","phase","latent_acquisition_probability",
      "production_available_probability","expression_factor","imitative_response_probability",
      "no_observation_baseline_probability","incentive_minus_spontaneous_probability")
    csvpath=ROOT/CSV_NAME
    with csvpath.open("w",newline="",encoding="utf-8") as f:
        w=csv.DictWriter(f,fieldnames=cols,lineterminator="\n")
        w.writeheader()
        for source in sources():w.writerow({k:str(source[k]) for k in cols})
    data={"research_id":"R303","original_catalogue_id":"03-001","freeze_commit":FREEZE,
      "scope":"E1_SYNTHETIC_ILLUSTRATION_BANDURA_ACQUISITION_VERSUS_EXPRESSION_NOT_AUTHOR_FITTED_MODEL",
      "research_project_custom_multiplicative_probability_equations_not_bandura_original":True,
      "synthetic_worlds":243,"original_phase_source_rows":486,
      "distinct_four_gate_tuples":81,"phases_each":2,"consequence_levels_each":3,
      "new_real_human_E2":0,"new_real_animal_E2":0,"new_historical_E3":0,
      "Bandura_original_1965_child_behavior_data_reanalyzed":False,
      "Najar_R063_social_value_learning_human_data_reused":False,
      "R073":"FROZEN","PESEN_v0_1":"FROZEN","worlds":[]}
    for a,r,p,m,c in CONDITIONS:
        v=evaluate(a,r,p,m,c)
        data["worlds"].append({"world":world_id(a,r,p,m,c),
          "attention":str(a),"retention":str(r),"motor_production":str(p),
          "baseline_motivation":str(m),"model_consequence":c,
          "latent_acquisition_probability":str(v["acquired_trace_probability"]),
          "production_available_probability":str(v["production_available_probability"]),
          "spontaneous_expression_factor":str(v["spontaneous_expression_factor"]),
          "spontaneous_imitation_probability":str(v["spontaneous_imitation_probability"]),
          "incentivized_imitation_probability":str(v["incentivized_imitation_probability"]),
          "incentive_performance_gap":str(v["incentive_performance_gap"]),
          "original_phases":2})
    data["reference_case"]={
      "fully_attending_retaining_producing_motivation_half_acquired":"1",
      "fully_attending_retaining_producing_motivation_half_REWARDED_spontaneous":"1/2",
      "fully_attending_retaining_producing_motivation_half_NEUTRAL_spontaneous":"1/4",
      "fully_attending_retaining_producing_motivation_half_PUNISHED_spontaneous":"1/8",
      "all_three_incentivized":"1","strong_spontaneous_order_gate_tuples":16}
    rp=ROOT/RESULT_NAME
    rp.write_text(json.dumps(data,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    rec={"research_id":"R303","freeze_commit":FREEZE,"source_rows":486,
      "source_sha256":hashlib.sha256(csvpath.read_bytes()).hexdigest(),
      "results_sha256":hashlib.sha256(rp.read_bytes()).hexdigest(),
      "new_real_E2":0,"new_historical_E3":0}
    (ROOT/RECEIPT_NAME).write_text(json.dumps(rec,indent=2)+"\n",encoding="utf-8")
    return rec

class Tests(unittest.TestCase):
    def test_all(self):self.assertTrue(validate())
    def test_world_count(self):self.assertEqual(len(CONDITIONS),243)
    def test_source_count(self):self.assertEqual(len(sources()),486)
    def test_acquisition_equals_attention_retention(self):self.assertEqual(evaluate(O,F(1,2),O,O,"PUNISHED")["acquired_trace_probability"],F(1,2))
    def test_rewarded(self):self.assertEqual(evaluate(O,O,O,F(1,2),"REWARDED")["spontaneous_imitation_probability"],F(1,2))
    def test_punished(self):self.assertEqual(evaluate(O,O,O,F(1,2),"PUNISHED")["spontaneous_imitation_probability"],F(1,8))
    def test_rewarded_incentive(self):self.assertEqual(evaluate(O,O,O,F(1,2),"REWARDED")["incentivized_imitation_probability"],O)
    def test_punished_incentive(self):self.assertEqual(evaluate(O,O,O,F(1,2),"PUNISHED")["incentivized_imitation_probability"],O)
    def test_no_attention(self):self.assertEqual(evaluate(Z,O,O,O,"REWARDED")["incentivized_imitation_probability"],Z)
    def test_no_retention(self):self.assertEqual(evaluate(O,Z,O,O,"REWARDED")["incentivized_imitation_probability"],Z)
    def test_no_production(self):self.assertEqual(evaluate(O,O,Z,O,"REWARDED")["incentivized_imitation_probability"],Z)
    def test_no_motivation_then_incentive(self):self.assertEqual(evaluate(O,O,O,Z,"REWARDED")["incentivized_imitation_probability"],O)
    def test_invalid_phase(self):
        with self.assertRaises(ValueError):row(O,O,O,O,"REWARDED","LEARNING")
    def test_invalid_consequence(self):
        with self.assertRaises(ValueError):evaluate(O,O,O,O,"RANDOM")
    def test_invalid_gate(self):
        with self.assertRaises(ValueError):evaluate(F(1,3),O,O,O,"REWARDED")

def generated(condition,phase,kind):
    def f(self):
        source=row(*condition,phase);expected=evaluate(*condition)
        if kind=="acquire":self.assertEqual(source["latent_acquisition_probability"],expected["acquired_trace_probability"])
        elif kind=="response":self.assertEqual(source["imitative_response_probability"],expected["spontaneous_imitation_probability"] if phase=="SPONTANEOUS" else expected["incentivized_imitation_probability"])
        elif kind=="gap":self.assertEqual(source["incentive_minus_spontaneous_probability"],expected["incentive_performance_gap"])
        else:raise AssertionError(kind)
    return f
for i,w in enumerate(CONDITIONS):
    for phase in PHASES:
        for kind in ("acquire","response","gap"):
            setattr(Tests,f"test_world{i}_phase{phase.lower()}_{kind}",generated(w,phase,kind))
if __name__=="__main__":
    p=argparse.ArgumentParser();g=p.add_mutually_exclusive_group(required=True)
    g.add_argument("--test",action="store_true");g.add_argument("--emit",action="store_true")
    a=p.parse_args()
    if a.test:unittest.main(argv=["R303"],verbosity=1)
    else:print(json.dumps(emit(),indent=2))
