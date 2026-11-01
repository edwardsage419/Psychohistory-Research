"""TH195: synthetic exact audit; no participant data, network, or external packages."""
from fractions import Fraction as Q
from itertools import combinations, product
import unittest


def shared_reports(p=Q(1, 2), lam=Q(1, 4)):
    """One shared Bernoulli draw with probability lam, else two independent draws."""
    if not (0 <= p <= 1 and 0 <= lam <= 1):
        raise ValueError("invalid probability")
    result = {}
    for a, b in product((0, 1), repeat=2):
        common = (p if a else 1-p) if a == b else Q(0)
        independent = (p if a else 1-p) * (p if b else 1-p)
        result[(a, b)] = lam * common + (1-lam) * independent
    return result


def truth_mixture(prevalence=Q(1, 2), sensitivity=Q(3, 4), false_positive=Q(1, 4)):
    """Independent reports conditional on unobserved truth Y."""
    if not all(0 <= x <= 1 for x in (prevalence, sensitivity, false_positive)):
        raise ValueError("invalid probability")
    result = {}
    for a, b in product((0, 1), repeat=2):
        result[(a, b)] = sum(
            weight * (rate if a else 1-rate) * (rate if b else 1-rate)
            for weight, rate in ((1-prevalence, false_positive), (prevalence, sensitivity))
        )
    return result


def dyad_assignments(n=4, treated=2):
    """All equally likely fixed-count cluster assignments."""
    if not (0 < treated < n):
        raise ValueError("invalid design")
    return tuple(combinations(range(n), treated))


def observed_contrast(z, y0=(0, 0, 1, 1), y1=(1, 0, 1, 1)):
    """Dyad-weighted difference under a specified assignment."""
    if len(y0) != len(y1) or len(z) in (0, len(y0)):
        raise ValueError("invalid outcomes")
    selected = set(z)
    if len(selected) != len(z) or any(i < 0 or i >= len(y0) for i in z):
        raise ValueError("invalid assignment")
    obs = [y1[i] if i in selected else y0[i] for i in range(len(y0))]
    return (sum(obs[i] for i in selected) / Q(len(selected))
            - sum(obs[i] for i in range(len(y0)) if i not in selected) / Q(len(y0)-len(selected)))


def sharp_null_p(y, z, two_sided=True):
    """Exact conditional Fisher randomization tail, ties included."""
    assignments = dyad_assignments(len(y), len(z))
    observed = observed_contrast(z, y, y)
    values = [observed_contrast(a, y, y) for a in assignments]
    if two_sided:
        return Q(sum(abs(v) >= abs(observed) for v in values), len(values))
    return Q(sum(v >= observed for v in values), len(values))


class TH195SyntheticTests(unittest.TestCase):
    def test_shared_joint(self):
        self.assertEqual(shared_reports(), {(0, 0): Q(5,16), (0,1): Q(3,16), (1,0): Q(3,16), (1,1): Q(5,16)})

    def test_truth_mixture_joint(self):
        self.assertEqual(truth_mixture(), shared_reports())

    def test_distinct_truth_rates(self):
        self.assertNotEqual(Q(0), Q(1,2))
        self.assertEqual(truth_mixture(Q(0), Q(3,4), Q(1,4))[(1,1)], Q(1,16))

    def test_marginals(self):
        for d in (shared_reports(), truth_mixture()):
            self.assertEqual(sum(d.values()), 1)
            self.assertEqual(d[(1,0)] + d[(1,1)], Q(1,2))
            self.assertEqual(d[(0,1)] + d[(1,1)], Q(1,2))

    def test_covariance_identical(self):
        for d in (shared_reports(), truth_mixture()):
            self.assertEqual(d[(1,1)] - Q(1,2)**2, Q(1,16))

    def test_shared_endpoints(self):
        self.assertEqual(shared_reports(lam=Q(0))[(1,1)], Q(1,4))
        self.assertEqual(shared_reports(lam=Q(1))[(1,1)], Q(1,2))

    def test_truth_mixture_conditional_independence(self):
        self.assertEqual(truth_mixture(prevalence=Q(0))[(1,1)], Q(1,16))
        self.assertEqual(truth_mixture(prevalence=Q(1))[(1,1)], Q(9,16))

    def test_invalid_parameters(self):
        with self.assertRaises(ValueError):
            shared_reports(lam=Q(5,4))
        with self.assertRaises(ValueError):
            truth_mixture(prevalence=Q(-1,2))

    def test_design_support(self):
        self.assertEqual(len(dyad_assignments()), 6)
        self.assertEqual(len(set(dyad_assignments())), 6)

    def test_assignment_probability(self):
        self.assertEqual(Q(1, len(dyad_assignments())), Q(1,6))
        self.assertEqual(Q(sum(0 in z for z in dyad_assignments()), 6), Q(1,2))

    def test_ate(self):
        y0, y1 = (0,0,1,1), (1,0,1,1)
        self.assertEqual(sum((Q(b-a) for a,b in zip(y0,y1)),Q())/4, Q(1,4))

    def test_design_unbiased(self):
        self.assertEqual(sum((observed_contrast(z) for z in dyad_assignments()),Q())/6, Q(1,4))

    def test_one_assignment_misleading(self):
        self.assertEqual(observed_contrast((0,1)), Q(-1,2))

    def test_exact_tied_tail(self):
        self.assertEqual(sharp_null_p((0,0,1,1), (0,1)), Q(1,3))
        self.assertEqual(sharp_null_p((0,0,1,1), (0,2)), Q(1))

    def test_design_invalid(self):
        with self.assertRaises(ValueError):
            dyad_assignments(4,4)
        with self.assertRaises(ValueError):
            observed_contrast((0,0))


if __name__ == "__main__":
    unittest.main()
