#!/usr/bin/env python3
"""Independent R267 S63 E1 gate using all primitive IID/LHS draws.

No imports from R267 or S63 computation programs. Non-blind internal audit.
"""
from __future__ import annotations

import argparse
import copy
import itertools
import json
from collections import Counter
from fractions import Fraction as F
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
RECEIPT = ROOT / "research/validation/R267_S63_FINITE_TAIL_RISK_RECEIPT_2026-10-29.json"
WORLDS = ("ADD_X", "ADD_X_PLUS_Y", "ADD_SQUARES", "PRODUCT_XY",
          "CENTERED_INTERACTION", "EQUAL_INDICATOR", "MODULAR_SUM",
          "THRESHOLD_SUM_GE2", "CORNER_22")
GRID = tuple(itertools.product(range(3), repeat=2))
PERMS = tuple(itertools.permutations(range(3)))


def f(name: str, x: int, y: int) -> int:
    if name == "ADD_X": return x
    if name == "ADD_X_PLUS_Y": return x + y
    if name == "ADD_SQUARES": return x*x + y*y
    if name == "PRODUCT_XY": return x*y
    if name == "CENTERED_INTERACTION": return (x-1)*(y-1)
    if name == "EQUAL_INDICATOR": return int(x == y)
    if name == "MODULAR_SUM": return (x+y) % 3
    if name == "THRESHOLD_SUM_GE2": return int(x+y >= 2)
    if name == "CORNER_22": return int(x == 2 and y == 2)
    raise ValueError("unfrozen integrand")


def independent_rows() -> list[dict]:
    rows = []
    for name in WORLDS:
        truth = F(sum(f(name,x,y) for x,y in GRID),9)
        for design in ("IID","LHS"):
            if design == "IID":
                primitive = itertools.product(GRID, repeat=3)
            else:
                primitive = (tuple(zip(px,py)) for px in PERMS for py in PERMS)
            counts = Counter(F(sum(f(name,x,y) for x,y in triplet),3)
                             for triplet in primitive)
            n = sum(counts.values())
            if n != (729 if design == "IID" else 36):
                raise ValueError("primitive source count mismatch")
            if F(sum(k*c for k,c in counts.items()),n) != truth:
                raise ValueError("primitive mean mismatch")
            rows.append({
                "world":name,"design":design,"source_atoms":n,
                "true_mean":str(truth),
                "variance":str(F(sum((k-truth)**2*c for k,c in counts.items()),n)),
                "tail_gt_1_3":str(F(sum(c for k,c in counts.items()
                                      if abs(k-truth)>F(1,3)),n)),
                "tail_gt_2_3":str(F(sum(c for k,c in counts.items()
                                      if abs(k-truth)>F(2,3)),n)),
                "expected_abs_error":str(F(sum(abs(k-truth)*c for k,c in counts.items()),n)),
                "max_abs_error":str(max(abs(k-truth) for k in counts)),
            })
    return rows


def rank(a: str,b: str) -> str:
    return "LHS_LOWER" if F(b)<F(a) else "IID_LOWER" if F(a)<F(b) else "TIE"


def expected_pairs(rows: list[dict]) -> list[dict]:
    pairs=[]
    for i in range(0,len(rows),2):
        a,b=rows[i:i+2]
        v=rank(a["variance"],b["variance"])
        t1=rank(a["tail_gt_1_3"],b["tail_gt_1_3"])
        t2=rank(a["tail_gt_2_3"],b["tail_gt_2_3"])
        pairs.append({
            "world":a["world"],"variance_ranking":v,
            "tail_1_3_ranking":t1,"tail_2_3_ranking":t2,
            "tail_ranking_changed":t1!=t2,
            "strict_tail_reversal":t1!="TIE" and t2!="TIE" and t1!=t2,
        })
    return pairs


def validate(receipt: dict, expected: list[dict]) -> int:
    if not isinstance(receipt,dict):
        raise ValueError("receipt must be object")
    expected_keys={"research_id","original_results_git_blob","prescore_freeze_commit",
                   "evidence_scope","thresholds","row_count","new_real_human_E2",
                   "new_historical_E3","R073","PESEN_v0_1","rows","paired_comparison"}
    if set(receipt)!=expected_keys:
        raise ValueError("receipt keys changed")
    fixed={
        "research_id":"R267_S63",
        "original_results_git_blob":"310aa78c2e903cf8505856921c832bf6c73b04ca",
        "prescore_freeze_commit":"6b086febb09dcf5da854bad0e2e5cc256b2ca2a7",
        "evidence_scope":"E1_FINITE_DISCRETE_ARTIFICIAL_ONLY",
        "R073":"FROZEN","PESEN_v0_1":"FROZEN",
    }
    if any(receipt.get(k)!=v for k,v in fixed.items()):
        raise ValueError("identity, freeze, or evidence upgrade")
    if receipt["thresholds"]!=["1/3","2/3"]:
        raise ValueError("wrong thresholds")
    for k,target in (("row_count",18),("new_real_human_E2",0),("new_historical_E3",0)):
        if type(receipt[k]) is not int or receipt[k]!=target:
            raise ValueError("wrong integer type or evidence count")
    actual=receipt["rows"]
    if type(actual) is not list or len(actual)!=18:
        raise ValueError("missing or extra rows")
    if any(type(row) is not dict or set(row)!=set(ref) for row,ref in zip(actual,expected)):
        raise ValueError("row schema changed")
    if any(type(row["source_atoms"]) is not int for row in actual):
        raise ValueError("invalid source atom type")
    keys={(row["world"],row["design"]) for row in actual}
    if len(keys)!=18 or keys!={(w,d) for w in WORLDS for d in ("IID","LHS")}:
        raise ValueError("duplicate or missing coverage")
    if actual!=expected:
        raise ValueError("primitive-source numeric comparison failed")
    pairs=receipt["paired_comparison"]
    if type(pairs) is not list or len(pairs)!=9:
        raise ValueError("pair coverage changed")
    if any(type(p["tail_ranking_changed"]) is not bool or
           type(p["strict_tail_reversal"]) is not bool for p in pairs):
        raise ValueError("invalid boolean type")
    if pairs!=expected_pairs(expected):
        raise ValueError("pair rankings changed")
    return 18*6+9*5


def negative_controls(receipt: dict, expected: list[dict]) -> int:
    def rejected(mutator):
        bad=copy.deepcopy(receipt)
        mutator(bad)
        try:
            validate(bad,expected)
        except (ValueError,KeyError,TypeError):
            return True
        return False
    def duplicate(r): r["rows"][1]=copy.deepcopy(r["rows"][0])
    def missing(r): r["rows"].pop()
    def bool_as_int(r): r["new_real_human_E2"]=False
    def tamper(r): r["rows"][0]["tail_gt_1_3"]="999"
    def evidence(r): r["evidence_scope"]="E2_REAL_HUMAN"
    def thresholds(r): r["thresholds"][0]="1/2"
    controls=(duplicate,missing,bool_as_int,tamper,evidence,thresholds)
    if not all(rejected(m) for m in controls):
        raise ValueError("one or more negative controls passed incorrectly")
    return len(controls)


def main() -> None:
    parser=argparse.ArgumentParser()
    parser.add_argument("--receipt",type=Path,default=RECEIPT)
    parser.add_argument("--self-test",action="store_true")
    args=parser.parse_args()
    receipt=json.loads(args.receipt.read_text(encoding="utf-8"))
    expected=independent_rows()
    comparisons=validate(receipt,expected)
    print(f"R267 S63 primitive-source B gate PASS: 18 rows, {comparisons} comparison fields")
    if args.self_test:
        count=negative_controls(receipt,expected)
        print(f"Negative controls PASS: {count} rejected")


if __name__=="__main__":
    main()
