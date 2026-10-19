"""R116 exact rational toy counterexamples only; no real participant records."""
import unittest
from fractions import Fraction as F
from dataclasses import FrozenInstanceError
import r116_normative_public_status_vs_informational_cue_exact as m

P=F(3,5); STRONG=F(3,4); WEAK=F(11,20); STATUS=F(1,4)

class NormativeVsInformation(unittest.TestCase):
    def test_initial_private_low_signal_exact_two_fifths(self):
        self.assertEqual(m.binary_signal_posterior(0,P),F(2,5))

    def test_initial_private_high_signal_exact_three_fifths(self):
        self.assertEqual(m.binary_signal_posterior(1,P),F(3,5))

    def test_private_complementarity(self):
        for p in (F(3,5),F(2,3),F(9,10)):
            self.assertEqual(m.binary_signal_posterior(0,p)+m.binary_signal_posterior(1,p),1)

    def test_strong_one_cue_posterior_exact_two_thirds(self):
        self.assertEqual(m.single_independent_cue_update(F(2,5),1,STRONG),F(2,3))

    def test_weak_one_cue_posterior_exact_twenty_two_forty_ninths(self):
        self.assertEqual(m.single_independent_cue_update(F(2,5),1,WEAK),F(22,49))

    def test_cue_zero_against_high_private_signal_mirror(self):
        self.assertEqual(m.single_independent_cue_update(F(3,5),0,STRONG),F(1,3))

    def test_strong_cue_shifts_belief_up(self):
        self.assertGreater(m.single_independent_cue_update(F(2,5),1,STRONG),F(2,5))

    def test_weak_cue_does_not_fully_overrule_private_signal(self):
        self.assertLess(m.single_independent_cue_update(F(2,5),1,WEAK),F(1,2))

    def test_bayesian_single_cue_symmetry(self):
        x=m.single_independent_cue_update(F(2,5),1,STRONG)
        y=m.single_independent_cue_update(F(3,5),0,STRONG)
        self.assertEqual(x+y,1)

    def test_single_cue_not_multiplied_by_number_of_public_actors(self):
        self.assertEqual(m.single_independent_cue_update(F(2,5),1,STRONG),F(2,3))
        self.assertNotEqual(m.single_independent_cue_update(F(2,3),1,STRONG),F(2,3))

    def test_status_choice_mechanism_is_immutable(self):
        with self.assertRaises(FrozenInstanceError):
            m.MODELS["NORMATIVE_ONLY"].public_dissent_cost=F(1,2)

    def test_frozen_four_status_models(self):
        self.assertEqual(set(m.MODELS),{"NO_INFLUENCE","NORMATIVE_ONLY","INFORMATIONAL_ONLY","BOTH"})
        self.assertEqual(m.MODELS["NORMATIVE_ONLY"],m.ToyMechanism(False,STATUS))
        self.assertEqual(m.MODELS["INFORMATIONAL_ONLY"],m.ToyMechanism(True,F(0)))

    def test_factorial_cell_names_frozen(self):
        self.assertEqual(m.CELLS,("C0_ANON","C0_PUBLIC","C1_ANON","C1_PUBLIC"))

    def test_no_influence_strong_cue_all_choose_private(self):
        self.assertEqual(tuple(m.factorial_choices(m.MODELS["NO_INFLUENCE"]).values()),(0,0,0,0))

    def test_normative_only_strong_cue_public_switches(self):
        self.assertEqual(tuple(m.factorial_choices(m.MODELS["NORMATIVE_ONLY"]).values()),(0,0,0,1))

    def test_informational_only_strong_cue_private_and_public_switch(self):
        self.assertEqual(tuple(m.factorial_choices(m.MODELS["INFORMATIONAL_ONLY"]).values()),(0,0,1,1))

    def test_both_strong_cue_private_and_public_switch(self):
        self.assertEqual(tuple(m.factorial_choices(m.MODELS["BOTH"]).values()),(0,0,1,1))

    def test_strong_cue_informational_and_both_actions_observationally_equal(self):
        self.assertEqual(m.factorial_choices(m.MODELS["INFORMATIONAL_ONLY"]),
                         m.factorial_choices(m.MODELS["BOTH"]))

    def test_normative_and_information_same_public_action_different_beliefs(self):
        norm=m.trial(m.MODELS["NORMATIVE_ONLY"])
        info=m.trial(m.MODELS["INFORMATIONAL_ONLY"])
        self.assertEqual(norm["choice"],info["choice"])
        self.assertEqual(norm["choice"],1)
        self.assertEqual(norm["belief_V1"],F(2,5))
        self.assertEqual(info["belief_V1"],F(2,3))

    def test_public_status_does_not_update_private_posterior(self):
        norm_private=m.trial(m.MODELS["NORMATIVE_ONLY"],response_public=False)
        norm_public=m.trial(m.MODELS["NORMATIVE_ONLY"],response_public=True)
        self.assertEqual(norm_private["belief_V1"],norm_public["belief_V1"])

    def test_public_vs_private_same_information_identical_belief(self):
        for name,model in m.MODELS.items():
            with self.subTest(name=name):
                private=m.trial(model,response_public=False)
                public=m.trial(model,response_public=True)
                self.assertEqual(private["belief_V1"],public["belief_V1"])

    def test_no_cue_public_status_penalty_disabled(self):
        for name,model in m.MODELS.items():
            with self.subTest(name=name):
                no_cue=m.trial(model,cue_exposed=False,response_public=True)
                self.assertEqual(no_cue["belief_V1"],F(2,5))
                self.assertEqual(no_cue["choice"],0)

    def test_private_answer_status_penalty_disabled(self):
        x=m.trial(m.MODELS["NORMATIVE_ONLY"],response_public=False)
        self.assertEqual(x["payoff_action0"],F(3,5))
        self.assertEqual(x["payoff_action1"],F(2,5))
        self.assertEqual(x["choice"],0)

    def test_public_normative_status_penalty_applied(self):
        x=m.trial(m.MODELS["NORMATIVE_ONLY"])
        self.assertEqual(x["payoff_action0"],F(3,5)-STATUS)
        self.assertEqual(x["payoff_action1"],F(2,5))
        self.assertEqual(x["choice"],1)

    def test_exact_normative_flip_threshold_one_fifth(self):
        self.assertEqual(m.public_conformity_threshold(),F(1,5))

    def test_public_cost_below_threshold_keeps_independent_action(self):
        toy=m.ToyMechanism(False,F(19,100))
        self.assertEqual(m.trial(toy)["choice"],0)

    def test_public_cost_exactly_threshold_tie_keeps_action_zero(self):
        toy=m.ToyMechanism(False,F(1,5))
        self.assertEqual(m.trial(toy)["payoff_action0"],m.trial(toy)["payoff_action1"])
        self.assertEqual(m.trial(toy)["choice"],0)

    def test_public_cost_above_threshold_switches_to_group_action(self):
        toy=m.ToyMechanism(False,F(21,100))
        self.assertEqual(m.trial(toy)["choice"],1)

    def test_group_report_zero_dissent_penalty_applied_only_to_action_one(self):
        toy=m.ToyMechanism(False,F(1,4))
        x=m.trial(toy,private_signal=1,group_cue=0)
        self.assertEqual(x["payoff_action1"],F(3,5)-STATUS)
        self.assertEqual(x["payoff_action0"],F(2,5))
        self.assertEqual(x["choice"],0)

    def test_informational_only_weak_cue_does_not_switch_public_action(self):
        x=m.trial(m.MODELS["INFORMATIONAL_ONLY"],group_accuracy=WEAK)
        self.assertEqual(x["belief_V1"],F(22,49))
        self.assertEqual(x["choice"],0)

    def test_both_weak_cue_switches_only_public_action(self):
        model=m.MODELS["BOTH"]
        self.assertEqual(m.trial(model,response_public=False,group_accuracy=WEAK)["choice"],0)
        self.assertEqual(m.trial(model,response_public=True,group_accuracy=WEAK)["choice"],1)

    def test_both_weak_cue_public_agreement_does_not_mean_belief_over_half(self):
        x=m.trial(m.MODELS["BOTH"],group_accuracy=WEAK)
        self.assertEqual(x["choice"],1)
        self.assertLess(x["belief_V1"],F(1,2))

    def test_weak_information_and_both_factorial_distinct(self):
        self.assertNotEqual(m.factorial_choices(m.MODELS["INFORMATIONAL_ONLY"],group_accuracy=WEAK),
                            m.factorial_choices(m.MODELS["BOTH"],group_accuracy=WEAK))

    def test_status_model_weak_cue_same_status_pattern(self):
        self.assertEqual(m.factorial_choices(m.MODELS["NORMATIVE_ONLY"],group_accuracy=WEAK),
                         {"C0_ANON":0,"C0_PUBLIC":0,"C1_ANON":0,"C1_PUBLIC":1})

    def test_status_zero_infomodel_strong_has_no_public_additional_effect(self):
        info=m.MODELS["INFORMATIONAL_ONLY"]
        self.assertEqual(m.trial(info,response_public=True)["payoff_action1"],
                         m.trial(info,response_public=False)["payoff_action1"])

    def test_bad_signal_values_fail_closed(self):
        for bad in (True,False,-1,2,"0",0.0,1.0,None):
            with self.subTest(bad=bad),self.assertRaises(m.NormativeDesignError):
                m.binary_signal_posterior(bad,P)

    def test_bad_group_cue_values_fail_closed(self):
        for bad in (True,False,2,-1,1.0,"1",None):
            with self.subTest(bad=bad),self.assertRaises(m.NormativeDesignError):
                m.trial(m.MODELS["NORMATIVE_ONLY"],group_cue=bad)

    def test_reliability_rejects_floats_bool_and_closed_bounds(self):
        for bad in (.6,True,F(1,2),F(1),F(0),F(2)):
            with self.subTest(bad=bad),self.assertRaises(m.NormativeDesignError):
                m.binary_signal_posterior(0,bad)
            with self.subTest(bad=bad),self.assertRaises(m.NormativeDesignError):
                m.trial(m.MODELS["BOTH"],group_accuracy=bad)

    def test_belief_prior_requires_interior_exact_fraction(self):
        for bad in (0,1,F(0),F(1),.5,True,F(-1,2)):
            with self.subTest(bad=bad),self.assertRaises(m.NormativeDesignError):
                m.single_independent_cue_update(bad,1,STRONG)

    def test_status_cost_rejects_negative_float_and_bool(self):
        for bad in (-F(1,4),0.25,0,True,None):
            with self.subTest(bad=bad),self.assertRaises(m.NormativeDesignError):
                m.ToyMechanism(False,bad)

    def test_design_flags_reject_nonboolean(self):
        for bad in (0,1,"True",F(1),None):
            with self.subTest(bad=bad),self.assertRaises(m.NormativeDesignError):
                m.trial(m.MODELS["BOTH"],response_public=bad)
            with self.subTest(bad=bad),self.assertRaises(m.NormativeDesignError):
                m.trial(m.MODELS["BOTH"],cue_exposed=bad)

    def test_toy_model_must_be_real_instance(self):
        with self.assertRaises(m.NormativeDesignError):
            m.trial({},cue_exposed=True)
        with self.assertRaises(m.NormativeDesignError):
            m.factorial_choices("NORMATIVE_ONLY")

    def test_independence_flag_rejects_int_coercion(self):
        with self.assertRaises(m.NormativeDesignError):
            m.ToyMechanism(1,STATUS)

    def test_receipt_firstparty_identifiers(self):
        x=m.study_receipt()
        self.assertEqual(x["sources"]["Bernheim_1994"],"10.1086/261957")
        self.assertEqual(x["sources"]["Asch_1955"],"10.1038/scientificamerican1155-31")

    def test_receipt_exact_belief_and_observation_equivalence(self):
        x=m.study_receipt()
        self.assertEqual(x["strong_cue_normative_private_belief_V1"],"2/5")
        self.assertEqual(x["strong_cue_informational_private_belief_V1"],"2/3")
        self.assertTrue(x["strong_cue_both_vs_informational_grid_indistinguishable"])

    def test_receipt_exact_weak_cue_distinguishes_only_under_toy(self):
        x=m.study_receipt()
        self.assertTrue(x["weak_cue_public_actions_identify_extra_status_only_under_frozen_toy_assumptions"])
        self.assertTrue(x["unobserved_private_state_and_social_motive_not_identified_from_single_public_choice"])

    def test_receipt_no_author_equilibrium_or_real_human_replication(self):
        x=m.study_receipt()
        self.assertFalse(x["fitted_Bernheim_1994_game_equilibrium"])
        self.assertFalse(x["original_1955_individual_observations_reanalyzed"])
        self.assertEqual(x["original_human_E2_evaluations"],0)
        self.assertEqual(x["PESEN_v0_1"],"FROZEN")

    def test_fixed_reproducibility(self):
        self.assertEqual(m.study_receipt(),m.study_receipt())


if __name__ == "__main__":
    unittest.main()
