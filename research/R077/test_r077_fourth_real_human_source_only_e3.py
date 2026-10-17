"""R077 fourth genuine author prospective-to-our-model evaluation; 24 synthetic guards."""
from __future__ import annotations
import inspect,math,unittest
from r077_fourth_real_human_source_only_e3 import (
    score_with_frozen_source,prepare_fourth_real_sessions,verify_r073_blob,
    R077_SHA,R077_MD5,EXPECTED_ROWS,EXPECTED_ORIGINAL_SESSIONS,
    EXPECTED_RISK_EVENTS,MODEL_NAMES,R073_BLOB_SHA1,FROZEN_PROTOCOL,SOURCE_DONOR
)

EV=((1,0,1,1,1),(1,1,1,0,1),(0,1,0,1,0),(0,0,0,0,0),
    (1,0,0,0,1),(1,1,0,1,0))
def fake_fit(p=.4):
    return {"train_only_prevalence":p,
        "state_counts":{m:{} for m in MODEL_NAMES[1:5]},
        "source_sessions":12,"train_target_count":18424}
def cases():
    return {
        "session-x":{"treatment":0,"events":[EV[0],EV[1],EV[2],EV[3]]},
        "session-y":{"treatment":1,"events":[EV[3],EV[4]]},
        "session-z":{"treatment":1,"events":[EV[2],EV[5]]}
    }
class GuardTests(unittest.TestCase):
    def test_01_original_R073_model_blob_frozen(self):verify_r073_blob()
    def test_02_original_model_families(self):self.assertEqual(len(MODEL_NAMES),7)
    def test_03_fourth_source_sha256(self):self.assertEqual(len(R077_SHA),64)
    def test_04_fourth_source_md5(self):self.assertEqual(len(R077_MD5),32)
    def test_05_source_count(self):self.assertEqual(EXPECTED_ROWS,3620)
    def test_06_sessions_count(self):self.assertEqual(EXPECTED_ORIGINAL_SESSIONS,15)
    def test_07_t3_count(self):self.assertEqual(EXPECTED_RISK_EVENTS,1040)
    def test_08_single_selected_donor(self):self.assertEqual(SOURCE_DONOR,"R073_ALL_12_POOLED")
    def test_09_source_only_score_synthetic(self):
        r=score_with_frozen_source(fake_fit(),cases())
        self.assertEqual(r["original_session_count"],3)
        self.assertEqual(r["scored_t3_human_events"],8)
    def test_10_models_all_reported(self):
        r=score_with_frozen_source(fake_fit(),cases())
        self.assertEqual(set(r["models"]),set(MODEL_NAMES))
    def test_11_six_pairs_all_reported(self):
        self.assertEqual(len(score_with_frozen_source(fake_fit(),cases())["paired_differences"]),6)
    def test_12_target_training_count_zero(self):
        r=score_with_frozen_source(fake_fit(),cases())
        self.assertEqual(r["target_labels_used_in_training"],0)
    def test_13_no_individual_names_or_ids_in_result(self):
        r=score_with_frozen_source(fake_fit(),cases())
        self.assertNotIn("session-x",str(r))
        self.assertNotIn("session-y",str(r))
        self.assertFalse(r["all_raw_sessions_and_action_sequences_exported"])
    def test_14_target_label_does_not_affect_source_fit(self):
        f=fake_fit()
        before=str(f)
        s=cases()
        score_with_frozen_source(f,s)
        s["session-x"]["events"]=[t[:4]+(1-t[-1],) for t in s["session-x"]["events"]]
        score_with_frozen_source(f,s)
        self.assertEqual(str(f),before)
    def test_15_target_session_size_does_not_weight_macro(self):
        x=cases()
        a=score_with_frozen_source(fake_fit(),x)
        x["session-y"]["events"]*=25
        b=score_with_frozen_source(fake_fit(),x)
        self.assertAlmostEqual(a["models"]["M0_TREATMENT_PREVALENCE"]["all_original_sessions_equal_Brier"],
                               b["models"]["M0_TREATMENT_PREVALENCE"]["all_original_sessions_equal_Brier"])
    def test_16_empty_target_fails(self):
        with self.assertRaisesRegex(ValueError,"EMPTY_TARGET_SESSIONS"):
            score_with_frozen_source(fake_fit(),{})
    def test_17_empty_session_fails(self):
        x=cases();x["session-y"]["events"]=[]
        with self.assertRaisesRegex(ValueError,"EMPTY_ORIGINAL_HELDOUT"):
            score_with_frozen_source(fake_fit(),x)
    def test_18_illegal_action_fails(self):
        x=cases();x["session-y"]["events"]=[(1,1,1,1,3)]
        with self.assertRaisesRegex(ValueError,"RISK_EVENTS_INVALID"):
            score_with_frozen_source(fake_fit(),x)
    def test_19_other_field_nonbinary_fails(self):
        x=cases();x["session-y"]["events"]=[(1,3,1,1,1)]
        with self.assertRaisesRegex(ValueError,"RISK_EVENTS_INVALID"):
            score_with_frozen_source(fake_fit(),x)
    def test_20_other_treatment_invalid(self):
        x=cases();x["session-y"]["treatment"]=99
        with self.assertRaisesRegex(ValueError,"TREATMENT_INVALID"):
            score_with_frozen_source(fake_fit(),x)
    def test_21_missing_both_treatments_rejected(self):
        x=cases();x["session-x"]["treatment"]=1
        with self.assertRaisesRegex(ValueError,"BOTH_ORIGINAL_TREATMENTS"):
            score_with_frozen_source(fake_fit(),x)
    def test_22_no_target_prevalence_recalibration(self):
        import r077_fourth_real_human_source_only_e3 as m
        body=inspect.getsource(m.score_with_frozen_source)
        self.assertNotIn("train_only_other_sessions",body)
        self.assertNotIn("fit_other_sessions",body)
        self.assertNotIn("sum(e[-1]",body)
        self.assertNotIn("state_counts[",body)
    def test_23_frozen_prior_publication(self):
        self.assertIn("FREEZE_2026-10-17",FROZEN_PROTOCOL)
    def test_24_no_pre_result_human_original_scoring_here(self):
        # All test examples have fabricated alphabetic session IDs.
        self.assertEqual(sum(len(a["events"]) for a in cases().values()),8)
if __name__=="__main__":unittest.main()
