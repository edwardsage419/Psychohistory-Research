#!/usr/bin/env python3
"""R272 workflow archived-input preimage and trigger coverage audit.

Read-only, standard library. Checks workflow text and original generator source.
Does not execute GitHub Actions or establish historical tampering.
"""
import argparse
import fnmatch
import json
import unittest
from pathlib import Path

WORKFLOW = '.github/workflows/r272-exact-train-test-oos-e1.yml'
GENERATOR = 'research/R272/r272_exact_train_test_prediction.py'
ARCHIVES = (
    'research/R272/R272_ALL_576_ORIGINAL_TRAIN_AND_TEST_SOURCES.csv',
    'research/R272/R272_EXACT_RESULTS.json',
    'research/R272/R272_MACHINE_RECEIPT.json',
)
CANDIDATE = 'research/validation/R272_P0_FAILCLOSED_CANDIDATE_20261102.zip'


def push_paths(yaml_text):
    """Extract the known simple push.paths list and fail on missing structure."""
    lines = yaml_text.splitlines()
    try:
        push = next(i for i, s in enumerate(lines) if s == '  push:')
        paths = next(i for i in range(push + 1, len(lines)) if lines[i] == '    paths:')
    except StopIteration as exc:
        raise ValueError('push.paths not found') from exc
    out = []
    for line in lines[paths + 1:]:
        if line.startswith('      - '):
            out.append(line[8:].strip().strip("'\""))
        elif line and not line.startswith('      '):
            break
    if not out:
        raise ValueError('empty push.paths')
    return out


def matches(paths, filename):
    return any(fnmatch.fnmatchcase(filename, pattern) for pattern in paths)


def audit(workflow, generator):
    paths = push_paths(workflow)
    emit = 'python research/R272/r272_exact_train_test_prediction.py --emit'
    audit_start = 'rows=list(csv.DictReader(source.open()))'
    first = workflow.find(emit)
    second = workflow.find(audit_start)
    if first < 0 or second < 0:
        raise ValueError('workflow emit or archive read not found')
    writes = (
        'with src.open("w",encoding="utf-8",newline="")',
        'jp.write_text(json.dumps(results,indent=2,ensure_ascii=False)+"\\n"',
        '(HERE/"R272_MACHINE_RECEIPT.json").write_text(',
    )
    return {
        'archive_push_covered': {p: matches(paths, p) for p in ARCHIVES},
        'candidate_push_covered': matches(paths, CANDIDATE),
        'generator_push_covered': matches(paths, GENERATOR),
        'workflow_push_covered': matches(paths, WORKFLOW),
        'emit_before_archive_read': first < second,
        'generator_writes_all_three_archives': all(s in generator for s in writes),
        'mandatory_failclosed_candidate_called': 'r272_failclosed_independent_receipt_gate_20261102.py --root' in workflow,
        'workflow_can_commit_archives': 'permissions:\n  contents: write' in workflow and 'git add research/R272/' in workflow,
    }


class Tests(unittest.TestCase):
    def setUp(self):
        self.yaml = """name: R272
on:
  push:
    paths:
      - 'research/R272/r272_exact_train_test_prediction.py'
      - '.github/workflows/r272-exact-train-test-oos-e1.yml'
  workflow_dispatch:
permissions:
  contents: write
steps:
  run: |
    python research/R272/r272_exact_train_test_prediction.py --emit
    rows=list(csv.DictReader(source.open()))
    git add research/R272/file
"""
        self.source = """with src.open("w",encoding="utf-8",newline=""):
 jp.write_text(json.dumps(results,indent=2,ensure_ascii=False)+"\\n")
 (HERE/"R272_MACHINE_RECEIPT.json").write_text(
"""

    def test_existing_archive_paths_uncovered(self):
        r = audit(self.yaml, self.source)
        self.assertEqual(list(r['archive_push_covered'].values()), [False] * 3)
        self.assertFalse(r['candidate_push_covered'])

    def test_existing_generator_and_workflow_covered(self):
        r = audit(self.yaml, self.source)
        self.assertTrue(r['generator_push_covered'] and r['workflow_push_covered'])

    def test_emit_precedes_read(self):
        r = audit(self.yaml, self.source)
        self.assertTrue(r['emit_before_archive_read'])
        self.assertTrue(r['generator_writes_all_three_archives'])
        self.assertTrue(r['workflow_can_commit_archives'])

    def test_no_mandatory_candidate(self):
        self.assertFalse(audit(self.yaml, self.source)['mandatory_failclosed_candidate_called'])

    def test_explicit_archive_trigger_would_cover(self):
        amended = self.yaml.replace("      - 'research/R272/r272_exact_train_test_prediction.py'",
            "      - 'research/R272/**'\n      - 'research/validation/**'")
        r = audit(amended, self.source)
        self.assertTrue(all(r['archive_push_covered'].values()))
        self.assertTrue(r['candidate_push_covered'])

    def test_read_before_emit_removes_masking_order(self):
        changed = self.yaml.replace(
            '    python research/R272/r272_exact_train_test_prediction.py --emit\n    rows=list(csv.DictReader(source.open()))',
            '    rows=list(csv.DictReader(source.open()))\n    python research/R272/r272_exact_train_test_prediction.py --emit')
        self.assertFalse(audit(changed, self.source)['emit_before_archive_read'])

    def test_missing_or_ambiguous_structure_rejected(self):
        with self.assertRaises(ValueError):
            push_paths('on:\n  push:\n    branches: [main]\n')


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--root', type=Path)
    p.add_argument('--self-test', action='store_true')
    args = p.parse_args()
    if args.self_test:
        unittest.main(argv=['audit'], verbosity=2)
    elif args.root:
        print(json.dumps(audit((args.root / WORKFLOW).read_text(),
                              (args.root / GENERATOR).read_text()), indent=2, sort_keys=True))
    else:
        p.error('use --root or --self-test')
