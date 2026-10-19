"""R115 exact rational original-equation reconstruction; no original human records."""
import unittest
from fractions import Fraction as F

import r115_bhw_1992_informational_action_cascade_exact as m

P = F(7,10)
HALF = F(1,2)


class ExactInformationalActionCascade(unittest.TestCase):
    def test_original_initial_prior(self):
        self.assertEqual(m.trace_public_actions((), P)[0], (HALF,))

    def test_published_signal_condition_good_state(self):
        self.assertEqual(m.likelihood_private_signal(1,1,P),P)
        self.assertEqual(m.likelihood_private_signal(0,1,P),1-P)

    def test_published_signal_condition_bad_state(self):
        self.assertEqual(m.likelihood_private_signal(0,0,P),P)
        self.assertEqual(m.likelihood_private_signal(1,0,P),1-P)

    def test_initial_signal_high_is_posterior_p(self):
        self.assertEqual(m.posterior_after_private_signal(HALF,1,P),P)

    def test_initial_signal_low_is_posterior_one_minus_p(self):
        self.assertEqual(m.posterior_after_private_signal(HALF,0,P),1-P)

    def test_first_agent_action_follows_private_signal(self):
        self.assertEqual(m.adopt_probability_given_signal(HALF,1,P),1)
        self.assertEqual(m.adopt_probability_given_signal(HALF,0,P),0)

    def test_agent_two_low_signal_after_one_adopter_is_true_tie(self):
        self.assertEqual(m.adopt_probability_given_signal(P,0,P),HALF)

    def test_agent_two_high_signal_after_one_adopter_adopts(self):
        self.assertEqual(m.adopt_probability_given_signal(P,1,P),1)

    def test_action_likelihood_first_adoption_matches_signal_likelihood(self):
        self.assertEqual(m.action_likelihoods(HALF,1,P),(P,1-P))

    def test_action_likelihood_for_second_adoption_marginalizes_coin(self):
        self.assertEqual(m.action_likelihoods(P,1,P),(F(17,20),F(13,20)))

    def test_action_likelihood_for_second_rejection_marginalizes_coin(self):
        self.assertEqual(m.action_likelihoods(P,0,P),(F(3,20),F(7,20)))

    def test_first_public_adoption_prior_seven_tenths(self):
        self.assertEqual(m.bayes_public_action_update(HALF,1,P)[0],P)

    def test_first_public_rejection_prior_three_tenths(self):
        self.assertEqual(m.bayes_public_action_update(HALF,0,P)[0],1-P)

    def test_second_public_adoption_exact_one_hundred_nineteen_over_one_fifty_eight(self):
        x=m.trace_public_actions((1,1),P)[0]
        self.assertEqual(x,(HALF,P,F(119,158)))

    def test_closed_form_matches_sequential_action_bayes(self):
        self.assertEqual(m.first_two_identical_adoption_posterior(P),F(119,158))

    def test_naive_repeated_action_as_signal_is_misleading(self):
        naive=m.naive_two_actions_as_two_independent_high_signals(P)
        exact=m.first_two_identical_adoption_posterior(P)
        self.assertEqual(naive,F(49,58))
        self.assertGreater(naive,exact)

    def test_first_two_rejections_mirror_up_cascade(self):
        posterior=m.trace_public_actions((0,0),P)[0][-1]
        self.assertEqual(posterior,F(39,158))
        self.assertEqual(posterior,1-F(119,158))

    def test_first_two_opposite_actions_reset_public_prior(self):
        for actions in ((1,0),(0,1)):
            with self.subTest(actions=actions):
                self.assertEqual(m.trace_public_actions(actions,P)[0][-1],HALF)

    def test_after_opposite_actions_third_signal_matters(self):
        self.assertIsNone(m.cascade_action(HALF,P))
        self.assertEqual(m.adopt_probability_given_signal(HALF,0,P),0)
        self.assertEqual(m.adopt_probability_given_signal(HALF,1,P),1)

    def test_after_two_adoptions_cascade_forces_adopt_even_low_signal(self):
        belief=F(119,158)
        self.assertEqual(m.adopt_probability_given_signal(belief,0,P),1)
        self.assertEqual(m.adopt_probability_given_signal(belief,1,P),1)
        self.assertEqual(m.cascade_action(belief,P),1)

    def test_after_two_rejections_cascade_forces_reject_even_high_signal(self):
        belief=F(39,158)
        self.assertEqual(m.adopt_probability_given_signal(belief,0,P),0)
        self.assertEqual(m.adopt_probability_given_signal(belief,1,P),0)
        self.assertEqual(m.cascade_action(belief,P),0)

    def test_third_action_cascade_probability_one_given_either_hidden_state(self):
        self.assertEqual(m.action_likelihoods(F(119,158),1,P),(1,1))

    def test_third_adoption_in_cascade_provides_zero_new_information(self):
        progression=m.trace_public_actions((1,1,1),P)[0]
        self.assertEqual(progression[-1],progression[-2])

    def test_fourth_fifth_adoption_in_cascade_provide_zero_new_information(self):
        history=m.trace_public_actions((1,1,1,1,1),P)[0]
        self.assertTrue(all(x==F(119,158) for x in history[2:]))

    def test_impossible_counter_action_under_up_cascade_rejected(self):
        with self.assertRaisesRegex(m.CascadeEvidenceError,"IMPOSSIBLE"):
            m.trace_public_actions((1,1,0),P)

    def test_impossible_counter_action_under_down_cascade_rejected(self):
        with self.assertRaisesRegex(m.CascadeEvidenceError,"IMPOSSIBLE"):
            m.trace_public_actions((0,0,1),P)

    def test_first_two_adopters_conditional_good_state_matches_original_derivation(self):
        self.assertEqual(m.history_likelihood_given_state((1,1),1,P),F(119,200))

    def test_first_two_adopters_conditional_bad_state_wrong_cascade_nonzero(self):
        self.assertEqual(m.history_likelihood_given_state((1,1),0,P),F(39,200))

    def test_first_two_rejections_bad_state_correct_down_probability(self):
        self.assertEqual(m.history_likelihood_given_state((0,0),0,P),F(119,200))

    def test_first_two_rejections_good_state_wrong_down_probability(self):
        self.assertEqual(m.history_likelihood_given_state((0,0),1,P),F(39,200))

    def test_all_public_action_histories_n0_normalize_exactly(self):
        self.assertEqual(m.enumerate_public_histories(0,P),{(): (HALF,F(1))})

    def test_all_public_action_histories_n2_normalize_exactly(self):
        histories=m.enumerate_public_histories(2,P)
        self.assertEqual(len(histories),4)
        self.assertEqual(sum((v[1] for v in histories.values()),F(0)),1)

    def test_first_two_up_and_down_each_seventy_nine_over_two_hundred(self):
        x=m.ex_ante_cascade_masses_after_n(2,P)
        self.assertEqual(x["up_cascade"],F(79,200))
        self.assertEqual(x["down_cascade"],F(79,200))

    def test_first_two_no_cascade_twenty_one_percent(self):
        self.assertEqual(m.ex_ante_cascade_masses_after_n(2,P)["no_cascade"],F(21,100))

    def test_first_four_original_author_equation_one(self):
        self.assertEqual(m.ex_ante_cascade_masses_after_n(4,P),m.author_equation_1_even_n(4,P))
        self.assertEqual(m.ex_ante_cascade_masses_after_n(4,P)["no_cascade"],F(441,10000))

    def test_first_six_original_author_equation_one(self):
        self.assertEqual(m.ex_ante_cascade_masses_after_n(6,P),m.author_equation_1_even_n(6,P))
        self.assertEqual(m.ex_ante_cascade_masses_after_n(6,P)["no_cascade"],F(9261,1000000))

    def test_first_two_author_equation_one(self):
        self.assertEqual(m.ex_ante_cascade_masses_after_n(2,P),m.author_equation_1_even_n(2,P))

    def test_other_signal_reliability_three_fifths_author_formula(self):
        p=F(3,5)
        for n in (2,4,6):
            with self.subTest(n=n):
                self.assertEqual(m.ex_ante_cascade_masses_after_n(n,p),m.author_equation_1_even_n(n,p))

    def test_other_signal_reliability_four_fifths_author_formula(self):
        p=F(4,5)
        for n in (2,4,6):
            with self.subTest(n=n):
                self.assertEqual(m.ex_ante_cascade_masses_after_n(n,p),m.author_equation_1_even_n(n,p))

    def test_all_histories_n6_probability_one_and_no_observation_missing(self):
        states=m.enumerate_public_histories(6,P)
        self.assertEqual(sum((x[1] for x in states.values()),F(0)),F(1))
        self.assertTrue(states)

    def test_source_even_n_formula_refuses_odd_or_zero(self):
        for n in (0,1,3,5,7,13,True):
            with self.subTest(n=n),self.assertRaises(m.CascadeEvidenceError):
                m.author_equation_1_even_n(n,P)

    def test_history_length_refuses_oversized_and_non_integer(self):
        for n in (-1,13,True,1.,None):
            with self.subTest(n=n),self.assertRaises(m.CascadeEvidenceError):
                m.enumerate_public_histories(n,P)

    def test_hidden_state_and_signal_refuse_boolean_or_nonbinary(self):
        for bad in (True,False,2,-1,"1",1.0):
            with self.subTest(bad=bad),self.assertRaises(m.CascadeEvidenceError):
                m.likelihood_private_signal(bad,1,P)

    def test_observed_action_refuses_boolean_text_and_nonbinary(self):
        for bad in (True,False,2,-1,"1",1.):
            with self.subTest(bad=bad),self.assertRaises(m.CascadeEvidenceError):
                m.bayes_public_action_update(HALF,bad,P)

    def test_reliability_must_be_strictly_informative_fraction(self):
        for bad in (0,.7,F(1,2),F(1),F(0),True,F(11,10)):
            with self.subTest(bad=bad),self.assertRaises(m.CascadeEvidenceError):
                m.trace_public_actions((1,),bad)

    def test_public_prior_must_be_strictly_interior_fraction(self):
        for bad in (0,1,F(0),F(1),.5,True,F(-1,2)):
            with self.subTest(bad=bad),self.assertRaises(m.CascadeEvidenceError):
                m.posterior_after_private_signal(bad,1,P)

    def test_receipt_never_claims_independent_human_reproduction(self):
        x=m.diagnostic_exact_receipt()
        self.assertTrue(x["synthetic_mathematical_replication_only"])
        self.assertEqual(x["original_human_E2_records"],0)
        self.assertEqual(x["correct_analytical_after_two"],"119/158")
        self.assertEqual(x["posterior_after_actions_1_1"],"119/158")
        self.assertEqual(x["after_third_cascade_action_posterior"],"119/158")
        self.assertEqual(x["PESEN_v0_1"],"FROZEN")
        self.assertEqual(x["R073"],"FROZEN")

    def test_diagnostic_receipt_reproducibly_identical(self):
        self.assertEqual(m.diagnostic_exact_receipt(),m.diagnostic_exact_receipt())


if __name__ == "__main__":
    unittest.main()
