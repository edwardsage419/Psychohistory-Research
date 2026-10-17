"""R074 E3 external comparison synthetic tests. No real humans in tests."""
import copy
import json
import unittest
from r074_dalbo_external_human_e3 import (
    MODEL_NAMES, R073_GIT_BLOB, SOURCE_SHA256, verify_frozen_code,
    prepare_external_sessions, fit_other_sessions, evaluate_external,
    predict, brier,
)

EVENTS=[
    (1,1,1,1,1),
    (1,0,1,1,1),
    (0,0,0,0,0),
    (0,1,1,0,0),
    (1,1,0,1,1),
    (0,1,0,1,0),
]

def fabricate():
    return {
        f"s{i}":{"treatment":(32,"0.5"),"events":list(EVENTS)}
        for i in range(1,4)
    }

class E3OriginalExperimentTests(unittest.TestCase):
    def test_01_code_pin(self):
        verify_frozen_code()
        self.assertEqual(len(R073_GIT_BLOB),40)

    def test_02_original_sha_pin(self):
        self.assertEqual(len(SOURCE_SHA256),64)

    def test_03_model_names_exact(self):
        self.assertEqual(len(MODEL_NAMES),7)
        self.assertEqual(MODEL_NAMES[0],"M0_TREATMENT_PREVALENCE")

    def test_04_three_session_common_risk_set(self):
        r=evaluate_external(fabricate())
        self.assertEqual(r["sessions_equal_weighted"],3)
        self.assertEqual(r["scored_decisions"],len(EVENTS)*3)
        self.assertEqual(len(r["model_macro"]),7)

    def test_05_two_other_sessions_only(self):
        f=fit_other_sessions(fabricate(),"s1")
        self.assertEqual(f["trained_from_other_sessions_same_treatment"],2)
        self.assertEqual(f["train_target_count"],len(EVENTS)*2)

    def test_06_treatment_isolation(self):
        s=fabricate()
        a=fit_other_sessions(s,"s1")
        for i in range(4,7):
            s[f"s{i}"]={"treatment":(40,"0.75"),"events":list(EVENTS)}
        b=fit_other_sessions(s,"s1")
        self.assertEqual(a,b)

    def test_07_modify_heldout_targets_no_effect_on_fit(self):
        s=fabricate()
        a=fit_other_sessions(s,"s1")
        s["s1"]["events"]=[(x[0],x[1],x[2],x[3],1-x[4])
                            for x in s["s1"]["events"]]
        b=fit_other_sessions(s,"s1")
        self.assertEqual(a,b)

    def test_08_own_target_does_not_change_same_round_prediction(self):
        f=fit_other_sessions(fabricate(),"s1")
        r=(1,0,1,1,0)
        p=predict("M3_JOINT_LAST",r,f)
        self.assertEqual(p,predict("M3_JOINT_LAST",r[:4]+(1,),f))

    def test_09_tft_reference_exact(self):
        f=fit_other_sessions(fabricate(),"s1")
        self.assertAlmostEqual(predict("M5_TFT_NOISY",(1,0,0,0,1),f),.05)
        self.assertAlmostEqual(predict("M5_TFT_NOISY",(0,1,0,0,0),f),.95)

    def test_10_wsls_reference_exact(self):
        f=fit_other_sessions(fabricate(),"s1")
        self.assertAlmostEqual(predict("M6_WSLS_NOISY",(1,1,0,0,0),f),.95)
        self.assertAlmostEqual(predict("M6_WSLS_NOISY",(0,1,0,0,1),f),.05)

    def test_11_all_macro_probs_finite(self):
        r=evaluate_external(fabricate())
        for v in r["model_macro"].values():
            self.assertTrue(0<=v["all_sessions_equal_weight_Brier"]<=1)
            self.assertGreaterEqual(v["all_sessions_equal_weight_log_loss"],0)

    def test_12_all_paired_names_and_votes(self):
        r=evaluate_external(fabricate())
        self.assertEqual(len(r["paired_comparisons"]),6)
        for x in r["paired_comparisons"].values():
            self.assertEqual(x["all_sessions_better"]+
                             x["all_sessions_equal"]+
                             x["all_sessions_worse"],3)

    def test_13_per_treatment_votes_equal_three(self):
        r=evaluate_external(fabricate())
        for comparison in r["paired_comparisons"].values():
            self.assertEqual(len(comparison["per_treatment"]),1)
            self.assertEqual(next(iter(comparison["per_treatment"].values()))["sessions"],3)

    def test_14_no_session_id_export(self):
        r=json.dumps(evaluate_external(fabricate()))
        for name in ("s1","s2","s3"):
            self.assertNotIn('"'+name+'"',r)

    def test_15_one_session_cannot_train(self):
        s=fabricate()
        s.pop("s2")
        s.pop("s3")
        with self.assertRaisesRegex(ValueError,"SINGLE_SESSION"):
            evaluate_external(s)

    def test_16_empty_holdout_forbidden(self):
        s=fabricate()
        s["s1"]["events"]=[]
        with self.assertRaisesRegex(ValueError,"NO_TEST_EVENTS"):
            evaluate_external(s)

    def test_17_bad_binary_forbidden(self):
        s=fabricate()
        s["s1"]["events"].append((2,0,1,0,1))
        with self.assertRaisesRegex(ValueError,"INVALID_EVENT"):
            evaluate_external(s)

    def test_18_p0_degenerate_forbidden(self):
        s=fabricate()
        s["s2"]["events"]=[ev[:4]+(1,) for ev in EVENTS]
        s["s3"]["events"]=[ev[:4]+(1,) for ev in EVENTS]
        with self.assertRaisesRegex(ValueError,"DEGENERATE"):
            fit_other_sessions(s,"s1")

    def test_19_hash_wrong_source_blocks_before_scores(self):
        with self.assertRaisesRegex(ValueError,"SHA256_MISMATCH"):
            prepare_external_sessions(b"fake data")

    def test_20_joint_condition_is_not_guaranteed_to_win(self):
        # Intentionally fabricate a fit where tiny substate misleads M3.
        fit={"train_only_prevalence":0.5,
             "state_counts":{
                 "M1_OWN_LAST":{(1,):(9,10)},
                 "M3_JOINT_LAST":{(1,1):(0,5)}
             }}
        target=(1,1,1,1,1)
        p1=predict("M1_OWN_LAST",target,fit)
        p3=predict("M3_JOINT_LAST",target,fit)
        self.assertGreater(brier(1,p3),brier(1,p1))

if __name__=="__main__":
    unittest.main()
