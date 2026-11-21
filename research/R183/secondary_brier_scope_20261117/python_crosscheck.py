"""Independent Python/Fraction spot controls for the R183 Brier scope audit.

Only synthetic binomial cases. The full 45-world verification uses the
separate archived-PMF JavaScript verifier.
"""
from fractions import Fraction as F
from math import comb


def require(condition: bool, message: str) -> None:
    """Keep scientific checks active under python -O."""
    if condition is not True:
        raise ValueError(message)


def evaluate(n: int, p: F):
    require(type(n) is int and n > 0, "NONPOSITIVE_N")
    require(isinstance(p, F) and F(0) <= p <= F(1), "INVALID_PROBABILITY")
    masses = [F(comb(n, k)) * p**k * (1 - p)**(n - k)
              for k in range(n + 1)]
    require(sum(masses) == 1, "BINOMIAL_PMF_NOT_NORMALIZED")
    require(sum((k * mass for k, mass in enumerate(masses)), F(0)) == n * p,
            "BINOMIAL_MARGINAL_MEAN_MISMATCH")

    def brier(q: F):
        return p * (1 - q)**2 + (1 - p) * q**2

    mle = sum((mass * brier(F(k, n))
               for k, mass in enumerate(masses)), F(0))
    half = sum((mass * brier(F(2 * k + 1, 2 * n + 2))
                for k, mass in enumerate(masses)), F(0))
    variance = sum((mass * (F(k, n) - p)**2
                    for k, mass in enumerate(masses)), F(0))
    analytic = (F(2 * n + 1) * variance - (F(1, 2) - p)**2) / (n + 1)**2
    require(mle - half == analytic, "BASIC_BRIER_RISK_MOMENT_IDENTITY_FAILED")
    return mle, half, analytic


def main():
    cases = (
        (4, F(1, 100), (F(99, 8000), F(659, 31250), F(-8713, 1000000))),
        (4, F(1, 4), (F(15, 64), F(11, 50), F(23, 1600))),
        (12, F(1, 8), (F(91, 768), F(319, 2704), F(67, 129792))),
    )
    for n, p, expected in cases:
        got = evaluate(n, p)
        require(got == expected, f"SPOT_CHECK_MISMATCH: n={n} p={p} actual={got} expected={expected}")
        print(f"PASS n={n}, p={p}, MLE={got[0]}, half={got[1]}, delta={got[2]}")
    print("PYTHON_FRACTION_SPOT_CHECK_PASS 3")


if __name__ == "__main__":
    main()
