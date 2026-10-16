"""Finite mechanistic/algebraic tests; synthetic E1, never empirical E2."""
import math
import unittest

from r066_three_opinion_models import (
    REFERENCE_W, REFERENCE_X, benchmark, degroot_step, fj_step, hk_step,
    simulate, validate_opinions, validate_weights,
)


class OpinionDynamicsTests(unittest.TestCase):
    def assertVecAlmostEqual(self, x, expected):
        self.assertEqual(len(x),len(expected))
        for a,b in zip(x,expected):
            self.assertAlmostEqual(a,b,places=12)

    def test_reference_benchmark_all_models(self):
        b=benchmark()
        self.assertEqual(b["status"],"SYNTHETIC_MECHANISM_PASS")
        self.assertVecAlmostEqual(b["results"]["degroot"][1],[.4,.4,.4])
        self.assertVecAlmostEqual(b["results"]["fj"][1],[.2,.3,.7])
        self.assertVecAlmostEqual(b["results"]["hk"][1],[.1,.1,1.0])

    def test_uniform_degroot_consensus(self):
        self.assertVecAlmostEqual(degroot_step(REFERENCE_X,REFERENCE_W),[.4]*3)

    def test_degroot_identity_stays_fixed(self):
        W=((1,0,0),(0,1,0),(0,0,1))
        self.assertVecAlmostEqual(degroot_step(REFERENCE_X,W),REFERENCE_X)

    def test_degroot_not_every_network_consensus(self):
        W=((1,0,0),(0,1,0),(0,0,1))
        self.assertNotEqual(len(set(degroot_step(REFERENCE_X,W))),1)

    def test_fj_unit_susceptibility_equals_degroot(self):
        self.assertVecAlmostEqual(
            fj_step(REFERENCE_X,REFERENCE_X,REFERENCE_W,(1,1,1)),
            degroot_step(REFERENCE_X,REFERENCE_W))

    def test_fj_zero_susceptibility_fixed_initial(self):
        self.assertVecAlmostEqual(
            fj_step((.4,.4,.4),REFERENCE_X,REFERENCE_W,(0,0,0)),
            REFERENCE_X)

    def test_fj_half_susceptibility_at_fixed_point(self):
        first=fj_step(REFERENCE_X,REFERENCE_X,REFERENCE_W,(.5,)*3)
        second=fj_step(first,REFERENCE_X,REFERENCE_W,(.5,)*3)
        self.assertVecAlmostEqual(first,(.2,.3,.7))
        self.assertVecAlmostEqual(second,first)

    def test_hk_small_confidence_two_clusters(self):
        self.assertVecAlmostEqual(hk_step(REFERENCE_X,.25),(.1,.1,1))
        self.assertVecAlmostEqual(hk_step((.1,.1,1),.25),(.1,.1,1))

    def test_hk_full_confidence_equals_uniform_degroot(self):
        self.assertVecAlmostEqual(hk_step(REFERENCE_X,1.0),
                                  degroot_step(REFERENCE_X,REFERENCE_W))

    def test_hk_zero_radius_distinct_unchanged(self):
        self.assertVecAlmostEqual(hk_step(REFERENCE_X,0),REFERENCE_X)

    def test_hk_synchronous_uses_old_vector(self):
        self.assertVecAlmostEqual(hk_step((0,.4,.8),.4),(.2,.4,.6))

    def test_no_unjustified_weight_rescaling(self):
        W=((1,1,0),(0,1,0),(0,0,1))
        with self.assertRaises(ValueError):
            degroot_step(REFERENCE_X,W)

    def test_no_negative_weight(self):
        W=((-1,2,0),(0,1,0),(0,0,1))
        with self.assertRaises(ValueError):
            validate_weights(W,3)

    def test_no_wrong_matrix_shape(self):
        with self.assertRaises(ValueError):
            degroot_step((.3,.4),((1,0,0),(0,1,0)))

    def test_no_nonfinite_opinion(self):
        for bad in (float('nan'),float('inf'),float('-inf')):
            with self.assertRaises(ValueError):
                validate_opinions((0.0,bad))

    def test_empty_agent_rejected(self):
        with self.assertRaises(ValueError):
            validate_opinions(())

    def test_reject_opinion_beyond_unit_interval(self):
        with self.assertRaises(ValueError):
            validate_opinions((.5,1.1))

    def test_reject_alpha_not_in_unit_interval(self):
        with self.assertRaises(ValueError):
            fj_step(REFERENCE_X,REFERENCE_X,REFERENCE_W,(.5,1.01,.5))

    def test_reject_alpha_wrong_length(self):
        with self.assertRaises(ValueError):
            fj_step(REFERENCE_X,REFERENCE_X,REFERENCE_W,(.5,.5))

    def test_reject_invalid_hk_radius(self):
        for bad in (-.1,1.1,math.inf,math.nan):
            with self.assertRaises(ValueError):
                hk_step(REFERENCE_X,bad)

    def test_state_bounds_in_all_three_models(self):
        for name,kw in (("degroot",{"W":REFERENCE_W}),
                        ("fj",{"W":REFERENCE_W,"alpha":(.5,)*3}),
                        ("hk",{"epsilon":.25})):
            h=simulate(name,REFERENCE_X,20,**kw)
            self.assertEqual(len(h),21)
            self.assertTrue(all(0<=v<=1 for state in h for v in state))

    def test_invalid_model_fails(self):
        with self.assertRaises(ValueError):
            simulate("unknown",REFERENCE_X,2)

    def test_negative_steps_fail(self):
        with self.assertRaises(ValueError):
            simulate("degroot",REFERENCE_X,-1,W=REFERENCE_W)

    def test_return_history_includes_initial_state(self):
        h=simulate("degroot",REFERENCE_X,0,W=REFERENCE_W)
        self.assertEqual(h,[list(REFERENCE_X)])

    def test_degenerate_fj_equals_degroot_over_multiple_times(self):
        a=simulate("degroot",REFERENCE_X,3,W=REFERENCE_W)
        b=simulate("fj",REFERENCE_X,3,W=REFERENCE_W,alpha=(1,1,1))
        for x,y in zip(a,b):
            self.assertVecAlmostEqual(x,y)


if __name__=="__main__":
    unittest.main()
