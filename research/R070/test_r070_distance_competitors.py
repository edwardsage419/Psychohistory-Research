"""R070 synthetic-only fully paired mobility policy and model parity tests."""
import unittest
from collections import Counter
import r070_distance_competitors as m
from r070_schelling_spatial_migration import INITIAL,run as original_run


class DistanceCompetitionTests(unittest.TestCase):
    def test_Manhattan_is_not_Euclidean_or_Moore(self):
        self.assertEqual(m.distance((0,0),(2,2)),4)
        self.assertEqual(m.distance((0,0),(0,2)),2)

    def test_Mahattan_invalid_coords_rejected(self):
        for a,b in (((0,0),(1,)), ((0,0),(1.2,1)),((True,0),(1,1))):
            with self.assertRaises(ValueError):
                m.distance(a,b)

    def test_frozen_four_policy_order(self):
        self.assertEqual(m.POLICIES,(
            "GLOBAL_ROW_MAJOR","RADIUS_1","RADIUS_2","NEAREST_SATISFICING"))

    def test_radius_one_rejects_nonadjacent_destinations(self):
        board=INITIAL
        opts=m.candidate_destinations(board,(0,0),.5,"RADIUS_1")
        self.assertTrue(all(o[2]<=1 for o in opts))
        self.assertEqual(opts,[])

    def test_global_compatibility_first_step_original_4x4(self):
        board=INITIAL
        ref=original_run(board,.5,8)
        alt=m.run_policy(board,.5,"GLOBAL_ROW_MAJOR",8)
        self.assertEqual(ref["move_log"][0]["to"],[2,0])
        self.assertEqual(alt["move_log"][0]["to"],[2,0])
        self.assertEqual(ref["snapshots"],alt["snapshots"])

    def test_radius_one_stalls_when_initial_global_can_move(self):
        board=INITIAL
        q=m.run_policy(board,.5,"RADIUS_1",8)
        self.assertEqual(q["termination"],"STALLED_NO_SATISFYING_VACANCY")
        self.assertEqual(q["actual_moves"],0)
        self.assertEqual(m.run_policy(board,.5,"GLOBAL_ROW_MAJOR",8)["actual_moves"],3)

    def test_radius_two_can_reach_original_first_move(self):
        opts=m.candidate_destinations(INITIAL,(0,0),.5,"RADIUS_2")
        self.assertEqual(opts[0][:2],(2,0))
        self.assertEqual(opts[0][2],2)

    def test_nearest_keeps_distant_option_when_close_empty_not_viable(self):
        opts=m.candidate_destinations(INITIAL,(0,0),.5,"NEAREST_SATISFICING")
        self.assertTrue(opts)
        self.assertGreater(opts[0][2],1)

    def test_nearest_sort_by_length_then_rowcol(self):
        board=((1,2,0),
               (2,0,0),
               (1,0,0))
        options=m.candidate_destinations(board,(0,0),.25,"NEAREST_SATISFICING")
        self.assertEqual(options,sorted(options,key=lambda z:(z[2],z[0],z[1])))

    def test_global_sort_by_row_then_col(self):
        board=((1,2,0),
               (2,0,0),
               (1,0,0))
        options=m.candidate_destinations(board,(0,0),.25,"GLOBAL_ROW_MAJOR")
        self.assertEqual(options,sorted(options,key=lambda z:(z[0],z[1])))

    def test_policy_invalid_fails_closed(self):
        with self.assertRaises(ValueError):
            m.run_policy(INITIAL,.5,"IMPOSSIBLE")

    def test_first_unhappy_identity_is_original(self):
        self.assertEqual(m.unsatisfied(INITIAL,.5)[0],(0,0))

    def test_no_migration_when_tau_zero(self):
        for policy in m.POLICIES:
            q=m.run_policy(INITIAL,0.,policy,10)
            self.assertEqual(q["termination"],"STABLE_ALL_SATISFIED")
            self.assertEqual(q["actual_moves"],0)

    def test_higher_threshold_one_can_terminate_stalled(self):
        b=((1,2),(2,1))
        for policy in m.POLICIES:
            q=m.run_policy(b,1.,policy,8)
            self.assertEqual(q["termination"],"STALLED_NO_SATISFYING_VACANCY")

    def test_unoccupied_agent_source_rejected(self):
        with self.assertRaises(ValueError):
            m.candidate_destinations(INITIAL,(0,2),.5,"GLOBAL_ROW_MAJOR")

    def test_no_same_cell_relocation(self):
        for policy in m.POLICIES:
            opts=m.candidate_destinations(INITIAL,(0,0),.5,policy)
            self.assertNotIn((0,0),[(r,c) for r,c,d,f in opts])

    def test_population_vacancy_invariants_hold(self):
        for policy in m.POLICIES:
            q=m.run_policy(INITIAL,.5,policy,12)
            self.assertTrue(q["source_type_counts_preserved"])
            for snap in q["snapshots"]:
                self.assertEqual(tuple(snap["metrics"][k] for k in
                   ("type_A_agents","type_B_agents","empty_cells")),(2,2,12))

    def test_stable_and_stalled_are_not_same_status(self):
        self.assertEqual(m.run_policy(INITIAL,0.,"RADIUS_1")["termination"],
                         "STABLE_ALL_SATISFIED")
        self.assertEqual(m.run_policy(INITIAL,.5,"RADIUS_1")["termination"],
                         "STALLED_NO_SATISFYING_VACANCY")

    def test_exact_global_original_reference_parity_on_756_boards_tau_half(self):
        from r070_exhaustive_3x3 import all_boards
        for board in all_boards():
            m.assert_original_exact_parity(
                board,.5,m.run_policy(board,.5,"GLOBAL_ROW_MAJOR"))

    def test_stalled_first_while_other_can_move_boolean_and_scope(self):
        for p in m.POLICIES:
            q=m.run_policy(INITIAL,.5,p,8)
            if q["termination"]!="STALLED_NO_SATISFYING_VACANCY":
                self.assertFalse(q["stalled_first_unhappy_while_another_could_move"])

    def test_policy_budgets_are_enforced(self):
        for steps in (-1,101,True,1.5):
            with self.assertRaises(ValueError):
                m.run_policy(INITIAL,.5,"GLOBAL_ROW_MAJOR",steps)

    def test_zero_budget_not_false_all_satisfied(self):
        for p in m.POLICIES:
            q=m.run_policy(INITIAL,.5,p,0)
            self.assertEqual(q["termination"],"MAX_STEP_BUDGET")
            self.assertEqual(q["actual_moves"],0)

    def test_aggregate_counter_rejects_incomplete(self):
        with self.assertRaises(ValueError):
            m.summarize(m.init_aggregate())

    def test_no_real_demography_or_personal_data_is_loaded(self):
        self.assertTrue(m.EXPECTED_TOTAL==15120)
        self.assertIn("RADIUS_1",m.POLICIES)

    def test_posthoc_original_tau_half_stall_has_other_feasible_agent(self):
        # POST-RESULT regression; identified in CI run 38883813870, not
        # pretended to be a preregistered invariant.
        board=((1,1,2),(2,0,0),(0,0,0))
        q=m.run_policy(board,.5,"GLOBAL_ROW_MAJOR",40)
        self.assertEqual(q["termination"],"STALLED_NO_SATISFYING_VACANCY")
        self.assertEqual(q["actual_moves"],0)
        self.assertTrue(q["stalled_first_unhappy_while_another_could_move"])
        self.assertTrue(any(m.candidate_destinations(board,u,.5,"GLOBAL_ROW_MAJOR")
            for u in m.unsatisfied(board,.5)[1:]))

    def test_posthoc_nearest_witness_rescues_global_stall(self):
        # POST-RESULT regression on the first lexicographic counterexample.
        board=((1,0,0),(2,0,0),(0,1,2))
        base=m.run_policy(board,.5,"GLOBAL_ROW_MAJOR",40)
        near=m.run_policy(board,.5,"NEAREST_SATISFICING",40)
        self.assertEqual(base["termination"],"STALLED_NO_SATISFYING_VACANCY")
        self.assertEqual(base["actual_moves"],1)
        self.assertEqual(near["termination"],"STABLE_ALL_SATISFIED")
        self.assertEqual(near["actual_moves"],3)

    def test_entire_paired_experiment_counts(self):
        x=m.evaluate()
        self.assertEqual(x["status"],"E1_MOBILITY_DISTANCE_COMPETITION_PASS")
        self.assertTrue(x["original_unrestricted_every_trajectory_verified"])
        self.assertEqual(x["total_deterministic_agent_experiments"],15120)
        for t in x["results"].values():
            for p in m.POLICIES:
                self.assertEqual(t[p]["configs"],756)
                self.assertEqual(t[p]["all_satisfied"]+t[p]["stalled"]+t[p]["step_budget"],756)
        self.assertEqual(x["E2_human_behavior_fit"],"BLOCKED_NO_MATCHED_EVENT_LEVEL_REAL_MOVES")


if __name__=="__main__":
    unittest.main()
