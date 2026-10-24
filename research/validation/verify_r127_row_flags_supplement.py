#!/usr/bin/env python3
"""R127 supplemental row flags. Run from any directory in the original checkout.
E1 finite constructed payoffs only. No human E2 or historical E3.
"""
import argparse
import csv
import hashlib
import importlib.util
import io
import itertools
import pathlib
import subprocess
from fractions import Fraction

ROOT = pathlib.Path(__file__).resolve().parents[2]
SOURCE = ROOT / "research/R127/r127_van_huyck_1990_min_effort_coordination_selection_exact.py"
RAW = ROOT / "research/validation/R127_INTEGER_TENT_2793_PROFILES_2026-10-24.csv"
RECEIPT = ROOT / "research/validation/R127_INTEGER_TENT_2793_PROFILES_CI_FLAG_SUPPLEMENT_2026-10-24.csv"
SOURCE_BLOB = "6964fa57e291e719e8cc071cc3a70d73836363e4"
RAW_SHA256 = "821f785bf21a96eae5b65d1200389a5a2baa45ad63e5a115e48505051a2e9df4"
HEADER = ["group_size", "efforts", "minimum", "payoff_numerators", "exact_comparison_flag"]

def produce():
    blob = subprocess.check_output(["git", "hash-object", str(SOURCE)], text=True).strip()
    if blob != SOURCE_BLOB:
        raise AssertionError("original source Git blob changed")
    data = RAW.read_bytes()
    if hashlib.sha256(data).hexdigest() != RAW_SHA256:
        raise AssertionError("raw data SHA256 changed")
    spec = importlib.util.spec_from_file_location("r127_original_receipt", SOURCE)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    expected_rows = []
    for n in (2, 3, 4):
        for p in itertools.product(range(1, 8), repeat=n):
            minimum = min(p)
            numerators = tuple(6 + 2 * minimum - e for e in p)
            actual = module.payoff_vector(p, experimental=True)
            if actual != tuple(Fraction(v, 10) for v in numerators):
                raise AssertionError(f"original payoff mismatch for {p}")
            expected_rows.append([str(n), "|".join(map(str, p)), str(minimum),
                                  "|".join(map(str, numerators)), "PASS"])
    actual_rows = list(csv.reader(io.StringIO(data.decode("utf-8"))))
    if actual_rows[0] != HEADER[:-1]:
        raise AssertionError("original raw header changed")
    if [r[:-1] for r in expected_rows] != actual_rows[1:]:
        raise AssertionError("original raw row mismatch")
    out = io.StringIO(newline="")
    writer = csv.writer(out, lineterminator="\n")
    writer.writerow(HEADER)
    writer.writerows(expected_rows)
    return out.getvalue().encode("utf-8")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--verify-existing", action="store_true")
    parser.add_argument("--output", type=pathlib.Path)
    args = parser.parse_args()
    result = produce()
    if args.verify_existing and RECEIPT.read_bytes() != result:
        raise AssertionError("archived supplementary receipt mismatch")
    if args.output:
        args.output.write_bytes(result)
    print(f"R127 row flags PASS: 2793; receipt_bytes={len(result)}; "
          f"receipt_sha256={hashlib.sha256(result).hexdigest()}")

if __name__ == "__main__":
    main()
