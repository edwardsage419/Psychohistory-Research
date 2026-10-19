"""R120 author 2003 threshold/live-edge FULL SET distribution equivalence, no humans."""
import unittest
from fractions import Fraction as F
from unittest.mock import patch
import r120_kkt_2003_uniform_linear_threshold_exact as m


class KKTLinearThresholdSourceTests(unittest.TestCase):
    def test_graph_empty_edges_valid(self):
        inc,s=m._inputs(3,(),())
        self.assertEqual(inc,((),(),()))
        self.assertEqual(s,frozenset())

    def test_seed_collection_empty_valid(self):
        self.assertEqual(m.synchronous_fixed_threshold(2,(),(),(F(1),F(1)))["active"],frozenset())

    def test_zero_weight_edge_never_causes_activation(self):
        edge=((0,1,F(0)),)
        self.assertEqual(m.synchronous_fixed_threshold(2,edge,(0,),(F(1),F(1)))["active"],frozenset((0,)))

    def test_fixed_exact_threshold_equality_causes_activation(self):
        edge=((0,1,F(1,2)),)
        self.assertEqual(m.synchronous_fixed_threshold(2,edge,(0,),(F(1),F(1,2)))["active"],frozenset((0,1)))

    def test_fixed_threshold_above_incoming_weight_not_active(self):
        edge=((0,1,F(1,2)),)
        self.assertEqual(m.synchronous_fixed_threshold(2,edge,(0,),(F(1),F(3,4)))["active"],frozenset((0,)))

    def test_fixed_irreversible_three_node_chain(self):
        e=((0,1,F(1)),(1,2,F(1)))
        x=m.synchronous_fixed_threshold(3,e,(0,),(F(1),)*3)
        self.assertEqual(x["history"],(frozenset((0,)),frozenset((0,1)),frozenset((0,1,2))))

    def test_source_single_target_incoming_sum_exact_three_quarters(self):
        e=((0,2,F(1,2)),(1,2,F(1,4)))
        inc,_=m._inputs(3,e,(0,))
        self.assertEqual(sum((v for _,v in inc[2]),F(0)),F(3,4))

    def test_single_target_seed0_probability_half(self):
        e=((0,2,F(1,2)),(1,2,F(1,4)))
        x=m.exact_threshold_distribution(3,e,(0,))
        self.assertEqual(x,{frozenset((0,)):F(1,2),frozenset((0,2)):F(1,2)})

    def test_single_target_seed1_probability_quarter(self):
        e=((0,2,F(1,2)),(1,2,F(1,4)))
        x=m.exact_threshold_distribution(3,e,(1,))
        self.assertEqual(x,{frozenset((1,)):F(3,4),frozenset((1,2)):F(1,4)})

    def test_source_fixture_seed0_sigma_three_halves(self):
        self.assertEqual(m.source_analytic_fixtures()["single_node_probability_nonlinearity"]["seed_0"],"3/2")

    def test_source_fixture_seed1_sigma_five_quarters(self):
        e=((0,2,F(1,2)),(1,2,F(1,4)))
        self.assertEqual(m.expected_influence(m.verify_distribution_equivalence(3,e,(1,))),F(5,4))

    def test_source_fixture_both_seed_sigma_eleven_quarters(self):
        e=((0,2,F(1,2)),(1,2,F(1,4)))
        self.assertEqual(m.expected_influence(m.verify_distribution_equivalence(3,e,(0,1))),F(11,4))

    def test_target_no_live_edge_has_exact_quarter_probability(self):
        e=((0,2,F(1,2)),(1,2,F(1,4)))
        inc,_=m._inputs(3,e,())
        options=m._live_edge_options(inc)
        self.assertEqual(dict(options[2]),{0:F(1,2),1:F(1,4),None:F(1,4)})

    def test_live_edge_chooses_one_parent_not_independent_each_edge(self):
        e=((0,2,F(1,2)),(1,2,F(1,4)))
        inc,_=m._inputs(3,e,())
        self.assertEqual(len(m._live_edge_options(inc)[2]),3)
        self.assertEqual(sum((p for _,p in m._live_edge_options(inc)[2]),F(0)),1)

    def test_original_claim_live_edge_equals_threshold_FULL_distribution(self):
        e=((0,2,F(1,2)),(1,2,F(1,4)))
        for seeds in ((0,),(1,),(0,1),(2,),()):
            with self.subTest(seeds=seeds):
                self.assertEqual(m.exact_threshold_distribution(3,e,seeds),
                                 m.exact_live_edge_distribution(3,e,seeds))

    def test_no_live_edge_when_one_incoming_weight_is_one(self):
        inc,_=m._inputs(2,((0,1,F(1)),),())
        self.assertEqual(m._live_edge_options(inc)[1],((0,F(1)),))

    def test_no_edges_none_parent_probability_one(self):
        inc,_=m._inputs(3,(),())
        self.assertEqual(m._live_edge_options(inc),(((None,F(1)),),)*3)

    def test_zero_edge_weight_ignored_in_live_edge(self):
        inc,_=m._inputs(2,((0,1,F(0)),),())
        self.assertEqual(m._live_edge_options(inc)[1],((None,F(1)),))

    def test_uniform_threshold_exact_interval_weights_sum_one(self):
        inc,_=m._inputs(3,((0,2,F(1,2)),(1,2,F(1,4))),())
        regions=m._threshold_regions(inc)
        self.assertEqual(regions[2],(
            (F(1,8),F(1,4)),(F(3,8),F(1,4)),(F(5,8),F(1,4)),(F(7,8),F(1,4))
        ))

    def test_four_node_weighted_chain_exact_25_over_12(self):
        e=((0,1,F(1,2)),(1,2,F(2,3)),(2,3,F(3,4)))
        dist=m.verify_distribution_equivalence(4,e,(0,))
        self.assertEqual(m.expected_influence(dist),F(25,12))

    def test_four_node_chain_probability_last_activated_one_quarter(self):
        e=((0,1,F(1,2)),(1,2,F(2,3)),(2,3,F(3,4)))
        d=m.verify_distribution_equivalence(4,e,(0,))
        self.assertEqual(sum((p for nodes,p in d.items() if 3 in nodes),F(0)),F(1,4))

    def test_directed_cycle_3_nodes_exact_seven_quarters(self):
        e=((0,1,F(1,2)),(1,2,F(1,2)),(2,0,F(1,2)))
        self.assertEqual(m.expected_influence(m.verify_distribution_equivalence(3,e,(0,))),F(7,4))

    def test_directed_cycle_full_active_set_probability_quarter(self):
        e=((0,1,F(1,2)),(1,2,F(1,2)),(2,0,F(1,2)))
        d=m.verify_distribution_equivalence(3,e,(0,))
        self.assertEqual(d[frozenset((0,1,2))],F(1,4))

    def test_zero_seeds_no_spontaneous_activation_with_positive_threshold(self):
        e=((0,1,F(1)),(1,0,F(1)))
        self.assertEqual(m.verify_distribution_equivalence(2,e,()),{frozenset():F(1)})

    def test_all_nodes_seeds_always_all_active(self):
        e=((0,1,F(1,3)),)
        self.assertEqual(m.verify_distribution_equivalence(2,e,(0,1)),{frozenset((0,1)):F(1)})

    def test_original_author_expected_influence_submodular_sample(self):
        e=((0,1,F(1,2)),(1,2,F(1,2)),(2,0,F(1,2)))
        self.assertTrue(m.verify_monotone_submodular(m.all_seed_influence(3,e)))

    def test_fixed_threshold_can_fail_submodularity(self):
        a=m.fixed_threshold_failure_of_submodularity()
        self.assertEqual([a["fixed_empty"],a["fixed_seed0"],a["fixed_seed1"],a["fixed_both"]],[0,1,1,3])
        self.assertLess(a["fixed_marginal_seed0_without_seed1"],
                        a["fixed_marginal_seed0_with_seed1"])

    def test_uniform_expected_sigma_does_not_share_fixed_nonsubmodularity(self):
        a=m.fixed_threshold_failure_of_submodularity()
        self.assertEqual(a["expected_marginal_seed0_without_seed1"],"3/2")
        self.assertEqual(a["expected_marginal_seed0_with_seed1"],"3/2")

    def test_exact_submodularity_checker_rejects_bogus_function(self):
        fake={frozenset():F(0),frozenset((0,)):F(1),frozenset((1,)):F(1),frozenset((0,1)):F(3)}
        with self.assertRaisesRegex(m.LinearThresholdError,"NOT_SUBMODULAR"):
            m.verify_monotone_submodular(fake)

    def test_influence_calculator_rejects_missing_probability_mass(self):
        with self.assertRaises(m.LinearThresholdError):
            m.expected_influence({frozenset((0,)):F(1,2)})

    def test_influence_calculator_rejects_float_probability(self):
        with self.assertRaises(m.LinearThresholdError):
            m.expected_influence({frozenset((0,)):1.0})

    def test_seed_power_set_required_for_expected_submodularity(self):
        with self.assertRaises(m.LinearThresholdError):
            m.verify_monotone_submodular({frozenset():F(0),frozenset((0,)):F(1),frozenset((0,1)):F(2)})

    def test_nonuniform_or_invalid_threshold_disallowed(self):
        for bad in (0,0.5,True,F(0),F(-1,2),F(3,2)):
            with self.subTest(value=bad),self.assertRaises(m.LinearThresholdError):
                m.synchronous_fixed_threshold(2,(),(0,),(F(1),bad))

    def test_incoming_edges_sum_over_one_is_rejected(self):
        with self.assertRaisesRegex(m.LinearThresholdError,"EXCEEDS_ONE"):
            m._inputs(3,((0,2,F(3,4)),(1,2,F(3,4))),())

    def test_edge_weight_fraction_only_and_in_unit_interval(self):
        for bad in (1,0.4,True,F(-1,2),F(3,2)):
            with self.subTest(value=bad),self.assertRaises(m.LinearThresholdError):
                m._inputs(2,((0,1,bad),),())

    def test_duplicate_directed_edge_rejected(self):
        with self.assertRaisesRegex(m.LinearThresholdError,"DUPLICATE_DIRECTED_EDGE"):
            m._inputs(2,((0,1,F(1,4)),(0,1,F(1,4))),())

    def test_opposing_directed_edges_are_different_edges(self):
        inc,_=m._inputs(2,((0,1,F(1,2)),(1,0,F(1,2))),())
        self.assertEqual(len(inc[0]),1)
        self.assertEqual(len(inc[1]),1)

    def test_self_edge_rejected(self):
        with self.assertRaisesRegex(m.LinearThresholdError,"SELF_LOOP"):
            m._inputs(2,((0,0,F(1)),),())

    def test_malformed_edges_and_nodes_rejected(self):
        for edge in ((0,1),(0,1,F(1),F(0)),(True,1,F(1)),(0,2,F(1)),("0",1,F(1))):
            with self.subTest(edge=edge),self.assertRaises(m.LinearThresholdError):
                m._inputs(2,(edge,),())

    def test_n_must_be_strict_small_integer(self):
        for bad in (0,7,True,1.,-1,"3"):
            with self.subTest(value=bad),self.assertRaises(m.LinearThresholdError):
                m._inputs(bad,(),())

    def test_seed_types_duplicates_and_out_of_range_denied(self):
        for bad in ((False,),(True,),(3,),(-1,),("0",),(0,0)):
            with self.subTest(value=bad),self.assertRaises(m.LinearThresholdError):
                m._inputs(2,(),bad)

    def test_bad_containers_rejected(self):
        for edges,seeds in ((set(),"x"),(iter([]),()),((),(i for i in [0]))):
            with self.subTest(edges=str(type(edges)),seeds=str(type(seeds))),self.assertRaises(m.LinearThresholdError):
                m._inputs(2,edges,seeds)

    def test_exact_three_node_all_digraphs_all_seed_full_distribution_equivalence(self):
        self.assertEqual(m.all_three_node_digraphs(),{"1":2,"2":16,"3":512})

    def test_study_is_pure_mathematics_not_human_E2(self):
        self.assertTrue(m.__doc__.find("No human behaviors")>=0)
        self.assertEqual(sum(m.all_three_node_digraphs().values()),530)

    def test_repeated_exact_expected_determinism(self):
        e=((0,2,F(1,2)),(1,2,F(1,4)))
        self.assertEqual(m.verify_distribution_equivalence(3,e,(0,)),m.verify_distribution_equivalence(3,e,(0,)))


if __name__=="__main__":
    unittest.main()
