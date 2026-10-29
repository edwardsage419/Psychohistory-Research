#!/usr/bin/env python3
"""R276 S72: exact ordered Z source enumeration and binomial count oracle.

Standard library only. Nonblind artificial E1 extension; does not alter R276.
Usage: python r276_s72_auxiliary_z_sample_curve_20261030.py --output-dir DIR
       python r276_s72_auxiliary_z_sample_curve_20261030.py --check DIR
       python r276_s72_auxiliary_z_sample_curve_20261030.py --selftest
"""
from __future__ import annotations
import argparse
import csv
import hashlib
import io
import itertools
import json
import unittest
from fractions import Fraction as F
from math import comb
from pathlib import Path

PROTOCOL = "8e3eb673efa5daeddf1c5defe03ae205a2aa9429"
ORIGINAL = "58e192c523cc87b4fd4f6b9758af118d620a1951"
MODELS = ("PARAM_A", "PARAM_B", "PARAM_C")
THETA = (F(1, 2), F(1, 4), F(1, 1))
GRID = tuple(range(9))
FIELDNAMES = ("m", "true_model", "ordered_z", "successes",
              "source_mass", "selected", "correct",
              "posterior_A", "posterior_B", "posterior_C")

def likelihood(theta: F, k: int, m: int) -> F:
    return theta ** k * (1 - theta) ** (m - k)

def decision(likes: tuple[F, ...]) -> int:
    best = max(likes)
    return next(i for i, x in enumerate(likes) if x == best)

def ordered_route():
    rows = []
    summaries = []
    for m in GRID:
        matrix = [[F(0) for _ in MODELS] for _ in MODELS]
        positive, total = 0, 0
        for true_index, name in enumerate(MODELS):
            for bits in itertools.product("01", repeat=m):
                z = "".join(bits)
                k = z.count("1")
                likes = tuple(likelihood(t, k, m) for t in THETA)
                denom = sum(likes)
                assert denom > 0
                selected = decision(likes)
                mass = likes[true_index]
                matrix[true_index][selected] += mass
                positive += mass > 0
                total += 1
                rows.append({
                    "m": m, "true_model": name, "ordered_z": z,
                    "successes": k, "source_mass": str(mass),
                    "selected": MODELS[selected], "correct": int(selected == true_index),
                    "posterior_A": str(likes[0] / denom),
                    "posterior_B": str(likes[1] / denom),
                    "posterior_C": str(likes[2] / denom)})
        assert total == 3 * 2 ** m
        assert all(sum(row) == 1 for row in matrix)
        acc = tuple(matrix[i][i] for i in range(3))
        macro = sum(acc) / 3
        summaries.append({
            "m": m, "source_rows": total, "positive_mass_rows": positive,
            "confusion": [[str(x) for x in row] for row in matrix],
            "conditional_accuracy": [str(x) for x in acc],
            "macro_accuracy": str(macro), "macro_error": str(1 - macro)})
    return rows, summaries

def independent_binomial_oracle():
    """Independent count distribution; no ordered-source construction."""
    out = []
    for m in GRID:
        matrix = [[F(0) for _ in MODELS] for _ in MODELS]
        for k in range(m + 1):
            scores = [t ** k * (1 - t) ** (m - k) for t in THETA]
            winner = next(i for i in range(3) if scores[i] == max(scores))
            for i, t in enumerate(THETA):
                matrix[i][winner] += F(comb(m, k)) * t ** k * (1 - t) ** (m - k)
        out.append(matrix)
    return out

def make_result():
    rows, summaries = ordered_route()
    oracle = independent_binomial_oracle()
    assert len(rows) == 1533
    for s, mat in zip(summaries, oracle):
        assert s["confusion"] == [[str(x) for x in r] for r in mat]
    assert summaries[0]["macro_accuracy"] == "1/3"
    assert summaries[2]["macro_accuracy"] == "11/16"
    assert summaries[2]["conditional_accuracy"] == ["1/2", "9/16", "1"]
    curve = [F(s["macro_accuracy"]) for s in summaries]
    assert all(a <= b for a, b in zip(curve, curve[1:]))
    threshold = next((s["m"] for s in summaries if F(s["macro_accuracy"]) >= F(9, 10)), None)
    result = {
        "research_id": "R276_S72", "original_research_id": "R276",
        "original_freeze_commit": ORIGINAL, "s72_prescore_freeze_commit": PROTOCOL,
        "evidence": "EXPLORATORY_E1_NONBLIND_FINITE_ARTIFICIAL",
        "model_order": list(MODELS), "theta1": [str(t) for t in THETA],
        "m_grid": list(GRID), "source_rows": len(rows),
        "macro_threshold": "9/10", "first_m_reaching_threshold": threshold,
        "ordered_vs_binomial_oracle_equal": True,
        "R073": "FROZEN", "PESEN_v0_1": "FROZEN",
        "new_E2_predictions": 0, "new_E3_predictions": 0,
        "summaries": summaries}
    return rows, result

def output_bytes():
    rows, result = make_result()
    buf = io.StringIO(newline="")
    writer = csv.DictWriter(buf, fieldnames=FIELDNAMES, lineterminator="\n")
    writer.writeheader()
    writer.writerows(rows)
    return (buf.getvalue().encode("utf-8"),
            (json.dumps(result, ensure_ascii=False, indent=2) + "\n").encode("utf-8"))

def check(csv_path: Path, json_path: Path):
    expected_csv, expected_json = output_bytes()
    actual_csv, actual_json = csv_path.read_bytes(), json_path.read_bytes()
    if actual_csv != expected_csv:
        raise ValueError("ordered source CSV byte mismatch")
    if actual_json != expected_json:
        raise ValueError("result JSON byte mismatch")
    return {
        "source_rows": 1533,
        "csv_sha256": hashlib.sha256(actual_csv).hexdigest(),
        "json_sha256": hashlib.sha256(actual_json).hexdigest(),
        "status": "PASS"}

class Tests(unittest.TestCase):
    def test_count(self):
        self.assertEqual(len(make_result()[0]), 1533)
    def test_frozen_original(self):
        s = make_result()[1]["summaries"]
        self.assertEqual(s[0]["macro_accuracy"], "1/3")
        self.assertEqual(s[2]["macro_accuracy"], "11/16")
    def test_all_oracle_cells(self):
        self.assertTrue(make_result()[1]["ordered_vs_binomial_oracle_equal"])
    def test_probabilities(self):
        for s in make_result()[1]["summaries"]:
            for row in s["confusion"]:
                self.assertEqual(sum(map(F, row)), F(1))
    def test_monotone_bayes(self):
        s = make_result()[1]["summaries"]
        self.assertTrue(all(F(x["macro_accuracy"]) <= F(y["macro_accuracy"])
                            for x, y in zip(s, s[1:])))
    def test_no_duplicate_sources(self):
        rows = make_result()[0]
        self.assertEqual(len({(r["m"], r["true_model"], r["ordered_z"]) for r in rows}), len(rows))
    def test_csv_mutation_rejected(self):
        import tempfile
        with tempfile.TemporaryDirectory() as d:
            c, j = output_bytes()
            p, q = Path(d)/"rows.csv", Path(d)/"results.json"
            p.write_bytes(c); q.write_bytes(j)
            self.assertEqual(check(p, q)["status"], "PASS")
            p.write_bytes(c.replace(b"PARAM_A", b"PARAM_B", 1))
            with self.assertRaises(ValueError): check(p, q)
    def test_json_mutation_rejected(self):
        import tempfile
        with tempfile.TemporaryDirectory() as d:
            c, j = output_bytes()
            p, q = Path(d)/"rows.csv", Path(d)/"results.json"
            p.write_bytes(c); q.write_bytes(j)
            q.write_bytes(j.replace(b"11/16", b"10/16", 1))
            with self.assertRaises(ValueError): check(p, q)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    g = parser.add_mutually_exclusive_group(required=True)
    g.add_argument("--output-dir", type=Path)
    g.add_argument("--check", type=Path)
    g.add_argument("--selftest", action="store_true")
    args = parser.parse_args()
    if args.selftest:
        unittest.main(argv=["r276_s72"], exit=False)
    elif args.output_dir is not None:
        args.output_dir.mkdir(parents=True, exist_ok=True)
        c, j = output_bytes()
        (args.output_dir/"R276_S72_ALL_1533_ORDERED_Z_SOURCES_2026-10-30.csv").write_bytes(c)
        (args.output_dir/"R276_S72_EXACT_RESULTS_2026-10-30.json").write_bytes(j)
        print(json.dumps({"rows": 1533, "csv_sha256": hashlib.sha256(c).hexdigest(),
                          "json_sha256": hashlib.sha256(j).hexdigest()}))
    else:
        d = args.check
        print(json.dumps(check(d/"R276_S72_ALL_1533_ORDERED_Z_SOURCES_2026-10-30.csv",
                               d/"R276_S72_EXACT_RESULTS_2026-10-30.json")))
