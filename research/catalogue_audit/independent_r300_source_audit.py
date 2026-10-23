#!/usr/bin/env python3
"""Independent exhaustive HMM hidden-path enumerator for 128 original prefixes; no model import."""
from __future__ import annotations
import argparse,csv,hashlib,itertools,json,unittest
from fractions import Fraction as Q
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]/"research/R300"
SOURCE=ROOT/"R300_ALL_128_ORIGINAL_HMM_PREFIX_SOURCES.csv"
RESULT=ROOT/"R300_EXACT_HMM_FORWARD_RESULTS.json"
RECEIPT=ROOT/"R300_MACHINE_RECEIPT.json"
MODELS={"PERSISTENT_HMM":Q(3,4),"IID_HIDDEN_NEGATIVE_CONTROL":Q(1,2)}
OBSERVATIONS=tuple("".join(bits) for bits in itertools.product("01",repeat=4))
LENGTHS=(1,2,3,4)
Z,O=Q(0),Q(1)
ACC=Q(3,4)
NUMERICS=("alpha_hidden_0","alpha_hidden_1","prefix_evidence",
      "posterior_hidden_1","predictive_next_hidden_1","predictive_next_observed_1")
FIELDS=("full_observation_bits","prefix_bits","prefix_length")+NUMERICS

def obj(path):return json.loads(path.read_text(encoding="utf-8"))
def load():
    with SOURCE.open(newline="",encoding="utf-8") as f:return list(csv.DictReader(f))
def emission(h,y):return ACC if h==y else O-ACC

def brute_prefix(world,prefix):
    if world not in MODELS or not prefix or any(b not in "01" for b in prefix) or len(prefix)>4:
        raise AssertionError("unknown source")
    stay=MODELS[world]
    n=len(prefix)
    counts=[Z,Z]
    for hidden in itertools.product((0,1),repeat=n):
        prob=Q(1,2)
        for t,y in enumerate(prefix):
            if t:prob*=stay if hidden[t]==hidden[t-1] else O-stay
            prob*=emission(hidden[t],int(y))
        counts[hidden[-1]]+=prob
    evidence=sum(counts,Z)
    posterior=counts[1]/evidence
    # Independent full-joint extension: sum over n+1 hidden paths,
    # weight the first n observed bits and either next latent state or Y_next=1.
    next_hidden_mass=Z
    next_observed1_mass=Z
    for hidden in itertools.product((0,1),repeat=n+1):
        prob=Q(1,2)
        for t,h in enumerate(hidden):
            if t:
                prob*=stay if h==hidden[t-1] else O-stay
            if t<n:
                prob*=emission(h,int(prefix[t]))
        if hidden[-1]==1:next_hidden_mass+=prob
        next_observed1_mass+=prob*emission(hidden[-1],1)
    return {"alpha_hidden_0":counts[0],"alpha_hidden_1":counts[1],
      "prefix_evidence":evidence,"posterior_hidden_1":posterior,
      "predictive_next_hidden_1":next_hidden_mass/evidence,
      "predictive_next_observed_1":next_observed1_mass/evidence}

def verify(original,result):
    if len(original)!=128 or result["complete_original_source_rows"]!=128:
        raise AssertionError("128 original sources required")
    if result["artificial_worlds"]!=2 or len(result["worlds"])!=2:
        raise AssertionError("two exact worlds required")
    known=set((w,obs,t) for w in MODELS for obs in OBSERVATIONS for t in LENGTHS)
    seen={}
    for row in original:
        try:
            world=row["world"];ob=row["full_observation_bits"];t=int(row["prefix_length"])
        except (KeyError,ValueError) as err:raise AssertionError("invalid source row") from err
        key=(world,ob,t)
        if key not in known or key in seen:raise AssertionError("missing/duplicate invalid cell")
        if row["prefix_bits"]!=ob[:t]:raise AssertionError("source prefix mismatch")
        if Q(row["stay_probability"])!=MODELS[world] or Q(row["emission_match_probability"])!=ACC:
            raise AssertionError("changed emission/transition model")
        exact=brute_prefix(world,ob[:t])
        for field in NUMERICS:
            if Q(row[field])!=exact[field]:raise AssertionError("independent hidden-path source "+field)
        seen[key]=exact
    if set(seen)!=known:raise AssertionError("uncovered original sources")
    for ix,world in enumerate(MODELS):
        record=result["worlds"][ix]
        if record["world"]!=world or record["stay_probability"]!=str(MODELS[world]):
            raise AssertionError("result world label")
        if record["source_rows"]!=64 or record["full_sequence_count"]!=16:
            raise AssertionError("stored world original source count")
        if len(record["complete_source_records"])!=64:
            raise AssertionError("incomplete stored result rows")
        expected=[]
        for obs in OBSERVATIONS:
            for t in LENGTHS:
                r={"full_observation_bits":obs,"prefix_bits":obs[:t],"prefix_length":str(t)}
                r.update({field:str(seen[(world,obs,t)][field]) for field in NUMERICS})
                expected.append(r)
        if record["complete_source_records"]!=expected:
            raise AssertionError("result JSON original rows differ from enumerated source")
        for t in LENGTHS:
            prefixes=("".join(bit) for bit in itertools.product("01",repeat=t))
            if sum((brute_prefix(world,p)["prefix_evidence"] for p in prefixes),Z)!=O:
                raise AssertionError("marginal evidence not normalized")
            if record["evidence_sum_each_prefix_length"][str(t)]!="1":
                raise AssertionError("result normalization metadata tamper")
    a=brute_prefix("PERSISTENT_HMM","1110")
    b=brute_prefix("PERSISTENT_HMM","0000")
    if a["posterior_hidden_1"]==b["posterior_hidden_1"]:
        raise AssertionError("persistence history contrast absent")
    if a["predictive_next_observed_1"]==b["predictive_next_observed_1"]:
        raise AssertionError("persistence prediction contrast absent")
    if brute_prefix("IID_HIDDEN_NEGATIVE_CONTROL","1110")["posterior_hidden_1"]!=Q(1,4):
        raise AssertionError("IID not last-symbol-only")
    x=result["history_effect_demo"]
    correct={"persistent_1110_posterior_hidden1":str(a["posterior_hidden_1"]),
      "persistent_0000_posterior_hidden1":str(b["posterior_hidden_1"]),
      "persistent_1110_next_obs1":str(a["predictive_next_observed_1"]),
      "persistent_0000_next_obs1":str(b["predictive_next_observed_1"]),
      "iid_same_last_obs_posterior_hidden1":"1/4","iid_next_observation1":"1/2"}
    if x!=correct:raise AssertionError("summary ungrounded")
    return {"research":"R300","original_labeled_source_rows":128,
      "unique_observation_sequences_each_world":16,
      "complete_hidden_path_enumeration_audit":"PASS",
      "i_i_d_no_memory_negative_control":"PASS",
      "persistent_hidden_history_effect":"PASS","new_real_E2":0,"new_historical_E3":0}

def audit():
    r,j=obj(RECEIPT),obj(RESULT)
    freeze="ef56b01c3c2b5da98e433f9d2fefdd61fd9028c3"
    if r["freeze_commit"]!=freeze or j["freeze_commit"]!=freeze:
        raise AssertionError("no prescore protocol")
    if j["original_catalogue_id"]!="02-008" or r["source_rows"]!=128:
        raise AssertionError("wrong original candidate or source count")
    if any(j[k]!=0 for k in ("real_human_E2_added","real_animal_E2_added","historical_E3_added")):
        raise AssertionError("false E2/E3")
    if r["new_real_E2"]!=0 or r["new_historical_E3"]!=0:
        raise AssertionError("bad receipt")
    if j["parameters_learned_from_empirical_data"] is not False or j["viterbi_path_decoding_performed"] is not False:
        raise AssertionError("unwarranted algorithm scope")
    if r["source_sha256"]!=hashlib.sha256(SOURCE.read_bytes()).hexdigest():
        raise AssertionError("original CSV SHA")
    if r["results_sha256"]!=hashlib.sha256(RESULT.read_bytes()).hexdigest():
        raise AssertionError("result JSON SHA")
    return {**verify(load(),j),"source_sha256":r["source_sha256"],"results_sha256":r["results_sha256"]}

class Tests(unittest.TestCase):
    def test_all(self):self.assertEqual(audit()["original_labeled_source_rows"],128)
    def test_worlds(self):self.assertEqual(len(MODELS),2)
    def test_independent_first_posterior(self):self.assertEqual(brute_prefix("PERSISTENT_HMM","1")["posterior_hidden_1"],Q(3,4))
    def test_iid_next(self):self.assertEqual(brute_prefix("IID_HIDDEN_NEGATIVE_CONTROL","1110")["predictive_next_observed_1"],Q(1,2))
    def test_IID_evidence(self):self.assertEqual(brute_prefix("IID_HIDDEN_NEGATIVE_CONTROL","1110")["prefix_evidence"],Q(1,16))
    def test_persistent_effect(self):self.assertNotEqual(brute_prefix("PERSISTENT_HMM","1110")["posterior_hidden_1"],brute_prefix("PERSISTENT_HMM","0000")["posterior_hidden_1"])
    def test_drop_row(self):
        with self.assertRaises(AssertionError):verify(load()[:-1],obj(RESULT))
    def test_duplicate_row(self):
        d=load();d[1]=dict(d[0])
        with self.assertRaises(AssertionError):verify(d,obj(RESULT))
    def test_wrong_transition(self):
        d=load();d[1]=dict(d[1]);d[1]["stay_probability"]="1/5"
        with self.assertRaises(AssertionError):verify(d,obj(RESULT))
    def test_wrong_emission(self):
        d=load();d[1]=dict(d[1]);d[1]["emission_match_probability"]="1/2"
        with self.assertRaises(AssertionError):verify(d,obj(RESULT))
    def test_wrong_posterior(self):
        d=load();d[1]=dict(d[1]);d[1]["posterior_hidden_1"]="99"
        with self.assertRaises(AssertionError):verify(d,obj(RESULT))
    def test_wrong_predictive(self):
        d=load();d[1]=dict(d[1]);d[1]["predictive_next_observed_1"]="88"
        with self.assertRaises(AssertionError):verify(d,obj(RESULT))
    def test_bad_prefix(self):
        d=load();d[1]=dict(d[1]);d[1]["prefix_bits"]="001101"
        with self.assertRaises(AssertionError):verify(d,obj(RESULT))
    def test_result_tamper(self):
        x=obj(RESULT);x["worlds"][0]["complete_source_records"][0]["prefix_evidence"]="9"
        with self.assertRaises(AssertionError):verify(load(),x)
    def test_negative_control_wrong_result(self):
        x=obj(RESULT);x["history_effect_demo"]["iid_same_last_obs_posterior_hidden1"]="3/4"
        with self.assertRaises(AssertionError):verify(load(),x)
    def test_digest_tamper(self):self.assertNotEqual(hashlib.sha256(SOURCE.read_bytes()+b"changed").hexdigest(),obj(RECEIPT)["source_sha256"])

if __name__=="__main__":
    p=argparse.ArgumentParser()
    g=p.add_mutually_exclusive_group(required=True)
    g.add_argument("--test",action="store_true")
    g.add_argument("--audit",action="store_true")
    args=p.parse_args()
    if args.test:unittest.main(argv=["R300 hidden-path"],verbosity=1)
    else:print(json.dumps(audit(),indent=2))
