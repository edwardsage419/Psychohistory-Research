#!/usr/bin/env python3
"""R127 third-method audit of the frozen 2026-10-24 integer tent-payoff protocol.
Constructed E1 only. Uses no R127 core payoff helpers for expected values.
"""
import argparse
import csv
import hashlib
import importlib
import io
import itertools
import json
import pathlib
import subprocess
import sys
from fractions import Fraction

ROOT = pathlib.Path(__file__).resolve().parents[2]
SOURCE = ROOT / "research/R127/r127_van_huyck_1990_min_effort_coordination_selection_exact.py"
DATA = ROOT / "research/validation/R127_INTEGER_TENT_2793_PROFILES_2026-10-24.csv"
EXPECTED_BLOB = "6964fa57e291e719e8cc071cc3a70d73836363e4"
HEADER = ["group_size", "efforts", "minimum", "payoff_numerators"]

def check_source_identity(path=SOURCE, expected=EXPECTED_BLOB):
    actual = subprocess.check_output(["git", "hash-object", str(path)], text=True).strip()
    if actual != expected:
        raise AssertionError("R127 original source identity mismatch")
    return actual

def independent_payoff_numerators(profile):
    smallest = min(profile)
    return tuple(6 + 2 * smallest - effort for effort in profile)

def rows():
    for n in (2, 3, 4):
        for p in itertools.product(range(1, 8), repeat=n):
            yield [str(n), "|".join(map(str, p)), str(min(p)),
                   "|".join(map(str, independent_payoff_numerators(p)))]

def canonical_csv():
    buffer = io.StringIO(newline="")
    writer = csv.writer(buffer, lineterminator="\n")
    writer.writerow(HEADER)
    writer.writerows(rows())
    return buffer.getvalue().encode("utf-8")

def check_raw_data(raw, expected):
    if raw != expected:
        raise AssertionError("R127 frozen raw CSV byte mismatch")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--verify", action="store_true")
    args = parser.parse_args()
    blob = check_source_identity()
    expected_raw = canonical_csv()
    actual_raw = DATA.read_bytes()
    check_raw_data(actual_raw, expected_raw)
    try:
        check_source_identity(expected="0" * 40)
    except AssertionError:
        pass
    else:
        raise AssertionError("wrong original blob was accepted")
    corrupted = bytearray(actual_raw)
    corrupted[-2] = ord("0") if corrupted[-2] != ord("0") else ord("1")
    try:
        check_raw_data(bytes(corrupted), expected_raw)
    except AssertionError:
        pass
    else:
        raise AssertionError("tampered raw CSV was accepted")
    sys.path.insert(0, str(SOURCE.parent))
    original = importlib.import_module("r127_van_huyck_1990_min_effort_coordination_selection_exact")
    profiles = 0
    payoffs = 0
    for n in (2, 3, 4):
        for profile in itertools.product(range(1, 8), repeat=n):
            expected = independent_payoff_numerators(profile)
            observed = original.payoff_vector(profile, experimental=True)
            if tuple(Fraction(x, 10) for x in expected) != observed:
                raise AssertionError("original R127 payoff mismatch")
            profiles += 1
            payoffs += n
    opponent_profiles = 0
    candidate_deviations = 0
    for length in (1, 2, 3):
        for others in itertools.product(range(1, 8), repeat=length):
            q = min(others)
            values = {}
            for e in range(1, 8):
                values[e] = 6 + e if e <= q else 6 + 2 * q - e
                candidate_deviations += 1
                original_payoff = original.payoff_vector((e,) + others)[0]
                if original_payoff != Fraction(values[e], 10):
                    raise AssertionError("candidate deviation payoff mismatch")
            maximizers = [e for e, v in values.items() if v == max(values.values())]
            if maximizers != [q] or original.strict_best_effort_against_others(others) != q:
                raise AssertionError("unique best response mismatch")
            opponent_profiles += 1
    controls = {
        (1, 1): (7, 7), (7, 7): (13, 13),
        (7, 1): (1, 7), (1, 7, 7, 7): (7, 1, 1, 1)
    }
    for profile, expected in controls.items():
        if independent_payoff_numerators(profile) != expected:
            raise AssertionError("frozen positive control mismatch")
    if (profiles, payoffs, opponent_profiles, candidate_deviations) != (2793, 10731, 399, 2793):
        raise AssertionError("frozen enumeration count mismatch")
    print(json.dumps({
        "research_id": "R127", "evidence": "CONSTRUCTED_E1",
        "profiles": profiles, "person_payoff_comparisons": payoffs,
        "opponent_profiles": opponent_profiles, "candidate_deviations": candidate_deviations,
        "source_git_blob": blob, "raw_csv_sha256": hashlib.sha256(actual_raw).hexdigest(),
        "negative_controls": 2, "positive_controls": 4,
        "result": "PASS_BOUNDED_INTERNAL_INTEGER_TENT_BEST_RESPONSE_E1_COMPUTATIONAL_CHECK"
    }, sort_keys=True))
if __name__ == "__main__":
    main()
