"""R069 synthetic graph transmission exactness, boundaries and science labeling."""
import math,unittest
from r069_network_cascade_baselines import (
    N,PATH,SEED,benchmark,validate_graph,threshold_trace,
    independent_cascade_exact,bass_euler
)

class NetworkCascadeTests(unittest.TestCase):
    def test_watts_half_path_propagates_one_node_per_round(self):
        got=threshold_trace(6,PATH,{0},.5,5)
        self.assertEqual(got,[tuple(range(i+1)) for i in range(6)])

    def test_watts_high_threshold_traps_seed(self):
        self.assertEqual(threshold_trace(6,PATH,{0},.75,3),[(0,)]*4)

    def test_watts_single_round_uses_previous_state_synchronously(self):
        self.assertEqual(threshold_trace(6,PATH,{0},.5,1)[1],(0,1))

    def test_watts_irreversibility(self):
        hist=threshold_trace(6,PATH,{0},.5,5)
        self.assertTrue(all(set(a).issubset(b) for a,b in zip(hist[:-1],hist[1:])))

    def test_isolated_unseeded_never_self_activates(self):
        hist=threshold_trace(3,[(0,1)],{0},0.,3)
        self.assertEqual(hist[-1],(0,1))

    def test_independent_cascade_path_exact_node_probabilities(self):
        y=independent_cascade_exact(6,PATH,{0},.5)
        self.assertEqual(y["live_edge_subsets_enumerated"],32)
        self.assertEqual(y["node_adoption_probabilities"],[1,.5,.25,.125,.0625,.03125])
        self.assertAlmostEqual(y["expected_final_adopters"],1.96875)

    def test_zero_transmission_preserves_seed(self):
        y=independent_cascade_exact(6,PATH,{0},0)
        self.assertEqual(y["expected_final_adopters"],1)

    def test_full_transmission_reaches_all_path(self):
        y=independent_cascade_exact(6,PATH,{0},1)
        self.assertEqual(y["expected_final_adopters"],6)

    def test_orientation_matters_for_independent_cascade(self):
        y=independent_cascade_exact(2,[(1,0)],{0},1)
        self.assertEqual(y["node_adoption_probabilities"],[1,0])

    def test_invalid_repeated_undirected_edge_rejected(self):
        with self.assertRaises(ValueError):
            validate_graph(2,[(0,1),(1,0)],directed=False)

    def test_self_loop_rejected(self):
        with self.assertRaises(ValueError):
            validate_graph(2,[(0,0)])

    def test_outside_graph_node_rejected(self):
        with self.assertRaises(ValueError):
            validate_graph(2,[(0,2)])

    def test_empty_seed_rejected(self):
        with self.assertRaises(ValueError):
            threshold_trace(3,[(0,1)],[],.5,1)

    def test_negative_threshold_rejected(self):
        with self.assertRaises(ValueError):
            threshold_trace(3,[(0,1)],{0},-.1,1)

    def test_IC_invalid_probability_rejected(self):
        with self.assertRaises(ValueError):
            independent_cascade_exact(3,[(0,1)],{0},float("nan"))

    def test_IC_exact_edge_enumeration_cap(self):
        graph=[(i,i+1) for i in range(13)]
        with self.assertRaises(ValueError):
            independent_cascade_exact(14,graph,{0},.5)

    def test_bass_first_step_value(self):
        self.assertAlmostEqual(bass_euler(1/6,.03,.4,1,1)[1],.24722222222222223)

    def test_bass_synthetic_monotonic(self):
        seq=bass_euler(1/6,.03,.4,1,5)
        self.assertEqual(len(seq),6)
        self.assertTrue(all(b>=a for a,b in zip(seq[:-1],seq[1:])))

    def test_bass_invalid_euler_jump_fail_not_clip(self):
        with self.assertRaises(ValueError):
            bass_euler(.5,1,1,1,1)

    def test_bass_invalid_time_interval_fail(self):
        with self.assertRaises(ValueError):
            bass_euler(.5,.03,.4,-.1,1)

    def test_bass_zero_innovation_zero_seed_fixed(self):
        seq=bass_euler(0,0,.4,1,10)
        self.assertTrue(all(x==0 for x in seq))

    def test_benchmark_e1_not_human(self):
        v=benchmark()
        self.assertEqual(v["status"],"E1_MECHANISM_PASS")
        self.assertEqual(v["e2_empirical_adoption_network"],"OPEN")
        self.assertEqual(v["historical_technology_adoption_calibration"],"NOT_PERFORMED")
        self.assertFalse(v["independent_cascade"]["simulation_or_monte_carlo_used"])

if __name__=="__main__":
    unittest.main()
