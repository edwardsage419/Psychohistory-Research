"""R151 B audit: independent exact Fraction cohort accounting and observability.
Usage: python r151_b_independent_fraction_observability.py [main_receipt.json]
Only project-created synthetic E1 evidence. No empirical population claims.
"""
from fractions import Fraction as F
from itertools import product
from collections import Counter
import json
import sys


def totals(initial, fertility, juvenile_survival, adult_survival):
    j, a, o = (F(x) for x in initial)
    k, sj, sa = fertility, juvenile_survival, adult_survival
    n0 = j + a + o
    j1, a1, o1 = k * (a + o / 2), sj * j, sa * a
    n1 = j1 + a1 + o1
    j2, a2, o2 = k * (a1 + o1 / 2), sj * j1, sa * a1
    n2 = j2 + a2 + o2
    j3, a3, o3 = k * (a2 + o2 / 2), sj * j2, sa * a2
    return n0, n1, n2, j3 + a3 + o3


def det3(rows):
    a, b, c = rows
    return (a[0] * (b[1] * c[2] - b[2] * c[1])
            - a[1] * (b[0] * c[2] - b[2] * c[0])
            + a[2] * (b[0] * c[1] - b[1] * c[0]))


def independent_audit():
    cohorts = [(j, a, 12-j-a) for j in range(13) for a in range(13-j)]
    assert len(cohorts) == 91
    cases = []
    for k, sj, sa in product((F(0), F(1), F(3, 2)),
                             (F(1, 2), F(3, 4)), (F(1, 2), F(2, 3))):
        paths = [totals(x, k, sj, sa) for x in cohorts]
        stats = []
        for t in range(4):
            groups = Counter(p[:t+1] for p in paths)
            sizes = list(groups.values())
            stats.append(dict(last_observed_t=t,
                              distinct_signatures=len(groups),
                              max_class_size=max(sizes),
                              indistinguishable_pairs=sum(n*(n-1)//2 for n in sizes)))
        # Independent determinant from direct accounting on each unit-basis input.
        columns = [totals(tuple(int(i == j) for i in range(3)), k, sj, sa)
                   for j in range(3)]
        observation_rows = [tuple(columns[j][i] for j in range(3))
                            for i in range(3)]
        determinant = det3(observation_rows)
        cases.append(dict(fertility=str(k), juvenile_survival=str(sj),
                          adult_survival=str(sa), observability_det=str(determinant),
                          stats=stats))
    assert len(cases) == 12
    assert all(F(c["observability_det"]) != 0 for c in cases)
    assert all(c["stats"][2]["distinct_signatures"] == 91 for c in cases)
    assert sum(c["stats"][1]["distinct_signatures"] == 91 for c in cases) == 2
    assert sum(c["stats"][1]["distinct_signatures"] < 91 for c in cases) == 10
    return cases


if __name__ == "__main__":
    cases = independent_audit()
    if len(sys.argv) == 2:
        with open(sys.argv[1], encoding="utf-8") as fh:
            receipt = json.load(fh)
        assert len(receipt["parameter_rows"]) == len(cases)
        for main, independent in zip(receipt["parameter_rows"], cases):
            assert main["fertility"] == independent["fertility"]
            assert main["juvenile_survival"] == independent["juvenile_survival"]
            assert main["adult_survival"] == independent["adult_survival"]
            assert F(main["observability_det_numerator"], main["observability_det_denominator"]) == F(independent["observability_det"])
            assert main["stats"] == independent["stats"]
    print(json.dumps({"research_id": "R151", "audit": "INTERNAL_INDEPENDENT_METHOD_E1",
                      "parameter_sets": len(cases),
                      "full_rank_sets": sum(F(c["observability_det"]) != 0 for c in cases),
                      "finite_unique_two_observation_sets": sum(c["stats"][1]["distinct_signatures"] == 91 for c in cases),
                      "finite_unique_three_observation_sets": sum(c["stats"][2]["distinct_signatures"] == 91 for c in cases),
                      "cross_method_receipt_compared": len(sys.argv) == 2}, sort_keys=True))
