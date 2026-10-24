#!/usr/bin/env python3
"""Independent integer log-odds and Decimal probability audit for R114.

Expected results are computed without calling the original implementation.
The original is imported solely for a post-hoc comparison.
"""
import importlib.util
import json
from decimal import Decimal, localcontext
from pathlib import Path

PARAMETERS = {
    "DESCRIPTIVE": (-1, 2, 0, 0),
    "NORMATIVE_ONLY": (-1, 0, 2, 0),
    "BOTH_ADDITIVE": (-1, 1, 1, 0),
    "INTERACTION": (-1, 1, 1, 1),
}
CELLS = {"E0N0": (0, 0), "E1N0": (1, 0),
         "E0N1": (0, 1), "E1N1": (1, 1)}


def independent_grid(coefficients):
    a, b, c, d = coefficients
    logits = {name: a + b * e + c * n + d * e * n
              for name, (e, n) in CELLS.items()}
    with localcontext() as ctx:
        ctx.prec = 65
        probabilities = {
            name: Decimal(1) / (Decimal(1) + (-Decimal(z)).exp())
            for name, z in logits.items()
        }
    return logits, probabilities


def contrast(logits):
    return (logits["E1N1"] - logits["E1N0"]
            - logits["E0N1"] + logits["E0N0"])


def main():
    path = Path("research/R114/r114_conditional_norm_compliance_discordant_expectations.py")
    assert path.is_file(), "Original source missing"
    expected = {name: independent_grid(p) for name, p in PARAMETERS.items()}
    spec = importlib.util.spec_from_file_location("r114_original", path)
    assert spec is not None and spec.loader is not None
    import sys
    original = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = original
    spec.loader.exec_module(original)

    checks = 0
    for name, params in PARAMETERS.items():
        logits, probs = expected[name]
        assert contrast(logits) == params[3]
        checks += 1
        observed = original.MODELS[name].grid()
        assert set(observed) == set(CELLS)
        checks += 1
        for cell, (e, n) in CELLS.items():
            assert logits[cell] == params[0] + params[1]*e + params[2]*n + params[3]*e*n
            checks += 1
            assert abs(Decimal(str(observed[cell])) - probs[cell]) < Decimal("1e-14"), (name, cell)
            checks += 1

    descriptive = expected["DESCRIPTIVE"][0]
    normative = expected["NORMATIVE_ONLY"][0]
    for cell in ("E0N0", "E1N1"):
        assert descriptive[cell] == normative[cell]
        checks += 1
    for cell in ("E1N0", "E0N1"):
        assert descriptive[cell] != normative[cell]
        checks += 1
    assert descriptive["E1N0"] > normative["E1N0"]
    assert descriptive["E0N1"] < normative["E0N1"]
    checks += 2

    # The first three observed logits permit arbitrarily different interactions.
    base = expected["INTERACTION"][0]
    a = base["E0N0"]
    b = base["E1N0"] - a
    c = base["E0N1"] - a
    assert (a, b, c) == (-1, 1, 1)
    assert independent_grid((a, b, c, -9))[0]["E1N1"] != independent_grid((a, b, c, 9))[0]["E1N1"]
    checks += 2

    # Mutation tests: both deliberately corrupted inputs must be rejected.
    tampered = dict(original.MODELS["INTERACTION"].grid())
    tampered["E1N1"] += 0.01
    assert abs(Decimal(str(tampered["E1N1"])) - expected["INTERACTION"][1]["E1N1"]) > Decimal("1e-14")
    checks += 1
    tampered_logit = dict(expected["INTERACTION"][0])
    tampered_logit["E1N1"] += 1
    assert contrast(tampered_logit) != PARAMETERS["INTERACTION"][3]
    checks += 1

    print(json.dumps({
        "research_id": "R114", "catalogue_id": "03-008",
        "status": "PASS_BOUNDED_INTERNAL_SYMBOLIC_E1",
        "checks_passed": checks, "constructed_cells": 16,
        "negative_controls_rejected": 2, "human_E2_new": 0,
        "historical_E3_new": 0, "external_replication": False,
        "held_out_human_prediction": "NOT_PERFORMED",
        "R073": "FROZEN", "PESEN_v0_1": "FROZEN"
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
