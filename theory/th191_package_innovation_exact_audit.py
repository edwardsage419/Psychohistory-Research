"""TH191: exact synthetic two-trait package and innovation audit.

No external data, network access, random sampling, or third-party packages.
"""
from collections import defaultdict
from fractions import Fraction as F
from itertools import product
import unittest

SOURCE = ((0, 0), (1, 1))
STATES = tuple(product((0, 1), repeat=2))


def joint(mode, flip=F(0), source=SOURCE):
    """Exact two-trait output distribution under linked/split donor selection."""
    if mode not in ("linked", "split"):
        raise ValueError("mode")
    if not F(0) <= flip <= F(1):
        raise ValueError("flip")
    n = len(source)
    if n < 1 or any(len(s) != 2 for s in source):
        raise ValueError("source")
    result = defaultdict(F)
    donor_pairs = ((i, i) for i in range(n)) if mode == "linked" else product(range(n), repeat=2)
    denominator = n if mode == "linked" else n * n
    for ia, ib in donor_pairs:
        original = (source[ia][0], source[ib][1])
        for mask in STATES:
            output = (original[0] ^ mask[0], original[1] ^ mask[1])
            probability = (flip if mask[0] else 1 - flip) * (flip if mask[1] else 1 - flip)
            result[output] += probability / denominator
    return {s: result[s] for s in STATES}


def covariance(dist):
    pa = sum(p for (a, b), p in dist.items() if a)
    pb = sum(p for (a, b), p in dist.items() if b)
    pab = dist[(1, 1)]
    return pab - pa * pb


def total_variation(a, b):
    return sum(abs(a[s] - b[s]) for s in STATES) / 2


def mismatched(dist):
    return dist[(0, 1)] + dist[(1, 0)]


def copy_or_flip_probability(input_bit, retention, innovation):
    """Retain source bit with probability retention, else use 0, then flip."""
    if input_bit not in (0, 1):
        raise ValueError("input_bit")
    if not (0 <= retention <= 1 and 0 <= innovation <= 1):
        raise ValueError("probabilities")
    preflip_one = retention * input_bit
    return preflip_one * (1 - innovation) + (1 - preflip_one) * innovation


class ExactAudit(unittest.TestCase):
    def test_linked_normalization(self):
        self.assertEqual(sum(joint("linked").values()), 1)

    def test_split_normalization(self):
        self.assertEqual(sum(joint("split").values()), 1)

    def test_linked_no_flip(self):
        self.assertEqual(joint("linked"), {(0, 0): F(1, 2), (0, 1): F(0), (1, 0): F(0), (1, 1): F(1, 2)})

    def test_split_uniform(self):
        self.assertEqual(joint("split"), dict.fromkeys(STATES, F(1, 4)))

    def test_equal_marginals(self):
        for mode in ("linked", "split"):
            dist = joint(mode)
            self.assertEqual(dist[(1, 0)] + dist[(1, 1)], F(1, 2))
            self.assertEqual(dist[(0, 1)] + dist[(1, 1)], F(1, 2))

    def test_linked_covariance(self):
        self.assertEqual(covariance(joint("linked")), F(1, 4))

    def test_split_covariance(self):
        self.assertEqual(covariance(joint("split")), F(0))

    def test_unflipped_tv(self):
        self.assertEqual(total_variation(joint("linked"), joint("split")), F(1, 2))

    def test_flipped_linked_distribution(self):
        self.assertEqual(joint("linked", F(1, 4)), {(0, 0): F(5, 16), (0, 1): F(3, 16), (1, 0): F(3, 16), (1, 1): F(5, 16)})

    def test_flipped_split_distribution(self):
        self.assertEqual(joint("split", F(1, 4)), dict.fromkeys(STATES, F(1, 4)))

    def test_flipped_covariance(self):
        self.assertEqual(covariance(joint("linked", F(1, 4))), F(1, 16))

    def test_flipped_tv(self):
        self.assertEqual(total_variation(joint("linked", F(1, 4)), joint("split", F(1, 4))), F(1, 8))

    def test_mismatch_probabilities(self):
        self.assertEqual([mismatched(joint(m, e)) for m, e in (("linked", F(0)), ("split", F(0)), ("linked", F(1, 4)), ("split", F(1, 4)))], [F(0), F(1, 2), F(3, 8), F(1, 2)])

    def test_no_source_diversity_no_identification(self):
        source = ((0, 0), (0, 1), (1, 0), (1, 1))
        self.assertEqual(joint("linked", source=source), joint("split", source=source))

    def test_latent_preference_observational_equivalence(self):
        latent_preference = {(0, 0): F(1, 2), (0, 1): F(0), (1, 0): F(0), (1, 1): F(1, 2)}
        self.assertEqual(latent_preference, joint("linked"))

    def test_finite_sample_overlap(self):
        self.assertEqual(mismatched(joint("split")), F(1, 2))
        self.assertEqual((1 - mismatched(joint("split"))) ** 4, F(1, 16))

    def test_retention_innovation_ambiguous_on_input_one(self):
        self.assertEqual(copy_or_flip_probability(1, F(3, 4), F(0)), F(3, 4))
        self.assertEqual(copy_or_flip_probability(1, F(1), F(1, 4)), F(3, 4))

    def test_balanced_input_breaks_that_ambiguity(self):
        self.assertEqual(copy_or_flip_probability(0, F(3, 4), F(0)), F(0))
        self.assertEqual(copy_or_flip_probability(0, F(1), F(1, 4)), F(1, 4))

    def test_invalid_mode(self):
        with self.assertRaises(ValueError):
            joint("unknown")

    def test_invalid_probability(self):
        with self.assertRaises(ValueError):
            joint("linked", F(-1, 4))


if __name__ == "__main__":
    unittest.main(verbosity=2)
