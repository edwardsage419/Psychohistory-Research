import copy
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

import run_audit

ROOT = Path(__file__).resolve().parents[3]
FIXTURE = 'research/validation/R258_S54_COARSE_OBSERVATION_EXACT_RECEIPT_2026-10-29.json'


class Tests(unittest.TestCase):
    def setUp(self):
        self.receipt = json.loads((ROOT/FIXTURE).read_text())

    def test_real_archive_matches_itself(self):
        run_audit.check_archive(copy.deepcopy(self.receipt), self.receipt)

    def test_changed_minimizer_count_rejected(self):
        other = copy.deepcopy(self.receipt)
        other['results'][0]['minimizer_count_A'] = 1
        self.assertNotEqual(other, self.receipt)
        with self.assertRaises(ValueError): run_audit.check_archive(other, self.receipt)

    def test_evidence_upgrade_rejected(self):
        other = copy.deepcopy(self.receipt)
        other['evidence'] = 'E3'
        with self.assertRaises(ValueError): run_audit.check_archive(other, self.receipt)

    def test_boolean_zero_not_interchangeable(self):
        other = copy.deepcopy(self.receipt)
        other['new_human_E2'] = False
        with self.assertRaises(ValueError): run_audit.check_archive(other, self.receipt)

    def test_duplicate_world_rejected(self):
        other = copy.deepcopy(self.receipt)
        other['results'][1] = copy.deepcopy(other['results'][0])
        with self.assertRaises(ValueError): run_audit.check_archive(other, self.receipt)

    def test_failed_rerun_removes_old_success(self):
        with tempfile.TemporaryDirectory() as tmp:
            out=Path(tmp)/'out';out.mkdir()
            receipt=out/'execution.json';receipt.write_text('{"status":"COMPLETE"}')
            p=subprocess.run([sys.executable,'-B',run_audit.__file__,str(Path(tmp)/'missing'),
                              '--output',str(out)],capture_output=True,text=True)
            self.assertNotEqual(p.returncode,0)
            self.assertFalse(receipt.exists())

    def test_successful_replay_leaves_sources_unchanged(self):
        paths = [
            'research/R258/r258_exact_finite_stochastic_control.py',
            'research/R258/R258_ALL_1728_ORIGINAL_THREESTEP_CONTROL_SOURCE_ATOMS.csv',
            'research/R258/R258_EXACT_RESULTS.json',
            'research/R258/R258_FINAL_MACHINE_ACCEPTANCE.json',
            'research/R258/R258_FINAL_ACCEPTANCE_STATUS.json',
            FIXTURE,
            'research/validation/r258_s54_coarse_state_observation_20261029.py',
            'research/evidence_audit/b_r258_s54_distribution_oracle_20261029.py',
            'research/evidence_audit/b_r258_s54_crossroute_gate_20261029.py',
        ]
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)/'source'
            for path in paths:
                target=root/path;target.parent.mkdir(parents=True,exist_ok=True)
                shutil.copyfile(ROOT/path,target)
            before={str(p.relative_to(root)):p.read_bytes() for p in root.rglob('*') if p.is_file()}
            out=Path(tmp)/'out'
            p=subprocess.run([sys.executable,'-B',run_audit.__file__,str(root),'--output',str(out)],
                             capture_output=True,text=True,timeout=120)
            self.assertEqual(p.returncode,0,p.stderr)
            self.assertTrue((out/'execution.json').exists())
            after={str(p.relative_to(root)):p.read_bytes() for p in root.rglob('*') if p.is_file()}
            self.assertEqual(before,after)


if __name__=='__main__':unittest.main()
