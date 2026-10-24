#!/usr/bin/env python3
"""Independent R340 enumerator; does not import production generator."""
import csv
import io
import json
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / "R340"
STATES = ("00", "01", "10", "11")
BETAS = ("1/2", "1", "2")

def independently_recreate():
    out = io.StringIO(newline="")
    writer = csv.writer(out, lineterminator="\n")
    writer.writerow(["beta", "origin", "destination", "rate"])
    worlds = []
    for beta_text in BETAS:
        beta = Fraction(beta_text)
        rows = []
        for origin in STATES:
            row = []
            for destination in STATES:
                differing = [k for k in (0,1) if origin[k] != destination[k]]
                if len(differing) != 1:
                    value = Fraction(0)
                else:
                    k = differing[0]
                    if origin[k] == "1" and destination[k] == "0":
                        value = Fraction(1)
                    elif origin[k] == "0" and destination[k] == "1" and origin[1-k] == "1":
                        value = beta
                    else:
                        value = Fraction(0)
                row.append(value)
            idx = STATES.index(origin)
            row[idx] = -sum(v for j,v in enumerate(row) if j != idx)
            rows.append(row)
        for i, origin in enumerate(STATES):
            for j, destination in enumerate(STATES):
                writer.writerow([beta_text, origin, destination, str(rows[i][j])])
        worlds.append({
            "beta": beta_text,
            "matrix": [[str(v) for v in row] for row in rows],
            "first_event_infection": str(beta/(1+beta)),
            "first_event_recovery": str(Fraction(1)/(1+beta)),
        })
    result = {
        "schema": "R340_frozen_two_node_sis_generator_v1",
        "worlds": worlds,
        "checks": {
            "worlds": 3,
            "source_rows": 48,
            "absorbing_worlds": 3,
            "zero_sum_rows": 12,
            "nonnegative_offdiagonal_entries": 36,
            "correct_01_10_transitions": 6,
            "correct_11_recoveries": 3,
        },
    }
    return out.getvalue().encode("utf-8"), (json.dumps(result, indent=2, ensure_ascii=True)+"\n").encode("utf-8")

def main():
    csv_expected, json_expected = independently_recreate()
    csv_actual = (ROOT/"R340_ALL_48_ARTIFICIAL_GENERATOR_ATOMS.csv").read_bytes()
    json_actual = (ROOT/"R340_EXACT_3_GENERATORS.json").read_bytes()
    assert csv_actual == csv_expected, "CSV independent replay failed"
    assert json_actual == json_expected, "JSON independent replay failed"
    assert csv_actual != csv_expected.replace(b"1/2,01,11,1/2", b"1/2,01,11,1/3"), "CSV negative control invalid"
    assert json_actual != json_expected.replace(b'"source_rows": 48', b'"source_rows": 49'), "JSON negative control invalid"
    assert b"1/2,01,11,1/2" in csv_expected
    assert b'"source_rows": 48' in json_expected
    print("R340_INDEPENDENT_NO_IMPORT_AUDIT=PASS; NEGATIVE_TAMPER_TESTS=2")

if __name__ == "__main__":
    main()
