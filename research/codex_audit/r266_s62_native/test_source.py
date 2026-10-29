import copy
import json
from pathlib import Path
import unittest
import source_audit

ROOT=Path(__file__).resolve().parents[3]
class SourceTests(unittest.TestCase):
    def setUp(self):
        self.csv=(ROOT/'research/R266/R266_ALL_5328_FINITE_MONTE_CARLO_ORIGINAL_SOURCES.csv').read_text()
        self.baseline=json.loads((ROOT/'research/R266/R266_EXACT_FINITE_MC_RESULTS.json').read_text())
        self.receipt=json.loads((ROOT/'research/validation/R266_S62_EXACT_SCORE_COVERAGE_RECEIPT_2026-10-29.json').read_text())
    def run_audit(self):return source_audit.audit(self.csv,self.baseline,self.receipt)
    def test_all_sources_and_metrics(self):
        r=self.run_audit();self.assertEqual(r.get('source_rows'),5328);self.assertEqual(r.get('metric_fields'),180)
    def test_frozen_counterexample(self):
        r=self.run_audit();self.assertEqual(r.get('symmetric_N6_antithetic_coverage'),'3/4')
        self.assertEqual(r.get('symmetric_N6_antithetic_variance_ratio'),'1/3')
    def test_missing_source(self):
        self.csv='\n'.join(self.csv.splitlines()[:-1])+'\n'
        with self.assertRaises(ValueError):self.run_audit()
    def test_duplicate_source(self):
        lines=self.csv.splitlines();lines[2]=lines[1];self.csv='\n'.join(lines)+'\n'
        with self.assertRaises(ValueError):self.run_audit()
    def test_self_consistent_wrong_hit(self):
        # First tuple is 0;0 with two Q1 hits. Change every derived field
        # coherently to one hit: only reconstructing the primitive event catches it.
        lines=self.csv.splitlines();r=lines[1].split(',');r[7:]=['1','1/2','1/4','1/16'];lines[1]=','.join(r);self.csv='\n'.join(lines)+'\n'
        with self.assertRaises(ValueError):self.run_audit()
    def test_changed_baseline_variance(self):
        self.baseline['worlds'][0]['designs']['IID']['exact_variance']='999'
        with self.assertRaises(ValueError):self.run_audit()
    def test_wrong_coverage(self):
        self.receipt['results'][0]['exact_score_z2_coverage']='999'
        with self.assertRaises(ValueError):self.run_audit()
    def test_zero_variance_ratio_must_be_null(self):
        row=next(r for r in self.receipt['results'] if r['world']=='THRESHOLD_HALF_N2' and r['design']=='ANTITHETIC');row['naive_plugin_over_actual_variance']='0'
        with self.assertRaises(ValueError):self.run_audit()

if __name__=='__main__':unittest.main()
