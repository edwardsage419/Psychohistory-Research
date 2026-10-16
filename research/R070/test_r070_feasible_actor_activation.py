"""R070 E1 first feasible agent versus first unhappy agent activation probes."""
import unittest
from r070_exhaustive_3x3 import all_boards, TOLERANCES, MOVE_BUDGET
from r070_distance_competitors import POLICIES, run_policy, unsatisfied, candidate_destinations
from r070_schelling_spatial_migration import INITIAL
from r070_feasible_actor_activation import (
    feasible_step,run_feasible,evaluate,score_one,summarize,
)


def counterexample():
    return ((1,1,2),(2,0,0),(0,0,0))


class FeasibleActivationTests(unittest.TestCase):
    def test_original_stall_remains_actual_stall(self):
        q=run_policy(counterexample(),.5,"GLOBAL_ROW_MAJOR")
        self.assertEqual(q["actual_moves"],0)
        self.assertEqual(q["termination"],"STALLED_NO_SATISFYING_VACANCY")

    def test_new_activation_skips_immobile_actor(self):
        nxt,evt=feasible_step(counterexample(),.5,"GLOBAL_ROW_MAJOR")
        self.assertTrue(evt["moved"])
        self.assertGreater(evt["skipped_immobile_unhappy"],0)
        self.assertNotEqual(nxt,counterexample())

    def test_new_selected_actor_is_first_feasible_in_order(self):
        board=counterexample()
        nxt,evt=feasible_step(board,.5,"GLOBAL_ROW_MAJOR")
        candidates=[u for u in unsatisfied(board,.5)
                    if candidate_destinations(board,u,.5,"GLOBAL_ROW_MAJOR")]
        self.assertEqual(tuple(evt["from"]),candidates[0])

    def test_new_destination_equals_frozen_policy_first_target(self):
        board=counterexample()
        nxt,evt=feasible_step(board,.5,"GLOBAL_ROW_MAJOR")
        option=candidate_destinations(board,tuple(evt["from"]),.5,"GLOBAL_ROW_MAJOR")[0]
        self.assertEqual(tuple(evt["to"]),option[:2])

    def test_population_conservation_on_skip(self):
        z=run_feasible(counterexample(),.5,"GLOBAL_ROW_MAJOR")
        self.assertTrue(z["source_type_counts_preserved"])
        for s in z["snapshots"]:
            m=s["metrics"]
            self.assertEqual((m["type_A_agents"],m["type_B_agents"],m["empty_cells"]),(2,2,5))

    def test_empty_source_not_actor(self):
        with self.assertRaises(ValueError):
            candidate_destinations(counterexample(),(1,1),.5,"GLOBAL_ROW_MAJOR")

    def test_tau_zero_all_policies_stable(self):
        for policy in POLICIES:
            z=run_feasible(INITIAL,0.,policy)
            self.assertEqual(z["termination"],"STABLE_ALL_SATISFIED")
            self.assertEqual(z["actual_moves"],0)

    def test_radius_one_can_be_terminal_fully_immobile(self):
        # Non-convergence must not be called "all happy".
        q=run_feasible(INITIAL,.5,"RADIUS_1")
        if q["termination"]=="STALLED_ALL_UNHAPPY_IMMOBILE":
            board=q["snapshots"][-1]["board"]
            self.assertTrue(unsatisfied(board,.5))
            self.assertTrue(all(not candidate_destinations(board,u,.5,"RADIUS_1")
                               for u in unsatisfied(board,.5)))

    def test_unknown_policy_fails(self):
        with self.assertRaises(ValueError):
            run_feasible(INITIAL,.5,"UNDECLARED")

    def test_unknown_budget_fails(self):
        for val in (-1,True,1.4,101):
            with self.assertRaises(ValueError):
                run_feasible(INITIAL,.5,"GLOBAL_ROW_MAJOR",val)

    def test_zero_budget_is_not_fake_stability(self):
        q=run_feasible(INITIAL,.5,"GLOBAL_ROW_MAJOR",0)
        self.assertEqual(q["termination"],"MAX_STEP_BUDGET")
        self.assertEqual(q["actual_moves"],0)

    def test_one_move_alters_exactly_two_cells(self):
        board=counterexample()
        nxt,event=feasible_step(board,.5,"GLOBAL_ROW_MAJOR")
        self.assertEqual(sum(board[r][c]!=nxt[r][c]
                             for r in range(3) for c in range(3)),2)

    def test_moved_agent_is_happy_in_new_location(self):
        from r070_schelling_spatial_migration import happy
        board=counterexample()
        for policy in POLICIES:
            next_board,event=feasible_step(board,.5,policy)
            if event["moved"]:
                self.assertTrue(happy(next_board,*event["to"],.5))

    def test_no_eligible_move_is_separate_from_all_satisfied(self):
        b=((1,2),(2,1))
        for p in POLICIES:
            z=run_feasible(b,.5,p,8)
            self.assertEqual(z["termination"],"STALLED_ALL_UNHAPPY_IMMOBILE")
            self.assertGreater(z["snapshots"][-1]["metrics"]["unhappy_agents"],0)

    def test_new_cannot_fake_vacant_isolated_destination(self):
        from r070_schelling_spatial_migration import fraction
        for policy in POLICIES:
            nxt,evt=feasible_step(counterexample(),.5,policy)
            if evt["moved"]:
                source=tuple(evt["from"])
                without=[list(row) for row in counterexample()]
                without[source[0]][source[1]]=0
                self.assertIsNotNone(fraction(without,*evt["to"],evt["abstract_type"]))

    def test_first_feasible_can_consider_second_person_only(self):
        board=counterexample()
        self.assertEqual(
            candidate_destinations(board,unsatisfied(board,.5)[0],.5,"GLOBAL_ROW_MAJOR"),[])
        self.assertTrue(any(candidate_destinations(board,u,.5,"GLOBAL_ROW_MAJOR")
                            for u in unsatisfied(board,.5)[1:]))

    def test_strict_3x3_entire_layout_count(self):
        boards=list(all_boards())
        self.assertEqual(len(boards),756)
        self.assertEqual(len(set(boards)),756)

    def test_no_drop_of_immobile_candidates_in_case_universe(self):
        for policy in POLICIES:
            old=run_policy(counterexample(),.5,policy)
            new=run_feasible(counterexample(),.5,policy)
            self.assertTrue(old["snapshots"])
            self.assertTrue(new["snapshots"])

    def test_four_mobility_policies_and_five_tau_values(self):
        self.assertEqual(len(POLICIES),4)
        self.assertEqual(TOLERANCES,(0.,.25,.5,.75,1.))

    def test_40_step_cap_requires_explicit_budget(self):
        q=run_feasible(counterexample(),.5,"GLOBAL_ROW_MAJOR",MOVE_BUDGET)
        self.assertLessEqual(q["actual_moves"],MOVE_BUDGET)

    def test_disallow_fake_independent_human_evidence(self):
        q=run_feasible(counterexample(),.5,"GLOBAL_ROW_MAJOR",3)
        self.assertNotIn("census",str(q).lower())
        self.assertNotIn("participant",str(q).lower())

    def test_complete_paired_30240_outcomes(self):
        result=evaluate()
        self.assertEqual(result["status"],"E1_AGENT_ACTIVATION_COMPETITION_PASS")
        self.assertEqual(result["executed_trajectories"],30240)
        self.assertEqual(result["human_event_level_E2"],
                         "BLOCKED_EVENT_LEVEL_SOURCE_AND_RULE_PARITY")
        for t in result["experimental_results"].values():
            for p in POLICIES:
                case=t[p]
                old=case["original_first_unhappy"]
                new=case["new_first_feasible_unhappy"]
                self.assertEqual(old["satisfied"]+old["first_actor_stalled"]+
                                 old["budget_exhausted"],756)
                self.assertEqual(new["satisfied"]+new["all_unhappy_agents_immobile"]+
                                 new["budget_exhausted"],756)

    def test_macro_null_stays_undefined_in_model(self):
        from r070_schelling_spatial_migration import metrics
        b=((1,0,0),(0,0,0),(0,0,2))
        self.assertIsNone(metrics(b,.5)["cardinal_different_type_edge_share"])


if __name__=="__main__":
    unittest.main()
