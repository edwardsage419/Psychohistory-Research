"""Exact arithmetic audit of Schelling (1969) p.491 threshold compatibility.

The script tests logical feasibility only. It does not reproduce the paper's
spatial dynamics or estimate historical segregation.
"""
from fractions import Fraction as F


def acceptable(white_count: int, black_count: int, white_limit: F, black_limit: F) -> bool:
    assert white_count > 0 and black_count > 0
    return (F(black_count, white_count) <= white_limit
            and F(white_count, black_count) <= black_limit)


def run() -> None:
    checks = 0

    def check(value: bool) -> None:
        nonlocal checks
        assert value
        checks += 1

    # Boundary product == 1 permits an exactly feasible mixed ratio.
    a, b = F(3, 2), F(2, 3)
    check(a * b == 1)
    check(acceptable(2, 3, a, b))
    check(F(3, 2) == a)
    check(F(2, 3) == b)

    # Product > 1 permits a positive-width feasible interval.
    a, b = F(2, 1), F(1, 1)
    check(a * b > 1)
    check(F(1, b) < a)
    check(acceptable(2, 3, a, b))
    check(acceptable(1, 1, a, b))

    # Product < 1 rules out all positive mixed ratios.
    a, b = F(3, 2), F(1, 2)
    check(a * b < 1)
    check(F(1, b) > a)
    for w in range(1, 21):
        for k in range(1, 21):
            check(not acceptable(w, k, a, b))

    print(f"PASS: {checks} exact arithmetic/logical checks; synthetic only")


if __name__ == "__main__":
    run()
