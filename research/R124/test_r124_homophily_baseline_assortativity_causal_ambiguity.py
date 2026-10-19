"""R124 standalone exact homophily, opportunity and observational-equivalence checks."""
import unittest
from fractions import Fraction as F
from itertools import combinations
from unittest.mock import patch

import r124_homophily_baseline_assortativity_causal_ambiguity as m

LABELS=("A","A","A","B","B","B")
TRIANGLES=((0,1),(0,2),(1,2),(3,4),(3,5),(4,5))
SIX_RING=((0,1),(1,2),(2,3),(3,4),(4,5),(5,0))
K33=tuple((i,j) for i in range(3) for j in range(3,6))
K6=tuple(combinations(range(6),2))


class FirstPartyHomophilyMath(unittest.TestCase):
    def test_original_2001_source_distinguishes_baseline_and_inbreeding(self):
        self.assertIn("McPherson",m.__doc__)
        self.assertIn("2001",m.__doc__)

    def test_original_2003_Newman_source_in_docstring(self):
        self.assertIn("Newman",m.__doc__)
        self.assertIn("026126",m.__doc__)

    def test_original_2009_empirical_paper_only_public_abstract(self):
        self.assertIn("abstract ONLY",m.__doc__)

    def test_perfect_two_triangles_100percent_same(self):
        self.assertEqual(m.newman_mixing_direct(6,LABELS,TRIANGLES)["same_edge_fraction"],F(1))

    def test_perfect_two_triangles_newman_r_one(self):
        self.assertEqual(m.verify_independent_mixing(6,LABELS,TRIANGLES)["assortativity"],F(1))

    def test_two_triangles_original_source_E_matrix_diagonal(self):
        e=m.newman_mixing_direct(6,LABELS,TRIANGLES)["mixing_matrix"]
        self.assertEqual(e,((F(1,2),F(0)),(F(0),F(1,2))))

    def test_two_triangles_stubs_both_half(self):
        self.assertEqual(m.independent_stub_arithmetic(6,LABELS,TRIANGLES)["endpoint_marginals"],(F(1,2),F(1,2)))

    def test_cyclic_C6_two_cross_four_same(self):
        x=m.verify_independent_mixing(6,LABELS,SIX_RING)
        self.assertEqual(x["same_edge_fraction"],F(2,3))
        self.assertEqual(x["assortativity"],F(1,3))

    def test_cyclic_C6_original_newman_mixing_matrix(self):
        x=m.newman_mixing_direct(6,LABELS,SIX_RING)
        self.assertEqual(x["mixing_matrix"],((F(1,3),F(1,6)),(F(1,6),F(1,3))))

    def test_complete_K33_all_cross_negative_one(self):
        x=m.verify_independent_mixing(6,LABELS,K33)
        self.assertEqual(x["same_edge_fraction"],F(0))
        self.assertEqual(x["assortativity"],F(-1))

    def test_same_edge_not_equivalent_to_positive_Newman_assortativity(self):
        x=m.verify_independent_mixing(6,("A",)*5+("B",),K6)
        self.assertEqual(x["same_edge_fraction"],F(2,3))
        self.assertEqual(x["assortativity"],F(-1,5))

    def test_K6_skew_population_full_pair_baseline_equals_observed_same(self):
        labels=("A",)*5+("B",)
        self.assertEqual(m.population_without_replacement_baseline(labels),F(2,3))
        self.assertEqual(m.verify_independent_mixing(6,labels,K6)["same_edge_fraction"],F(2,3))

    def test_K6_skew_Newman_baseline_is_different_stub_null(self):
        x=m.verify_independent_mixing(6,("A",)*5+("B",),K6)
        self.assertEqual(x["endpoint_marginals"],(F(5,6),F(1,6)))
        self.assertEqual(x["stub_independence_baseline"],F(13,18))

    def test_one_label_at_all_nonisolated_endpoints_r_must_be_undefined(self):
        x=m.verify_independent_mixing(3,("A","A","B"),((0,1),))
        self.assertIsNone(x["assortativity"])
        self.assertEqual(x["same_edge_fraction"],1)
        self.assertEqual(x["undefined_reason"],"ONLY_ONE_CATEGORY_AT_ALL_EDGE_ENDPOINTS")

    def test_one_label_at_all_endpoints_not_relabelled_perfect_r_one(self):
        self.assertNotEqual(m.newman_mixing_direct(3,("A","A","B"),((0,1),))["assortativity"],F(1))

    def test_independent_stub_solver_does_not_call_mixing_matrix_solver(self):
        with patch.object(m,"newman_mixing_direct",side_effect=AssertionError("NO_MIX")):
            self.assertEqual(m.independent_stub_arithmetic(6,LABELS,TRIANGLES)["assortativity"],1)

    def test_mixing_solver_does_not_call_independent_stub_solver(self):
        with patch.object(m,"independent_stub_arithmetic",side_effect=AssertionError("NO_STUB")):
            self.assertEqual(m.newman_mixing_direct(6,LABELS,TRIANGLES)["assortativity"],1)

    def test_all_undirected_edges_reversed_have_same_assortativity(self):
        backwards=tuple((j,i) for i,j in TRIANGLES[::-1])
        self.assertEqual(m.verify_independent_mixing(6,LABELS,TRIANGLES),
                         m.verify_independent_mixing(6,LABELS,backwards))

    def test_global_population_baseline_for_three_three_is_two_fifths(self):
        self.assertEqual(m.population_without_replacement_baseline(LABELS),F(2,5))

    def test_global_population_pair_baseline_for_one_three_versus_one_is_half(self):
        self.assertEqual(m.population_without_replacement_baseline(("A","A","A","B")),F(1,2))

    def test_exact_permutation_null_c6_population_expected_same_edges(self):
        x=m.exact_uniform_label_permutation_null(6,LABELS,SIX_RING)
        self.assertEqual(x["expected_same_edges"],F(12,5))

    def test_triangles_exact_label_null_has_twenty_placements(self):
        self.assertEqual(m.exact_uniform_label_permutation_null(6,LABELS,TRIANGLES)["permutations"],20)

    def test_triangles_null_exact_frequency_only_two_or_six_same(self):
        x=m.exact_uniform_label_permutation_null(6,LABELS,TRIANGLES)
        self.assertEqual(x["same_edge_count_frequencies"],{2:18,6:2})

    def test_triangles_null_right_tail_exact_one_tenth(self):
        self.assertEqual(m.exact_uniform_label_permutation_null(6,LABELS,TRIANGLES)[
            "right_tail_probability_under_exchangeable_label_null"],F(1,10))

    def test_triangles_null_expected_same_two_and_two_fifths(self):
        x=m.exact_uniform_label_permutation_null(6,LABELS,TRIANGLES)
        self.assertEqual(x["expected_same_edges"],F(12,5))
        self.assertEqual(x["baseline_fraction_same"],F(2,5))

    def test_random_label_null_not_misrepresented_as_empirical_p_value(self):
        self.assertTrue(m.exact_uniform_label_permutation_null(6,LABELS,TRIANGLES)[
            "this_is_NOT_an_empirical_p_value"])

    def test_permutation_count_two_labels_three_four(self):
        x=m.exact_uniform_label_permutation_null(4,("A","A","B","B"),((0,1),(2,3)))
        self.assertEqual(x["permutations"],6)

    def test_focal_opportunity_pool_has_six_all_same_pairs(self):
        x=m.fixed_opportunity_baseline(6,LABELS,TRIANGLES,TRIANGLES)
        self.assertEqual(x["eligible_pair_count"],6)
        self.assertEqual(x["opportunity_same_fraction"],1)

    def test_observed_perfect_homophily_has_zero_excess_given_foci(self):
        x=m.fixed_opportunity_baseline(6,LABELS,TRIANGLES,TRIANGLES)
        self.assertEqual(x["opportunity_excess"],0)

    def test_same_observed_graph_above_unrestricted_opportunity_pool(self):
        x=m.fixed_opportunity_baseline(6,LABELS,TRIANGLES,K6)
        self.assertEqual(x["global_population_pair_excess"],F(3,5))
        self.assertEqual(x["opportunity_excess"],F(3,5))

    def test_same_graph_global_vs_focal_opportunity_excess_contrasts(self):
        restricted=m.fixed_opportunity_baseline(6,LABELS,TRIANGLES,TRIANGLES)
        unrestricted=m.fixed_opportunity_baseline(6,LABELS,TRIANGLES,K6)
        self.assertEqual((restricted["opportunity_excess"],unrestricted["opportunity_excess"]),(F(0),F(3,5)))

    def test_fixed_opportunities_cannot_omit_real_observed_edge(self):
        with self.assertRaisesRegex(m.HomophilyAuditError,"OUTSIDE"):
            m.fixed_opportunity_baseline(6,LABELS,TRIANGLES,((0,1),))

    def test_fixed_opportunity_assumption_not_empirically_identified(self):
        self.assertTrue(m.fixed_opportunity_baseline(6,LABELS,TRIANGLES,K6)[
            "opportunity_model_is_assumed_not_inferred"])

    def test_selection_story_final_graph_matches_two_triangles(self):
        x=m.identical_snapshot_three_generating_histories()
        self.assertEqual(x["final_edge_pairs"],[list(pair) for pair in TRIANGLES])
        self.assertEqual(x["selection_story_formed_ties"],6)

    def test_selection_story_unrestricted_opportunity_count_fifteen(self):
        self.assertEqual(m.identical_snapshot_three_generating_histories()[
            "selection_story_eligible_pairs"],15)

    def test_focal_opportunity_story_only_six_eligible_all_formed(self):
        x=m.identical_snapshot_three_generating_histories()
        self.assertEqual(x["opportunity_story_formed_ties"],x["opportunity_story_eligible_pairs"])
        self.assertEqual(x["opportunity_story_eligible_pairs"],6)

    def test_influence_story_starts_with_two_local_majorities_not_all_same(self):
        x=m.identical_snapshot_three_generating_histories()
        self.assertEqual(x["influence_story_initial_attributes"],["A","A","B","B","B","A"])

    def test_influence_story_clique_majority_ends_three_A_three_B(self):
        x=m.identical_snapshot_three_generating_histories()
        self.assertEqual(x["influence_story_attributes_after_one_majority_step"],["A","A","A","B","B","B"])

    def test_influence_story_has_no_edge_change(self):
        self.assertEqual(m.identical_snapshot_three_generating_histories()["influence_story_edge_changes"],0)

    def test_three_distinct_histories_same_observation_does_not_identify_selection(self):
        x=m.identical_snapshot_three_generating_histories()
        self.assertTrue(x["all_final_snapshots_identical"])
        self.assertTrue(x["selection_preference_effect_not_identified_from_snapshot"])

    def test_same_final_snapshot_has_identical_Newman_r_one(self):
        x=m.identical_snapshot_three_generating_histories()
        edges=tuple(map(tuple,x["final_edge_pairs"]))
        self.assertEqual(m.verify_independent_mixing(6,x["final_attributes"],edges)["assortativity"],1)

    def test_graph_rejects_empty_edge_metric_domain(self):
        with self.assertRaisesRegex(m.HomophilyAuditError,"NONEMPTY"):
            m.verify_independent_mixing(2,("A","B"),())

    def test_graph_rejects_duplicate_undirected_edges_both_orders(self):
        with self.assertRaisesRegex(m.HomophilyAuditError,"DUPLICATE"):
            m.graph(3,("A","A","B"),((0,1),(1,0)))

    def test_graph_rejects_self_loop(self):
        with self.assertRaisesRegex(m.HomophilyAuditError,"NO_SELF_LOOP"):
            m.graph(2,("A","B"),((0,0),))

    def test_graph_rejects_bad_edge_arity(self):
        for bad in ((0,1,2),(0,),"01"):
            with self.subTest(edge=bad),self.assertRaises(m.HomophilyAuditError):
                m.graph(3,("A","A","B"),(bad,))

    def test_graph_rejects_bool_nonint_invalid_endpoint(self):
        for bad in (True,False,-1,3,1.0,"1",None):
            with self.subTest(edge=bad),self.assertRaises(m.HomophilyAuditError):
                m.graph(3,("A","A","B"),((0,bad),))

    def test_graph_rejects_invalid_n(self):
        for bad in (0,1,9,True,False,2.0,"6"):
            with self.subTest(n=bad),self.assertRaises(m.HomophilyAuditError):
                m.graph(bad,(),())

    def test_graph_rejects_invalid_categories_type_values_or_length(self):
        for bad in ((1,"B"),("A","C"),(True,"B"),("A",),("A","A"),("B","B"),"AB"):
            with self.subTest(labels=bad),self.assertRaises(m.HomophilyAuditError):
                m.graph(2,bad,((0,1),))

    def test_graph_rejects_generator_edge_input(self):
        with self.assertRaises(m.HomophilyAuditError):
            m.graph(2,("A","B"),((0,1) for _ in range(1)))

    def test_population_baseline_rejects_only_one_category(self):
        with self.assertRaises(m.HomophilyAuditError):
            m.population_without_replacement_baseline(("A","A"))

    def test_strict_binary_all_graph_label_exhaustion_total_948(self):
        x=m.exhaustive_small_binary_network_audit()
        self.assertEqual(x["total_cases_by_n"],{"2":4,"3":48,"4":896})
        self.assertEqual(x["all_graph_label_cases"],948)

    def test_graph_exhaustion_explicitly_counts_22_empty_cases(self):
        x=m.exhaustive_small_binary_network_audit()
        self.assertEqual(x["empty_no_metric_by_n"],{"2":2,"3":6,"4":14})
        self.assertEqual(sum(x["nonempty_networks_by_n"].values()),926)

    def test_graph_exhaustion_tracks_Newman_undefined_denominators(self):
        x=m.exhaustive_small_binary_network_audit()
        self.assertGreater(sum(x["nonempty_newman_denominator_zero_by_n"].values()),0)
        self.assertTrue(x["newman_assortativity_never_silently_imputed_when_undefined"])

    def test_toy_repeats_deterministically(self):
        self.assertEqual(m.identical_snapshot_three_generating_histories(),
                         m.identical_snapshot_three_generating_histories())

    def test_all_metrics_return_exact_Fraction_except_undefined(self):
        x=m.newman_mixing_direct(6,LABELS,TRIANGLES)
        self.assertIs(type(x["assortativity"]),F)
        self.assertIs(type(x["same_edge_fraction"]),F)

    def test_research_scope_no_actual_human_E2(self):
        x=m.original_project_frozen_graph_examples()
        self.assertTrue(x["no_causal_effect_or_real_people_fitted"])


if __name__=="__main__":
    unittest.main()
