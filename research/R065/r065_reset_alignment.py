#!/usr/bin/env python3
"""R065 Phase C: audit author model reset dates against observed block timing.

No behavioral model is fitted here. For direct source verification, provide an
unmodified local copy of the author's objectives.py. Python 3.10+ standard lib.
"""
from __future__ import annotations
import argparse
import ast
import hashlib
import json
from pathlib import Path

AUTHOR_REPO = "arielevy8/obs-learning-fishing"
AUTHOR_SOURCE = "model_fitting/objectives.py"
AUTHOR_BLOB = "5e98133fa274ef2a112b24f6fdcd802d4f9d3eec"
KNOWN_RESETS = (23, 45, 67, 89, 111)
BLOCK_COUNT, BLOCK_LENGTH, FIRST_DAY = 8, 17, 1
CRITICAL_DAYS = tuple(4 + i * BLOCK_LENGTH for i in range(BLOCK_COUNT))


def git_blob_sha1(raw: bytes) -> str:
    return hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\x00" + raw).hexdigest()


def inspect_source(source: str) -> dict[int, tuple[int, ...]]:
    """Extract 'row[day] in [literal dates]' guards from each model AST."""
    tree = ast.parse(source)
    models: dict[int, tuple[int, ...]] = {}
    for node in tree.body:
        if not isinstance(node, ast.FunctionDef):
            continue
        if not node.name.startswith("model_") or not node.name.endswith("_objective"):
            continue
        mid = node.name[len("model_"):-len("_objective")]
        if not mid.isdecimal():
            continue
        guards = []
        for part in ast.walk(node):
            if not isinstance(part, ast.Compare) or len(part.ops) != 1:
                continue
            if not isinstance(part.ops[0], ast.In) or len(part.comparators) != 1:
                continue
            left = part.left
            if (isinstance(left, ast.Subscript)
                    and isinstance(left.value, ast.Name)
                    and left.value.id == "row"
                    and isinstance(left.slice, ast.Constant)
                    and left.slice.value == "day"
                    and isinstance(part.comparators[0], (ast.List, ast.Tuple))):
                vals = part.comparators[0].elts
                if not vals or any(not isinstance(v, ast.Constant) or type(v.value) is not int for v in vals):
                    raise ValueError(f"Nonliteral reset date in model {mid}")
                guards.append(tuple(v.value for v in vals))
        if len(guards) != 1:
            raise ValueError(f"Expected exactly one literal reset guard in model {mid}; found {len(guards)}")
        models[int(mid)] = guards[0]
    if set(models) != set(range(1, 8)):
        raise ValueError("Expected exactly seven model objectives")
    return models


def inspect_verified_file(path: Path) -> dict[int, tuple[int, ...]]:
    raw = path.read_bytes()
    if git_blob_sha1(raw) != AUTHOR_BLOB:
        raise ValueError("FAIL CLOSED: upstream objectives.py Git blob SHA1 mismatch")
    return inspect_source(raw.decode("utf-8"))


def audit_alignment(models: dict[int, tuple[int, ...]], blocks: int = BLOCK_COUNT,
                    block_length: int = BLOCK_LENGTH) -> dict:
    if blocks < 2 or block_length < 2:
        raise ValueError("Invalid positive multi-block design")
    expected = tuple(FIRST_DAY + j * block_length for j in range(1, blocks))
    critical = tuple(FIRST_DAY + 3 + j * block_length for j in range(blocks))
    if set(models) != set(range(1, 8)):
        raise ValueError("Missing or extra model objective")
    per_model = {}
    for mid, dates in sorted(models.items()):
        if not dates or len(set(dates)) != len(dates):
            raise ValueError("Empty or duplicate model reset dates")
        given = set(dates)
        per_model[str(mid)] = {
            "source_reset_days": list(dates),
            "observed_internal_block_starts": list(expected),
            "matched_block_start_days": sorted(given & set(expected)),
            "unexpected_resets": sorted(given - set(expected)),
            "unreset_block_starts": sorted(set(expected) - given),
            "critical_days_reset_by_source": sorted(given & set(critical)),
        }
    return {
        "upstream_repo": AUTHOR_REPO, "upstream_source": AUTHOR_SOURCE,
        "upstream_source_git_blob_sha1": AUTHOR_BLOB,
        "comparison_type": "SOURCE_RESET_GUARD_VS_OBSERVED_EXPERIMENT_BLOCK_BOUNDARY",
        "observed_design": {"blocks": blocks, "days_per_block": block_length,
                            "first_day": FIRST_DAY, "critical_days": list(critical),
                            "internal_block_starts": list(expected)},
        "models": per_model,
        "interpretation": "Source reset guards differ from observed block starts; model fits and publication results were NOT rerun.",
    }


def fresh_state_two_action_probabilities(
    transition: tuple[tuple[float, ...], ...],
    available: tuple[int, int] = (0, 1),
    inverse_temperature: float = 10.0,
    emulation_weight: float = 0.37,
) -> dict:
    """Diagnostic consequence of resetting each author model before a play trial.

    This is a structural calculation, not a fit of the original seven functions.
    Assumes two available boats, three outcomes, uniform token prior,
    zero initialized imitation values and absent last-observed action.
    """
    import math
    if len(transition) != 3 or any(len(row) != 3 for row in transition):
        raise ValueError("A three-boat, three-token matrix is required")
    if any(not all(math.isfinite(v) and v >= 0 for v in row) or
           abs(sum(row) - 1.0) > 1e-10 for row in transition):
        raise ValueError("Invalid normalized boat transition rows")
    if len(set(available)) != 2 or any(j not in (0, 1, 2) for j in available):
        raise ValueError("Exactly two distinct boats required")
    if (not math.isfinite(inverse_temperature) or inverse_temperature < 0 or
            not 0 <= emulation_weight <= 1):
        raise ValueError("Invalid model parameters")
    # Each boat has expected value 1/3 under a uniform token prior,
    # provided its three transition probabilities sum to one.
    expected = [sum(transition[j][t] / 3 for t in range(3)) for j in available]
    logits = [inverse_temperature * (v - max(expected)) for v in expected]
    exps = [math.exp(x) for x in logits]
    emulation = [x / sum(exps) for x in exps]
    imitation = [0.5, 0.5]
    copy_last = [0.5, 0.5]  # last observed action is None after reset
    mixed = [emulation_weight * e + (1-emulation_weight) * i
             for e, i in zip(emulation, imitation)]
    return {"emulation": emulation, "imitation": imitation,
            "copy_last": copy_last, "mixture": mixed,
            "expected_boat_values": expected}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, required=True, help="unmodified author objectives.py")
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    report = audit_alignment(inspect_verified_file(args.source))
    args.output.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({"status": "PASS", "source_git_blob": AUTHOR_BLOB,
                      "models": len(report["models"])}))


if __name__ == "__main__":
    main()
