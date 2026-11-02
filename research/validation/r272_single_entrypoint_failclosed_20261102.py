#!/usr/bin/env python3
"""R272 proposed single-entrypoint fail-closed local acceptance executor.

Runs only on an already available complete repository checkout. Never dispatches
Actions, writes archived evidence, or executes shell command strings. This is a
candidate for independent review, not a production workflow installation.
"""
from __future__ import annotations

import argparse
import hashlib
import io
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import zipfile

ZIP_PATH = 'research/validation/R272_P0_FAILCLOSED_CANDIDATE_20261102.zip'
ZIP_SHA256 = 'f23b04706b60ac70bdbee6f051a74551779fb9d9a9b9af08c96cda345b055151'
GATE_NAME = 'r272_failclosed_independent_receipt_gate_20261102.py'
GATE_SHA256 = 'f7109f8f815d166128ca3429fb42ff3e7cac780d03fb78f8243aeabbd6fbb786'
WRAPPER = 'research/validation/r272_preimage_first_readonly_gate_20261102.py'
WRAPPER_BLOB = '8722fd4388421e3b1f77c6648b4ed1b38088c4b0'
NEGATIVE = 'research/validation/r272_pinned_native_replay_and_preimage_negative_20261102.py'
NEGATIVE_BLOB = '9b8a5a566b7f48c7e72ba34505d49eebe3a94b44'
ORIGINAL = 'research/R272/r272_exact_train_test_prediction.py'
FREEZE = 'protocols/R272_OUT_OF_SAMPLE_9_BERNOULLI_WORLDS_576_FULL_SOURCE_PRESCORE_FREEZE_2026-10-23.md'
ARCHIVES = (
    'research/R272/R272_ALL_576_ORIGINAL_TRAIN_AND_TEST_SOURCES.csv',
    'research/R272/R272_EXACT_RESULTS.json',
    'research/R272/R272_MACHINE_RECEIPT.json',
)
BLOBS = {
    ORIGINAL: '13843eecf2f9f05c19ee5545bdb224f58313f367',
    FREEZE: '9fbdb0078a58c4a9c0a548643227e30da5731119',
    ARCHIVES[0]: '8fbbc73d239765f5c66395af1bcf9cf7a8df1f41',
    ARCHIVES[1]: 'db3ca11ae224af52c2caf385c898e24aaa0cc54b',
    ARCHIVES[2]: '85d36858911a7eb79c73c607cddf45ea88852a60',
    WRAPPER: WRAPPER_BLOB,
    NEGATIVE: NEGATIVE_BLOB,
}


def require(condition: bool, reason: str) -> None:
    if not condition:
        raise ValueError(reason)


def git_blob(data: bytes) -> str:
    return hashlib.sha1(b'blob ' + str(len(data)).encode('ascii') + b'\0' + data).hexdigest()


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def read_pinned(root: Path, relative: str, expected: str) -> bytes:
    path = root / relative
    require(path.is_file() and not path.is_symlink(), 'missing or symlink: ' + relative)
    raw = path.read_bytes()
    require(git_blob(raw) == expected, 'Git blob mismatch: ' + relative)
    return raw


def gate_from_zip(raw: bytes) -> bytes:
    require(sha256(raw) == ZIP_SHA256, 'checker ZIP SHA256 mismatch')
    with zipfile.ZipFile(io.BytesIO(raw)) as archive:
        members = archive.infolist()
        require(len(members) == 1 and members[0].filename == GATE_NAME,
                'checker ZIP must contain exactly the pinned member')
        require(not members[0].is_dir() and members[0].file_size < 2_000_000,
                'checker ZIP member invalid or oversized')
        gate = archive.read(members[0])
    require(sha256(gate) == GATE_SHA256, 'extracted checker SHA256 mismatch')
    return gate


def run_checked(args: list[str], cwd: Path, *, expect_json: bool = False,
                stderr_contains: str | None = None) -> dict | str:
    require(all(isinstance(x, str) and x for x in args), 'invalid process arguments')
    process = subprocess.run(args, cwd=cwd, text=True, capture_output=True,
                             timeout=180, check=False, shell=False)
    require(process.returncode == 0,
            'child failed with exit ' + str(process.returncode) + ': '
            + repr(args) + '\n' + process.stderr[-1500:])
    if stderr_contains is not None:
        require(stderr_contains in process.stderr,
                "expected test receipt missing: " + stderr_contains)
    if not expect_json:
        return process.stdout
    try:
        result = json.loads(process.stdout)
    except json.JSONDecodeError as exc:
        raise ValueError('child returned invalid JSON: ' + repr(args)) from exc
    require(isinstance(result, dict) and result.get('status') == 'PASS',
            'child returned non-PASS or malformed JSON: ' + repr(args))
    return result


def audit(root: Path) -> dict:
    root = root.resolve(strict=True)
    before = {p: read_pinned(root, p, digest) for p, digest in BLOBS.items()}
    zip_path = root / ZIP_PATH
    require(zip_path.is_file() and not zip_path.is_symlink(), 'checker ZIP unavailable')
    gate_bytes = gate_from_zip(zip_path.read_bytes())
    results = []
    with tempfile.TemporaryDirectory(prefix='r272_single_entry_') as tmp:
        gate_path = Path(tmp) / GATE_NAME
        gate_path.write_bytes(gate_bytes)
        gate_path.chmod(0o444)
        for flags, label in (([], 'normal'), (['-O'], 'optimized'), (['-OO'], 'double_optimized')):
            wrapper_result = run_checked(
                [sys.executable, *flags, str(root / WRAPPER), '--root', str(root),
                 '--gate', str(gate_path), '--regenerate'], root, expect_json=True)
            require(wrapper_result.get('checked_archived_preimage') is True
                    and wrapper_result.get('isolated_regeneration_compared') is True
                    and wrapper_result.get('original_archives_untouched') is True,
                    'mandatory wrapper evidence incomplete: ' + label)
            science = wrapper_result.get('scientific')
            require(isinstance(science, dict) and science.get('status') == 'PASS'
                    and science.get('rows') == 576,
                    'scientific checker evidence incomplete: ' + label)
            test_stdout = run_checked(
                [sys.executable, *flags, str(root / ORIGINAL), '--test'], root,
                stderr_contains='Ran 83 tests')
            require(isinstance(test_stdout, str), 'generator test output malformed')
            negative = run_checked(
                [sys.executable, *flags, str(root / NEGATIVE), '--root', str(root),
                 '--wrapper', str(root / WRAPPER), '--gate', str(gate_path)],
                root, expect_json=True)
            require(negative.get('negative_rejections_total') == 15
                    and negative.get('preimage_corruption_rejected_before_emit') is True
                    and negative.get('same_corruption_masked_by_original_emit_then_accepted') is True,
                    'native negative regression incomplete: ' + label)
            for path, payload in before.items():
                require(read_pinned(root, path, BLOBS[path]) == payload,
                        'tracked source or archive changed during audit: ' + path)
            results.append({'mode': label, 'preimage': 'PASS',
                            'isolated_regeneration': 'PASS', 'native_negatives': 15,
                            'original_tests_exit': 0})
    return {'status': 'PASS', 'scope': 'INTERNAL_NONBLIND_ARTIFICIAL_E1',
            'workflow_adopted': False, 'actions_executed': False,
            'archive_bytes_preserved': True, 'modes': results}


def self_test() -> dict:
    require(git_blob(b'') == 'e69de29bb2d1d6434b8b29ae775ad8c2e48c5391',
            'Git blob oracle failed')
    with tempfile.TemporaryDirectory(prefix='r272_single_selftest_') as tmp:
        root = Path(tmp)
        p = root / 'pinned.txt'
        p.write_bytes(b'hello')
        require(read_pinned(root, 'pinned.txt', git_blob(b'hello')) == b'hello',
                'positive identity control failed')
        rejects = 0
        for case in ('identity', 'nonzero', 'false_pass', 'invalid_json', 'wrong_zip'):
            try:
                if case == 'identity':
                    read_pinned(root, 'pinned.txt', git_blob(b'other'))
                elif case == 'nonzero':
                    run_checked([sys.executable, '-c', 'raise SystemExit(9)'], root)
                elif case == 'false_pass':
                    run_checked([sys.executable, '-c', 'print(\'{"status":"FAIL"}\')'],
                                root, expect_json=True)
                elif case == 'invalid_json':
                    run_checked([sys.executable, '-c', 'print("not json")'],
                                root, expect_json=True)
                else:
                    gate_from_zip(b'not-a-zip')
            except (ValueError, zipfile.BadZipFile):
                rejects += 1
        require(rejects == 5, 'selftest did not reject every negative case')
    return {'status': 'PASS', 'negative_controls_rejected': rejects,
            'scope': 'SELFTEST_ONLY', 'complete_checkout_execution': False}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('--root', type=Path)
    parser.add_argument('--selftest', action='store_true')
    args = parser.parse_args()
    require(args.selftest or args.root is not None, 'supply --root or --selftest')
    result = self_test() if args.selftest else audit(args.root)
    print(json.dumps(result, sort_keys=True))


if __name__ == '__main__':
    try:
        main()
    except (ValueError, OSError, RuntimeError, subprocess.TimeoutExpired,
            zipfile.BadZipFile) as exc:
        raise SystemExit('FAIL: ' + str(exc)) from exc
