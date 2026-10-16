"""R065 M5 post-failure source-replay gate on synthetic 24-person inputs."""
from copy import deepcopy
import unittest

from r065_phase_l_native_heldout import FOLD_A, FOLD_B, sum_author_nll
from r065_phase_m_model5_fixed_param_diagnostic import evaluate_saved_params


class FixedParameterReplayTests(unittest.TestCase):
    def setUp(self):
        self.frames = list(range(1,25))
        self.plays = [55] * 24
        self.plays[0] = 62  # A 667, B 660
        def objective(theta, person, transform=True):
            if transform is not True:
                raise AssertionError('must use native transformed parameter entrypoint')
            return person * 0.01 + sum(float(x)**2 for x in theta) / 100
        self.objective = objective
        self.cases = {}
        for stage in ('L','M'):
            for fold in ('A','B'):
                test = FOLD_A if fold == 'A' else FOLD_B
                train = FOLD_B if fold == 'A' else FOLD_A
                params = [0.2, 1.2, -0.4, 0.6, 0.8]
                self.cases[stage+'_'+fold] = {
                    'params': params, 'fold': fold,
                    'train_nll': sum_author_nll(objective, params, [self.frames[i] for i in train]),
                    'test_mean_nll': sum_author_nll(objective, params, [self.frames[i] for i in test]) /
                                     sum(self.plays[i] for i in test)
                }

    def test_four_fixed_params_match_identical_evaluation(self):
        result = evaluate_saved_params(self.objective,self.frames,self.plays,self.cases)
        self.assertEqual(result['status'],'FOUR_PARAMETER_VECTORS_REPLAY_PASS')
        self.assertFalse(result['phase_m_seven_model_complete'])
        self.assertEqual(result['phase_m_model5_clock_comparison'],'STILL_FAIL_CLOSED')

    def test_saved_train_nll_mismatch_fails(self):
        d=deepcopy(self.cases)
        d['M_A']['train_nll'] += .00001
        result=evaluate_saved_params(self.objective,self.frames,self.plays,d)
        self.assertEqual(result['status'],'FAIL_CLOSED_FIXED_PARAMS_DISAGREE')

    def test_saved_heldout_nll_mismatch_fails(self):
        d=deepcopy(self.cases)
        d['L_B']['test_mean_nll'] += .00001
        result=evaluate_saved_params(self.objective,self.frames,self.plays,d)
        self.assertEqual(result['status'],'FAIL_CLOSED_FIXED_PARAMS_DISAGREE')

    def test_invalid_person_universe_rejected(self):
        with self.assertRaises(ValueError):
            evaluate_saved_params(self.objective,self.frames[:23],self.plays,self.cases)

    def test_wrong_play_total_rejected(self):
        with self.assertRaises(ValueError):
            evaluate_saved_params(self.objective,self.frames,[50]*24,self.cases)

    def test_extra_parameter_case_rejected(self):
        d=deepcopy(self.cases)
        d['L_A']['params']=[1,2]
        with self.assertRaises(ValueError):
            evaluate_saved_params(self.objective,self.frames,self.plays,d)

    def test_absent_saved_case_rejected(self):
        d=deepcopy(self.cases)
        del d['M_B']
        with self.assertRaises(ValueError):
            evaluate_saved_params(self.objective,self.frames,self.plays,d)


if __name__ == '__main__':
    unittest.main()
