#!/usr/bin/env python3
"""R272 native replay from pinned generator and freeze, with preimage negatives.

Requires local files authenticated against the recorded Git blob identities.
All generation and corruption occur in disposable directories. This is an
internal nonblind E1 program audit, not an external-data replication or CI.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

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
}
WRAPPER_BLOB = '8722fd4388421e3b1f77c6648b4ed1b38088c4b0'
GATE_SHA256 = 'f7109f8f815d166128ca3429fb42ff3e7cac780d03fb78f8243aeabbd6fbb786'


def require(ok: bool, why: str) -> None:
    if not ok:
        raise RuntimeError(why)


def blob(raw: bytes) -> str:
    return hashlib.sha1(b'blob ' + str(len(raw)).encode() + b'\0' + raw).hexdigest()


def get(root: Path, relative: str) -> bytes:
    p = root / relative
    require(p.is_file() and not p.is_symlink(), 'missing or symlink: ' + relative)
    return p.read_bytes()


def run(argv: list[str], cwd: Path, expected_success: bool = True) -> subprocess.CompletedProcess[str]:
    proc = subprocess.run(argv, cwd=cwd, text=True, capture_output=True,
                          timeout=120, check=False)
    if expected_success:
        require(proc.returncode == 0, 'unexpected rejection: ' + repr(argv) + '\n' + proc.stderr[-1500:])
    else:
        require(proc.returncode != 0, 'false acceptance: ' + repr(argv) + '\n' + proc.stdout[-1500:])
        require(proc.stderr.startswith('FAIL:'), 'negative rejected for unexpected reason: ' + proc.stderr[-1500:])
    return proc


def copy_input(root: Path, temp: Path, relative: str) -> None:
    target = temp / relative
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(get(root, relative))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('--root', type=Path, required=True,
                        help='local checkout containing authentic generator and freeze')
    parser.add_argument('--wrapper', type=Path, required=True)
    parser.add_argument('--gate', type=Path, required=True)
    args = parser.parse_args()
    root = args.root.resolve(strict=True)
    wrapper = args.wrapper.resolve(strict=True)
    gate = args.gate.resolve(strict=True)
    require(blob(wrapper.read_bytes()) == WRAPPER_BLOB, 'wrapper identity mismatch')
    require(hashlib.sha256(gate.read_bytes()).hexdigest() == GATE_SHA256,
            'independent checker identity mismatch')
    for relative in (ORIGINAL, FREEZE):
        require(blob(get(root, relative)) == BLOBS[relative], 'input identity mismatch: ' + relative)
    modes = ((), ('-O',), ('-OO',))
    results = []
    with tempfile.TemporaryDirectory(prefix='r272_pinned_native_') as work:
        base = Path(work) / 'base'
        for relative in (ORIGINAL, FREEZE):
            copy_input(root, base, relative)
        # The archived files are regenerated only inside this disposable root.
        run([sys.executable, str(base / ORIGINAL), '--emit'], base)
        originals = {}
        for relative in ARCHIVES:
            raw = get(base, relative)
            require(blob(raw) == BLOBS[relative], 'regenerated historical blob differs: ' + relative)
            originals[relative] = raw
        for mode in modes:
            label = mode[0] if mode else 'normal'
            tests = run([sys.executable, *mode, str(base / ORIGINAL), '--test'], base)
            require('Ran 83 tests' in tests.stderr, 'native unittest count differs')
            native = run([sys.executable, *mode, str(gate), '--root', str(base)], base)
            native_result = json.loads(native.stdout)
            require(native_result['status'] == 'PASS' and native_result['rows'] == 576,
                    'independent gate incomplete')
            wrapper_cmd = [sys.executable, *mode, str(wrapper), '--root', str(base),
                           '--gate', str(gate), '--regenerate']
            good = json.loads(run(wrapper_cmd, base).stdout)
            require(good['status'] == 'PASS' and good['checked_archived_preimage']
                    and good['isolated_regeneration_compared'] and good['original_archives_untouched'],
                    'wrapper missing required success claims')
            for relative in (ORIGINAL, FREEZE, *ARCHIVES):
                require(blob(get(base, relative)) == BLOBS[relative],
                        'base root changed: ' + relative)
            rejected = []
            for relative in (ORIGINAL, FREEZE, *ARCHIVES):
                mutant = Path(work) / ('mutant_' + label.replace('-', '') + '_' + str(len(rejected)))
                for item in (ORIGINAL, FREEZE, *ARCHIVES):
                    copy_input(base, mutant, item)
                changed = get(mutant, relative) + b'\n'
                (mutant / relative).write_bytes(changed)
                bad_cmd = [sys.executable, *mode, str(wrapper), '--root', str(mutant),
                           '--gate', str(gate), '--regenerate']
                run(bad_cmd, mutant, expected_success=False)
                require(get(mutant, relative) == changed,
                        'negative input overwritten during rejection')
                rejected.append(relative)
            results.append({'mode': label, 'positive': 1, 'negative_rejections': len(rejected),
                            'generator_tests': 'PASS', 'native_gate': 'PASS',
                            'isolated_regeneration': 'PASS'})
        # Actual pinned generator can mask a corrupt preimage if it runs first.
        masking = Path(work) / 'masking'
        for relative in (ORIGINAL, FREEZE, *ARCHIVES):
            copy_input(base, masking, relative)
        corrupt = ARCHIVES[0]
        (masking / corrupt).write_bytes(originals[corrupt] + b'\n')
        precheck = [sys.executable, str(wrapper), '--root', str(masking),
                    '--gate', str(gate), '--regenerate']
        run(precheck, masking, expected_success=False)
        require(get(masking, corrupt) != originals[corrupt], 'preimage unexpectedly repaired')
        run([sys.executable, str(masking / ORIGINAL), '--emit'], masking)
        require(get(masking, corrupt) == originals[corrupt], 'generator failed to overwrite corruption')
        repaired = json.loads(run(precheck, masking).stdout)
        require(repaired['status'] == 'PASS', 'post-overwrite control failed')
    print(json.dumps({
        'status': 'PASS', 'scope': 'INTERNAL_NONBLIND_FINITE_ARTIFICIAL_E1',
        'input_source_blobs': {x: BLOBS[x] for x in (ORIGINAL, FREEZE)},
        'reconstructed_archive_blobs': {x: BLOBS[x] for x in ARCHIVES},
        'python': sys.version.split()[0], 'modes': results,
        'negative_rejections_total': sum(x['negative_rejections'] for x in results),
        'preimage_corruption_rejected_before_emit': True,
        'same_corruption_masked_by_original_emit_then_accepted': True,
        'historical_remote_checkout_preimage_downloaded': False,
        'github_actions_executed': False,
        'external_data_or_team_reproduction': False,
    }, ensure_ascii=False, sort_keys=True))


if __name__ == '__main__':
    try:
        main()
    except (RuntimeError, ValueError, OSError, subprocess.TimeoutExpired) as exc:
        raise SystemExit('FAIL: ' + str(exc)) from exc
