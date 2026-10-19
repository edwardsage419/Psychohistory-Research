"""R112 reproducible mathematical and constructed-data tests, no human data."""
import itertools
import math
import unittest
from r112_bayesian_belief_updating import (
    BetaBernoulli, EvidenceError, binary_likelihood_ratio_prior,
    duplicated_evidence_counterexample, posterior, sequential_posterior,
)

class BayesianMathematicalAudit(unittest.TestCase):
    def test_two_hypothesis_bayes_rule(self):
        self.assertAlmostEqual(posterior((.2,.8),(.9,.1))[0],.18/.26)

    def test_weights_normalized_and_nonnegative(self):
        p=posterior((7,2,1),(.5,.5,.3))
        self.assertAlmostEqual(sum(p),1.)
        self.assertTrue(all(0 <= x <= 1 for x in p))

    def test_zero_prior_support_never_revives(self):
        self.assertEqual(posterior((1.,0.),(.3,1.)),(1.,0.))

    def test_zero_likelihood_eliminates_hypothesis(self):
        self.assertEqual(posterior((.2,.8),(0.,1.)),(0.,1.))

    def test_all_supported_hypotheses_impossible_rejected(self):
        with self.assertRaisesRegex(EvidenceError,"IMPOSSIBLE"):
            posterior((.2,.8),(0.,0.))

    def test_empty_priors_rejected(self):
        with self.assertRaisesRegex(EvidenceError,"EMPTY"):
            posterior([],[])

    def test_invalid_prior_boolean_negative_nan_inf_rejected(self):
        for values in ((True,.5),(-1,2),(float("nan"),1.),
                       (float("inf"),1.),(0.,0.)):
            with self.subTest(values=values),self.assertRaises(EvidenceError):
                posterior(values,(.5,.5))

    def test_likelihood_dimension_and_out_of_range_rejected(self):
        for likelihoods in ((.1,),(-.1,.1),(1.1,.5),(True,.5),
                            (float("nan"),.5),(float("inf"),.5)):
            with self.subTest(likelihoods=likelihoods),self.assertRaises(EvidenceError):
                posterior((.5,.5),likelihoods)

    def test_log_weight_rare_evidence_stable(self):
        p=posterior((.3,.7),(1e-300,2e-300))
        self.assertAlmostEqual(p[0],.3/(.3+1.4))

    def test_uniform_likelihoods_return_same_prior(self):
        prior=(.1,.2,.7)
        for x,y in zip(prior,posterior(prior,(.02,.02,.02))):
            self.assertAlmostEqual(x,y)

    def test_sequential_product_matches_joint_independent_likelihoods(self):
        a=sequential_posterior((.4,.6),((.9,.2),(.3,.8)))
        b=posterior((.4,.6),(.27,.16))
        for x,y in zip(a,b):self.assertAlmostEqual(x,y)

    def test_independent_evidence_order_commutative(self):
        a=sequential_posterior((.6,.4),((.3,.7),(.8,.4)))
        b=sequential_posterior((.6,.4),((.8,.4),(.3,.7)))
        for x,y in zip(a,b):self.assertAlmostEqual(x,y)

    def test_perfect_duplicate_evidence_no_additional_information(self):
        x=duplicated_evidence_counterexample()
        self.assertAlmostEqual(x["first_posterior_H1"],.9)
        self.assertAlmostEqual(x["correct_duplicate_conditioned_H1"],.9)

    def test_duplicate_naive_independence_double_counts(self):
        x=duplicated_evidence_counterexample()
        self.assertAlmostEqual(x["independence_assumed_duplicate_H1"],81/82)
        self.assertGreater(x["independence_assumed_duplicate_H1"],
                           x["correct_duplicate_conditioned_H1"])

    def test_bayes_odds_likelihood_ratio(self):
        r=binary_likelihood_ratio_prior(.25,.6,.2)
        self.assertAlmostEqual(r["Bayes_factor_e"],3.)
        self.assertAlmostEqual(r["posterior_H1"],.5)

    def test_infinite_bayes_factor_boundary(self):
        r=binary_likelihood_ratio_prior(.5,1.,0.)
        self.assertTrue(math.isinf(r["Bayes_factor_e"]))
        self.assertEqual(r["posterior_H1"],1.)

    def test_prior_odds_invalid_rejected(self):
        for prior in (0.,1.,True,float("nan"),-1.):
            with self.subTest(prior=prior),self.assertRaises(EvidenceError):
                binary_likelihood_ratio_prior(prior,.4,.6)

    def test_beta_bernoulli_posterior_counts(self):
        original=BetaBernoulli(2.,3.)
        p=original.update_counts(3,1)
        self.assertEqual(p,BetaBernoulli(5.,4.))
        self.assertEqual(original,BetaBernoulli(2.,3.))

    def test_beta_sequential_matches_batch_and_order(self):
        a=BetaBernoulli(1.,1.)
        for obs in (1,0,1,1,0):
            a=a.update(obs)
        b=BetaBernoulli(1.,1.).update_counts(3,2)
        self.assertEqual(a,b)
        self.assertAlmostEqual(a.predictive_next_one(),4/7)

    def test_beta_one_step_predictive_and_variance(self):
        p=BetaBernoulli(2.,2.)
        self.assertAlmostEqual(p.predictive_next_one(),.5)
        self.assertAlmostEqual(p.predictive_variance_theta(),1/20)

    def test_beta_log_marginal_matches_predictive_chain(self):
        prior=BetaBernoulli(2.,3.)
        data=[1,1,0,1,0]
        current=prior
        lp=0.
        for y in data:
            pred=current.predictive_next_one()
            lp+=math.log(pred if y==1 else 1-pred)
            current=current.update(y)
        self.assertAlmostEqual(lp,prior.log_sequence_marginal(data),places=12)

    def test_beta_exact_small_sequence_marginal_enumeration(self):
        prior=BetaBernoulli(1.,1.)
        for seq in itertools.product((0,1),repeat=3):
            count=sum(seq)
            analytic=math.exp(prior.log_sequence_marginal(seq))
            self.assertAlmostEqual(analytic,
                math.exp(math.lgamma(1+count)+math.lgamma(1+3-count)
                         -math.lgamma(2+3) - math.lgamma(1)
                         -math.lgamma(1) + math.lgamma(2)))

    def test_beta_prior_predictive_empty_sequence_is_one(self):
        self.assertAlmostEqual(BetaBernoulli(3.,4.).log_sequence_marginal([]),0.)

    def test_beta_invalid_shape_parameters_rejected(self):
        for a,b in ((0,1),(-1,3),(2,0),(True,2),(float("nan"),1),
                    (1,float("inf"))):
            with self.subTest(alpha=a,beta=b),self.assertRaises(EvidenceError):
                BetaBernoulli(a,b)

    def test_beta_bad_observation_and_count_rejected(self):
        p=BetaBernoulli(1.,1.)
        for bad in ("1",True,2,-1,.0):
            with self.subTest(obs=bad),self.assertRaises(EvidenceError):
                p.update(bad)
        for successes,failures in ((-1,1),(1,-1),(True,0),(1,.0)):
            with self.subTest(counts=(successes,failures)),self.assertRaises(EvidenceError):
                p.update_counts(successes,failures)
        with self.assertRaises(EvidenceError):
            p.log_sequence_marginal([1,2])

if __name__=="__main__":
    unittest.main()
