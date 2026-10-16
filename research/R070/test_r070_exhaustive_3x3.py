"""Independent mathematical guards for complete 3x3 two abstract-type grid."""
import itertools
import unittest
from collections import Counter
import r070_exhaustive_3x3 as e
from r070_schelling_spatial_migration import run,metrics,step

class ExhaustiveGridTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.boards=list(e.all_boards())

    def test_complete_nine_choose_two_seven_choose_two(self):
        self.assertEqual(len(self.boards),36*21)
        self.assertEqual(len(self.boards),756)

    def test_all_state_encodings_unique(self):
        self.assertEqual(len({e.board_digest(x) for x in self.boards}),756)

    def test_each_state_population_count_preserved(self):
        for board in self.boards:
            cell=Counter(x for row in board for x in row)
            self.assertEqual((cell[0],cell[1],cell[2]),(5,2,2))

    def test_all_boards_3x3(self):
        self.assertTrue(all(len(x)==3 and all(len(row)==3 for row in x) for x in self.boards))

    def test_enumerated_state_count_independent_of_parameter(self):
        for tau in e.TOLERANCES:
            self.assertEqual(len(self.boards),e.N_BOARDS)
        self.assertEqual(len(e.TOLERANCES)*e.N_BOARDS,3780)

    def test_tau_zero_no_moves_for_every_configuration(self):
        for board in self.boards:
            y,evt=step(board,0.)
            self.assertFalse(evt["moved"])
            self.assertEqual(evt["status"],"STABLE_ALL_SATISFIED")
            self.assertEqual(y,board)

    def test_max_move_budget_constant(self):
        self.assertEqual(e.MOVE_BUDGET,40)

    def test_absorbing_all_satisfied_test(self):
        b=((1,1,0),(0,0,0),(0,2,2))
        outcome=run(b,.5,5)
        self.assertEqual(outcome["termination"],"STABLE_ALL_SATISFIED")
        self.assertEqual(outcome["actual_moves"],0)

    def test_summary_rejects_unfrozen_tolerance(self):
        with self.assertRaises(ValueError):
            e.summarize_tolerance(.3333,self.boards)

    def test_summary_rejects_duplicate_board_identity(self):
        boards=[self.boards[0]]*756
        with self.assertRaisesRegex(ValueError,"duplicate"):
            e.summarize_tolerance(.5,boards)

    def test_summary_rejects_partial_universe(self):
        with self.assertRaisesRegex(ValueError,"incomplete"):
            e.summarize_tolerance(0.,self.boards[:-1])

    def test_tau_zero_exhaustive_counts(self):
        q=e.summarize_tolerance(0.,self.boards)
        self.assertEqual(q["terminal_status_counts"]["STABLE_ALL_SATISFIED"],756)
        self.assertEqual(q["total_moves"],0)
        self.assertEqual(q["distinct_initial_boards"],756)

    def test_null_macro_contact_does_not_become_zero(self):
        b=((1,0,0),(0,2,0),(0,0,0))
        self.assertIsNone(metrics(b,.5)["cardinal_different_type_edge_share"])

    def test_concrete_relocation_uses_existing_r070_rule(self):
        board=self.boards[100]
        z=run(board,.5,12)
        self.assertTrue(z["source_type_counts_preserved"])
        self.assertLessEqual(z["actual_moves"],12)

    def test_all_syn_outcomes_have_three_status_keys(self):
        q=e.summarize_tolerance(1.,self.boards)
        self.assertEqual(set(q["terminal_status_counts"]),set(e.TERMINATIONS))
        self.assertEqual(sum(q["terminal_status_counts"].values()),756)

    def test_three_quarter_and_full_satisfaction_identical_on_all_756(self):
        # With only two of each abstract type, an agent can have at most
        # one similar neighbor; any occupied-neighbor fraction is
        # 0, 1/3, 1/2 or 1 (or undefined for isolation). Thus tau=.75 and
        # tau=1 demand exactly the same local condition on this board.
        for board in self.boards:
            a=e.run(board,.75,e.MOVE_BUDGET)
            b=e.run(board,1.,e.MOVE_BUDGET)
            self.assertEqual(a["termination"],b["termination"])
            self.assertEqual(a["actual_moves"],b["actual_moves"])
            self.assertEqual(a["snapshots"][-1]["board"],b["snapshots"][-1]["board"])

    def test_e1_summary_keeps_zero_real_human_claims(self):
        self.assertIn("E1",e.evaluate()["status"])
        self.assertEqual(e.evaluate()["empirical_human_e2"],
                         "OPEN_NO_EVENT_LEVEL_PUBLIC_LAB_DATA_VERIFIED")


if __name__=="__main__":
    unittest.main()
