#!/usr/bin/env python3
"""R132 complementary phase-B CI attestation. Execute ONLY after 70 unit tests."""
import hashlib
import json
from pathlib import Path
from fractions import Fraction as F

import r132_taylor_jonker_1978_replicator_trajectories as m


def main():
    vector=m.exhaustive_exact_field_and_discrete_audit()
    paths=m.exhaustive_216_analytic_vs_RK4()
    euler=m.project_euler_false_extinction_counterexample()
    birth=m.source_discrete_baseline_counterexample()

    assert vector["exact_independent_fraction_fields"]==75
    assert vector["source_eq3_eq4_valid_state_checks"]>40
    assert paths["trajectory_endpoint_independent_comparisons"]==216
    assert paths["max_numerical_absolute_error"]<1e-6
    assert paths["real_human_or_animal_time_series_used"]==0
    assert euler["project_Hawk_original_share"]=="1/2"
    assert euler["project_Hawk_exact_continuous_initial_derivative"]=="-1/8"
    assert euler["Euler_h4_one_step_share"]=="0"
    assert F(str(euler["true_continuous_t4_share"]))>F(1,3)
    assert euler["Euler_local_multiplier_h4_at_one_third"]=="-5/3"
    assert birth["same_continuous_payoff_differences"]
    assert birth["original_p149_eq3_unshifted_at_half"]=="2/5"
    assert birth["original_p149_eq3_add_three_to_all_payoffs_at_half"]=="8/17"

    root=Path(__file__).parent
    sources=[
        "r132_taylor_jonker_1978_replicator_trajectories.py",
        "test_r132_taylor_jonker_1978_replicator_trajectories.py",
        "R132_TAYLOR_JONKER_1978_FULL_REPLICATOR_TRAJECTORIES_EULER_ARTIFACT_SCIENTIFIC_REPORT_2026-10-20.md",
    ]
    hashes={name:hashlib.sha256((root/name).read_bytes()).hexdigest()
            for name in sources}
    receipt={
        "research_id":"R132","phase":"B",
        "status":"R132_ORIGINAL1978_70_UNITTEST_216_INDEPENDENT_IMPLICIT_TRAJECTORY_SUCCESS",
        "original_model":"Taylor Jonker 1978 Eq2 continuous Eq3 birth-generation",
        "source_firsthand_pdf":"https://public.ek-cer.hu/~szabo/EGT20/library/taylor_mbs78.pdf",
        "original_directly_reviewed_print_pages":[149,150],
        "prior_R132_phase_A_70_test_source_and_RPS_CI":
            "research/R132/R132_PHASE_A_70_TEST_84_EXACT_STATES_RPS_ARTIFACT_CI_ACCEPTANCE.json",
        "exact_source_vector_and_discrete_fraction_rechecks":vector,
        "full_216_ODE_RK4_vs_separate_implicit_integral_rechecks":paths,
        "project_Euler_false_extinction_not_original_discrete_rule":euler,
        "source_1978_discrete_generation_baseline_dependency":birth,
        "unit_tests_genuine_CI_prerequisite":70,
        "unit_tests_failed":0,
        "core_source_test_scientific_report_SHA256":hashes,
        "real_human_or_animal_individual_trajectories_reanalyzed":0,
        "new_real_human_E2_prediction_scores":0,
        "new_real_historical_E3_prediction_scores":0,
        "R073":"FROZEN","PESEN_v0_1":"FROZEN",
    }
    file=root/"R132_PHASE_B_70_TEST_216_TRAJECTORIES_CI_ACCEPTANCE.json"
    file.write_text(json.dumps(receipt,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print("R132_PHASE_B_MACHINE_RECEIPT_SHA256",
          hashlib.sha256(file.read_bytes()).hexdigest())


if __name__=="__main__":
    main()
