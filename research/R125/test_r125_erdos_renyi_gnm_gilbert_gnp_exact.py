"""R125 original 1959 ER and Gilbert source-grounded exact finite math tests."""
import unittest
from fractions import Fraction as F
from math import comb
from unittest.mock import patch

import r125_erdos_renyi_gnm_gilbert_gnp_exact as m


class Primary1959FixedVsIndependentRandomGraphs(unittest.TestCase):
    def test_erdos_source_1959_exactly_m_model_description(self):
        self.assertIn("Erdős & Rényi",m.__doc__)
        self.assertIn("exactly",m.__doc__)

    def test_gilbert_source_1959_independent_bernoulli_description(self):
        self.assertIn("E N Gilbert",m.__doc__)
        self.assertIn("Bernoulli",m.__doc__)

    def test_n1_no_possible_edges(self):
        self.assertEqual(m.candidate_edges(1),())

    def test_n4_six_possible_simple_edges(self):
        self.assertEqual(len(m.candidate_edges(4)),6)

    def test_n5_ten_possible_simple_edges(self):
        self.assertEqual(len(m.candidate_edges(5)),10)

    def test_n4_complete_graph_6_edges(self):
        x=m.graph_properties(4,m.candidate_edges(4))
        self.assertEqual((x["edges"],x["connected"],x["component_count"]),(6,True,1))

    def test_n4_empty_graph_is_four_isolates(self):
        x=m.graph_properties(4,())
        self.assertEqual((x["largest_component"],x["isolates"],x["component_count"]),(1,4,4))

    def test_n4_triangle_plus_isolate_largest_three(self):
        x=m.graph_properties(4,((0,1),(0,2),(1,2)))
        self.assertEqual((x["largest_component"],x["isolates"],x["connected"]),(3,1,False))

    def test_n4_tree_has_zero_isolates_and_connected(self):
        x=m.graph_properties(4,((0,1),(1,2),(2,3)))
        self.assertEqual((x["largest_component"],x["isolates"],x["connected"]),(4,0,True))

    def test_n4_graph_edge_order_and_undirected_orientation_irrelevant(self):
        a=m.graph_properties(4,((0,1),(1,2),(2,3)))
        b=m.graph_properties(4,((3,2),(2,1),(1,0)))
        self.assertEqual(a,b)

    def test_n4_fixed_m3_twenty_equiprobable_graphs(self):
        x=m.full_exact_gnm_edge_conditioned_distribution(4,3)
        self.assertEqual((x["graph_count"],x["total_mass"]),(20,1))

    def test_n4_fixed_m3_connected_sixteen_of_twenty(self):
        x=m.full_exact_gnm_edge_conditioned_distribution(4,3)
        self.assertEqual(x["connectivity_probability"],F(4,5))
        self.assertEqual(x["graph_count"]*x["connectivity_probability"],16)

    def test_n4_fixed_m3_four_triangles_with_isolates(self):
        x=m.full_exact_gnm_edge_conditioned_distribution(4,3)
        self.assertEqual(x["expected_isolates"],F(1,5))
        self.assertEqual(x["largest_component_distribution"],{3:F(1,5),4:F(4,5)})

    def test_n4_independent_half_connected_thirtyeight_of_sixtyfour(self):
        x=m.full_exact_gnp_graph_distribution(4,F(1,2))
        self.assertEqual(x["connectivity_probability"],F(19,32))
        self.assertEqual(x["graph_count"]*x["connectivity_probability"],38)

    def test_n4_gilbert_original_recursion_equals_nineteen_thirtyseconds(self):
        self.assertEqual(m.independent_gilbert1959_connected_recurrence(4,F(1,2)),F(19,32))

    def test_gilbert_recursion_never_calls_graph_enumerator(self):
        with patch.object(m,"all_labeled_graphs",side_effect=AssertionError("NOT_ALLOWED")):
            self.assertEqual(m.independent_gilbert1959_connected_recurrence(4,F(1,2)),F(19,32))

    def test_fixed_m_vs_independent_p_same_average_edges_different_connectivity(self):
        fixed=m.full_exact_gnm_edge_conditioned_distribution(4,3)
        rand=m.full_exact_gnp_graph_distribution(4,F(1,2))
        self.assertNotEqual(fixed["connectivity_probability"],rand["connectivity_probability"])

    def test_fixed_m3_edge_count_variance_zero(self):
        self.assertEqual(m.gnm_edge_count_moments(4,3),{"mean":F(3),"variance":F(0)})

    def test_independent_p_half_edges_mean_three_variance_three_halves(self):
        self.assertEqual(m.gnp_edge_count_moments(4,F(1,2)),{"mean":F(3),"variance":F(3,2)})

    def test_conditional_edge_count_three_has_five_sixteenths_probability(self):
        self.assertEqual(m.gnp_edge_count_mass(4,F(1,2),3),F(5,16))

    def test_fixed_specific_three_edge_graph_mass_one_twentieth(self):
        edges=((0,1),(0,2),(1,2))
        self.assertEqual(m.gnm_graph_mass(4,3,edges),F(1,20))

    def test_independent_specific_three_edge_graph_mass_one_sixtyfourth(self):
        edges=((0,1),(0,2),(1,2))
        self.assertEqual(m.gnp_graph_mass(4,F(1,2),edges),F(1,64))

    def test_Condition_on_three_edges_equals_uniform_one_twentieth(self):
        edges=((0,1),(0,2),(1,2))
        self.assertEqual(m.gnp_conditional_on_edge_count_mass(4,F(1,2),3,edges),F(1,20))

    def test_conditional_non_matching_graph_mass_zero(self):
        edges=((0,1),)
        self.assertEqual(m.gnp_conditional_on_edge_count_mass(4,F(1,2),3,edges),F(0))

    def test_prob_zero_conditioning_on_positive_edge_count_is_undefined(self):
        with self.assertRaisesRegex(m.RandomGraphAuditError,"ZERO_PROBABILITY"):
            m.gnp_conditional_on_edge_count_mass(4,F(0),3,((0,1),(0,2),(1,2)))

    def test_prob_one_conditioning_on_noncomplete_edge_count_is_undefined(self):
        with self.assertRaisesRegex(m.RandomGraphAuditError,"ZERO_PROBABILITY"):
            m.gnp_conditional_on_edge_count_mass(4,F(1),3,((0,1),(0,2),(1,2)))

    def test_prob_zero_all_edges_absent_almost_surely(self):
        x=m.full_exact_gnp_graph_distribution(4,F(0))
        self.assertEqual(x["largest_component_distribution"],{1:F(1)})
        self.assertEqual(x["connectivity_probability"],0)

    def test_prob_one_all_edges_present_almost_surely(self):
        x=m.full_exact_gnp_graph_distribution(4,F(1))
        self.assertEqual(x["largest_component_distribution"],{4:F(1)})
        self.assertEqual(x["connectivity_probability"],1)

    def test_n1_connected_even_with_no_edges(self):
        self.assertTrue(m.graph_properties(1,())["connected"])
        self.assertEqual(m.independent_gilbert1959_connected_recurrence(1,F(0)),1)

    def test_empty_edges_n4_under_fixed_m_zero_mass_one(self):
        x=m.full_exact_gnm_edge_conditioned_distribution(4,0)
        self.assertEqual((x["graph_count"],x["connectivity_probability"],x["expected_isolates"]),(1,0,4))

    def test_complete_edges_n4_fixed_m6_connected_certain(self):
        x=m.full_exact_gnm_edge_conditioned_distribution(4,6)
        self.assertEqual((x["graph_count"],x["connectivity_probability"],x["expected_isolates"]),(1,1,0))

    def test_n4_independent_expected_isolates_one_half(self):
        x=m.full_exact_gnp_graph_distribution(4,F(1,2))
        self.assertEqual(x["expected_isolates"],F(1,2))

    def test_n4_independent_isolates_analytic_versus_enum_exact(self):
        self.assertEqual(m.gnp_expected_isolates(4,F(1,2)),F(1,2))

    def test_fixed_m3_vs_independent_same_expected_edges_isolates_differ(self):
        a=m.full_exact_gnm_edge_conditioned_distribution(4,3)
        b=m.full_exact_gnp_graph_distribution(4,F(1,2))
        self.assertEqual((a["expected_isolates"],b["expected_isolates"]),(F(1,5),F(1,2)))

    def test_n4_degree_zero_random_bernoulli_binomial_distribution(self):
        x=m.full_exact_gnp_graph_distribution(4,F(1,2))
        self.assertEqual(x["degree_zero_distribution"],{0:F(1,8),1:F(3,8),2:F(3,8),3:F(1,8)})

    def test_n4_degree_zero_fixed_m3_is_hypergeometric(self):
        x=m.full_exact_gnm_edge_conditioned_distribution(4,3)
        self.assertEqual(x["degree_zero_distribution"],{0:F(1,20),1:F(9,20),2:F(9,20),3:F(1,20)})

    def test_general_gnp_binomial_degree_formula_sums_one(self):
        for n in range(1,6):
            self.assertEqual(sum((m.gnp_degree_zero_mass(n,F(1,3),k) for k in range(n)),F(0)),1)

    def test_general_gnm_hypergeom_degree_formula_sums_one(self):
        for n in range(1,6):
            for edges in range(len(m.candidate_edges(n))+1):
                with self.subTest(n=n,m=edges):
                    self.assertEqual(sum((m.gnm_degree_zero_mass(n,edges,k) for k in range(n)),F(0)),1)

    def test_uniform_graphs_fixed_edge_count_distribution_normalizes(self):
        for edge_count in range(7):
            with self.subTest(m=edge_count):
                self.assertEqual(m.full_exact_gnm_edge_conditioned_distribution(4,edge_count)["total_mass"],1)

    def test_all_1099_exact_graphs_and_4396_gnp_weights(self):
        x=m.audit_all_small_graphs()
        self.assertEqual(x["enumerated_graphs_by_n"],{"1":1,"2":2,"3":8,"4":64,"5":1024})
        self.assertEqual(x["unique_labeled_graphs_total"],1099)
        self.assertEqual(x["Gnp_graph_probability_weighings_total"],4396)

    def test_all_25_fixed_edge_probability_buckets_are_valid(self):
        x=m.audit_all_small_graphs()
        self.assertEqual(x["Gnm_fixed_m_distribution_buckets_by_n"],{"1":1,"2":2,"3":4,"4":7,"5":11})
        self.assertEqual(x["Gnm_distribution_bucket_count"],25)

    def test_audit_confirms_Gnp_conditioned_on_m_equals_Gnm(self):
        self.assertTrue(m.audit_all_small_graphs()[
            "same_exact_distribution_Gnp_conditioned_edge_count_as_Gnm_all_valid_n_m"])

    def test_graph_rejects_duplicate_undirected_reverse_edges(self):
        with self.assertRaisesRegex(m.RandomGraphAuditError,"DUPLICATE"):
            m.validate_edges(3,((0,1),(1,0)))

    def test_graph_rejects_self_loops(self):
        with self.assertRaisesRegex(m.RandomGraphAuditError,"SELF_LOOPS"):
            m.validate_edges(2,((0,0),))

    def test_graph_rejects_bad_edge_arity(self):
        for e in ((0,1,2),(0,),"0,1"):
            with self.subTest(e=e),self.assertRaises(m.RandomGraphAuditError):
                m.validate_edges(2,(e,))

    def test_graph_rejects_bool_invalid_or_float_node(self):
        for v in (True,False,-1,4,1.0,"1",None):
            with self.subTest(v=v),self.assertRaises(m.RandomGraphAuditError):
                m.validate_edges(4,((0,v),))

    def test_graph_rejects_generator_edge_container(self):
        with self.assertRaises(m.RandomGraphAuditError):
            m.validate_edges(3,(pair for pair in ((0,1),)))

    def test_invalid_n_outside_1_to5_strict_integer(self):
        for n in (0,6,-1,True,2.0,"3"):
            with self.subTest(n=n),self.assertRaises(m.RandomGraphAuditError):
                m.candidate_edges(n)

    def test_invalid_p_float_int_bool_negative_above_one(self):
        for p in (0,1,0.5,True,False,F(-1,4),F(5,4),"1/2"):
            with self.subTest(p=p),self.assertRaises(m.RandomGraphAuditError):
                m.gnp_graph_mass(2,p,())

    def test_invalid_m_out_of_range_bool_float(self):
        for value in (-1,7,True,False,2.0,"3"):
            with self.subTest(m=value),self.assertRaises(m.RandomGraphAuditError):
                m.gnm_graph_mass(4,value,())

    def test_bad_degree_index_type_or_range(self):
        for j in (True,False,-1,4,1.0,"0"):
            with self.subTest(j=j),self.assertRaises(m.RandomGraphAuditError):
                m.gnp_degree_zero_mass(4,F(1,2),j)
            with self.subTest(j=j),self.assertRaises(m.RandomGraphAuditError):
                m.gnm_degree_zero_mass(4,3,j)

    def test_frozen_four_person_audit_source_distinctions(self):
        v=m.frozen_four_vertex_comparison()
        self.assertEqual(v["Gnm_m3_number_of_possible_graphs"],20)
        self.assertEqual(v["Gnm_m3_connected_graphs"],16)
        self.assertEqual(v["Gnp_p_half_connected_graphs"],38)
        # R125-CORR-002: successful math must still serialize machine receipts.
        self.assertIs(type(v["Gnm_m3_connected_graphs"]),int)
        self.assertIs(type(v["Gnp_p_half_connected_graphs"]),int)
        self.assertEqual(v["Gnm_m3_connectivity"],"4/5")
        self.assertEqual(v["Gnp_p_half_connectivity"],"19/32")

    def test_random_connectivity_not_equal_to_giant_component_threshold(self):
        r=m.full_exact_gnp_graph_distribution(4,F(1,2))
        self.assertEqual(r["largest_component_distribution"][4],r["connectivity_probability"])
        self.assertNotEqual(r["largest_component_distribution"][3],0)

    def test_repeated_exact_math_determinism(self):
        self.assertEqual(m.frozen_four_vertex_comparison(),m.frozen_four_vertex_comparison())


if __name__=="__main__":
    unittest.main()
