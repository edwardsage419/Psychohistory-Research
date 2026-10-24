#!/usr/bin/env python3
"""Independent source and scope audit for existing R112 Bayesian mathematics."""
import ast
import hashlib
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
BASE=ROOT/"research/R112"
EXPECTED={
    "R112_BAYESIAN_BELIEF_UPDATING_SOURCE_MECHANISM_AUDIT_2026-10-19.md":"a993eab18f4ce84ac54f17c82163c704f2a5049d1a955b652e57421dc62c183b",
    "r112_bayesian_belief_updating.py":"5712912b943d8ec61e3c7481180e3d295bdc8f608da9b3a0e3dbf62019fb180c",
    "test_r112_bayesian_belief_updating.py":"c557d7611e3ce149cb7a4009bc25f83d622cd4335a079f1846dad93f30442564",
}

def sha256(b):return hashlib.sha256(b).hexdigest()

def main():
    receipt=json.loads((BASE/"R112_PHASE_A_SYNTHETIC_BAYES_CI_ACCEPTANCE_STATUS.json").read_text())
    formal=json.loads((BASE/"R112_FINAL_ACCEPTANCE_STATUS.json").read_text())
    assert receipt["file_SHA256"]==EXPECTED
    for name,digest in EXPECTED.items():
        b=(BASE/name).read_bytes()
        assert sha256(b)==digest,(name,sha256(b))
        assert sha256(b+b"\n")!=digest,"tamper rejection"
    tests=ast.parse((BASE/"test_r112_bayesian_belief_updating.py").read_text())
    count=sum(isinstance(n,ast.FunctionDef) and n.name.startswith("test_") for n in ast.walk(tests))
    assert count==25,count
    assert receipt["knowledge_catalogue_item"]==formal["original_research_catalogue_item"]=="02-006"
    assert receipt["research_id"]==formal["research_id"]=="R112"
    assert receipt["pure_synthetic_unittest_count"]==formal["number_of_executed_synthetic_tests"]==25
    assert receipt["pure_synthetic_unittest_failures"]==formal["number_of_failed_synthetic_tests"]==0
    assert receipt["real_human_data_loaded"] is False
    assert receipt["real_human_E2_prediction_scores"]==formal["actual_human_E2_prediction_observations"]==0
    assert formal["real_human_cognitive_correspondence_established"] is False
    assert formal["true_independent_social_information_verified"] is False
    assert formal["cross_experiment_prediction"] is False
    assert formal["mathematical_mechanism_is_normative_not_empirically_established"] is True
    assert formal["research_scope"]=="FINITE_DISCRETE_HYPOTHESIS_UPDATING_AND_BETA_BERNOULLI_CONJUGACY"
    assert receipt["PESEN_v0_1"]=="FROZEN"
    print("ORIGINAL239_02_006_R112_SCOPE_SHA256_AUDIT=PASS; TEST_FUNCTIONS=25; E2=0; E3=NOT_ESTABLISHED")

if __name__=="__main__":
    main()
