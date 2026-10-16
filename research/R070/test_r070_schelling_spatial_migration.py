"""R070 deterministic synthetic-only Schelling micro-to-macro rule tests."""
import math
import unittest
import r070_schelling_spatial_migration as m


class SpatialMicroMacroTests(unittest.TestCase):
    def test_initial_board_type_universe(self):
        x=m.metrics(m.INITIAL,.5)
        self.assertEqual((x["type_A_agents"],x["type_B_agents"],x["empty_cells"]),(2,2,12))

    def test_first_moore_neighbor_same_ratio(self):
        self.assertAlmostEqual(m.fraction(m.INITIAL,0,0,1),1/3)

    def test_first_agent_unsatisfied_half(self):
        self.assertFalse(m.happy(m.INITIAL,0,0,.5))

    def test_first_fixed_rowmajor_satisficing_relocation(self):
        q,event=m.step(m.INITIAL,.5)
        self.assertEqual(event["from"],[0,0])
        self.assertEqual(event["to"],[2,0])
        self.assertEqual(q[2][0],1)
        self.assertEqual(q[0][0],0)
        self.assertGreaterEqual(event["destination_same_neighbor_fraction"],.5)

    def test_tau_zero_neutral_has_no_move(self):
        result=m.run(m.INITIAL,0.,8)
        self.assertEqual(result["actual_moves"],0)
        self.assertEqual(result["termination"],"STABLE_ALL_SATISFIED")
        self.assertEqual(result["snapshots"][0]["board"],result["snapshots"][-1]["board"])

    def test_agent_identity_counts_never_change(self):
        out=m.run(m.INITIAL,.5,8)
        self.assertTrue(out["source_type_counts_preserved"])
        for step in out["snapshots"]:
            self.assertEqual(step["metrics"]["type_A_agents"],2)
            self.assertEqual(step["metrics"]["type_B_agents"],2)
            self.assertEqual(step["metrics"]["empty_cells"],12)

    def test_step_moves_at_most_one_agent(self):
        a,b=m.step(m.INITIAL,.5)
        self.assertEqual(sum(m.INITIAL[r][c]!=a[r][c] for r in range(4) for c in range(4)),2)

    def test_fully_satisfied_board_stable(self):
        board=((1,1),(1,1))
        z,e=m.step(board,1.)
        self.assertEqual(z,board)
        self.assertEqual(e["status"],"STABLE_ALL_SATISFIED")

    def test_no_vacancy_fails_as_stalled_not_satisfied(self):
        z,e=m.step(((1,2),(2,1)),.5)
        self.assertEqual(e["status"],"STALLED_NO_SATISFYING_VACANCY")
        self.assertEqual(z,((1,2),(2,1)))

    def test_isolated_existing_agent_has_no_neighborhood(self):
        board=((1,0,0),(0,0,0),(0,0,0))
        self.assertIsNone(m.fraction(board,0,0,1))
        self.assertTrue(m.happy(board,0,0,1))

    def test_empty_destination_must_not_be_isolated(self):
        # The row-major earlier isolated vacancy at (0,3) cannot be selected
        _,ev=m.step(m.INITIAL,.5)
        self.assertNotEqual(ev["to"],[0,3])

    def test_neighborhood_edge_is_not_periodic(self):
        neighbors=set(m.neighbors(m.INITIAL,0,0))
        self.assertEqual(neighbors,{(0,1),(1,0),(1,1)})

    def test_cardinal_contacts_are_not_moore_contacts(self):
        q=m.metrics(m.INITIAL,.5)
        self.assertEqual(q["cardinal_occupied_same_type_edges"],2)
        self.assertEqual(q["cardinal_occupied_different_type_edges"],2)
        self.assertAlmostEqual(q["cardinal_different_type_edge_share"],.5)

    def test_one_agent_no_cardinal_contact_is_undefined_not_div0(self):
        board=((1,0,0),(0,0,0),(0,0,0))
        self.assertIsNone(m.metrics(board,.5)["cardinal_different_type_edge_share"])

    def test_nonrectangular_board_rejected(self):
        with self.assertRaises(ValueError):m.validate(((1,2),(1,)),.5)

    def test_illegal_type_rejected(self):
        with self.assertRaises(ValueError):m.validate(((1,3),(0,2)),.5)

    def test_bool_not_an_abstract_agent(self):
        with self.assertRaises(ValueError):m.validate(((True,0),(0,2)),.5)

    def test_nonfinite_tau_rejected(self):
        for t in (math.nan,math.inf,-.01,1.01):
            with self.assertRaises(ValueError):m.validate(m.INITIAL,t)

    def test_invalid_step_budget_rejected(self):
        for v in (-1,2.1,True,200):
            with self.assertRaises(ValueError):m.run(m.INITIAL,.5,v)

    def test_benchmark_two_comparators_and_no_real_claims(self):
        q=m.benchmark()
        self.assertEqual(q["status"],"E1_SYNTHETIC_SPATIAL_RULE_PASS")
        self.assertEqual(q["real_residential_mobility_e2"],"OPEN")
        self.assertEqual(q["real_discrimination_or_historical_social_causality"],"NOT_IDENTIFIED")

    def test_no_original_human_population_in_output(self):
        q=m.benchmark()
        text=str(q)
        self.assertNotIn("census",text.lower())
        self.assertTrue(q["synthetic_only"])

    def test_exact_tick_cannot_exceed_budget(self):
        out=m.run(m.INITIAL,.5,8)
        self.assertLessEqual(out["actual_moves"],8)
        self.assertEqual(len(out["snapshots"]),out["actual_moves"]+1)


if __name__=="__main__":
    unittest.main()
