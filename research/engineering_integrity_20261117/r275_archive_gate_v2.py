#!/usr/bin/env python3
"""Opt-in E1 archival revalidation; never routes a workflow or production caller.

Authenticate frozen bytes, replace the exact original 18 assert conditions with
explicit failures in memory, and reuse the historical Fraction/K-count math.
The historical checker and its optimized-mode defect remain unchanged.
"""
import argparse
import ast
import hashlib
import json
from pathlib import Path
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "research/evidence_audit/b_r275_s71_independent_gate_20261030.py"
RESULTS = ROOT / "research/validation/R275_S71_EXACT_RESULTS_2026-10-30.json"
ROWS = ROOT / "research/validation/R275_S71_ALL_3072_NOISY_PAIR_ROWS_2026-10-30.csv"
PINS = {
    "source": (3109, "d6da1a90f84a81a5a0c1a9db252cdb4b977ffa47903a0929ed5281bc604a39ed"),
    "results_json": (2577, "632da3835df48660dac38d9e69d8e0679382f34d1de8b38f487ad51efc120532"),
    "rows_csv": (159435, "71f25b29b294dc8827ba2803e80ae89c446550134d0009ea4ae7b7c5cef88fab"),
}
GUARD_COUNT = 18
EXPECTED = {"source_rows": 3072, "epsilons": 4, "confusion_cells": 36,
            "MAP_values": 4, "status": "PASS"}


class ArchiveGateError(ValueError):
    """The bounded archival check must stop without a passing receipt."""


def _require(condition, message):
    if not condition:
        raise ArchiveGateError("R275_ARCHIVE_V2:" + message)


def _authenticate(raw, label):
    size, digest = PINS[label]
    _require(len(raw) == size and hashlib.sha256(raw).hexdigest() == digest,
             "IDENTITY:" + label)
    return raw


def _read_pinned(path, label):
    # Read one bounded snapshot; never authenticate a path then reopen its bytes.
    with Path(path).open("rb") as stream:
        raw = stream.read(PINS[label][0] + 1)
    return _authenticate(raw, label)


def _build_checker(source):
    """Private semantic engine; public archival validation also pins input bytes.

    Pinning the complete original source authenticates every condition and all
    mathematical expressions. Only Assert nodes are replaced; their original
    condition and optional duplicate-source message are retained verbatim in AST.
    """
    _authenticate(source, "source")
    tree = ast.parse(source, filename=str(SOURCE))
    original_guards = [node for node in ast.walk(tree) if isinstance(node, ast.Assert)]
    _require(len(original_guards) == GUARD_COUNT, "GUARD_COUNT")

    class ExplicitGuards(ast.NodeTransformer):
        def visit_Assert(self, node):
            message = node.msg if node.msg is not None else ast.Constant(
                "original_guard_line_" + str(node.lineno))
            replacement = ast.Expr(value=ast.Call(
                func=ast.Name(id="_archive_require", ctx=ast.Load()),
                args=[node.test, message], keywords=[]))
            return ast.copy_location(replacement, node)

    tree = ast.fix_missing_locations(ExplicitGuards().visit(tree))
    _require(not any(isinstance(node, ast.Assert) for node in ast.walk(tree)),
             "ASSERT_REMAINS")
    namespace = {"__name__": "_r275_authenticated_archival_engine",
                 "_archive_require": _require}
    exec(compile(tree, str(SOURCE) + "[explicit archival guards]", "exec"), namespace)
    _require(callable(namespace.get("check")), "CHECK_ENTRY")
    return namespace["check"]


def validate_archive(results_path=RESULTS, rows_path=ROWS):
    """Accept only the pinned frozen archive, using authenticated private copies."""
    source = _read_pinned(SOURCE, "source")
    results = _read_pinned(results_path, "results_json")
    rows = _read_pinned(rows_path, "rows_csv")
    check = _build_checker(source)
    with tempfile.TemporaryDirectory(prefix="r275-archive-v2-") as temporary:
        snapshot = Path(temporary)
        result_copy, rows_copy = snapshot / "results.json", snapshot / "rows.csv"
        result_copy.write_bytes(results)
        rows_copy.write_bytes(rows)
        receipt = check(result_copy, rows_copy)
    _require(receipt == EXPECTED, "RECEIPT")
    return {
        "research_id": "R275_S71", "evidence": "E1_ARTIFICIAL_NONBLIND",
        "new_E2": 0, "new_E3": 0, "status": "PASS_BOUNDED_ARCHIVE_REVALIDATION",
        "scope": "opt_in_engineering_archive_only", "explicit_guards": GUARD_COUNT,
        "production_ready": False, "workflow_adopted": False,
        "legacy_callable": "STILL_BLOCKED_FOR_PRODUCTION_PENDING_OWNER_APPROVED_ROUTING",
        "scientific_acceptance": "UNCHANGED", "archive_receipt": receipt,
        "authenticated_sha256": {label: pin[1] for label, pin in PINS.items()},
    }


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("results_json", nargs="?", type=Path, default=RESULTS)
    parser.add_argument("rows_csv", nargs="?", type=Path, default=ROWS)
    args = parser.parse_args(argv)
    try:
        receipt = validate_archive(args.results_json, args.rows_csv)
    except Exception as error:
        print("BLOCKED " + type(error).__name__ + ": " + str(error), file=sys.stderr)
        return 1
    print(json.dumps(receipt, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
