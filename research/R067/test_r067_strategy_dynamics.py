"""R067 E1 game dynamics mathematical and numeric fail-closed tests."""
import math
import unittest
from r067_strategy_dynamics import (
    PRISONERS_DILEMMA,COORDINATION,
    best_response_step,logit_response_step,logit_prob_c,replicator_step,
    payoffs,delta,trajectory,benchmark,
)


class StrategyDynamicsTests(unittest.TestCase):
    def test_exact_pd_expected_payoffs(self):
        c,d=payoffs(.5,PRISONERS_DILEMMA)
        self.assertEqual(c,1.5)
        self.assertEqual(d,3.0)
        self.assertEqual(delta(.5,PRISONERS_DILEMMA),-1.5)

    def test_pd_replicator_euler_probe(self):
        self.assertAlmostEqual(replicator_step(.5,PRISONERS_DILEMMA,.1),.4625,12)

    def test_pd_logit_probe(self):
        self.assertAlmostEqual(logit_response_step(.5,PRISONERS_DILEMMA,2,.2),
                               .4+.2/(1+math.exp(3)),12)

    def test_pd_best_response_probe(self):
        self.assertAlmostEqual(best_response_step(.5,PRISONERS_DILEMMA,.2),.4,12)

    def test_coordination_replicator_probe(self):
        self.assertAlmostEqual(replicator_step(.5,COORDINATION,.1),.5125,12)

    def test_coordination_best_response_probe(self):
        self.assertAlmostEqual(best_response_step(.5,COORDINATION,.2),.6,12)

    def test_coordination_indifference_threshold(self):
        self.assertAlmostEqual(delta(3/7,COORDINATION),0,12)
        self.assertLess(delta(.4,COORDINATION),0)
        self.assertGreater(delta(.5,COORDINATION),0)

    def test_logit_lam_zero_targets_half(self):
        self.assertAlmostEqual(logit_response_step(.1,PRISONERS_DILEMMA,0,1),.5,12)

    def test_logit_numerical_stability_tails(self):
        self.assertTrue(0 <= logit_prob_c(-1000,100) <= 1)
        self.assertTrue(0 <= logit_prob_c(1000,100) <= 1)

    def test_best_response_equal_payoffs_stays(self):
        neutral=((1,1),(1,1))
        self.assertEqual(best_response_step(.3,neutral,.2),.3)

    def test_replicator_extinction_and_fixation_absorbing(self):
        self.assertEqual(replicator_step(0,PRISONERS_DILEMMA,.1),0)
        self.assertEqual(replicator_step(1,PRISONERS_DILEMMA,.1),1)

    def test_replicator_euler_invalid_jump_not_clipped(self):
        A=((1000,1000),(0,0))
        with self.assertRaises(ValueError):
            replicator_step(.5,A,1)

    def test_negative_euler_step_rejected(self):
        with self.assertRaises(ValueError):
            replicator_step(.5,COORDINATION,-.01)

    def test_invalid_payoff_matrix_rejected(self):
        with self.assertRaises(ValueError):
            payoffs(.5,((1,2,3),(4,5,6)))

    def test_nonfinite_payoff_rejected(self):
        with self.assertRaises(ValueError):
            payoffs(.5,((1,2),(math.nan,3)))

    def test_probability_out_of_range_rejected(self):
        for x in (-.001,1.001,math.inf,math.nan):
            with self.assertRaises(ValueError):
                payoffs(x,PRISONERS_DILEMMA)

    def test_invalid_logit_lambda_rejected(self):
        with self.assertRaises(ValueError):
            logit_response_step(.5,COORDINATION,-1,.2)

    def test_invalid_behavioral_update_eta_rejected(self):
        with self.assertRaises(ValueError):
            best_response_step(.5,COORDINATION,1.5)

    def test_all_trajectories_within_unit(self):
        for A in (PRISONERS_DILEMMA,COORDINATION):
            for name in ("replicator","logit_response","best_response"):
                y=trajectory(name,.5,A,20)
                self.assertEqual(len(y),21)
                self.assertTrue(all(0<=x<=1 for x in y))

    def test_full_benchmark_has_exact_frozen_readout(self):
        q=benchmark()
        self.assertEqual(q["status"],"E1_MECHANISM_PASS")
        self.assertFalse(q["real_behavioral_experiment_fitted"])
        self.assertTrue(q["not_a_QRE_fixed_point_solution"])

    def test_reject_unrecognized_dynamics(self):
        with self.assertRaises(ValueError):
            trajectory("unrecognized",.5,COORDINATION,1)

    def test_reject_invalid_steps(self):
        for bad in (-1,1.5,1001):
            with self.assertRaises(ValueError):
                trajectory("replicator",.5,COORDINATION,bad)


if __name__=="__main__":
    unittest.main()
