#!/usr/bin/env python3
"""Bounded standard-library audit of Henrich (2004) Appendix A3/A4."""
import math

EULER_GAMMA = 0.5772156649015329

def midpoint_integral(a, beta, n, correct_density):
    mode_max = a + beta * math.log(n)
    low, high = mode_max - 20.0 * beta, mode_max + 25.0 * beta
    steps = 40000
    dx = (high - low) / steps
    total = 0.0
    for k in range(steps):
        x = low + (k + 0.5) * dx
        u = math.exp((a - x) / beta)
        integrand = n * u * math.exp(-n * u) * x
        if correct_density:
            integrand /= beta
        total += integrand
    return total * dx

def main():
    cases = [(4.0, 1.0, 100), (4.0, 2.0, 100),
             (4.0, 0.5, 100), (5.0, 1.7, 25)]
    for a, beta, n in cases:
        formula_a4 = a + beta * (EULER_GAMMA + math.log(n))
        printed_a3 = midpoint_integral(a, beta, n, False)
        corrected_a3 = midpoint_integral(a, beta, n, True)
        assert abs(corrected_a3 - formula_a4) < 1e-6
        assert abs(printed_a3 - beta * formula_a4) < 1e-6
        print(f"a={a}, beta={beta}, N={n}: printed A3={printed_a3:.9f}, "
              f"corrected A3={corrected_a3:.9f}, A4={formula_a4:.9f}")
    def growth(n, cost):
        return -0.5 + EULER_GAMMA + (1.0 - cost) * math.log(n)
    assert growth(1, 2.0) > 0
    assert growth(4, 2.0) < 0
    assert growth(4, 0.0) > growth(1, 0.0)
    print("PASS: 8 integral checks and 3 constructive extension checks")

if __name__ == "__main__":
    main()
