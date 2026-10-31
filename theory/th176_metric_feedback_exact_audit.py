"""TH176 artificial metric feedback audit, standard library only.

All numbers are synthetic. These tests establish algebraic examples,
not empirical effects, model calibration, or causal identification.
"""
from fractions import Fraction as F
import unittest

HALF = F(1, 2)


def response(b, kappa, audit=F(0)):
    """Agent maximizes b(x+g)-x^2/2-(1/kappa+audit)*g^2/2.

    x is genuine improvement; g is metric manipulation. The baseline
    latent and reported scores are 1/2. For kappa=0 gaming is disabled.
    """
    b, kappa, audit = F(b), F(kappa), F(audit)
    if min(b, kappa, audit) < 0:
        raise ValueError("parameters must be nonnegative")
    x = b
    g = b / (1 / kappa + audit) if kappa else F(0)
    measured = HALF + x + g
    latent = HALF + x - g / 2
    return {"x": x, "g": g, "measured": measured, "latent": latent}


def same_proxy_worlds():
    """Same reported rate, distinct latent outcomes and mechanisms."""
    return (
        (HALF + F(1, 10), HALF + F(1, 10)),
        (HALF + F(1, 10), HALF - F(1, 20)),
    )


def selective_denominator():
    """Synthetic 20 easy and 80 hard cases; exclude 40 failures."""
    easy_n, easy_success = 20, 18
    hard_n, hard_success = 80, 32
    full = F(easy_success + hard_success, easy_n + hard_n)
    reported = F(easy_success + hard_success, easy_n + hard_n - 40)
    return full, reported


class MetricFeedbackAudit(unittest.TestCase):
    def test_zero_incentive(self):
        self.assertEqual(response(0, 4)["measured"], HALF)

    def test_zero_incentive_latent(self):
        self.assertEqual(response(0, 4)["latent"], HALF)

    def test_high_gaming_x(self):
        self.assertEqual(response(F(1, 10), 4)["x"], F(1, 10))

    def test_high_gaming_g(self):
        self.assertEqual(response(F(1, 10), 4)["g"], F(2, 5))

    def test_high_gaming_reported(self):
        self.assertEqual(response(F(1, 10), 4)["measured"], F(1))

    def test_high_gaming_latent(self):
        self.assertEqual(response(F(1, 10), 4)["latent"], F(2, 5))

    def test_audit_g(self):
        self.assertEqual(response(F(1, 10), 4, 1)["g"], F(2, 25))

    def test_audit_reported(self):
        self.assertEqual(response(F(1, 10), 4, 1)["measured"], F(17, 25))

    def test_audit_latent(self):
        self.assertEqual(response(F(1, 10), 4, 1)["latent"], F(14, 25))

    def test_threshold_audit(self):
        self.assertEqual(response(F(1, 10), 4, F(1, 4))["latent"], HALF)

    def test_weak_gaming_improves_latent(self):
        self.assertEqual(response(F(1, 10), 1)["latent"], F(11, 20))

    def test_no_gaming_improves_latent(self):
        self.assertEqual(response(F(1, 10), 0)["latent"], F(3, 5))

    def test_measured_latent_gap(self):
        for k in (F(0), F(1), F(4)):
            r = response(F(1, 10), k)
            self.assertEqual(r["measured"] - r["latent"], F(3, 2) * r["g"])

    def test_equal_proxy_worlds(self):
        a, b = same_proxy_worlds()
        self.assertEqual(a[0], b[0])
        self.assertEqual(a[0], F(3, 5))
        self.assertEqual(a[1], F(3, 5))
        self.assertEqual(b[1], F(9, 20))

    def test_selection_baseline(self):
        self.assertEqual(selective_denominator()[0], HALF)

    def test_selection_reported(self):
        self.assertEqual(selective_denominator()[1], F(5, 6))

    def test_selection_excluded_feasible(self):
        self.assertLessEqual(40, 80 - 32)

    def test_first_order_conditions(self):
        b, k, a = F(1, 10), F(4), F(1)
        r = response(b, k, a)
        self.assertEqual(b - r["x"], 0)
        self.assertEqual(b - (1 / k + a) * r["g"], 0)

    def test_strict_concavity(self):
        self.assertGreater(1 / F(4) + F(1), 0)

    def test_invalid_parameter(self):
        with self.assertRaises(ValueError):
            response(F(-1, 10), 4)


if __name__ == "__main__":
    unittest.main(verbosity=2)
