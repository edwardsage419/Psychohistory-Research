#!/usr/bin/env python3
"""Mutation-sensitive direct verify_preimage regression, R272 E1 only.

Run with --wrapper and --gate. Uses synthetic stand-in source and freeze bytes;
never invokes the historical generator or modifies repository archives.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

BASELINE_WRAPPER_BLOB = '8722fd4388421e3b1f77c6648b4ed1b38088c4b0'
GATE_SHA256 = 'f7109f8f815d166128ca3429fb42ff3e7cac780d03fb78f8243aeabbd6fbb786'
RECEIPT_BLOB = '85d36858911a7eb79c73c607cddf45ea88852a60'
GUARDS = {
    'source': "    require(blob(original) == ORIGINAL_BLOB, 'original generator Git blob differs')\n",
    'freeze': "    require(blob(freeze) == FREEZE_BLOB, 'prescore freeze Git blob differs')\n",
    'receipt': "    require(blob(mb) == RECEIPT_BLOB, 'archived machine receipt Git blob differs')\n",
}


def need(ok: bool, message: str) -> None:
    if not ok:
        raise RuntimeError(message)


def git_blob(data: bytes) -> str:
    return hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()


def load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    need(spec is not None and spec.loader is not None, 'module load failure')
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def fixture(gate):
    csv_bytes, result_bytes, receipt_bytes = gate.synthetic_fixture()
    result_bytes = (json.dumps(json.loads(result_bytes), indent=2, ensure_ascii=False) + '\n').encode()
    receipt = json.loads(receipt_bytes)
    receipt['results_sha256'] = hashlib.sha256(result_bytes).hexdigest()
    receipt_bytes = (json.dumps(receipt, indent=2) + '\n').encode()
    need(hashlib.sha256(csv_bytes).hexdigest() == gate.CSV_SHA, 'CSV historical pin differs')
    need(hashlib.sha256(result_bytes).hexdigest() == gate.JSON_SHA, 'results historical pin differs')
    need(git_blob(receipt_bytes) == RECEIPT_BLOB, 'receipt historical pin differs')
    need(gate.verify(csv_bytes, result_bytes, receipt_bytes, pins=True)['status'] == 'PASS',
         'scientific positive control failed')
    return csv_bytes, result_bytes, receipt_bytes


def execute_direct(wrapper_path: Path, gate_path: Path):
    wrapper = load('r272_wrapper_direct', wrapper_path)
    gate = load('r272_checker_direct', gate_path)
    cb, rb, mb = fixture(gate)
    original = b'R272 synthetic stand-in source; never executed\n'
    freeze = b'R272 synthetic stand-in freeze; not an authentic protocol\n'
    wrapper.ORIGINAL_BLOB = git_blob(original)
    wrapper.FREEZE_BLOB = git_blob(freeze)
    labels = ('source', 'freeze', 'csv', 'results', 'receipt')
    payloads = (original, freeze, cb, rb, mb)
    with tempfile.TemporaryDirectory(prefix='r272_preimage_regression_') as tmp:
        root = Path(tmp)
        paths = [root / rel for rel in (wrapper.ORIGINAL, wrapper.FREEZE, *wrapper.ARCHIVES)]
        for path, payload in zip(paths, payloads):
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(payload)
        need(wrapper.verify_preimage(root, gate)[1]['status'] == 'PASS', 'positive control failed')
        rejections = []
        for label, path, payload in zip(labels, paths, payloads):
            # Append a newline to alter bytes while preserving scientific values.
            path.write_bytes(payload + b'\n')
            try:
                wrapper.verify_preimage(root, gate)
            except (ValueError, OSError):
                rejections.append(label)
            finally:
                path.write_bytes(payload)
        # All five inputs must also reject a symlink, even if bytes are identical.
        link_rejections = []
        for label, path, payload in zip(labels, paths, payloads):
            elsewhere = root / ('target_' + label)
            elsewhere.write_bytes(payload)
            path.unlink()
            try:
                path.symlink_to(elsewhere)
                try:
                    wrapper.verify_preimage(root, gate)
                except (ValueError, OSError):
                    link_rejections.append(label)
            finally:
                path.unlink(missing_ok=True)
                path.write_bytes(payload)
        result = dict(positive=1, byte_rejections=rejections, symlink_rejections=link_rejections,
                      missed_byte=[x for x in labels if x not in rejections],
                      missed_symlink=[x for x in labels if x not in link_rejections])
        print(json.dumps(result, sort_keys=True))
        need(len(rejections) == 5 and len(link_rejections) == 5,
             'direct preimage guard regression: ' + repr(result))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--wrapper', type=Path, required=True)
    parser.add_argument('--gate', type=Path, required=True)
    parser.add_argument('--direct', action='store_true', help='internal child process direct tests')
    args = parser.parse_args()
    wrapper_path = args.wrapper.resolve(strict=True)
    gate_path = args.gate.resolve(strict=True)
    need(hashlib.sha256(gate_path.read_bytes()).hexdigest() == GATE_SHA256,
         'checker identity mismatch')
    if args.direct:
        execute_direct(wrapper_path, gate_path)
        return
    source = wrapper_path.read_bytes()
    need(git_blob(source) == BASELINE_WRAPPER_BLOB, 'baseline wrapper identity mismatch')
    text = source.decode('utf-8')
    modes = ((), ('-O',), ('-OO',))
    baseline = []
    mutants = []
    with tempfile.TemporaryDirectory(prefix='r272_guard_mutants_') as tmp:
        for mode in modes:
            run = subprocess.run([sys.executable, *mode, __file__, '--wrapper', str(wrapper_path),
                                  '--gate', str(gate_path), '--direct'], capture_output=True,
                                 text=True, timeout=90, check=False)
            need(run.returncode == 0, 'baseline direct path failed: ' + run.stderr[-2000:])
            data = json.loads(run.stdout)
            need(len(data['byte_rejections']) == 5 and len(data['symlink_rejections']) == 5,
                 'baseline incomplete')
            baseline.append(dict(mode=mode[0] if mode else 'normal', **data))
        for label, guard in GUARDS.items():
            need(text.count(guard) == 1, 'guard signature changed: ' + label)
            path = Path(tmp) / (label + '_guard_removed.py')
            path.write_text(text.replace(guard, '', 1), encoding='utf-8')
            for mode in modes:
                run = subprocess.run([sys.executable, *mode, __file__, '--wrapper', str(path),
                                      '--gate', str(gate_path), '--direct'], capture_output=True,
                                     text=True, timeout=90, check=False)
                need(run.returncode != 0, 'removed guard escaped regression: ' + label)
                data = json.loads(run.stdout)
                need(label in data['missed_byte'], 'unexpected mutant failure: ' + label)
                mutants.append(dict(removed_guard=label, mode=mode[0] if mode else 'normal',
                                    missed_byte=data['missed_byte'],
                                    regression_exit_nonzero=True))
    print(json.dumps(dict(status='PASS', scope='INTERNAL_NONBLIND_SYNTHETIC_E1',
                          wrapper_blob=BASELINE_WRAPPER_BLOB, gate_sha256=GATE_SHA256,
                          baseline_modes=len(baseline), baseline_positive=len(baseline),
                          baseline_byte_rejections=sum(len(x['byte_rejections']) for x in baseline),
                          baseline_symlink_rejections=sum(len(x['symlink_rejections']) for x in baseline),
                          removed_guard_regression_failures=len(mutants), mutants=mutants,
                          source_and_freeze='SYNTHETIC_STAND_INS',
                          native_full_checkout='NOT_RUN', original_generator='NOT_RUN',
                          github_actions='NOT_RUN'), sort_keys=True))


if __name__ == '__main__':
    try:
        main()
    except (RuntimeError, ValueError, OSError, subprocess.TimeoutExpired) as error:
        raise SystemExit('FAIL: ' + str(error)) from error
