#!/usr/bin/env python3
"""MKT173: exact synthetic correlation and withdrawal tail comparison.

No product code, real customer data, market calibration or paid service is used.
"""
from fractions import Fraction as F
from itertools import product

INITIAL = F(100)
WITHDRAWAL = F(30)
THRESHOLD = F(35)
SHOCKS = (-1, 1)
AMPLITUDE = F(2, 5)


def simulate(shocks, cross_asset_sign):
    """Two equally weighted assets, annual rebalancing and start-year withdrawal."""
    capital = INITIAL
    for shock in shocks:
        asset1 = F(shock) * AMPLITUDE
        asset2 = F(shock * cross_asset_sign) * AMPLITUDE
        portfolio_return = (asset1 + asset2) / 2
        capital = (capital - WITHDRAWAL) * (1 + portfolio_return)
    return capital


def summarize(cross_asset_sign):
    values = tuple(simulate(path, cross_asset_sign) for path in product(SHOCKS, repeat=2))
    success = sum(value >= THRESHOLD for value in values)
    return {"paths": values, "mean": sum(values) / len(values),
            "success_count": success, "total": len(values),
            "worst_quartile": min(values)}


def check(condition, message):
    if not condition:
        raise ValueError(message)


def run():
    positive = summarize(1)
    negative = summarize(-1)
    check(positive["paths"] == (F(36, 5), F(84, 5), F(204, 5), F(476, 5)), "positive paths")
    check(negative["paths"] == (F(40),) * 4, "negative paths")
    check(positive["mean"] == negative["mean"] == F(40), "mean")
    check(positive["success_count"] == 2, "positive success")
    check(negative["success_count"] == 4, "negative success")
    check(positive["worst_quartile"] == F(36, 5), "positive tail")
    check(negative["worst_quartile"] == F(40), "negative tail")
    check(sum(F(s) * AMPLITUDE for s in SHOCKS) == 0, "marginal mean")
    check(F(2, 5) ** 2 == F(4, 25), "marginal variance")
    # Same single-asset marginal returns in both scenarios.
    for asset in (0, 1):
        for sign in (1, -1):
            marginal = sorted((F(s) * AMPLITUDE if asset == 0 else F(s * sign) * AMPLITUDE) for s in SHOCKS)
            check(marginal == [-F(2, 5), F(2, 5)], "marginal distribution")
    print("MKT173 PASS")
    for name, result in (("positive_correlation", positive), ("negative_correlation", negative)):
        print(name, "paths", [str(x) for x in result["paths"]],
              "mean", str(result["mean"]),
              "success", f'{result["success_count"]}/{result["total"]}',
              "worst_quartile", str(result["worst_quartile"]))


if __name__ == "__main__":
    run()
