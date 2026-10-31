"""Regression cases name omissions that would weaken the receipt gate."""
import copy
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from validate_receipt import validate

FIXTURE = Path(__file__).resolve().parents[2] / 'validation/R257_S53_EXACT_RECEIPT_2026-10-29.json'
SCRIPT = Path(__file__).with_name('validate_receipt.py')


class ReceiptTests(unittest.TestCase):
    def setUp(self):
        self.data = json.loads(FIXTURE.read_text())

    def test_archive_passes_with_limits(self):
        result = validate(self.data)
        self.assertEqual(result['capacity_certificates'], 40)
        self.assertEqual(result['secants_checked'], 32)
        self.assertEqual(result['baseline_multipliers_checked'], 8)
        self.assertEqual(result['blinded_prescore_order'], 'FAIL')
        self.assertEqual(result['full_scientific_acceptance'], 'PARTIAL')

    def test_reordering_does_not_change_scientific_identity(self):
        expected = validate(self.data)
        self.data['worlds'].reverse()
        for w in self.data['worlds']:
            w['perturbations'].reverse()
            w['secants'].reverse()
        self.assertEqual(validate(self.data), expected)

    def test_complementarity_rejects_objective_consistent_suboptimal_point(self):
        # Feasible, objective-consistent and dual-feasible, but mux*x != 0.
        # Align the secant too so it cannot accidentally mask a missing KKT check.
        self.data['worlds'][0]['perturbations'][1].update(point=['7/10', '1/5'], minimum='1/100')
        self.data['worlds'][0]['secants'][1]['left_secant'] = '-4/25'
        with self.assertRaisesRegex(ValueError, 'complementarity'):
            validate(self.data)

    def test_cli_archive(self):
        p = subprocess.run([sys.executable, str(SCRIPT), str(FIXTURE)], capture_output=True, text=True)
        self.assertEqual(p.returncode, 0, p.stderr)
        self.assertEqual(json.loads(p.stdout)['capacity_certificates'], 40)

    def test_cli_optimized_rejects_wrong_multiplier(self):
        self.data['worlds'][1]['baseline_lambda'] = '999'
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'bad.json'
            path.write_text(json.dumps(self.data))
            p = subprocess.run([sys.executable, '-O', str(SCRIPT), str(path)], capture_output=True, text=True)
        self.assertEqual(p.returncode, 1)
        self.assertEqual(json.loads(p.stdout)['status'], 'BLOCKED')

    def test_cli_rejects_duplicate_json_keys(self):
        raw = FIXTURE.read_text().replace('"evidence": "E1"', '"evidence": "E3", "evidence": "E1"')
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'duplicate.json'
            path.write_text(raw)
            p = subprocess.run([sys.executable, str(SCRIPT), str(path)], capture_output=True, text=True)
        self.assertEqual(p.returncode, 1)
        self.assertEqual(json.loads(p.stdout)['status'], 'BLOCKED')


# Each case removes a necessary validation branch. All expectations are rejection,
# not numeric outputs recomputed with the implementation under test.
MUTATIONS = {
    'duplicate_worlds': lambda d: d.update(worlds=[copy.deepcopy(d['worlds'][0]) for _ in range(8)]),
    'duplicate_capacity': lambda d: d['worlds'][0]['perturbations'].__setitem__(4, copy.deepcopy(d['worlds'][0]['perturbations'][0])),
    'wrong_multiplier': lambda d: d['worlds'][1].update(baseline_lambda='999'),
    'wrong_delta': lambda d: d['worlds'][0]['perturbations'][0].update(delta='999'),
    'wrong_derivative': lambda d: d['worlds'][1].update(local_derivative='999'),
    'evidence_upgrade': lambda d: d.update(evidence='E3'),
    'wrong_minimum': lambda d: d['worlds'][0]['perturbations'][0].update(minimum='999'),
    'feasible_nonoptimal_point': lambda d: d['worlds'][0]['perturbations'][2].update(point=['0', '0'], minimum='2/5'),
    'infeasible_point': lambda d: d['worlds'][0]['perturbations'][0].update(point=['1', '1']),
    'wrong_secant': lambda d: d['worlds'][1]['secants'][0].update(left_secant='0'),
    'duplicate_step': lambda d: d['worlds'][0]['secants'].__setitem__(1, copy.deepcopy(d['worlds'][0]['secants'][0])),
    'missing_world': lambda d: d['worlds'].pop(),
    'unknown_world': lambda d: d['worlds'][0].update(world='NEW_WORLD'),
    'wrong_capacity': lambda d: d['worlds'][0]['perturbations'][0].update(capacity='0'),
    'wrong_baseline_value': lambda d: d['worlds'][1].update(baseline_minimum='0'),
    'wrong_count': lambda d: d.update(capacity_evaluations=39),
    'boolean_count': lambda d: d.update(new_human_E2=False),
    'float_rational': lambda d: d['worlds'][0].update(baseline_capacity=1.0),
    'zero_denominator': lambda d: d['worlds'][0].update(baseline_capacity='1/0'),
    'decimal_string': lambda d: d['worlds'][0].update(baseline_capacity='1.0'),
    'wrong_point_arity': lambda d: d['worlds'][0]['perturbations'][0].update(point=['0']),
    'missing_field': lambda d: d.pop('evidence'),
    'unexpected_field': lambda d: d.update(blinded_order='PASS'),
    'missing_world_list': lambda d: d.update(worlds=None),
    'invalid_world_object': lambda d: d['worlds'].__setitem__(0, None),
    'wrong_nonconvex_control': lambda d: d.update(nonconvex_negative_control='KKT_sufficient'),
}


def rejection_test(mutate):
    def test(self):
        mutate(self.data)
        with self.assertRaises(ValueError):
            validate(self.data)
    return test


for name, mutation in MUTATIONS.items():
    setattr(ReceiptTests, 'test_reject_' + name, rejection_test(mutation))

if __name__ == '__main__':
    unittest.main()
