import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

import authenticate as gate

ROOT = Path(__file__).resolve().parents[3]
PR3 = '97d5f74df5d84916917db943156120f08144f445'
VP = 'research/codex_audit/r257_s53_validator/validate_receipt.py'
RECEIPT = 'research/validation/R257_S53_EXACT_RECEIPT_2026-10-29.json'


class AuthenticatedTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / 'root'
        self.validator = Path(self.temp.name) / 'validator.py'
        self.validator.write_bytes(subprocess.check_output(['git', '-C', str(ROOT), 'show', PR3 + ':' + VP]))
        for path in gate.PINS:
            target = self.root / path
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(ROOT / path, target)

    def test_authentic_composition_preserves_limits(self):
        result = gate.verify(self.root, self.validator)
        self.assertEqual(result['status'], 'COMPLETE_PINNED_COMPOSITION')
        self.assertEqual(result['source_link']['original_rows'], 225)
        self.assertEqual(result['mathematical_gate']['capacity_certificates'], 40)
        self.assertEqual(result['mathematical_gate']['source_authentication'], 'NOT_RUN')
        self.assertEqual(result['full_scientific_acceptance'], 'PARTIAL')
        self.assertEqual(result['blinded_prescore_order'], 'FAIL')
        self.assertEqual(len(result['identities']), len(gate.PINS) + 1)

    def test_every_changed_pinned_input_is_rejected(self):
        for path in gate.PINS:
            with self.subTest(path=path):
                target = self.root / path
                raw = target.read_bytes()
                target.write_bytes(raw + b'\n')
                with self.assertRaisesRegex(ValueError, 'identity mismatch'):
                    gate.verify(self.root, self.validator)
                target.write_bytes(raw)

    def test_semantic_receipt_reserialization_is_rejected(self):
        target = self.root / RECEIPT
        target.write_text(json.dumps(json.loads(target.read_bytes()), separators=(',', ':')))
        with self.assertRaisesRegex(ValueError, 'identity mismatch'):
            gate.verify(self.root, self.validator)

    def test_changed_validator_rejected_before_execution(self):
        marker = Path(self.temp.name) / 'EXECUTED'
        self.validator.write_text('from pathlib import Path\nPath(' + repr(str(marker)) + ').touch()\n')
        with self.assertRaisesRegex(ValueError, 'identity mismatch'):
            gate.verify(self.root, self.validator)
        self.assertFalse(marker.exists())

    def test_missing_validator_rejected(self):
        self.validator.unlink()
        with self.assertRaises(OSError):
            gate.verify(self.root, self.validator)

    def test_missing_receipt_rejected(self):
        (self.root / RECEIPT).unlink()
        with self.assertRaises(OSError):
            gate.verify(self.root, self.validator)

    def test_untrusted_child_success_is_rejected(self):
        fake = subprocess.CompletedProcess([], 0, '{"status":"COMPLETE"}', '')
        with patch.object(gate.subprocess, 'run', return_value=fake):
            with self.assertRaisesRegex(ValueError, 'summary mismatch'):
                gate.verify(self.root, self.validator)

    def test_boolean_count_in_child_math_summary_is_rejected(self):
        bad = dict(gate.MATH_EXPECTED, new_human_E2=False)
        source = subprocess.CompletedProcess([], 0, json.dumps(gate.SOURCE_EXPECTED), '')
        math = subprocess.CompletedProcess([], 0, json.dumps(bad), '')
        with patch.object(gate.subprocess, 'run', side_effect=[source, math]):
            with self.assertRaisesRegex(ValueError, 'summary mismatch'):
                gate.verify(self.root, self.validator)

    def test_duplicate_child_json_key_is_rejected(self):
        raw = json.dumps(gate.SOURCE_EXPECTED)
        raw = raw.replace('"original_rows": 225', '"original_rows": 999, "original_rows": 225')
        fake = subprocess.CompletedProcess([], 0, raw, '')
        with patch.object(gate.subprocess, 'run', return_value=fake):
            with self.assertRaisesRegex(ValueError, 'duplicate JSON key'):
                gate.verify(self.root, self.validator)

    def test_child_failure_is_not_accepted(self):
        fake = subprocess.CompletedProcess([], 1, '{}', 'failure')
        with patch.object(gate.subprocess, 'run', return_value=fake):
            with self.assertRaisesRegex(ValueError, 'child exit'):
                gate.verify(self.root, self.validator)

    def test_cli_and_sources_unchanged(self):
        files = [self.root / p for p in gate.PINS] + [self.validator]
        before = {str(p): hashlib.sha256(p.read_bytes()).hexdigest() for p in files}
        command = [sys.executable, '-B'] + (['-O'] if sys.flags.optimize else [])
        command += [str(Path(gate.__file__)), str(self.root), '--validator', str(self.validator)]
        good = subprocess.run(command, capture_output=True, text=True)
        self.assertEqual(good.returncode, 0, good.stderr)
        self.assertEqual(json.loads(good.stdout)['status'], 'COMPLETE_PINNED_COMPOSITION')
        self.assertEqual(before, {str(p): hashlib.sha256(p.read_bytes()).hexdigest() for p in files})
        (self.root / RECEIPT).unlink()
        bad = subprocess.run(command, capture_output=True, text=True)
        self.assertNotEqual(bad.returncode, 0)
        self.assertEqual(json.loads(bad.stdout)['status'], 'BLOCKED')


if __name__ == '__main__':
    unittest.main()
