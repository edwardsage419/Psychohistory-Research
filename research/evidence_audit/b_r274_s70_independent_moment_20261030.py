#!/usr/bin/env python3
"""R274 S70 independent exact-moment oracle; no source enumeration or R import."""
from fractions import Fraction as F

REGIMES = {
    "STABLE_HALF": (F(1, 2), F(1, 2)),
    "RISING_RATE": (F(1, 4), F(3, 4)),
    "FALLING_RATE": (F(3, 4), F(1, 4)),
}
POLICIES = ("PAST_FIXED", "ONLINE_ONE_STEP", "PRECOMMITTED_HALF")

def risk(a, b, policy, t):
    if policy == "PRECOMMITTED_HALF":
        mean, variance = F(1, 2), F(0)
    elif policy == "ONLINE_ONE_STEP" and t == 6:
        mean = (4 * a + b + 1) / 7
        variance = (4 * a * (1 - a) + b * (1 - b)) / 49
    else:
        mean = (4 * a + 1) / 6
        variance = 4 * a * (1 - a) / 36
    return b * (1 - b) + variance + (mean - b) ** 2

def exact_results():
    return {(regime, policy): (risk(a, b, policy, 5), risk(a, b, policy, 6))
            for regime, (a, b) in REGIMES.items() for policy in POLICIES}

if __name__ == "__main__":
    result = exact_results()
    assert len(result) == 9
    assert result["STABLE_HALF", "ONLINE_ONE_STEP"] == (F(5, 18), F(27, 98))
    assert result["RISING_RATE", "ONLINE_ONE_STEP"] == (F(55, 144), F(131, 392))
    assert result["FALLING_RATE", "ONLINE_ONE_STEP"] == (F(55, 144), F(131, 392))
    for (regime, policy), (r5, r6) in result.items():
        print(regime, policy, r5, r6, (r5 + r6) / 2)
    print("PASS: 18 independent exact-moment time scores, 9 means")
