#!/usr/bin/env python3
"""Read-only source-identity and session audit of a public human experiment CSV."""
from __future__ import annotations
import argparse
import csv
from collections import Counter
import hashlib
import io
import json
from pathlib import Path

EXPECTED_GIT_BLOB = "f5767dd72928b16eaa30c8cc67af15b17ad25d4c"
EXPECTED_SESSION_ROWS = {"C1":240,"C2":400,"T1":480,"T2":480,"T3":400,"T4":400}
EXPECTED_SESSION_SUBJECTS = {"C1":24,"C2":20,"T1":24,"T2":24,"T3":20,"T4":20}
REQUIRED = {"session","period","subject","group","contrib","profit",
            "pun1","pun2","pun3","con1","con2","con3","opp1","opp2","opp3"}

def git_blob_hash(raw: bytes) -> str:
    return hashlib.sha1(b"blob "+str(len(raw)).encode()+b"\0"+raw).hexdigest()

def audit_rows(rows: list[dict], headers: list[str]) -> dict:
    if len(headers)!=28 or not REQUIRED.issubset(headers):
        raise ValueError("SCHEMA_MISMATCH")
    if len(rows)!=2400:
        raise ValueError("ROW_COUNT_MISMATCH")
    session_counts=Counter()
    subject_by_session={}
    periods_by_session={}
    group_period=Counter()
    seen=set()
    for row in rows:
        s=row["session"]
        if s not in EXPECTED_SESSION_ROWS:
            raise ValueError("UNKNOWN_SESSION")
        key=(s,row["period"],row["subject"])
        if key in seen:
            raise ValueError("DUPLICATE_SESSION_PERIOD_SUBJECT")
        seen.add(key)
        session_counts[s]+=1
        subject_by_session.setdefault(s,set()).add(row["subject"])
        periods_by_session.setdefault(s,set()).add(row["period"])
        group_period[(s,row["period"],row["group"])]+=1
        if not row["contrib"]:
            raise ValueError("MISSING_CONTRIBUTION")
    if dict(session_counts)!=EXPECTED_SESSION_ROWS:
        raise ValueError("SESSION_ROW_COUNTS_MISMATCH")
    if {s:len(v) for s,v in subject_by_session.items()}!=EXPECTED_SESSION_SUBJECTS:
        raise ValueError("SESSION_SUBJECT_COUNTS_MISMATCH")
    if set(group_period.values())!={4}:
        raise ValueError("GROUP_PERIOD_SIZE_NOT_FOUR")
    labels=Counter(subject for subjects in subject_by_session.values() for subject in subjects)
    return {"rows":len(rows),"columns":len(headers),
            "session_rows":dict(sorted(session_counts.items())),
            "session_subjects":{s:len(v) for s,v in sorted(subject_by_session.items())},
            "session_periods":{s:len(v) for s,v in sorted(periods_by_session.items())},
            "unique_session_subject_keys":sum(map(len,subject_by_session.values())),
            "numeric_subject_labels_reused_across_sessions":sum(n>1 for n in labels.values()),
            "group_period_cells":len(group_period),"group_size":4}

def audit(raw: bytes):
    sha=git_blob_hash(raw)
    if sha!=EXPECTED_GIT_BLOB:
        raise ValueError("SOURCE_GIT_BLOB_MISMATCH")
    parsed=csv.DictReader(io.StringIO(raw.decode("utf-8")))
    headers=parsed.fieldnames
    rows=list(parsed)
    result=audit_rows(rows,headers)
    negatives=0
    changed=[dict(x) for x in rows]
    changed[1]=dict(changed[0])
    try:
        audit_rows(changed,headers)
    except ValueError:
        negatives+=1
    changed=[dict(x) for x in rows]
    changed[0]["session"]="UNKNOWN"
    try:
        audit_rows(changed,headers)
    except ValueError:
        negatives+=1
    if negatives!=2:
        raise AssertionError("NEGATIVE_CONTROL_FAILURE")
    return {"source_git_blob_sha1":sha,"status":"SOURCE_BYTES_AND_STRUCTURE_VERIFIED",
            "negative_controls_rejected":negatives,
            "new_R073_external_E2_predictions":0,
            "dataset_kind":"human_public_goods_punishment_not_repeated_PD",
            "license":"NOT_IDENTIFIED_DO_NOT_REDISTRIBUTE",**result}

if __name__=="__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("--file",required=True,type=Path)
    args=parser.parse_args()
    print(json.dumps(audit(args.file.read_bytes()),indent=2,sort_keys=True))
