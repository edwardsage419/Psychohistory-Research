#!/usr/bin/env python3
"""R301 exact BOCPD Beta(1,1)-Bernoulli, 192 complete artificial prefix sources."""
from __future__ import annotations
import argparse,csv,hashlib,itertools,json,unittest
from fractions import Fraction as F
from functools import lru_cache
from pathlib import Path

ROOT=Path(__file__).resolve().parent
FREEZE="1e0209ffa2c8597d3d3f2a7ccef40eea0be4485e"
Z,O=F(0),F(1)
HAZARDS=(Z,F(1,4),F(1,2))
STRINGS=tuple("".join(bits) for bits in itertools.product("01",repeat=4))
TIMES=(1,2,3,4)
WORLDS=tuple(itertools.product(HAZARDS,STRINGS))
SOURCE_NAME="R301_ALL_192_ORIGINAL_BAYESIAN_CHANGEPOINT_PREFIX_SOURCES.csv"
RESULT_NAME="R301_EXACT_CHANGEPOINT_RUN_LENGTH_RESULTS.json"
RECEIPT_NAME="R301_MACHINE_RECEIPT.json"

def beta_predict(segment,y):
    if not segment or any(k not in "01" for k in segment) or y not in "01":
        raise ValueError("unfrozen segment observation")
    ones=segment.count("1")
    p1=F(ones+1,len(segment)+2)
    return p1 if y=="1" else O-p1

@lru_cache(maxsize=260)
def filter_prefix(hazard,prefix):
    if hazard not in HAZARDS or not prefix or len(prefix)>4 or any(y not in "01" for y in prefix):
        raise ValueError("unfrozen BOCPD input")
    weights={1:F(1,2)}
    for t in range(2,len(prefix)+1):
        observation=prefix[t-1]
        next_weights={}
        change=sum(weights.values(),Z)*hazard*F(1,2)
        next_weights[1]=change
        for length,mass in weights.items():
            segment=prefix[t-1-length:t-1]
            next_weights[length+1]=(O-hazard)*mass*beta_predict(segment,observation)
        weights=next_weights
    evidence=sum(weights.values(),Z)
    if evidence<=0:raise AssertionError("zero likelihood")
    posterior={l:mass/evidence for l,mass in weights.items()}
    next_p1=hazard*F(1,2)+(O-hazard)*sum(
        (prob*F(prefix[-length:].count("1")+1,length+2) for length,prob in posterior.items()),Z)
    return {"run_length_joint":weights,"run_length_posterior":posterior,
        "prefix_evidence":evidence,
        "last_boundary_change_posterior":posterior.get(1,Z) if len(prefix)>1 else Z,
        "next_observation_one_predictive":next_p1}

def row(hazard,full,t):
    if hazard not in HAZARDS or full not in STRINGS or t not in TIMES:raise ValueError("unfrozen original source")
    prefix=full[:t]
    f=filter_prefix(hazard,prefix)
    return {"world":f"hazard={hazard}|observations={full}","hazard":hazard,
        "original_four_bit_observations":full,"prefix_length":t,"observed_prefix":prefix,
        "joint_run_length_weights":";".join(f"{l}:{f['run_length_joint'][l]}" for l in range(1,t+1)),
        "posterior_run_length":";".join(f"{l}:{f['run_length_posterior'][l]}" for l in range(1,t+1)),
        "prefix_evidence":f["prefix_evidence"],
        "current_last_boundary_change_posterior":f["last_boundary_change_posterior"],
        "predictive_next_observed_one":f["next_observation_one_predictive"]}

def sources():return tuple(row(h,seq,t) for h,seq in WORLDS for t in TIMES)

def validate():
    assert len(WORLDS)==48 and len(sources())==192
    assert len(set((x["world"],x["prefix_length"]) for x in sources()))==192
    for h in HAZARDS:
        for t in TIMES:
            prefixes=("".join(b) for b in itertools.product("01",repeat=t))
            assert sum((filter_prefix(h,p)["prefix_evidence"] for p in prefixes),Z)==O
            for p in ("".join(b) for b in itertools.product("01",repeat=t)):
                res=filter_prefix(h,p)
                assert set(res["run_length_joint"])==set(range(1,t+1))
                assert sum(res["run_length_joint"].values(),Z)==res["prefix_evidence"]
                assert sum(res["run_length_posterior"].values(),Z)==O
                assert all(Z<=v<=O for v in res["run_length_posterior"].values())
                assert Z<=res["next_observation_one_predictive"]<=O
                if h==Z:
                    assert res["run_length_posterior"][t]==O
                    assert res["last_boundary_change_posterior"]==Z
                    assert res["next_observation_one_predictive"]==F(p.count("1")+1,t+2)
                if t==1:
                    assert res["prefix_evidence"]==F(1,2)
                    assert res["last_boundary_change_posterior"]==Z
    for seq,evidence,last,predict in (
         ("0000",F(757,5120),F(135,757),F(1717,6056)),
         ("0001",F(323,5120),F(135,323),F(1301,2584))):
        s=filter_prefix(F(1,4),seq)
        assert (s["prefix_evidence"],s["last_boundary_change_posterior"],s["next_observation_one_predictive"])==(evidence,last,predict)
    assert filter_prefix(F(1,2),"0001")["last_boundary_change_posterior"]==F(15,23)
    assert filter_prefix(Z,"0000")["next_observation_one_predictive"]==F(1,6)
    assert filter_prefix(Z,"0001")["next_observation_one_predictive"]==F(1,3)
    return True

def emit():
    validate()
    cols=("world","hazard","original_four_bit_observations","prefix_length","observed_prefix",
          "joint_run_length_weights","posterior_run_length","prefix_evidence",
          "current_last_boundary_change_posterior","predictive_next_observed_one")
    p=ROOT/SOURCE_NAME
    with p.open("w",encoding="utf-8",newline="") as f:
        w=csv.DictWriter(f,fieldnames=cols,lineterminator="\n")
        w.writeheader()
        for s in sources():w.writerow({k:str(s[k]) for k in cols})
    result={"research_id":"R301","original_catalogue_id":"02-012","freeze_commit":FREEZE,
        "scope":"E1_EXACT_ARTIFICIAL_BERNOULLI_BETA_ONLINE_CHANGEPOINT_RUN_LENGTH_NOT_REAL_DETECTION",
        "original_full_source_rows":192,"synthetic_worlds":48,"hazards":[str(x) for x in HAZARDS],
        "four_bit_original_observation_strings":16,"prefix_lengths_each":4,
        "new_real_human_E2":0,"new_real_animal_E2":0,"new_historical_E3":0,
        "Bayesian_hazard_estimated_from_data":False,
        "empirical_detection_false_positive_calibration":False,
        "R073":"FROZEN","PESEN_v0_1":"FROZEN","worlds":[]}
    for h,seq in WORLDS:
        rs=[row(h,seq,t) for t in TIMES]
        result["worlds"].append({"world":rs[0]["world"],"hazard":str(h),
            "full_observation_bits":seq,"source_rows":4,
            "epoch_records":[{key:str(s[key]) for key in cols if key not in
                ("world","hazard","original_four_bit_observations")} for s in rs]})
    result["reference_cases"]={
       "h_quarter_0000_evidence":"757/5120",
       "h_quarter_0000_last_change":"135/757",
       "h_quarter_0000_predict_one":"1717/6056",
       "h_quarter_0001_evidence":"323/5120",
       "h_quarter_0001_last_change":"135/323",
       "h_quarter_0001_predict_one":"1301/2584",
       "h_zero_0000_predict_one":"1/6",
       "h_zero_0001_predict_one":"1/3",
       "h_half_0001_last_change":"15/23"}
    rp=ROOT/RESULT_NAME
    rp.write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    rec={"research_id":"R301","freeze_commit":FREEZE,"original_source_rows":192,
         "source_sha256":hashlib.sha256(p.read_bytes()).hexdigest(),
         "results_sha256":hashlib.sha256(rp.read_bytes()).hexdigest(),
         "new_E2":0,"new_E3":0}
    (ROOT/RECEIPT_NAME).write_text(json.dumps(rec,indent=2)+"\n",encoding="utf-8")
    return rec

class Tests(unittest.TestCase):
    def test_all(self):self.assertTrue(validate())
    def test_count(self):self.assertEqual(len(sources()),192)
    def test_worlds(self):self.assertEqual(len(WORLDS),48)
    def test_hazard_zero(self):self.assertEqual(filter_prefix(Z,"0001")["last_boundary_change_posterior"],Z)
    def test_hazard_quarter(self):self.assertEqual(filter_prefix(F(1,4),"0001")["last_boundary_change_posterior"],F(135,323))
    def test_hazard_half(self):self.assertEqual(filter_prefix(F(1,2),"0001")["last_boundary_change_posterior"],F(15,23))
    def test_change_not_certain(self):self.assertLess(filter_prefix(F(1,4),"0001")["last_boundary_change_posterior"],O)
    def test_negative_control_no_change_predict(self):self.assertEqual(filter_prefix(Z,"0000")["next_observation_one_predictive"],F(1,6))
    def test_new_sample_not_proof(self):self.assertGreater(filter_prefix(F(1,4),"0001")["last_boundary_change_posterior"],filter_prefix(F(1,4),"0000")["last_boundary_change_posterior"])
    def test_reject_hazard(self):
        with self.assertRaises(ValueError):filter_prefix(F(1,3),"0001")
    def test_reject_obs(self):
        with self.assertRaises(ValueError):filter_prefix(Z,"0002")
    def test_reject_length(self):
        with self.assertRaises(ValueError):row(Z,"0000",5)

def build_case(h,seq,t,kind):
    def check(self):
        src=row(h,seq,t)
        f=filter_prefix(h,seq[:t])
        if kind=="evidence":self.assertEqual(src["prefix_evidence"],f["prefix_evidence"])
        elif kind=="posterior":self.assertEqual(sum(f["run_length_posterior"].values(),Z),O)
        elif kind=="mass":self.assertEqual(sum(f["run_length_joint"].values(),Z),f["prefix_evidence"])
        else:raise AssertionError(kind)
    return check
for i,(h,seq) in enumerate(WORLDS):
    for t in TIMES:
        for kind in ("evidence","posterior","mass"):
            setattr(Tests,f"test_world{i}_t{t}_{kind}",build_case(h,seq,t,kind))
if __name__=="__main__":
    p=argparse.ArgumentParser()
    m=p.add_mutually_exclusive_group(required=True)
    m.add_argument("--test",action="store_true")
    m.add_argument("--emit",action="store_true")
    args=p.parse_args()
    if args.test:unittest.main(argv=["R301"],verbosity=1)
    else:print(json.dumps(emit(),indent=2))
