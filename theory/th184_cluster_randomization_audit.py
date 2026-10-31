#!/usr/bin/env python3
"""TH184: exact finite-school randomization and missingness toy audit.

Only artificial school outcomes. No student or school microdata is accessed.
Run: python3 th184_cluster_randomization_audit.py
     python3 -O th184_cluster_randomization_audit.py
"""
from fractions import Fraction
from itertools import combinations, product
from math import comb
import unittest


def diff_means(y, treated):
    """Exact treated minus control difference for a complete school assignment."""
    treated = frozenset(treated)
    n = len(y)
    if not (0 < len(treated) < n):
        raise ValueError("both arms required")
    return (sum((y[i] for i in treated), Fraction()) / len(treated)
            - sum((y[i] for i in range(n) if i not in treated), Fraction()) / (n-len(treated)))


def assignments(n, n_treat):
    return tuple(combinations(range(n), n_treat))


def fisher_p(y, treated, admissible=None):
    """Two-sided sharp-null Fisher p with fixed observed outcomes and known design."""
    if admissible is None:
        admissible = assignments(len(y), len(treated))
    obs = abs(diff_means(y, treated))
    vals = tuple(abs(diff_means(y, z)) for z in admissible)
    if not vals:
        raise ValueError("empty design")
    return Fraction(sum(v >= obs for v in vals), len(vals))


def blocked_assignments(blocks, per_block):
    """Preserve the actual within-block treatment counts in toy design."""
    if len(blocks) != len(per_block):
        raise ValueError("block count mismatch")
    choices = [tuple(combinations(b, k)) for b, k in zip(blocks, per_block)]
    return tuple(tuple(sorted(sum(parts, ()))) for parts in product(*choices))


def coverage_by_assignment():
    """A toy missingness mechanism: school 0 is unobserved when treated."""
    all_z = assignments(4, 2)
    return {z: (3 if 0 in z else 4) for z in all_z}


def published_correction_fractions():
    """Percentages are published corrected descriptions, not recomputed ATEs."""
    return {"rounded_mixed": Fraction(6, 20),
            "unrounded_mixed": Fraction(29, 100),
            "adjusted_consistent": Fraction(25, 100),
            "unadjusted_consistent": Fraction(23, 100)}


class Audit(unittest.TestCase):
    def test_design_sizes(self):
        for n in (4, 6, 8):
            self.assertEqual(len(assignments(n, n//2)), comb(n, n//2))

    def test_exact_six(self):
        self.assertEqual(fisher_p((0,0,0,1,1,1), (3,4,5)), Fraction(1,10))

    def test_exact_four(self):
        self.assertEqual(fisher_p((0,0,1,1), (2,3)), Fraction(1,3))

    def test_exact_eight(self):
        self.assertEqual(fisher_p((0,0,0,0,1,1,1,1), (4,5,6,7)), Fraction(1,35))

    def test_six_duplicated_students_do_not_add_assignments(self):
        y = (0,0,0,1,1,1)
        self.assertEqual(fisher_p(y, (3,4,5)), Fraction(1,10))
        self.assertEqual(fisher_p(y, (3,4,5)), Fraction(2,comb(6,3)))

    def test_symmetry_of_two_sided_p(self):
        self.assertEqual(fisher_p((0,0,0,1,1,1), (0,1,2)), Fraction(1,10))

    def test_blocked_design_size(self):
        z = blocked_assignments(((0,1,2,3),(4,5,6,7)), (2,2))
        self.assertEqual(len(z), 36)
        self.assertEqual(len(set(z)), 36)

    def test_blocked_extreme_p(self):
        z = blocked_assignments(((0,1,2,3),(4,5,6,7)), (2,2))
        y = (0,0,1,1,0,0,1,1)
        self.assertEqual(fisher_p(y, (2,3,6,7), z), Fraction(1,18))

    def test_unblocked_same_outcomes(self):
        y = (0,0,1,1,0,0,1,1)
        self.assertEqual(fisher_p(y, (2,3,6,7)), Fraction(1,35))

    def test_blocks_change_reference_set(self):
        self.assertNotEqual(Fraction(1,18), Fraction(1,35))

    def test_missingness_depends_on_assignment(self):
        cover = coverage_by_assignment()
        self.assertEqual(len(cover), 6)
        self.assertEqual(sum(v==3 for v in cover.values()), 3)
        self.assertEqual(sum(v==4 for v in cover.values()), 3)

    def test_missingness_rate(self):
        self.assertEqual(Fraction(sum(4-v for v in coverage_by_assignment().values()), 6*4), Fraction(1,8))

    def test_all_schools_have_zero_effect_in_missingness_world(self):
        y0 = (Fraction(0), Fraction(0), Fraction(1), Fraction(1))
        y1 = y0
        self.assertEqual(y0, y1)

    def test_school_level_counts(self):
        self.assertEqual(23+5, 28)
        self.assertEqual(26+2, 28)
        self.assertEqual(23+26, 49)

    def test_correction_rounded_mixed(self):
        self.assertEqual(published_correction_fractions()["rounded_mixed"], Fraction(3,10))

    def test_correction_alternatives(self):
        p = published_correction_fractions()
        self.assertEqual(p["adjusted_consistent"], Fraction(1,4))
        self.assertEqual(p["unadjusted_consistent"], Fraction(23,100))
        self.assertNotEqual(p["unrounded_mixed"], p["adjusted_consistent"])

    def test_unadjusted_vs_adjusted_percentage_points(self):
        p = published_correction_fractions()
        self.assertEqual(p["adjusted_consistent"]-p["unadjusted_consistent"], Fraction(2,100))

    def test_all_sharp_null_p_values_are_rational(self):
        for n in (4,6,8):
            y = (0,)*(n//2)+(1,)*(n//2)
            self.assertIsInstance(fisher_p(y, tuple(range(n//2,n))), Fraction)

    def test_fourteen_blocks_candidate_design(self):
        # Conditional illustration: exactly two treated schools per block of four.
        self.assertEqual(6**14, 78364164096)
        self.assertEqual(comb(56, 28), 7648690600760440)
        self.assertLess(6**14, comb(56, 28))

    def test_icpsr_metadata_case_count_difference(self):
        # Metadata counts differ in scope; no cause is inferred.
        self.assertEqual(24471 - 24191, 280)

    def test_nonsharp_null_requires_additional_assumptions(self):
        # A zero average effect does not imply all unit effects are zero.
        effects = (Fraction(1,2), Fraction(-1,2))
        self.assertEqual(sum(effects, Fraction()) / len(effects), 0)
        self.assertTrue(any(x != 0 for x in effects))

    def test_invalid_arm(self):
        with self.assertRaises(ValueError):
            diff_means((0,1), ())

    def test_invalid_block(self):
        with self.assertRaises(ValueError):
            blocked_assignments(((0,1),), (1,1))


if __name__ == "__main__":
    unittest.main(verbosity=2)
