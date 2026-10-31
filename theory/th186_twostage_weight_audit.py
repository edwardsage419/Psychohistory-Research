"""TH186: synthetic exact design audit. No human data, no external dependencies."""
from fractions import Fraction as F
from itertools import product
import unittest

# Two artificial clusters, with two and four individuals respectively.
SIZES = (2, 4)
POTENTIAL = ((F(8), F(4), F(2)), (F(2), F(1), F(0)))  # direct, spill, pure
N = sum(SIZES)


def assignments():
    """Stage one selects one cluster, stage two selects one member of it."""
    return [(i, j) for i, size in enumerate(SIZES) for j in range(size)]


def exposure(i, j, chosen_cluster, chosen_person):
    if i != chosen_cluster:
        return "pure"
    return "direct" if j == chosen_person else "spill"


def exposure_prob(i, kind):
    n = SIZES[i]
    return {"direct": F(1, 2 * n), "spill": F(n - 1, 2 * n), "pure": F(1, 2)}[kind]


def ht_mean(a, kind, individual=True):
    total = F(0)
    for i, n in enumerate(SIZES):
        weight = F(1, N) if individual else F(1, len(SIZES) * n)
        for j in range(n):
            if exposure(i, j, *a) == kind:
                value = POTENTIAL[i][{"direct": 0, "spill": 1, "pure": 2}[kind]]
                total += weight * value / exposure_prob(i, kind)
    return total


def estimand(kind, individual=True):
    k = {"direct": 0, "spill": 1, "pure": 2}[kind]
    return sum((SIZES[i] if individual else 1) * POTENTIAL[i][k]
               for i in range(2)) / (N if individual else 2)


def expectation(f):
    a = assignments()
    return sum((F(1, 2 * SIZES[x[0]]) * f(x) for x in a), F(0))


def naive_direct_minus_pure(a):
    # One directly treated individual; the other cluster is a pure control.
    i, _ = a
    control = 1 - i
    return POTENTIAL[i][0] - POTENTIAL[control][2]


class TestSyntheticTwoStage(unittest.TestCase):
    def test_assignment_count(self): self.assertEqual(len(assignments()), 6)
    def test_unique_assignments(self): self.assertEqual(len(set(assignments())), 6)
    def test_direct_small(self): self.assertEqual(exposure_prob(0, "direct"), F(1, 4))
    def test_direct_large(self): self.assertEqual(exposure_prob(1, "direct"), F(1, 8))
    def test_spill_small(self): self.assertEqual(exposure_prob(0, "spill"), F(1, 4))
    def test_spill_large(self): self.assertEqual(exposure_prob(1, "spill"), F(3, 8))
    def test_pure(self): self.assertEqual(exposure_prob(0, "pure"), F(1, 2))
    def test_probability_partition(self):
        for i in range(2):
            self.assertEqual(sum((exposure_prob(i, k) for k in ("direct", "spill", "pure")), F(0)), 1)
    def test_individual_direct(self): self.assertEqual(estimand("direct") - estimand("pure"), F(10, 3))
    def test_household_direct(self): self.assertEqual(estimand("direct", False) - estimand("pure", False), 4)
    def test_individual_spill(self): self.assertEqual(estimand("spill") - estimand("pure"), F(4, 3))
    def test_household_spill(self): self.assertEqual(estimand("spill", False) - estimand("pure", False), F(3, 2))
    def test_ht_unbiased_six(self):
        for individual, kind in product((True, False), ("direct", "spill", "pure")):
            self.assertEqual(expectation(lambda a: ht_mean(a, kind, individual)), estimand(kind, individual))
    def test_ht_effect_unbiased(self):
        for individual in (True, False):
            self.assertEqual(expectation(lambda a: ht_mean(a, "direct", individual) - ht_mean(a, "pure", individual)),
                             estimand("direct", individual) - estimand("pure", individual))
    def test_naive_difference_bias(self):
        self.assertEqual(expectation(naive_direct_minus_pure), 4)
        self.assertEqual(expectation(naive_direct_minus_pure) - (estimand("direct") - estimand("pure")), F(2, 3))
    def test_unsupported_policy(self):
        self.assertTrue(all(sum(1 for i in range(2) if i == a[0]) == 1 for a in assignments()))
        self.assertNotIn(("both_clusters_treated",), assignments())
    def test_policy_nonidentification(self):
        # The observed design is identical in both worlds; all-treated is never assigned.
        worlds = {"A": F(10), "B": F(-5)}
        self.assertNotEqual(worlds["A"], worlds["B"])
        self.assertEqual(expectation(lambda a: ht_mean(a, "direct")), F(4))
    def test_ht_variability(self):
        vals = {ht_mean(a, "direct") - ht_mean(a, "pure") for a in assignments()}
        self.assertGreater(len(vals), 1)


if __name__ == "__main__":
    unittest.main(verbosity=2)
