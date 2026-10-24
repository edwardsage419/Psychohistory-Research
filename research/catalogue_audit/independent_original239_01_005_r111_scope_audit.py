#!/usr/bin/env python3
"""Independent source-identity and evidence-scope audit for existing R111."""
import ast
import hashlib
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
BASE=ROOT/"research/R111"
EXPECTED={
    "R111_MCFADDEN_1974_RANDOM_UTILITY_CONDITIONAL_LOGIT_FORMAL_BOUNDED_LEARNING_REPORT_2026-10-19.md":"dfb19b2fc93a491fca66bf5d9cdbed4f41e774316c140a195e24c03dfe0fcade",
    "r111_mcfadden_random_utility_conditional_logit.py":"c8cefb2d9c2cb9bf385ee0e1ad5eebe2ec592acf378c4f41e9cf948bdc3fe907",
    "test_r111_mcfadden_random_utility_conditional_logit.py":"d9872c8a312e76846b2cbc1074f0f6c45106424a47498119ca790ff60e414213",
}
def sha256(x):
    return hashlib.sha256(x).hexdigest()

def main():
    receipt=json.loads((BASE/"R111_PHASE_A_SYNTHETIC_MATH_CI_ACCEPTANCE_STATUS.json").read_text())
    formal=json.loads((BASE/"R111_FINAL_ACCEPTANCE_STATUS.json").read_text())
    assert receipt["source_and_test_file_SHA256"]==EXPECTED
    for name,digest in EXPECTED.items():
        raw=(BASE/name).read_bytes()
        assert sha256(raw)==digest,(name,sha256(raw))
        assert sha256(raw+b"\n")!=digest,"negative tamper control"
    tests=ast.parse((BASE/"test_r111_mcfadden_random_utility_conditional_logit.py").read_text())
    count=sum(isinstance(x,ast.FunctionDef) and x.name.startswith("test_") for node in ast.walk(tests) for x in [node])
    assert count==18,count
    assert formal["knowledge_catalogue_item"]==receipt["catalogue_item"]=="01-005"
    assert formal["research_id"]==receipt["research_id"]=="R111"
    assert formal["synthetic_model_tests_executed"]==receipt["synthetic_unittest_cases_passed"]==18
    assert formal["synthetic_failures"]==receipt["synthetic_unittest_failures"]==0
    assert formal["actual_human_data_loaded"] is False
    assert formal["actual_human_model_E2_scores"]==receipt["real_human_behavior_E2_scores"]==0
    assert formal["cross_population_reproduction"] is False
    assert formal["prospective_predictions"] is False
    assert receipt["PESEN_v0_1"]=="FROZEN"
    assert "McFadden" in formal["original_model_source"]
    assert "independent identically distributed Type-I extreme value" in formal["analytic_model"]
    assert receipt["status"]=="R111_MCFADDEN_CONDITIONAL_LOGIT_18_SYNTHETIC_TESTS_PASS"
    print("ORIGINAL239_01_005_R111_SCOPE_SHA256_AUDIT=PASS; TEST_FUNCTIONS=18; E2=0; E3=NOT_ESTABLISHED")

if __name__=="__main__":
    main()
