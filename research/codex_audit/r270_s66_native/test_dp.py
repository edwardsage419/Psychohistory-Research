import copy
from fractions import Fraction as F
import json
from pathlib import Path
import unittest
import dp_oracle as oracle

ROOT=Path(__file__).resolve().parents[3]
RECEIPT=ROOT/'research/validation/R270_S66_EXACT_PPC_ALARM_RECEIPT_2026-10-29.json'

class DPTests(unittest.TestCase):
    def setUp(self):self.data=json.loads(RECEIPT.read_text())
    def test_original_receipt(self):self.assertEqual(oracle.verify(self.data).get('exact_tails'),192)
    def test_dp_count_edge_cases(self):
        c=oracle.counts();self.assertEqual(sum(c.values()),64)
        self.assertEqual(c.get((3,0)),2);self.assertEqual(c.get((0,5)),1)
    def test_original_alternating_tails(self):
        d=oracle.calculate()
        for prior,want in [('1,1','10/429'),('2,2','7/286'),('1,3','16/715')]:
            self.assertEqual(d.get('lower_tails',{}).get(prior,[None]*64)[21],want)
    def test_known_alarm_risk(self):
        a=oracle.calculate().get('alarms',{})
        self.assertEqual(a.get('1,1|1/4|1/20',{}).get('alarm_probability'),'27/2048')
        self.assertEqual(a.get('1,1|1/2|1/5',{}).get('alarm_probability'),'3/16')
    def test_changed_tail_rejected(self):
        self.data['lower_tails']['1,1'][0]='999'
        with self.assertRaises(ValueError):oracle.verify(self.data)
    def test_float_alarm_count_rejected(self):
        self.data['alarms']['1,1|1/4|1/20']['alarm_sequence_count']=2.0
        with self.assertRaises(ValueError):oracle.verify(self.data)
    def test_boolean_source_count_rejected(self):
        self.data['observation_count_per_prior']=False
        with self.assertRaises(ValueError):oracle.verify(self.data)
    def test_missing_tail_rejected(self):
        self.data['lower_tails']['1,1'].pop()
        with self.assertRaises(ValueError):oracle.verify(self.data)
    def test_evidence_promotion_rejected(self):
        self.data['evidence']='E2_HUMAN'
        with self.assertRaises(ValueError):oracle.verify(self.data)
    def test_semantic_key_reorder_allowed(self):
        reordered=dict(reversed(list(self.data.items())))
        self.assertEqual(oracle.verify(reordered).get('alarm_probabilities'),27)

if __name__=='__main__':unittest.main()
