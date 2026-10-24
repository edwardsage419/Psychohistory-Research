#!/usr/bin/env python3
"""Exact R133 strict ESS versus frozen R132 625-game phase portraits.

Only finite artificial payoff games; no human or historical evidence.
"""
import csv
import hashlib
import json
from collections import Counter
from pathlib import Path

R132_CSV_BLOB = "6f1a5b18c5fd11aba9a656fa5667516334499e30"
R133_STATUS_BLOB = "70d36423e87eca9a14f7b6f9f18177e66c9116d5"
EXPECTED = {
    "pure_A_ESS": 300,
    "pure_B_ESS": 300,
    "both_pure_ESS": 100,
    "internal_mixed_ESS": 100,
    "no_strict_ESS": 25,
}


def blob_sha(data: bytes) -> str:
    return hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()


def strict_ess(a: int, b: int, c: int, d: int):
    # Maynard Smith and Price's second condition resolves weak Nash ties.
    pure_a = (a > c) or (a == c and b > d)
    pure_b = (d > b) or (d == b and c > a)
    mixed = (b > d and c > a)
    return pure_a, pure_b, mixed


def run(csv_path: Path, status_path: Path | None = None) -> dict:
    data = csv_path.read_bytes()
    assert blob_sha(data) == R132_CSV_BLOB, "R132 frozen CSV identity drift"
    rows = list(csv.DictReader(data.decode("utf-8").splitlines()))
    assert len(rows) == 625
    seen = set()
    counts = Counter()
    for row in rows:
        a, b, c, d = (int(row[k]) for k in ("a", "b", "c", "d"))
        assert (a, b, c, d) not in seen
        seen.add((a, b, c, d))
        pure_a, pure_b, mixed = strict_ess(a, b, c, d)
        assert not (mixed and (pure_a or pure_b))
        if pure_a:
            counts["pure_A_ESS"] += 1
        if pure_b:
            counts["pure_B_ESS"] += 1
        if pure_a and pure_b:
            counts["both_pure_ESS"] += 1
        if mixed:
            counts["internal_mixed_ESS"] += 1
        if not (pure_a or pure_b or mixed):
            counts["no_strict_ESS"] += 1
        predicted = (
            "bistable_threshold" if pure_a and pure_b else
            "A_monotone" if pure_a else
            "B_monotone" if pure_b else
            "stable_coexistence" if mixed else
            "neutral_continuum"
        )
        assert predicted == row["phase_class"], (a, b, c, d, predicted, row["phase_class"])
    assert dict(counts) == EXPECTED, (counts, EXPECTED)
    assert len(seen) == 625
    # Deliberately invalid ESS rules: strict Nash only misses weak ESS;
    # treating neutral weak Nash as strict ESS falsely admits all-tied games.
    assert strict_ess(0, 1, 0, 0)[0] and not (0 > 0)
    assert strict_ess(0, 0, 0, 0) == (False, False, False)
    status_verified = False
    if status_path is not None and status_path.is_file():
        raw = status_path.read_bytes()
        assert blob_sha(raw) == R133_STATUS_BLOB, "R133 acceptance identity drift"
        status = json.loads(raw)
        for key, value in EXPECTED.items():
            assert status[key] == value, (key, status[key], value)
        status_verified = True
    return {
        "checked_games": len(seen),
        "crossmodel_class_matches": len(seen),
        "counts": dict(sorted(counts.items())),
        "R133_frozen_status_verified": status_verified,
        "negative_controls_rejected": 2,
        "evidence": "E1 synthetic finite 2x2 games only",
        "E2": 0, "E3": 0,
    }


if __name__ == "__main__":
    root = Path(__file__).resolve().parents[2]
    csv_file = Path(__file__).with_name("R132_EXHAUSTIVE_625_TWO_STRATEGY_PHASE_PORTRAITS_2026-10-25.csv")
    result = run(csv_file, root / "research/R133/R133_FINAL_ACCEPTANCE_STATUS.json")
    print(json.dumps(result, sort_keys=True))
