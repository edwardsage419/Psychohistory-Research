"""R121 exact source-based IC, two mathematically separate full-set solvers."""
import unittest
from fractions import Fraction as F
from unittest.mock import patch

import r121_kkt_2003_independent_cascade_exact as m


class ICSourceMechanismExactTests(unittest.TestCase):
    def test_valid_empty_graph_no_seed(self):
        self.assertEqual(m.verify_complete_distribution(3,(),()),{frozenset():F(1)})

    def test_single_seed_without_edges(self):
        self.assertEqual(m.verify_complete_distribution(3,(),(1,)),{frozenset((1,)):F(1)})

    def test_every_node_seeded(self):
        self.assertEqual(m.verify_complete_distribution(3,((0,2,F(1,2)),),(0,1,2)),
                         {frozenset((0,1,2)):F(1)})

    def test_single_edge_half_exact_two_terminal_sets(self):
        x=m.verify_complete_distribution(2,((0,1,F(1,2)),),(0,))
        self.assertEqual(x,{frozenset((0,)):F(1,2),frozenset((0,1)):F(1,2)})

    def test_zero_probability_edge_never_activates(self):
        self.assertEqual(m.verify_complete_distribution(2,((0,1,F(0)),),(0,)),
                         {frozenset((0,)):F(1)})

    def test_one_probability_edge_always_activates(self):
        self.assertEqual(m.verify_complete_distribution(2,((0,1,F(1)),),(0,)),
                         {frozenset((0,1)):F(1)})

    def test_zero_probability_first_link_blocks_later_deterministic_link(self):
        edges=((0,1,F(0)),(1,2,F(1)))
        self.assertEqual(m.verify_complete_distribution(3,edges,(0,)),
                         {frozenset((0,)):F(1)})

    def test_deterministic_path_always_fully_activates(self):
        edges=((0,1,F(1)),(1,2,F(1)),(2,3,F(1)))
        self.assertEqual(m.verify_complete_distribution(4,edges,(0,)),
                         {frozenset((0,1,2,3)):F(1)})

    def test_timed_path_new_frontier_next_round_only(self):
        self.assertEqual(m.deterministic_three_round_trace(),
                         (frozenset((0,)),frozenset((0,1)),frozenset((0,1,2))))

    def test_direct_success_and_indirect_path_do_not_count_twice(self):
        edges=((0,1,F(1)),(1,2,F(1)),(0,2,F(1)))
        self.assertEqual(m.verify_complete_distribution(3,edges,(0,)),
                         {frozenset((0,1,2)):F(1)})

    def test_two_successful_same_round_attempts_activate_target_once(self):
        edges=((0,2,F(1)),(1,2,F(1)))
        x=m.verify_complete_distribution(3,edges,(0,1))
        self.assertEqual(x,{frozenset((0,1,2)):F(1)})
        self.assertEqual(m.expected_final_count(x),3)

    def test_two_incoming_sources_probability_or_independent(self):
        x=m.fixed_primary_mechanism_cases()
        self.assertEqual(x["both_sources_target_activation_probability"],"5/8")

    def test_first_source_to_target_half(self):
        x=m.fixed_primary_mechanism_cases()
        self.assertEqual(x["single_source0_expected"],"3/2")

    def test_second_source_to_target_quarter(self):
        x=m.fixed_primary_mechanism_cases()
        self.assertEqual(x["single_source1_expected"],"5/4")

    def test_double_seed_three_nodes_expected_twenty_one_eighths(self):
        x=m.fixed_primary_mechanism_cases()
        self.assertEqual(x["both_sources_expected"],"21/8")

    def test_IC_both_incoming_live_simultaneously_can_happen(self):
        self.assertEqual(m.fixed_primary_mechanism_cases()["both_edges_live_joint_probability"],"1/8")

    def test_IC_vs_LT_same_marginal_edges_not_same_two_seed_expectation(self):
        x=m.fixed_primary_mechanism_cases()
        self.assertEqual(x["same_weights_as_LT_R120_both_sources_expected"],"11/4")
        self.assertNotEqual(x["both_sources_expected"],x["same_weights_as_LT_R120_both_sources_expected"])
        self.assertTrue(x["IC_vs_LT_random_edge_construction_different"])

    def test_four_node_weighted_chain_expected_twenty_five_twelfths(self):
        x=m.fixed_primary_mechanism_cases()
        self.assertEqual(x["four_chain_seed0_expected"],"25/12")

    def test_four_node_chain_final_node_probability_one_quarter(self):
        x=m.fixed_primary_mechanism_cases()
        self.assertEqual(x["four_chain_last_node_probability"],"1/4")

    def test_three_node_directed_cycle_exact_seven_fourths(self):
        x=m.fixed_primary_mechanism_cases()
        self.assertEqual(x["three_cycle_seed0_expected"],"7/4")

    def test_directed_cycle_no_retry_after_self_already_activated(self):
        edges=((0,1,F(1)),(1,2,F(1)),(2,0,F(1)))
        self.assertEqual(m.verify_complete_distribution(3,edges,(0,)),
                         {frozenset((0,1,2)):F(1)})

    def test_reverse_directed_edges_are_distinct(self):
        edges=((0,1,F(1,2)),(1,0,F(3,4)))
        x=m.verify_complete_distribution(2,edges,(0,))
        self.assertEqual(x,{frozenset((0,)):F(1,2),frozenset((0,1)):F(1,2)})

    def test_both_solvers_normalized_exact_one(self):
        edges=((0,1,F(1,3)),(0,2,F(1,4)),(1,2,F(2,3)))
        for solver in (m.exact_one_chance_round_distribution,m.exact_independent_live_edge_distribution):
            self.assertEqual(sum(solver(3,edges,(0,)).values(),F(0)),1)

    def test_full_distribution_not_just_expected_matches(self):
        edges=((0,1,F(1,3)),(1,2,F(2,3)),(0,2,F(1,4)))
        self.assertEqual(m.exact_one_chance_round_distribution(3,edges,(0,)),
                         m.exact_independent_live_edge_distribution(3,edges,(0,)))

    def test_round_solver_does_not_call_live_edge_solver(self):
        with patch.object(m,"exact_independent_live_edge_distribution",
                          side_effect=AssertionError("LIVE_FORBIDDEN")):
            self.assertEqual(m.exact_one_chance_round_distribution(
                2,((0,1,F(1,2)),),(0,))[frozenset((0,1))],F(1,2))

    def test_live_edge_solver_does_not_call_round_solver(self):
        with patch.object(m,"exact_one_chance_round_distribution",
                          side_effect=AssertionError("ROUND_FORBIDDEN")):
            self.assertEqual(m.exact_independent_live_edge_distribution(
                2,((0,1,F(1,2)),),(0,))[frozenset((0,1))],F(1,2))

    def test_expected_count_exact_fraction(self):
        x={frozenset((0,)):F(1,4),frozenset((0,1)):F(3,4)}
        self.assertEqual(m.expected_final_count(x),F(7,4))

    def test_expected_count_rejects_wrong_mass_or_type(self):
        for bad in ({frozenset((0,)):F(1,2)},
                    {frozenset((0,)):0.5,frozenset((0,1)):0.5},
                    {frozenset((0,)):-F(1)}):
            with self.subTest(v=bad),self.assertRaises(m.CascadeAuditError):
                m.expected_final_count(bad)

    def test_expected_count_rejects_non_frozenset_keys(self):
        with self.assertRaises(m.CascadeAuditError):
            m.expected_final_count({(0,):F(1)})

    def test_no_seed_returns_zero_expected_influence(self):
        edges=((0,1,F(1)),(1,2,F(1)))
        self.assertEqual(m.expected_final_count(m.verify_complete_distribution(3,edges,())),0)

    def test_expected_influence_monotone_and_submodular_for_triangle(self):
        edges=((0,1,F(1,2)),(1,2,F(2,3)),(0,2,F(1,4)))
        self.assertTrue(m.check_monotone_submodular_expected(m.all_seed_expected_influence(3,edges)))

    def test_checker_rejects_bogus_supermodular_map(self):
        influence={frozenset():F(0),frozenset((0,)):F(1),
                   frozenset((1,)):F(1),frozenset((0,1)):F(3)}
        with self.assertRaisesRegex(m.CascadeAuditError,"NOT_SUBMODULAR"):
            m.check_monotone_submodular_expected(influence)

    def test_checker_rejects_incomplete_seed_powerset(self):
        influence={frozenset():F(0),frozenset((0,)):F(1),
                   frozenset((0,1)):F(2)}
        with self.assertRaises(m.CascadeAuditError):
            m.check_monotone_submodular_expected(influence)

    def test_full_n_to_three_graph_seed_probability_comparison_1060(self):
        self.assertEqual(m.exhaustive_small_directed_graphs(),
                         {"1":4,"2":32,"3":1024})

    def test_original_paper_2003_doi_and_citation_present(self):
        self.assertIn("doi:10.1145/956750.956769",m.__doc__)

    def test_probability_types_float_int_boolean_rejected(self):
        for bad in (0.5,1,True,False,"1/2",None):
            with self.subTest(bad=bad),self.assertRaises(m.CascadeAuditError):
                m.validate(2,((0,1,bad),),(0,))

    def test_probability_out_of_range_rejected(self):
        for bad in (F(-1,2),F(3,2)):
            with self.subTest(bad=bad),self.assertRaises(m.CascadeAuditError):
                m.validate(2,((0,1,bad),),(0,))

    def test_graph_n_bounds_types_rejected(self):
        for bad in (0,6,-1,True,1.0,"3"):
            with self.subTest(bad=bad),self.assertRaises(m.CascadeAuditError):
                m.validate(bad,(),())

    def test_directed_edges_self_loop_rejected(self):
        with self.assertRaisesRegex(m.CascadeAuditError,"NO_SELF_LOOPS"):
            m.validate(2,((0,0,F(1,2)),),(0,))

    def test_duplicate_directed_edges_rejected(self):
        with self.assertRaisesRegex(m.CascadeAuditError,"DUPLICATE_DIRECTED_EDGE"):
            m.validate(2,((0,1,F(1,2)),(0,1,F(1,4))),(0,))

    def test_invalid_edge_length_rejected(self):
        for bad in ((0,1),(0,1,F(1),F(0)),"010"):
            with self.subTest(edge=bad),self.assertRaises(m.CascadeAuditError):
                m.validate(2,(bad,),(0,))

    def test_invalid_edge_node_rejected(self):
        for bad in (-1,2,False,True,0.0,"0"):
            with self.subTest(edge_node=bad),self.assertRaises(m.CascadeAuditError):
                m.validate(2,((bad,1,F(1)),),(0,))

    def test_invalid_seeds_rejected(self):
        for bad in ((-1,),(2,),(False,),(True,),("0",),(0,0)):
            with self.subTest(seeds=bad),self.assertRaises(m.CascadeAuditError):
                m.validate(2,(),bad)

    def test_bad_edges_and_seed_container_rejected(self):
        for edges,seeds in ((iter([]),()),((),iter([])),("nothing",())):
            with self.subTest(t=str(type(edges))),self.assertRaises(m.CascadeAuditError):
                m.validate(2,edges,seeds)

    def test_more_than_twelve_edges_fails_closed(self):
        edges=tuple((u,v,F(1,2)) for u in range(5) for v in range(5) if u!=v)
        with self.assertRaisesRegex(m.CascadeAuditError,"AT_MOST_12"):
            m.validate(5,edges,(0,))

    def test_one_chance_binary_event_outcomes_exclude_zero_mass(self):
        self.assertEqual(m._bernoulli_outcomes(F(0)),((False,F(1)),))
        self.assertEqual(m._bernoulli_outcomes(F(1)),((True,F(1)),))

    def test_no_real_human_E2_and_frozen_baseline(self):
        x=m.fixed_primary_mechanism_cases()
        self.assertEqual(x["human_E2_observations"],0)
        self.assertEqual(x["PESEN_v0_1"],"FROZEN")
        self.assertEqual(x["R073"],"FROZEN")

    def test_deterministic_repeated_replay(self):
        e=((0,1,F(1,2)),(1,2,F(1,2)))
        self.assertEqual(m.verify_complete_distribution(3,e,(0,)),m.verify_complete_distribution(3,e,(0,)))


if __name__=="__main__":
    unittest.main()
