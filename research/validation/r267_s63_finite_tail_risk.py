#!/usr/bin/env python3
"""R267 S63 finite exact tail risks from the archived R267 PMFs.

Prescore protocol: protocols/R267_S63_FINITE_TAIL_RISK_PRESCORE_FREEZE_2026-10-29.md
Standard library only. E1 artificial probability experiment, not human data.
"""
from __future__ import annotations

import argparse
import json
from fractions import Fraction as F
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "research/R267/R267_EXACT_RESULTS.json"
OUTPUT = ROOT / "research/validation/R267_S63_FINITE_TAIL_RISK_RECEIPT_2026-10-29.json"
WORLDS = (
    "ADD_X", "ADD_X_PLUS_Y", "ADD_SQUARES", "PRODUCT_XY",
    "CENTERED_INTERACTION", "EQUAL_INDICATOR", "MODULAR_SUM",
    "THRESHOLD_SUM_GE2", "CORNER_22",
)
THRESHOLDS = (F(1, 3), F(2, 3))
SOURCE_BLOB = "310aa78c2e903cf8505856921c832bf6c73b04ca"
FREEZE_COMMIT = "6b086febb09dcf5da854bad0e2e5cc256b2ca2a7"


def rank(iid: str, lhs: str) -> str:
    a, b = F(iid), F(lhs)
    return "LHS_LOWER" if b < a else "IID_LOWER" if a < b else "TIE"


def derive(source: dict) -> dict:
    if source["research_id"] != "R267" or source["world_count"] != 9:
        raise ValueError("wrong baseline research")
    worlds = source["world_results"]
    if [w["world"] for w in worlds] != list(WORLDS):
        raise ValueError("wrong world coverage or ordering")
    rows = []
    for w in worlds:
        mu = F(w["target_grid_expectation"])
        if set(w["designs"]) != {"IID", "LHS"}:
            raise ValueError("wrong design coverage")
        for design in ("IID", "LHS"):
            d = w["designs"][design]
            count = 729 if design == "IID" else 36
            if type(d["source_atoms"]) is not int or d["source_atoms"] != count:
                raise ValueError("source atom count or type mismatch")
            if type(d["function_evaluations"]) is not int or d["function_evaluations"] != 3:
                raise ValueError("function evaluation count or type mismatch")
            pmf = {F(x): F(p) for x, p in d["complete_exact_estimator_PMF"].items()}
            if sum(pmf.values(), F(0)) != 1 or any(p <= 0 for p in pmf.values()):
                raise ValueError("PMF normalization or positivity failure")
            mean = sum((x * p for x, p in pmf.items()), F(0))
            variance = sum(((x - mu) ** 2 * p for x, p in pmf.items()), F(0))
            if mean != mu or mean != F(d["exact_mean"]) or variance != F(d["exact_variance"]):
                raise ValueError("original R267 moment mismatch")
            rows.append({
                "world": w["world"], "design": design, "source_atoms": count,
                "true_mean": str(mu), "variance": str(variance),
                "tail_gt_1_3": str(sum((p for x, p in pmf.items() if abs(x - mu) > THRESHOLDS[0]), F(0))),
                "tail_gt_2_3": str(sum((p for x, p in pmf.items() if abs(x - mu) > THRESHOLDS[1]), F(0))),
                "expected_abs_error": str(sum((abs(x - mu) * p for x, p in pmf.items()), F(0))),
                "max_abs_error": str(max(abs(x - mu) for x in pmf)),
            })
    paired = []
    for i in range(0, len(rows), 2):
        a, b = rows[i:i+2]
        v = rank(a["variance"], b["variance"])
        t1 = rank(a["tail_gt_1_3"], b["tail_gt_1_3"])
        t2 = rank(a["tail_gt_2_3"], b["tail_gt_2_3"])
        paired.append({
            "world": a["world"], "variance_ranking": v,
            "tail_1_3_ranking": t1, "tail_2_3_ranking": t2,
            "tail_ranking_changed": t1 != t2,
            "strict_tail_reversal": t1 != "TIE" and t2 != "TIE" and t1 != t2,
        })
    return {
        "research_id": "R267_S63",
        "original_results_git_blob": SOURCE_BLOB,
        "prescore_freeze_commit": FREEZE_COMMIT,
        "evidence_scope": "E1_FINITE_DISCRETE_ARTIFICIAL_ONLY",
        "thresholds": ["1/3", "2/3"],
        "row_count": 18,
        "new_real_human_E2": 0,
        "new_historical_E3": 0,
        "R073": "FROZEN",
        "PESEN_v0_1": "FROZEN",
        "rows": rows, "paired_comparison": paired,
    }


def check(receipt: dict, source: dict) -> None:
    expected = derive(source)
    if receipt != expected:
        raise ValueError("persisted receipt mismatch")
    # Python bool == int: explicit check closes the false/0 type substitution.
    if type(receipt["row_count"]) is not int or type(receipt["new_real_human_E2"]) is not int:
        raise ValueError("invalid integer type")
    if type(receipt["new_historical_E3"]) is not int:
        raise ValueError("invalid evidence type")
    if any(type(row["source_atoms"]) is not int for row in receipt["rows"]):
        raise ValueError("invalid source type")
    if any(type(p["tail_ranking_changed"]) is not bool or
           type(p["strict_tail_reversal"]) is not bool for p in receipt["paired_comparison"]):
        raise ValueError("invalid comparison boolean type")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--emit", action="store_true")
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--source", type=Path, default=SOURCE)
    parser.add_argument("--receipt", type=Path, default=OUTPUT)
    args = parser.parse_args()
    if args.emit == args.check:
        parser.error("select exactly one of --emit or --check")
    source = json.loads(args.source.read_text(encoding="utf-8"))
    if args.emit:
        print(json.dumps(derive(source), ensure_ascii=False, indent=2))
    else:
        receipt = json.loads(args.receipt.read_text(encoding="utf-8"))
        check(receipt, source)
        print("R267 S63 archived PMF receipt: PASS, 18 rows, 36 exact tail probabilities")


if __name__ == "__main__":
    main()
