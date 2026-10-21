"""R157 structural-demographic-inspired artificial three-pressure system.

Primary source: Turchin 2013 Psi=MMP*EMP*SFD; only the product structure
is transcribed. The recurrences are NEW, synthetic, not author equations.
All experimental states are exact Fraction, with no historical observations.
"""
from __future__ import annotations

from fractions import Fraction as F
import json

TARGETS = (F(1, 4), F(1, 2), F(1))
LAGS = (F(1, 4), F(1, 2))
RELIEFS = (F(0), F(1, 2), F(1))
HORIZON = 12
ZERO = (F(0), F(0), F(0))


def unit(value: object, label: str) -> F:
    """Reject floats, booleans and out-of-bound pressure units."""
    if isinstance(value, bool) or not isinstance(value, (int, F)):
        raise ValueError(f"{label} must be int or Fraction")
    x = F(value)
    if x < 0 or x > 1:
        raise ValueError(f"{label} is outside [0,1]")
    return x


def valid_params(h, a, b, c, r):
    return (unit(h, "target"), unit(a, "mass rate"),
            unit(b, "elite lag"), unit(c, "fiscal lag"),
            unit(r, "fiscal buffer"))


def scoring(state):
    if len(state) != 3:
        raise ValueError("three components required")
    m, e, f = (unit(x, "artificial pressure") for x in state)
    return (m * e * f, (m + e + f) / 3)


def step(state, h, a, b, c, r):
    """Simultaneous project-defined update. Q and Psi are never state drivers."""
    if len(state) != 3:
        raise ValueError("3-component state required")
    m, e, f = (unit(x, "state") for x in state)
    h, a, b, c, r = valid_params(h, a, b, c, r)
    return ((1-a)*m + a*h,
            (1-b)*e + b*m,
            (1-c)*f + c*(1-r)*e)


def direct_history(h, a, b, c, r, horizon=HORIZON):
    if isinstance(horizon, bool) or not isinstance(horizon, int) or horizon < 0:
        raise ValueError("nonnegative integer horizon required")
    valid_params(h, a, b, c, r)
    state = ZERO
    out = [state]
    for _ in range(horizon):
        state = step(state, h, a, b, c, r)
        out.append(state)
    return tuple(out)


def _matmul(left, right):
    """Independent Fraction matrix operation with a fixed 3x3 dimension."""
    return tuple(tuple(sum((left[i][k]*right[k][j] for k in range(3)), F(0))
                       for j in range(3)) for i in range(3))


def _matvec(matrix, vector):
    return tuple(sum((matrix[i][k]*vector[k] for k in range(3)), F(0))
                 for i in range(3))


def matrix_history(h, a, b, c, r, horizon=HORIZON):
    """Independent affine-power sum x[t]=SUM(A**k * drive) from x0=0."""
    if isinstance(horizon, bool) or not isinstance(horizon, int) or horizon < 0:
        raise ValueError("nonnegative integer horizon required")
    h, a, b, c, r = valid_params(h, a, b, c, r)
    matrix = ((1-a, F(0), F(0)),
              (b, 1-b, F(0)),
              (F(0), c*(1-r), 1-c))
    drive = (a*h, F(0), F(0))
    power = ((F(1),F(0),F(0)),
             (F(0),F(1),F(0)),
             (F(0),F(0),F(1)))
    total = (F(0),F(0),F(0))
    path = [total]
    for _ in range(horizon):
        additional = _matvec(power, drive)
        total = tuple(total[k] + additional[k] for k in range(3))
        path.append(total)
        power = _matmul(power, matrix)
    return tuple(path)


def record():
    worlds = []
    for hi, h in enumerate(TARGETS):
        for ai, a in enumerate(LAGS):
            for bi, b in enumerate(LAGS):
                for ci, c in enumerate(LAGS):
                    for ri, r in enumerate(RELIEFS):
                        direct = direct_history(h,a,b,c,r)
                        affine = matrix_history(h,a,b,c,r)
                        if direct != affine:
                            raise AssertionError("independent exact Fraction paths disagree")
                        readings = []
                        for t,state in enumerate(direct):
                            psi,mean = scoring(state)
                            if not all(0 <= v <= 1 for v in (*state,psi,mean)):
                                raise AssertionError("unit boundedness failure")
                            readings.append({
                                "t":t,"mass":str(state[0]),"elite":str(state[1]),
                                "fiscal":str(state[2]),"psi_product":str(psi),
                                "alternative_mean":str(mean)
                            })
                        worlds.append({
                            "id":f"h{hi}_a{ai}_b{bi}_c{ci}_r{ri}",
                            "target":str(h),"mass_adjustment":str(a),
                            "elite_delay":str(b),"fiscal_delay":str(c),
                            "fiscal_buffer":str(r),
                            "steady_limit":[str(h),str(h),str((1-r)*h)],
                            "direct_equals_independent_affine":True,
                            "points":readings
                        })
    if len(worlds) != 72 or len(set(x["id"] for x in worlds))!=72:
        raise AssertionError("frozen scenario identity mismatch")
    first = direct_history(F(1), F(1,4), F(1,4),F(1,4), F(0))
    second = direct_history(F(1,2),F(1,2),F(1,4),F(1,4),F(0))
    if first[1] != second[1] or first[2] == second[2]:
        raise AssertionError("prespecified single-time identification contrast lost")
    return {
        "research_id":"R157","evidence":"E1_PROJECT_AUTHORED_EXACT_MATH",
        "author_original_dynamics_recreated":False,
        "historical_instability_outcomes_used":False,
        "real_event_probabilities_estimated":False,
        "model_scope":"synthetic normalized lag filters; PSI product schematic only",
        "scenario_count":72,"observations_per_world":13,
        "worlds":worlds,
        "predeclared_counterexamples":{
            "one_observation_same_t1":[str(x) for x in first[1]],
            "differing_t2_world_A":[str(x) for x in first[2]],
            "differing_t2_world_B":[str(x) for x in second[2]],
            "aggregation_A":{"components":["1","1","0"],"psi":"0","mean":"2/3"},
            "aggregation_B":{"components":["1/2","1/2","1/2"],"psi":"1/8","mean":"1/2"},
            "perfect_buffer_psi_all_zero":all(
                scoring(s)[0] == 0 for s in direct_history(F(1),F(1,2),F(1,2),F(1,2),F(1))),
            "first_nonzero_fiscal_t":next(t for t,s in enumerate(first) if s[2]>0)
        }
    }


def main():
    print(json.dumps(record(), indent=2, sort_keys=True, ensure_ascii=False))


if __name__ == "__main__":
    main()
