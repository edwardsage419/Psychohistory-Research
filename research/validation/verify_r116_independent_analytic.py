#!/usr/bin/env python3
"""R116 finite E1 independent analytic oracle, Python standard library only."""
from __future__ import annotations
import argparse
from fractions import Fraction as F
from pathlib import Path
import importlib.util
import hashlib
import json
import sys

ACCURACY = {"strong": F(3, 4), "weak": F(11, 20)}
MODELS = {"NO_INFLUENCE": (False, F(0)),
          "NORMATIVE_ONLY": (False, F(1, 4)),
          "INFORMATIONAL_ONLY": (True, F(0)),
          "BOTH": (True, F(1, 4))}
CELLS = [("C0_ANON", False, False), ("C0_PUBLIC", False, True),
         ("C1_ANON", True, False), ("C1_PUBLIC", True, True)]
FROZEN = {
    "strong": {"NO_INFLUENCE": "0000", "NORMATIVE_ONLY": "0001",
               "INFORMATIONAL_ONLY": "0011", "BOTH": "0011"},
    "weak": {"NO_INFLUENCE": "0000", "NORMATIVE_ONLY": "0001",
             "INFORMATIONAL_ONLY": "0000", "BOTH": "0001"},
}

def oracle(seen, public, informative, cost, group_accuracy):
    # Independently enumerate the hidden fact, self-signal=0 and one group-signal=1.
    joint = {}
    for fact in (0, 1):
        own_likelihood = F(3, 5) if fact == 0 else F(2, 5)
        cue_likelihood = ((group_accuracy if fact else 1-group_accuracy)
                          if seen and informative else F(1))
        joint[fact] = F(1, 2) * own_likelihood * cue_likelihood
    q = joint[1] / (joint[0] + joint[1])
    u0 = 1-q-(cost if seen and public else 0)
    u1 = q
    return (q, u0, u1, int(u1 > u0))

def grids():
    return {s: {name: {cell: oracle(seen, public, info, cost, acc)[-1]
                       for cell, seen, public in CELLS}
                for name, (info, cost) in MODELS.items()}
            for s, acc in ACCURACY.items()}

def check_receipt(receipt, expected):
    inner = receipt["full_anonymous_fixed_synthetic_receipt"]
    for s in ACCURACY:
        assert inner[s + "_single_cue_choice_grid"] == expected[s], s
    assert inner["strong_cue_normative_private_belief_V1"] == "2/5"
    assert inner["strong_cue_informational_private_belief_V1"] == "2/3"
    assert inner["original_human_E2_evaluations"] == 0
    assert inner["fitted_Bernheim_1994_game_equilibrium"] is False
    assert inner["R073"] == inner["PESEN_v0_1"] == "FROZEN"

def test_negative_controls(expected):
    from copy import deepcopy
    sample = {"full_anonymous_fixed_synthetic_receipt": {
        "strong_single_cue_choice_grid": deepcopy(expected["strong"]),
        "weak_single_cue_choice_grid": deepcopy(expected["weak"]),
        "strong_cue_normative_private_belief_V1": "2/5",
        "strong_cue_informational_private_belief_V1": "2/3",
        "original_human_E2_evaluations": 0,
        "fitted_Bernheim_1994_game_equilibrium": False,
        "R073": "FROZEN", "PESEN_v0_1": "FROZEN"}}
    check_receipt(sample, expected)
    for field in ("grid", "belief"):
        mutated = deepcopy(sample)
        inner = mutated["full_anonymous_fixed_synthetic_receipt"]
        if field == "grid":
            inner["strong_single_cue_choice_grid"]["BOTH"]["C1_PUBLIC"] = 0
        else:
            inner["strong_cue_informational_private_belief_V1"] = "1/2"
        try:
            check_receipt(mutated, expected)
        except AssertionError:
            continue
        raise AssertionError("TAMPER_NOT_REJECTED_" + field)
    return 2

def run(root=None):
    expected = grids()
    checks = 0
    for strength, models in FROZEN.items():
        for name, frozen in models.items():
            observed = "".join(str(expected[strength][name][c]) for c, _, _ in CELLS)
            assert observed == frozen, (strength, name, observed)
            checks += 4
    assert oracle(False, False, False, F(0), ACCURACY["strong"])[0] == F(2, 5)
    assert oracle(True, False, True, F(0), ACCURACY["strong"])[0] == F(2, 3)
    assert oracle(True, False, True, F(0), ACCURACY["weak"])[0] == F(22, 49)
    assert (1-F(2, 5))-F(2, 5) == F(1, 5)
    assert oracle(True, True, False, F(1, 5), ACCURACY["strong"])[-1] == 0
    tamper = test_negative_controls(expected)
    result = {"research_id": "R116", "scope": "INTERNAL_INDEPENDENT_METHOD_E1",
              "frozen_action_cells": checks, "tamper_rejections": tamper,
              "source_and_receipt_checked": False, "new_E2": 0, "new_E3": 0,
              "R073": "FROZEN", "PESEN_v0_1": "FROZEN"}
    if root is not None:
        source = root / "research/R116/r116_normative_public_status_vs_informational_cue_exact.py"
        receipt_path = root / "research/R116/R116_PHASE_A_48_SYNTHETIC_PUBLIC_STATUS_INFO_CI_ACCEPTANCE.json"
        assert source.is_file() and receipt_path.is_file(), "SOURCE_MISSING"
        spec = importlib.util.spec_from_file_location("r116_subject", source)
        assert spec and spec.loader
        module = importlib.util.module_from_spec(spec)
        sys.modules[spec.name] = module
        spec.loader.exec_module(module)
        n = 0
        for strength, accuracy in ACCURACY.items():
            for name, (info, cost) in MODELS.items():
                for cell, seen, public in CELLS:
                    observed = module.trial(module.MODELS[name], cue_exposed=seen,
                                            response_public=public, group_accuracy=accuracy)
                    q, u0, u1, choice = oracle(seen, public, info, cost, accuracy)
                    assert (observed["belief_V1"], observed["payoff_action0"],
                            observed["payoff_action1"], observed["choice"]) == (
                            q, u0, u1, choice), (strength, name, cell)
                    n += 1
        receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
        check_receipt(receipt, expected)
        assert receipt["actual_synthetic_tests_executed"] == 48
        assert receipt["actual_synthetic_test_failures"] == 0
        result.update({"source_and_receipt_checked": True, "source_comparisons": n,
                       "source_sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
                       "receipt_sha256": hashlib.sha256(receipt_path.read_bytes()).hexdigest()})
        result["status"] = "PASS_BOUNDED_INTERNAL_INDEPENDENT_METHOD_E1"
    else:
        result["status"] = "PASS_STANDALONE_ORACLE_ONLY"
    return result

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", type=Path)
    args = parser.parse_args()
    print(json.dumps(run(args.repo_root), indent=2, sort_keys=True))
