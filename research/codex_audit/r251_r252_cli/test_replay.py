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
J251='research/validation/R251_S47_FINITE_WINDOW_EXACT_RECEIPT_2026-10-29.json'
J252='research/validation/R252_S48_FINITE_SAMPLE_INFORMATION_RECEIPT_2026-10-29.json'
KEYS=('research_id','source_rows','independent_cohorts','source_field_checks','failed_checks','worlds')


class Tests(unittest.TestCase):
    def setUp(self):
        self.a=json.loads((ROOT/J251).read_text())
        self.b=json.loads((ROOT/J252).read_text())
        self.projection={k:self.a[k] for k in KEYS}

    def test_projection_returns_explicit_ignored_fields(self):
        omitted=run_audit.check_251(self.projection,self.a)
        self.assertEqual(set(omitted),set(self.a)-set(KEYS))

    def test_projection_cannot_drop_computation_fields(self):
        self.projection.pop('worlds')
        with self.assertRaises(ValueError):run_audit.check_251(self.projection,self.a)

    def test_changed_cohort_rejected(self):
        self.projection['worlds']=copy.deepcopy(self.projection['worlds'])
        self.projection['worlds'][0]['strict4_cohorts']+=1
        with self.assertRaises(ValueError):run_audit.check_251(self.projection,self.a)

    def test_full_metrics_change_rejected(self):
        changed=copy.deepcopy(self.b);changed['records'][0]['metrics']['I_XY']['approx_bits']=999
        with self.assertRaises(ValueError):run_audit.equal_json(changed,self.b)

    def test_full_boolean_zero_type_change_rejected(self):
        changed=copy.deepcopy(self.b);changed['new_human_E2']=False
        with self.assertRaises(ValueError):run_audit.equal_json(changed,self.b)

    def test_failed_rerun_clears_old_success(self):
        with tempfile.TemporaryDirectory() as tmp:
            out=Path(tmp)/'out';out.mkdir();receipt=out/'execution.json'
            receipt.write_text('{"status":"COMPLETE"}')
            p=subprocess.run([sys.executable,'-B',run_audit.__file__,str(Path(tmp)/'missing'),'--output',str(out)],capture_output=True,text=True)
            self.assertNotEqual(p.returncode,0)
            self.assertFalse(receipt.exists())

    def test_full_replay_does_not_write_source(self):
        paths=[J251,J252,
          'research/R251/R251_ALL_405_ORIGINAL_LYAPUNOV_SOURCE_ATOMS.csv',
          'research/R252/R252_ALL_576_ORIGINAL_SIXBIT_INFORMATION_SOURCES.csv',
          'research/R251/R251_FINAL_ACCEPTANCE_STATUS.json','research/R252/R252_FINAL_ACCEPTANCE_STATUS.json',
          'research/validation/r251_s47_finite_window_exact_20261029.js',
          'research/validation/r252_s48_exact_source_information_20261029.js',
          'research/evidence_audit/b_r251_s47_independent_fraction_20261029.py',
          'research/evidence_audit/b_r252_s48_independent_numeric_oracle_20261029.py',
          'research/operations/e081_r251_s47_exact_receipt_20261029.js',
          'research/operations/e082_r252_s48_source_numeric_20261029.js']
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
