#!/usr/bin/env python3
"""R313: exact one-step Axelrod kernel on a fixed 3-node path, F=q=2.

Only synthetic E1. No claim about long-run clustering, observed humans, or causal evidence.
Run: python research/R313/r313_exact_axelrod.py --test
     python research/R313/r313_exact_axelrod.py --audit
"""
from __future__ import annotations
import argparse
import csv
import io
import json
from collections import defaultdict
from fractions import Fraction
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parent
CSV_PATH = ROOT / "R313_ALL_512_ORIGINAL_FEATURE_SOURCE_ATOMS.csv"
JSON_PATH = ROOT / "R313_EXACT_64_WORLD_ONE_STEP_RESULTS.json"
DIRECTED = ((0, 1), (1, 0), (1, 2), (2, 1))
UNDIRECTED = ((0, 1), (1, 2))
FIELDS = ("world", "active", "neighbor", "feature", "active_trait",
          "neighbor_trait", "matches", "differences", "selection_weight",
          "conditional_copy_probability", "unconditional_copy_probability", "next_world")

def state(world: int) -> tuple[int, ...]:
    assert 0 <= world < 64
    return tuple(int(x) for x in f"{world:06b}")

def encode(bits: tuple[int, ...]) -> int:
    assert len(bits) == 6 and all(x in (0, 1) for x in bits)
    return int("".join(str(x) for x in bits), 2)

def matches(bits: tuple[int, ...], a: int, b: int) -> int:
    return sum(bits[2*a + k] == bits[2*b + k] for k in (0, 1))

def weight(a: int) -> Fraction:
    return Fraction(1, 6) if a == 1 else Fraction(1, 3)

def copy_probability(bits: tuple[int, ...], a: int, b: int, f: int) -> Fraction:
    m = matches(bits, a, b)
    d = 2 - m
    if not d or bits[2*a + f] == bits[2*b + f]:
        return Fraction(0)
    return Fraction(m, 2*d)

def copied(bits: tuple[int, ...], a: int, b: int, f: int) -> tuple[int, ...]:
    new = list(bits)
    new[2*a + f] = bits[2*b + f]
    return tuple(new)

def is_absorbing(bits: tuple[int, ...]) -> bool:
    return all(matches(bits, a, b) in (0, 2) for a, b in UNDIRECTED)

def generate() -> tuple[list[dict[str, str]], dict]:
    atoms: list[dict[str, str]] = []
    worlds = []
    for world in range(64):
        bits = state(world)
        distribution: dict[int, Fraction] = defaultdict(Fraction)
        distribution[world] = Fraction(1)
        for a, b in DIRECTED:
            for f in (0, 1):
                prob = copy_probability(bits, a, b, f)
                weighted = weight(a)*prob
                target = encode(copied(bits, a, b, f)) if prob else world
                atoms.append(dict(zip(FIELDS, map(str, (
                    world, a, b, f, bits[2*a+f], bits[2*b+f], matches(bits, a, b),
                    2-matches(bits, a, b), weight(a), prob, weighted, target)))))
                if weighted:
                    distribution[world] -= weighted
                    distribution[target] += weighted
        assert sum(distribution.values()) == 1
        assert all(p >= 0 for p in distribution.values())
        worlds.append({
            "world": world,
            "state": f"{world:06b}",
            "absorbing": is_absorbing(bits),
            "next_world_probabilities": [
                {"world": k, "probability": str(p)}
                for k, p in sorted(distribution.items()) if p
            ],
        })
    return atoms, {
        "schema": "r313_axelrod_three_site_two_binary_feature_exact_e1_v1",
        "original_catalogue_id": "04-014",
        "source_scope": "SYNTHETIC_EXACT_E1_ONLY",
        "world_count": 64,
        "directed_event_count": 256,
        "potential_feature_source_count": 512,
        "absorbing_world_count": sum(x["absorbing"] for x in worlds),
        "positive_copy_atom_count": sum(Fraction(x["unconditional_copy_probability"]) > 0 for x in atoms),
        "worlds": worlds,
    }

def csv_text(rows: list[dict[str, str]]) -> str:
    out = io.StringIO(newline="")
    writer = csv.DictWriter(out, fieldnames=FIELDS, lineterminator="\n")
    writer.writeheader()
    writer.writerows(rows)
    return out.getvalue()

def verify_archive() -> None:
    actual_rows = list(csv.DictReader(CSV_PATH.open(encoding="utf-8", newline="")))
    actual_json = json.loads(JSON_PATH.read_text(encoding="utf-8"))
    rows, result = generate()
    if actual_rows != rows:
        raise AssertionError("archived 512 feature atoms differ from original formula")
    if actual_json != result:
        raise AssertionError("archived 64 world transition probabilities differ")
    assert len(rows) == 512 and len(result["worlds"]) == 64
    assert result["absorbing_world_count"] == 16
    assert result["positive_copy_atom_count"] == 128

class ExactAxelrodTests(unittest.TestCase):
    def test_00_world_state(self): self.assertEqual(state(0), (0,)*6)
    def test_63_world_state(self): self.assertEqual(state(63), (1,)*6)
    def test_encode_decode(self):
        for w in range(64): self.assertEqual(encode(state(w)), w)
    def test_num_directed_pairs(self): self.assertEqual(len(DIRECTED), 4)
    def test_end_activation_weight(self): self.assertEqual(weight(0), Fraction(1, 3))
    def test_mid_activation_weight(self): self.assertEqual(weight(1), Fraction(1, 6))
    def test_directed_weights_sum(self): self.assertEqual(sum(weight(a) for a,b in DIRECTED), 1)
    def test_identity_matches_two(self): self.assertEqual(matches(state(0), 0, 1), 2)
    def test_disjoint_matches_zero(self): self.assertEqual(matches(state(3), 1, 2), 0)
    def test_half_similar(self): self.assertEqual(matches(state(1), 1, 2), 1)
    def test_disjoint_never_copies(self):
        b = state(3)
        self.assertEqual([copy_probability(b, 1, 2, f) for f in (0, 1)], [0, 0])
    def test_identical_never_copies(self):
        b = state(0)
        self.assertEqual([copy_probability(b, 0, 1, f) for f in (0, 1)], [0, 0])
    def test_half_similar_copy(self):
        b = state(1)
        self.assertEqual(copy_probability(b, 1, 2, 1), Fraction(1, 2))
    def test_matching_feature_has_zero_copy(self):
        b = state(1)
        self.assertEqual(copy_probability(b, 1, 2, 0), 0)
    def test_copy_changes_active_only(self):
        b = state(1); t = copied(b, 1, 2, 1)
        self.assertEqual(t, (0, 0, 0, 1, 0, 1))
    def test_neighbour_unmodified(self):
        b = state(1); t = copied(b, 1, 2, 1)
        self.assertEqual(t[4:], b[4:])
    def test_active_neighbor_similarity_gains_one(self):
        for w in range(64):
            b = state(w)
            for a, n in DIRECTED:
                for f in (0, 1):
                    if copy_probability(b, a, n, f):
                        self.assertEqual(matches(copied(b,a,n,f),a,n), matches(b,a,n)+1)
    def test_all_512_atoms(self): self.assertEqual(len(generate()[0]), 512)
    def test_unique_atom_keys(self):
        atoms,_ = generate()
        self.assertEqual(len({(r["world"],r["active"],r["neighbor"],r["feature"]) for r in atoms}), 512)
    def test_all_worlds(self): self.assertEqual(len(generate()[1]["worlds"]), 64)
    def test_positive_atoms(self): self.assertEqual(generate()[1]["positive_copy_atom_count"], 128)
    def test_absorbing_count(self): self.assertEqual(generate()[1]["absorbing_world_count"], 16)
    def test_all_probabilities_sum_one(self):
        for record in generate()[1]["worlds"]:
            self.assertEqual(sum(Fraction(x["probability"]) for x in record["next_world_probabilities"]), 1)
    def test_absorbing_is_point_mass(self):
        for record in generate()[1]["worlds"]:
            if record["absorbing"]:
                self.assertEqual(record["next_world_probabilities"], [{"world":record["world"],"probability":"1"}])
    def test_mixed_world_can_change(self):
        rec = generate()[1]["worlds"][1]
        self.assertTrue(any(x["world"]!=1 for x in rec["next_world_probabilities"]))
    def test_one_other_edge_can_lose_similarity(self):
        b = state(1); self.assertEqual(matches(b, 0, 1), 2)
        self.assertEqual(matches(copied(b,1,2,1), 0, 1), 1)
    def test_unconditional_mid_copy(self):
        b = state(1)
        self.assertEqual(weight(1)*copy_probability(b,1,2,1), Fraction(1,12))
    def test_conditional_never_above_one(self):
        rows,_ = generate()
        self.assertTrue(all(0 <= Fraction(r["conditional_copy_probability"]) <= 1 for r in rows))
    def test_csv_json_archive_replay(self): verify_archive()

if __name__ == "__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("--test", action="store_true")
    parser.add_argument("--audit", action="store_true")
    args=parser.parse_args()
    if args.test:
        suite=unittest.defaultTestLoader.loadTestsFromTestCase(ExactAxelrodTests)
        result=unittest.TextTestRunner(verbosity=1).run(suite)
        if not result.wasSuccessful(): raise SystemExit(1)
    elif args.audit:
        verify_archive()
        print("R313 exact source audit PASS: 64 worlds, 256 directed events, 512 atoms; 16 absorbing worlds; 128 positive atoms")
    else:
        print(json.dumps(generate()[1], ensure_ascii=False, indent=2))
