"""R111 source-independent analytic identities and finite Monte Carlo checks."""
import math
import unittest
import r111_mcfadden_random_utility_conditional_logit as r

class ConditionalLogitPureMath(unittest.TestCase):
    def test_uniform_equal_utility(self):
        self.assertEqual(r.probabilities([0,0,0]),[1/3]*3)
    def test_probabilities_sum_to_one_and_nonnegative(self):
        p=r.probabilities([-9000,0,8000])
        self.assertAlmostEqual(sum(p),1)
        self.assertTrue(all(0<=v<=1 for v in p))
    def test_shift_invariance_normalization(self):
        a=r.probabilities([0,1,-2])
        b=r.probabilities([1000,1001,998])
        for x,y in zip(a,b):self.assertAlmostEqual(x,y,places=12)
    def test_joint_utility_and_scale_unidentifiable(self):
        a=r.probabilities([-3,2,5],scale=0.7)
        b=r.probabilities([-30,20,50],scale=7)
        for x,y in zip(a,b):self.assertAlmostEqual(x,y,places=12)
    def test_choice_set_availability_is_not_missing_at_random(self):
        p=r.probabilities([0,1,2],available=[True,False,True])
        self.assertEqual(p[1],0)
        self.assertAlmostEqual(p[0]+p[2],1)
    def test_iia_odds_independent_of_third_utility(self):
        a=r.probabilities([0,0.5,0])
        b=r.probabilities([0,0.5,5])
        self.assertAlmostEqual(a[1]/a[0],b[1]/b[0])
        self.assertAlmostEqual(a[1]/a[0],math.exp(0.5))
    def test_red_bus_blue_bus_limitation_exact(self):
        x=r.red_bus_blue_bus_counterexample()
        self.assertAlmostEqual(x["before_car"],2/3)
        self.assertAlmostEqual(x["after_car"],1/2)
        self.assertAlmostEqual(x["after_red_bus"],1/4)
        self.assertAlmostEqual(x["after_blue_bus"],1/4)
    def test_temperature_limits(self):
        self.assertGreater(r.probabilities([0,1],scale=0.01)[1],0.999)
        self.assertAlmostEqual(r.probabilities([0,1],scale=1000000)[1],0.5,places=5)
    def test_finite_derivative_against_theory(self):
        u=[-0.2,0.5,1.0];h=1e-6
        p=r.probabilities(u,0.9)
        vv=u.copy();vv[1]+=h
        qq=r.probabilities(vv,0.9)
        self.assertAlmostEqual((qq[1]-p[1])/h,p[1]*(1-p[1])/0.9,places=5)
    def test_features_linear_theta(self):
        p=r.conditional_logit([[0,1],[1,0]],[2,3])
        q=r.probabilities([3,2])
        self.assertEqual(p,q)
    def test_nll_one_choice_matches_log_probability(self):
        x=[([[-1],[0],[2]],2,[True,True,True])]
        p=r.probabilities([-1,0,2])
        self.assertAlmostEqual(r.negative_log_likelihood(x,[1]),-math.log(p[2]))
    def test_nll_extremely_rare_available_choice_no_underflow(self):
        x=[([[0],[-10000]],1,[True,True])]
        self.assertAlmostEqual(r.negative_log_likelihood(x,[1]),10000)
    def test_gumbel_independent_mc_matches_theory_within_sample_error(self):
        p=r.probabilities([0,0.6,-0.5],scale=0.8)
        mc=r.iid_gumbel_mc_probabilities([0,0.6,-0.5],scale=0.8,draws=20000,seed=111)
        for a,b in zip(mc,p):self.assertLess(abs(a-b),0.016)
    def test_extreme_cases_rejected(self):
        bad=[
            ([],1,None),([1,2],0,None),([1,2],float("nan"),None),
            ([1,float("inf")],1,None),([1],1,[False]),
            ([1,2],1,[True]),([1,2],1,[1,1])
        ]
        for v,s,m in bad:
            with self.subTest(v=v,s=s,m=m),self.assertRaises(ValueError):
                r.probabilities(v,s,m)
    def test_observed_chosen_unavailable_rejected(self):
        with self.assertRaises(ValueError):
            r.negative_log_likelihood([([[1],[2]],1,[True,False])],[1])
    def test_empty_observations_or_feature_mismatch_rejected(self):
        with self.assertRaises(ValueError):r.negative_log_likelihood([],[1])
        with self.assertRaises(ValueError):r.conditional_logit([[1,2]],[1])
    def test_monotonic_utility_and_logit_choice(self):
        p=r.probabilities([0,1,2])
        self.assertTrue(p[0]<p[1]<p[2])
    def test_deterministic_monte_carlo_replay(self):
        a=r.iid_gumbel_mc_probabilities([0,2],draws=100,seed=5)
        b=r.iid_gumbel_mc_probabilities([0,2],draws=100,seed=5)
        self.assertEqual(a,b)

if __name__=="__main__":
    unittest.main()
