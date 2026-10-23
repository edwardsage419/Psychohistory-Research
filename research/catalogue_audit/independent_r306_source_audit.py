#!/usr/bin/env python3
"""Independent original R306 group polarization full 648 source proof, no import of model."""
from __future__ import annotations
import argparse,csv,hashlib,itertools,json,unittest
from collections import Counter
from fractions import Fraction as Q
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]/"research/R306"
CSV=ROOT/"R306_ALL_648_ORIGINAL_POLARIZATION_PERSON_SOURCES.csv"
RESULT=ROOT/"R306_EXACT_GROUP_POLARIZATION_RESULTS.json"
RECEIPT=ROOT/"R306_MACHINE_RECEIPT.json"
ZERO,ONE=Q(0),Q(1)
LEVELS=(Q(-1,2),ZERO,Q(1,2))
GROUPS=tuple(itertools.product(LEVELS,repeat=3))
WEIGHTS={"CONSENSUS_AVERAGING":(ZERO,ZERO),
  "SOCIAL_COMPARISON_ONLY":(Q(1,2),ZERO),
  "PERSUASIVE_ARGUMENT_ONLY":(ZERO,Q(1,2)),
  "COMBINED_SOCIAL_AND_ARGUMENT":(Q(1,2),Q(1,2))}
CONTEXTS=("SUPPORT_PRE_DISCUSSION_DIRECTION","COUNTER_PRE_DISCUSSION_DIRECTION")
WORLDS=list(itertools.product(GROUPS,tuple(WEIGHTS),CONTEXTS))
SOURCE_FIELDS=("full_original_pre_opinion_triplet","policy","argument_context","person_index",
  "person_pre_opinion","person_post_consensus_opinion","person_opinion_changed",
  "pre_group_mean","pre_group_direction","social_comparison_target","argument_target",
  "social_comparison_weight","persuasive_argument_weight","post_consensus_mean",
  "group_mean_signed_change","absolute_extremity_change","polarization_status",
  "strict_same_direction_polarization","direction_flipped")

def obj(path):return json.loads(path.read_text(encoding="utf-8"))
def load():
    with CSV.open(newline="",encoding="utf-8") as f:return list(csv.DictReader(f))
def name(group,policy,context):
    return "group="+",".join(str(v) for v in group)+"|policy="+policy+"|context="+context
def group_mean(group):return sum(group,ZERO)/3
def sign(x):return (x>ZERO)-(x<ZERO)
def independent(world):
    group,policy,context=world
    mean=group_mean(group)
    direction=sign(mean)
    best=max(group) if direction>0 else (min(group) if direction<0 else ZERO)
    argument=Q(direction) if context==CONTEXTS[0] else -Q(direction)
    alpha,beta=WEIGHTS[policy]
    # Equivalent but independently authored convex mixture vs main additive deltas.
    new=(ONE-alpha-beta)*mean + alpha*best + beta*argument
    if mean==ZERO:status="NO_INITIAL_DIRECTION"
    elif new==ZERO:status="AT_ZERO"
    elif mean*new<ZERO:status="DIRECTION_FLIP"
    elif abs(new)>abs(mean):status="POLARIZED"
    elif abs(new)<abs(mean):status="DEPOLARIZED"
    else:status="UNCHANGED"
    return {"pre_group_mean":mean,"pre_group_direction":direction,
       "social_comparison_target":best,"argument_target":argument,
       "social_comparison_weight":alpha,"persuasive_argument_weight":beta,
       "post_consensus_mean":new,"group_mean_signed_change":new-mean,
       "absolute_extremity_change":abs(new)-abs(mean),
       "polarization_status":status,
       "strict_same_direction_polarization":status=="POLARIZED",
       "direction_flipped":status=="DIRECTION_FLIP"}
def expected_source(world,i):
    group,policy,context=world
    g=independent(world)
    x={"full_original_pre_opinion_triplet":";".join(str(v) for v in group),
       "policy":policy,"argument_context":context,"person_index":i,
       "person_pre_opinion":group[i],
       "person_post_consensus_opinion":g["post_consensus_mean"],
       "person_opinion_changed":group[i]!=g["post_consensus_mean"],**g}
    return {key:str(x[key]) for key in SOURCE_FIELDS}

def verify(source_rows,result):
    if len(source_rows)!=648 or len(result["worlds"])!=216:
        raise AssertionError("full 648 original source rows required")
    if result["all_original_source_person_rows"]!=648 or result["synthetic_group_worlds"]!=216:
        raise AssertionError("wrong model universe")
    source_set={(w,i) for w in WORLDS for i in range(3)}
    seen={}
    for source in source_rows:
        try:
            group=tuple(Q(x) for x in source["full_original_pre_opinion_triplet"].split(";"))
            policy=source["policy"];context=source["argument_context"];i=int(source["person_index"])
        except (KeyError,ValueError,ZeroDivisionError) as e:raise AssertionError("malformed source") from e
        key=((group,policy,context),i)
        if key not in source_set or key in seen:raise AssertionError("duplicate or invalid source")
        if source["world"]!=name(group,policy,context):raise AssertionError("wrong original world")
        for k,v in expected_source(key[0],i).items():
            if source[k]!=v:raise AssertionError("independent exact source mismatch "+k)
        seen[key]=source
    if set(seen)!=source_set:raise AssertionError("missing person source")
    counts={p:{context:Counter() for context in CONTEXTS} for p in WEIGHTS}
    for ix,world in enumerate(WORLDS):
        group,policy,context=world
        calculated=independent(world)
        entry=result["worlds"][ix]
        if entry["world"]!=name(group,policy,context) or entry["policy"]!=policy or entry["argument_context"]!=context:
            raise AssertionError("result id/policy")
        if entry["pre_opinions"]!=[str(v) for v in group]:raise AssertionError("wrong pre-opinions")
        if entry["outcome"]!={key:str(val) for key,val in calculated.items()}:
            raise AssertionError("result outcome mismatch")
        if entry["three_original_person_sources"]!=[expected_source(world,i) for i in range(3)]:
            raise AssertionError("result individual sources mismatch")
        counts[policy][context][calculated["polarization_status"]]+=1
    statuses=("POLARIZED","DEPOLARIZED","DIRECTION_FLIP","UNCHANGED","AT_ZERO","NO_INITIAL_DIRECTION")
    expected_counts={p:{ctx:{s:counts[p][ctx][s] for s in statuses} for ctx in CONTEXTS} for p in WEIGHTS}
    if result["status_counts_by_policy_and_argument"]!=expected_counts:
        raise AssertionError("aggregate synthetic status count mismatch")
    expected_refs={"homogeneous_social_comparison_support":"1/2",
     "homogeneous_supportive_argument":"3/4","homogeneous_counterargument":"-1/4",
     "heterogeneous_social_comparison_support":"1/3",
     "heterogeneous_supportive_argument":"7/12",
     "heterogeneous_combined_support":"3/4",
     "heterogeneous_counterargument":"-5/12","all_neutral_stays_neutral":True}
    if result["frozen_reference"]!=expected_refs:raise AssertionError("frozen cases mismatch")
    for group in GROUPS:
        for context in CONTEXTS:
            if independent((group,"CONSENSUS_AVERAGING",context))["post_consensus_mean"]!=group_mean(group):
                raise AssertionError("averaging should preserve mean")
            opposite=tuple(-x for x in group)
            for policy in WEIGHTS:
                if independent((group,policy,context))["post_consensus_mean"]!=-independent((opposite,policy,context))["post_consensus_mean"]:
                    raise AssertionError("direction mirror")
    return {"all_original_person_source_rows":648,"synthetic_group_worlds":216,
      "independent_convex_combination_verification":"PASS",
      "averaging_no_group_mean_shift":"PASS",
      "argument_counterdirection_flip_protected":"PASS",
      "real_human_animal_E2":0,"historical_E3":0}

def audit():
    receipt,res=obj(RECEIPT),obj(RESULT)
    freeze="1db7fc7cc12cbf1bbec67e3df25c634d689c25b6"
    if receipt["freeze_commit"]!=freeze or res["freeze_commit"]!=freeze:
        raise AssertionError("unfrozen source")
    if res["research_id"]!="R306" or res["original_catalogue_id"]!="03-012":
        raise AssertionError("wrong research")
    if res["new_project_mathematics_not_original_Moscovici_Myers_fitted_equation"] is not True:
        raise AssertionError("false original author equation")
    if res["original_1969_or_1976_human_data_reproduced"] is not False:
        raise AssertionError("unwarranted E2")
    if any(res[k]!=0 for k in ("new_real_human_E2","new_real_animal_E2","new_historical_E3")):
        raise AssertionError("synthetic promoted to real")
    if receipt["original_source_rows"]!=648 or receipt["new_E2"]!=0 or receipt["new_E3"]!=0:
        raise AssertionError("receipt")
    if hashlib.sha256(CSV.read_bytes()).hexdigest()!=receipt["source_sha256"]:
        raise AssertionError("source SHA256")
    if hashlib.sha256(RESULT.read_bytes()).hexdigest()!=receipt["results_sha256"]:
        raise AssertionError("result SHA256")
    return {**verify(load(),res),"source_sha256":receipt["source_sha256"],
      "results_sha256":receipt["results_sha256"]}

class Tests(unittest.TestCase):
    def test_full(self):self.assertEqual(audit()["all_original_person_source_rows"],648)
    def test_worlds(self):self.assertEqual(len(WORLDS),216)
    def test_avg(self):self.assertEqual(independent(((ZERO,ZERO,Q(1,2)),"CONSENSUS_AVERAGING",CONTEXTS[0]))["post_consensus_mean"],Q(1,6))
    def test_homogeneous_social(self):self.assertEqual(independent(((Q(1,2),)*3,"SOCIAL_COMPARISON_ONLY",CONTEXTS[0]))["post_consensus_mean"],Q(1,2))
    def test_support(self):self.assertEqual(independent(((Q(1,2),)*3,"PERSUASIVE_ARGUMENT_ONLY",CONTEXTS[0]))["post_consensus_mean"],Q(3,4))
    def test_counter(self):self.assertEqual(independent(((Q(1,2),)*3,"PERSUASIVE_ARGUMENT_ONLY",CONTEXTS[1]))["post_consensus_mean"],Q(-1,4))
    def test_social_hetero(self):self.assertEqual(independent(((ZERO,ZERO,Q(1,2)),"SOCIAL_COMPARISON_ONLY",CONTEXTS[0]))["post_consensus_mean"],Q(1,3))
    def test_combined(self):self.assertEqual(independent(((ZERO,ZERO,Q(1,2)),"COMBINED_SOCIAL_AND_ARGUMENT",CONTEXTS[0]))["post_consensus_mean"],Q(3,4))
    def test_no_initial_direction(self):self.assertEqual(independent(((ZERO,)*3,"PERSUASIVE_ARGUMENT_ONLY",CONTEXTS[0]))["polarization_status"],"NO_INITIAL_DIRECTION")
    def test_missing(self):
        with self.assertRaises(AssertionError):verify(load()[:-1],obj(RESULT))
    def test_duplicate(self):
        rows=load();rows[1]=dict(rows[0])
        with self.assertRaises(AssertionError):verify(rows,obj(RESULT))
    def test_wrong_mean(self):
        rows=load();rows[1]=dict(rows[1]);rows[1]["post_consensus_mean"]="7"
        with self.assertRaises(AssertionError):verify(rows,obj(RESULT))
    def test_wrong_status(self):
        rows=load();rows[1]=dict(rows[1]);rows[1]["polarization_status"]="POLARIZED"
        with self.assertRaises(AssertionError):verify(rows,obj(RESULT))
    def test_wrong_person(self):
        rows=load();rows[1]=dict(rows[1]);rows[1]["person_pre_opinion"]="9"
        with self.assertRaises(AssertionError):verify(rows,obj(RESULT))
    def test_result_tamper(self):
        j=obj(RESULT);j["worlds"][0]["outcome"]["post_consensus_mean"]="9"
        with self.assertRaises(AssertionError):verify(load(),j)
    def test_count_tamper(self):
        j=obj(RESULT);j["status_counts_by_policy_and_argument"]["CONSENSUS_AVERAGING"][CONTEXTS[0]]["POLARIZED"]=100
        with self.assertRaises(AssertionError):verify(load(),j)
    def test_sha_tamper(self):self.assertNotEqual(hashlib.sha256(CSV.read_bytes()+b"x").hexdigest(),obj(RECEIPT)["source_sha256"])
if __name__=="__main__":
    p=argparse.ArgumentParser()
    g=p.add_mutually_exclusive_group(required=True)
    g.add_argument("--test",action="store_true");g.add_argument("--audit",action="store_true")
    a=p.parse_args()
    if a.test:unittest.main(argv=["R306 independent"],verbosity=1)
    else:print(json.dumps(audit(),ensure_ascii=False,indent=2))
