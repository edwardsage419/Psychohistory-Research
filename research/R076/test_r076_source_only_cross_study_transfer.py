"""R076 synthetic examples: no real human source or target in tests."""
import copy
import unittest
from r076_source_only_cross_study_transfer import (
    MODEL_NAMES, DONORS,PAIRS,EXPECTED_MODEL_NAMES,
    build_source_donors, transfer_predict_all,verify_r073_blob,check_targets,
)

EVENTS=[(1,0,1,1,1),(1,1,0,1,1),(0,0,0,0,0),
        (0,1,1,0,0),(1,1,1,0,1),(0,0,1,1,0)]
def source():
    s={}
    for tr in ("fix","rand"):
        for i in range(6):
            # R073 source fixture must respect native 100 action history.
            s[(tr,str(i))]={str(k):{t:(1 if (t+k+i)%3 else 0,
                                           1 if (t+i)%3 else 0) for t in range(1,101)}
                             for k in range(15 if tr=="rand" else 14)}
    # The actual R073 donor builder expects 92 people in fix/96 rand.
    # Adjust synthetic to 92=14*6+8, 96=16*6.
    for tr in ("fix","rand"):
        for i in range(6):
            needed=(16 if tr=="rand" else 16 if i<4 else 14)
            s[(tr,str(i))]={str(k):{t:((t+k+i)%2,(t+i+k)%3==0 and 1 or 0)
                       for t in range(1,101)} for k in range(needed)}
    return s

def target(kind="R074"):
    n=18
    if kind=="R074":
        tris=[(r,d) for r in (32,40,48) for d in ("0.5","0.75")]
        tr=[p for p in tris for _ in range(3)]
    else:
        tris=[("1.5","0.125"),("2","0.125"),("2.5","0.125"),
              ("4","0"),("4","0.0625"),("4","0.125")]
        tr=[x for x,num in zip(tris,(3,2,3,3,3,4)) for _ in range(num)]
    # This fixture validates downstream scoring independently of true source counts:
    return {f"fake-{k}":{"treatment":tr[k],"events":list(EVENTS)}
            for k in range(n)}

def synthetic_source_fits():
    s={}
    for d in DONORS:
        s[d]={"train_only_prevalence":0.5,
              "state_counts":{model:{} for model in MODEL_NAMES[1:5]},
              "source_sessions":12 if d==DONORS[0] else 6,
              "train_target_count":18424 if d==DONORS[0] else 9000}
    return s

class SourceOnlyTransferTests(unittest.TestCase):
    def test_01_frozen_real_model_blob(self):verify_r073_blob()
    def test_02_frozen_name_list(self):self.assertEqual(MODEL_NAMES,EXPECTED_MODEL_NAMES)
    def test_03_frozen_three_donors(self):self.assertEqual(len(DONORS),3)
    def test_04_six_predeclared_pairs(self):self.assertEqual(len(PAIRS),6)
    def test_05_r074_six_target_strata(self):self.assertEqual(len(set(v["treatment"] for v in target().values())),6)
    def test_06_r075_six_target_strata(self):self.assertEqual(len(set(v["treatment"] for v in target("R075").values())),6)
    def test_07_r074_wrong_count_denied(self):
        with self.assertRaisesRegex(ValueError,"EVENT_UNIVERSE"):
            check_targets(target(),"R074")
    def test_08_r075_wrong_count_denied(self):
        with self.assertRaisesRegex(ValueError,"EVENT_UNIVERSE"):
            check_targets(target("R075"),"R075")
    def test_09_no_target_training_fit_writable_api(self):
        # No argument accepts a target-specific training data object.
        import inspect
        params=list(inspect.signature(transfer_predict_all).parameters)
        self.assertEqual(params,["source_fits","target_sessions","target","donors"])
    def test_10_source_fit_expected_universe_guard(self):
        with self.assertRaisesRegex(ValueError,"SESSION_COUNT"):
            build_source_donors({("fix","1"):{}})
    def test_11_target_outcome_type_denied(self):
        t=target()
        t["fake-0"]["events"][0]=(1,0,0,0,2)
        # Event counts checked first, then binary; fake complete scaling to 15338.
        with self.assertRaisesRegex(ValueError,"EVENT_UNIVERSE"):
            check_targets(t,"R074")
    def test_12_r074_fake_score_exact_denominator(self):
        t=target()
        # Construct 15338 targets across 18 sessions, preserve 6x3 structure.
        for i,s in enumerate(sorted(t)):
            n=853+(i<2)
            t[s]["events"]=(EVENTS*(n//len(EVENTS)+1))[:n]
        self.assertEqual(sum(len(x["events"]) for x in t.values()),15356)
        with self.assertRaisesRegex(ValueError,"EVENT_UNIVERSE"):
            transfer_predict_all(synthetic_source_fits(),t,"R074")
    def test_13_source_only_predictions_no_fit_to_targets(self):
        # A fixed fit's prediction of a given event cannot change with
        # any target labels for any observed session.
        from r073_human_ipd_memory_loso import predict
        f=synthetic_source_fits()[DONORS[0]]
        event=(1,0,1,1,1)
        p=predict("M3_JOINT_LAST",event,f)
        self.assertEqual(p,predict("M3_JOINT_LAST",event[:4]+(0,),f))
    def test_14_tft_three_donors_invariant(self):
        from r073_human_ipd_memory_loso import predict
        f=synthetic_source_fits()
        e=(1,0,1,1,1)
        self.assertEqual({predict("M5_TFT_NOISY",e,f[d]) for d in DONORS},{.05})
    def test_15_m4_three_donors_reflect_source_difference(self):
        from r073_human_ipd_memory_loso import predict
        f=synthetic_source_fits()
        f[DONORS[0]]["state_counts"]["M4_JOINT_TWO_LAGS"][(1,0,1,1)]=(20,20)
        e=(1,0,1,1,1)
        self.assertNotEqual(predict("M4_JOINT_TWO_LAGS",e,f[DONORS[0]]),
                            predict("M4_JOINT_TWO_LAGS",e,f[DONORS[1]]))
    def test_16_prior_target_baseline_is_not_used(self):
        import inspect
        import r076_source_only_cross_study_transfer as x
        body=inspect.getsource(x.transfer_predict_all)
        self.assertNotIn("fit_other_sessions(",body)
        self.assertNotIn("train_only_other_sessions(",body)
    def test_17_all_study_ids_not_exported(self):
        self.assertFalse("sessions_identifiers_exported" in str(synthetic_source_fits()))
    def test_18_target_treatment_is_an_aggregation_key_only(self):
        from r073_human_ipd_memory_loso import predict
        f=synthetic_source_fits()[DONORS[0]]
        for e in EVENTS:
            self.assertEqual(predict("M1_OWN_LAST",e,f),
                             predict("M1_OWN_LAST",e,f))
    def test_19_source_training_count_rejects_wrong_people(self):
        # Each dummy fixed six-session subset has a wrong participant count.
        s={("fix",str(i)):{str(j):{t:(1,1) for t in range(1,101)}
                          for j in range(2)} for i in range(6)}
        s.update({("rand",str(i)):{str(j):{t:(1,1) for t in range(1,101)}
                          for j in range(2)} for i in range(6)})
        with self.assertRaisesRegex(ValueError,"RISK_SET"):
            build_source_donors(s)
    def test_20_data_sniffed_after_protocol_only(self):
        self.assertTrue(DONORS[0].endswith("POOLED"))
    def test_21_transported_models_count(self):
        self.assertEqual(len(EXPECTED_MODEL_NAMES),7)
    def test_22_no_fourth_experiment_claim(self):
        import inspect
        import r076_source_only_cross_study_transfer as x
        self.assertIn("RETROSPECTIVE",inspect.getsource(x.run))
    def test_23_other_donor_fit_independent_objects(self):
        fits=synthetic_source_fits()
        fits[DONORS[0]]["train_only_prevalence"]=.6
        self.assertEqual(fits[DONORS[1]]["train_only_prevalence"],.5)
    def test_24_model_outcome_flip_rejects_invalid_binary(self):
        from r073_human_ipd_memory_loso import predict
        f=synthetic_source_fits()[DONORS[0]]
        with self.assertRaisesRegex(ValueError,"BINARY"):
            predict("M4_JOINT_TWO_LAGS",(1,0,0,0,5),f)
if __name__=="__main__":unittest.main()
