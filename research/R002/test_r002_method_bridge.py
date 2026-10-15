#!/usr/bin/env python3
import unittest
from r002_method_bridge import (expit, make_panel, add_history_features,
    predict, fit, candidates, neglogprob, one_run)

class R002Tests(unittest.TestCase):
    def test_expit(self): self.assertAlmostEqual(expit(0),.5)
    def test_expit_extremes(self):
        self.assertEqual(expit(-1000),0.0)
        self.assertEqual(expit(1000),1.0)
    def test_generation_count(self): self.assertEqual(len(make_panel("M1",11,3,7)),21)
    def test_determinism(self): self.assertEqual(make_panel("M2",11,3,7),make_panel("M2",11,3,7))
    def test_distinct_seed(self): self.assertNotEqual(make_panel("M2",11,3,7),make_panel("M2",12,3,7))
    def test_history_starts_at_half(self):
        r=make_panel("M2",1,2,4)
        self.assertTrue(all(x["h_065"]==.5 for x in r if x["t"]==0))
    def test_history_one_step_lag(self):
        r=make_panel("M2",1,2,4)
        self.assertAlmostEqual(r[1]["h_065"], .65*.5+.35*r[0]["z"])
    def test_no_current_signal_in_delayed_history(self):
        a=make_panel("M2",1,2,4)
        b=[dict(row) for row in a]
        b[1]["z"]=1-b[1]["z"]
        add_history_features(b)
        self.assertEqual(a[1]["h_065"], b[1]["h_065"])
        self.assertNotEqual(a[2]["h_065"], b[2]["h_065"])
    def test_no_y_in_features(self):
        a=make_panel("M2",1,2,4)
        b=[dict(row) for row in a]
        b[0]["y"]=1-b[0]["y"]
        add_history_features(b)
        self.assertEqual([r["h_065"] for r in a],[r["h_065"] for r in b])
    def test_zero_gamma_immediate_equivalence(self):
        r=make_panel("M0",4,3,5)[0]
        self.assertEqual(predict(r,"M0",-.7,.9),predict(r,"M1",-.7,.9,0))
    def test_zero_gamma_delayed_equivalence(self):
        r=make_panel("M2",4,3,5)[2]
        self.assertEqual(predict(r,"M0",-.7,.9),predict(r,"M2",-.7,.9,0,None))
    def test_outcome_in_score(self): self.assertGreater(neglogprob(1,.2),neglogprob(1,.8))
    def test_candidates_nonempty(self): self.assertGreater(len(list(candidates("M2"))),len(list(candidates("M1"))))
    def test_fit_is_grid_member(self):
        r=make_panel("M1",5,10,4)
        self.assertIn(fit(r,"M1"),list(candidates("M1")))
    def test_model_predict_uses_contemporaneous_exposure(self):
        row=make_panel("M1",1,1,2)[0]
        row2=dict(row);row2["z"]=1-row["z"]
        self.assertNotEqual(predict(row,"M1",-.7,.9,2.1),predict(row2,"M1",-.7,.9,2.1))
    def test_delayed_predict_not_affected_current_exposure(self):
        row=make_panel("M2",1,1,2)[0]
        row2=dict(row);row2["z"]=1-row["z"]
        self.assertEqual(predict(row,"M2",-.7,.9,2.1,.65),predict(row2,"M2",-.7,.9,2.1,.65))
    def test_truth_M0_is_tied_or_best(self):
        r=one_run("M0",train_people=180,test_people=80)
        self.assertEqual(r["best_test_logloss"],"M0")
    def test_truth_M1_wins(self):
        r=one_run("M1",train_people=180,test_people=80)
        self.assertEqual(r["best_test_logloss"],"M1")
    def test_truth_M2_wins(self):
        r=one_run("M2",train_people=180,test_people=80)
        self.assertEqual(r["best_test_logloss"],"M2")
    def test_train_test_subject_id_disjoint(self):
        a=make_panel("M2",425,8,3); b=make_panel("M2",984,8,3)
        self.assertFalse({r["person"] for r in a} & {r["person"] for r in b})
    def test_no_fake_claim(self):
        from r002_method_bridge import __doc__
        self.assertIn("NOT",__doc__)

if __name__=="__main__": unittest.main()
