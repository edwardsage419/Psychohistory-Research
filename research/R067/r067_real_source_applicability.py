#!/usr/bin/env python3
"""Real-source-only applicability gate; no R067 empirical model fit or binary recoding.

Uses byte-pinned original R047 CSV and author's model/theory scripts.
Dryad API section checks public catalog metadata only, never individual records.
"""
from __future__ import annotations
import argparse
import csv
import hashlib
import io
import json
import math
import re
import socket
from collections import Counter, defaultdict
from pathlib import Path
from urllib import error, parse, request

UPSTREAM_COMMIT="1142b0915a0a46e72264358378b3535948f6b2b4"
SOURCE_BLOB="73c02176bc9e060af987149594a85f9f7b591230"
EXPECTED_BYTES=239510
THEORY_BLOB="8b6f116b0e1f4b750ceb312a46a0b6f505faf09d"
MAX_METADATA_BYTES=1_000_000
DOI="10.5061/dryad.37pvmcvmk"
DRYAD_API="https://datadryad.org/api/v2/datasets/doi%3A10.5061%2Fdryad.37pvmcvmk"

def git_sha(raw:bytes)->str:
    return hashlib.sha1(b"blob "+str(len(raw)).encode()+b"\0"+raw).hexdigest()

def _numeric(val:str,integer=False):
    if val in ("", ".", "NA", "NaN"):
        raise ValueError("missing required numeric source field")
    z=float(val)
    if not math.isfinite(z) or (integer and not z.is_integer()):
        raise ValueError("invalid numeric original data")
    return int(z) if integer else z

def parse_original_r047(raw:bytes,theory:bytes):
    if len(raw)!=EXPECTED_BYTES or git_sha(raw)!=SOURCE_BLOB:
        raise ValueError("source data Git blob or length differs from pinned author")
    if git_sha(theory)!=THEORY_BLOB:
        raise ValueError("author theory Git blob differs from pinned source")
    text=theory.decode("utf-8")
    if "payoff = private + surplus_share*surplus_value" not in text or "0.025*surplus^2" not in text:
        raise ValueError("source formula identity not found")
    reader=csv.DictReader(io.StringIO(raw.decode("utf-8-sig"),newline=""))
    header=reader.fieldnames
    needed=("ProfileID","GameID","RoundID","Token","Invest","Session","FF","Homo")
    if header is None or any(key not in header for key in needed):
        raise ValueError("source R047 fields not recovered")
    active=[]
    empty_after=0
    for row in reader:
        if len(active)>=2048:
            if any((row.get(key) or "").strip() not in ("", ".") for key in needed):
                raise ValueError("unexpected nonblank original row after author 2048 boundary")
            empty_after+=1
            continue
        if not row.get("ProfileID","").strip():
            raise ValueError("empty row within author source 2048 boundary")
        active.append(row)
    if len(active)!=2048:
        raise ValueError("expected exactly 2048 original experimental rows before practice removal")
    participants=set()
    groups=defaultdict(list)
    treatments=Counter()
    by_endowment=Counter()
    condition_cells=Counter()
    all_invest=Counter()
    post_invest=Counter()
    per_person=Counter()
    for row in active:
        person=str(row["ProfileID"])
        gid=_numeric(row["GameID"],True)
        session=_numeric(row["Session"],True)
        roundid=_numeric(row["RoundID"],True)
        token=_numeric(row["Token"],True)
        invest=_numeric(row["Invest"])
        ff=_numeric(row["FF"],True)
        homo=_numeric(row["Homo"],True)
        if ff not in (0,1) or homo not in (0,1):
            raise ValueError("unexpected experiment binary conditions")
        if roundid not in range(1,17) or token not in (40,50,60):
            raise ValueError("unexpected endowment or round")
        if invest<0 or invest>token:
            raise ValueError("Invest outside source endowment")
        group=100*homo+10*session+gid
        groups[group].append((person,roundid,invest))
        participants.add(person)
        per_person[person]+=1
        all_invest[invest]+=1
        treatments[ff]+=1
        by_endowment[token]+=1
        condition_cells[(ff,homo)]+=1
        if roundid!=1:
            post_invest[invest]+=1
    if (len(participants)!=128 or len(groups)!=32 or
        any(v!=16 for v in per_person.values()) or
        any(len(rows)!=64 for rows in groups.values())):
        raise ValueError("source participant/group/round source universe mismatch")
    for key,rows in groups.items():
        rounds=Counter(roundid for _,roundid,_ in rows)
        if set(rounds)!=set(range(1,17)) or any(c!=4 for c in rounds.values()):
            raise ValueError("group rounds or participant count mismatch")
    post=1920
    if sum(post_invest.values())!=post:
        raise ValueError("practice-round exclusion mismatch")
    group_multiaction=sum(
        len({invest for _,r,invest in rows if r!=1})>=3
        for rows in groups.values()
    )
    # Invest is a number of units extracted. It is not C vs D of a
    # prespecified binary treatment with a 2x2 game payoff matrix.
    return {
        "source_status":"R047_ORIGINAL_BYTES_AND_STRUCTURE_PASS",
        "source_git_blob":SOURCE_BLOB,
        "theory_git_blob":THEORY_BLOB,
        "source_bytes":len(raw),
        "raw_experimental_rows":len(active),
        "source_tail_blank_rows_ignored":empty_after,
        "post_practice_rows":post,
        "distinct_participants":len(participants),
        "distinct_four_person_groups":len(groups),
        "participant_rows_per_person":16,
        "periods":16,
        "practice_period_excluded":1,
        "endowment_counts":{str(k):v for k,v in sorted(by_endowment.items())},
        "punishment_FF_condition_counts":{str(k):v for k,v in sorted(treatments.items())},
        "condition_FF_by_Homo_counts":{f"FF={k[0]},Homo={k[1]}":v for k,v in sorted(condition_cells.items())},
        "Invest_unique_values_all_rounds":len(all_invest),
        "Invest_unique_values_postpractice":len(post_invest),
        "Invest_min_postpractice":min(post_invest),
        "Invest_max_postpractice":max(post_invest),
        "groups_with_three_or_more_distinct_postpractice_extractions":group_multiaction,
        "source_mechanism":"CONTINUOUS_OR_MULTILEVEL_COMMON_POOL_EXTRACTION_WITH_NONLINEAR_SURPLUS_AND_SANCTION_CONDITIONS",
        "binary_cooperate_defect_directly_observed":False,
        "exact_2x2_PD_payoff_mapping":"NOT_ESTABLISHED",
        "fixed_R067_PD_e2_fit":"BLOCKED_MODEL_MISMATCH",
        "binary_recoding_undertaken":False,
        "no_person_rows_or_IDs_redistributed":True,
    }

def dryad_catalog_probe(opener=request.urlopen):
    req=request.Request(DRYAD_API,headers={"Accept":"application/json",
                                             "User-Agent":"R067-source-catalog-audit/1.0"})
    try:
        with opener(req,timeout=15) as resp:
            status=resp.status
            raw=resp.read(MAX_METADATA_BYTES+1)
        if len(raw)>MAX_METADATA_BYTES:
            return {"catalog_status":"RESPONSE_LIMIT_EXCEEDED"}
        payload=json.loads(raw.decode("utf-8"))
    except error.HTTPError as exc:
        return {"catalog_status":"HTTP_UNRESOLVED","http_status":exc.code}
    except (socket.timeout, TimeoutError, error.URLError, OSError):
        return {"catalog_status":"NETWORK_OR_API_UNRESOLVED"}
    except (ValueError, UnicodeError):
        return {"catalog_status":"INVALID_API_SCHEMA"}
    if status!=200 or not isinstance(payload,dict):
        return {"catalog_status":"INVALID_API_SCHEMA","http_status":status}
    # Dryad v2 API metadata: a DOI and published record URL, not data bytes.
    record_doi=str(payload.get("identifier",""))[:200]
    if DOI not in record_doi and record_doi.lower() not in (DOI.lower(),"doi:"+DOI.lower()):
        return {"catalog_status":"IDENTITY_UNRESOLVED",
                "reported_identifier":record_doi}
    files=payload.get("versionFiles")
    count=None
    if isinstance(files,list):
        count=len(files)
    license=payload.get("license")
    return {"catalog_status":"PUBLIC_METADATA_MATCHES_DOI",
            "dataset_doi":DOI,
            "metadata_identifier":record_doi,
            "version_label":str(payload.get("versionNumber",""))[:32],
            "public_license":str(license)[:200] if license is not None else None,
            "version_file_count_if_included":count,
            "raw_participant_files_read":False}

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--r047-csv",type=Path,required=True)
    p.add_argument("--theory",type=Path,required=True)
    p.add_argument("--output",type=Path,required=True)
    args=p.parse_args()
    try:
        source=parse_original_r047(args.r047_csv.read_bytes(),args.theory.read_bytes())
    except (ValueError,OSError,UnicodeError,csv.Error) as exc:
        source={"source_status":"R047_SOURCE_FAIL_CLOSED",
                "error_type":type(exc).__name__,
                "failure_reason":str(exc)[:220],
                "binary_recoding_undertaken":False}
    cat=dryad_catalog_probe()
    out={"study":"R067",
         "stage":"E2_R047_AND_BINARY_PD_SOURCE_APPLICABILITY",
         "protocol":"protocols/R067_E2_BEHAVIORAL_DATA_APPLICABILITY_2026-10-16.md",
         "original_repo":"lrdegeest/InequalityCPR",
         "original_commit":UPSTREAM_COMMIT,
         "source_A":source,
         "candidate_B_dryad_catalog":cat,
         "human_pd_behavioral_data_fitted":False,
         "pesen_v01":"FROZEN"}
    args.output.write_text(json.dumps(out,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({"stage":out["stage"],"R047":source["source_status"],
                      "distinct_extractions":source.get("Invest_unique_values_postpractice"),
                      "group_ge3_extractions":source.get("groups_with_three_or_more_distinct_postpractice_extractions"),
                      "dryad_catalog":cat["catalog_status"]},sort_keys=True))
    if source["source_status"]!="R047_ORIGINAL_BYTES_AND_STRUCTURE_PASS":
        raise RuntimeError("R047 exact source gate failed")

if __name__=="__main__":
    main()
