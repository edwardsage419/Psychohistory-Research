#!/usr/bin/env python3
"""Retrospective R065 phase B: critical-trial order and time sensitivity.

Reads fixed author processed CSV only after Git SHA1 validation by
r065_critical_replay.parse_verified. Python 3.10+, standard library.
"""
from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
from r065_critical_replay import CRITICAL_DAYS, parse_verified


def order_audit(rows: list[dict], draws: int = 20000, seed: int = 20261015) -> dict:
    subjects: dict[str, dict] = {}
    for row in rows:
        for field in ("participant_id", "accurate", "copied", "stakes", "critical",
                      "day", "counterbalance", "comprehension_check_repetitions"):
            if row.get(field) in (None, "", "NA", "NaN", "nan"):
                raise ValueError("Missing mandatory field: " + field)
        pid = row["participant_id"]
        a, c, is_critical = (float(row[k]) for k in ("accurate", "copied", "critical"))
        reps = float(row["comprehension_check_repetitions"])
        if a not in (0, 1) or c not in (0, 1) or is_critical not in (0, 1) or not math.isfinite(reps):
            raise ValueError("Invalid measurement")
        p = subjects.setdefault(pid, {"n": 0, "accuracy": 0., "checks": 0., "trials": []})
        p["n"] += 1
        p["accuracy"] += a
        p["checks"] += reps
        if is_critical:
            day = float(row["day"])
            if not day.is_integer() or row["stakes"] not in ("high", "low") or row["counterbalance"] not in ("0", "1"):
                raise ValueError("Malformed diagnostic design")
            p["trials"].append((int(day), row["stakes"], int(c), row["counterbalance"]))

    eligible = []
    for p in subjects.values():
        if p["accuracy"] / p["n"] < 0.45 or p["checks"] / p["n"] > 2:
            continue
        seq = sorted(p["trials"])
        if [x[0] for x in seq] != list(CRITICAL_DAYS):
            raise ValueError("Diagnostic days incomplete or duplicated")
        stakes = "".join("H" if x[1] == "high" else "L" for x in seq)
        if stakes not in ("HLHLHLHL", "LHLHLHLH"):
            raise ValueError("Diagnostic conditions do not alternate")
        counters = {x[3] for x in seq}
        if counters != ({"1"} if stakes[0] == "H" else {"0"}):
            raise ValueError("Counterbalance mismatch")
        copy = [x[2] for x in seq]
        hc = sum(x[2] for x in seq if x[1] == "high")
        lc = sum(x[2] for x in seq if x[1] == "low")
        eligible.append({"first": "high" if stakes[0] == "H" else "low",
                         "copy": copy,
                         "early_minus_late": (copy[0] + copy[1] - copy[6] - copy[7]) / 2,
                         "slope": sum((j - 3.5) * y for j, y in enumerate(copy)) / 42,
                         "stake_delta": (hc - lc) / 4})
    if len(eligible) < 10:
        raise ValueError("Too few participants")
    high = [p for p in eligible if p["first"] == "high"]
    low = [p for p in eligible if p["first"] == "low"]
    if not high or not low:
        raise ValueError("Both condition sequences are required")

    def avg(items, key):
        return sum(p[key] for p in items) / len(items)

    block_rates = [sum(p["copy"][j] for p in eligible) / len(eligible) for j in range(8)]
    observed = {"early_minus_late": avg(eligible, "early_minus_late"),
                "slope_per_block": avg(eligible, "slope"),
                "high_first_stake_delta": avg(high, "stake_delta"),
                "low_first_stake_delta": avg(low, "stake_delta")}
    observed["difference_between_sequences"] = observed["high_first_stake_delta"] - observed["low_first_stake_delta"]

    # Xorshift32; bootstrap resamples people and preserves within-person trials.
    state = seed & 0xffffffff
    def random():
        nonlocal state
        state ^= (state << 13) & 0xffffffff
        state ^= state >> 17
        state ^= (state << 5) & 0xffffffff
        state &= 0xffffffff
        return state / 4294967296.0

    boot = {key: [] for key in observed}
    for _ in range(draws):
        sample = [eligible[int(random() * len(eligible))] for _ in eligible]
        hi = [high[int(random() * len(high))] for _ in high]
        lo = [low[int(random() * len(low))] for _ in low]
        vals = {"early_minus_late": avg(sample, "early_minus_late"),
                "slope_per_block": avg(sample, "slope"),
                "high_first_stake_delta": avg(hi, "stake_delta"),
                "low_first_stake_delta": avg(lo, "stake_delta")}
        vals["difference_between_sequences"] = vals["high_first_stake_delta"] - vals["low_first_stake_delta"]
        for key in boot:
            boot[key].append(vals[key])
    intervals = {}
    for key, values in boot.items():
        values.sort()
        intervals[key] = [values[math.floor(.025 * (draws - 1))],
                          values[math.ceil(.975 * (draws - 1))]]
    return {"status": "EXPLORATORY_RETROSPECTIVE_ORDER_AUDIT",
            "n": len(eligible), "sequence_counts": {"HLHLHLHL": len(high), "LHLHLHLH": len(low)},
            "critical_copying_by_block": block_rates,
            "first_two_copy_rate": (block_rates[0] + block_rates[1]) / 2,
            "last_two_copy_rate": (block_rates[6] + block_rates[7]) / 2,
            "observed": observed,
            "bootstrap": {"seed": seed, "draws": draws, "CI95": intervals}}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = order_audit(parse_verified(args.source.read_bytes()))
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": result["status"], "n": result["n"]}))


if __name__ == "__main__":
    main()
