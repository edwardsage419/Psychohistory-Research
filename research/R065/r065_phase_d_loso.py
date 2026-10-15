#!/usr/bin/env python3
"""R065 Phase D: LOSO copying prediction with fixed source Git blob.

Retrospective comparison; use the exact author-processed CSV locally.
No third-party trial records are written to output. Python 3.10+, stdlib.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import math
from collections import defaultdict
from pathlib import Path

SOURCE_BLOB = "01bf211468abe093618dfa5e5c39e883230c9c03"
DAYS = (4, 21, 38, 55, 72, 89, 106, 123)
MODELS = ("M0", "M1", "M2", "M3")
PAIRS = (("M1", "M0"), ("M2", "M0"), ("M3", "M2"),
         ("M3", "M1"), ("M2", "M1"))


def parse_source(raw: bytes) -> list[dict[str, str]]:
    digest = hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\0" + raw).hexdigest()
    if digest != SOURCE_BLOB:
        raise ValueError("FAIL CLOSED: original processed CSV Git blob mismatch")
    return list(csv.DictReader(io.StringIO(raw.decode("utf-8-sig"), newline="")))


def cell_name(model: str, row: dict) -> str:
    if model == "M0":
        return "*"
    if model == "M1":
        return row["stake"]
    if model == "M2":
        return str(row["block"])
    if model == "M3":
        return str(row["block"]) + "|" + row["stake"]
    raise ValueError("Unsupported model")


def loo_cell_probability(total: tuple[int, int], subject: tuple[int, int]) -> float:
    """Return Beta(4,4) cell mean after removing ALL subject observations."""
    n, k = total
    sn, sk = subject
    if sn > n or sk > k or sk > sn or k - sk > n - sn:
        raise ValueError("Inconsistent training/test cell totals")
    return (k - sk + 4) / (n - sn + 8)


def analyze(rows: list[dict[str, str]], draws: int = 20000,
            seed: int = 20261016, min_subjects: int = 10) -> dict:
    required = ("participant_id", "stakes", "copied", "accurate",
                "comprehension_check_repetitions", "critical", "day")
    people = {}
    for row in rows:
        if any(row.get(field) in (None, "", "NA", "NaN", "nan") for field in required):
            raise ValueError("Missing required data")
        pid = row["participant_id"]
        stake, copy = row["stakes"], float(row["copied"])
        accuracy, check = float(row["accurate"]), float(row["comprehension_check_repetitions"])
        critical, day = float(row["critical"]), float(row["day"])
        if (stake not in ("high", "low") or copy not in (0, 1) or
                accuracy not in (0, 1) or critical not in (0, 1) or
                not math.isfinite(check) or not day.is_integer()):
            raise ValueError("Invalid source measurement")
        person = people.setdefault(pid, {"n": 0, "acc": 0., "checks": 0., "critical": []})
        person["n"] += 1
        person["acc"] += accuracy
        person["checks"] += check
        if critical:
            person["critical"].append({"day": int(day), "stake": stake, "copy": int(copy)})

    excluded = {"accuracy": 0, "comprehension": 0, "union": 0, "rows": 0}
    subjects = []
    for person in people.values():
        a = person["acc"] / person["n"] < 0.45
        c = person["checks"] / person["n"] > 2
        excluded["accuracy"] += int(a)
        excluded["comprehension"] += int(c)
        excluded["union"] += int(a or c)
        if a or c:
            excluded["rows"] += person["n"]
            continue
        items = sorted(person["critical"], key=lambda x: x["day"])
        if tuple(x["day"] for x in items) != DAYS:
            raise ValueError("Invalid diagnostic-day schedule")
        if sum(x["stake"] == "high" for x in items) != 4:
            raise ValueError("Invalid stake balance")
        for i, item in enumerate(items):
            item["block"] = i
        subjects.append(items)
    if len(subjects) < min_subjects:
        raise ValueError("Insufficient eligible participants")

    total = {m: defaultdict(lambda: [0, 0]) for m in MODELS}
    own = []
    for subject in subjects:
        own_s = {m: defaultdict(lambda: [0, 0]) for m in MODELS}
        for item in subject:
            for model in MODELS:
                key = cell_name(model, item)
                total[model][key][0] += 1
                total[model][key][1] += item["copy"]
                own_s[model][key][0] += 1
                own_s[model][key][1] += item["copy"]
        own.append(own_s)

    per = []
    for subject, own_s in zip(subjects, own):
        scores = {}
        for model in MODELS:
            loss = brier = 0.
            for item in subject:
                key = cell_name(model, item)
                p = loo_cell_probability(tuple(total[model][key]), tuple(own_s[model][key]))
                y = item["copy"]
                loss += -(y * math.log(p) + (1-y) * math.log1p(-p))
                brier += (y-p)**2
            scores[model] = {"logloss": loss / 8, "brier": brier / 8}
        per.append(scores)

    def mean(seq):
        return sum(seq)/len(seq)

    averages = {m: {metric: mean([x[m][metric] for x in per])
                     for metric in ("logloss", "brier")} for m in MODELS}
    contrasts = {}
    for a, b in PAIRS:
        key = a + "_minus_" + b
        diff = [x[a]["logloss"] - x[b]["logloss"] for x in per]
        contrasts[key] = {
            "mean_logloss": mean(diff),
            "mean_brier": mean([x[a]["brier"] - x[b]["brier"] for x in per]),
            "wins": sum(v < -1e-12 for v in diff),
            "losses": sum(v > 1e-12 for v in diff),
            "ties": sum(abs(v) <= 1e-12 for v in diff),
        }

    state = seed & 0xffffffff
    def next_rng():
        nonlocal state
        state ^= (state << 13) & 0xffffffff
        state ^= state >> 17
        state ^= (state << 5) & 0xffffffff
        state &= 0xffffffff
        return state / 4294967296.0

    boot = {a + "_minus_" + b: {"logloss": [], "brier": []} for a, b in PAIRS}
    for _ in range(draws):
        sums = {key: {"logloss": 0., "brier": 0.} for key in boot}
        for _ in per:
            person = per[int(next_rng() * len(per))]
            for a, b in PAIRS:
                for metric in ("logloss", "brier"):
                    sums[a + "_minus_" + b][metric] += person[a][metric] - person[b][metric]
        for key in boot:
            for metric in ("logloss", "brier"):
                boot[key][metric].append(sums[key][metric]/len(per))
    for key in boot:
        for metric in ("logloss", "brier"):
            vals = sorted(boot[key][metric])
            boot[key][metric] = [vals[math.floor(.025*(draws-1))],
                                 vals[math.ceil(.975*(draws-1))]]
    return {
        "source_blob_sha1": SOURCE_BLOB, "raw_rows": len(rows),
        "raw_participants": len(people), "excluded": excluded,
        "eligible_participants": len(subjects), "diagnostic_rows": len(subjects)*8,
        "models": averages, "contrasts": contrasts,
        "bootstrap_95": boot, "draws": draws, "seed": seed,
        "provenance": "LOCAL_SOURCE_GIT_BLOB_SHA1_REQUIRED",
        "limitations": "Retrospective post-hoc. No independent validation or mechanism identification.",
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    res = analyze(parse_source(args.source.read_bytes()))
    res["provenance"] = "AUTHOR_PROCESSED_CSV_LOCALLY_GIT_SHA1_VERIFIED"
    args.output.write_text(json.dumps(res, indent=2, ensure_ascii=False)+"\n", encoding="utf-8")
    print(json.dumps({"status":"PASS", "participants":res["eligible_participants"]}))


if __name__ == "__main__":
    main()
