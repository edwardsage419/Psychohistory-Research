"""Independent real-CLI regressions for fixed S78/S85 proposed gates.

Run from any checkout containing the fixed Git objects; no candidate checkout
or third-party Python package is needed. Never fetches or writes research files.
"""
import argparse
import csv
import hashlib
import io
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

REPO = Path(__file__).resolve().parents[3]
BASE = '25bcd51dd58bf0c245ae84c563406e679a966b5a'
HEADS = {22: 'c4aa392a39e6cddad9857febfed29f3b00e41dd9',
         23: '30050722a94ad68640b9a12cbeeb2a0a7e3e014c'}
MODULES = {22: 'research/codex_b/2026-11-10-r282-paired-certificate',
           23: 'research/codex_b/2026-11-10-r289-holdout-contract'}
ARTIFACTS = {22: ('research/validation/R282_S78_ALL_192_SOURCE_OBSERVATIONS.csv',
                  'research/validation/R282_S78_EXACT_RESULTS.json'),
             23: ('research/validation/R289_S85_ALL_243_PAIRED_OFFERS.csv',
                  'research/validation/R289_S85_EXACT_RESULTS.json')}
B_PATH = 'research/evidence_audit/b_r282_s78_strict_remote_receipt_gate_20261030.js'
RECORDS = []


def export(repo, root):
    """Export only executable dependencies/artifacts from immutable Git objects."""
    identities = []
    entries = [(BASE, B_PATH)]
    for number in HEADS:
        names = ('audit.py', 'algebra.py') if number == 22 else ('audit.py', 'stopping.py')
        entries += [(HEADS[number], MODULES[number]+'/'+name) for name in names]
        entries += [(BASE, name) for name in ARTIFACTS[number]]
    for commit, name in entries:
        raw = subprocess.check_output(['git', '-C', str(repo), 'show', commit+':'+name])
        path = root/name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(raw)
        identities.append(dict(commit=commit, path=name, sha256=hashlib.sha256(raw).hexdigest(),
                               git_blob=hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()))
    return identities


class CLIContracts(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temporary = tempfile.TemporaryDirectory(prefix='codex-a-cli-review-')
        cls.addClassCleanup(cls.temporary.cleanup)
        cls.root = Path(cls.temporary.name)
        cls.identities = export(REPO, cls.root)

    def call(self, number, data=None, document=None, raw=None, reason=None):
        with tempfile.TemporaryDirectory(prefix='case-', dir=self.root) as directory:
            folder = Path(directory)
            a, j = folder/'sources.csv', folder/'result.json'
            a.write_bytes(data if data is not None else (self.root/ARTIFACTS[number][0]).read_bytes())
            if raw is None:
                raw = (json.dumps(document).encode() if document is not None
                       else (self.root/ARTIFACTS[number][1]).read_bytes())
            j.write_bytes(raw)
            command = [sys.executable, '-B']+(['-O'] if sys.flags.optimize else [])+[
                str(self.root/MODULES[number]/'audit.py'), str(a), str(j)]
            child = subprocess.run(command, cwd=self.root, capture_output=True, timeout=30)
            RECORDS.append(dict(test=self.id(), pr=number, command=command, exit=child.returncode,
                                csv_sha256=hashlib.sha256(a.read_bytes()).hexdigest(),
                                json_sha256=hashlib.sha256(raw).hexdigest(),
                                stdout=child.stdout.decode(), stderr=child.stderr.decode()))
            self.assertEqual(child.stderr, b'', 'CLI must report a structured outcome, not a traceback')
            result = json.loads(child.stdout)
            self.assertIs(type(result), dict)
            if reason is None:
                self.assertEqual(child.returncode, 0)
                expected = {22: 'PASS_PAIRED_GF2_SUPPLEMENT',
                            23: 'PASS_INDEPENDENT_STOPPING_HOLDOUT_CONTRACT'}[number]
                self.assertEqual(result['status'], expected)
            else:
                self.assertEqual(child.returncode, 2)
                self.assertEqual(result['status'], 'REJECTED')
                self.assertIn(reason, result['reason'])
            return result

    def document(self, number):
        return json.loads((self.root/ARTIFACTS[number][1]).read_bytes())

    def table(self, number):
        return list(csv.reader(io.StringIO((self.root/ARTIFACTS[number][0]).read_text())))

    @staticmethod
    def encoded(rows):
        stream = io.StringIO(newline='')
        csv.writer(stream, lineterminator='\n').writerows(rows)
        return stream.getvalue().encode()

    def test_archived_cli_summaries(self):
        a, b = self.call(22), self.call(23)
        self.assertEqual((a['source_rows'], a['paired_integer_fields']), (192, 4))
        self.assertEqual(a['paired_counts_from_GF2'], a['paired_counts_from_CSV'])
        self.assertEqual((b['source_rows'], b['result_leaf_checks']), (243, 136))

    def test_csv_reordering_preserves_identity(self):
        for number in HEADS:
            with self.subTest(pr=number):
                rows = self.table(number)
                self.call(number, data=self.encoded([rows[0], *reversed(rows[1:])]))
        rows = self.table(22)
        schedules = ('SYNC', 'A_THEN_B', 'B_THEN_A')
        for rotated in schedules:
            with self.subTest(independently_rotated_schedule=rotated):
                changed = [rows[0]]
                for schedule in schedules:
                    group = [row for row in rows[1:] if row[0] == schedule]
                    changed.extend(group[1:]+group[:1] if schedule == rotated else group)
                self.call(22, data=self.encoded(changed))

    def test_s85_identity_collections_can_be_reordered(self):
        fields = ('worlds', 'independent_polynomial', 'mutation_tests')
        for field in fields:
            with self.subTest(independently_reversed_collection=field):
                doc = self.document(23)
                doc[field].reverse()
                self.call(23, document=doc)
        doc = self.document(23)
        for field in fields:
            doc[field].reverse()
        self.call(23, document=doc)

    def test_s85_duplicate_identities_rejected(self):
        for field, reason in (('worlds', 'DUPLICATE_WORLD'),
                              ('independent_polynomial', 'DUPLICATE_WORLD'),
                              ('mutation_tests', 'FLAG_ID')):
            with self.subTest(field=field):
                doc = self.document(23)
                doc[field][-1] = doc[field][0]
                self.call(23, document=doc, reason=reason)

    def test_duplicate_json_keys_at_root_and_nested_depth(self):
        for number in HEADS:
            text = json.dumps(self.document(number), separators=(',', ':'))
            nested = ('"A_THEN_B":[32,48]' if number == 22 else '"training_episodes":1')
            for needle in ('"new_E2":0', nested):
                with self.subTest(pr=number, needle=needle):
                    self.assertIn(needle, text)
                    raw = text.replace(needle, needle+','+needle, 1).encode()
                    self.call(number, raw=raw, reason='DUPLICATE_JSON_KEY')

    def test_nonfinite_json_rejected_before_schema_comparison(self):
        for number in HEADS:
            for value in ('NaN', 'Infinity', '-Infinity'):
                with self.subTest(pr=number, value=value):
                    raw = (json.dumps(self.document(number))[:-1]+',"ignored":'+value+'}').encode()
                    self.call(number, raw=raw, reason='NONFINITE_JSON_CONSTANT')

    def test_s78_source_coverage_rejected(self):
        rows = self.table(22)
        for altered in (rows[:-1], [*rows[:-1], rows[1]]):
            with self.subTest(rows=len(altered)):
                self.call(22, data=self.encoded(altered), reason='ORIGINAL_B_REJECTED')

    def test_declared_identity_and_count_type_confusion_rejected(self):
        for value in (False, 32.0):
            with self.subTest(pr=22, value=value):
                doc = self.document(22)
                doc['original_R282_paired_counts']['A_THEN_B'][0] = value
                self.call(22, document=doc, reason='PAIRED_SHAPE_OR_TYPE')
        for value in (True, 1.0):
            with self.subTest(pr=23, value=value):
                doc = self.document(23)
                doc['worlds'][0]['training_episodes'] = value
                self.call(23, document=doc, reason='WORLD_ID')

    def test_missing_or_success_shaped_extra_fields_rejected(self):
        for number in HEADS:
            for missing in (False, True):
                with self.subTest(pr=number, missing=missing):
                    doc = self.document(number)
                    if missing:
                        del doc['study']
                    else:
                        doc['status'] = 'PASS'
                    self.call(number, document=doc, reason='SCHEMA')

    def test_s78_original_executable_identity_is_mandatory(self):
        path = self.root/B_PATH
        original = path.read_bytes()
        try:
            path.write_bytes(original+b'\n// disposable identity corruption\n')
            self.call(22, reason='ORIGINAL_B_CODE_CHANGED')
        finally:
            path.write_bytes(original)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repo', type=Path, default=REPO)
    parser.add_argument('--evidence', type=Path)
    args, remaining = parser.parse_known_args()
    REPO = args.repo.resolve()
    if args.evidence:
        args.evidence.mkdir(parents=True, exist_ok=False)
    program = unittest.main(argv=[sys.argv[0], *remaining], exit=False)
    if args.evidence:
        result = dict(optimized=bool(sys.flags.optimize), sources=getattr(CLIContracts, 'identities', []),
                      methods=program.result.testsRun, failures=len(program.result.failures),
                      errors=len(program.result.errors), skipped=len(program.result.skipped),
                      calls=RECORDS)
        (args.evidence/'execution.json').write_text(json.dumps(result, indent=2)+'\n')
    sys.exit(0 if program.result.wasSuccessful() else 1)
