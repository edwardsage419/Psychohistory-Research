#!/usr/bin/env python3
"""R065 critical-trial audit of the fixed Levy et al. processed CSV.

Python >= 3.10, standard library only. Requires the original Git blob bytes.
This retrospective exploratory audit is separate from R064's frozen primary analysis.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import math
from pathlib import Path

SOURCE_REPO = "arielevy8/obs-learning-fishing"
SOURCE_PATH = "data/processed/unified_data_2025-01-16_00.csv"
SOURCE_BLOB = "01bf211468abe093618dfa5e5c39e883230c9c03"
CRITICAL_DAYS = (4, 21, 38, 55, 72, 89, 106, 123)
REQUIRED = ("participant_id", "stakes", "copied", "accurate",
            "comprehension_check_repetitions", "critical", "day")


def parse_verified(raw: bytes) -> list[dict[str, str]]:
    digest = hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\0" + raw).hexdigest()
    if digest != SOURCE_BLOB:
        raise ValueError("Source Git blob SHA1 mismatch: fail closed")
    reader = csv.DictReader(io.StringIO(raw.decode("utf-8-sig"), newline=""))
    if not set(REQUIRED).issubset(set(reader.fieldnames or ())):
        raise ValueError("Required source columns missing")
    return list(reader)


def summarize(rows: list[dict[str, str]], draws: int = 20000,
              seed: int = 20261015, min_paired: int = 10) -> dict:
    """Reapply full-trial author exclusion, then audit only diagnostic trials."""
    participants: dict[str, dict] = {}
    for row in rows:
        if any(row.get(k) in (None, "", "NA", "NaN", "nan") for k in REQUIRED):
            raise ValueError("Required data absent: fail closed")
        pid, stake = row["participant_id"], row["stakes"]
        if stake not in ("high", "low"):
            raise ValueError("Unexpected stake label")
        copied, accurate = float(row["copied"]), float(row["accurate"])
        repeat = float(row["comprehension_check_repetitions"])
        critical, day = float(row["critical"]), float(row["day"])
        if (copied not in (0, 1) or accurate not in (0, 1)
                or critical not in (0, 1) or not math.isfinite(repeat)
                or not day.is_integer()):
            raise ValueError("Invalid or nonfinite measurement")
        record = participants.setdefault(pid, {"n": 0, "acc": 0.,
                 "repeat": 0., "critical": []})
        record["n"] += 1
        record["acc"] += accurate
        record["repeat"] += repeat
        if critical:
            record["critical"].append((stake, int(copied), int(accurate), int(day)))

    exclusions = {"accuracy": 0, "comprehension": 0, "union": 0,
                  "excluded_rows": 0}
    selected = []
    for subject in participants.values():
        excluded_acc = subject["acc"] / subject["n"] < 0.45
        excluded_repeat = subject["repeat"] / subject["n"] > 2
        exclusions["accuracy"] += int(excluded_acc)
        exclusions["comprehension"] += int(excluded_repeat)
        exclusions["union"] += int(excluded_acc or excluded_repeat)
        if excluded_acc or excluded_repeat:
            exclusions["excluded_rows"] += subject["n"]
        else:
            selected.append(subject)
    if len(selected) < min_paired:
        raise ValueError("Insufficient eligible participants")

    total = {"high": {"n": 0, "k": 0, "accurate": 0},
             "low": {"n": 0, "k": 0, "accurate": 0}}
    unit = []
    for subject in selected:
        rows_c = subject["critical"]
        if sorted(row[3] for row in rows_c) != list(CRITICAL_DAYS):
            raise ValueError("Incomplete or duplicated diagnostic-day schedule")
        a = {"high": {"n": 0, "k": 0}, "low": {"n": 0, "k": 0}}
        for stake, copied, accurate, day in rows_c:
            if copied + accurate != 1:
                raise ValueError("Diagnostic accuracy/copying complement violated")
            a[stake]["n"] += 1
            a[stake]["k"] += copied
            total[stake]["n"] += 1
            total[stake]["k"] += copied
            total[stake]["accurate"] += accurate
        if a["high"]["n"] != 4 or a["low"]["n"] != 4:
            raise ValueError("Diagnostic stake schedule is not 4/4")
        unit.append(a)

    per = []
    t = total
    for a in unit:
        hn, hk = a["high"]["n"], a["high"]["k"]
        ln, lk = a["low"]["n"], a["low"]["k"]
        n, k = hn + ln, hk + lk
        # Leave this participant's eight outcomes entirely out of training.
        p0 = (t["high"]["k"] + t["low"]["k"] - k + 4) / (
              t["high"]["n"] + t["low"]["n"] - n + 8)
        ph = (t["high"]["k"] - hk + 4) / (t["high"]["n"] - hn + 8)
        pl = (t["low"]["k"] - lk + 4) / (t["low"]["n"] - ln + 8)

        def ll(nn: int, kk: int, p: float) -> float:
            return -(kk * math.log(p) + (nn - kk) * math.log1p(-p)) / nn

        def brier(nn: int, kk: int, p: float) -> float:
            return (kk * (1-p)**2 + (nn-kk) * p**2) / nn

        l0, b0 = ll(n, k, p0), brier(n, k, p0)
        l1 = (hn * ll(hn, hk, ph) + ln * ll(ln, lk, pl)) / n
        b1 = (hn * brier(hn, hk, ph) + ln * brier(ln, lk, pl)) / n
        per.append({"stake": hk/hn - lk/ln, "loss": l1-l0,
                    "brier": b1-b0, "l0": l0, "l1": l1,
                    "b0": b0, "b1": b1})

    def mean(key: str) -> float:
        return sum(p[key] for p in per) / len(per)

    def random_generator(initial: int):
        state = initial & 0xffffffff
        while True:
            state ^= (state << 13) & 0xffffffff
            state ^= state >> 17
            state ^= (state << 5) & 0xffffffff
            state &= 0xffffffff
            yield state / 4294967296.0

    random = random_generator(seed)
    boot = {key: [] for key in ("stake", "loss", "brier")}
    for _ in range(draws):
        sums = {key: 0. for key in boot}
        for _ in range(len(per)):
            x = per[int(next(random) * len(per))]
            for key in sums:
                sums[key] += x[key]
        for key in sums:
            boot[key].append(sums[key] / len(per))
    intervals = {}
    for key, values in boot.items():
        values.sort()
        intervals[key] = [values[math.floor(.025 * (draws-1))],
                          values[math.ceil(.975 * (draws-1))]]

    return {"status": "LOCAL_BYTE_VERIFIED_ONLY_WHEN_CLI_SOURCE_PROVIDED",
            "source_git_blob_sha1": SOURCE_BLOB,
            "raw_rows": len(rows), "raw_participants": len(participants),
            "exclusion": exclusions, "participants": len(selected),
            "critical_rows": sum(v["n"] for v in total.values()),
            "critical_stakes": total,
            "critical_copying_high_minus_low": mean("stake"),
            "critical_emulation_consistent_fraction": sum(v["accurate"] for v in total.values()) / sum(v["n"] for v in total.values()),
            "leave_one_participant_out": {
                "M0_logloss": mean("l0"), "M1_logloss": mean("l1"),
                "M1_minus_M0_logloss": mean("loss"),
                "M0_brier": mean("b0"), "M1_brier": mean("b1"),
                "M1_minus_M0_brier": mean("brier"),
                "M1_wins": sum(p["loss"] < -1e-12 for p in per),
                "M1_loses": sum(p["loss"] > 1e-12 for p in per)},
            "participant_bootstrap": {"seed": seed, "draws": draws,
                                      "CI95": intervals}}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = summarize(parse_verified(args.source.read_bytes()))
    result["status"] = "AUTHOR_PROCESSED_SOURCE_LOCALLY_SHA1_VERIFIED"
    args.output.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n",
                           encoding="utf-8")
    print(json.dumps({"status": "PASS", "participants": result["participants"],
                      "critical_rows": result["critical_rows"]}))


if __name__ == "__main__":
    main()
