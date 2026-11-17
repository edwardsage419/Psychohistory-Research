"""Bounded archive gate tests, including preserved legacy RED and new GREEN.

Semantic-engine tests deliberately bypass public archive identity qualification to
prove that the original six bad-file guards themselves survive optimization.
The public CLI never offers that bypass.
"""
import copy
import csv
import hashlib
import io
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

import r275_archive_gate_v2 as gate

MODES = ("normal", "O", "env1")
CATEGORIES = ("duplicate", "missing", "probability", "MAP", "posterior", "evidence")
SEMANTIC_WORKER = """
import sys
sys.path.insert(0, sys.argv[1])
import r275_archive_gate_v2 as gate
try:
    check = gate._build_checker(gate._read_pinned(gate.SOURCE, 'source'))
    print(__import__('json').dumps(check(sys.argv[2], sys.argv[3])))
except gate.ArchiveGateError as error:
    print('BLOCKED ' + str(error), file=sys.stderr)
    raise SystemExit(1)
"""


class ArchiveGateTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temporary = tempfile.TemporaryDirectory(prefix="r275-archive-v2-tests-")
        cls.temp = Path(cls.temporary.name)
        cls.records = []
        cls.environment = {key: value for key, value in os.environ.items()
                           if not key.startswith("PYTHON")}
        cls.original = cls.temp / "legacy.py"
        cls.original.write_bytes(gate._read_pinned(gate.SOURCE, "source"))
        raw_json = gate._read_pinned(gate.RESULTS, "results_json")
        raw_csv = gate._read_pinned(gate.ROWS, "rows_csv")
        obj = json.loads(raw_json)
        original_rows = list(csv.DictReader(io.StringIO(raw_csv.decode())))
        cls.cases = {"good": (gate.RESULTS, gate.ROWS)}
        for name in CATEGORIES:
            data, rows = copy.deepcopy(obj), copy.deepcopy(original_rows)
            if name == "duplicate":
                rows.append(copy.deepcopy(rows[0]))
            elif name == "missing":
                rows.pop()
            elif name == "probability":
                rows[0]["true_source_probability"] = "1/255"
            elif name == "MAP":
                rows[0]["MAP_selected"] = "FLIP_PAIR"
            elif name == "posterior":
                rows[0]["posterior_IID"] = "1/18"
            elif name == "evidence":
                data["evidence"] = "E3"
            stream = io.StringIO(newline="")
            writer = csv.DictWriter(stream, fieldnames=list(original_rows[0]), lineterminator="\n")
            writer.writeheader()
            writer.writerows(rows)
            result_path, rows_path = cls.temp / (name + ".json"), cls.temp / (name + ".csv")
            result_path.write_bytes(raw_json if name != "evidence" else
                                    (json.dumps(data, indent=2) + "\n").encode())
            rows_path.write_bytes(raw_csv if name == "evidence" else stream.getvalue().encode())
            cls.cases[name] = (result_path, rows_path)

    @classmethod
    def tearDownClass(cls):
        log_path = os.environ.get("R275_ARCHIVE_V2_TEST_LOG")
        if log_path:
            Path(log_path).write_text(json.dumps(cls.records, indent=2) + "\n")
        cls.temporary.cleanup()

    def run_mode(self, label, arguments, mode):
        env = self.environment.copy()
        flags = ["-O"] if mode == "O" else []
        if mode == "env1":
            env["PYTHONOPTIMIZE"] = "1"
        argv = [sys.executable, "-B", *flags, *map(str, arguments)]
        process = subprocess.run(argv, env=env, cwd=self.temp, capture_output=True,
                                 text=True, timeout=30)
        self.records.append({"label": label, "mode": mode, "argv": argv,
                             "PYTHONOPTIMIZE": env.get("PYTHONOPTIMIZE"),
                             "exit_code": process.returncode, "stdout": process.stdout,
                             "stderr": process.stderr})
        return process

    def rejected(self, process, marker):
        self.assertEqual(process.returncode, 1, process.stdout + process.stderr)
        self.assertEqual(process.stdout, "")
        self.assertIn(marker, process.stderr)
        self.assertNotIn("SyntaxError", process.stderr)
        self.assertNotIn("ModuleNotFoundError", process.stderr)

    def test_good_archive_and_receipt_in_all_three_modes(self):
        for mode in MODES:
            with self.subTest(mode=mode):
                process = self.run_mode("new-good", [gate.__file__], mode)
                self.assertEqual(process.returncode, 0, process.stderr)
                self.assertEqual(process.stderr, "")
                receipt = json.loads(process.stdout)
                self.assertEqual(receipt["archive_receipt"], gate.EXPECTED)
                self.assertEqual(receipt["evidence"], "E1_ARTIFICIAL_NONBLIND")
                self.assertEqual(receipt["new_E2"], 0)
                self.assertEqual(receipt["new_E3"], 0)
                self.assertFalse(receipt["production_ready"])
                self.assertFalse(receipt["workflow_adopted"])
                self.assertEqual(receipt["scientific_acceptance"], "UNCHANGED")
                self.assertIn("STILL_BLOCKED", receipt["legacy_callable"])

    def test_public_cli_rejects_all_six_changed_archives_in_all_modes(self):
        for name in CATEGORIES:
            for mode in MODES:
                with self.subTest(case=name, mode=mode):
                    process = self.run_mode("new-identity-" + name,
                                            [gate.__file__, *self.cases[name]], mode)
                    self.rejected(process, "R275_ARCHIVE_V2:IDENTITY:")

    def test_original_semantic_guards_survive_all_modes(self):
        for name in CATEGORIES:
            for mode in MODES:
                with self.subTest(case=name, mode=mode):
                    process = self.run_mode("new-semantic-" + name,
                        ["-c", SEMANTIC_WORKER, Path(gate.__file__).parent, *self.cases[name]], mode)
                    self.rejected(process, "BLOCKED R275_ARCHIVE_V2:")
                    self.assertNotIn("IDENTITY", process.stderr)

    def test_legacy_red_e3_false_acceptance_is_preserved(self):
        for mode in MODES:
            with self.subTest(mode=mode):
                process = self.run_mode("legacy-RED-evidence",
                                        [self.original, *self.cases["evidence"]], mode)
                if mode == "normal":
                    self.rejected(process, "AssertionError")
                else:
                    self.assertEqual(process.returncode, 0, process.stderr)
                    self.assertEqual(json.loads(process.stdout)["status"], "PASS")

    def test_source_mutation_and_truncation_fail_before_execution(self):
        source = gate.SOURCE.read_bytes()
        for bad in (source.replace(b"F(1,16)", b"F(1,15)", 1),
                    source.replace(b"data['evidence']=='E1_ARTIFICIAL_NONBLIND'", b"True", 1),
                    source[:-1]):
            with self.subTest(digest=hashlib.sha256(bad).hexdigest()):
                with self.assertRaisesRegex(gate.ArchiveGateError, "IDENTITY:source"):
                    gate._build_checker(bad)

    def test_missing_input_fails_closed_without_receipt(self):
        process = self.run_mode("new-missing-file",
            [gate.__file__, self.temp / "absent.json", gate.ROWS], "normal")
        self.rejected(process, "BLOCKED FileNotFoundError")


if __name__ == "__main__":
    unittest.main(verbosity=2)
