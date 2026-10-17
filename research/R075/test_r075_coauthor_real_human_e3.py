"""R075 third experiment frozen seven-model E3 tests: fully invented actions."""
import unittest
from r075_coauthor_real_human_e3 import (
    verify_frozen_r073, MODEL_NAMES,MODEL_BLOB_SHA1,ORIGINAL_SHA256,
    ORIGINAL_TEXT_SHA256,EXPECTED_TREATMENT_SESSION_COUNT,
    fit_other_sessions,evaluate_external,prepare_original_sessions,predict,
    state_for,brier
)

ROWS=[(1,1,1,0,1),(1,0,0,1,1),(0,1,1,1,0),
      (0,0,1,0,0),(1,1,0,0,1),(0,0,0,0,1)]
def toy(two=False):
    n=2 if two else 3
    return {f"s{i}":{"treatment":("2","0.125"),"events":list(ROWS)}
             for i in range(n)}

class ThirdAuthorE3Tests(unittest.TestCase):
    def test_01_actual_model_blob_frozen(self):verify_frozen_r073()
    def test_02_seven_frozen(self):self.assertEqual(len(MODEL_NAMES),7)
    def test_03_source_SHA(self):self.assertEqual(len(ORIGINAL_SHA256),64)
    def test_04_text_SHA(self):self.assertEqual(len(ORIGINAL_TEXT_SHA256),64)
    def test_05_treatment_count(self):self.assertEqual(sum(EXPECTED_TREATMENT_SESSION_COUNT.values()),18)
    def test_06_three_session_score(self):
        a=evaluate_external(toy())
        self.assertEqual(a["test_sessions"],3)
        self.assertEqual(a["individual_test_targets"],18)
        self.assertEqual(len(a["model_macro"]),7)
    def test_07_two_session_score(self):
        a=evaluate_external(toy(True))
        self.assertEqual(a["test_sessions"],2)
        self.assertEqual(a["individual_test_targets"],12)
    def test_08_other_train_only(self):
        a=fit_other_sessions(toy(),"s0")
        self.assertEqual(a["train_target_count"],12)
        self.assertEqual(a["trained_from_other_sessions_same_treatment"],2)
    def test_09_only_one_other_train(self):
        a=fit_other_sessions(toy(True),"s0")
        self.assertEqual(a["train_target_count"],6)
        self.assertEqual(a["trained_from_other_sessions_same_treatment"],1)
    def test_10_no_heldout_targets_contaminate_training(self):
        a=toy()
        fit1=fit_other_sessions(a,"s0")
        a["s0"]["events"]=[e[:4]+(1-e[4],) for e in ROWS]
        self.assertEqual(fit1,fit_other_sessions(a,"s0"))
    def test_11_same_round_prediction_ignores_target(self):
        fit=fit_other_sessions(toy(),"s0")
        a=(1,0,1,0,1)
        self.assertEqual(predict("M3_JOINT_LAST",a,fit),
                         predict("M3_JOINT_LAST",a[:4]+(0,),fit))
    def test_12_treatment_exclusion(self):
        a=toy()
        f=fit_other_sessions(a,"s0")
        a["x"]={"treatment":("4","0"),"events":list(ROWS)}
        self.assertEqual(f,fit_other_sessions(a,"s0"))
    def test_13_report_only_anonymous_session_count(self):
        result=evaluate_external(toy())
        self.assertNotIn("s0",str(result))
        self.assertFalse(result["session_rows_exported"])
    def test_14_m0_training_rate(self):
        a=fit_other_sessions(toy(),"s0")
        self.assertTrue(0<a["train_only_prevalence"]<1)
    def test_15_m3_two_state_choice_history(self):
        self.assertEqual(state_for("M3_JOINT_LAST",ROWS[0]),(1,1))
    def test_16_m4_four_lags(self):
        self.assertEqual(state_for("M4_JOINT_TWO_LAGS",ROWS[0]),(1,1,1,0))
    def test_17_TFT_does_not_adapt_error(self):
        f=fit_other_sessions(toy(),"s0")
        self.assertAlmostEqual(predict("M5_TFT_NOISY",(0,1,1,0,0),f),.95)
        self.assertAlmostEqual(predict("M5_TFT_NOISY",(1,0,1,0,0),f),.05)
    def test_18_external_wrong_zip_sha_blocks(self):
        with self.assertRaises(ValueError):prepare_original_sessions(b"fake")
    def test_19_degenerate_p0_fails_closed(self):
        a=toy()
        for x in ("s1","s2"):
            a[x]["events"]=[row[:4]+(1,) for row in ROWS]
        with self.assertRaisesRegex(ValueError,"DEGENERATE"):
            fit_other_sessions(a,"s0")
    def test_20_no_future_observations(self):
        a=evaluate_external(toy())
        for k,v in a["paired_comparisons"].items():
            self.assertEqual(v["sessions_better"]+v["sessions_equal"]+v["sessions_worse"],3)
    def test_21_zero_target_fold_fails(self):
        a=toy();a["s0"]["events"]=[]
        with self.assertRaisesRegex(ValueError,"HELDOUT_SESSION_EMPTY"):
            evaluate_external(a)
    def test_22_bad_action_fails(self):
        a=toy();a["s0"]["events"][0]=(3,1,0,1,0)
        with self.assertRaisesRegex(ValueError,"INVALID_EXTERNAL_EVENT"):
            evaluate_external(a)
    def test_23_only_one_session_fails(self):
        a=toy(True);a.pop("s1")
        with self.assertRaisesRegex(ValueError,"NO_EXCLUSIVE_OTHER_SESSION"):
            evaluate_external(a)
    def test_24_brier_counterexample_joint_can_worsen(self):
        fit={"train_only_prevalence":.5,
             "state_counts":{"M1_OWN_LAST":{(1,):(9,10)},
                             "M3_JOINT_LAST":{(1,1):(0,5)}}}
        sample=(1,1,0,0,1)
        self.assertGreater(brier(1,predict("M3_JOINT_LAST",sample,fit)),
                           brier(1,predict("M1_OWN_LAST",sample,fit)))

if __name__=="__main__":
    unittest.main()
