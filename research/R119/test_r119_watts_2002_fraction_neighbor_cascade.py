"""R119 first-party Watts source mathematical finite and infinite branch checks."""
import unittest
from fractions import Fraction as F
from itertools import combinations
from unittest.mock import patch
import r119_watts_2002_fraction_neighbor_cascade as m

H=F(1,2)


class WattsFractionalNeighborThresholdTests(unittest.TestCase):
    def test_original_primary_DOI(self):
        self.assertEqual(m.study_receipt.__module__,"r119_watts_2002_fraction_neighbor_cascade")

    def test_path_six_from_endpoint_reaches_all(self):
        path=tuple((i,i+1) for i in range(5))
        self.assertEqual(m.validate_final_closure(6,path,(H,)*6,0)["size"],6)

    def test_star_leaf_cannot_activate_high_degree_center(self):
        edges=tuple((0,i) for i in range(1,6))
        x=m.validate_final_closure(6,edges,(H,)*6,1)
        self.assertEqual(x["active"],frozenset((1,)))

    def test_star_center_activates_all_five_leaves(self):
        edges=tuple((0,i) for i in range(1,6))
        self.assertEqual(m.validate_final_closure(6,edges,(H,)*6,0)["size"],6)

    def test_six_cycle_one_seed_reaches_all(self):
        edges=tuple((i,(i+1)%6) for i in range(6))
        self.assertEqual(m.validate_final_closure(6,edges,(H,)*6,0)["size"],6)

    def test_two_triangles_equal_degrees_but_only_three(self):
        edges=((0,1),(1,2),(0,2),(3,4),(4,5),(3,5))
        self.assertEqual(m.validate_final_closure(6,edges,(H,)*6,0)["size"],3)
        degree,_=m.degree_profile(6,edges,(H,)*6,0)
        self.assertEqual(degree,(2,)*6)

    def test_same_degree_sequences_different_final_cascades(self):
        x=m.frozen_network_counterexamples()
        self.assertTrue(x["cycle_and_triangles_same_degree_multiset"])
        self.assertEqual(x["final_sizes"]["cycle_seed_0"],6)
        self.assertEqual(x["final_sizes"]["two_triangles_seed_0"],3)

    def test_same_edge_count_path_star_different_effect_from_leaf_seed(self):
        x=m.frozen_network_counterexamples()
        self.assertTrue(x["path_and_star_same_edge_count"])
        self.assertEqual(x["final_sizes"]["path_seed_endpoint"],6)
        self.assertEqual(x["final_sizes"]["star_seed_leaf"],1)

    def test_diamond_stable_node_needs_two_active_neighbors(self):
        edges=((0,1),(0,2),(1,3),(2,3))
        thresholds=(H,H,H,F(3,4))
        v=m.validate_final_closure(4,edges,thresholds,0)
        self.assertEqual(v["history"],(frozenset([0]),frozenset([0,1,2]),frozenset([0,1,2,3])))
        self.assertEqual(m.degree_profile(4,edges,thresholds,0)[1][3],False)

    def test_original_fraction_threshold_equality_is_vulnerable(self):
        self.assertTrue(m.vulnerable_from_one_neighbor(2,H))
        self.assertTrue(m.vulnerable_from_one_neighbor(3,F(1,3)))
        self.assertFalse(m.vulnerable_from_one_neighbor(3,H))

    def test_isolated_node_never_spontaneously_adopts(self):
        x=m.validate_final_closure(3,(),(H,)*3,0)
        self.assertEqual(x["active"],frozenset([0]))

    def test_isolated_seed_only_no_other_activation(self):
        edges=((1,2),)
        self.assertEqual(m.validate_final_closure(3,edges,(H,)*3,0)["size"],1)

    def test_seed_is_exogenously_active_even_if_high_threshold(self):
        self.assertEqual(m.validate_final_closure(2,((0,1),),(F(1),F(1)),0)["size"],2)

    def test_neighbor_activation_at_exact_fraction_equality(self):
        edges=((0,1),(1,2))
        thresholds=(F(1),H,F(1))
        self.assertEqual(m.validate_final_closure(3,edges,thresholds,0)["size"],3)

    def test_high_degree_stable_leaf_seed_never_cascade(self):
        edges=tuple((0,i) for i in range(1,6))
        self.assertEqual(m.synchronous_cascade(6,edges,(F(1),)*6,1)["size"],1)

    def test_monotone_sync_trace_and_closed_final_membership(self):
        graph=((0,1),(1,2),(2,3))
        result=m.validate_final_closure(4,graph,(H,)*4,0)
        self.assertEqual(result["history"][0],frozenset([0]))
        self.assertEqual(result["history"][-1],frozenset(range(4)))
        self.assertTrue(all(x<y for x,y in zip(result["history"],result["history"][1:])))

    def test_asynchronous_solver_not_calling_synchronous_solver(self):
        with patch.object(m,"synchronous_cascade",side_effect=AssertionError("NO_SYNC")):
            self.assertEqual(m.independently_asynchronous_cascade(3,((0,1),(1,2)),(H,)*3,0),frozenset((0,1,2)))

    def test_synchronous_solver_not_calling_asynchronous_solver(self):
        with patch.object(m,"independently_asynchronous_cascade",side_effect=AssertionError("NO_ASYNC")):
            self.assertEqual(m.synchronous_cascade(3,((0,1),(1,2)),(H,)*3,0)["size"],3)

    def test_simple_graph_reverse_edge_duplicate_denied(self):
        with self.assertRaisesRegex(m.WattsInputError,"DUPLICATE"):
            m.validate_graph(3,((0,1),(1,0)),(H,)*3,0)

    def test_self_loop_denied(self):
        with self.assertRaisesRegex(m.WattsInputError,"SELF_LOOP"):
            m.validate_graph(2,((1,1),),(H,)*2,0)

    def test_nonexistent_node_edge_denied(self):
        with self.assertRaises(m.WattsInputError):
            m.validate_graph(2,((0,2),),(H,)*2,0)

    def test_boolean_edge_node_denied(self):
        with self.assertRaises(m.WattsInputError):
            m.validate_graph(2,((False,1),),(H,)*2,0)

    def test_edge_wrong_arity_and_container_denied(self):
        for bad in (("0",1),(0,),(0,1,1),[0,1,2]):
            with self.subTest(bad=bad),self.assertRaises(m.WattsInputError):
                m.validate_graph(3,(bad,),(H,)*3,0)

    def test_bad_graph_size_denied(self):
        for bad in (0,11,-1,True,3.0,"3"):
            with self.subTest(bad=bad),self.assertRaises(m.WattsInputError):
                m.validate_graph(bad,(),(),0)

    def test_empty_or_mismatched_thresholds_denied(self):
        with self.assertRaises(m.WattsInputError):
            m.validate_graph(2,(),(H,),0)

    def test_non_fraction_threshold_denied(self):
        for v in (0,0.5,True,False,"1/2",None):
            with self.subTest(v=v),self.assertRaises(m.WattsInputError):
                m.validate_graph(1,(),(v,),0)

    def test_invalid_threshold_range_denied(self):
        for v in (F(0),F(-1,2),F(3,2)):
            with self.subTest(v=v),self.assertRaises(m.WattsInputError):
                m.validate_graph(1,(),(v,),0)

    def test_non_integer_or_invalid_seed_denied(self):
        for v in (-1,3,True,1.0,"0",None):
            with self.subTest(v=v),self.assertRaises(m.WattsInputError):
                m.validate_graph(3,(),(H,)*3,v)

    def test_non_sequence_edges_or_thresholds_denied(self):
        with self.assertRaises(m.WattsInputError):
            m.validate_graph(1,(x for x in []),(H,),0)
        with self.assertRaises(m.WattsInputError):
            m.validate_graph(1,(),(x for x in [H]),0)

    def test_branching_original_eq5_degree_three_all_vulnerable(self):
        x=m.branching_ratio([F(0),F(0),F(0),F(1)],[F(0),F(0),F(0),F(1)])
        self.assertEqual((x["z"],x["branching_ratio"],x["regime"]),(3,2,"SUPERCRITICAL"))

    def test_branching_degree_three_none_vulnerable_subcritical(self):
        x=m.branching_ratio([F(0),F(0),F(0),F(1)],[F(0)]*4)
        self.assertEqual((x["branching_ratio"],x["regime"]),(0,"SUBCRITICAL"))

    def test_branching_degree_two_critical_not_supercritical(self):
        x=m.branching_ratio([F(0),F(0),F(1)],[F(0),F(0),F(1)])
        self.assertEqual((x["branching_ratio"],x["regime"]),(1,"CRITICAL_BOUNDARY"))

    def test_branching_degree_one_all_vulnerable_still_subcritical(self):
        x=m.branching_ratio([F(0),F(1)],[F(0),F(1)])
        self.assertEqual(x["branching_ratio"],0)

    def test_branching_half_degree_one_half_degree_three_exact_three_halves(self):
        x=m.branching_ratio([F(0),F(1,2),F(0),F(1,2)],[F(0),F(1),F(0),F(1)])
        self.assertEqual((x["z"],x["branching_ratio"]),(2,F(3,2)))

    def test_branching_zero_edges_undefined(self):
        with self.assertRaisesRegex(m.WattsInputError,"ZERO_MEAN_DEGREE"):
            m.branching_ratio([F(1)],[F(0)])

    def test_branching_degree_probs_must_exactly_normalize(self):
        with self.assertRaisesRegex(m.WattsInputError,"NOT_NORMALIZED"):
            m.branching_ratio([F(0),F(1,2)],[F(0),F(1)])

    def test_branching_degree_and_vulnerability_dimensions_must_match(self):
        with self.assertRaises(m.WattsInputError):
            m.branching_ratio([F(0),F(1)],[F(0)])

    def test_branching_probability_fraction_only_and_bounds(self):
        for bad in (0.5,1,True,F(-1,2),F(2)):
            with self.subTest(v=bad),self.assertRaises(m.WattsInputError):
                m.branching_ratio([F(0),F(1)],[F(0),bad])

    def test_vulnerability_degree_nonnegative_int(self):
        for bad in (-1,True,1.0,"3"):
            with self.subTest(v=bad),self.assertRaises(m.WattsInputError):
                m.vulnerable_from_one_neighbor(bad,H)

    def test_tiny_graph_exhaustive_counts_n_to_four(self):
        self.assertEqual(m.exhaustive_tiny_graphs(),{"1":3,"2":36,"3":648,"4":20736})

    def test_exhaustive_invalid_high_or_bool_limit_denied(self):
        for bad in (0,5,True,None,4.0):
            with self.subTest(v=bad),self.assertRaises(m.WattsInputError):
                m.exhaustive_tiny_graphs(bad)

    def test_original_model_source_and_zero_human_E2(self):
        # Do not run entire exhaustive study again here.
        self.assertEqual(m.__doc__.count("doi:10.1073/pnas.082090499"),1)
        x=m.frozen_network_counterexamples()
        self.assertTrue(x["finite_graph_not_random_ER_phase_diagram"])

    def test_same_degree_counterexample_is_reproducible(self):
        self.assertEqual(m.frozen_network_counterexamples(),m.frozen_network_counterexamples())


if __name__=="__main__":
    unittest.main()
