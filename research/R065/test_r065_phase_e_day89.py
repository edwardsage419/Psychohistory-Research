"""Synthetic, no real participant records; 8 constrained tests."""
import math
import unittest
from r065_phase_e_day89 import analyze,heldout_prediction,parse_verified


def fake(n=12):
    days=(4,21,38,55,72,89,106,123)
    out=[]
    for i in range(n):
        first='high' if i%2==0 else 'low'
        for j,day in enumerate(days):
            stake=first if j%2==0 else ('low' if first=='high' else 'high')
            copied=int((j==5 and i%3==0) or j==0)
            out.append({'participant_id':str(i),'critical':'1','day':str(day),
                        'accurate':str(1-copied),'copied':str(copied),'stakes':stake,
                        'counterbalance':'1' if first=='high' else '0',
                        'comprehension_check_repetitions':'0'})
    return out


class TestPhaseE(unittest.TestCase):
    def test_exact_sha_gate(self):
        with self.assertRaisesRegex(ValueError,'blob identity'):
            parse_verified(b'not the author source')

    def test_two_opposite_heldouts(self):
        self.assertAlmostEqual(heldout_prediction(1,1,2),4/9)
        self.assertAlmostEqual(heldout_prediction(0,1,2),5/9)

    def test_zero_and_one_extreme_still_finite(self):
        for y,k in ((0,0),(1,12)):
            v=heldout_prediction(y,k,12)
            self.assertTrue(0 < v < 1)

    def test_subject_count_and_loss(self):
        v=analyze(fake(),draws=5)
        self.assertEqual(v['eligible_participants'],12)
        self.assertEqual(v['copied_day89'],4)
        self.assertAlmostEqual(v['uniform_logloss'],math.log(2))

    def test_seed_reproducible(self):
        self.assertEqual(analyze(fake(),draws=7),analyze(fake(),draws=7))

    def test_critical_complement_fails(self):
        data=fake()
        data[0]['accurate']='1'
        with self.assertRaisesRegex(ValueError,'complementary'):
            analyze(data,draws=3)

    def test_wrong_day_fails(self):
        data=fake()
        data[0]['day']='999'
        with self.assertRaisesRegex(ValueError,'critical schedule'):
            analyze(data,draws=3)

    def test_exclusions_before_critical(self):
        data=fake()
        for row in data:
            if row['participant_id']=='0':
                row['comprehension_check_repetitions']='3'
        v=analyze(data,draws=5)
        self.assertEqual(v['eligible_participants'],11)
        self.assertEqual(v['excluded']['union'],1)


if __name__=='__main__':
    unittest.main()
