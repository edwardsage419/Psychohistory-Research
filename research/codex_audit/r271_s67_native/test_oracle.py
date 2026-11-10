import copy
from fractions import Fraction as F
import json
from pathlib import Path
import unittest
import oracle

ROOT=Path(__file__).resolve().parents[3]
DATA=ROOT/'research/validation/R271_S67_EXACT_FAMILYWISE_RISKS.json'

class OracleTests(unittest.TestCase):
    def setUp(self):self.obj=json.loads(DATA.read_text())
    def test_archived_27_worlds(self):
        self.assertEqual(oracle.verify_results(self.obj).get('worlds_verified'),27)
    def test_hand_derived_overlap_contrasts(self):
        r=oracle.risks()
        self.assertEqual(r.get('ROLLING_M2_FLEXIBLE_ANY'),F(3,32))
        self.assertEqual(r.get('ROLLING_M3_FLEXIBLE_ANY'),F(1,8))
        self.assertEqual(r.get('DISJOINT_M3_FLEXIBLE_ANY'),F(721,4096))
        self.assertEqual(r.get('DISJOINT_M3_BONFERRONI_ANY'),0)
        self.assertEqual(r.get('IDENTICAL_M3_FLEXIBLE_ANY'),F(1,16))
    def test_duplicate_world_rejected(self):
        self.obj['worlds'][1]=copy.deepcopy(self.obj['worlds'][0])
        with self.assertRaises(ValueError):oracle.verify_results(self.obj)
    def test_missing_world_rejected(self):
        self.obj['worlds'].pop()
        with self.assertRaises(ValueError):oracle.verify_results(self.obj)
    def test_wrong_exact_fraction_rejected(self):
        self.obj['worlds'][0]['exact_familywise_false_positive_risk']='999'
        with self.assertRaises(ValueError):oracle.verify_results(self.obj)
    def test_boolean_source_count_rejected(self):
        self.obj['worlds'][0]['source_count']=True
        with self.assertRaises(ValueError):oracle.verify_results(self.obj)
    def test_original_freeze_claim_change_rejected(self):
        self.obj['R073']='MODIFIED'
        with self.assertRaises(ValueError):oracle.verify_results(self.obj)
    def test_promotion_to_blind_rejected(self):
        self.obj['strict_blind_prescore_freeze']=True
        with self.assertRaises(ValueError):oracle.verify_results(self.obj)

if __name__=='__main__':unittest.main()
