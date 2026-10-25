"""R164 frozen 72-world observation partition extension. Python standard library only."""
from __future__ import annotations
from collections import Counter, defaultdict
from fractions import Fraction as F
from pathlib import Path
import hashlib
import json

SOURCE = Path(__file__).resolve().parents[1] / "R164" / "R164_EXACT_RESULTS.json"
SOURCE_SHA256 = "ce27a70aee6ee82ca360efc93b12632c44f6bbd7a73b32bf1aaafc602df69f52"


def step(p: F, r: int, h: F, e: F) -> F:
    # Algebraic difference between weighted selection and random selection.
    salience_increment = F(r - 1) * p * (1 - p) / (1 + F(r - 1) * p)
    return (1 - e) * (p + h * salience_increment) + e / 2


def load_worlds() -> dict:
    raw = SOURCE.read_bytes()
    assert hashlib.sha256(raw).hexdigest() == SOURCE_SHA256, "frozen JSON changed"
    doc = json.loads(raw)
    assert doc["research_id"] == "R164" and len(doc["worlds"]) == 72
    worlds = {}
    for row in doc["worlds"]:
        ident = row["id"]
        p0 = F(row["initial_A"])
        r = row["salience_multiplier"]
        h, e = F(row["content_copy_strength"]), F(row["symmetric_reset"])
        frozen = tuple(F(point["A_frequency"]) for point in row["points"])
        path = [p0]
        for _ in range(4):
            path.append(step(path[-1], r, h, e))
        assert len(frozen) == 5 and tuple(path) == frozen
        assert all(0 <= p <= 1 for p in path)
        assert ident not in worlds
        worlds[ident] = {"p0": p0, "r": r, "h": h, "e": e, "path": tuple(path)}
    assert len(worlds) == 72
    assert len({(w["p0"], w["r"], w["h"], w["e"]) for w in worlds.values()}) == 72
    return worlds


def partitions(worlds: dict, points: int, known_e: bool) -> list[list[str]]:
    groups = defaultdict(list)
    for ident, w in worlds.items():
        key = (w["p0"], w["e"] if known_e else None, w["path"][:points])
        groups[key].append(ident)
    return sorted((sorted(v) for v in groups.values()), key=lambda x: x[0])


def summarize(parts: list[list[str]]) -> dict:
    size_counts = Counter(map(len, parts))
    return {
        "class_count": len(parts),
        "singleton_worlds": sum(len(p) == 1 for p in parts),
        "ambiguous_worlds": sum(len(p) for p in parts if len(p) > 1),
        "largest_class": max(map(len, parts)),
        "class_size_histogram": {str(k): size_counts[k] for k in sorted(size_counts)},
        "membership": parts,
    }


def result() -> dict:
    worlds = load_worlds()
    regimes = {}
    for points in (2, 3, 5):
        for known_e in (False, True):
            label = f"points_{points}_e_{'known' if known_e else 'unknown'}"
            regimes[label] = summarize(partitions(worlds, points, known_e))
    per_start = {}
    for p0 in sorted({w["p0"] for w in worlds.values()}):
        subset = {i: w for i, w in worlds.items() if w["p0"] == p0}
        per_start[str(p0)] = {
            str(points): summarize(partitions(subset, points, False))
            for points in (2, 3, 5)
        }
    nontrivial = {}
    for points in (2, 3, 5):
        nontrivial[str(points)] = [
            group for group in regimes[f"points_{points}_e_unknown"]["membership"]
            if len(group) > 1 and any(worlds[i]["r"] > 1 and worlds[i]["h"] > 0 for i in group)
        ]
    assert len(regimes["points_2_e_unknown"]["membership"]) == 39
    assert len(regimes["points_3_e_unknown"]["membership"]) == 40
    assert regimes["points_5_e_unknown"]["membership"] == regimes["points_3_e_unknown"]["membership"]
    return {
        "research_id": "R164",
        "scope": "E1_SYNTHETIC_INTERNAL_OBSERVATIONAL_PARTITIONS_ONLY",
        "frozen_source_sha256": SOURCE_SHA256,
        "world_count": len(worlds),
        "observed_state_count": 5 * len(worlds),
        "regimes": regimes,
        "per_start_unknown_e": per_start,
        "nontrivial_collisions": nontrivial,
        "new_E2": 0,
        "new_E3": 0,
        "external_replication": 0,
    }


if __name__ == "__main__":
    print(json.dumps(result(), ensure_ascii=False, sort_keys=True, indent=2))
