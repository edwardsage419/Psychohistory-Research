"""No individual trial data used; all checks are aggregate arithmetic or synthetic."""
import copy
import json
import unittest
from pathlib import Path
from r065_phase_g_cell_certificate import cell_score, certificate

TABLE = json.loads((Path(__file__).parent/'R065_PHASE_G_CELLS.json').read_text())['cells']

class TestAggregateCells(unittest.TestCase):
    def test_m2_matches_archived_phase_d(self):
        r=certificate(TABLE)
        self.assertAlmostEqual(r['scores']['M2']['logloss'], 0.6615627546126365, places=12)
        self.assertAlmostEqual(r['scores']['M2']['brier'], 0.2343594760065642, places=12)

    def test_m3_matches_archived_phase_d(self):
        r=certificate(TABLE)
        self.assertAlmostEqual(r['scores']['M3']['logloss'], 0.6630223954616707, places=12)
        self.assertAlmostEqual(r['scores']['M3']['brier'], 0.2350364741552214, places=12)

    def test_aliasing_by_parity(self):
        for i,x in enumerate(TABLE):
            self.assertEqual(x['high_n'],121 if i%2==0 else 105)
            self.assertEqual(x['low_n'],105 if i%2==0 else 121)

    def test_day89_counts(self):
        self.assertEqual(TABLE[5]['high_copied']+TABLE[5]['low_copied'],73)

    def test_aggregate_copy_counts(self):
        self.assertEqual(sum(x['high_copied'] for x in TABLE),344)
        self.assertEqual(sum(x['low_copied'] for x in TABLE),340)

    def test_known_two_subject_cell(self):
        loss,brier = cell_score(2,1,4)
        self.assertAlmostEqual(loss, -2*__import__('math').log(4/9),places=12)
        self.assertAlmostEqual(brier, 2*(5/9)**2,places=12)

    def test_extreme_cells_finite(self):
        for n,k in ((2,0),(2,2),(226,0),(226,226)):
            with self.subTest(n=n,k=k):
                a,b=cell_score(n,k)
                self.assertGreaterEqual(a,0)
                self.assertGreaterEqual(b,0)

    def test_bad_counts_refused(self):
        for n,k in ((0,0),(2,-1),(2,3),(2.3,1),(True,0)):
            with self.subTest(n=n,k=k),self.assertRaises(ValueError):
                cell_score(n,k)

    def test_changed_copy_counts_fail_closed(self):
        t=copy.deepcopy(TABLE)
        t[0]['high_copied']+=1
        with self.assertRaisesRegex(ValueError,'total'):
            certificate(t)

    def test_changed_sequence_allocation_fails(self):
        t=copy.deepcopy(TABLE)
        t[0]['high_n']=120
        with self.assertRaisesRegex(ValueError,'counterbalance'):
            certificate(t)

    def test_prior_sensitivity_is_real(self):
        self.assertNotEqual(certificate(TABLE,1)['scores']['M2']['logloss'],certificate(TABLE,4)['scores']['M2']['logloss'])

    def test_reject_invalid_prior(self):
        with self.assertRaises(ValueError):
            certificate(TABLE,0)

if __name__=='__main__':
    unittest.main()
