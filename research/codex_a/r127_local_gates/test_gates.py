import copy
import hashlib
import json
from pathlib import Path
import subprocess
import tempfile
import unittest
import sys

import gate

ROOT = Path(__file__).resolve().parents[3]
RECEIPT = 'research/R127/R127_PHASE_A_1990_ORIGINAL_MIN_EFFORT_60_TEST_75117_DEVIATIONS_1296_2X2_CI_ACCEPTANCE.json'
LINKS = {
    'original': 'published_source_A_treatment_seven_experiments_p1_p10_only',
    'equilibria': 'source_A_seven_strict_common_effort_Nash_security_and_payoff_rank',
    'payoff_table': 'original_source_A_payoff_table_rows',
    'audit': 'n2to4_original_source_payoff_complete_synthetic_profiles_and_deviations',
    'toy': 'two_player_symmetric_coordination_project_created_conflict_and_risk_tie',
    'grid': 'synthetic_all_six_level_symmetric_2x2_payoffs',
}


class GatesTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.receipt = json.loads((ROOT/RECEIPT).read_bytes())
        cls.observed = {key: cls.receipt[name] for key, name in LINKS.items()}

    def test_plain_60_success(self):
        self.assertEqual(gate.parse_test_log(b'Ran 60 tests in 0.123s\n\nOK\n', 0)['tests'], 60)

    def test_failure_markers_cannot_hide_behind_ok(self):
        for marker in ('FAILED (failures=1)', '  ERROR: traceback', 'FAIL: case'):
            with self.subTest(marker=marker), self.assertRaises(ValueError):
                gate.parse_test_log(('Ran 60 tests in 0.1s\n'+marker+'\nOK\n').encode(), 0)

    def test_wrong_zero_duplicate_and_nested_counts_rejected(self):
        logs = [b'Ran 59 tests in 0.1s\n\nOK\n', b'Ran 0 tests in 0.1s\n\nOK\n',
                b'Ran 60 tests in 0.1s\nRan 60 tests in 0.1s\n\nOK\n',
                b'Ran 1 test in 0.1s\n\nOK\nRan 60 tests in 0.1s\n\nOK\n']
        for log in logs:
            with self.subTest(log=log), self.assertRaises(ValueError):gate.parse_test_log(log, 0)

    def test_skip_expected_failure_and_duplicate_ok_rejected(self):
        for ending in ('OK (skipped=1)', 'OK (expected failures=1)', 'OK\nOK', 'OK\nextra'):
            with self.subTest(ending=ending), self.assertRaises(ValueError):
                gate.parse_test_log(('Ran 60 tests in 0.1s\n\n'+ending+'\n').encode(), 0)

    def test_child_failure_and_boolean_exit_rejected(self):
        for code in (1, -9, False):
            with self.subTest(code=code), self.assertRaises(ValueError):
                gate.parse_test_log(b'Ran 60 tests in 0.1s\n\nOK\n', code)

    def test_complete_stage2_matches_archive(self):
        result = gate.validate_stage2(copy.deepcopy(self.observed), self.receipt)
        self.assertGreater(result['checked_leaf_fields'], 100)
        self.assertIs(type(result['new_real_person_level_E2_prediction_scores']), int)
        self.assertEqual(result['new_real_person_level_E2_prediction_scores'], 0)

    def test_upstream_e2_seven_is_rejected(self):
        changed = copy.deepcopy(self.observed)
        changed['original']['new_real_human_E2_prediction_scores'] = 7
        with self.assertRaisesRegex(ValueError, 'new_real_human_E2_prediction_scores'):
            gate.validate_stage2(changed, self.receipt)

    def test_boolean_and_float_counts_are_not_integers(self):
        for value in (False, 0.0):
            with self.subTest(value=value):
                changed = copy.deepcopy(self.observed)
                changed['original']['new_real_human_E2_prediction_scores'] = value
                with self.assertRaises(ValueError):gate.validate_stage2(changed, self.receipt)

    def test_enumeration_total_mutation(self):
        for field in ('all_original_payoff_profiles', 'all_exact_individual_candidate_deviations'):
            changed = copy.deepcopy(self.observed); changed['audit'][field] += 1
            with self.subTest(field=field), self.assertRaises(ValueError):
                gate.validate_stage2(changed, self.receipt)

    def test_missing_and_success_shaped_extra_fields(self):
        for missing in (False, True):
            changed = copy.deepcopy(self.observed)
            if missing:del changed['toy']['equal_risk_selection']
            else:changed['status'] = 'PASS'
            with self.subTest(missing=missing), self.assertRaises(ValueError):
                gate.validate_stage2(changed, self.receipt)

    def test_each_stage2_leaf_is_compared(self):
        def leaves(value, path=()):
            if type(value) is dict:
                for key, item in value.items():yield from leaves(item, path+(key,))
            elif type(value) is list:
                for key, item in enumerate(value):yield from leaves(item, path+(key,))
            else:yield path
        for path in leaves(self.observed):
            changed = copy.deepcopy(self.observed); target = changed
            for key in path[:-1]:target = target[key]
            target[path[-1]] = {'forged': 'PASS'}
            with self.subTest(path=path), self.assertRaises(ValueError):gate.validate_stage2(changed, self.receipt)

    def test_duplicate_json_and_nonfinite_rejected(self):
        for raw in (b'{"a":0,"a":0}', b'{"x":{"a":0,"a":0}}', b'{"x":NaN}', b'{"x":Infinity}'):
            with self.subTest(raw=raw), self.assertRaises(ValueError):gate.load_json(raw)


class SourceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp = tempfile.TemporaryDirectory(prefix='r127-source-fixture-')
        cls.addClassCleanup(cls.temp.cleanup)
        cls.root = Path(cls.temp.name)
        cls.pins = json.loads((Path(__file__).parent/'pins.json').read_bytes())
        for name in cls.pins:
            path = cls.root/name; path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes((ROOT/name).read_bytes())
        for args in (['init', '-q'], ['add', '.'], ['-c', 'user.name=Fixture', '-c', 'user.email=fixture@example.invalid', 'commit', '-qm', 'fixture']):
            subprocess.run(['git', *args], cwd=cls.root, check=True, capture_output=True)

    def test_pinned_source_capture(self):
        raw, identities, head = gate.capture(self.root)
        self.assertEqual(set(raw), set(self.pins))
        self.assertEqual(len(head), 40)
        self.assertTrue(all(identities[name] == self.pins[name] for name in raw))

    def test_changed_workflow_bytes_rejected_without_execution(self):
        name = '.github/workflows/r127-van-huyck-1990-coordination-source-table-60-tests.yml'
        path = self.root/name; original = path.read_bytes()
        try:
            path.write_bytes(original+b'\n# temporary negative control\n')
            with self.assertRaisesRegex(ValueError, 'IDENTITY'):gate.capture(self.root)
        finally:path.write_bytes(original)

    def test_untracked_checkout_identity_rejected(self):
        name = next(iter(self.pins))
        subprocess.run(['git', 'update-index', '--force-remove', name], cwd=self.root, check=True, capture_output=True)
        subprocess.run(['git', '-c', 'user.name=Fixture', '-c', 'user.email=fixture@example.invalid', 'commit', '-qm', 'remove tracked path'], cwd=self.root, check=True, capture_output=True)
        try:
            with self.assertRaises(ValueError):gate.capture(self.root)
        finally:
            # Restore only this disposable fixture's original index/commit.
            subprocess.run(['git', 'add', name], cwd=self.root, check=True, capture_output=True)
            subprocess.run(['git', '-c', 'user.name=Fixture', '-c', 'user.email=fixture@example.invalid', 'commit', '-qm', 'restore tracked path'], cwd=self.root, check=True, capture_output=True)

    def test_gate_changed_during_real_replay_blocks_success(self):
        with tempfile.TemporaryDirectory(prefix='r127-gate-copy-') as directory:
            folder = Path(directory)
            for name in ('gate.py', 'pins.json'):
                (folder/name).write_bytes((Path(__file__).parent/name).read_bytes())
            code = '''import importlib.util,json,sys
from pathlib import Path
spec=importlib.util.spec_from_file_location("copied_gate",sys.argv[1])
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
original=m.run_child
changed=False
def change_after_real_child(command,cwd):
 global changed
 result=original(command,cwd)
 if not changed:
  path=Path(m.__file__);path.write_bytes(path.read_bytes()+b"\\n# disposable concurrent gate edit\\n")
  changed=True
 return result
m.run_child=change_after_real_child
try:result=m.verify(sys.argv[2])
except ValueError as exc:
 print(json.dumps({"status":"BLOCKED","reason":str(exc)}));sys.exit(1)
print(json.dumps(result))
'''
            command = [sys.executable, '-I', '-B']+(['-O'] if sys.flags.optimize else [])+[
                '-c', code, str(folder/'gate.py'), str(self.root)]
            child = subprocess.run(command, capture_output=True, timeout=120)
            self.assertEqual(child.returncode, 1, child.stderr.decode())
            result = json.loads(child.stdout)
            self.assertEqual(result['status'], 'BLOCKED')
            self.assertEqual(result['reason'], 'GATE_SOURCE_CHANGED_DURING_REPLAY')


if __name__ == '__main__':unittest.main()
