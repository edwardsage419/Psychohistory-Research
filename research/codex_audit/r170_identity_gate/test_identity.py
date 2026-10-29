"""Authentic fixtures are read-only inputs; each negative uses a private copy."""
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
import identity_gate as gate

FIXTURE=Path(os.environ.get('R170_FIXTURE',str(Path(__file__).resolve().parents[3])))
B_RECEIPT=Path(os.environ.get('R170_B_RECEIPT',str(FIXTURE/'research/codex_audit/r170_full_state/logs/B_full_receipt.json')))
JS='research/validation/r170_observation_ladder_20261026.js'
PY='research/evidence_audit/r170_b_edge_utterance_20261026.py'
R='research/validation/R170_OBSERVATION_LADDER_EXACT_RECEIPT_2026-10-26.json'
S='research/evidence_audit/B_R170_INDEPENDENT_PYTHON_EXECUTION_SUMMARY_2026-10-26.json'

class IdentityTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup)
        self.root=Path(self.tmp.name)/'root';self.root.mkdir()
        for path in (JS,PY,R,S):
            target=self.root/path;target.parent.mkdir(parents=True,exist_ok=True)
            shutil.copyfile(FIXTURE/path,target)
        self.receipt=Path(self.tmp.name)/'B.json';shutil.copyfile(B_RECEIPT,self.receipt)
    def reject_source(self,path):
        with (self.root/path).open('ab') as f:f.write(b'\n')
        with self.assertRaisesRegex(ValueError,'source identity'):gate.verify(self.root,self.receipt)
    def test_authentic_bytes(self):
        r=gate.verify(self.root,self.receipt)
        self.assertEqual(r.get('status'),'COMPLETE');self.assertEqual(r.get('source_files_verified'),4)
        self.assertEqual(r.get('B_receipt_bytes'),23004)
        self.assertEqual(r.get('full_frozen_extension_acceptance'),'PARTIAL')
    def test_changed_js(self):self.reject_source(JS)
    def test_changed_python(self):self.reject_source(PY)
    def test_changed_r_receipt(self):self.reject_source(R)
    def test_changed_historical_summary(self):self.reject_source(S)
    def test_same_length_wrong_receipt(self):
        raw=self.receipt.read_bytes();self.receipt.write_bytes(raw.replace(b'72',b'73',1))
        self.assertEqual(len(raw),self.receipt.stat().st_size)
        with self.assertRaisesRegex(ValueError,'receipt digest'):gate.verify(self.root,self.receipt)
    def test_semantic_equal_receipt_different_bytes(self):
        self.receipt.write_text(json.dumps(json.loads(self.receipt.read_text()),separators=(',',':')))
        with self.assertRaisesRegex(ValueError,'receipt (length|digest)'):gate.verify(self.root,self.receipt)
    def test_missing_receipt(self):
        self.receipt.unlink()
        with self.assertRaises((ValueError,FileNotFoundError)):gate.verify(self.root,self.receipt)
    def test_cli_invalidates_stale_success(self):
        output=Path(self.tmp.name)/'result.json'
        cmd=[sys.executable,'-B',str(Path(gate.__file__)),str(self.root),str(self.receipt),'--output',str(output)]
        self.assertEqual(subprocess.run(cmd,capture_output=True).returncode,0)
        self.assertEqual(json.loads(output.read_text())['status'],'COMPLETE')
        self.receipt.write_bytes(b'corrupt')
        p=subprocess.run(cmd,capture_output=True,text=True)
        self.assertNotEqual(p.returncode,0);self.assertFalse(output.exists())
        self.assertEqual(json.loads(p.stdout)['status'],'PARTIAL')
    def test_cli_refuses_output_over_input(self):
        raw=self.receipt.read_bytes()
        p=subprocess.run([sys.executable,'-B',str(Path(gate.__file__)),str(self.root),str(self.receipt),'--output',str(self.receipt)],capture_output=True)
        self.assertNotEqual(p.returncode,0);self.assertEqual(self.receipt.read_bytes(),raw)
    def test_cli_invalidates_stale_success_under_root(self):
        output=self.root/'result.json';output.write_text('{"status":"COMPLETE"}')
        self.receipt.write_bytes(b'corrupt')
        p=subprocess.run([sys.executable,'-B',str(Path(gate.__file__)),str(self.root),str(self.receipt),'--output',str(output)],capture_output=True)
        self.assertNotEqual(p.returncode,0);self.assertFalse(output.exists())

if __name__=='__main__':unittest.main()
