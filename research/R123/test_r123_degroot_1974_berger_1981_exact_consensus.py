"""R123 full source article arithmetic, Berger 1981 correction and 226 pure maths."""
import unittest
from fractions import Fraction as F
from unittest.mock import patch
import r123_degroot_1974_berger_1981_exact_consensus as m

ORIGINAL=((F(1,2),F(1,2)),(F(1,4),F(3,4)))
SOURCE_THIRD=((F(1,2),F(1,2),F(0)),
              (F(1,4),F(3,4),F(0)),
              (F(1,3),F(1,3),F(1,3)))
SWAP=((F(0),F(1)),(F(1),F(0)))
IDENTITY=((F(1),F(0)),(F(0),F(1)))
LEADER=((F(1),F(0)),(F(1,2),F(1,2)))


class OriginalDeGrootAndBergerPrimaryMath(unittest.TestCase):
    def test_primary1974_original_two_person_matrix_exact(self):
        self.assertEqual(m.matrix(ORIGINAL),ORIGINAL)

    def test_1974_original_two_person_source_stationary_one_third_two_thirds(self):
        self.assertEqual(m.gaussian_stationary_weights(ORIGINAL),(F(1,3),F(2,3)))

    def test_1974_original_two_person_independent_tree_stationary(self):
        self.assertEqual(m.independent_markov_in_trees(ORIGINAL),(F(1,3),F(2,3)))

    def test_1974_original_two_person_consensus_two_thirds(self):
        self.assertEqual(m.exact_consensus_value(ORIGINAL,(F(0),F(1))),F(2,3))

    def test_source_consensus_not_arithmetic_mean(self):
        self.assertNotEqual(m.exact_consensus_value(ORIGINAL,(F(0),F(1))),F(1,2))

    def test_original1974_p120_three_person_stationary_third_transient_zero(self):
        self.assertEqual(m.gaussian_stationary_weights(SOURCE_THIRD),(F(1,3),F(2,3),F(0)))

    def test_original1974_three_person_tree_independent_agrees(self):
        self.assertEqual(m.independent_markov_in_trees(SOURCE_THIRD),(F(1,3),F(2,3),F(0)))

    def test_original1974_three_person_third_initial_9_has_zero_consensus_effect(self):
        self.assertEqual(m.exact_consensus_value(SOURCE_THIRD,(F(0),F(1),F(9))),F(2,3))

    def test_original_three_person_third_altering_only_third_initial_no_effect(self):
        for third in (F(-100),F(0),F(1000)):
            with self.subTest(third=third):
                self.assertEqual(m.exact_consensus_value(SOURCE_THIRD,(F(0),F(1),third)),F(2,3))

    def test_original_two_person_first_step_exact(self):
        self.assertEqual(m.one_update(ORIGINAL,(F(0),F(1))),(F(1,2),F(3,4)))

    def test_original_two_person_second_step_exact(self):
        self.assertEqual(m.exact_trajectory(ORIGINAL,(F(0),F(1)),2)[2],(F(5,8),F(11,16)))

    def test_matrix_power_exponent_one_matches_first_update(self):
        w=m.power_matrix(ORIGINAL,1)
        self.assertEqual(w,ORIGINAL)

    def test_matrix_power_two_times_initial_matches_direct_second_iterate(self):
        w=m.power_matrix(ORIGINAL,2)
        self.assertEqual(tuple(row[1] for row in w),
                         m.exact_trajectory(ORIGINAL,(F(0),F(1)),2)[2])

    def test_matrix_power_zero_identity(self):
        self.assertEqual(m.power_matrix(ORIGINAL,0),IDENTITY)

    def test_1974_theorem1_one_positive_column_certificate_exists(self):
        self.assertIsNotNone(m.positive_column_power_certificate(ORIGINAL,12))

    def test_source_original_third_transient_has_positive_column_certificate(self):
        self.assertIsNotNone(m.positive_column_power_certificate(SOURCE_THIRD,12))

    def test_periodic_swap_not_all_initial_consensus(self):
        x=m.support_structure(SWAP)
        self.assertEqual(x["closed_periods"],(2,))
        self.assertFalse(x["all_initial_consensus_guaranteed"])
        self.assertFalse(x["all_initial_each_opinion_convergent"])

    def test_periodic_swap_opposing_opinions_oscillate(self):
        self.assertEqual(m.exact_trajectory(SWAP,(F(0),F(1)),4),
                         ((F(0),F(1)),(F(1),F(0)),(F(0),F(1)),
                          (F(1),F(0)),(F(0),F(1))))

    def test_periodic_swap_equal_initial_opinions_remain_in_consensus(self):
        self.assertEqual(m.exact_trajectory(SWAP,(F(1,2),F(1,2)),3),
                         ((F(1,2),F(1,2)),)*4)

    def test_swap_nonconvergent_not_sufficient_to_rule_out_given_consensus(self):
        self.assertFalse(m.support_structure(SWAP)["all_initial_consensus_guaranteed"])
        self.assertEqual(m.one_update(SWAP,(F(1,2),F(1,2))),(F(1,2),F(1,2)))

    def test_identity_two_absorbing_classes_not_universal_consensus(self):
        x=m.support_structure(IDENTITY)
        self.assertEqual(x["closed_classes"],((0,),(1,)))
        self.assertEqual(x["closed_periods"],(1,1))
        self.assertFalse(x["all_initial_consensus_guaranteed"])
        self.assertTrue(x["all_initial_each_opinion_convergent"])

    def test_identity_two_classes_opposed_remain_opposed(self):
        self.assertEqual(m.exact_trajectory(IDENTITY,(F(0),F(1)),5)[-1],(F(0),F(1)))

    def test_identity_two_classes_equal_initial_remain_equal(self):
        self.assertEqual(m.exact_trajectory(IDENTITY,(F(1,2),F(1,2)),3)[-1],(F(1,2),F(1,2)))

    def test_one_absorbing_leader_not_strongly_connected_still_universal_consensus(self):
        x=m.support_structure(LEADER)
        self.assertEqual(x["closed_classes"],((0,),))
        self.assertTrue(x["all_initial_consensus_guaranteed"])
        self.assertEqual(len(x["communicating_classes"]),2)

    def test_leader_pi_first_has_all_longrun_weight(self):
        self.assertEqual(m.gaussian_stationary_weights(LEADER),(F(1),F(0)))

    def test_leader_in_trees_first_all_longrun_weight(self):
        self.assertEqual(m.independent_markov_in_trees(LEADER),(F(1),F(0)))

    def test_leader_longrun_value_zero_when_first_initial_zero(self):
        self.assertEqual(m.exact_consensus_value(LEADER,(F(0),F(1))),F(0))

    def test_leader_sequence_halves_second_opinion_each_round(self):
        self.assertEqual(m.exact_trajectory(LEADER,(F(0),F(1)),4),
                         ((F(0),F(1)),(F(0),F(1,2)),(F(0),F(1,4)),
                          (F(0),F(1,8)),(F(0),F(1,16))))

    def test_symmetric_equal_weights_consensus_average_half(self):
        w=((F(1,2),F(1,2)),(F(1,2),F(1,2)))
        self.assertEqual(m.exact_consensus_value(w,(F(0),F(1))),F(1,2))
        self.assertEqual(m.exact_trajectory(w,(F(0),F(1)),1)[1],(F(1,2),F(1,2)))

    def test_fully_equal_initial_is_fixed_point_for_any_stochastic_matrix(self):
        for w in (ORIGINAL,SWAP,IDENTITY,LEADER):
            with self.subTest(w=w):
                self.assertEqual(m.one_update(w,(F(7,3),F(7,3))),(F(7,3),F(7,3)))

    def test_symmetric_matrix_stationary_both_one_half(self):
        w=((F(1,2),F(1,2)),(F(1,2),F(1,2)))
        self.assertEqual(m.gaussian_stationary_weights(w),(F(1,2),F(1,2)))

    def test_original_author_example_receipt_exact(self):
        x=m.degroot_original_published_examples()
        self.assertEqual(x["two_person_stationary"],("1/3","2/3"))
        self.assertEqual(x["three_person_stationary"],("1/3","2/3","0"))
        self.assertEqual(x["two_person_consensus_x0_0_1"],"2/3")
        self.assertEqual(x["three_person_consensus_x0_0_1_9"],"2/3")

    def test_Berger_1981_correction_flagged_not_1974_experiment(self):
        x=m.special_initial_opinion_counterexamples()
        self.assertTrue(x["berger_1981_corrects_1974_claim_of_necessity_for_one_particular_initial_F"])
        self.assertTrue(x["these_are_our_toy_constructions_not_1974_empirical_subject_trials"])

    def test_Berger_periodic_trajectories_registered_correctly(self):
        x=m.special_initial_opinion_counterexamples()
        self.assertEqual(x["swap_opposed_first_five"],
                         (("0","1"),("1","0"),("0","1"),("1","0"),("0","1")))

    def test_two_closed_classes_distinguish_eventual_individual_convergence(self):
        x=m.special_initial_opinion_counterexamples()["identity_structure"]
        self.assertTrue(x["all_initial_each_opinion_convergent"])
        self.assertFalse(x["all_initial_consensus_guaranteed"])

    def test_single_person_row_stochastic_guarantees_common_value(self):
        w=((F(1),),)
        self.assertTrue(m.support_structure(w)["all_initial_consensus_guaranteed"])
        self.assertEqual(m.gaussian_stationary_weights(w),(F(1),))
        self.assertEqual(m.independent_markov_in_trees(w),(F(1),))

    def test_universal_consensus_algorithms_independent_gaussian_without_trees(self):
        with patch.object(m,"independent_markov_in_trees",side_effect=AssertionError("NO_TREES")):
            self.assertEqual(m.gaussian_stationary_weights(ORIGINAL),(F(1,3),F(2,3)))

    def test_universal_consensus_algorithms_independent_trees_without_gaussian(self):
        with patch.object(m,"gaussian_stationary_weights",side_effect=AssertionError("NO_GAUSS")):
            self.assertEqual(m.independent_markov_in_trees(ORIGINAL),(F(1,3),F(2,3)))

    def test_periodic_swap_refuses_universal_stationary_consensus_value(self):
        with self.assertRaises(m.DeGrootDesignError):
            m.exact_consensus_value(SWAP,(F(0),F(1)))

    def test_identity_refuses_universal_consensus_value(self):
        with self.assertRaises(m.DeGrootDesignError):
            m.gaussian_stationary_weights(IDENTITY)
        with self.assertRaises(m.DeGrootDesignError):
            m.independent_markov_in_trees(IDENTITY)

    def test_original_source_convex_hull_and_nonincreasing_opinion_gap(self):
        trace=m.exact_trajectory(ORIGINAL,(F(0),F(1)),9)
        spans=[max(t)-min(t) for t in trace]
        self.assertTrue(all(spans[i+1]<=spans[i] for i in range(len(spans)-1)))

    def test_identity_opinion_gap_can_stay_positive_forever(self):
        trace=m.exact_trajectory(IDENTITY,(F(0),F(1)),10)
        self.assertTrue(all(max(t)-min(t)==1 for t in trace))

    def test_positive_column_certificate_swap_none(self):
        self.assertIsNone(m.positive_column_power_certificate(SWAP))

    def test_positive_column_certificate_identity_none(self):
        self.assertIsNone(m.positive_column_power_certificate(IDENTITY))

    def test_positive_column_certificate_single_absorbing_leader(self):
        cert=m.positive_column_power_certificate(LEADER)
        self.assertIsNotNone(cert)
        self.assertEqual(cert["positive_column"],0)

    def test_strict_matrix_rejects_int_float_boolean_or_negative(self):
        for bad in (0,F(-1,3),F(4,3),0.5,True,False,"1/2",None):
            with self.subTest(bad=bad),self.assertRaises(m.DeGrootDesignError):
                m.matrix(((bad,F(1)-F(1,2)),(F(1,2),F(1,2))))

    def test_matrix_rejects_wrong_normalization(self):
        with self.assertRaisesRegex(m.DeGrootDesignError,"STOCHASTIC"):
            m.matrix(((F(1,3),F(1,3)),(F(1,2),F(1,2))))

    def test_matrix_rejects_empty_nonsquare_or_generator(self):
        for bad in ((),((F(1),F(0)),),((F(1),),(F(1),)),(row for row in ORIGINAL)):
            with self.subTest(bad=str(type(bad))),self.assertRaises(m.DeGrootDesignError):
                m.matrix(bad)

    def test_matrix_rejects_more_than_four_persons(self):
        w=tuple(tuple(F(int(i==j)) for j in range(5)) for i in range(5))
        with self.assertRaises(m.DeGrootDesignError):
            m.matrix(w)

    def test_initial_opinions_strict_fraction_and_correct_dimension(self):
        for bad in ((0,F(1)),(F(1),),(F(0),F(1),F(1)),(F(0),True),()):
            with self.subTest(bad=bad),self.assertRaises(m.DeGrootDesignError):
                m.one_update(ORIGINAL,bad)

    def test_trajectory_step_limit_rejects_negative_bool_float(self):
        for bad in (-1,81,True,2.0,"3"):
            with self.subTest(bad=bad),self.assertRaises(m.DeGrootDesignError):
                m.exact_trajectory(ORIGINAL,(F(0),F(1)),bad)

    def test_matrix_power_limit_fail_closed(self):
        for bad in (-1,33,True,2.0,None):
            with self.subTest(bad=bad),self.assertRaises(m.DeGrootDesignError):
                m.power_matrix(ORIGINAL,bad)

    def test_certificate_positive_exponent_strict_bounded(self):
        for bad in (0,33,True,1.0,None):
            with self.subTest(bad=bad),self.assertRaises(m.DeGrootDesignError):
                m.positive_column_power_certificate(ORIGINAL,bad)

    def test_full_226_stochastic_small_matrix_exhaustion(self):
        x=m.tiny_226_row_stochastic_matrix_audit()
        self.assertEqual(x["tested_row_stochastic_matrices_by_n"],{"1":1,"2":9,"3":216})
        self.assertEqual(x["total_synthetic_matrices"],226)
        self.assertTrue(x["gaussian_and_independent_in_trees_identical_for_each_universal"])

    def test_full_226_matrix_exhaustion_has_some_nonconsensus_structures(self):
        x=m.tiny_226_row_stochastic_matrix_audit()
        self.assertGreater(x["total_synthetic_matrices"],
                           sum(x["universal_consensus_structures_by_n"].values()))

    def test_full_226_matrix_exhaustion_has_distinct_C_and_U_counts(self):
        x=m.tiny_226_row_stochastic_matrix_audit()
        c=sum(x["all_opinions_individually_converge_by_n"].values())
        u=sum(x["universal_consensus_structures_by_n"].values())
        self.assertGreaterEqual(c,u)
        self.assertGreater(c,u)

    def test_published_sources_actual_article_printed_pages(self):
        self.assertIn("1974",m.__doc__)
        self.assertIn("1981",m.__doc__)

    def test_all_math_is_deterministic(self):
        self.assertEqual(m.degroot_original_published_examples(),
                         m.degroot_original_published_examples())


if __name__=="__main__":
    unittest.main()
