#!/usr/bin/env python3
"""Local synthetic contract tests; no original model or receipt is imported."""
import importlib.util
import json
import shutil
from pathlib import Path
import tempfile
import unittest
from unittest import mock

SRC = Path(__file__).with_name("r333_r340_composite_acceptance_20261101.py")
spec = importlib.util.spec_from_file_location("composite", SRC)
gate = importlib.util.module_from_spec(spec)
spec.loader.exec_module(gate)


def math_receipt():
    return {"status": "PASS_ALL_EIGHT_BOUNDED_E1_RECEIPTS", "evidence": "E1_ARTIFICIAL_ONLY",
            "subprocess_checks": 16,
            "models": [{"model": x, "gate_blob": "a"*40, "result": "PASS_BOUNDED_E1_RECEIPT"}
                       for x in gate.MODELS]}


def claim_receipt():
    return {"status": "PASS_HISTORICAL_CLAIMS_E1_IDENTITY_ONLY", "files_checked": 16,
            "mathematical_gate": "NOT_RUN", "production_adoption": "NOT_ESTABLISHED",
            "models": [{"model": x, "machine_blob": "a"*40, "final_blob": "b"*40,
                        "CI_run": 40000000000} for x in gate.MODELS]}


class Contract(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.audit = self.root / gate.AUDIT
        self.audit.mkdir(parents=True)
        self.pins = {}
        for name in gate.PINS:
            raw = ("mock " + name).encode()
            (self.audit / name).write_bytes(raw)
            self.pins[name] = gate.git_blob(raw)

    def run_case(self, outputs):
        with mock.patch.object(gate, "run_json", side_effect=outputs) as run:
            result = gate.verify(self.root, pins=self.pins)
            self.assertEqual(run.call_count, 3)
            self.assertEqual(result["status"], "PASS_COMPOSITE_CANDIDATE_E1_ONLY")
            return run.call_args_list

    def test_positive_and_optimized_invocation(self):
        calls = self.run_case([claim_receipt(), math_receipt(), math_receipt()])
        self.assertIn("-O", calls[2].args[0])
        self.assertNotIn("-O", calls[1].args[0])

    def test_missing_claim_blocks_math(self):
        with mock.patch.object(gate, "run_json", side_effect=[ValueError("claim rejected")]) as run:
            with self.assertRaisesRegex(ValueError, "claim rejected"):
                gate.verify(self.root, pins=self.pins)
            self.assertEqual(run.call_count, 1)

    def test_optimized_math_failure(self):
        with mock.patch.object(gate, "run_json", side_effect=[claim_receipt(), math_receipt(), ValueError("optimized rejected")]):
            with self.assertRaisesRegex(ValueError, "optimized rejected"):
                gate.verify(self.root, pins=self.pins)

    def test_model_shrink(self):
        c = claim_receipt()
        c["models"].pop()
        with mock.patch.object(gate, "run_json", return_value=c):
            with self.assertRaisesRegex(ValueError, "claim universe"):
                gate.verify(self.root, pins=self.pins)

    def test_math_grade_upgrade(self):
        m = math_receipt()
        m["evidence"] = "E2_HUMAN"
        with mock.patch.object(gate, "run_json", side_effect=[claim_receipt(), m]):
            with self.assertRaisesRegex(ValueError, "math evidence"):
                gate.verify(self.root, pins=self.pins)

    def test_math_optimized_mismatch(self):
        m = math_receipt()
        m2 = math_receipt()
        m2["models"][0]["gate_blob"] = "b"*40
        with mock.patch.object(gate, "run_json", side_effect=[claim_receipt(), m, m2]):
            with self.assertRaisesRegex(ValueError, "disagree"):
                gate.verify(self.root, pins=self.pins)

    def test_gate_source_corruption(self):
        name = next(iter(self.pins))
        (self.audit / name).write_bytes(b"changed")
        with mock.patch.object(gate, "run_json") as run:
            with self.assertRaisesRegex(ValueError, "gate source mismatch"):
                gate.verify(self.root, pins=self.pins)
            run.assert_not_called()

    def test_gate_symlink(self):
        name = next(iter(self.pins))
        p = self.audit / name
        p.rename(self.audit / "old")
        p.symlink_to("old")
        with self.assertRaisesRegex(ValueError, "symlink"):
            gate.verify(self.root, pins=self.pins)

    def test_duplicate_child_json(self):
        with mock.patch.object(gate.subprocess, "run", return_value=mock.Mock(
            returncode=0, stderr="", stdout='{"status":"PASS","status":"PASS"}')):
            with self.assertRaisesRegex(ValueError, "duplicate JSON key"):
                gate.run_json(["fake"], timeout=1)

    def test_child_stderr(self):
        with mock.patch.object(gate.subprocess, "run", return_value=mock.Mock(
            returncode=0, stderr="warning", stdout=json.dumps(claim_receipt()))):
            with self.assertRaisesRegex(ValueError, "stderr"):
                gate.run_json(["fake"], timeout=1)

    def test_missing_model_math(self):
        m = math_receipt()
        m["models"].pop()
        with mock.patch.object(gate, "run_json", side_effect=[claim_receipt(), m]):
            with self.assertRaisesRegex(ValueError, "math universe"):
                gate.verify(self.root, pins=self.pins)

    @unittest.skipUnless(shutil.which("node"), "Node.js unavailable")
    def test_native_synthetic_three_processes(self):
        math_name = "r333_r340_acceptance_entry_20261101.py"
        claim_name = "r333_r340_claim_receipt_gate_20261101.js"
        math_source = "print(" + repr(json.dumps(math_receipt())) + ")\n"
        claim_source = "console.log(" + json.dumps(json.dumps(claim_receipt())) + ");\n"
        (self.audit / math_name).write_text(math_source)
        (self.audit / claim_name).write_text(claim_source)
        for name in self.pins:
            self.pins[name] = gate.git_blob((self.audit / name).read_bytes())
        result = gate.verify(self.root, pins=self.pins)
        self.assertEqual(result["math_entry_runs"], 2)

    @unittest.skipUnless(shutil.which("node"), "Node.js unavailable")
    def test_native_optimized_only_rejection(self):
        math_name = "r333_r340_acceptance_entry_20261101.py"
        claim_name = "r333_r340_claim_receipt_gate_20261101.js"
        math_source = ("import sys\n"
                       "if sys.flags.optimize: raise SystemExit(3)\n"
                       "print(" + repr(json.dumps(math_receipt())) + ")\n")
        claim_source = "console.log(" + json.dumps(json.dumps(claim_receipt())) + ");\n"
        (self.audit / math_name).write_text(math_source)
        (self.audit / claim_name).write_text(claim_source)
        for name in self.pins:
            self.pins[name] = gate.git_blob((self.audit / name).read_bytes())
        with self.assertRaisesRegex(ValueError, "child exit 3"):
            gate.verify(self.root, pins=self.pins)

    def test_claim_grade_overreach(self):
        c = claim_receipt()
        c["status"] = "PASS_HUMAN_E2"
        with mock.patch.object(gate, "run_json", return_value=c):
            with self.assertRaisesRegex(ValueError, "claim status"):
                gate.verify(self.root, pins=self.pins)


if __name__ == "__main__":
    unittest.main(verbosity=2)
