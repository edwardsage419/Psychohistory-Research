"""TH193: exact synthetic source-dependence and archive-selection counterexamples.

Standard library only. No personal, historical microdata or external services.
"""
from fractions import Fraction as F
from itertools import product
import unittest


def independent_false_reports(error=F(1, 4)):
    """Two independent binary false-positive reports when true event is absent."""
    if not F(0) <= error <= F(1):
        raise ValueError("error must be a probability")
    return {(a, b): (error if a else 1-error) * (error if b else 1-error)
            for a, b in product((0, 1), repeat=2)}


def common_source_false_reports(error=F(1, 4)):
    """Both reports copy the same one-bit upstream report."""
    if not F(0) <= error <= F(1):
        raise ValueError("error must be a probability")
    return {(0, 0): 1-error, (0, 1): F(0),
            (1, 0): F(0), (1, 1): error}


def marginal(report_distribution, position):
    if position not in (0, 1):
        raise ValueError("position must be 0 or 1")
    return sum((p for reports, p in report_distribution.items()
                if reports[position] == 1), F(0))


def archive_observables(prevalence, keep_positive, keep_negative):
    """Observed event only when archived; missing event type is unobserved."""
    vals = (prevalence, keep_positive, keep_negative)
    if any(not F(0) <= x <= F(1) for x in vals):
        raise ValueError("all arguments must be probabilities")
    positive = prevalence * keep_positive
    negative = (1-prevalence) * keep_negative
    return {"kept_positive": positive,
            "kept_negative": negative,
            "missing_untyped": 1-positive-negative}


def archived_positive_rate(observed):
    denominator = observed["kept_positive"] + observed["kept_negative"]
    if denominator == 0:
        raise ValueError("no archived cases")
    return observed["kept_positive"] / denominator


def pair_agreement(reports):
    if len(reports) < 2:
        raise ValueError("need at least two reports")
    return F(sum(a == b for i, a in enumerate(reports)
                 for b in reports[i+1:]), len(reports) * (len(reports)-1)//2)


def accuracy(reports, truth):
    if not reports or truth not in (0, 1) or any(x not in (0, 1) for x in reports):
        raise ValueError("binary truth and nonempty binary reports required")
    return F(sum(x == truth for x in reports), len(reports))


class ExactAudit(unittest.TestCase):
    def setUp(self):
        self.ind = independent_false_reports()
        self.com = common_source_false_reports()
        self.selective = archive_observables(F(1, 2), F(3, 4), F(1, 4))
        self.uniform = archive_observables(F(3, 4), F(1, 2), F(1, 2))

    def test_independent_mass(self):
        self.assertEqual(sum(self.ind.values()), 1)

    def test_common_mass(self):
        self.assertEqual(sum(self.com.values()), 1)

    def test_marginal_independent_first(self):
        self.assertEqual(marginal(self.ind, 0), F(1, 4))

    def test_marginal_common_first(self):
        self.assertEqual(marginal(self.com, 0), F(1, 4))

    def test_marginal_independent_second(self):
        self.assertEqual(marginal(self.ind, 1), F(1, 4))

    def test_marginal_common_second(self):
        self.assertEqual(marginal(self.com, 1), F(1, 4))

    def test_joint_independent(self):
        self.assertEqual(self.ind[(1, 1)], F(1, 16))

    def test_joint_common(self):
        self.assertEqual(self.com[(1, 1)], F(1, 4))

    def test_joint_dependence_factor(self):
        self.assertEqual(self.com[(1, 1)] / self.ind[(1, 1)], 4)

    def test_anti_discordance_common(self):
        self.assertEqual(self.com[(1, 0)] + self.com[(0, 1)], 0)

    def test_discordance_independent(self):
        self.assertEqual(self.ind[(1, 0)] + self.ind[(0, 1)], F(3, 8))

    def test_archive_observables_equal(self):
        self.assertEqual(self.selective, self.uniform)

    def test_archive_positive_mass(self):
        self.assertEqual(self.selective["kept_positive"], F(3, 8))

    def test_archive_negative_mass(self):
        self.assertEqual(self.selective["kept_negative"], F(1, 8))

    def test_archive_missing_mass(self):
        self.assertEqual(self.selective["missing_untyped"], F(1, 2))

    def test_archive_conditional_rate(self):
        self.assertEqual(archived_positive_rate(self.selective), F(3, 4))

    def test_population_prevalence_differs(self):
        self.assertNotEqual(F(1, 2), F(3, 4))

    def test_agreement_true_and_false(self):
        self.assertEqual(pair_agreement((1, 1, 1, 1)), 1)
        self.assertEqual(accuracy((1, 1, 1, 1), 1), 1)
        self.assertEqual(accuracy((1, 1, 1, 1), 0), 0)

    def test_invalid_probability_rejected(self):
        with self.assertRaises(ValueError):
            archive_observables(F(2), F(1, 2), F(1, 2))
        with self.assertRaises(ValueError):
            common_source_false_reports(F(-1, 4))

    def test_empty_archive_rejected(self):
        with self.assertRaises(ValueError):
            archived_positive_rate(archive_observables(F(1, 2), 0, 0))

    def test_bad_pair_input_rejected(self):
        with self.assertRaises(ValueError):
            pair_agreement((1,))

    def test_bad_marginal_index_rejected(self):
        with self.assertRaises(ValueError):
            marginal(self.com, 2)


if __name__ == "__main__":
    unittest.main(verbosity=2)
