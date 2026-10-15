"""Synthetic tests of the author's model-3 reset and softmax definitions."""
import math
import unittest
from r065_phase_h_model3_reset import (AUTHOR_RESET, BLOCK_RESET,
  git_blob_sha1, source_trials, predict, summarize)


def example(day, kind, chosen, available=(0, 1)):
    return {'day': day, 'type': kind, 'chosen': chosen, 'available': list(available)}


class Model3Tests(unittest.TestCase):
    def test_git_hash_formula(self):
        self.assertEqual(git_blob_sha1(b'test content\n'),
                         'd670460b4b4aece5915caf5c68d12f560a9fe3e4')

    def test_raw_source_refuses_synthetic_file(self):
        with self.assertRaisesRegex(ValueError, 'Git blob mismatch'):
            source_trials(b'phase,day\nexperimental,1\n', '0' * 40)

    def test_no_observation_is_uniform(self):
        self.assertAlmostEqual(predict([example(4, 'play', 0)], AUTHOR_RESET)[0]['p'], .5)

    def test_softmax_matches_both_boat_choices(self):
        q = predict([example(1,'observe', 1),example(2,'play',1),example(3,'play',0)],(),beta=5)
        self.assertAlmostEqual(q[0]['p'], 1/(1+math.exp(-5)))
        self.assertAlmostEqual(q[1]['p'], 1/(1+math.exp(+5)))

    def test_last_observed_unavailable_is_uniform(self):
        q=predict([example(1,'observe',0,(0,1)), example(2,'play',2,(1,2))],(),5)
        self.assertEqual(q[0]['p'],.5)

    def test_play_does_not_update_observed_action(self):
        q=predict([example(1,'observe',0),example(2,'play',1),example(3,'play',0)],(),5)
        self.assertGreater(q[1]['p'],.99)

    def test_reset_happens_before_current_play(self):
        q=predict([example(88,'observe',0),example(89,'play',0)],AUTHOR_RESET,5)
        self.assertEqual(q[0]['p'],.5)
        v=predict([example(88,'observe',0),example(89,'play',0)],BLOCK_RESET,5)
        self.assertGreater(v[0]['p'],.99)

    def test_after_boundary_reset_then_observe_updates_normally(self):
        q=predict([example(17,'observe',0),example(18,'observe',1),example(19,'play',1)],BLOCK_RESET,5)
        self.assertGreater(q[0]['p'],.99)

    def test_different_guards_change_prediction_not_trials(self):
        seq=[example(88,'observe',0),example(89,'play',1),example(90,'play',0)]
        a=predict(seq,AUTHOR_RESET,5)
        b=predict(seq,BLOCK_RESET,5)
        self.assertEqual(len(a),len(b))
        self.assertTrue(any(abs(x['p']-y['p'])>.1 for x,y in zip(a,b)))

    def test_invalid_beta_fails(self):
        for x in (float('nan'),float('inf'),-1):
            with self.subTest(x=x), self.assertRaises(ValueError):
                predict([example(2,'play',0)],(),x)

    def test_duplicate_reset_date_fails(self):
        with self.assertRaises(ValueError):
            predict([example(2,'play',0)],(23,23),5)

    def test_missing_day89_play_fails_summary(self):
        with self.assertRaisesRegex(ValueError,'missing day89'):
            summarize([[example(1,'play',0)]])


if __name__=='__main__':
    unittest.main()
