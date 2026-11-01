#!/usr/bin/env python3
"""Isolated synthetic controls for the eight-model acceptance entrypoint.

These mocks validate orchestration and failure behavior only. They do not
substitute for a native checkout replay of the four archived validators.
"""
import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("gate", HERE / "r333_r340_acceptance_entry_20261101.py")
gate = importlib.util.module_from_spec(spec)
spec.loader.exec_module(gate)

MOCK = '''import json,sys
from pathlib import Path
args=sys.argv[1:]
if len(args)==2 and args[0]=='--root':
    root=Path(args[1]); model=root.name; positional=False
elif len(args)==2:
    model=args[0]; root=Path(args[1]); positional=True
else:
    sys.exit(17)
if not (root/'receipt.txt').is_file() or (root/'receipt.txt').read_text()!='OK':
    sys.exit(18)
if positional:
    print('STRICT_GATE_PASS '+model)
else:
    print(json.dumps({'status':'PASS_BOUNDED_E1_RECEIPT','model':model}))
'''

class AcceptanceTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.audit = self.root / 'research' / 'evidence_audit'
        self.audit.mkdir(parents=True)
        self.specs = {}
        for model, (filename, _, mode) in gate.GATES.items():
            (self.root / 'research' / model).mkdir()
            (self.root / 'research' / model / 'receipt.txt').write_text('OK')
            path = self.audit / filename
            path.write_text(MOCK)
            self.specs[model] = (filename, gate.git_blob(MOCK.encode()), mode)

    def run_gate(self):
        return gate.verify_all(self.root, gate_specs=self.specs, timeout=3)

    def test_valid_all_eight_both_modes(self):
        out = self.run_gate()
        self.assertEqual(out['subprocess_checks'], 16)
        self.assertEqual(len(out['models']), 8)
        self.assertEqual(out['evidence'], 'E1_ARTIFICIAL_ONLY')

    def test_corrupted_validator_rejected_before_execution(self):
        path = self.audit / self.specs['R333'][0]
        path.write_text(path.read_text()+'\n# changed\n')
        with self.assertRaisesRegex(ValueError, 'Git blob mismatch'):
            self.run_gate()

    def test_missing_validator_rejected(self):
        (self.audit / self.specs['R334'][0]).unlink()
        with self.assertRaisesRegex(ValueError, 'validator missing'):
            self.run_gate()

    def test_missing_receipt_rejected(self):
        (self.root / 'research' / 'R338' / 'receipt.txt').unlink()
        with self.assertRaisesRegex(ValueError, 'validator rejected R338'):
            self.run_gate()

    def test_corrupt_receipt_rejected(self):
        (self.root / 'research' / 'R340' / 'receipt.txt').write_text('CORRUPT')
        with self.assertRaisesRegex(ValueError, 'validator rejected R340'):
            self.run_gate()

    def test_missing_model_rejected(self):
        (self.root / 'research' / 'R335' / 'receipt.txt').unlink()
        (self.root / 'research' / 'R335').rmdir()
        with self.assertRaisesRegex(ValueError, 'model directory missing'):
            self.run_gate()

    def test_universe_shrinkage_rejected(self):
        del self.specs['R339']
        with self.assertRaisesRegex(ValueError, 'full eight-model'):
            self.run_gate()

    def test_spoofed_success_stdout_rejected(self):
        filename = self.specs['R333'][0]
        new = MOCK.replace("print('STRICT_GATE_PASS '+model)", "print('PRODUCTION_REPLAY_PASS '+model)")
        (self.audit / filename).write_text(new)
        for model in ('R333','R337','R338','R339'):
            self.specs[model] = (filename, gate.git_blob(new.encode()), 'positional')
        with self.assertRaisesRegex(ValueError, 'invalid validator success receipt'):
            self.run_gate()

    def test_wrong_json_status_rejected(self):
        filename = self.specs['R334'][0]
        new = MOCK.replace("'PASS_BOUNDED_E1_RECEIPT'", "'PASS_EMPIRICAL_E2'")
        (self.audit / filename).write_text(new)
        self.specs['R334'] = (filename, gate.git_blob(new.encode()), 'root')
        with self.assertRaisesRegex(ValueError, 'invalid validator E1 status'):
            self.run_gate()

    def test_symlink_validator_rejected(self):
        name = self.specs['R334'][0]
        target = self.audit / name
        target.rename(self.audit / 'backup.py')
        target.symlink_to(self.audit / 'backup.py')
        with self.assertRaisesRegex(ValueError, 'symlink'):
            self.run_gate()

    def test_conflicting_shared_validator_pins_rejected(self):
        name, sha, mode = self.specs['R333']
        self.specs['R337'] = (name, '0'*40, mode)
        with self.assertRaisesRegex(ValueError, 'Git blob mismatch'):
            self.run_gate()

    def test_optimized_unittest_runner(self):
        self.assertTrue(gate.GATES['R340'][0].endswith('.py'))

if __name__ == '__main__':
    unittest.main()
