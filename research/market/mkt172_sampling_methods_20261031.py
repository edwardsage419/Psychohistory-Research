#!/usr/bin/env python3
"""MKT172: finite synthetic sampling-method comparison; not ProjectionLab implementation."""
from fractions import Fraction as F
from itertools import product
from collections import Counter
import random

RETURNS = (F(-1, 2), F(0), F(1, 2), F(1))
START = F(100)
WITHDRAW = F(40)

def evaluate(path):
    wealth = START
    balances = []
    for rate in path:
        wealth = wealth * (1 + rate) - WITHDRAW
        balances.append(wealth)
    return all(x >= 0 for x in balances), tuple(balances)

def sample_summary(paths):
    outcomes = [evaluate(path)[0] for path in paths]
    return {"paths": len(paths), "success": sum(outcomes),
            "rate": str(F(sum(outcomes), len(outcomes)))}

def main():
    historical_no_loop = [RETURNS[i:i+2] for i in range(len(RETURNS)-1)]
    circular_start = [(RETURNS[i], RETURNS[(i+1) % 4]) for i in range(4)]
    independent_draw = list(product(RETURNS, repeat=2))
    results = {"historical_no_loop_analogue": sample_summary(historical_no_loop),
               "circular_start_analogue": sample_summary(circular_start),
               "iid_with_replacement_analogue": sample_summary(independent_draw)}
    assert len(historical_no_loop) == 3
    assert len(circular_start) == 4
    assert len(independent_draw) == 16
    assert len(set(independent_draw)) == 16
    assert results["historical_no_loop_analogue"]["rate"] != results["iid_with_replacement_analogue"]["rate"]
    assert evaluate((F(-1,2), F(1)))[1] == (F(10), F(-20))
    assert evaluate((F(1), F(-1,2)))[1] == (F(160), F(40))
    rng1 = random.Random(172)
    rng2 = random.Random(172)
    draws1 = [tuple(rng1.choice(RETURNS) for _ in range(2)) for _ in range(2000)]
    draws2 = [tuple(rng2.choice(RETURNS) for _ in range(2)) for _ in range(2000)]
    assert draws1 == draws2
    assert sample_summary(draws1[:20])["rate"] != sample_summary(draws1)["rate"]
    results["seed172_first20"] = sample_summary(draws1[:20])
    results["seed172_first2000"] = sample_summary(draws1)
    print(results)
    print("PASS 9 synthetic assertions")

if __name__ == "__main__":
    main()
