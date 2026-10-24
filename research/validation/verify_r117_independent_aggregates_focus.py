#!/usr/bin/env python3
"""Independent published rounded aggregate and artificial focus audit of R117."""
import importlib.util
import json
from decimal import Decimal
from fractions import Fraction
from pathlib import Path

FIGURE = ((31, 6), (50, 14), (24, 54), (34, 32))
ENERGY = ((64, "21.47", "20.25"), (79, "10.38", "11.27"),
          (63, "20.63", "18.91"), (81, "10.34", "10.58"))


def rounded_percent(count, n):
    return (200 * count + n) // (2 * n)


def reconstruct_counts(cells):
    candidates = [[k for k in range(n + 1) if rounded_percent(k, n) == p]
                  for n, p in cells]
    assert all(len(x) == 1 for x in candidates), "ROUNDING_AMBIGUITY"
    return [x[0] for x in candidates]


def exact_focus(d, i, focus_d, focus_i):
    return (Fraction(1, 2)
            + (d - Fraction(1, 2)) * Fraction(int(focus_d), 2)
            + (i - Fraction(1, 2)) * Fraction(int(focus_i), 2))


def main():
    counts = reconstruct_counts(FIGURE)
    assert counts == [2, 7, 13, 11]
    assert sum(n for n, _ in FIGURE) == 139
    p = [pct for n, pct in FIGURE]
    assert (p[0] - p[1], p[2] - p[3], p[2] - p[3] - p[0] + p[1]) == (-8, 22, 30)
    fractions = [Fraction(k, n) for k, (n, _) in zip(counts, FIGURE)]
    exact_did = fractions[2] - fractions[3] - fractions[0] + fractions[1]
    assert exact_did == Fraction(92843, 316200)
    assert exact_did != Fraction(30, 100)
    changes = [Decimal(end) - Decimal(start) for _, start, end in ENERGY]
    assert changes == [Decimal("-1.22"), Decimal("0.89"),
                       Decimal("-1.72"), Decimal("0.24")]
    assert sum(n for n, _, _ in ENERGY) == 287 == 290 - 3
    focus = {(fd, fi): exact_focus(Fraction(1, 5), Fraction(9, 10), fd, fi)
             for fd in (False, True) for fi in (False, True)}
    assert focus == {(False, False): Fraction(1, 2),
                     (True, False): Fraction(7, 20),
                     (False, True): Fraction(7, 10),
                     (True, True): Fraction(11, 20)}
    assert exact_focus(Fraction(4, 5), Fraction(4, 5), True, False) == Fraction(13, 20)
    assert exact_focus(Fraction(4, 5), Fraction(4, 5), False, True) == Fraction(13, 20)

    path = Path("research/R117/r117_descriptive_injunctive_norms_published_aggregate_focus.py")
    assert path.is_file()
    spec = importlib.util.spec_from_file_location("r117_original", path)
    assert spec is not None and spec.loader is not None
    import sys
    original = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = original
    spec.loader.exec_module(original)
    first = original.published_1990_figure1_arithmetic()
    second = original.published_2007_short_term_arithmetic()
    assert [r["integer_litter_count_uniquely_inferred_from_printed_rounding"]
            for r in first["published_groups"]] == counts
    assert Fraction(first["uniquely_inferred_integer_count_interaction_fraction_exact"]) == exact_did
    assert [Decimal(r["simple_difference_of_published_rounded_means_kwh_day"])
            for r in second["source_short_term_4_cells"]] == changes
    for (fd, fi), expected in focus.items():
        observed = original.toy_prosocial_action_probability(
            Fraction(1, 5), Fraction(9, 10),
            focus_descriptive=fd, focus_injunctive=fi)
        assert observed == expected, (fd, fi, observed, expected)

    # Two corruptions must be rejected by independent arithmetic.
    corrupted_figure = list(FIGURE)
    corrupted_figure[0] = (31, 14)
    try:
        altered = reconstruct_counts(corrupted_figure)
    except AssertionError:
        altered = []
    assert altered != counts
    corrupted_energy = list(ENERGY)
    corrupted_energy[1] = (79, "10.38", "11.28")
    assert [Decimal(end) - Decimal(start) for _, start, end in corrupted_energy] != changes
    print(json.dumps({
        "research_id": "R117", "catalogue_id": "03-009",
        "published_1990_inferred_counts": counts,
        "published_1990_exact_fraction_DID": str(exact_did),
        "published_2007_changes_kwh_day": [str(x) for x in changes],
        "focus_worlds": {str(k): str(v) for k, v in focus.items()},
        "tamper_controls_rejected": 2,
        "status": "PASS_BOUNDED_INTERNAL_AGGREGATE_AND_SYNTHETIC_E1",
        "new_human_E2": 0, "new_historical_E3": 0,
        "external_replication": False, "R073": "FROZEN", "PESEN_v0_1": "FROZEN"
    }, sort_keys=True, indent=2))


if __name__ == "__main__":
    main()
