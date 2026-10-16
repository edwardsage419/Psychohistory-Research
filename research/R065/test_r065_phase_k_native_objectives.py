"""Fail-closed synthetic tests for the R065 K native source gate."""
import math
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace

from r065_phase_k_native_objectives import (
    MODEL_IDS, EXPECTED_PLAYS, verified_upstream, assert_model3_anchor,
    evaluate_native,
)


class NativeGateTests(unittest.TestCase):
    def setUp(self):
        self.manifest = {'models': {'author': {
            'beta_optimal': 0.4,
            'in_sample_mean_nll': 0.68,
            'fixed_beta5_mean_nll': 1.2,
        }}}

    def test_model_count_and_order(self):
        self.assertEqual(MODEL_IDS, (1, 2, 3, 4, 5, 6, 7))

    def test_upstream_missing_fails(self):
        with tempfile.TemporaryDirectory() as d:
            with self.assertRaises(FileNotFoundError):
                verified_upstream(Path(d))

    def test_upstream_modified_fails(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d)
            (p / 'objectives.py').write_text('pass\n')
            (p / 'fit_utils.py').write_text('pass\n')
            with self.assertRaisesRegex(ValueError, 'mismatch'):
                verified_upstream(p)

    def test_anchor_passes_exact(self):
        assert_model3_anchor(0.68 * EXPECTED_PLAYS, 1.2 * EXPECTED_PLAYS,
                             self.manifest, EXPECTED_PLAYS)

    def test_anchor_rejects_optimal_disagreement(self):
        with self.assertRaisesRegex(ValueError, 'in_sample_mean_nll'):
            assert_model3_anchor(0.69 * EXPECTED_PLAYS, 1.2 * EXPECTED_PLAYS,
                                 self.manifest, EXPECTED_PLAYS)

    def test_anchor_rejects_beta5_disagreement(self):
        with self.assertRaisesRegex(ValueError, 'fixed_beta5_mean_nll'):
            assert_model3_anchor(0.68 * EXPECTED_PLAYS, 1.21 * EXPECTED_PLAYS,
                                 self.manifest, EXPECTED_PLAYS)

    def test_anchor_rejects_nonfinite(self):
        with self.assertRaises(ValueError):
            assert_model3_anchor(math.nan, 1.2 * EXPECTED_PLAYS,
                                 self.manifest, EXPECTED_PLAYS)

    def test_anchor_rejects_wrong_universe(self):
        with self.assertRaises(ValueError):
            assert_model3_anchor(0.68 * EXPECTED_PLAYS, 1.2 * EXPECTED_PLAYS,
                                 self.manifest, 20)

    def test_native_synthetic_seven_functions(self):
        class FakeNative:
            @staticmethod
            def get_model_specs(model_num):
                def objective(params, df, transform=True):
                    return float(model_num + sum(params))
                return {'params': [0., 0.], 'types': ['01', '0_30'], 'objective': objective}
        with self.assertRaisesRegex(ValueError, 'disagrees'):
            evaluate_native(FakeNative(), ['stub'], self.manifest, EXPECTED_PLAYS)

    def test_native_rejects_bad_universe(self):
        with self.assertRaises(ValueError):
            evaluate_native(SimpleNamespace(), ['stub'], self.manifest, 0)


if __name__ == '__main__':
    unittest.main()
