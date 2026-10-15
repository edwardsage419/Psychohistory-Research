#!/usr/bin/env python3
"""R064 exact-author-blob, frozen-protocol observational-learning analysis.

The manuscript direction was known before this retrospective evaluation. This
analysis is not an independent test of R063 metaVS and makes no causal claim.
Python >=3.10, standard library only. Never fetches or bundles personal data.
"""
from __future__ import annotations
import argparse
import csv
import hashlib
import io
import json
import math
from pathlib import Path

REPO = "arielevy8/obs-learning-fishing"
BLOB = "01bf211468abe093618dfa5e5c39e883230c9c03"
REQUIRED = ("participant_id", "stakes", "copied", "accurate", "comprehension_check_repetitions")
SEED = 20261015
BOOTSTRAPS = 20_000


def blob_sha(data: bytes) -> str:
    return hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()


def parse_source(raw: bytes) -> list[dict]:
    if blob_sha(raw) != BLOB:
        raise ValueError("FAIL CLOSED: processed source Git blob SHA1 mismatch")
    reader = csv.DictReader(io.StringIO(raw.decode("utf-8-sig"), newline=""))
    if not set(REQUIRED).issubset(set(reader.fieldnames or ())):
        raise ValueError("Required columns missing")
    return list(reader)


def prepare(rows: list[dict], min_paired: int = 10) -> tuple[list[dict], list[dict], dict]:
    missing = {k: 0 for k in REQUIRED}
    by_id: dict[str, dict] = {}
    valid_rows = 0
    for row in rows:
        if any(row.get(k) in (None, "", "NA", "NaN", "nan") for k in REQUIRED):
            for k in REQUIRED:
                if row.get(k) in (None, "", "NA", "NaN", "nan"):
                    missing[k] += 1
            continue
        pid = row["participant_id"]
        stakes = row["stakes"]
        if stakes not in ("low", "high"):
            raise ValueError("Stake level lacks unambiguous high/low label")
        copied, accurate = float(row["copied"]), float(row["accurate"])
        check = float(row["comprehension_check_repetitions"])
        if copied not in (0, 1) or accurate not in (0, 1) or not math.isfinite(check):
            raise ValueError("Invalid copied/accurate/check value")
        a = by_id.setdefault(pid, {"n": 0, "sum_acc": 0., "sum_check": 0.,
                                      "high": {"n": 0, "k": 0},
                                      "low": {"n": 0, "k": 0}})
        a["n"] += 1
        a["sum_acc"] += accurate
        a["sum_check"] += check
        a[stakes]["n"] += 1
        a[stakes]["k"] += int(copied)
        valid_rows += 1
    all_parts = list(by_id.values())
    excluded_a = excluded_c = excluded_union = excluded_rows = 0
    selected, full_pair = [], []
    eligible_without_both = 0
    for a in all_parts:
        both = a["high"]["n"] > 0 and a["low"]["n"] > 0
        if both:
            full_pair.append(a)
        fail_a = a["sum_acc"]/a["n"] < .45
        fail_c = a["sum_check"]/a["n"] > 2
        excluded_a += int(fail_a)
        excluded_c += int(fail_c)
        if fail_a or fail_c:
            excluded_union += 1
            excluded_rows += a["n"]
        elif both:
            selected.append(a)
        else:
            eligible_without_both += 1
    if len(selected) < min_paired:
        raise ValueError("FAIL CLOSED: fewer than required paired participants")
    checks = {"raw_rows": len(rows), "valid_complete_rows": valid_rows,
              "missing_by_required_field": missing, "raw_participants": len(all_parts),
              "excluded_accuracy": excluded_a, "excluded_comprehension": excluded_c,
              "excluded_union": excluded_union, "excluded_rows": excluded_rows,
              "eligible_both_stakes": len(selected),
              "eligible_without_both_stakes": eligible_without_both,
              "valid_paired_before_exclusion": len(full_pair)}
    return selected, full_pair, checks


def totals(parts: list[dict]) -> dict:
    return {stage + key: sum(a[stage][target] for a in parts)
            for stage in ("high", "low") for key, target in (("N", "n"), ("K", "k"))}


def describe(parts: list[dict]) -> dict:
    t = totals(parts)
    differences = [a["high"]["k"]/a["high"]["n"] -
                   a["low"]["k"]/a["low"]["n"] for a in parts]
    return {"participants": len(parts), "mean_participant_high_minus_low": sum(differences)/len(parts),
            "pooled_high_minus_low": t["highK"]/t["highN"]-t["lowK"]/t["lowN"],
            "high_rate": t["highK"]/t["highN"], "low_rate": t["lowK"]/t["lowN"],
            "totals": t,
            "minimum_high_trials": min(a["high"]["n"] for a in parts),
            "maximum_high_trials": max(a["high"]["n"] for a in parts),
            "minimum_low_trials": min(a["low"]["n"] for a in parts),
            "maximum_low_trials": max(a["low"]["n"] for a in parts)}


def predictions_for_subject(a: dict, total: dict) -> tuple[float,float,float]:
    """Leave-one-subject-out: no held-out outcomes enter any training rate."""
    hn, hk, ln, lk = (a["high"]["n"], a["high"]["k"],
                       a["low"]["n"], a["low"]["k"])
    global_rate = (total["highK"] + total["lowK"] - hk - lk + 4) / (
                   total["highN"] + total["lowN"] - hn - ln + 8)
    high_rate = (total["highK"]-hk+4)/(total["highN"]-hn+8)
    low_rate = (total["lowK"]-lk+4)/(total["lowN"]-ln+8)
    return global_rate, high_rate, low_rate


def score(n: int, k: int, p: float) -> tuple[float,float]:
    return (-(k*math.log(p)+(n-k)*math.log1p(-p))/n,
            (k*(1-p)**2+(n-k)*p*p)/n)


def per_subject_deltas(parts: list[dict]) -> tuple[list[dict], dict]:
    t = totals(parts)
    per=[]
    for a in parts:
        hn,hk=a["high"]["n"],a["high"]["k"]
        ln,lk=a["low"]["n"],a["low"]["k"]
        all_n=hn+ln
        p0, ph, pl = predictions_for_subject(a,t)
        l0,b0=score(all_n,hk+lk,p0)
        lh,bh=score(hn,hk,ph)
        ll,bl=score(ln,lk,pl)
        l1=(hn*lh+ln*ll)/all_n
        b1=(hn*bh+ln*bl)/all_n
        per.append({"stake":hk/hn-lk/ln, "loss":l1-l0, "brier":b1-b0,
                    "l0":l0,"l1":l1,"b0":b0,"b1":b1})
    n=len(per)
    mean=lambda k:sum(a[k] for a in per)/n
    wins=sum(a["loss"] < -1e-12 for a in per)
    ties=sum(abs(a["loss"])<=1e-12 for a in per)
    summary={"participants":n,
             "macro_log_loss_M0":mean("l0"),"macro_log_loss_M1":mean("l1"),
             "macro_loss_delta_M1_minus_M0":mean("loss"),
             "macro_brier_M0":mean("b0"),"macro_brier_M1":mean("b1"),
             "macro_brier_delta_M1_minus_M0":mean("brier"),
             "M1_wins":wins,"ties":ties,"M1_loses":n-wins-ties}
    return per,summary


def xorshift_random(seed=SEED):
    state = seed & 0xffffffff
    while True:
        state ^= (state << 13) & 0xffffffff
        state ^= state >> 17
        state ^= (state << 5) & 0xffffffff
        state &= 0xffffffff
        yield state/4294967296.0


def bootstrap_cis(per: list[dict], draws=BOOTSTRAPS, seed=SEED) -> dict:
    n=len(per)
    rng=xorshift_random(seed)
    draws_by_metric={"stake":[],"loss":[],"brier":[]}
    for _ in range(draws):
        sums={k:0.0 for k in draws_by_metric}
        for _ in range(n):
            a=per[int(next(rng)*n)]
            for k in sums:
                sums[k] += a[k]
        for k in sums:
            draws_by_metric[k].append(sums[k]/n)
    cis={}
    for k,vals in draws_by_metric.items():
        vals.sort()
        cis[k]=[vals[math.floor(.025*(draws-1))], vals[math.ceil(.975*(draws-1))]]
    return cis


def analysis(rows: list[dict], min_paired=10, draws=BOOTSTRAPS):
    selected,pre,checks=prepare(rows,min_paired)
    per,pred=per_subject_deltas(selected)
    return {"provenance":"ORIGINAL_BLOB_REQUIRED_FOR_LOCAL_REPLAY",
            "source_repo":REPO, "source_blob_sha1":BLOB,
            "schema_and_exclusion":checks,
            "primary_eligible":describe(selected),
            "sensitivity_before_exclusion":describe(pre),
            "predictive_leave_one_participant_out":pred,
            "bootstrap":{"method":"paired subject resampling", "draws":draws,
                         "seed":SEED,"intervals_95":bootstrap_cis(per,draws)},
            "interpretation":"Retrospective independent-author task; observational predictive contrast; no causal P-value; no R063 metaVS validation."}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source",type=Path,required=True,
                        help="Unmodified author's processed Git blob as an on-disk CSV")
    parser.add_argument("--output",type=Path,required=True)
    args=parser.parse_args()
    results=analysis(parse_source(args.source.read_bytes()))
    results["provenance"]="AUTHOR_PROCESSED_RAW_BLOB_LOCALLY_SHA1_VERIFIED"
    args.output.write_text(json.dumps(results,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    print(json.dumps({"status":"PASS", "source_blob":BLOB,
       "primary":results["primary_eligible"]["mean_participant_high_minus_low"]}))

if __name__=="__main__":
    main()
