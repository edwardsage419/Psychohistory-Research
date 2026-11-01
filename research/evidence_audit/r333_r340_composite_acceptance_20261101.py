#!/usr/bin/env python3
"""Candidate composite R333..R340 E1 acceptance gate.

Requires both the frozen mathematical entry and the historical claim gate.
This is an additive research tool. Production caller adoption is unestablished.
Run with --repo-root PATH. Python standard library and local Node.js required.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

AUDIT = Path("research/evidence_audit")
PINS = {
    "r333_r340_acceptance_entry_20261101.py": "9822418253c6a2888119c2a823ffee62dd945d7c",
    "r333_r340_claim_receipt_gate_20261101.js": "add869ed3c8dc3f9eb39d91fb836ac9df5eb307f",
}
MODELS = [f"R{x}" for x in range(333, 341)]


def git_blob(data: bytes) -> str:
    return hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()


def no_duplicate_keys(pairs):
    out = {}
    for key, value in pairs:
        if key in out:
            raise ValueError("duplicate JSON key: " + key)
        out[key] = value
    return out


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def run_json(command: list[str], *, timeout: int) -> dict:
    try:
        result = subprocess.run(command, capture_output=True, text=True, timeout=timeout,
                                check=False, encoding="utf-8")
    except (OSError, subprocess.TimeoutExpired, UnicodeError) as exc:
        raise ValueError("child invocation failed: " + str(exc)) from exc
    require(result.returncode == 0, "child exit " + str(result.returncode) + ": " + result.stderr[:300])
    require(not result.stderr.strip(), "unexpected child stderr: " + result.stderr[:300])
    try:
        value = json.loads(result.stdout, object_pairs_hook=no_duplicate_keys)
    except (ValueError, TypeError) as exc:
        raise ValueError("invalid child JSON: " + str(exc)) from exc
    require(isinstance(value, dict), "child output must be JSON object")
    return value


def validate_math(value: dict) -> None:
    require(value.get("status") == "PASS_ALL_EIGHT_BOUNDED_E1_RECEIPTS", "math status")
    require(value.get("evidence") == "E1_ARTIFICIAL_ONLY", "math evidence")
    require(type(value.get("subprocess_checks")) is int and value["subprocess_checks"] == 16,
            "math subprocess count")
    models = value.get("models")
    require(isinstance(models, list) and len(models) == 8, "math universe length")
    require([m.get("model") for m in models if isinstance(m, dict)] == MODELS,
            "math universe identity/order")
    require(all(m.get("result") == "PASS_BOUNDED_E1_RECEIPT" and
                isinstance(m.get("gate_blob"), str) and len(m["gate_blob"]) == 40
                for m in models), "math model results")


def validate_claim(value: dict) -> None:
    require(value.get("status") == "PASS_HISTORICAL_CLAIMS_E1_IDENTITY_ONLY", "claim status")
    require(type(value.get("files_checked")) is int and value["files_checked"] == 16,
            "claim file count")
    require(value.get("mathematical_gate") == "NOT_RUN", "claim mathematical boundary")
    require(value.get("production_adoption") == "NOT_ESTABLISHED", "claim adoption boundary")
    models = value.get("models")
    require(isinstance(models, list) and len(models) == 8, "claim universe length")
    require([m.get("model") for m in models if isinstance(m, dict)] == MODELS,
            "claim universe identity/order")
    require(all(isinstance(m.get("machine_blob"), str) and len(m["machine_blob"]) == 40
                and isinstance(m.get("final_blob"), str) and len(m["final_blob"]) == 40
                and type(m.get("CI_run")) is int for m in models), "claim receipts")


def verify(repo_root: Path, *, pins: dict | None = None,
           python_executable: str | None = None, node_executable: str = "node",
           timeout: int = 120) -> dict:
    """pins override is for synthetic unit tests only. CLI always uses PINS."""
    root = repo_root.resolve(strict=True)
    require(root.is_dir(), "repo root is not directory")
    audit = root / AUDIT
    require(audit.is_dir() and not audit.is_symlink(), "unsafe audit directory")
    specs = PINS if pins is None else pins
    require(set(specs) == set(PINS), "exact two-gate universe required")
    for name, expected in specs.items():
        file = audit / name
        require(file.is_file() and not file.is_symlink(), "missing or symlink gate " + name)
        require(git_blob(file.read_bytes()) == expected, "gate source mismatch " + name)
    py = python_executable or sys.executable
    math = audit / "r333_r340_acceptance_entry_20261101.py"
    claim = audit / "r333_r340_claim_receipt_gate_20261101.js"
    # The claim gate and both Python interpreter modes are mandatory.
    claim_result = run_json([node_executable, str(claim), "--repo-root", str(root)], timeout=timeout)
    validate_claim(claim_result)
    math_results = []
    for optimized in (False, True):
        cmd = [py, "-I"]
        if optimized:
            cmd.append("-O")
        cmd.extend((str(math), "--repo-root", str(root)))
        result = run_json(cmd, timeout=timeout)
        validate_math(result)
        math_results.append(result)
    require(math_results[0] == math_results[1], "normal and optimized math receipts disagree")
    return {
        "status": "PASS_COMPOSITE_CANDIDATE_E1_ONLY",
        "models": MODELS,
        "claim_files_checked": 16,
        "math_entry_runs": 2,
        "math_child_checks_claimed": 32,
        "evidence": "E1_ARTIFICIAL_ONLY",
        "production_adoption": "NOT_ESTABLISHED",
        "independent_data_validation": "NOT_RUN",
        "external_team_replication": "NOT_RUN",
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", type=Path, default=Path(__file__).resolve().parents[2])
    parser.add_argument("--node", default="node")
    args = parser.parse_args()
    try:
        output = verify(args.repo_root, node_executable=args.node)
    except (ValueError, OSError) as exc:
        print("COMPOSITE_ACCEPTANCE_FAIL: " + str(exc), file=sys.stderr)
        return 1
    print(json.dumps(output, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
