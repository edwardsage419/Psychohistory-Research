#!/usr/bin/env python3
"""R321 S117: exact finite sequential forced-terminal choice; artificial E1."""
import argparse
import csv
import itertools
import json
from fractions import Fraction as Q
from pathlib import Path

PAIRS = ((Q(1, 4), Q(3, 4)), (Q(1, 3), Q(2, 3)))
FIELDS = ("world_id", "p0", "p1", "K", "true_hypothesis", "p_true",
          "path_bits", "ones", "full_path_probability", "stop_time", "decision", "censored")

def compute(source_csv=None):
    expected_rows = {}
    out = []
    for p0, p1 in PAIRS:
        for k in (2, 3):
            for truth in ("H0", "H1"):
                wid = len(out)
                p = p0 if truth == "H0" else p1
                d = {name: Q(0) for name in ("S_H0", "S_H1", "F_H0", "F_H1", "S_error",
                    "F_error", "disagree", "disagree_early", "disagree_censored",
                    "observed_steps", "A_censor", "A_error", "A_decided")}
                for bits in itertools.product((0, 1), repeat=7):
                    bitstr = "".join(map(str, bits))
                    mass = p ** sum(bits) * (1-p) ** (7-sum(bits))
                    score, stop, a = 0, 7, None
                    for t, bit in enumerate(bits, 1):
                        score += 2*bit-1
                        if abs(score) >= k:
                            stop, a = t, ("H1" if score > 0 else "H0")
                            break
                    fixed = "H1" if sum(bits) >= 4 else "H0"
                    seq = a or fixed
                    d["S_"+seq] += mass
                    d["F_"+fixed] += mass
                    d["S_error"] += mass * (seq != truth)
                    d["F_error"] += mass * (fixed != truth)
                    d["observed_steps"] += mass * stop
                    if seq != fixed:
                        d["disagree"] += mass
                        d["disagree_early" if a else "disagree_censored"] += mass
                    if a is None:
                        d["A_censor"] += mass
                    else:
                        d["A_decided"] += mass
                        d["A_error"] += mass * (a != truth)
                    expected_rows[(str(wid), bitstr)] = {
                        "world_id": str(wid), "p0": str(p0), "p1": str(p1),
                        "K": str(k), "true_hypothesis": truth, "p_true": str(p),
                        "path_bits": bitstr, "ones": str(sum(bits)),
                        "full_path_probability": str(mass),
                        "stop_time": str(stop) if a else "",
                        "decision": a or "none", "censored": str(a is None).lower()
                    }
                assert d["S_H0"]+d["S_H1"] == d["F_H0"]+d["F_H1"] == 1
                assert d["disagree_censored"] == 0
                out.append(dict(world_id=wid, p0=str(p0), p1=str(p1), K=k,
                    truth=truth, source_paths=128, **{name:str(value) for name,value in d.items()},
                    S_minus_F_error=str(d["S_error"]-d["F_error"]),
                    A_conditional_error=str(d["A_error"]/d["A_decided"])))
    if source_csv is not None:
        with open(source_csv, newline="", encoding="utf-8") as f:
            rows = list(csv.DictReader(f))
        if len(rows) != 1024 or len({(r["world_id"],r["path_bits"]) for r in rows}) != 1024:
            raise ValueError("original source count or uniqueness changed")
        for row in rows:
            if set(row) != set(FIELDS) or expected_rows.get((row["world_id"],row["path_bits"])) != row:
                raise ValueError("original source field mismatch")
    return out

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--source-csv", type=Path)
    ap.add_argument("--output", type=Path)
    args = ap.parse_args()
    result = {"schema":"r321_s117_terminal_forced_choice_e1_v1",
              "original_source_rows":1024, "world_count":8, "evidence":"E1_SYNTHETIC_ONLY",
              "worlds":compute(args.source_csv)}
    body = json.dumps(result, indent=2, ensure_ascii=False)+"\n"
    if args.output:
        args.output.write_text(body, encoding="utf-8")
    else:
        print(body, end="")
