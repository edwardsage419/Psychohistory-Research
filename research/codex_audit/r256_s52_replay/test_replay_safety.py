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


if __name__ == '__main__':
    unittest.main()
