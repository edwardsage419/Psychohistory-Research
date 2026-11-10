import copy
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

import preflight

ROOT = Path(__file__).resolve().parents[3]
COMMIT = '9de51508daa160d33d0d05b13ba1454f8333f21d'
DIAGNOSTIC = 'research/codex_b/2026-11-10-r077-exact-paired-ties/evidence/py312/permutation-diagnostics.stdout'


class PreflightTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = json.loads(subprocess.check_output(['git', '-C', str(ROOT), 'show', COMMIT+':'+DIAGNOSTIC]))

    def test_completed_diagnostic_still_vetoes_production(self):
        result = preflight.classify(copy.deepcopy(self.data))
        self.assertEqual(result['status'], 'BLOCKED_ORIGINAL_R077_UNREPAIRED')
        self.assertIs(result['production_ready'], False)
        self.assertEqual(result['exit_code'], 2)
        self.assertEqual(result['engineering_preflight'], 'COMPLETE')
        self.assertEqual(result['original_failure_cases'], 11)

    def test_missing_or_success_shaped_extra_field_rejected(self):
        for missing in (False, True):
            doc = copy.deepcopy(self.data)
            if missing:del doc['guard_rejections']
            else:doc['status'] = 'PASS'
            with self.subTest(missing=missing), self.assertRaises(ValueError):preflight.classify(doc)

    def test_boolean_and_float_counts_rejected(self):
        for value in (True, 11.0):
            doc = copy.deepcopy(self.data);doc['guard_rejections'] = value
            with self.subTest(value=value), self.assertRaises(ValueError):preflight.classify(doc)

    def test_duplicate_case_identity_rejected(self):
        doc = copy.deepcopy(self.data);doc['permutations'][-1] = doc['permutations'][0]
        with self.assertRaises(ValueError):preflight.classify(doc)

    def test_wrong_case_universe_rejected(self):
        doc = copy.deepcopy(self.data);doc['permutations'][0]['positive_positions'] = [0, 1, 7]
        with self.assertRaises(ValueError):preflight.classify(doc)

    def test_flags_and_vote_histogram_must_match(self):
        for field in ('flag', 'histogram'):
            doc = copy.deepcopy(self.data)
            if field == 'flag':doc['permutations'][0]['original_rejected_by_exact_votes'] = not doc['permutations'][0]['original_rejected_by_exact_votes']
            else:doc['original_vote_histogram'] = {'(0, 2, 0)': 35}
            with self.subTest(field=field), self.assertRaises(ValueError):preflight.classify(doc)

    def test_human_source_upgrade_rejected(self):
        doc = copy.deepcopy(self.data);doc['data_class'] = 'QUALIFIED_HUMAN'
        with self.assertRaises(ValueError):preflight.classify(doc)

    def test_wrong_exact_case_count_rejected(self):
        doc = copy.deepcopy(self.data);doc['exact_ties'] = 34
        with self.assertRaises(ValueError):preflight.classify(doc)

    def test_boolean_votes_and_flags_rejected(self):
        for field in ('vote', 'flag'):
            doc = copy.deepcopy(self.data)
            if field == 'vote':doc['permutations'][0]['original']['sessions_better'] = False
            else:doc['permutations'][0]['original_rejected_by_exact_votes'] = 0
            with self.subTest(field=field), self.assertRaises(ValueError):preflight.classify(doc)

    def test_duplicate_json_and_nonfinite_rejected(self):
        for raw in (b'{"x":0,"x":0}', b'{"x":{"a":0,"a":0}}', b'{"x":NaN}'):
            with self.subTest(raw=raw), self.assertRaises(ValueError):preflight.load_json(raw)


class SourceBoundaryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp = tempfile.TemporaryDirectory(prefix='r077-boundary-fixture-')
        cls.addClassCleanup(cls.temp.cleanup)
        cls.repo = Path(cls.temp.name)/'repo'
        subprocess.run(['git', 'clone', '--shared', '--no-checkout', str(ROOT), str(cls.repo)],
                       check=True, capture_output=True)
        # Populate only the fixed 40 source copies; original checkout stays read-only.
        cls.head, cls.pins, _ = preflight.capture(ROOT, cls.repo)

    def cli(self):
        command = [sys.executable, '-I', '-B']+(['-O'] if sys.flags.optimize else [])+[
            str(Path(preflight.__file__).resolve()), str(self.repo), '--artificial-preflight']
        child = subprocess.run(command, capture_output=True, timeout=60)
        self.assertEqual(child.returncode, 1, child.stderr.decode())
        self.assertFalse(child.stderr)
        result = json.loads(child.stdout)
        self.assertEqual(result['status'], 'BLOCKED_INVALID_PREFLIGHT')
        self.assertNotIn('production_ready', result)
        return result

    def test_changed_source_copy_blocks_before_diagnostic(self):
        path = self.repo/'research/R077/r077_fourth_real_human_source_only_e3.py'
        original = path.read_bytes()
        try:
            path.write_bytes(original+b'\n# disposable identity negative control\n')
            self.assertIn('WORKTREE_IDENTITY:', self.cli()['reason'])
        finally:path.write_bytes(original)

    def test_checkout_tree_mismatch_blocks_even_with_correct_live_bytes(self):
        subprocess.run(['git', 'read-tree', '--empty'], cwd=self.repo, check=True, capture_output=True)
        subprocess.run(['git', '-c', 'user.name=Fixture', '-c', 'user.email=fixture@example.invalid',
                        'commit', '-qm', 'empty fixture tree'], cwd=self.repo, check=True, capture_output=True)
        try:self.assertEqual(self.cli()['reason'], 'GIT_SOURCE_UNAVAILABLE')
        finally:
            subprocess.run(['git', 'update-ref', 'HEAD', self.head], cwd=self.repo, check=True, capture_output=True)


if __name__ == '__main__':unittest.main()
