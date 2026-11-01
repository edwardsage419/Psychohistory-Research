#!/usr/bin/env python3
"""Fail-closed entrypoint for the eight frozen R333..R340 finite-E1 receipts.

This is an additive acceptance dependency. It never edits historical sources,
receipts, or protocols. A PASS proves only bounded archived E1 consistency.
Run from the repository with:
    python research/evidence_audit/r333_r340_acceptance_entry_20261101.py
    python -O research/evidence_audit/r333_r340_acceptance_entry_20261101.py
"""
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from pathlib import Path

GATES = {
    "R333": ("r333_r337_r338_r339_strict_gate_20261101.py", "fce37d846c96598f491a155be684c3b009f7d7a0", "positional"),
    "R334": ("r334_strict_receipt_gate_20261101.py", "bc025931c6bfaf3489ba3dcf91054a1e32fdaa29", "root"),
    "R335": ("r335_strict_receipt_gate_20261101.py", "8c42c0e7f53a6ac855d295d0ee72c5618dc664d9", "root"),
    "R336": ("r336_r340_strict_receipt_gate_20261101.py", "bdd44dbc0422b1e4bd33b6bc5281e00227cce865", "positional"),
    "R337": ("r333_r337_r338_r339_strict_gate_20261101.py", "fce37d846c96598f491a155be684c3b009f7d7a0", "positional"),
    "R338": ("r333_r337_r338_r339_strict_gate_20261101.py", "fce37d846c96598f491a155be684c3b009f7d7a0", "positional"),
    "R339": ("r333_r337_r338_r339_strict_gate_20261101.py", "fce37d846c96598f491a155be684c3b009f7d7a0", "positional"),
    "R340": ("r336_r340_strict_receipt_gate_20261101.py", "bdd44dbc0422b1e4bd33b6bc5281e00227cce865", "positional"),
}


def git_blob(raw: bytes) -> str:
    return hashlib.sha1(b"blob " + str(len(raw)).encode("ascii") + b"\0" + raw).hexdigest()


def reject_duplicate_keys(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("duplicate JSON key: " + key)
        result[key] = value
    return result


def verify_all(repo_root: Path, *, gate_specs=None, timeout=30, python=None):
    """Require all eight exact gate identities and independently checked receipts.

    gate_specs injection is used only by synthetic harness tests; the CLI always
    uses the frozen GATES map. The caller must treat that CLI as its trust root.
    """
    specs = GATES if gate_specs is None else gate_specs
    if set(specs) != {f"R{i}" for i in range(333, 341)}:
        raise ValueError("the full eight-model acceptance universe is mandatory")
    root = repo_root.resolve(strict=True)
    audit_dir = root / "research" / "evidence_audit"
    if not audit_dir.is_dir():
        raise ValueError("audit directory missing")
    # Authenticate all validator source bytes before executing any validator.
    unique_scripts = {}
    for model, (name, expected, mode) in sorted(specs.items()):
        if mode not in ("positional", "root") or Path(name).name != name:
            raise ValueError("invalid validator declaration for " + model)
        script = audit_dir / name
        if not script.is_file() or script.is_symlink():
            raise ValueError("validator missing or symlink: " + name)
        actual = git_blob(script.read_bytes())
        if actual != expected:
            raise ValueError("validator Git blob mismatch: " + name)
        if name in unique_scripts and unique_scripts[name] != expected:
            raise ValueError("inconsistent validator pin: " + name)
        unique_scripts[name] = expected
    executable = sys.executable if python is None else python
    results = []
    for model in sorted(specs):
        name, _, mode = specs[model]
        model_dir = root / "research" / model
        if not model_dir.is_dir() or model_dir.is_symlink():
            raise ValueError("model directory missing or symlink: " + model)
        for optimized in (False, True):
            cmd = [executable, "-I"]
            if optimized:
                cmd.append("-O")
            cmd.append(str(audit_dir / name))
            if mode == "positional":
                cmd.extend((model, str(model_dir)))
            else:
                cmd.extend(("--root", str(model_dir)))
            try:
                proc = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout, check=False)
            except (OSError, subprocess.TimeoutExpired) as exc:
                raise ValueError("validator execution error " + model + ": " + str(exc)) from exc
            if proc.returncode != 0 or proc.stderr.strip():
                raise ValueError("validator rejected " + model + " optimized=" + str(optimized) +
                                 " (exit=" + str(proc.returncode) + "): " + proc.stderr[:400])
            output = proc.stdout.strip()
            if mode == "positional":
                if output != "STRICT_GATE_PASS " + model:
                    raise ValueError("invalid validator success receipt: " + model)
            else:
                try:
                    receipt = json.loads(output, object_pairs_hook=reject_duplicate_keys)
                except (ValueError, TypeError) as exc:
                    raise ValueError("invalid validator JSON: " + model) from exc
                if not isinstance(receipt, dict) or receipt.get("status") != "PASS_BOUNDED_E1_RECEIPT":
                    raise ValueError("invalid validator E1 status: " + model)
                # Original source/receipt pins and finite arithmetic are
                # independently enforced inside the authenticated validator.
        results.append({"model": model, "gate_blob": specs[model][1], "result": "PASS_BOUNDED_E1_RECEIPT"})
    return {"status": "PASS_ALL_EIGHT_BOUNDED_E1_RECEIPTS", "evidence": "E1_ARTIFICIAL_ONLY",
            "models": results, "subprocess_checks": 16}


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--repo-root", type=Path, default=Path(__file__).resolve().parents[2])
    args = p.parse_args()
    try:
        result = verify_all(args.repo_root)
    except (ValueError, OSError) as exc:
        print("R333_R340_ACCEPTANCE_FAIL: " + str(exc), file=sys.stderr)
        return 1
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
