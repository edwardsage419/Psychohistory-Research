#!/usr/bin/env python3
"""R319 finite two-point mixed logit. Synthetic rational source, no human data."""
from __future__ import annotations
import argparse
import csv
import io
import json
import unittest
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / "R319_ALL_84_ORIGINAL_CONDITIONAL_MIXTURE_SOURCE_ATOMS.csv"
RESULT = ROOT / "R319_EXACT_15_MIXED_LOGIT_WORLDS.json"
SETS = ((0, 1), (0, 1, 2), (0, 1, 1), (0, 2, 1), (0, 2, 2))
QS = (Fraction(1, 4), Fraction(1, 2), Fraction(3, 4))
BETAS = (-1, 1)
FIELDS = ("world_id", "choice_set_id", "features", "q_plus", "beta",
          "alternative_index", "feature_x", "conditional_probability",
          "mixing_mass", "weighted_contribution", "mixed_probability")

def power_two(k):
    if type(k) is not int:
        raise ValueError("integer exponent required")
    return Fraction(2 ** k, 1) if k >= 0 else Fraction(1, 2 ** (-k))

def conditional(beta, features):
    if type(beta) is not int or beta not in BETAS:
        raise ValueError("invalid coefficient")
    if not features or any(type(x) is not int for x in features):
        raise ValueError("invalid features")
    terms = [power_two(beta * x) for x in features]
    denom = sum(terms, Fraction(0))
    return tuple(t / denom for t in terms)

def mixed(q, features):
    if not isinstance(q, Fraction) or not 0 <= q <= 1:
        raise ValueError("invalid mixing mass")
    pos = conditional(1, features)
    neg = conditional(-1, features)
    return tuple(q * a + (1-q) * b for a, b in zip(pos, neg))

def generate():
    rows = []
    worlds = []
    for s, xs in enumerate(SETS):
        for q in QS:
            world_id = len(worlds)
            marg = mixed(q, xs)
            worlds.append({"world_id": world_id, "choice_set_id": f"S{s}",
                           "features": list(xs), "q_plus": str(q),
                           "marginal_probabilities": [str(p) for p in marg]})
            for beta in BETAS:
                mass = q if beta == 1 else 1-q
                for j, (x, prob) in enumerate(zip(xs, conditional(beta, xs))):
                    rows.append(dict(zip(FIELDS, map(str, (
                        world_id, f"S{s}", "|".join(map(str, xs)), q, beta,
                        j, x, prob, mass, mass * prob, marg[j])))))
    return rows, {"schema": "r319_finite_two_point_mixed_logit_e1_v1",
                  "original_catalogue_id": "01-007",
                  "synthetic_only": True, "original_source_atoms": len(rows),
                  "choice_worlds": len(worlds),
                  "marginal_alternative_probabilities":
                      sum(len(w["features"]) for w in worlds),
                  "worlds": worlds}

def csv_text(rows):
    buf = io.StringIO(newline="")
    writer = csv.DictWriter(buf, fieldnames=FIELDS, lineterminator="\n")
    writer.writeheader()
    writer.writerows(rows)
    return buf.getvalue()

def json_text(result):
    return json.dumps(result, ensure_ascii=False, indent=2) + "\n"

def check_source_text(csv_data, json_data):
    rows, results = generate()
    if csv_data != csv_text(rows):
        raise AssertionError("R319 source CSV bytes differ from frozen grid")
    if json.loads(json_data) != results:
        raise AssertionError("R319 result JSON differs from frozen grid")
    return True

def replay():
    return check_source_text(SOURCE.read_text(encoding="utf-8"),
                             RESULT.read_text(encoding="utf-8"))

class FiniteMixedLogitTests(unittest.TestCase):
    def test_01_choice_sets(self): self.assertEqual(len(SETS), 5)
    def test_02_masses(self): self.assertEqual(QS, (Fraction(1,4), Fraction(1,2), Fraction(3,4)))
    def test_03_world_count(self): self.assertEqual(len(generate()[1]["worlds"]), 15)
    def test_04_atom_count(self): self.assertEqual(len(generate()[0]), 84)
    def test_05_marginal_count(self): self.assertEqual(generate()[1]["marginal_alternative_probabilities"], 42)
    def test_06_unique_atoms(self):
        r,_ = generate()
        self.assertEqual(len({(x["world_id"],x["beta"],x["alternative_index"]) for x in r}),84)
    def test_07_conditional_sum(self):
        for xs in SETS:
            for b in BETAS: self.assertEqual(sum(conditional(b,xs)),1)
    def test_08_marginal_sum(self):
        for xs in SETS:
            for q in QS: self.assertEqual(sum(mixed(q,xs)),1)
    def test_09_strict_positive(self):
        for xs in SETS:
            for q in QS: self.assertTrue(all(x>0 for x in mixed(q,xs)))
    def test_10_components(self):
        for xs in SETS:
            for q in QS:
                for j,p in enumerate(mixed(q,xs)):
                    self.assertEqual(p,q*conditional(1,xs)[j]+(1-q)*conditional(-1,xs)[j])
    def test_11_source_mass(self):
        for r in generate()[0]:
            q=Fraction(r["q_plus"])
            self.assertEqual(Fraction(r["mixing_mass"]),q if r["beta"]=="1" else 1-q)
    def test_12_source_contribution(self):
        for r in generate()[0]:
            self.assertEqual(Fraction(r["weighted_contribution"]),
                             Fraction(r["mixing_mass"])*Fraction(r["conditional_probability"]))
    def test_13_binary_witness(self):
        self.assertEqual(mixed(Fraction(1,2),SETS[0]),(Fraction(1,2),Fraction(1,2)))
    def test_14_triple_witness(self):
        self.assertEqual(mixed(Fraction(1,2),SETS[1]),
                         (Fraction(5,14),Fraction(2,7),Fraction(5,14)))
    def test_15_mixed_iia_witness(self):
        a=mixed(Fraction(1,2),SETS[0]); b=mixed(Fraction(1,2),SETS[1])
        self.assertEqual((a[0]/a[1],b[0]/b[1]),(Fraction(1),Fraction(5,4)))
    def test_16_conditional_iia(self):
        for b in BETAS:
            x=conditional(b,SETS[0]); y=conditional(b,SETS[1])
            self.assertEqual(x[0]/x[1],y[0]/y[1])
    def test_17_conditional_sign_symmetry(self):
        for xs in SETS:
            self.assertEqual(conditional(1,xs),conditional(-1,tuple(-x for x in xs)))
    def test_18_equal_features(self):
        for q in QS:
            for s in (2,4):
                p=mixed(q,SETS[s]); self.assertEqual(p[1],p[2])
    def test_19_q_zero_degeneracy(self):
        for xs in SETS: self.assertEqual(mixed(Fraction(0),xs),conditional(-1,xs))
    def test_20_q_one_degeneracy(self):
        for xs in SETS: self.assertEqual(mixed(Fraction(1),xs),conditional(1,xs))
    def test_21_q_half(self):
        for xs in SETS:
            self.assertEqual(mixed(Fraction(1,2),xs),
                             tuple((a+b)/2 for a,b in zip(conditional(1,xs),conditional(-1,xs))))
    def test_22_invalid_beta(self):
        with self.assertRaises(ValueError): conditional(0,(0,1))
    def test_23_invalid_features(self):
        with self.assertRaises(ValueError): conditional(1,())
    def test_24_invalid_q(self):
        with self.assertRaises(ValueError): mixed(Fraction(5,4),(0,1))
    def test_25_invalid_q_float(self):
        with self.assertRaises(ValueError): mixed(.5,(0,1))
    def test_26_integer_exponent(self):
        with self.assertRaises(ValueError): power_two(1.0)
    def test_27_deterministic_render(self):
        self.assertEqual(csv_text(generate()[0]),csv_text(generate()[0]))
    def test_28_replay(self): self.assertTrue(replay())
    def test_29_corrupt_source_rejected(self):
        with self.assertRaises(AssertionError):
            check_source_text(csv_text(generate()[0]).replace("1/3","1/7",1),
                              json_text(generate()[1]))
    def test_30_world_id(self):
        self.assertEqual([w["world_id"] for w in generate()[1]["worlds"]],list(range(15)))
    def test_31_source_rows_per_world(self):
        from collections import Counter
        counts=Counter(int(r["world_id"]) for r in generate()[0])
        self.assertEqual(sorted(counts.values()),[4]*3+[6]*12)
    def test_32_source_metadata(self):
        self.assertEqual(generate()[1]["original_catalogue_id"],"01-007")
        self.assertTrue(generate()[1]["synthetic_only"])
    def test_33_type_swap_mass(self):
        for xs in SETS:
            for q in QS:
                self.assertEqual(mixed(q,xs),mixed(1-q,tuple(-x for x in xs)))
    def test_34_conditional_binary(self):
        self.assertEqual(conditional(1,(0,1)),(Fraction(1,3),Fraction(2,3)))
    def test_35_all_marginal_source_rows(self):
        for r in generate()[0]:
            self.assertEqual(Fraction(r["mixed_probability"]),
                             mixed(Fraction(r["q_plus"]),tuple(map(int,r["features"].split("|"))))[int(r["alternative_index"])])

if __name__ == "__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("--generate",action="store_true")
    parser.add_argument("--audit",action="store_true")
    parser.add_argument("--test",action="store_true")
    args=parser.parse_args()
    if args.generate:
        rows,results=generate()
        SOURCE.write_text(csv_text(rows),encoding="utf-8")
        RESULT.write_text(json_text(results),encoding="utf-8")
        print("R319_GENERATED",len(rows),len(results["worlds"]))
    elif args.audit:
        replay()
        print("R319_REPLAY_PASS 84_ATOMS 15_WORLDS 42_MARGINALS")
    else:
        unittest.main(argv=["r319"] if args.test else None)
