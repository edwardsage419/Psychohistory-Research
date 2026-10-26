"""Independent exact analytic audit for R182, plus real R181 tie-omission negative control.
Run from repository root: python research/evidence_audit/b_r182_shift_r181_tie_negative_control_20261026.py
Only Python standard library. Read-only: no files are modified.
"""
from fractions import Fraction as F
from itertools import combinations
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[2]
def load(p):
    return json.loads((ROOT / p).read_text(encoding="utf-8"))

def conditional_z(counts, x):
    return F(counts[2*x+1], counts[2*x]+counts[2*x+1])

def risk_formula(train, target, c, e, omit_shift=False):
    """Independent conditional Bernoulli variance and squared transport bias."""
    n = sum(target)
    value = e * e
    for x in (0, 1):
        qt = conditional_z(target, x)
        qtr = conditional_z(train, x)
        px = F(target[2*x]+target[2*x+1], n)
        value += c*c*px*(qt*(1-qt) + (F(0) if omit_shift else (qt-qtr)**2))
    return value

def r182_audit():
    src = load("research/R182/R182_EXACT_RESULTS.json")["all_worlds"]
    receipt = load("research/validation/R182_COVARIATE_SHIFT_960_EXACT_RECEIPT_2026-10-26.json")
    designs = {
        "BALANCED": (2,2,2,2),
        "POSITIVE": (4,2,2,4),
        "NEGATIVE": (2,4,4,2),
        "STRONG_POSITIVE": (6,2,2,6)
    }
    assert len(src) == 240 and len(receipt["rows"]) == 960
    index = {(r["world_index"], r["target_design"]): r for r in receipt["rows"]}
    assert len(index) == 960
    counts = {"m0_excess_positive":0, "m0_excess_zero":0,
              "risk_increase":0, "risk_decrease":0, "risk_same":0,
              "wrong_no_shift_detected":0}
    for i, w in enumerate(src):
        train = tuple(w["cell_counts_in_00_01_10_11_order"])
        c, e = F(w["true_group_slope_c"]), F(w["residual_amplitude_e"])
        base = risk_formula(train, train, c, e)
        for target_name, target in designs.items():
            row = index[(i,target_name)]
            assert row["train_design"] == w["design"]
            correct = risk_formula(train, target, c, e)
            assert F(row["mse_m0"]) == correct
            assert F(row["mse_m1"]) == e*e
            assert F(row["m0_excess"]) == correct-e*e
            assert correct-e*e >= 0
            counts["m0_excess_positive" if correct>e*e else "m0_excess_zero"] += 1
            counts["risk_increase" if correct>base else "risk_decrease" if correct<base else "risk_same"] += 1
            if risk_formula(train,target,c,e,omit_shift=True) != correct:
                counts["wrong_no_shift_detected"] += 1
    assert counts == {
        "m0_excess_positive":768, "m0_excess_zero":192,
        "risk_increase":384, "risk_decrease":48, "risk_same":528,
        "wrong_no_shift_detected":576
    }, counts
    return {"checked_target_worlds":960,"independent_formula_checks":960,**counts}

def r181_tie_audit():
    receipt = load("research/validation/R181_PVALUE_RESOLUTION_THIRD_METHOD_EXACT_RECEIPT_2026-10-26.json")
    assignments = list(combinations(range(6),3))
    assert len(assignments) == 20 and len(receipt["rows"]) == 210
    detected = 0
    example = None
    for row in receipt["rows"]:
        k = [int(v) for v in row["k"]]
        total = sum(k)
        values = [abs(2*sum(k[j] for j in subset)-total) for subset in assignments]
        observed = max(values)
        correct = F(sum(v>=observed for v in values),20)
        wrong = F(sum(v>observed for v in values),20)
        assert correct == F(row["min_p"])
        if wrong != correct:
            detected += 1
        if row["k"] == "000123":
            example = {"profile":row["k"],"correct":str(correct),"wrong":str(wrong)}
            assert correct == F(1,10) and wrong == 0
    assert detected == 210
    return {"profiles_checked":210,"actual_strict_greater_than_bug_detected":detected,
            "example":example,"previous_B_badTie_constant_expression_not_reused":True}

if __name__ == "__main__":
    print(json.dumps({"R182":r182_audit(),"R181":r181_tie_audit(),
                      "evidence":"internal method-independent E1 audit, not external replication"},
                     ensure_ascii=False,indent=2))
