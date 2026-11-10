import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

import run_audit


class SafetyTests(unittest.TestCase):
    def test_failed_rerun_cannot_leave_previous_success_receipt(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / 'out'
            out.mkdir()
            receipt = out / 'execution.json'
            receipt.write_text('{"status":"COMPLETE"}')
            proc = subprocess.run([sys.executable, run_audit.__file__, str(Path(tmp)/'missing'),
                                   '--output', str(out)], capture_output=True, text=True)
            self.assertNotEqual(proc.returncode, 0)
            self.assertFalse(receipt.exists(), 'stale success survives failed rerun')

    def test_successful_audit_does_not_write_in_source_directories(self):
        root = Path(__file__).resolve().parents[3]
        with tempfile.TemporaryDirectory() as tmp:
            sandbox = Path(tmp) / 'source'
            paths = [run_audit.CSV, run_audit.NATIVE, run_audit.RECEIPT, *run_audit.SCRIPTS.values()]
            for path in paths:
                target = sandbox/path
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(root/path, target)
            before = {str(p.relative_to(sandbox)): p.read_bytes() for p in sandbox.rglob('*') if p.is_file()}
            proc = subprocess.run([sys.executable, run_audit.__file__, str(sandbox),
                                   '--output', str(Path(tmp)/'out')], capture_output=True, text=True, timeout=60)
            self.assertEqual(proc.returncode, 0, proc.stderr)
            after = {str(p.relative_to(sandbox)): p.read_bytes() for p in sandbox.rglob('*') if p.is_file()}
            self.assertEqual(set(before), set(after), 'source tree gained files')
            self.assertEqual(before, after)


class OutputAliasTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / 'source'
        self.out = Path(self.temp.name) / 'out'
        self.out.mkdir()
        original = Path(__file__).resolve().parents[3]
        for path in [run_audit.CSV, run_audit.NATIVE, run_audit.RECEIPT, *run_audit.SCRIPTS.values()]:
            target = self.root / path
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(original / path, target)
        self.target = self.root / run_audit.RECEIPT

    def invoke(self):
        options = ['-B'] + (['-O'] if sys.flags.optimize else [])
        return subprocess.run([sys.executable, *options, run_audit.__file__, str(self.root),
                               '--output', str(self.out)], capture_output=True, text=True, timeout=60)

    def check_alias(self, name, hard=False):
        import os
        alias = self.out / name
        if hard:
            os.link(self.target, alias)
        else:
            alias.symlink_to(self.target)
        before = self.target.read_bytes()
        result = self.invoke()
        self.assertEqual(self.target.read_bytes(), before, 'protected input changed through output alias')
        self.assertNotEqual(result.returncode, 0, 'output alias must be rejected')
        self.assertTrue(alias.exists(), 'rejected alias was removed')
        self.assertIn('unsafe output', result.stderr)

    def test_stdout_symlink_cannot_truncate_source(self):
        self.check_alias('native_tests.stdout')

    def test_stderr_symlink_cannot_overwrite_source(self):
        self.check_alias('native_tests.stderr')

    def test_stdout_hardlink_cannot_overwrite_source(self):
        self.check_alias('native_tests.stdout', hard=True)

    def test_execution_alias_rejected_before_stale_unlink(self):
        self.check_alias('execution.json')

    def test_dangling_output_symlink_rejected(self):
        target = self.root / 'must-not-be-created'
        alias = self.out / 'native_tests.stdout'
        alias.symlink_to(target)
        result = self.invoke()
        self.assertFalse(target.exists(), 'source root gained a file through a dangling alias')
        self.assertTrue(alias.is_symlink())
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('unsafe output', result.stderr)


if __name__ == "__main__":
    unittest.main()
