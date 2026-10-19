"""R118 bounded original theory finite arithmetic, exhaustive small crowds only."""
import itertools
import unittest
from fractions import Fraction
from dataclasses import FrozenInstanceError

import r118_granovetter_1978_finite_threshold_participation as m


class ThresholdParticipationMathematicalTests(unittest.TestCase):
    def test_primary_granovetter_doi(self):
        self.assertEqual(m.SOURCE_DOI,"10.1086/226707")

    def test_original_exact_hundred_person_chain(self):
        self.assertEqual(m.synchronous_participation(tuple(range(100))).final_participants,100)

    def test_original_exact_hundred_person_broken_chain_one(self):
        t=tuple(2 if x==1 else x for x in range(100))
        self.assertEqual(m.synchronous_participation(t).final_participants,1)

    def test_original_source_changes_only_one_person(self):
        r=m.original_author_one_threshold_counterexample()
        self.assertEqual(r["modified_people_count"],1)

    def test_original_source_hundred_person_chain_records_all_stages(self):
        r=m.original_author_one_threshold_counterexample()
        self.assertEqual(r["original_initial_to_terminal_count_trajectory"],list(range(101)))

    def test_original_source_broken_chain_stops_immediately_after_one(self):
        r=m.original_author_one_threshold_counterexample()
        self.assertEqual(r["broken_initial_to_terminal_count_trajectory"],[0,1])

    def test_original_source_exact_sum_plus_one_after_threshold_change(self):
        r=m.original_author_one_threshold_counterexample()
        self.assertEqual(r["original_threshold_sum"],4950)
        self.assertEqual(r["broken_threshold_sum"],4951)

    def test_original_hundred_chain_sorted_independent_solver(self):
        self.assertEqual(m.independently_sorted_minimal_closure(tuple(range(100))),100)

    def test_original_broken_chain_sorted_independent_solver(self):
        t=tuple(2 if x==1 else x for x in range(100))
        self.assertEqual(m.independently_sorted_minimal_closure(t),1)

    def test_new_project_compensated_example_preserves_exact_mean(self):
        v=m.same_mean_different_collective_outcome()
        self.assertEqual(v["original_mean_exact"],"99/2")
        self.assertEqual(v["compensated_mean_exact"],"99/2")
        self.assertEqual(v["original_threshold_sum"],v["compensated_threshold_sum"])

    def test_new_project_compensated_changes_exactly_two_people(self):
        self.assertEqual(m.same_mean_different_collective_outcome()["modified_people_count"],2)

    def test_new_project_compensated_identical_mean_outcomes_diverge(self):
        v=m.same_mean_different_collective_outcome()
        self.assertEqual(v["original_final_participants"],100)
        self.assertEqual(v["compensated_final_participants"],1)
        self.assertTrue(v["constructed_by_project_not_source_author"])

    def test_no_zero_threshold_person_no_initial_activation(self):
        self.assertEqual(m.synchronous_participation((1,1,1,1)).final_participants,0)

    def test_every_person_zero_threshold_all_join_first_round(self):
        s=m.synchronous_participation((0,0,0,0,0))
        self.assertEqual(s.final_participants,5)
        self.assertEqual(s.counts_from_initial_zero,(0,5))
        self.assertEqual(s.activation_rounds,1)

    def test_threshold_n_never_spontaneously_joins(self):
        self.assertEqual(m.synchronous_participation((0,0,3)).final_participants,2)

    def test_one_person_threshold_zero_spontaneously_joins(self):
        self.assertEqual(m.synchronous_participation((0,)).final_participants,1)

    def test_one_person_threshold_one_cannot_join(self):
        self.assertEqual(m.synchronous_participation((1,)).final_participants,0)

    def test_mixed_thresholds_synchronous_batch_entry(self):
        s=m.synchronous_participation((0,0,2,2,4))
        self.assertEqual(s.counts_from_initial_zero,(0,2,4,5))

    def test_incomplete_chain_ends_with_fixed_point(self):
        s=m.synchronous_participation((0,1,5,5,5))
        self.assertEqual(s.counts_from_initial_zero,(0,1,2))
        self.assertEqual(m.threshold_cdf_count((0,1,5,5,5),2),2)

    def test_no_participants_is_fixed_point_when_all_thresholds_positive(self):
        self.assertEqual(m.threshold_cdf_count((1,1,1),0),0)

    def test_source_finite_cdf_recursion_step(self):
        self.assertEqual(m.threshold_cdf_count((0,1,2,3),0),1)
        self.assertEqual(m.threshold_cdf_count((0,1,2,3),1),2)

    def test_threshold_cdf_count_exact_includes_equality(self):
        self.assertEqual(m.threshold_cdf_count((0,0,1,2,3),1),3)

    def test_result_participation_fraction_is_exact(self):
        x=m.synchronous_participation((0,1,4,4))
        self.assertEqual(x.final_participants,2)
        self.assertEqual(x.participation_fraction,Fraction(1,2))

    def test_result_is_frozen(self):
        with self.assertRaises(FrozenInstanceError):
            m.synchronous_participation((0,1)).final_participants=0

    def test_shuffle_order_invariant_final_participation(self):
        original=(0,2,1,5,5,1)
        for perm in ((1,5,0,1,5,2),(5,5,2,1,1,0),original[::-1]):
            self.assertEqual(m.verify_both_solvers(original).final_participants,
                             m.verify_both_solvers(perm).final_participants)

    def test_threshold_reduction_does_not_reduce_participation(self):
        t=(0,2,2,3,4,5)
        more=(0,1,2,3,4,5)
        self.assertLessEqual(m.verify_both_solvers(t).final_participants,
                             m.verify_both_solvers(more).final_participants)

    def test_one_missing_threshold_blocks_rest_despite_low_mean(self):
        t=(0,2,2,2,2,2)
        self.assertEqual(m.verify_both_solvers(t).final_participants,1)

    def test_full_participation_requires_each_chain_link_for_sequence(self):
        for n in range(1,20):
            self.assertEqual(m.verify_both_solvers(tuple(range(n))).final_participants,n)

    def test_small_n_exact_exhaustive_coverage_one(self):
        self.assertEqual(m.exhaustive_small_groups(1),{"1":2})

    def test_small_n_exact_exhaustive_coverage_two(self):
        self.assertEqual(m.exhaustive_small_groups(2),{"1":2,"2":9})

    def test_full_finite_ordered_threshold_enumeration_n_to_five(self):
        counts=m.exhaustive_small_groups(5)
        self.assertEqual(counts,{"1":2,"2":9,"3":64,"4":625,"5":7776})
        self.assertEqual(sum(counts.values()),8476)

    def test_sorted_solver_does_not_call_dynamic_solver(self):
        from unittest.mock import patch
        with patch.object(m,"synchronous_participation",side_effect=AssertionError("DYNAMIC_FORBIDDEN")):
            self.assertEqual(m.independently_sorted_minimal_closure((0,1,3)),2)

    def test_dynamic_solver_does_not_call_sorted_solver(self):
        from unittest.mock import patch
        with patch.object(m,"independently_sorted_minimal_closure",side_effect=AssertionError("SORTED_FORBIDDEN")):
            self.assertEqual(m.synchronous_participation((0,1,3)).final_participants,2)

    def test_no_multiple_equilibria_claim_from_single_reachable_closure(self):
        self.assertEqual(m.synchronous_participation((1,1)).final_participants,0)
        self.assertEqual(m.synchronous_participation((0,0)).final_participants,2)

    def test_invalid_threshold_float_bool_negative_string_rejected(self):
        for bad in (0.0,True,False,-1,"1",None,Fraction(1)):
            with self.subTest(bad=bad),self.assertRaises(m.ThresholdModelError):
                m.synchronous_participation((0,bad,1))

    def test_threshold_exceeding_n_rejected(self):
        with self.assertRaises(m.ThresholdModelError):
            m.synchronous_participation((0,3))

    def test_empty_thresholds_rejected(self):
        with self.assertRaises(m.ThresholdModelError):
            m.synchronous_participation(())

    def test_generator_or_set_not_accepted_silently(self):
        for bad in ({0,1},(x for x in [0,1]),"01"):
            with self.subTest(value=type(bad)),self.assertRaises(m.ThresholdModelError):
                m.synchronous_participation(bad)

    def test_large_group_resource_limit(self):
        with self.assertRaises(m.ThresholdModelError):
            m.synchronous_participation((0,)*2001)

    def test_cdf_bad_count_or_type_rejected(self):
        for bad in (-1,3,True,1.0,"1"):
            with self.subTest(value=bad),self.assertRaises(m.ThresholdModelError):
                m.threshold_cdf_count((0,1),bad)

    def test_exhaustive_limits_reject_false_count_types(self):
        for bad in (0,6,True,1.,None):
            with self.subTest(value=bad),self.assertRaises(m.ThresholdModelError):
                m.exhaustive_small_groups(bad)

    def test_new_example_has_no_real_human_reanalysis_claim(self):
        x=m.study_receipt()
        self.assertEqual(x["original_human_E2_score_observations"],0)
        self.assertTrue(x["source_mathematical_mechanism_not_empirical_fit"])
        self.assertTrue(x["no_network_or_dropout_assumed"])
        self.assertEqual(x["R073"],"FROZEN")
        self.assertEqual(x["PESEN_v0_1"],"FROZEN")

    def test_exact_source_three_references_and_disjoint_new_example(self):
        x=m.study_receipt()
        self.assertEqual(x["first_party_printed_pages"],[1422,1424,1425,1426])
        self.assertEqual(x["original_author_100person_counterexample"]["modified_people_count"],1)
        self.assertEqual(x["new_project_same_mean_counterexample"]["modified_people_count"],2)

    def test_full_receipt_deterministic(self):
        self.assertEqual(m.study_receipt(),m.study_receipt())


if __name__=="__main__":
    unittest.main()
