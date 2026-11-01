"""TH192: exact synthetic audit of cultural transmission stages and network order.

Only standard-library Fraction and unittest are used. No real human data, I/O,
network calls, or model fitting. This is a theory counterexample, not a replication.
"""
from fractions import Fraction as F
import unittest


def terminal_probability(receive, recall_given_received, transmit_given_recalled):
    """Conditional three-stage path probability under the stated stage model."""
    rates = (receive, recall_given_received, transmit_given_recalled)
    if any(not isinstance(v, F) or v < 0 or v > 1 for v in rates):
        raise ValueError("all rates must be Fraction probabilities in [0,1]")
    return receive * recall_given_received * transmit_given_recalled


def stage_worlds():
    return {
        "selection": (F(1, 2), F(1), F(1)),
        "memory": (F(1), F(1, 2), F(1)),
        "sharing": (F(1), F(1), F(1, 2)),
    }


def reach_by_rounds(rounds, initially_informed=("A",)):
    """Within each round, pair contacts occur simultaneously."""
    informed = set(initially_informed)
    history = [frozenset(informed)]
    for pairs in rounds:
        edges = [tuple(p) for p in pairs]
        endpoints = [p for edge in edges for p in edge]
        if len(set(endpoints)) != len(endpoints):
            raise ValueError("each participant may appear at most once per round")
        new = set(informed)
        for a, b in edges:
            if a in informed or b in informed:
                new.update((a, b))
        informed = new
        history.append(frozenset(informed))
    return history


R1 = (("A", "B"), ("C", "D"), ("E", "F"), ("G", "H"))
R2 = (("A", "C"), ("B", "D"), ("E", "G"), ("F", "H"))
R3_EARLY = (("A", "E"), ("B", "F"), ("C", "G"), ("D", "H"))
R3_LATE = (("A", "D"), ("B", "C"), ("E", "H"), ("F", "G"))


def validate_unique_contacts(rounds):
    edges = [frozenset(e) for r in rounds for e in r]
    return len(edges) == len(set(edges)) and all(len(e) == 2 for e in edges)


class ThreeStageTests(unittest.TestCase):
    def test_selection_world(self):
        self.assertEqual(terminal_probability(*stage_worlds()["selection"]), F(1, 2))

    def test_memory_world(self):
        self.assertEqual(terminal_probability(*stage_worlds()["memory"]), F(1, 2))

    def test_sharing_world(self):
        self.assertEqual(terminal_probability(*stage_worlds()["sharing"]), F(1, 2))

    def test_three_worlds_observationally_identical_terminal(self):
        self.assertEqual(len({terminal_probability(*x) for x in stage_worlds().values()}), 1)

    def test_stage_rates_are_distinct(self):
        self.assertEqual(len(set(stage_worlds().values())), 3)

    def test_content_advantage_can_be_cancelled(self):
        salient = terminal_probability(F(3, 4), F(2, 3), F(1))
        ordinary = terminal_probability(F(1, 2), F(1), F(1))
        self.assertEqual(salient, ordinary)

    def test_content_conditional_recall_is_different(self):
        self.assertNotEqual(F(2, 3), F(1))

    def test_zero_gate(self):
        self.assertEqual(terminal_probability(F(1), F(0), F(1)), F(0))

    def test_perfect_gate(self):
        self.assertEqual(terminal_probability(F(1), F(1), F(1)), F(1))

    def test_probabilities_bounded(self):
        self.assertLessEqual(terminal_probability(F(2, 3), F(3, 4), F(4, 5)), F(1))

    def test_reject_negative(self):
        with self.assertRaises(ValueError):
            terminal_probability(F(-1, 4), F(1), F(1))

    def test_reject_over_one(self):
        with self.assertRaises(ValueError):
            terminal_probability(F(5, 4), F(1), F(1))

    def test_reject_float(self):
        with self.assertRaises(ValueError):
            terminal_probability(0.5, F(1), F(1))


class NetworkTests(unittest.TestCase):
    def test_early_unique_contacts(self):
        self.assertTrue(validate_unique_contacts((R1, R2, R3_EARLY)))

    def test_late_unique_contacts(self):
        self.assertTrue(validate_unique_contacts((R1, R2, R3_LATE)))

    def test_same_contact_count(self):
        self.assertEqual(sum(map(len, (R1, R2, R3_EARLY))), 12)
        self.assertEqual(sum(map(len, (R1, R2, R3_LATE))), 12)

    def test_same_first_two_rounds(self):
        a = reach_by_rounds((R1, R2, R3_EARLY))
        b = reach_by_rounds((R1, R2, R3_LATE))
        self.assertEqual([len(s) for s in a[:3]], [1, 2, 4])
        self.assertEqual(a[:3], b[:3])

    def test_early_full_reach(self):
        self.assertEqual(len(reach_by_rounds((R1, R2, R3_EARLY))[-1]), 8)

    def test_late_partial_reach(self):
        self.assertEqual(len(reach_by_rounds((R1, R2, R3_LATE))[-1]), 4)

    def test_same_final_edges_not_needed(self):
        self.assertNotEqual(set(map(frozenset, R3_EARLY)), set(map(frozenset, R3_LATE)))

    def test_invalid_simultaneous_contact(self):
        with self.assertRaises(ValueError):
            reach_by_rounds((("A", "B"), ("A", "C")))


if __name__ == "__main__":
    unittest.main(verbosity=2)
