#!/usr/bin/env python3
"""Independent local SHA256 regeneration of original R266 source CSV.
Runs offline with Python standard library. This reconstructs the frozen
four-value design, never downloads or overwrites the archived original CSV.
"""
import csv
import hashlib
import io
import itertools
from fractions import Fraction as F

EXPECTED = "5e0aac41c960ee21b54d3266064793a7e9a2454dbb4493ae8e4451591d48587a"
FIELDS = ("world", "function", "evaluations", "design", "primitive_independent_draws",
          "original_source_tuple", "exact_source_mass", "event_success_count",
          "estimate", "true_integral", "squared_error")
WORLDS = tuple((f, n) for f in ("THRESHOLD_Q1", "THRESHOLD_HALF", "THRESHOLD_Q3")
               for n in (2, 4)) + tuple(("SYMMETRIC_EXTREMES", n) for n in (2, 4, 6))


def event(fn, u):
    if fn == "THRESHOLD_Q1":
        return int(u == 0)
    if fn == "THRESHOLD_HALF":
        return int(u <= 1)
    if fn == "THRESHOLD_Q3":
        return int(u <= 2)
    if fn == "SYMMETRIC_EXTREMES":
        return int(u in (0, 3))
    raise ValueError("unexpected frozen function")


def regenerate():
    stream = io.StringIO(newline="")
    writer = csv.DictWriter(stream, fieldnames=FIELDS, lineterminator="\n")
    writer.writeheader()
    count = 0
    for fn, n in WORLDS:
        truth = F(sum(event(fn, u) for u in range(4)), 4)
        for design in ("IID", "ANTITHETIC"):
            draws = n if design == "IID" else n // 2
            for origin in itertools.product(range(4), repeat=draws):
                hit = sum(event(fn, u) if design == "IID"
                          else event(fn, u) + event(fn, 3 - u) for u in origin)
                est = F(hit, n)
                row = dict(world=f"{fn}_N{n}", function=fn, evaluations=n,
                           design=design, primitive_independent_draws=draws,
                           original_source_tuple=";".join(map(str, origin)),
                           exact_source_mass=F(1, 4 ** draws),
                           event_success_count=hit, estimate=est,
                           true_integral=truth, squared_error=(est - truth) ** 2)
                writer.writerow({key: str(row[key]) for key in FIELDS})
                count += 1
    return stream.getvalue().encode("utf-8"), count


if __name__ == "__main__":
    content, count = regenerate()
    digest = hashlib.sha256(content).hexdigest()
    if count != 5328 or digest != EXPECTED:
        raise SystemExit(f"FAIL rows={count} bytes={len(content)} sha256={digest}")
    print(f"PASS rows={count} bytes={len(content)} sha256={digest}")
