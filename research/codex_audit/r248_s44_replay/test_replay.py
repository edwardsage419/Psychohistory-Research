import copy
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
import run_audit

ROOT=Path(__file__).resolve().parents[3]
RECEIPT='research/validation/R248_S44_FINITE_TRAJECTORY_EXACT_RECEIPT_2026-10-29.json'
META={'prescore_freeze_commit','source_git_blob'}


class Tests(unittest.TestCase):
    def setUp(self):
        self.archive=json.loads((ROOT/RECEIPT).read_text())
        self.generated={k:copy.deepcopy(v) for k,v in self.archive.items() if k not in META}

    def test_genuine_receipt_passes(self):
        run_audit.check_receipt(self.generated,self.archive)

    def test_truncated_distance_rejected(self):
        self.archive['rows'][0]['distances'].pop()
        with self.assertRaises(ValueError):run_audit.check_receipt(self.generated,self.archive)

    def test_duplicate_row_rejected(self):
        self.archive['rows'].append(copy.deepcopy(self.archive['rows'][0]))
        with self.assertRaises(ValueError):run_audit.check_receipt(self.generated,self.archive)

    def test_changed_distance_rejected(self):
        self.archive['rows'][0]['distances'][4]='999'
        with self.assertRaises(ValueError):run_audit.check_receipt(self.generated,self.archive)

    def test_forged_source_identity_rejected(self):
        self.archive['source_git_blob']='0'*40
        with self.assertRaises(ValueError):run_audit.check_receipt(self.generated,self.archive)

    def test_boolean_zero_alias_rejected(self):
        self.archive['new_E2']=False
        with self.assertRaises(ValueError):run_audit.check_receipt(self.generated,self.archive)

    def test_failed_rerun_removes_success(self):
        with tempfile.TemporaryDirectory() as tmp:
            out=Path(tmp)/'out';out.mkdir();r=out/'execution.json';r.write_text('{"status":"COMPLETE"}')
            p=subprocess.run([sys.executable,'-B',run_audit.__file__,str(Path(tmp)/'missing'),'--output',str(out)],capture_output=True,text=True)
            self.assertNotEqual(p.returncode,0)
            self.assertFalse(r.exists())

    def test_successful_audit_leaves_sources_unchanged(self):
        paths=[RECEIPT,'research/R248/R248_ALL_405_EXACT_MAP_IVP_TIME_SOURCES.csv',
          'research/R248/R248_FINAL_ACCEPTANCE_STATUS.json',
          'research/validation/r248_s44_finite_trajectory_exact_20261029.js',
          'research/evidence_audit/b_r248_s44_independent_formula_20261029.py',
          'research/operations/e078_r248_s44_source_receipt_third_route_20261029.js']
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)/'source'
            for path in paths:
                dest=root/path;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(ROOT/path,dest)
            before={str(p.relative_to(root)):p.read_bytes() for p in root.rglob('*') if p.is_file()}
            out=Path(tmp)/'out'
            p=subprocess.run([sys.executable,'-B',run_audit.__file__,str(root),'--output',str(out)],capture_output=True,text=True,timeout=60)
            self.assertEqual(p.returncode,0,p.stderr)
            self.assertTrue((out/'execution.json').exists())
            after={str(p.relative_to(root)):p.read_bytes() for p in root.rglob('*') if p.is_file()}
            self.assertEqual(before,after)


if __name__=='__main__':unittest.main()
