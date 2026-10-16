"""R073 strictly synthetic memory/social history tests, no real subjects."""
import math,unittest
from collections import Counter
import r073_human_ipd_memory_loso as m


def fictional_sessions():
    s={}
    for treatment in ("fix","rand"):
        for sess in range(6):
            count=(16 if treatment=="rand" or sess<5 else 12)
            people={}
            for i in range(count):
                rounds={}
                for t in range(1,101):
                    own=int((i+t+sess)%7 in (0,1,3))
                    opp=int((i//2+t+2*sess)%5 in (0,2,3))
                    rounds[t]=(own,opp)
                people[f"FICTIONAL_PERSON_{sess}_{i}"]=rounds
            s[(treatment,f"FICTIONAL_SESSION_{sess}")]=people
    return s


def toy_fit():
    return {"train_only_prevalence":.4,
            "state_counts":{
                "M1_OWN_LAST":{(1,):(9,10),(0,):(2,10)},
                "M2_OPPONENT_LAST":{(1,):(9,10),(0,):(2,10)},
                "M3_JOINT_LAST":{(1,0):(8,10),(1,1):(1,10)},
                "M4_JOINT_TWO_LAGS":{(1,0,0,1):(5,6)},
            }}


class HumanMemoryMechanismTests(unittest.TestCase):
    def test_source_synthetic_universe_188_and_12(self):
        z=m.validate_experiment(fictional_sessions())
        self.assertEqual(z["humans"],188)
        self.assertEqual(z["individual_scorable_outcomes"],18424)
        self.assertEqual(z["sessions"],12)

    def test_seven_competing_model_families_frozen(self):
        self.assertEqual(len(m.MODEL_NAMES),7)
        self.assertEqual(len(m.CONDITIONAL_MODELS),4)

    def test_common_98_targets_only_t3_to_t100(self):
        h={t:(int(t%2==0),int(t%3==0)) for t in range(1,101)}
        recs=[m.event_from_history(h,t) for t in range(3,101)]
        self.assertEqual(len(recs),98)
        self.assertEqual(recs[0],(h[2][0],h[2][1],h[1][0],h[1][1],h[3][0]))

    def test_no_future_opponent_action_used(self):
        history={t:(0,0) for t in range(1,101)}
        before=m.event_from_history(history,30)
        history[30]=(1,1)
        after=m.event_from_history(history,30)
        self.assertEqual(before[:4],after[:4])
        self.assertNotEqual(before[4],after[4])

    def test_only_5_other_same_treatment_sessions_training(self):
        s=fictional_sessions()
        fit=m.train_only_other_sessions(s,("fix","FICTIONAL_SESSION_0"))
        self.assertEqual(fit["trained_from_other_sessions_same_treatment"],5)
        self.assertEqual(fit["train_target_count"],(4*16+12)*98)

    def test_full_session_heldout_action_change_no_fit_leak(self):
        s=fictional_sessions()
        heldout=("rand","FICTIONAL_SESSION_0")
        before=m.train_only_other_sessions(s,heldout)
        s[heldout]["FICTIONAL_PERSON_0_0"][100]=(1,1)
        s[heldout]["FICTIONAL_PERSON_0_1"][50]=(0,0)
        self.assertEqual(before,m.train_only_other_sessions(s,heldout))

    def test_training_prevalence_only_own_t3_to_t100(self):
        s=fictional_sessions();held=("fix","FICTIONAL_SESSION_0")
        a=m.train_only_other_sessions(s,held)
        all_train=[m.event_from_history(hist,t)[4]
                   for key,people in s.items() if key[0]=="fix" and key!=held
                   for hist in people.values() for t in range(3,101)]
        self.assertAlmostEqual(a["train_only_prevalence"],sum(all_train)/len(all_train))

    def test_own_last_feature_ignores_opponent(self):
        a=(1,0,0,1,1);b=(1,1,0,0,0)
        self.assertEqual(m.state_for("M1_OWN_LAST",a),m.state_for("M1_OWN_LAST",b))

    def test_opponent_feature_ignores_own(self):
        a=(0,1,1,0,1);b=(1,1,0,1,0)
        self.assertEqual(m.state_for("M2_OPPONENT_LAST",a),m.state_for("M2_OPPONENT_LAST",b))

    def test_joint_second_lag_has_16_possible_states(self):
        from itertools import product
        self.assertEqual(len({m.state_for("M4_JOINT_TWO_LAGS",(*a,0)) for a in product((0,1),repeat=4)}),16)

    def test_smoothing_formula_and_unseen_context_train_prior(self):
        f=toy_fit()
        self.assertAlmostEqual(m.predict("M1_OWN_LAST",(1,0,0,1,0),f),(9+20*.4)/30)
        self.assertAlmostEqual(m.predict("M4_JOINT_TWO_LAGS",(0,1,1,1,0),f),.4)

    def test_tft_only_previous_opponent_not_current(self):
        fit=toy_fit()
        self.assertAlmostEqual(m.predict("M5_TFT_NOISY",(0,1,0,0,0),fit),.95)
        self.assertAlmostEqual(m.predict("M5_TFT_NOISY",(1,0,0,1,1),fit),.05)

    def test_wsls_cc_and_dd_cooperate_cd_dc_defect(self):
        fit=toy_fit()
        for own,opp in ((1,1),(0,0)):
            self.assertAlmostEqual(m.predict("M6_WSLS_NOISY",(own,opp,0,0,1),fit),.95)
        for own,opp in ((1,0),(0,1)):
            self.assertAlmostEqual(m.predict("M6_WSLS_NOISY",(own,opp,0,0,0),fit),.05)

    def test_prediction_does_not_read_outcome_component(self):
        fit=toy_fit()
        for model in m.MODEL_NAMES:
            a=m.predict(model,(1,0,0,1,0),fit)
            b=m.predict(model,(1,0,0,1,1),fit)
            self.assertEqual(a,b)

    def test_likelihood_and_brier_finite_for_extreme_predictions(self):
        for p in (.01,.05,.5,.95,.99):
            for y in (0,1):
                self.assertGreaterEqual(m.brier(y,p),0)
                self.assertTrue(math.isfinite(m.logloss(y,p)))

    def test_bad_heldout_training_partition_rejected(self):
        s=fictional_sessions()
        with self.assertRaisesRegex(ValueError,"PARTITION"):
            m.train_only_other_sessions(s,("fix","NOT_A_REAL_SESSION"))

    def test_missing_round_in_one_person_fails_closed(self):
        s=fictional_sessions()
        s[("fix","FICTIONAL_SESSION_0")]["FICTIONAL_PERSON_0_0"].pop(30)
        with self.assertRaisesRegex(ValueError,"ROUNDS"):
            m.validate_experiment(s)

    def test_missing_session_rejected(self):
        s=fictional_sessions()
        s.pop(("rand","FICTIONAL_SESSION_0"))
        with self.assertRaisesRegex(ValueError,"TWELVE"):
            m.validate_experiment(s)

    def test_binary_source_input_rejected(self):
        for s in ("yes","1","","0"):
            with self.assertRaises(ValueError):
                m.encode_action(s)

    def test_full_synthetic_seven_model_LOSO_and_all_equal_denominators(self):
        out=m.evaluate(fictional_sessions())
        self.assertEqual(set(out["models"]),set(m.MODEL_NAMES))
        for model,info in out["models"].items():
            self.assertEqual(info["individual_test_records"],18424)
            self.assertTrue(0<=info["all_12_sessions_equal_weight_Brier"]<=1)
            self.assertTrue(math.isfinite(info["all_12_sessions_equal_weight_log_loss"]))
        for pair in out["paired_comparisons"].values():
            for sub in pair.values():
                self.assertEqual(sub["sessions"],6)
                self.assertEqual(sub["sessions_better"]+sub["sessions_equal"]+sub["sessions_worse"],6)

    def test_raw_fake_person_and_session_not_leaked_by_metrics(self):
        result=m.evaluate(fictional_sessions())
        self.assertNotIn("FICTIONAL_PERSON",str(result))
        self.assertNotIn("FICTIONAL_SESSION",str(result))

    def test_probability_out_of_bounds_rejected(self):
        with self.assertRaises(ValueError):
            m.predict("M0_TREATMENT_PREVALENCE",(1,0,1,0,0),
                      {"train_only_prevalence":1.0})

    def test_no_future_observations_when_scoring_target_t(self):
        hist={t:(int(t%3==0),int(t%5==0)) for t in range(1,101)}
        event=m.event_from_history(hist,32)
        assert event[:4]==(hist[31][0],hist[31][1],hist[30][0],hist[30][1])


if __name__=="__main__":unittest.main()
