#!/usr/bin/env python3
"""R272 third-source independent frozen E1 archive audit.

Separate from original generator, the quarantined source wrapper, and its
negative suite. No source generation and no writes to archival evidence.
Use: python -B -I -S research/validation/r272_frozen_independent_third_source_20261117.py --root .
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import io
import itertools
import json
from collections import defaultdict
from fractions import Fraction as F
from math import comb
from pathlib import Path

SOURCE = "research/R272/R272_ALL_576_ORIGINAL_TRAIN_AND_TEST_SOURCES.csv"
RESULTS = "research/R272/R272_EXACT_RESULTS.json"
RECEIPT = "research/R272/R272_MACHINE_RECEIPT.json"
PINS = {
    SOURCE: "dc40ed773491817caf242ba6416e1bdf98ef2f1a2cd05e1956bdf5aec5801663",
    RESULTS: "f891df1c4640c2f49a457c436bc043f6bc08b768ac92594050e7e08061495a40",
}
FREEZE = "52f84dbfbe8563cf5c9a491e67d5e320223e0a56"
PS = (F(1, 4), F(1, 2), F(3, 4))
MODELS = ("CONSTANT_HALF", "TRAIN_MLE", "LAPLACE_BETA11")
COLUMNS = (
    "world", "true_p", "predictor", "original_full_sixbit_source",
    "original_training_four_bits", "original_future_test_two_bits",
    "train_successes", "test_successes", "exact_original_source_probability",
    "forecast_trained_on_four_bits_only", "original_train_brier_per_row",
    "original_test_brier_per_row", "exact_train_mean_brier",
    "exact_independent_test_mean_brier", "unfloored_future_log_loss_is_infinite"
)
LOCKED = {
    F(1, 4): (
        ("1/4", "1/4", "0"), ("9/64", "15/64", "291/2048"),
        ("11/72", "31/144", "0")),
    F(1, 2): (
        ("1/4", "1/4", "0"), ("3/16", "5/16", "3/32"),
        ("7/36", "5/18", "0")),
    F(3, 4): (
        ("1/4", "1/4", "0"), ("9/64", "15/64", "291/2048"),
        ("11/72", "31/144", "0")),
}


class SourceGateError(ValueError):
    pass


def require(ok: bool, label: str) -> None:
    if ok is not True:
        raise SourceGateError("R272_SOURCE_GATE_" + label)


def q(s: str) -> F:
    v = F(s)
    require(str(v) == s, "NONCANONICAL_FRACTION")
    return v


def source_integrity(row: dict[str, str]) -> tuple[F, str, str, F, F, F, F]:
    require(set(row) == set(COLUMNS), "SCHEMA")
    p = q(row["true_p"])
    require(p in PS, "PROBABILITY_WORLD")
    model = row["predictor"]
    require(model in MODELS, "MODEL_WORLD")
    bits = row["original_full_sixbit_source"]
    require(len(bits) == 6 and set(bits) <= {"0", "1"}, "ORIGINAL_BITS")
    require(row["original_training_four_bits"] == bits[:4] and
            row["original_future_test_two_bits"] == bits[4:],
            "HONEST_TRAIN_TEST_SPLIT")
    require(row["world"] == "TRUE_P" + str(p).replace("/", "OF") + "_" + model,
            "SOURCE_WORLD_ID")
    k = bits[:4].count("1")
    j = bits[4:].count("1")
    require(row["train_successes"] == str(k) and
            row["test_successes"] == str(j), "SOURCE_COUNTS")
    weight = p ** (k + j) * (1 - p) ** (6 - k - j)
    require(q(row["exact_original_source_probability"]) == weight,
            "SOURCE_WEIGHT")
    prediction = (
        F(1, 2) if model == "CONSTANT_HALF"
        else F(k, 4) if model == "TRAIN_MLE"
        else F(k + 1, 6)
    )
    require(q(row["forecast_trained_on_four_bits_only"]) == prediction,
            "NO_TEST_LEAKAGE_TO_MODEL")
    train_loss = [(F(int(z)) - prediction) ** 2 for z in bits[:4]]
    test_loss = [(F(int(z)) - prediction) ** 2 for z in bits[4:]]
    require(row["original_train_brier_per_row"] == ";".join(map(str, train_loss)),
            "TRAIN_LOSSES")
    require(row["original_test_brier_per_row"] == ";".join(map(str, test_loss)),
            "INDEPENDENT_TEST_LOSSES")
    train = sum(train_loss, F(0)) / 4
    test = sum(test_loss, F(0)) / 2
    require(q(row["exact_train_mean_brier"]) == train and
            q(row["exact_independent_test_mean_brier"]) == test,
            "PER_SOURCE_SCORE")
    infinite = int(prediction in (0, 1) and
                   ((prediction == 0 and j > 0) or
                    (prediction == 1 and j < 2)))
    require(row["unfloored_future_log_loss_is_infinite"] == str(infinite),
            "INF_LOG_LOSS_EVENT")
    return p, model, bits, weight, train, test, F(infinite)


def evaluate(s: str, e: str, receipt: dict) -> dict:
    reader = csv.DictReader(io.StringIO(s))
    require(tuple(reader.fieldnames or ()) == COLUMNS, "CSV_SCHEMA")
    rows = list(reader)
    require(len(rows) == 576, "EXACT_576_SOURCE_ROWS")
    archive = json.loads(e)
    require(archive.get("prescore_freeze_commit") == FREEZE and
            archive.get("original_catalogue_id") == "12-002" and
            archive.get("artificial_worlds") == 9 and
            archive.get("complete_source_types") == 576, "FROZEN_SCOPE")
    require(receipt.get("prescore_freeze_commit") == FREEZE and
            receipt.get("all_complete_original_sources") == 576 and
            receipt.get("independent_analytic_comparisons") == 9 and
            receipt.get("new_real_human_E2") == 0 and
            receipt.get("new_real_historical_E3") == 0, "HISTORICAL_RECEIPT")
    totals = defaultdict(lambda: [F(0), F(0), F(0), F(0)])
    unique = defaultdict(set)
    for item in rows:
        p, model, bits, mass, train, test, inf = source_integrity(item)
        key = (p, model)
        require(bits not in unique[key], "DUPLICATED_SOURCE")
        unique[key].add(bits)
        t = totals[key]
        for idx, value in enumerate((mass, mass * train, mass * test, mass * inf)):
            t[idx] += value
    expected_sources = set("".join(z) for z in itertools.product("01", repeat=6))
    original = archive.get("world_results")
    require(isinstance(original, list) and len(original) == 9, "NINE_WORLDS")
    visited = set()
    for world in original:
        p = q(world["true_p"])
        model = world["predictor"]
        key = (p, model)
        require(key not in visited and key in totals, "FROZEN_WORLD_UNIQUE")
        visited.add(key)
        require(unique[key] == expected_sources and totals[key][0] == 1,
                "COMPLETE_ORDERED_SOURCE_MASS")
        values = LOCKED[p][MODELS.index(model)]
        require(tuple(str(x) for x in totals[key][1:]) == values,
                "BEFORE_SCORE_FROZEN_COMPARISON")
        require(tuple(world[k] for k in (
            "exact_design_expected_train_mean_Brier",
            "exact_design_expected_independent_future_mean_Brier",
            "exact_unfloored_infinite_test_log_loss_event_probability")) == values,
            "ORIGINAL_FROZEN_JSON_COMPARISON")
        train = test = F(0)
        for successes in range(5):
            prob = F(comb(4, successes)) * p ** successes * (1 - p) ** (4-successes)
            pred = (
                F(1, 2) if model == "CONSTANT_HALF"
                else F(successes, 4) if model == "TRAIN_MLE"
                else F(successes + 1, 6)
            )
            train += prob * (successes * (1 - pred) ** 2 +
                             (4 - successes) * pred ** 2) / 4
            test += prob * (p * (1 - pred) ** 2 +
                            (1-p) * pred ** 2)
        inf = (
            (1-p)**4 * (1-(1-p)**2) + p**4 * (1-p**2)
            if model == "TRAIN_MLE" else F(0)
        )
        require((train, test, inf) == tuple(totals[key][1:]),
                "INDEPENDENT_BINOMIAL_MOMENTS")
    require(visited == set(totals) and len(visited) == 9, "COMPLETE_WORLD_SET")
    # Negative mutations are in memory and never touch historical bytes.
    mutants = 0
    for field, wrong, expected_label in (
        ("exact_original_source_probability", "1/2", "SOURCE_WEIGHT"),
        ("original_future_test_two_bits", "11", "HONEST_TRAIN_TEST_SPLIT"),
        ("exact_independent_test_mean_brier", "1/2", "PER_SOURCE_SCORE"),
    ):
        fake = rows[0].copy()
        fake[field] = wrong
        try:
            source_integrity(fake)
        except SourceGateError as err:
            require(str(err) == "R272_SOURCE_GATE_"+expected_label,
                    "MUTANT_UNEXPECTED_REJECT_PATH")
            mutants += 1
        else:
            raise SourceGateError("R272_SOURCE_GATE_MUTANT_ACCEPTED_"+field)
    return {
        "status": "PASS_R272_PRESCORE_FROZEN_THIRD_SOURCE_AUDIT",
        "archived_original_sources": len(rows),
        "separate_worlds": len(visited),
        "independent_source_bits_per_world": 64,
        "analytic_binomial_worlds": 9,
        "in_memory_mutations_rejected": mutants,
        "frozen_science_changed": False, "new_E2": 0, "new_E3": 0,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path("."))
    args = parser.parse_args()
    root = args.root.resolve(strict=True)
    blobs = {}
    for name, sha in PINS.items():
        file = root / name
        require(file.is_file() and not file.is_symlink(), "SOURCE_FILE")
        raw = file.read_bytes()
        require(hashlib.sha256(raw).hexdigest() == sha, "ARCHIVE_HASH_"+name)
        blobs[name] = raw.decode("utf-8")
    raw_receipt = (root / RECEIPT).read_text(encoding="utf-8")
    receipt = json.loads(raw_receipt)
    require(receipt.get("source_sha256") == PINS[SOURCE] and
            receipt.get("results_sha256") == PINS[RESULTS],
            "MACHINE_RECEIPT_HASHES")
    result = evaluate(blobs[SOURCE], blobs[RESULTS], receipt)
    result["source_sha256"] = PINS[SOURCE]
    result["results_sha256"] = PINS[RESULTS]
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    try:
        main()
    except (SourceGateError, ValueError, OSError, KeyError, TypeError) as e:
        raise SystemExit("FAIL: " + str(e)) from e
