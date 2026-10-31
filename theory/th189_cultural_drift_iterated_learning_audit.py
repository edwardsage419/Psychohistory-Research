"""TH189: exact synthetic audits of neutral drift and iterated learning.

No human microdata, external libraries, network access or stochastic sampling.
Run: python -m unittest -v th189_cultural_drift_iterated_learning_audit.py
"""
from fractions import Fraction as F
from math import comb
import unittest


def wf_prob(n, k, j):
    """One neutral Wright-Fisher generation: n offspring sample with replacement."""
    if not (0 <= k <= n and 0 <= j <= n and n > 0):
        raise ValueError("invalid population state")
    p = F(k, n)
    return F(comb(n, j)) * p**j * (1-p)**(n-j)


def heterozygosity(p):
    return 2*p*(1-p)


def innovate(p, mu):
    """Symmetric binary mutation/innovation, independent of parent identity."""
    if not (0 <= p <= 1 and 0 <= mu <= 1):
        raise ValueError("probability outside [0,1]")
    return mu + (1-2*mu)*p


PRIOR = F(3, 4)
ACCURACY = F(3, 4)


def likelihood(d, h):
    if d not in (0, 1) or h not in (0, 1):
        raise ValueError("binary states only")
    return ACCURACY if d == h else 1-ACCURACY


def posterior_one(d):
    numerator = PRIOR * likelihood(d, 1)
    denominator = numerator + (1-PRIOR)*likelihood(d, 0)
    return numerator/denominator


def sample_transition(h):
    """P(next hypothesis=1 | previous hypothesis=h), one signal per learner."""
    return sum((likelihood(d, h)*posterior_one(d) for d in (0, 1)), F(0))


def next_probability(p):
    return p*sample_transition(1)+(1-p)*sample_transition(0)


def iterated_probability(p, steps):
    for _ in range(steps):
        p = next_probability(p)
    return p


def map_transition(h, tie_to_one=False):
    """Deterministic MAP, with a declared tie rule."""
    return sum((likelihood(d, h)*F(int(posterior_one(d) > F(1,2) or
                    (tie_to_one and posterior_one(d) == F(1,2))))
                for d in (0, 1)), F(0))


class NeutralDriftTests(unittest.TestCase):
    def test_distribution(self):
        self.assertEqual([wf_prob(4,2,j) for j in range(5)],
                         [F(1,16),F(4,16),F(6,16),F(4,16),F(1,16)])
    def test_normalization(self):
        self.assertEqual(sum(wf_prob(4,2,j) for j in range(5)), 1)
    def test_expected_frequency(self):
        self.assertEqual(sum(F(j,4)*wf_prob(4,2,j) for j in range(5)), F(1,2))
    def test_variance(self):
        self.assertEqual(sum((F(j,4)-F(1,2))**2*wf_prob(4,2,j)
                             for j in range(5)), F(1,16))
    def test_heterozygosity(self):
        self.assertEqual(sum(heterozygosity(F(j,4))*wf_prob(4,2,j)
                             for j in range(5)), F(3,8))
    def test_fixation_one_step(self):
        self.assertEqual(wf_prob(4,2,0)+wf_prob(4,2,4), F(1,8))
    def test_zero_absorbing(self):
        self.assertEqual([wf_prob(4,0,j) for j in range(5)], [1,0,0,0,0])
    def test_one_absorbing(self):
        self.assertEqual([wf_prob(4,4,j) for j in range(5)], [0,0,0,0,1])
    def test_symmetry(self):
        self.assertEqual([wf_prob(4,1,j) for j in range(5)],
                         [wf_prob(4,3,4-j) for j in range(5)])
    def test_population_size_effect(self):
        for n in (2,4,6):
            p = F(1,2)
            self.assertEqual(sum((F(j,n)-p)**2*wf_prob(n,n//2,j)
                                 for j in range(n+1)), p*(1-p)/n)
    def test_invalid_population(self):
        with self.assertRaises(ValueError): wf_prob(0,0,0)


class InnovationTests(unittest.TestCase):
    def test_no_innovation(self): self.assertEqual(innovate(F(1,4),F(0)),F(1,4))
    def test_symmetric_innovation(self): self.assertEqual(innovate(F(1,4),F(1,10)),F(3,10))
    def test_half_innovation(self): self.assertEqual(innovate(F(1,4),F(1,2)),F(1,2))
    def test_invalid_rate(self):
        with self.assertRaises(ValueError): innovate(F(1,4),F(3,2))


class IteratedLearningTests(unittest.TestCase):
    def test_posterior_positive(self): self.assertEqual(posterior_one(1),F(9,10))
    def test_posterior_negative(self): self.assertEqual(posterior_one(0),F(1,2))
    def test_transition_from_one(self): self.assertEqual(sample_transition(1),F(4,5))
    def test_transition_from_zero(self): self.assertEqual(sample_transition(0),F(3,5))
    def test_prior_stationary(self): self.assertEqual(next_probability(PRIOR),PRIOR)
    def test_start_zero_one_step(self): self.assertEqual(iterated_probability(F(0),1),F(3,5))
    def test_start_zero_three_steps(self):
        self.assertEqual(iterated_probability(F(0),3),F(3,4)*(1-F(1,125)))
    def test_start_one_three_steps(self):
        self.assertEqual(iterated_probability(F(1),3),F(3,4)+F(1,4*125))
    def test_second_eigenvalue(self):
        self.assertEqual(sample_transition(1)-sample_transition(0),F(1,5))
    def test_map_tie_rule(self):
        self.assertEqual((map_transition(1,False),map_transition(0,False)),
                         (F(3,4),F(1,4)))
        self.assertEqual((map_transition(1,True),map_transition(0,True)),(1,1))
    def test_map_not_sampling(self):
        self.assertNotEqual(map_transition(1,False),sample_transition(1))
    def test_invalid_observation(self):
        with self.assertRaises(ValueError): posterior_one(2)


if __name__ == '__main__':
    unittest.main()
