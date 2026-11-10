"""Pinned cross-PR regression tests; reads Git objects, writes only temp files.

Run from a checkout with the pinned PR objects fetched:
python3 -B -m unittest discover -s research/codex_a/pr_integration_20261110 -v
No network calls, research-file writes, or scientific acceptance claims.
"""
import copy
import importlib.util
import json
from pathlib import Path
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[3]
P3 = '97d5f74df5d84916917db943156120f08144f445'
P8 = 'fd0d2c65084d1ef99b6040ce0464b237c38431b5'
P9 = '89a64ecd2975a7fa0409f000cef45b1b2792a8b4'
MAIN = 'e5f2baa7f6b13b1a2bf95f48ed49571f732e7611'
RECEIPT = 'research/validation/R257_S53_EXACT_RECEIPT_2026-10-29.json'


def blob(commit, path):
    return subprocess.check_output(['git', '-C', str(ROOT), 'show', commit + ':' + path])


def load(commit, path, directory, name):
    target = directory / (name + '.py')
    target.write_bytes(blob(commit, path))
    spec = importlib.util.spec_from_file_location(name, target)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class CrossPRContracts(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.work = Path(self.temp.name)
        self.validator = load(P3, 'research/codex_audit/r257_s53_validator/validate_receipt.py', self.work, 'strict')
        self.data = json.loads(blob(MAIN, RECEIPT))

    def test_current_main_receipt_passes_without_scientific_upgrade(self):
        result = self.validator.validate(self.data)
        self.assertEqual(result['full_scientific_acceptance'], 'PARTIAL')
        self.assertEqual(result['blinded_prescore_order'], 'FAIL')
        self.assertEqual(result['source_authentication'], 'NOT_RUN')

    def test_all_six_pr1_false_accepts_are_rejected_by_pr3(self):
        mutations = {
            'duplicate_world': lambda d: d.update(worlds=[copy.deepcopy(d['worlds'][0]) for _ in range(8)]),
            'duplicate_capacity': lambda d: d['worlds'][0]['perturbations'].__setitem__(4, copy.deepcopy(d['worlds'][0]['perturbations'][0])),
            'multiplier': lambda d: d['worlds'][1].update(baseline_lambda='999'),
            'delta': lambda d: d['worlds'][0]['perturbations'][0].update(delta='999'),
            'derivative': lambda d: d['worlds'][1].update(local_derivative='999'),
            'evidence': lambda d: d.update(evidence='E3'),
        }
        old = load(MAIN, 'research/evidence_audit/b_r257_s53_independent_1d_20261029.py', self.work, 'old')
        for name, mutate in mutations.items():
            with self.subTest(name=name):
                data = copy.deepcopy(self.data)
                mutate(data)
                self.assertEqual(old.compare(data), 72)
                with self.assertRaises(ValueError):
                    self.validator.validate(data)

    def identity_fixture(self):
        gate = load(P9, 'research/codex_audit/r170_identity_gate/identity_gate.py', self.work, 'identity')
        for path in gate.PINS:
            target = self.work / path
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(blob(MAIN, path))
        receipt = self.work / 'B.json'
        receipt.write_bytes(blob(P8, 'research/codex_audit/r170_full_state/logs/B_full_receipt.json'))
        return gate, receipt

    def test_pr8_receipt_passes_pr9_with_current_main_sources(self):
        gate, receipt = self.identity_fixture()
        result = gate.verify(self.work, receipt)
        self.assertEqual(result['source_files_verified'], 4)
        self.assertEqual(result['full_frozen_extension_acceptance'], 'PARTIAL')
        self.assertEqual(result['model_execution_this_gate'], 'NOT_RUN')

    def test_semantically_equal_receipt_cannot_bypass_byte_identity(self):
        gate, receipt = self.identity_fixture()
        receipt.write_text(json.dumps(json.loads(receipt.read_bytes()), separators=(',', ':')))
        with self.assertRaisesRegex(ValueError, 'receipt (length|digest) mismatch'):
            gate.verify(self.work, receipt)

    def test_source_mutation_cannot_reuse_pr8_receipt(self):
        gate, receipt = self.identity_fixture()
        source = self.work / gate.PY
        source.write_bytes(source.read_bytes() + b'\n')
        with self.assertRaisesRegex(ValueError, 'source identity mismatch'):
            gate.verify(self.work, receipt)


if __name__ == '__main__':
    unittest.main()
