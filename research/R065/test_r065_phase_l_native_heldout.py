"""R065 Phase L synthetic-only controls. No author participant data is shipped."""
import math
import unittest
from unittest.mock import patch

from r065_phase_l_native_heldout import (
    BOUNDS, EXPECTED_PLAYS, FOLD_A, FOLD_B,
    choose_converged, evaluate_model, get_starts, sum_author_nll,
    validate_folds,
)


class FakeNative:
    def get_model_specs(self, num):
        def objective(params, frame, transform=True):
            assert transform is True
            return float(frame + params[0]**2)
        return {'params': ['beta'], 'types': ['0_30'],
                'objective': objective}


class HeldoutGateTests(unittest.TestCase):
    def setUp(self):
        self.frames = list(range(1, 25))
        self.plays = [55]*23 + [62]
        self.assertEqual(sum(self.plays), EXPECTED_PLAYS)

    def test_two_disjoint_stratified_folds(self):
        validate_folds()
        self.assertEqual(len(set(FOLD_A) & set(FOLD_B)), 0)
        self.assertEqual(len(set(FOLD_A) | set(FOLD_B)), 24)

    def test_invalid_strata_rejected(self):
        with self.assertRaises(ValueError):
            validate_folds(tuple(range(12)), tuple(range(12, 24)))

    def test_duplicate_subject_rejected(self):
        with self.assertRaises(ValueError):
            validate_folds((FOLD_A[0],)*12, FOLD_B)

    def test_start_type_exact(self):
        self.assertEqual(get_starts(['0_30','01','05_1']),
                         [[-4.0,0.0,0.0],[-2.0,1.0,1.0]])

    def test_unknown_parameter_rejected(self):
        with self.assertRaises(ValueError):
            get_starts(['broken'])

    def test_training_objective_receives_exact_frames(self):
        seen=[]
        def fn(par, frame, transform=True):
            seen.append(frame)
            return float(frame)
        self.assertEqual(sum_author_nll(fn,[1.0],[1,2,3]),6.0)
        self.assertEqual(seen,[1,2,3])

    def test_nonfinite_objective_rejected(self):
        with self.assertRaises(ValueError):
            sum_author_nll(lambda *_args, **_kw: math.inf,[1.0],[1])

    def test_candidate_must_converge_and_be_finite(self):
        records=[
            {'success':False,'train_total_nll':1.0,'params':[0.0]},
            {'success':True,'train_total_nll':2.0,'params':[1.0]},
            {'success':True,'train_total_nll':3.0,'params':[0.0]},
        ]
        self.assertEqual(choose_converged(records)['train_total_nll'],2.0)
        self.assertIsNone(choose_converged(records[:1]))

    def test_candidate_out_of_bounds_rejected(self):
        self.assertIsNone(choose_converged([
            {'success':True,'train_total_nll':1.0,'params':[BOUNDS[1]+2]}
        ]))

    def test_each_test_subject_never_enters_own_training_fold(self):
        seen=[]
        def fake_fit(obj, types, train_frames):
            seen.append(set(train_frames))
            return {'selected':{'start':0,'train_total_nll':1.0,'params':[0.0]},
                    'candidates':[{'start':0,'success':True,
                                   'train_total_nll':1.0,'nit':0,
                                   'nfev':1,'params':[0.0],'message':'ok'}]}
        with patch('r065_phase_l_native_heldout.fit_one_fold',fake_fit):
            out=evaluate_model(FakeNative(),3,self.frames,self.plays)
        self.assertEqual(out['status'],'TWO_FOLD_COMPLETE')
        self.assertEqual(len(seen),2)
        self.assertEqual(seen[0],{self.frames[i] for i in FOLD_B})
        self.assertEqual(seen[1],{self.frames[i] for i in FOLD_A})
        self.assertAlmostEqual(out['heldout_total_nll'],sum(self.frames))

    def test_unresolved_fold_cannot_be_reported_complete(self):
        with patch('r065_phase_l_native_heldout.fit_one_fold',return_value={
            'selected':None,'candidates':[]
        }):
            out=evaluate_model(FakeNative(),3,self.frames,self.plays)
        self.assertEqual(out['status'],'UNRESOLVED')
        self.assertIsNone(out['heldout_mean_nll'])

    def test_wrong_total_play_rejected(self):
        with self.assertRaises(ValueError):
            evaluate_model(FakeNative(),3,self.frames,[10]*24)


if __name__ == '__main__':
    unittest.main()
