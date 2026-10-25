"""Independent R152 OD multinomial symmetry audit; exact synthetic E1 only."""
from fractions import Fraction
from math import factorial, prod
import json

TABLES = {
    "A": ((0, 0, 2), (1, 0, 2), (1, 3, 0)),
    "B": ((0, 1, 1), (0, 0, 3), (2, 2, 0)),
}
POP = (2, 3, 4)
COORDS = (0, 1, 3)


def margins(table):
    return (tuple(map(sum, table)), tuple(sum(table[i][j] for i in range(3)) for j in range(3)))


def pair_totals(table):
    return tuple(table[i][j] + table[j][i] for i in range(3) for j in range(i + 1, 3))


def coefficient(table):
    return Fraction(prod(factorial(sum(row)) for row in table), prod(factorial(v) for row in table for v in row))


def likelihood(table, alpha, directed=False):
    probability = coefficient(table)
    for i in range(3):
        kernel = [Fraction(0) if i == j else Fraction(POP[i] * POP[j], abs(COORDS[i] - COORDS[j]) ** alpha) * (2 if directed and i < j else 1) for j in range(3)]
        normalizer = sum(kernel)
        for j in range(3):
            if table[i][j]:
                probability *= (kernel[j] / normalizer) ** table[i][j]
    return probability


def run():
    a, b = TABLES["A"], TABLES["B"]
    assert margins(a) == margins(b) == ((2, 3, 4), (2, 3, 4))
    assert pair_totals(a) == pair_totals(b) == (1, 3, 5)
    assert coefficient(a) == coefficient(b) == 12
    rows = []
    for alpha in (0, 1, 2):
        la, lb = likelihood(a, alpha), likelihood(b, alpha)
        assert la == lb
        directed_a, directed_b = likelihood(a, alpha, True), likelihood(b, alpha, True)
        assert directed_b / directed_a == 2
        rows.append({"alpha": alpha, "multinomial_coefficient_A": str(coefficient(a)), "multinomial_coefficient_B": str(coefficient(b)), "likelihood_A": str(la), "likelihood_B": str(lb), "directed_likelihood_ratio_B_over_A": str(directed_b / directed_a)})
    return {"id": "B_R152_MULTINOMIAL_OD_SYMMETRY", "evidence": "E1_SYNTHETIC_ONLY", "row_margins": list(margins(a)[0]), "column_margins": list(margins(a)[1]), "undirected_pair_totals": list(pair_totals(a)), "rows": rows, "all_3_symmetric_likelihood_ties": True, "all_3_asymmetric_mutants_rejected": True, "external_replication": False}


if __name__ == "__main__":
    print(json.dumps(run(), ensure_ascii=False, sort_keys=True, indent=2))
