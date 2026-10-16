"""Synthetic-only 12-session human PD LOSO proof and no-label-leak tests."""
import copy
import unittest

from r067_human_ipd_session_loso import (
    REAL_PD,N_ROUNDS,CLASSES,H,L,ETA,
    delta,predict,variants,treatment_prior,fit_on_other_sessions,mse_next,
    evaluate
)


def fake_sessions():
    # Invented 12 sources, no real respondent data.
    return {
        (t,"FAKE_"+str(i)):tuple(
            max(0.0,min(1.0,(.6 if t=="fix" else .3)+.025*((k+i)%7-3)))
            for k in range(100))
        for t in ("fix","rand") for i in range(6)
    }


class HumanIPDLOSOTests(unittest.TestCase):
    def test_real_payoff_difference_constant_negative_one(self):
        for x in (0,.1,.5,.9,1):
            self.assertAlmostEqual(delta(x,REAL_PD),-1,12)

    def test_fixed_prespecified_grid_sizes(self):
        self.assertEqual(len(variants("persistence")),1)
        self.assertEqual(len(variants("replicator")),4)
        self.assertEqual(len(variants("dynamic_logit")),16)
        self.assertEqual(len(variants("best_response")),4)

    def test_replicator_decreases_in_PD_at_interior(self):
        self.assertLess(predict("replicator",.5,{"dt":.1}),.5)

    def test_best_response_strictly_defects(self):
        self.assertAlmostEqual(predict("best_response",.5,{"eta":.2}),.4)

    def test_logit_step_is_not_qre_solver(self):
        x=predict("dynamic_logit",.5,{"lam":2.0,"eta":.2})
        self.assertGreater(x,0)
        self.assertLess(x,.5)

    def test_all_grid_predictions_finite_and_bounded(self):
        for model in CLASSES:
            if model=="train_only_treatment_prevalence":continue
            for _,params in variants(model):
                for x in (0,.3,1):
                    z=predict(model,x,params)
                    self.assertTrue(0<=z<=1)

    def test_treatment_prevalence_uses_only_other_same_treatment_sessions(self):
        series=fake_sessions()
        heldout=("fix","FAKE_0")
        train=[s for s in series if s!=heldout]
        p=treatment_prior(series,train,"fix")
        self.assertGreater(p,.4)
        self.assertLess(p,.8)
        series[heldout]=tuple([0.0]*100)
        self.assertEqual(p,treatment_prior(series,train,"fix"))

    def test_model_fit_unchanged_by_any_heldout_values(self):
        series=fake_sessions()
        heldout=("fix","FAKE_0")
        fit=fit_on_other_sessions(series,heldout,"dynamic_logit")
        series[heldout]=tuple([1.0]*100)
        self.assertEqual(fit,fit_on_other_sessions(series,heldout,"dynamic_logit"))

    def test_full_12_session_within_group_loho(self):
        y=evaluate(fake_sessions())
        self.assertEqual(set(y),set(CLASSES))
        self.assertTrue(all(x["heldout_transitions"]==1188 for x in y.values()))
        self.assertTrue(all(x["heldout_sessions"]==12 for x in y.values()))
        self.assertTrue(all(not x["session_names_or_round_series_exported"] for x in y.values()))
        self.assertNotIn("FAKE_0",str(y))

    def test_session_missing_rejected(self):
        series=fake_sessions()
        series.pop(("rand","FAKE_0"))
        with self.assertRaises(ValueError):
            evaluate(series)

    def test_nonfinite_series_rejected_at_predict_step(self):
        with self.assertRaises(ValueError):
            predict("replicator",float("nan"),{"dt":.1})

    def test_mse_next_fixed_horizon(self):
        series=fake_sessions()
        key=("fix","FAKE_0")
        self.assertGreaterEqual(mse_next(series,key,"persistence",{}),0)


if __name__=="__main__":
    unittest.main()
