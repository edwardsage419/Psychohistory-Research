#!/usr/bin/env python3
"""R272 wrapper mutation sensitivity audit. Standard library, synthetic fixtures only.

This audit never changes the historical generator, frozen protocol, archived
receipts, or production workflow. It deliberately mutates disposable copies
of the proposed read-only wrapper and tests whether its self-test detects loss
of critical source/protocol/receipt identity guards.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import subprocess
import sys
import tempfile
from pathlib import Path

WRAPPER_GIT_BLOB = '8722fd4388421e3b1f77c6648b4ed1b38088c4b0'
GATE_SHA256 = 'f7109f8f815d166128ca3429fb42ff3e7cac780d03fb78f8243aeabbd6fbb786'
GUARDS = {
    'source_blob': "    require(blob(original) == ORIGINAL_BLOB, 'original generator Git blob differs')\n",
    'freeze_blob': "    require(blob(freeze) == FREEZE_BLOB, 'prescore freeze Git blob differs')\n",
    'receipt_blob': "    require(blob(mb) == RECEIPT_BLOB, 'archived machine receipt Git blob differs')\n",
}

def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def git_blob(data: bytes) -> str:
    return hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    require(spec is not None and spec.loader is not None, 'cannot load module')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def historical_fixture(gate):
    cb, rb, mb = gate.synthetic_fixture()
    rb = (json.dumps(json.loads(rb), indent=2, ensure_ascii=False) + '\n').encode()
    receipt = json.loads(mb)
    receipt['results_sha256'] = hashlib.sha256(rb).hexdigest()
    mb = (json.dumps(receipt, indent=2) + '\n').encode()
    require(git_blob(mb) == '85d36858911a7eb79c73c607cddf45ea88852a60', 'receipt fixture not pinned')
    require(gate.verify(cb, rb, mb, pins=True)['status'] == 'PASS', 'fixture scientific failure')
    return cb, rb, mb


def populate(root: Path, wrapper, cb: bytes, rb: bytes, mb: bytes):
    original = b'local synthetic original program for sensitivity audit\n'
    freeze = b'local synthetic prescore freeze for sensitivity audit\n'
    for rel, data in zip((wrapper.ORIGINAL, wrapper.FREEZE, *wrapper.ARCHIVES),
                         (original, freeze, cb, rb, mb)):
        path = root / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)
    wrapper.ORIGINAL_BLOB = git_blob(original)
    wrapper.FREEZE_BLOB = git_blob(freeze)


def rejected(wrapper, root: Path, gate) -> bool:
    try:
        wrapper.verify_preimage(root, gate)
    except ValueError:
        return True
    return False


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--wrapper', type=Path, required=True)
    parser.add_argument('--gate', type=Path, required=True)
    args = parser.parse_args()
    wrapper_bytes = args.wrapper.read_bytes()
    gate_bytes = args.gate.read_bytes()
    require(git_blob(wrapper_bytes) == WRAPPER_GIT_BLOB, 'wrapper source Git blob differs from main')
    require(hashlib.sha256(gate_bytes).hexdigest() == GATE_SHA256, 'gate source SHA256 differs')
    text = wrapper_bytes.decode('utf-8')
    baseline = load_module('r272_wrapper_baseline', args.wrapper)
    gate = load_module('r272_gate_sensitivity', args.gate)
    cb, rb, mb = historical_fixture(gate)
    with tempfile.TemporaryDirectory(prefix='r272_guard_sensitivity_') as temp:
        root = Path(temp) / 'synthetic_checkout'
        populate(root, baseline, cb, rb, mb)
        require(baseline.verify_preimage(root, gate)[1]['status'] == 'PASS', 'baseline positive')
        baseline_rejections = []
        for label, relative in (('source_blob', baseline.ORIGINAL),
                                ('freeze_blob', baseline.FREEZE),
                                ('receipt_blob', baseline.ARCHIVES[2])):
            target = root / relative
            original_bytes = target.read_bytes()
            target.write_bytes(original_bytes + b'\n')
            require(rejected(baseline, root, gate), 'baseline failed to reject ' + label)
            baseline_rejections.append(label)
            target.write_bytes(original_bytes)
        results = []
        for label, line in GUARDS.items():
            require(text.count(line) == 1, 'expected unique guard missing: ' + label)
            mutant_path = Path(temp) / (label + '_mutant.py')
            mutant_path.write_text(text.replace(line, '', 1), encoding='utf-8')
            mutant = load_module('r272_mutant_' + label, mutant_path)
            populate(root, mutant, cb, rb, mb)
            require(mutant.verify_preimage(root, gate)[1]['status'] == 'PASS', 'mutant positive failure')
            # Remove one input identity and test whether the corresponding guard still rejects.
            if label == 'source_blob':
                target = root / mutant.ORIGINAL
                target.write_bytes(target.read_bytes() + b'\n')
            elif label == 'freeze_blob':
                target = root / mutant.FREEZE
                target.write_bytes(target.read_bytes() + b'\n')
            else:
                target = root / mutant.ARCHIVES[2]
                target.write_bytes(mb + b'\n')
            require(not rejected(mutant, root, gate), 'mutant did not bypass removed guard: ' + label)
            modes = []
            for mode in ((), ('-O',), ('-OO',)):
                process = subprocess.run([sys.executable, *mode, str(mutant_path),
                                          '--gate', str(args.gate), '--self-test'],
                                         capture_output=True, text=True, check=False, timeout=30)
                require(process.returncode == 0,
                        'mutant self-test failed unexpectedly: ' + label + repr(mode) + process.stderr)
                self_result = json.loads(process.stdout)
                require(self_result['status'] == 'PASS', 'mutant self-test status failed')
                modes.append('normal' if not mode else mode[0])
            results.append(dict(removed_guard=label, corrupted_input_accepted=True,
                                wrapper_self_test_still_passes=True, modes=modes))
            # Reset root for next mutant.
            populate(root, baseline, cb, rb, mb)
        print(json.dumps(dict(status='PASS', evidence='INTERNAL_NONBLIND_SYNTHETIC_MUTATION_SENSITIVITY',
                              wrapper_git_blob=WRAPPER_GIT_BLOB, gate_sha256=GATE_SHA256,
                              baseline_clean_pass=True, baseline_corrupt_identity_rejections=baseline_rejections,
                              removed_guard_mutants=len(results), selftest_false_passes=sum(len(x["modes"]) for x in results),
                              cases=results, original_generator_executed=False,
                              full_checkout_native_execution=False, ci_triggered=False), sort_keys=True))

if __name__ == '__main__':
    try:
        main()
    except (RuntimeError, ValueError, OSError, subprocess.TimeoutExpired) as exc:
        raise SystemExit('FAIL: ' + str(exc)) from exc
