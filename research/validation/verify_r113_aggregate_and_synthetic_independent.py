#!/usr/bin/env python3
"""R113 independent published-aggregate and rational toy E1 recheck."""
from __future__ import annotations
from fractions import Fraction as F
from pathlib import Path
import hashlib
import importlib.util
import json

TABLE={"behavior":(44,12,44),"empirical":(44,28,28),
       "personal_normative":(100,22,52),"normative_expectation":(100,10,79)}

def verify_table(t):
    if t!=TABLE:
        raise AssertionError("FROZEN_PUBLISHED_TABLE2_MISMATCH")
    if sum(t["behavior"])!=100 or sum(t["empirical"])!=100:
        raise AssertionError("EXCLUSIVE_OPTIONS_TOTAL")
    if sum(t["personal_normative"])!=174 or sum(t["normative_expectation"])!=189:
        raise AssertionError("MULTISELECT_JUDGMENTS_MUST_NOT_BE_NORMALIZED")
    d1=tuple(e-b for e,b in zip(t["empirical"],t["behavior"]))
    d2=tuple(n-p for n,p in zip(t["normative_expectation"],t["personal_normative"]))
    if d1!=(0,16,-16) or d2!=(0,-12,27):
        raise AssertionError("PUBLISHED_PERCENTAGE_POINT_DIFFERENCE")
    return d1,d2

def choose(base,ew,nw,e,n):
    margin=base+ew*(e-F(1,2))+nw*(n-F(1,2))
    return int(margin>=0)

def independent_toy():
    high,low=F(4,5),F(1,5)
    unconditional=(F(1,10),F(0),F(0))
    conditional=(F(-1,5),F(1,2),F(1,2))
    observed=(choose(*unconditional,high,high),choose(*conditional,high,high))
    intervened=(choose(*unconditional,low,low),choose(*conditional,low,low))
    if observed!=(1,1) or intervened!=(1,0):
        raise AssertionError("COUNTERFACTUAL_IDENTIFIABILITY")
    eonly=(F(-1,10),F(1),F(0))
    nonly=(F(-1,10),F(0),F(1))
    econtr=(choose(*eonly,high,high),choose(*eonly,low,high),choose(*eonly,high,low))
    ncontr=(choose(*nonly,high,high),choose(*nonly,low,high),choose(*nonly,high,low))
    if econtr!=(1,0,1) or ncontr!=(1,1,0):
        raise AssertionError("SELECTIVE_EXPECTATION_CONTRAST")
    return observed,intervened,econtr,ncontr

def original(root):
    directory=root/"research/R113"
    receipt=json.loads((directory/"R113_PHASE_A_AGGREGATE_AND_SYNTHETIC_VERIFIED_ACCEPTANCE.json").read_text(encoding="utf-8"))
    for name,expected in receipt["source_and_test_file_SHA256"].items():
        if hashlib.sha256((directory/name).read_bytes()).hexdigest()!=expected:
            raise AssertionError("ORIGINAL_R113_SHA256_MISMATCH "+name)
    path=directory/"r113_social_norm_expectations_identifiability.py"
    spec=importlib.util.spec_from_file_location("r113_original_comparison_only",path)
    mod=importlib.util.module_from_spec(spec)
    import sys
    sys.modules[spec.name]=mod
    spec.loader.exec_module(mod)
    return mod

def run(root):
    mod=original(root)
    d1,d2=verify_table(TABLE)
    src=mod.published_table_2_arithmetic()
    if tuple(src["published_actor_behavior_percent"])!=TABLE["behavior"]:
        raise AssertionError("ORIGINAL_BEHAVIOR_MISMATCH")
    if tuple(src["published_responder_empirical_expectation_percent"])!=TABLE["empirical"]:
        raise AssertionError("ORIGINAL_EMPIRICAL_MISMATCH")
    if tuple(src["published_responder_personal_normative_belief_percent"])!=TABLE["personal_normative"]:
        raise AssertionError("ORIGINAL_PERSONAL_NORM_MISMATCH")
    if tuple(src["published_proposer_normative_expectation_percent"])!=TABLE["normative_expectation"]:
        raise AssertionError("ORIGINAL_NORMATIVE_EXPECTATION_MISMATCH")
    if tuple(src["empirical_minus_behavior_percentage_points"])!=d1:
        raise AssertionError("ORIGINAL_EMPIRICAL_DIFFERENCE")
    if tuple(src["normative_minus_personal_ought_percentage_points"])!=d2:
        raise AssertionError("ORIGINAL_NORMATIVE_DIFFERENCE")
    if src["sum_personal_normative_judgment_percent"]!=174 or src["sum_normative_expectation_judgment_percent"]!=189:
        raise AssertionError("ORIGINAL_MULTISELECT_SUM")
    observed,intervened,econtr,ncontr=independent_toy()
    toy=mod.observational_equivalence_counterexample()
    if (toy["unconditional_world"]["observed_action"],toy["conditional_world"]["observed_action"])!=observed:
        raise AssertionError("ORIGINAL_TOY_OBSERVED")
    if (toy["unconditional_world"]["intervened_action"],toy["conditional_world"]["intervened_action"])!=intervened:
        raise AssertionError("ORIGINAL_TOY_COUNTERFACTUAL")
    single=mod.isolated_expectation_manipulation()
    for key,expected in (("empirical_only",econtr),("normative_only",ncontr)):
        got=tuple(single[key][field] for field in ("original","switch_empirical_only","switch_normative_only"))
        if got!=expected:
            raise AssertionError("ORIGINAL_SELECTIVE_CONTRAST")
    rejected=0
    altered=dict(TABLE)
    altered["behavior"]=(45,12,44)
    try:
        verify_table(altered)
    except AssertionError:
        rejected+=1
    altered=dict(TABLE)
    altered["personal_normative"]=(60,20,20)
    try:
        verify_table(altered)
    except AssertionError:
        rejected+=1
    if rejected!=2:
        raise AssertionError("NEGATIVE_CONTROLS_NOT_REJECTED")
    return {"research_id":"R113","catalogue_id":"03-007",
            "grade":"PASS_BOUNDED_INTERNAL_INDEPENDENT_AGGREGATE_AND_SYNTHETIC_E1",
            "published_table_rows_checked":4,"published_table_cells_checked":12,
            "published_empirical_minus_behavior_pp":list(d1),
            "published_normative_minus_personal_pp":list(d2),
            "multiple_response_sums":[174,189],
            "independent_rational_toy_checks":4,
            "original_sha256_files_verified":3,"negative_controls_rejected":rejected,
            "original_person_level_human_data_obtained":False,
            "new_human_E2_scores":0,"new_historical_E3_scores":0,
            "causal_norm_identification":False,"external_independent_replication":False,
            "R073":"FROZEN","PESEN_v0_1":"FROZEN"}

if __name__=="__main__":
    print(json.dumps(run(Path(__file__).resolve().parents[2]),indent=2,sort_keys=True))
