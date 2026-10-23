#!/usr/bin/env python3
"""R306 synthetic group discussion mean shift vs social comparison and arguments: project toy E1."""
from __future__ import annotations
import argparse,csv,hashlib,itertools,json,unittest
from fractions import Fraction as F
from pathlib import Path

ROOT=Path(__file__).resolve().parent
FREEZE="1db7fc7cc12cbf1bbec67e3df25c634d689c25b6"
ZERO,ONE=F(0),F(1)
OPINION_LEVELS=(F(-1,2),ZERO,F(1,2))
GROUPS=tuple(itertools.product(OPINION_LEVELS,repeat=3))
POLICIES={"CONSENSUS_AVERAGING":(ZERO,ZERO),
  "SOCIAL_COMPARISON_ONLY":(F(1,2),ZERO),
  "PERSUASIVE_ARGUMENT_ONLY":(ZERO,F(1,2)),
  "COMBINED_SOCIAL_AND_ARGUMENT":(F(1,2),F(1,2))}
CONTEXTS=("SUPPORT_PRE_DISCUSSION_DIRECTION","COUNTER_PRE_DISCUSSION_DIRECTION")
WORLDS=tuple(itertools.product(GROUPS,tuple(POLICIES),CONTEXTS))
CSV_NAME="R306_ALL_648_ORIGINAL_POLARIZATION_PERSON_SOURCES.csv"
RESULT_NAME="R306_EXACT_GROUP_POLARIZATION_RESULTS.json"
RECEIPT_NAME="R306_MACHINE_RECEIPT.json"

def direction(x):return 1 if x>ZERO else (-1 if x<ZERO else 0)

def name(group,policy,context):
    return "group="+",".join(map(str,group))+"|policy="+policy+"|context="+context

def evaluate(group,policy,context):
    if (group,policy,context) not in WORLDS:raise ValueError("unknown frozen polarization world")
    m=sum(group,ZERO)/3
    q=direction(m)
    comparator=max(group) if q>0 else (min(group) if q<0 else ZERO)
    argument=F(q if context=="SUPPORT_PRE_DISCUSSION_DIRECTION" else -q)
    alpha,beta=POLICIES[policy]
    post=m+alpha*(comparator-m)+beta*(argument-m)
    if not -ONE<=post<=ONE:raise AssertionError("out of convex source range")
    if m==ZERO:status="NO_INITIAL_DIRECTION"
    elif post==ZERO:status="AT_ZERO"
    elif direction(post)!=q:status="DIRECTION_FLIP"
    elif abs(post)>abs(m):status="POLARIZED"
    elif abs(post)<abs(m):status="DEPOLARIZED"
    else:status="UNCHANGED"
    return {"pre_group_mean":m,"pre_group_direction":q,
       "social_comparison_target":comparator,
       "argument_target":argument,"social_comparison_weight":alpha,
       "persuasive_argument_weight":beta,"post_consensus_mean":post,
       "group_mean_signed_change":post-m,
       "absolute_extremity_change":abs(post)-abs(m),
       "polarization_status":status,
       "strict_same_direction_polarization":status=="POLARIZED",
       "direction_flipped":status=="DIRECTION_FLIP"}

def source(group,policy,context,person_index):
    if person_index not in (0,1,2):raise ValueError("person index not frozen")
    vals=evaluate(group,policy,context)
    return {"world":name(group,policy,context),
      "full_original_pre_opinion_triplet":";".join(str(x) for x in group),
      "policy":policy,"argument_context":context,"person_index":person_index,
      "person_pre_opinion":group[person_index],
      "person_post_consensus_opinion":vals["post_consensus_mean"],
      "person_opinion_changed":group[person_index]!=vals["post_consensus_mean"],
      **vals}

def sources():return tuple(source(*w,i) for w in WORLDS for i in range(3))

def verify():
    assert len(GROUPS)==27 and len(WORLDS)==216 and len(sources())==648
    assert len({(s["world"],s["person_index"]) for s in sources()})==648
    for group,policy,context in WORLDS:
        x=evaluate(group,policy,context)
        assert x["group_mean_signed_change"]==x["post_consensus_mean"]-x["pre_group_mean"]
        assert x["absolute_extremity_change"]==abs(x["post_consensus_mean"])-abs(x["pre_group_mean"])
        assert sum((source(group,policy,context,i)["person_post_consensus_opinion"] for i in range(3)),ZERO)/3==x["post_consensus_mean"]
        if policy=="CONSENSUS_AVERAGING":
            assert x["group_mean_signed_change"]==ZERO
            assert x["polarization_status"] in ("UNCHANGED","NO_INITIAL_DIRECTION")
        if sum(group,ZERO)==ZERO:
            assert x["post_consensus_mean"]==ZERO
            assert x["polarization_status"]=="NO_INITIAL_DIRECTION"
        mirror=tuple(-v for v in group)
        assert evaluate(mirror,policy,context)["post_consensus_mean"]==-x["post_consensus_mean"]
        assert evaluate(mirror,policy,context)["polarization_status"]==x["polarization_status"]
    homo=(F(1,2),)*3
    hetero=(ZERO,ZERO,F(1,2))
    assert evaluate(homo,"SOCIAL_COMPARISON_ONLY",CONTEXTS[0])["post_consensus_mean"]==F(1,2)
    assert evaluate(homo,"PERSUASIVE_ARGUMENT_ONLY",CONTEXTS[0])["post_consensus_mean"]==F(3,4)
    assert evaluate(homo,"PERSUASIVE_ARGUMENT_ONLY",CONTEXTS[1])["post_consensus_mean"]==F(-1,4)
    assert evaluate(homo,"PERSUASIVE_ARGUMENT_ONLY",CONTEXTS[1])["polarization_status"]=="DIRECTION_FLIP"
    assert evaluate(hetero,"SOCIAL_COMPARISON_ONLY",CONTEXTS[0])["post_consensus_mean"]==F(1,3)
    assert evaluate(hetero,"PERSUASIVE_ARGUMENT_ONLY",CONTEXTS[0])["post_consensus_mean"]==F(7,12)
    assert evaluate(hetero,"COMBINED_SOCIAL_AND_ARGUMENT",CONTEXTS[0])["post_consensus_mean"]==F(3,4)
    assert evaluate(hetero,"PERSUASIVE_ARGUMENT_ONLY",CONTEXTS[1])["post_consensus_mean"]==F(-5,12)
    return True

def emit():
    verify()
    cols=("world","full_original_pre_opinion_triplet","policy","argument_context","person_index",
      "person_pre_opinion","person_post_consensus_opinion","person_opinion_changed",
      "pre_group_mean","pre_group_direction","social_comparison_target","argument_target",
      "social_comparison_weight","persuasive_argument_weight","post_consensus_mean",
      "group_mean_signed_change","absolute_extremity_change","polarization_status",
      "strict_same_direction_polarization","direction_flipped")
    csvpath=ROOT/CSV_NAME
    with csvpath.open("w",newline="",encoding="utf-8") as f:
        w=csv.DictWriter(f,fieldnames=cols,lineterminator="\n");w.writeheader()
        for s in sources():w.writerow({k:str(s[k]) for k in cols})
    outcomes=[]
    for group,policy,context in WORLDS:
        result=evaluate(group,policy,context)
        outcomes.append({"world":name(group,policy,context),
           "pre_opinions":[str(x) for x in group],"policy":policy,"argument_context":context,
           "outcome":{k:str(v) for k,v in result.items()},
           "three_original_person_sources":[{k:str(source(group,policy,context,i)[k]) for k in cols if k!="world"} for i in range(3)]})
    counts={p:{context:{name:sum(evaluate(g,p,context)["polarization_status"]==name for g in GROUPS)
                    for name in ("POLARIZED","DEPOLARIZED","DIRECTION_FLIP","UNCHANGED","AT_ZERO","NO_INITIAL_DIRECTION")}
                for context in CONTEXTS}
            for p in POLICIES}
    data={"research_id":"R306","original_catalogue_id":"03-012","freeze_commit":FREEZE,
       "scope":"E1_SYNTHETIC_FINITE_GROUP_MEAN_POLARIZATION_PROJECT_INVENTED_CONSENSUS_MECHANISM",
       "all_original_source_person_rows":648,"synthetic_group_worlds":216,
       "ordered_artificial_opinion_triplets":27,"model_mechanism_policies":4,
       "argument_contexts":2,
       "new_project_mathematics_not_original_Moscovici_Myers_fitted_equation":True,
       "original_1969_or_1976_human_data_reproduced":False,
       "new_real_human_E2":0,"new_real_animal_E2":0,"new_historical_E3":0,
       "R073":"FROZEN","PESEN_v0_1":"FROZEN",
       "status_counts_by_policy_and_argument":counts,
       "frozen_reference":{"homogeneous_social_comparison_support":"1/2",
        "homogeneous_supportive_argument":"3/4",
        "homogeneous_counterargument":"-1/4",
        "heterogeneous_social_comparison_support":"1/3",
        "heterogeneous_supportive_argument":"7/12",
        "heterogeneous_combined_support":"3/4",
        "heterogeneous_counterargument":"-5/12",
        "all_neutral_stays_neutral":True},
       "worlds":outcomes}
    p=ROOT/RESULT_NAME
    p.write_text(json.dumps(data,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    receipt={"research_id":"R306","freeze_commit":FREEZE,"original_source_rows":648,
      "source_sha256":hashlib.sha256(csvpath.read_bytes()).hexdigest(),
      "results_sha256":hashlib.sha256(p.read_bytes()).hexdigest(),"new_E2":0,"new_E3":0}
    (ROOT/RECEIPT_NAME).write_text(json.dumps(receipt,indent=2)+"\n",encoding="utf-8")
    return receipt

class Tests(unittest.TestCase):
    def test_all(self):self.assertTrue(verify())
    def test_full_worlds(self):self.assertEqual(len(WORLDS),216)
    def test_all_source_rows(self):self.assertEqual(len(sources()),648)
    def test_avg(self):self.assertEqual(evaluate((ZERO,ZERO,F(1,2)),"CONSENSUS_AVERAGING",CONTEXTS[0])["post_consensus_mean"],F(1,6))
    def test_homogeneous_social(self):self.assertEqual(evaluate((F(1,2),)*3,"SOCIAL_COMPARISON_ONLY",CONTEXTS[0])["post_consensus_mean"],F(1,2))
    def test_homogeneous_argument(self):self.assertEqual(evaluate((F(1,2),)*3,"PERSUASIVE_ARGUMENT_ONLY",CONTEXTS[0])["post_consensus_mean"],F(3,4))
    def test_homogeneous_counterargument(self):self.assertEqual(evaluate((F(1,2),)*3,"PERSUASIVE_ARGUMENT_ONLY",CONTEXTS[1])["polarization_status"],"DIRECTION_FLIP")
    def test_heterogeneous_social(self):self.assertEqual(evaluate((ZERO,ZERO,F(1,2)),"SOCIAL_COMPARISON_ONLY",CONTEXTS[0])["post_consensus_mean"],F(1,3))
    def test_heterogeneous_argument(self):self.assertEqual(evaluate((ZERO,ZERO,F(1,2)),"PERSUASIVE_ARGUMENT_ONLY",CONTEXTS[0])["post_consensus_mean"],F(7,12))
    def test_heterogeneous_both(self):self.assertEqual(evaluate((ZERO,ZERO,F(1,2)),"COMBINED_SOCIAL_AND_ARGUMENT",CONTEXTS[0])["post_consensus_mean"],F(3,4))
    def test_no_initial(self):self.assertEqual(evaluate((ZERO,ZERO,ZERO),"COMBINED_SOCIAL_AND_ARGUMENT",CONTEXTS[0])["polarization_status"],"NO_INITIAL_DIRECTION")
    def test_bad_argument(self):
        with self.assertRaises(ValueError):evaluate((ZERO,ZERO,ZERO),"CONSENSUS_AVERAGING","ABSENT")
    def test_bad_policy(self):
        with self.assertRaises(ValueError):evaluate((ZERO,ZERO,ZERO),"X","SUPPORT_PRE_DISCUSSION_DIRECTION")
    def test_bad_pre_group(self):
        with self.assertRaises(ValueError):evaluate((ZERO,ZERO,F(1,4)),"CONSENSUS_AVERAGING",CONTEXTS[0])
    def test_bad_person(self):
        with self.assertRaises(ValueError):source((ZERO,ZERO,ZERO),"CONSENSUS_AVERAGING",CONTEXTS[0],3)

def generated(world,idx,kind):
    def case(self):
        z=source(*world,idx);e=evaluate(*world)
        if kind=="post":self.assertEqual(z["person_post_consensus_opinion"],e["post_consensus_mean"])
        elif kind=="status":self.assertEqual(z["polarization_status"],e["polarization_status"])
        elif kind=="pre":self.assertEqual(z["person_pre_opinion"],world[0][idx])
        else:raise AssertionError(kind)
    return case
for i,w in enumerate(WORLDS):
    for idx in range(3):
        for kind in ("post","status","pre"):
            setattr(Tests,f"test_world{i}_person{idx}_{kind}",generated(w,idx,kind))
if __name__=="__main__":
    p=argparse.ArgumentParser()
    m=p.add_mutually_exclusive_group(required=True)
    m.add_argument("--test",action="store_true");m.add_argument("--emit",action="store_true")
    a=p.parse_args()
    if a.test:unittest.main(argv=["R306"],verbosity=1)
    else:print(json.dumps(emit(),indent=2))
