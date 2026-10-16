"""R065 Phase M: synthetic tests for seven-reset adapter and comparison gates."""
import math
import tempfile
import unittest
from pathlib import Path

from r065_phase_k_native_objectives import verified_upstream
from r065_phase_m_native_two_clock import (
    BOUNDARY_CLOCK, ORIGINAL_CLOCK, PARITY_TOL, SOURCE_NEEDLE,
    check_author_clock_parity, compare_clock_fits,
    modify_only_reset_days,
)

TOY_SOURCE = '\n'.join([
    'def synthetic_model_' + str(j) + '(rows):\n'
    '    counter = 0\n'
    '    for row in rows:\n'
    '        ' + SOURCE_NEEDLE + '\n'
    '            counter += 1\n'
    '    return counter\n'
    for j in range(1, 8)
])


class MiniModels:
    def __init__(self, bump=0.0):
        self.bump = bump

    def get_model_specs(self, number):
        def objective(theta, frame, transform=True):
            return (number + self.bump + float(frame) / 100.0 +
                    float(theta[0])**2)
        return {'params': ['beta'], 'types': ['0_30'], 'objective': objective}


def make_fits(nll_a=0.6, nll_b=0.7, model=6):
    return {
        'model_number': model,
        'status': 'TWO_FOLD_COMPLETE',
        'heldout_mean_nll': (nll_a*667 + nll_b*660)/1327,
        'folds': [
            {'test_fold':'A','heldout_play':667,'status':'PASS',
             'heldout_mean_nll':nll_a},
            {'test_fold':'B','heldout_play':660,'status':'PASS',
             'heldout_mean_nll':nll_b},
        ],
    }


class NativeTwoClockSyntheticTests(unittest.TestCase):
    def test_source_pins_exactly_seven_locations(self):
        self.assertEqual(TOY_SOURCE.count(SOURCE_NEEDLE), 7)

    def test_author_clock_is_byte_identical(self):
        self.assertEqual(modify_only_reset_days(TOY_SOURCE, ORIGINAL_CLOCK),
                         TOY_SOURCE)

    def test_candidate_clock_changes_exactly_seven_predicates(self):
        converted = modify_only_reset_days(TOY_SOURCE, BOUNDARY_CLOCK)
        self.assertEqual(converted.count('if row [\'day\'] in [18, 35, 52, 69, 86, 103, 120]:'), 7)
        self.assertEqual(
            converted.replace("if row ['day'] in [18, 35, 52, 69, 86, 103, 120]:", SOURCE_NEEDLE),
            TOY_SOURCE
        )

    def test_synthetic_boundary_actions_change_only_reset_events(self):
        native = {}
        adapted = {}
        exec(compile(TOY_SOURCE, '<native-toy>', 'exec'), native)
        exec(compile(modify_only_reset_days(TOY_SOURCE, BOUNDARY_CLOCK),
                     '<adapted-toy>', 'exec'), adapted)
        rows = [{'day': 18}, {'day': 23}, {'day': 35},
                {'day': 45}, {'day': 120}, {'day': 121}]
        for num in range(1, 8):
            key = 'synthetic_model_' + str(num)
            self.assertEqual(native[key](rows), 2)
            self.assertEqual(adapted[key](rows), 3)

    def test_less_than_seven_occurrences_rejected(self):
        with self.assertRaises(ValueError):
            modify_only_reset_days(TOY_SOURCE.replace(SOURCE_NEEDLE,'NEVER',1),
                                   BOUNDARY_CLOCK)

    def test_extra_eighth_location_rejected(self):
        with self.assertRaises(ValueError):
            modify_only_reset_days(TOY_SOURCE + '\n' + SOURCE_NEEDLE,
                                   BOUNDARY_CLOCK)

    def test_unreviewed_schedule_rejected(self):
        with self.assertRaises(ValueError):
            modify_only_reset_days(TOY_SOURCE, (1,2,3))

    def test_source_hash_mismatch_fails_closed(self):
        with tempfile.TemporaryDirectory() as temp:
            p = Path(temp)
            (p / 'objectives.py').write_text(TOY_SOURCE)
            (p / 'fit_utils.py').write_text('some fake source')
            with self.assertRaises(ValueError):
                verified_upstream(p)

    def test_parity_probe_accepts_identical_author_implementations(self):
        check_author_clock_parity(MiniModels(), MiniModels(), list(range(24)))

    def test_parity_probe_rejects_different_author_implementation(self):
        with self.assertRaises(ValueError):
            check_author_clock_parity(MiniModels(), MiniModels(bump=0.05),
                                     list(range(24)))

    def test_native_crosscheck_requires_24_participants(self):
        with self.assertRaises(ValueError):
            check_author_clock_parity(MiniModels(), MiniModels(), [1,2,3])

    def test_delta_sign_and_weighting(self):
        author = make_fits()
        candidate = make_fits(.55, .72)
        compared = compare_clock_fits(author, candidate, make_fits())
        expected = (-.05*667 + .02*660) / 1327
        self.assertAlmostEqual(compared['candidate_minus_author_nll_per_play'],
                               expected, places=12)
        self.assertLess(expected, 0.0)

    def test_author_clock_must_reproduce_phase_l(self):
        with self.assertRaisesRegex(ValueError, 'Phase L'):
            compare_clock_fits(make_fits(), make_fits(), make_fits(.601,.7))

    def test_original_fit_must_converge(self):
        author = make_fits()
        author['status'] = 'UNRESOLVED'
        with self.assertRaises(ValueError):
            compare_clock_fits(author, make_fits(), make_fits())

    def test_candidate_fit_must_converge(self):
        candidate = make_fits()
        candidate['status'] = 'UNRESOLVED'
        with self.assertRaises(ValueError):
            compare_clock_fits(make_fits(), candidate, make_fits())

    def test_mismatched_fold_rejected(self):
        candidate = make_fits()
        candidate['folds'][0]['heldout_play'] = 666
        with self.assertRaises(ValueError):
            compare_clock_fits(make_fits(), candidate, make_fits())

    def test_nonfinite_delta_rejected(self):
        candidate = make_fits()
        candidate['folds'][0]['heldout_mean_nll'] = math.inf
        with self.assertRaises(ValueError):
            compare_clock_fits(make_fits(), candidate, make_fits())

    def test_model_identity_mismatch_rejected(self):
        with self.assertRaises(ValueError):
            compare_clock_fits(make_fits(), make_fits(model=5), make_fits())


if __name__ == '__main__':
    unittest.main()
