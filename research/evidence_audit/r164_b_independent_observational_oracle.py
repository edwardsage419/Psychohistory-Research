"""Independent R164 E1 oracle. Reads original frozen JSON, never imports R main code."""
from __future__ import annotations
from collections import defaultdict
from fractions import Fraction as F
from pathlib import Path
import hashlib
import json

ROOT = Path(__file__).resolve().parents[1]
FROZEN = ROOT / "R164" / "R164_EXACT_RESULTS.json"
MAIN_RECEIPT = ROOT / "validation" / "R164_OBSERVATIONAL_PARTITIONS_EXACT_RECEIPT_2026-10-25.json"
SOURCE_SHA256 = "ce27a70aee6ee82ca360efc93b12632c44f6bbd7a73b32bf1aaafc602df69f52"


def independent_step(p: F, r: int, h: F, e: F) -> F:
    # Three explicit channels: random copy, weighted copy, symmetric replacement.
    mass_a = r * p
    mass_b = 1 - p
    selected_a = mass_a / (mass_a + mass_b)
    random_copy_a = (1 - h) * p
    weighted_copy_a = h * selected_a
    return (1 - e) * (random_copy_a + weighted_copy_a) + e * F(1, 2)


def read_worlds() -> dict:
    raw = FROZEN.read_bytes()
    assert hashlib.sha256(raw).hexdigest() == SOURCE_SHA256
    original = json.loads(raw)
    assert len(original["worlds"]) == 72
    worlds = {}
    for w in original["worlds"]:
        ident = w["id"]
        p = F(w["initial_A"])
        r, h, e = w["salience_multiplier"], F(w["content_copy_strength"]), F(w["symmetric_reset"])
        trajectory = [p]
        for _ in range(4):
            p = independent_step(p, r, h, e)
            trajectory.append(p)
        assert tuple(trajectory) == tuple(F(z["A_frequency"]) for z in w["points"])
        assert ident not in worlds
        worlds[ident] = (trajectory, r, h, e)
    return worlds


def signature(worlds: dict, points: int, known_e: bool, only_start: F | None = None) -> list[list[str]]:
    classes = defaultdict(list)
    for ident, (path, r, h, e) in worlds.items():
        if only_start is not None and path[0] != only_start:
            continue
        key = (path[0], e if known_e else None, tuple(path[:points]))
        classes[key].append(ident)
    return sorted((sorted(v) for v in classes.values()), key=lambda z: z[0])


def audit() -> dict:
    worlds = read_worlds()
    receipt = json.loads(MAIN_RECEIPT.read_text(encoding="utf-8"))
    assert receipt["world_count"] == len(worlds) == 72
    checked_regimes = 0
    for points in (2, 3, 5):
        for known_e in (False, True):
            label = f"points_{points}_e_{'known' if known_e else 'unknown'}"
            assert signature(worlds, points, known_e) == receipt["regimes"][label]["membership"]
            checked_regimes += 1
    checked_starts = 0
    for start in (F(1, 5), F(2, 5), F(3, 5), F(4, 5)):
        for points in (2, 3, 5):
            assert signature(worlds, points, False, start) == receipt["per_start_unknown_e"][str(start)][str(points)]["membership"]
            checked_starts += 1

    mutant_r_detected = 0
    mutant_e_detected = 0
    for path, r, h, e in worlds.values():
        p = path[0]
        if r > 1 and h > 0:
            mutant = independent_step(p, 1, h, e)
            if mutant != path[1]:
                mutant_r_detected += 1
        if e > 0:
            mutant = independent_step(p, r, h, F(0))
            if mutant != path[1]:
                mutant_e_detected += 1
    assert mutant_r_detected > 0 and mutant_e_detected > 0
    return {
        "status": "PASS_INTERNAL_INDEPENDENT_METHOD_E1",
        "worlds_checked": 72,
        "frozen_states_checked": 360,
        "regime_signatures_checked": checked_regimes,
        "per_start_signatures_checked": checked_starts,
        "salience_omission_mutant_detected": mutant_r_detected,
        "replacement_omission_mutant_detected": mutant_e_detected,
        "new_E2": 0,
        "new_E3": 0,
        "external_replication": 0,
    }


if __name__ == "__main__":
    print(json.dumps(audit(), ensure_ascii=False, sort_keys=True, indent=2))
