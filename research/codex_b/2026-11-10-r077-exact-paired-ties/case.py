"""Completely fictional coherent source/target and independent integer proof."""
from fractions import Fraction
from itertools import combinations
from math import gcd


def source_events():
    return ([(1, 1, 0, 0, 0)]*8 + [(1, 0, 0, 0, 1)]*8
            + [(0, 0, 0, 0, 0)]*8 + [(0, 0, 0, 0, 1)]*8)


def legacy_fit():
    # Hand-derived counts, verified against all32 fictional rows in tests.
    return {
        "train_only_prevalence": .5, "source_sessions": 2, "train_target_count": 32,
        "state_counts": {
            "M1_OWN_LAST": {(1,): (8, 16), (0,): (8, 16)},
            "M2_OPPONENT_LAST": {(1,): (0, 8), (0,): (16, 24)},
            "M3_JOINT_LAST": {(1, 1): (0, 8), (1, 0): (8, 8), (0, 0): (8, 16)},
            "M4_JOINT_TWO_LAGS": {(1, 1, 0, 0): (0, 8), (1, 0, 0, 0): (8, 8), (0, 0, 0, 0): (8, 16)},
        },
    }


def rational_probabilities():
    # Frozen alpha20; source prevalence16/32. Uses no original model helper.
    p0 = Fraction(16, 32)
    reference = (8+20*p0)/(16+20)
    candidate = (0+20*p0)/(8+20)
    return candidate, reference


def target_cases():
    for positive_positions in combinations(range(7), 3):
        events = [(1, 1, 0, 0, int(i in positive_positions)) for i in range(7)]
        yield positive_positions, {
            f"ARTIFICIAL_SESSION_{tr}": {"treatment": tr, "events": list(events)}
            for tr in (0, 1)
        }


def exact_sessions(legacy_sessions):
    candidate, reference = rational_probabilities()
    return {name: {"treatment": info["treatment"],
                   "records": [(event[4], candidate, reference) for event in info["events"]]}
            for name, info in legacy_sessions.items()}


def integer_witness(outcomes):
    """No Fraction, fit, exact-kernel or archived helper used by this route."""
    if len(outcomes) != 7 or sum(outcomes) != 3 or any(type(y) is not int or y not in (0, 1) for y in outcomes):
        raise ValueError("WITNESS_EXPECTS_THREE_OF_SEVEN_BINARY_OUTCOMES")
    denominator = 7*14**2
    totals = {"candidate": sum((5-14*y)**2 for y in outcomes),
              "reference": sum((7-14*y)**2 for y in outcomes)}
    risks = {}
    for model, total in totals.items():
        divisor = gcd(total, denominator)
        risks[model] = str(total//divisor)+"/"+str(denominator//divisor)
    return {"integer_squared_sums": totals, "denominator": denominator, "risks": risks}
