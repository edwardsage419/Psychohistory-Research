#!/usr/bin/env python3
"""R301 independent complete segmentation enumeration; never imports main BOCPD source."""
from __future__ import annotations
import argparse,csv,hashlib,itertools,json,unittest
from collections import defaultdict
from fractions import Fraction as Q
from math import factorial
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]/"research/R301"
SOURCE=ROOT/"R301_ALL_192_ORIGINAL_BAYESIAN_CHANGEPOINT_PREFIX_SOURCES.csv"
RESULT=ROOT/"R301_EXACT_CHANGEPOINT_RUN_LENGTH_RESULTS.json"
RECEIPT=ROOT/"R301_MACHINE_RECEIPT.json"
Z,O=Q(0),Q(1)
HAZARDS=(Z,Q(1,4),Q(1,2))
STRINGS=("".join(b) for b in itertools.product("01",repeat=4))
TIMES=(1,2,3,4)
WORLDS=list(itertools.product(HAZARDS,STRINGS))
FIELDS=("prefix_length","observed_prefix","joint_run_length_weights","posterior_run_length",
        "prefix_evidence","current_last_boundary_change_posterior","predictive_next_observed_one")

def obj(path):return json.loads(path.read_text(encoding="utf-8"))
def load():
    with SOURCE.open(newline="",encoding="utf-8") as f:return list(csv.DictReader(f))
def beta_integral(seg):
    n=len(seg); k=seg.count("1")
    return Q(factorial(k)*factorial(n-k),factorial(n+1))
def partitions(prefix,hazard):
    t=len(prefix)
    for change_bits in itertools.product((0,1),repeat=t-1):
        starts=[0]+[i+1 for i,v in enumerate(change_bits) if v]
        bounds=starts+[t]
        prior=hazard**sum(change_bits)*(O-hazard)**(t-1-sum(change_bits))
        joint=prior
        for a,b in zip(bounds[:-1],bounds[1:]):
            joint*=beta_integral(prefix[a:b])
        yield t-starts[-1],joint
def enumerate_evidence(hazard,prefix):
    if hazard not in HAZARDS or not prefix or len(prefix)>4 or any(x not in "01" for x in prefix):
        raise AssertionError("illegal source")
    t=len(prefix)
    weights={i:Z for i in range(1,t+1)}
    for length,prob in partitions(prefix,hazard):
        weights[length]+=prob
    total=sum(weights.values(),Z)
    posterior={i:w/total for i,w in weights.items()}
    # Independently enumerate next-bit1 probability using complete t+1 partition
    # and the marginal likelihood of the observed prefix followed by 1.
    joint_next1=sum((mass for _,mass in partitions(prefix+"1",hazard)),Z)
    pred1=joint_next1/total
    return {"joint":weights,"posterior":posterior,"evidence":total,
        "recent_change":posterior[1] if t>1 else Z,
        "next1":pred1}
def fmt(values):return ";".join(f"{key}:{values[key]}" for key in sorted(values))
def original_world(h,full):return f"hazard={h}|observations={full}"

def verify(rows,result):
    if len(rows)!=192 or result["original_full_source_rows"]!=192 or result["synthetic_worlds"]!=48:
        raise AssertionError("all 192 frozen sources required")
    if len(result["worlds"])!=48 or result["four_bit_original_observation_strings"]!=16 or result["prefix_lengths_each"]!=4:
        raise AssertionError("worlds incomplete")
    expected=set((h,s,t) for h,s in WORLDS for t in TIMES)
    read={}
    for source in rows:
        try:
            h=Q(source["hazard"]);full=source["original_four_bit_observations"];t=int(source["prefix_length"])
        except (ValueError,KeyError,ZeroDivisionError) as e:raise AssertionError("source dimensions") from e
        k=(h,full,t)
        if k not in expected or k in read:raise AssertionError("missing/duplicate/unfrozen source")
        if source["world"]!=original_world(h,full) or source["observed_prefix"]!=full[:t]:
            raise AssertionError("source prefix provenance changed")
        v=enumerate_evidence(h,full[:t])
        candidates={"joint_run_length_weights":fmt(v["joint"]),
             "posterior_run_length":fmt(v["posterior"])}
        for field,string in candidates.items():
            if source[field]!=string:raise AssertionError("run length vector differs "+field)
        for field,truth in (("prefix_evidence",v["evidence"]),
          ("current_last_boundary_change_posterior",v["recent_change"]),
          ("predictive_next_observed_one",v["next1"])):
            if Q(source[field])!=truth:raise AssertionError("source exact posterior mismatches "+field)
        read[k]=source
    if set(read)!=expected:raise AssertionError("uncovered original sources")
    for ix,(h,s) in enumerate(WORLDS):
        world=result["worlds"][ix]
        if world["world"]!=original_world(h,s) or world["hazard"]!=str(h) or world["full_observation_bits"]!=s:
            raise AssertionError("result world identification mismatch")
        if world["source_rows"]!=4 or len(world["epoch_records"])!=4:raise AssertionError("missing result epoch")
        for t in TIMES:
            x=read[h,s,t]
            compare={f:str(x[f]) for f in FIELDS}
            if world["epoch_records"][t-1]!=compare:
                raise AssertionError("result JSON values mismatch original source")
    for h in HAZARDS:
        for t in TIMES:
            unique=("".join(bits) for bits in itertools.product("01",repeat=t))
            evidence_sum=sum((enumerate_evidence(h,p)["evidence"] for p in unique),Z)
            if evidence_sum!=O:raise AssertionError("unique-prefix normalization broken")
    cases={
       "h_quarter_0000_evidence":"757/5120",
       "h_quarter_0000_last_change":"135/757",
       "h_quarter_0000_predict_one":"1717/6056",
       "h_quarter_0001_evidence":"323/5120",
       "h_quarter_0001_last_change":"135/323",
       "h_quarter_0001_predict_one":"1301/2584",
       "h_zero_0000_predict_one":"1/6",
       "h_zero_0001_predict_one":"1/3",
       "h_half_0001_last_change":"15/23"}
    if result["reference_cases"]!=cases:raise AssertionError("prescore special cases changed")
    if enumerate_evidence(Q(1,4),"0001")["recent_change"]<=enumerate_evidence(Q(1,4),"0000")["recent_change"]:
        raise AssertionError("frozen contrast wrong")
    if enumerate_evidence(Z,"0001")["recent_change"]!=Z:
        raise AssertionError("no-change negative control violated")
    return {"original_full_artificial_sources":192,"finite_artificial_worlds":48,
        "all_possible_segmentations_enumerated":"PASS",
        "all_unique_prefix_likelihoods_normalized":"PASS",
        "no_change_negative_control":"PASS","no_single_observation_proves_change":"PASS",
        "new_human_animal_E2":0,"historical_E3":0}

def audit():
    r,result=obj(RECEIPT),obj(RESULT)
    freeze="1e0209ffa2c8597d3d3f2a7ccef40eea0be4485e"
    if r["freeze_commit"]!=freeze or result["freeze_commit"]!=freeze:raise AssertionError("wrong frozen protocol")
    if result["original_catalogue_id"]!="02-012" or result["research_id"]!="R301":
        raise AssertionError("wrong original candidate")
    if any(result[k]!=0 for k in ("new_real_human_E2","new_real_animal_E2","new_historical_E3")):
        raise AssertionError("artificial task spuriously E2/E3")
    if result["Bayesian_hazard_estimated_from_data"] is not False or result["empirical_detection_false_positive_calibration"] is not False:
        raise AssertionError("spurious hazard-fit/calibration claim")
    if r["original_source_rows"]!=192 or r["new_E2"]!=0 or r["new_E3"]!=0:
        raise AssertionError("invalid SHA receipt")
    if r["source_sha256"]!=hashlib.sha256(SOURCE.read_bytes()).hexdigest():
        raise AssertionError("source SHA256")
    if r["results_sha256"]!=hashlib.sha256(RESULT.read_bytes()).hexdigest():
        raise AssertionError("result SHA256")
    return {**verify(load(),result),"source_sha256":r["source_sha256"],
         "results_sha256":r["results_sha256"]}

class Tests(unittest.TestCase):
    def test_all(self):self.assertEqual(audit()["original_full_artificial_sources"],192)
    def test_worlds(self):self.assertEqual(len(WORLDS),48)
    def test_no_change(self):self.assertEqual(enumerate_evidence(Z,"0001")["recent_change"],Z)
    def test_rare(self):self.assertEqual(enumerate_evidence(Q(1,4),"0001")["recent_change"],Q(135,323))
    def test_half_hazard(self):self.assertEqual(enumerate_evidence(Q(1,2),"0001")["recent_change"],Q(15,23))
    def test_predictive(self):self.assertEqual(enumerate_evidence(Q(1,4),"0001")["next1"],Q(1301,2584))
    def test_source_deleted(self):
        with self.assertRaises(AssertionError):verify(load()[:-1],obj(RESULT))
    def test_duplicate(self):
        rows=load();rows[1]=dict(rows[0])
        with self.assertRaises(AssertionError):verify(rows,obj(RESULT))
    def test_bad_hazard(self):
        rows=load();rows[1]=dict(rows[1]);rows[1]["hazard"]="1/3"
        with self.assertRaises(AssertionError):verify(rows,obj(RESULT))
    def test_wrong_run_length(self):
        rows=load();rows[1]=dict(rows[1]);rows[1]["joint_run_length_weights"]="1:1"
        with self.assertRaises(AssertionError):verify(rows,obj(RESULT))
    def test_wrong_predictive(self):
        rows=load();rows[1]=dict(rows[1]);rows[1]["predictive_next_observed_one"]="9"
        with self.assertRaises(AssertionError):verify(rows,obj(RESULT))
    def test_wrong_prefix(self):
        rows=load();rows[1]=dict(rows[1]);rows[1]["observed_prefix"]="0111"
        with self.assertRaises(AssertionError):verify(rows,obj(RESULT))
    def test_wrong_result(self):
        result=obj(RESULT);result["worlds"][0]["epoch_records"][0]["prefix_evidence"]="100"
        with self.assertRaises(AssertionError):verify(load(),result)
    def test_wrong_reference(self):
        result=obj(RESULT);result["reference_cases"]["h_quarter_0001_last_change"]="1"
        with self.assertRaises(AssertionError):verify(load(),result)
    def test_sha_tamper(self):
        self.assertNotEqual(hashlib.sha256(SOURCE.read_bytes()+b"x").hexdigest(),obj(RECEIPT)["source_sha256"])
    def test_not_real(self):self.assertEqual(audit()["new_human_animal_E2"],0)

if __name__=="__main__":
    p=argparse.ArgumentParser()
    g=p.add_mutually_exclusive_group(required=True)
    g.add_argument("--test",action="store_true");g.add_argument("--audit",action="store_true")
    a=p.parse_args()
    if a.test:unittest.main(argv=["R301 segmentation"],verbosity=1)
    else:print(json.dumps(audit(),ensure_ascii=False,indent=2))
