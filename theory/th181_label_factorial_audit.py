"""TH181: artificial exact arithmetic only. No participant or empirical data."""
from fractions import Fraction as F
import unittest

CELLS = {(0, 0): F(2, 5), (1, 0): F(1, 2),
         (0, 1): F(3, 5), (1, 1): F(7, 10)}


def factorial_contrasts(cells):
    """Descriptive potential-outcome contrasts under a hypothetical randomized 2x2 design."""
    for l in (0, 1):
        for k in (0, 1):
            if (l, k) not in cells or not 0 <= cells[l, k] <= 1:
                raise ValueError('Missing or invalid cell')
    return {
        'label_at_k0': cells[1, 0] - cells[0, 0],
        'label_at_k1': cells[1, 1] - cells[0, 1],
        'evaluator_at_l0': cells[0, 1] - cells[0, 0],
        'evaluator_at_l1': cells[1, 1] - cells[1, 0],
        'interaction': cells[1, 1] - cells[1, 0] - cells[0, 1] + cells[0, 0],
    }


def missing_binary_bounds(total, observed, positives):
    """Sharp logical bounds with no restrictions on missing binary outcomes."""
    if not all(isinstance(x, int) for x in (total, observed, positives)):
        raise TypeError('Counts must be integers')
    if total <= 0 or not 0 <= positives <= observed <= total:
        raise ValueError('Invalid counts')
    return (F(positives, total), F(positives + total - observed, total))


def difference_bounds(a, b):
    """Sharp independent-group interval for b minus a."""
    return (b[0] - a[1], b[1] - a[0])


class SyntheticAudit(unittest.TestCase):
    def test_four_cells(self): self.assertEqual(len(CELLS), 4)
    def test_all_probabilities(self): self.assertTrue(all(0 <= p <= 1 for p in CELLS.values()))
    def test_label_at_k0(self): self.assertEqual(factorial_contrasts(CELLS)['label_at_k0'], F(1, 10))
    def test_label_at_k1(self): self.assertEqual(factorial_contrasts(CELLS)['label_at_k1'], F(1, 10))
    def test_evaluator_at_l0(self): self.assertEqual(factorial_contrasts(CELLS)['evaluator_at_l0'], F(1, 5))
    def test_evaluator_at_l1(self): self.assertEqual(factorial_contrasts(CELLS)['evaluator_at_l1'], F(1, 5))
    def test_zero_interaction(self): self.assertEqual(factorial_contrasts(CELLS)['interaction'], 0)
    def test_missing_cell(self):
        with self.assertRaises(ValueError): factorial_contrasts({(0, 0): F(1, 2)})
    def test_invalid_probability(self):
        with self.assertRaises(ValueError): factorial_contrasts({**CELLS, (0, 0): F(3, 2)})
    def test_true_full_rates(self): self.assertEqual(F(30, 50) - F(20, 50), F(1, 5))
    def test_selected_rates_reverse(self): self.assertEqual(F(10, 30) - F(20, 30), -F(1, 3))
    def test_missing_l0(self): self.assertEqual(missing_binary_bounds(50, 30, 20), (F(2, 5), F(4, 5)))
    def test_missing_l1(self): self.assertEqual(missing_binary_bounds(50, 30, 10), (F(1, 5), F(3, 5)))
    def test_difference_bounds(self):
        a = missing_binary_bounds(50, 30, 20)
        b = missing_binary_bounds(50, 30, 10)
        self.assertEqual(difference_bounds(a, b), (-F(3, 5), F(1, 5)))
    def test_truth_within_bounds(self):
        lo, hi = difference_bounds(missing_binary_bounds(50, 30, 20), missing_binary_bounds(50, 30, 10))
        self.assertTrue(lo <= F(1, 5) <= hi)
    def test_invalid_count(self):
        with self.assertRaises(ValueError): missing_binary_bounds(50, 30, 31)
    def test_noninteger_count(self):
        with self.assertRaises(TypeError): missing_binary_bounds(50, 30.0, 10)
    def test_full_observation_point(self): self.assertEqual(missing_binary_bounds(50, 50, 20), (F(2, 5), F(2, 5)))


if __name__ == '__main__':
    unittest.main(verbosity=2)
