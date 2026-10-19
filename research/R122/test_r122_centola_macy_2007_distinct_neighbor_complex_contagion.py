"""R122 source-bounded distinct-neighbor social reinforcement and ring formulas."""
import unittest
from fractions import Fraction as F
from unittest.mock import patch
from itertools import combinations
import r122_centola_macy_2007_distinct_neighbor_complex_contagion as m


class CentolaMacyDistinctSourceTests(unittest.TestCase):
    def test_original_Centola_Macy_DOI(self):
        self.assertEqual(m.PRIMARY_DOI,"10.1086/521848")

    def test_six_people_two_cliques_have_six_internal_edges(self):
        self.assertEqual(len(m._two_cliques()),6)

    def test_both_seeded_clique_simple_narrow_crosses_entire_graph(self):
        edges=m.frozen_bridge_topologies()["narrow_one"]
        self.assertEqual(m.verify_independent_final_sets(6,edges,(1,)*6,(0,1,2))["count"],6)

    def test_both_seeded_clique_complex_narrow_remains_three(self):
        edges=m.frozen_bridge_topologies()["narrow_one"]
        x=m.verify_independent_final_sets(6,edges,(2,)*6,(0,1,2))
        self.assertEqual(x["final"],frozenset((0,1,2)))

    def test_three_misallocated_edges_complex_still_blocked(self):
        edges=m.frozen_bridge_topologies()["misallocated_three"]
        self.assertEqual(m.verify_independent_final_sets(6,edges,(2,)*6,(0,1,2))["count"],3)

    def test_three_functional_edges_complex_activate_entire_graph(self):
        edges=m.frozen_bridge_topologies()["functional_three"]
        self.assertEqual(m.verify_independent_final_sets(6,edges,(2,)*6,(0,1,2))["count"],6)

    def test_same_cross_edge_count_misallocation_vs_functionality(self):
        x=m.toy_bridge_results()
        self.assertEqual(x["misallocated_three"]["cross_edges"],x["functional_three"]["cross_edges"])
        self.assertNotEqual(x["misallocated_three"]["complex_all_A_seeds_final_count"],
                            x["functional_three"]["complex_all_A_seeds_final_count"])

    def test_all_three_cross_bridge_types_spread_simple_contact(self):
        x=m.toy_bridge_results()
        self.assertTrue(all(v["simple_all_A_seeds_final_count"]==6 for v in x.values()))

    def test_narrow_complex_trace_stops_at_three(self):
        x=m.toy_bridge_results()
        self.assertEqual(x["narrow_one"]["complex_all_A_seeds_round_counts"],[3])

    def test_misallocated_complex_trace_stops_at_three(self):
        x=m.toy_bridge_results()
        self.assertEqual(x["misallocated_three"]["complex_all_A_seeds_round_counts"],[3])

    def test_functional_complex_trace_reinforces_two_distinct_neighbours(self):
        x=m.toy_bridge_results()
        self.assertEqual(x["functional_three"]["complex_all_A_seeds_round_counts"],[3,4,5,6])

    def test_simple_uses_only_one_distinct_active_neighbor(self):
        a=((0,1),)
        x=m.verify_independent_final_sets(2,a,(1,1),(0,))
        self.assertEqual(x["final"],frozenset((0,1)))

    def test_complex_not_triggered_by_single_distinct_neighbor(self):
        a=((0,1),)
        x=m.verify_independent_final_sets(2,a,(2,2),(0,))
        self.assertEqual(x["final"],frozenset((0,)))

    def test_one_source_repeated_reports_not_counted_multiple_times(self):
        a=((0,1),)
        adj,ts,seed=m.validate(2,a,(1,2),(0,))
        self.assertEqual(len(adj[1] & seed),1)
        self.assertEqual(m.verify_independent_final_sets(2,a,(1,2),(0,))["count"],1)

    def test_one_seed_cannot_start_complex_activation_inside_triangle(self):
        g=m._two_cliques()
        x=m.verify_independent_final_sets(6,g,(2,)*6,(0,))
        self.assertEqual(x["final"],frozenset((0,)))

    def test_two_seeds_are_sufficient_for_complex_local_triangle(self):
        g=m._two_cliques()
        x=m.verify_independent_final_sets(6,g,(2,)*6,(0,1))
        self.assertEqual(x["final"],frozenset((0,1,2)))

    def test_one_seed_is_sufficient_for_simple_local_triangle(self):
        g=m._two_cliques()
        self.assertEqual(m.verify_independent_final_sets(6,g,(1,)*6,(0,))["count"],3)

    def test_no_seed_positive_threshold_never_spontaneously_activates(self):
        g=m._two_cliques()
        self.assertEqual(m.verify_independent_final_sets(6,g,(1,)*6,())["count"],0)

    def test_seeds_preserved_even_when_threshold_unattainable(self):
        self.assertEqual(m.verify_independent_final_sets(3,(),(3,3,3),(2,))["final"],frozenset((2,)))

    def test_fully_seeded_set_is_terminal(self):
        self.assertEqual(m.verify_independent_final_sets(3,(),(2,)*3,(0,1,2))["count"],3)

    def test_isolated_nonseed_cannot_adopt_threshold_positive(self):
        self.assertEqual(m.verify_independent_final_sets(3,((0,1),),(1,1,1),(0,))["final"],frozenset((0,1)))

    def test_simple_synchronous_progress_on_path(self):
        path=((0,1),(1,2),(2,3))
        self.assertEqual(m.synchronous_distinct_neighbor_cascade(4,path,(1,)*4,(0,))["trajectory"],
                         (frozenset((0,)),frozenset((0,1)),frozenset((0,1,2)),frozenset((0,1,2,3))))

    def test_closed_set_solver_independent_of_synchronous_function(self):
        with patch.object(m,"synchronous_distinct_neighbor_cascade",side_effect=AssertionError("NOT_ALLOWED")):
            self.assertEqual(m.independent_least_closed_set(3,((0,1),(1,2)),(1,)*3,(0,)),frozenset((0,1,2)))

    def test_synchronous_solver_independent_of_closed_set_function(self):
        with patch.object(m,"independent_least_closed_set",side_effect=AssertionError("NOT_ALLOWED")):
            self.assertEqual(m.synchronous_distinct_neighbor_cascade(3,((0,1),(1,2)),(1,)*3,(0,))["count"],3)

    def test_edge_order_permutation_cannot_change_final_members(self):
        g=m.frozen_bridge_topologies()["functional_three"]
        for perm in (g,g[::-1]):
            self.assertEqual(m.verify_independent_final_sets(6,perm,(2,)*6,(0,1,2))["count"],6)

    def test_addition_of_edge_cannot_remove_activated_people_under_count_threshold(self):
        a=m._two_cliques()+((2,3),)
        b=m._two_cliques()+((2,3),(1,3),(2,4))
        before=m.verify_independent_final_sets(6,a,(2,)*6,(0,1,2))["final"]
        after=m.verify_independent_final_sets(6,b,(2,)*6,(0,1,2))["final"]
        self.assertTrue(before<=after)
        self.assertEqual((len(before),len(after)),(3,6))

    def test_source_ring_max_degree_four_equals_three(self):
        self.assertEqual(m.ring_max_effective_bridge_width(4),3)

    def test_source_ring_max_degree_six_equals_six(self):
        self.assertEqual(m.ring_max_effective_bridge_width(6),6)

    def test_ring_degree_two_max_bridge_equals_one(self):
        self.assertEqual(m.ring_max_effective_bridge_width(2),1)

    def test_ring_degree_eight_max_bridge_equals_ten(self):
        self.assertEqual(m.ring_max_effective_bridge_width(8),10)

    def test_source_ring_a1_critical_width_one(self):
        self.assertEqual(m.ring_critical_bridge_width(1),1)

    def test_source_ring_a2_critical_width_three(self):
        self.assertEqual(m.ring_critical_bridge_width(2),3)

    def test_source_ring_a3_critical_width_six(self):
        self.assertEqual(m.ring_critical_bridge_width(3),6)

    def test_ring_z4_threshold2_exactly_sufficient_width(self):
        x=m.ring_bridge_condition(4,2)
        self.assertEqual(x["max_width"],3)
        self.assertEqual(x["critical_width"],3)
        self.assertTrue(x["special_ring_width_sufficient"])

    def test_ring_z4_threshold3_exceeds_max_bridge_width(self):
        self.assertFalse(m.ring_bridge_condition(4,3)["special_ring_width_sufficient"])

    def test_ring_z6_threshold3_exactly_sufficient_width(self):
        self.assertTrue(m.ring_bridge_condition(6,3)["special_ring_width_sufficient"])

    def test_ring_degree_must_be_even_positive_real_integer_not_boolean(self):
        for bad in (0,1,3,-2,True,4.0,"4"):
            with self.subTest(bad=bad),self.assertRaises(m.ContagionDesignError):
                m.ring_max_effective_bridge_width(bad)

    def test_ring_activation_count_must_positive_integer_not_bool(self):
        for bad in (0,-1,True,2.0,"2"):
            with self.subTest(bad=bad),self.assertRaises(m.ContagionDesignError):
                m.ring_critical_bridge_width(bad)

    def test_invalid_n_zero_large_float_boolean(self):
        for bad in (0,9,-1,True,3.0,"3"):
            with self.subTest(bad=bad),self.assertRaises(m.ContagionDesignError):
                m.validate(bad,(),(),())

    def test_duplicate_undirected_edge_reverse_order_rejected(self):
        with self.assertRaisesRegex(m.ContagionDesignError,"DUPLICATE"):
            m.validate(3,((0,1),(1,0)),(1,1,1),(0,))

    def test_self_loop_rejected(self):
        with self.assertRaisesRegex(m.ContagionDesignError,"SELF"):
            m.validate(2,((0,0),),(1,1),(0,))

    def test_invalid_edge_container_and_arity_rejected(self):
        for bad in ((0,1,1),(0,),"0-1"):
            with self.subTest(bad=bad),self.assertRaises(m.ContagionDesignError):
                m.validate(2,(bad,),(1,1),(0,))

    def test_boolean_or_out_of_range_edge_endpoints_denied(self):
        for bad in (True,False,-1,2,1.0,"1"):
            with self.subTest(bad=bad),self.assertRaises(m.ContagionDesignError):
                m.validate(2,((0,bad),),(1,1),(0,))

    def test_invalid_threshold_zero_negative_above_n_float_bool_denied(self):
        for bad in (0,-1,3,1.0,True,False,"2"):
            with self.subTest(bad=bad),self.assertRaises(m.ContagionDesignError):
                m.validate(2,((0,1),),(1,bad),(0,))

    def test_invalid_threshold_length_and_container_denied(self):
        with self.assertRaises(m.ContagionDesignError):
            m.validate(2,(),(1,),())
        with self.assertRaises(m.ContagionDesignError):
            m.validate(2,(),(x for x in (1,1)),())

    def test_duplicate_and_invalid_seed_rejected(self):
        for bad in ((0,0),(-1,),(3,),(False,),(True,),(0.0,),("0",)):
            with self.subTest(bad=bad),self.assertRaises(m.ContagionDesignError):
                m.validate(3,(),(1,)*3,bad)

    def test_seed_generator_or_string_rejected(self):
        for bad in ((x for x in (0,)), "0"):
            with self.subTest(value=str(type(bad))),self.assertRaises(m.ContagionDesignError):
                m.validate(3,(),(1,)*3,bad)

    def test_exact_small_graph_enumeration_all_16930_configs(self):
        self.assertEqual(m.exact_small_graph_exhaustion(),
                         {"1":2,"2":32,"3":512,"4":16384})

    def test_no_human_E2_model_predictions_from_toy_receipt(self):
        x=m.toy_bridge_results()
        self.assertEqual(x["functional_three"]["complex_all_A_seeds_final_count"],6)
        self.assertNotIn("human_E2",x)

    def test_original_ring_source_not_universal_bridge_sufficiency(self):
        x=m.toy_bridge_results()
        self.assertEqual(x["misallocated_three"]["cross_edges"],3)
        self.assertEqual(m.ring_critical_bridge_width(2),3)
        self.assertEqual(x["misallocated_three"]["complex_all_A_seeds_final_count"],3)

    def test_reproducible_frozen_bridge_results(self):
        self.assertEqual(m.toy_bridge_results(),m.toy_bridge_results())


if __name__=="__main__":
    unittest.main()
