#!/usr/bin/env python3
"""R066: transparent finite-sample DeGroot, FJ, and HK opinion dynamics.

Only mechanism-level deterministic demonstrations. No empirical participants,
model fitting, calibrated history or predictive external validation.
See protocols/R066_OPINION_DYNAMICS_THREE_MODELS_2026-10-16.md.
"""
from __future__ import annotations

import argparse
import json
import math
from typing import Sequence

REFERENCE_X = (0.0, 0.2, 1.0)
REFERENCE_W = tuple((1/3, 1/3, 1/3) for _ in range(3))


def validate_opinions(x: Sequence[float]) -> tuple[float, ...]:
    if not x:
        raise ValueError("empty set of agents")
    a = tuple(float(z) for z in x)
    if any(not math.isfinite(z) or not 0.0 <= z <= 1.0 for z in a):
        raise ValueError("nonfinite or out-of-range opinion")
    return a


def validate_weights(W: Sequence[Sequence[float]], n: int) -> tuple[tuple[float, ...], ...]:
    if len(W) != n:
        raise ValueError("network number of rows is not agent count")
    rows = tuple(tuple(float(v) for v in row) for row in W)
    if any(len(row) != n for row in rows):
        raise ValueError("network must be square")
    for row in rows:
        if (any(not math.isfinite(w) or w < 0.0 or w > 1.0 for w in row)
                or abs(math.fsum(row) - 1.0) > 1e-12):
            raise ValueError("W must be a finite nonnegative row stochastic matrix")
    return rows


def degroot_step(x: Sequence[float], W: Sequence[Sequence[float]]) -> tuple[float, ...]:
    opinions = validate_opinions(x)
    weight = validate_weights(W, len(opinions))
    return tuple(math.fsum(w*y for w, y in zip(row, opinions)) for row in weight)


def fj_step(x: Sequence[float], x0: Sequence[float],
            W: Sequence[Sequence[float]], alpha: Sequence[float]) -> tuple[float, ...]:
    now, initial = validate_opinions(x), validate_opinions(x0)
    if len(now) != len(initial) or len(alpha) != len(now):
        raise ValueError("opinion and susceptibility lengths must match")
    effects = validate_weights(W, len(now))
    susceptibility = tuple(float(z) for z in alpha)
    if any(not math.isfinite(z) or z < 0.0 or z > 1.0 for z in susceptibility):
        raise ValueError("susceptibility must lie in [0,1]")
    out = []
    for i, row in enumerate(effects):
        influence = math.fsum(w*y for w, y in zip(row, now))
        out.append(susceptibility[i]*influence + (1.0-susceptibility[i])*initial[i])
    return tuple(out)


def hk_step(x: Sequence[float], epsilon: float) -> tuple[float, ...]:
    now = validate_opinions(x)
    eps = float(epsilon)
    if not math.isfinite(eps) or not 0 <= eps <= 1.0:
        raise ValueError("confidence radius must be finite within [0,1]")
    # Every neighbor set uses ONLY the original pre-update vector: synchronous HK.
    result = []
    for anchor in now:
        neighbors = [z for z in now if abs(z-anchor) <= eps]
        if not neighbors:
            raise RuntimeError("self neighbor missing in HK")
        result.append(math.fsum(neighbors) / len(neighbors))
    return tuple(result)


def simulate(method: str, x0: Sequence[float], steps: int,
             W=None, alpha=None, epsilon=None) -> list[list[float]]:
    if type(steps) is not int or not 0 <= steps <= 1000:
        raise ValueError("steps must be integer in [0,1000]")
    start = validate_opinions(x0)
    if method not in ("degroot", "fj", "hk"):
        raise ValueError("unsupported opinion model")
    if method in ("degroot","fj") and W is None:
        raise ValueError("linear opinion model requires network W")
    if method == "fj" and alpha is None:
        raise ValueError("FJ needs susceptibility alpha")
    if method == "hk" and epsilon is None:
        raise ValueError("HK needs confidence radius epsilon")
    now = start
    history = [list(start)]
    for _ in range(steps):
        if method == "degroot":
            now = degroot_step(now, W)
        elif method == "fj":
            now = fj_step(now, start, W, alpha)
        else:
            now = hk_step(now, epsilon)
        history.append(list(now))
    return history


def benchmark() -> dict:
    """Fixed results declared in the protocol before implementation/results."""
    x, W = REFERENCE_X, REFERENCE_W
    states = {
        "degroot": simulate("degroot", x, 2, W=W),
        "fj": simulate("fj", x, 2, W=W, alpha=(0.5,0.5,0.5)),
        "hk": simulate("hk", x, 2, epsilon=0.25),
    }
    expected = {
        "degroot": [0.4,0.4,0.4],
        "fj": [0.2,0.3,0.7],
        "hk": [0.1,0.1,1.0],
    }
    for name, series in states.items():
        if any(abs(a-b)>1e-12 for a,b in zip(series[1], expected[name])):
            raise AssertionError("frozen reference first step differs for " + name)
        if any(abs(a-b)>1e-12 for a,b in zip(series[2], expected[name])):
            raise AssertionError("frozen reference stationary second step differs " + name)
    return {
        "research_id":"R066", "stage":"MECHANISM_E1",
        "protocol":"protocols/R066_OPINION_DYNAMICS_THREE_MODELS_2026-10-16.md",
        "initial_opinions":list(x),
        "network":"dense equal weights 1/3 for DeGroot and FJ",
        "fj_susceptibility":[0.5]*3, "hk_epsilon":0.25,
        "results":states,
        "status":"SYNTHETIC_MECHANISM_PASS",
        "empirical_model_comparison":"OPEN",
        "independent_prediction":"OPEN",
        "pesen_v01":"FROZEN",
    }


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--output",default=None)
    args=ap.parse_args()
    data=benchmark()
    rendered=json.dumps(data,ensure_ascii=False,indent=2)+"\n"
    if args.output:
        from pathlib import Path
        Path(args.output).write_text(rendered,encoding="utf-8")
    print(json.dumps({"research_id":data["research_id"],"status":data["status"],
                      "first_step":{name:values[1] for name,values in data["results"].items()}},
                     sort_keys=True))


if __name__=="__main__":
    main()
