#!/usr/bin/env python3
"""R258 S54 cross-route exact comparison and negative receipt tests.

Run from any checkout: python research/evidence_audit/b_r258_s54_crossroute_gate_20261029.py
This checks 3456 policy-level expectations, not just 54 minima.
"""
from __future__ import annotations
import importlib.util
import json
from fractions import Fraction as F
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]

def load(name, relative):
    path=ROOT/relative
    spec=importlib.util.spec_from_file_location(name,path)
    mod=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

R=load("s54_r","research/validation/r258_s54_coarse_state_observation_20261029.py")
B=load("s54_b","research/evidence_audit/b_r258_s54_distribution_oracle_20261029.py")

def validate_receipt(rows):
    if len(rows)!=27:raise ValueError("incorrect world-initial count")
    expected={(w,x) for w in R.WORLDS for x in range(3)}
    if {(r["world"],r["x0"]) for r in rows}!=expected:
        raise ValueError("incomplete or unknown world-initial key")
    if len({(r["world"],r["x0"]) for r in rows})!=27:
        raise ValueError("duplicate world-initial key")
    for row in rows:
        world,x0=row["world"],row["x0"]
        if F(row["V_full"])!=F(R.BASELINE[world][0][x0]):
            raise ValueError("changed full-state baseline")
        if F(row["V_open"])!=F(R.BASELINE[world][1][x0]):
            raise ValueError("changed open-loop baseline")
        for sensor in ("A","B"):
            full,opened,value=(F(row[k]) for k in ("V_full","V_open","V_"+sensor))
            if not full<=value<=opened:raise ValueError("policy class nesting violated")
            if F(row["gap_"+sensor])!=value-full:raise ValueError("gap mismatch")
            if F(row["open_minus_"+sensor])!=opened-value:raise ValueError("open gap mismatch")
            if not (type(row["minimizer_count_"+sensor]) is int and
                    1<=row["minimizer_count_"+sensor]<=64):
                raise ValueError("invalid minimizer count")

def main():
    if len(R.POLICIES)!=64 or len(B.POLICIES)!=64 or R.POLICIES!=B.POLICIES:
        raise AssertionError("policy universe mismatch")
    compared=0
    for world in R.WORLDS:
        for x0 in range(3):
            for sensor in ("A","B"):
                for policy in R.POLICIES:
                    r=R.expected_cost(world,x0,sensor,policy)
                    b=B.evaluate_distribution(B.CONFIG[world],x0,sensor,policy)
                    if r!=b:raise AssertionError((world,x0,sensor,policy,r,b))
                    compared+=1
    if compared!=3456:raise AssertionError("incomplete comparison")
    rows=R.receipt()["results"]
    validate_receipt(rows)
    independent=B.results()
    if rows!=independent:raise AssertionError("27-row independent oracle mismatch")
    import copy
    for mutation in ("duplicate","gap","value","fraction"):
        changed=copy.deepcopy(rows)
        if mutation=="duplicate":changed[1]=copy.deepcopy(changed[0])
        elif mutation=="gap":changed[0]["gap_A"]="999"
        elif mutation=="value":changed[0]["V_B"]="999"
        else:changed[0]["gap_A"]="invalid/0"
        try:validate_receipt(changed)
        except (ValueError,ZeroDivisionError):pass
        else:raise AssertionError("false acceptance: "+mutation)
    print(json.dumps({"status":"PASS","exact_policy_comparisons":compared,
                      "complete_world_initial_pairs":27,"negative_mutations_rejected":4,
                      "scope":"internal_E1_only_no_external_replication"},indent=2))

if __name__=="__main__":main()
