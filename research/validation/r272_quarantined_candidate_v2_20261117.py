#!/usr/bin/env python3
"""R272 proposed quarantined local acceptance runner, version 2.

Engineering-only replay of previously archived R272 scientific controls.
Zero writes to the original checkout. Trust boundary: only SHA-pinned
preimages are copied into a private temporary tree. Unpinned neighboring
Python source files and PYTHONPATH are excluded before child execution.

This is an unadopted experimental candidate. It does not change the frozen
R272 protocol, archived science evidence, or the production CI workflow.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile

CANDIDATE = "research/validation/r272_single_entrypoint_failclosed_20261102.py"
CANDIDATE_BLOB = "f33e4e7e544560d65342a899606311d169e4d122"
ORIGINAL = "research/R272/r272_exact_train_test_prediction.py"
FREEZE = (
    "protocols/"
    "R272_OUT_OF_SAMPLE_9_BERNOULLI_WORLDS_576_FULL_SOURCE_"
    "PRESCORE_FREEZE_2026-10-23.md"
)
WRAPPER = "research/validation/r272_preimage_first_readonly_gate_20261102.py"
NEGATIVE = (
    "research/validation/"
    "r272_pinned_native_replay_and_preimage_negative_20261102.py"
)
ZIP = "research/validation/R272_P0_FAILCLOSED_CANDIDATE_20261102.zip"
BLOBS = {
    CANDIDATE: CANDIDATE_BLOB,
    ORIGINAL: "13843eecf2f9f05c19ee5545bdb224f58313f367",
    FREEZE: "9fbdb0078a58c4a9c0a548643227e30da5731119",
    WRAPPER: "8722fd4388421e3b1f77c6648b4ed1b38088c4b0",
    NEGATIVE: "9b8a5a566b7f48c7e72ba34505d49eebe3a94b44",
    "research/R272/R272_ALL_576_ORIGINAL_TRAIN_AND_TEST_SOURCES.csv":
        "8fbbc73d239765f5c66395af1bcf9cf7a8df1f41",
    "research/R272/R272_EXACT_RESULTS.json":
        "db3ca11ae224af52c2caf385c898e24aaa0cc54b",
    "research/R272/R272_MACHINE_RECEIPT.json":
        "85d36858911a7eb79c73c607cddf45ea88852a60",
}
ZIP_SHA256 = "f23b04706b60ac70bdbee6f051a74551779fb9d9a9b9af08c96cda345b055151"
PYTHON_MODES = ("normal", "optimized", "double_optimized")


class R272IntegrityError(ValueError):
    pass


def require(ok: bool, key: str) -> None:
    if ok is not True:
        raise R272IntegrityError("R272_QUARANTINE_" + key)


def git_blob(raw: bytes) -> str:
    return hashlib.sha1(
        b"blob " + str(len(raw)).encode("ascii") + b"\0" + raw
    ).hexdigest()


def regular_no_symlink(root: Path, name: str) -> Path:
    path = root / name
    require(path.is_file() and not path.is_symlink(), "MISSING_OR_LINK_" + name)
    # Reject a symlink in any path component, including parent directories.
    for parent in (path, *path.parents):
        if parent == root:
            break
        require(not parent.is_symlink(), "LINKED_ANCESTOR_" + name)
    return path


def authenticated_source(root: Path) -> dict[str, bytes]:
    original = {}
    for name, digest in BLOBS.items():
        data = regular_no_symlink(root, name).read_bytes()
        require(git_blob(data) == digest, "SOURCE_IDENTITY_MISMATCH_" + name)
        original[name] = data
    zip_data = regular_no_symlink(root, ZIP).read_bytes()
    require(hashlib.sha256(zip_data).hexdigest() == ZIP_SHA256, "ZIP_IDENTITY")
    original[ZIP] = zip_data
    return original


def trusted_child_environment() -> dict[str, str]:
    # Propagates to the historical candidate's nested child processes.
    # Remove all operator-provided PYTHON* overrides before invocation.
    env = {k: v for k, v in os.environ.items()
           if not k.upper().startswith("PYTHON")}
    env.update({
        "PYTHONSAFEPATH": "1",
        "PYTHONNOUSERSITE": "1",
        "PYTHONDONTWRITEBYTECODE": "1",
        "PYTHONHASHSEED": "0",
    })
    return env


def verify_modes(record: dict) -> None:
    require(record.get("status") == "PASS", "CANDIDATE_PASS")
    require(record.get("scope") == "INTERNAL_NONBLIND_ARTIFICIAL_E1",
            "EVIDENCE_SCOPE")
    require(record.get("workflow_adopted") is False, "PRODUCTION_CLAIM")
    require(record.get("actions_executed") is False, "NESTED_ACTION_CLAIM")
    require(record.get("archive_bytes_preserved") is True, "ARCHIVE_CLAIM")
    modes = record.get("modes")
    require(isinstance(modes, list) and len(modes) == 3, "MODE_COVERAGE")
    for expected, item in zip(PYTHON_MODES, modes):
        require(item.get("mode") == expected, "MODE_" + expected)
        require(item.get("preimage") == "PASS", "PREIMAGE_" + expected)
        require(item.get("isolated_regeneration") == "PASS",
                "REGEN_" + expected)
        require(item.get("native_negatives") == 15,
                "NEGATIVE_" + expected)
        require(item.get("original_tests_exit") == 0,
                "NATIVE_TEST_" + expected)


def audit(root: Path) -> dict:
    root = root.resolve(strict=True)
    original = authenticated_source(root)
    with tempfile.TemporaryDirectory(prefix="r272_quarantined_v2_") as td:
        sealed = Path(td)
        for name, data in original.items():
            out = sealed / name
            out.parent.mkdir(parents=True, exist_ok=True)
            out.write_bytes(data)
        # The fixed finite allowlist is also the complete set of source files
        # reachable in the private test tree. No sibling json.py can enter.
        present = {
            str(p.relative_to(sealed))
            for p in sealed.rglob("*")
            if p.is_file()
        }
        require(present == set(original), "SEALED_TREE_EXTRA_SOURCE")
        require(authenticated_source(sealed) == original,
                "SEALED_INPUT_IDENTITY")
        cmd = [
            sys.executable, "-B", "-I", "-S",
            str(sealed / CANDIDATE), "--root", str(sealed),
        ]
        result = subprocess.run(
            cmd, cwd=sealed, env=trusted_child_environment(),
            capture_output=True, text=True, shell=False, timeout=300,
            check=False,
        )
        require(result.returncode == 0, "INNER_CANDIDATE_EXIT")
        try:
            record = json.loads(result.stdout)
        except json.JSONDecodeError as exc:
            raise R272IntegrityError("R272_QUARANTINE_INVALID_JSON") from exc
        require(isinstance(record, dict), "CANDIDATE_JSON_OBJECT")
        verify_modes(record)
        require(authenticated_source(sealed) == original,
                "SEALED_ARCHIVED_SOURCE_WAS_MODIFIED")
        extra = {
            str(p.relative_to(sealed))
            for p in sealed.rglob("*") if p.is_file()
        } - set(original)
        require(not extra, "SEALED_UNEXPECTED_SIDE_EFFECTS")
    require(authenticated_source(root) == original,
            "ORIGINAL_CHECKOUT_WAS_MODIFIED")
    return {
        "status": "PASS_BOUNDED_QUARANTINED_R272_CANDIDATE",
        "scientific_scope": "INTERNAL_NONBLIND_FINITE_ARTIFICIAL_E1",
        "archive_source_identities_pinned": len(BLOBS),
        "historical_gate_zip_sha256_pinned": True,
        "complete_allowlist_files": len(original),
        "untrusted_neighbor_modules_excluded": True,
        "python_environment_isolated": True,
        "ordinary_optimized_double_optimized": list(PYTHON_MODES),
        "original_native_tests_each_mode": 83,
        "native_negative_controls_each_mode": 15,
        "archive_modified": False,
        "production_workflow_adopted": False,
        "frozen_science_modified": False,
        "external_team_replication": False,
        "new_E2": 0,
        "new_E3": 0,
    }


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--root", required=True, type=Path)
    args = p.parse_args()
    print(json.dumps(audit(args.root), sort_keys=True))


if __name__ == "__main__":
    try:
        main()
    except (R272IntegrityError, OSError, RuntimeError,
            subprocess.TimeoutExpired) as e:
        raise SystemExit("FAIL: " + str(e)) from e
