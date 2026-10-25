"""Independent B audit for R162: enumerate physical tickets, group observables.
No import of R162 original program or third-method JavaScript.
Python standard library only.
"""
from collections import Counter, defaultdict
from fractions import Fraction
from itertools import product
import json

PATTERNS = ((0, 0, 0), (1, 0, 0), (0, 1, 1), (1, 1, 1))

def run():
    partitions = [defaultdict(list) for _ in range(4)]
    rows = []
    for y, chosen, bonus, correct in product(PATTERNS, range(3), (0, 1, 3), (0, 1)):
        tickets = (0, 1, 2) + (chosen,) * bonus
        observed = Fraction(sum(y[index] for index in tickets), len(tickets))
        neutral = Fraction(sum(y), 3)
        advantage = (observed - neutral) * (2 * correct - 1)
        row = (y, chosen, bonus, correct, observed, advantage)
        rows.append(row)
        for key, bucket in zip(
            ((observed,), (observed, y), (observed, y, correct),
             (observed, y, correct, bonus)), partitions
        ):
            bucket[key].append(row)

    def summary(bucket):
        classes = list(bucket.values())
        mixed = [group for group in classes
                 if len({(r[5] > 0) - (r[5] < 0) for r in group}) > 1]
        return {
            "class_count": len(classes),
            "class_size_histogram": {str(k): v for k, v in sorted(
                Counter(map(len, classes)).items())},
            "maximum_class_size": max(map(len, classes)),
            "non_singleton_worlds": sum(len(g) for g in classes if len(g) > 1),
            "mixed_advantage_sign_classes": len(mixed),
            "mixed_advantage_sign_worlds": sum(map(len, mixed)),
        }

    def lookup(y, chosen, bonus, correct):
        return next(r for r in rows if r[:4] == (y, chosen, bonus, correct))
    a = lookup((1, 0, 0), 0, 3, 1)
    b = lookup((0, 1, 1), 0, 0, 1)
    c = lookup((1, 0, 0), 0, 3, 0)
    assert a[4:] == (Fraction(2, 3), Fraction(1, 3))
    assert b[4:] == (Fraction(2, 3), Fraction(0))
    assert c[4:] == (Fraction(2, 3), Fraction(-1, 3))
    neutral_mutant_detected = sum(r[4] != Fraction(sum(r[0]), 3) for r in rows)
    correctness_mutant_detected = sum(r[5] != 0 for r in rows)
    assert len(rows) == 72
    assert neutral_mutant_detected == 24
    assert correctness_mutant_detected == 24
    return {
        "audit": "B_R162_INTERNAL_INDEPENDENT_PYTHON",
        "verified_generated_worlds": len(rows),
        "partitions": {f"P{i}": summary(d) for i, d in enumerate(partitions)},
        "mutants": {
            "neutral_copying_detected": neutral_mutant_detected,
            "reverse_correct_token_detected": correctness_mutant_detected,
        },
        "scope": "E1_SYNTHETIC_ONLY",
        "E2": 0,
        "E3": 0,
        "external_reproduction": 0,
    }

if __name__ == "__main__":
    print(json.dumps(run(), ensure_ascii=False, indent=2))
