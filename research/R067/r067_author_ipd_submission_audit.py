#!/usr/bin/env python3
"""Verify human repeated PD binary action schema using author's submission tag.

No individual IDs, per-session summaries or player timelines are exported.
Unproven equivalence with final Dryad v8 is a preserved source boundary.
"""
from __future__ import annotations
import argparse,csv,hashlib,io,json,math
from collections import Counter
from pathlib import Path

SUBMISSION_COMMIT="4743f74d8a03a031b8f70aff64956f8ad5155182"
FILES={
    "fix.csv":(988279,"3bf78bf85f6642afee18d6f1965dca7272582f40"),
    "rand.csv":(1112614,"f5a86cd033b739da45d3fc7c5019068f612146a2"),
}
REQUIRED=("round","player","action_player","opponent","action_opponent",
          "payoff","who_played","treatment","session")
MAX_LINES=200_000
MISSING=frozenset(("", "NA","NaN",".","--"))

def git_sha(raw):
    return hashlib.sha1(b"blob "+str(len(raw)).encode()+b"\0"+raw).hexdigest()

def audit_csv_bytes(filename,raw):
    size,expected=FILES[filename]
    if len(raw)!=size or git_sha(raw)!=expected:
        raise ValueError("file byte or Git source blob mismatch")
    reader=csv.DictReader(io.StringIO(raw.decode("utf-8-sig"),newline=""))
    names=reader.fieldnames
    if names is None or len(names)!=len(set(names)) or not set(REQUIRED).issubset(names):
        raise ValueError("author experimental source schema missing or duplicated")
    total=0
    valid_action=Counter()
    valid_opponent=Counter()
    treatment=Counter()
    who=Counter()
    sessions=set()
    players=set()
    opponent_ids=set()
    rounds=set()
    invalid_rounds=0
    duplicates=0
    seen_rounds=set()
    empty_id=0
    for row in reader:
        total+=1
        if total>MAX_LINES:
            raise ValueError("too many source observations")
        if None in row or any(v is None for v in row.values()):
            raise ValueError("source nonrectangular CSV")
        action=row["action_player"].strip()
        oppon=row["action_opponent"].strip()
        valid_action[action if action in ("C","D") else "OTHER_OR_MISSING"]+=1
        valid_opponent[oppon if oppon in ("C","D") else "OTHER_OR_MISSING"]+=1
        tr=row["treatment"].strip()
        treatment["fix" if tr=="fix" else "rand" if tr=="rand" else "OTHER_OR_MISSING"]+=1
        w=row["who_played"].strip()
        who["user" if w=="user" else "OTHER_OR_MISSING"]+=1
        session=row["session"].strip()
        player=row["player"].strip()
        opponent=row["opponent"].strip()
        if any(k in MISSING for k in (session,player)):
            empty_id+=1
        else:
            sessions.add(session)
            players.add((session,player))
        if opponent not in MISSING:
            opponent_ids.add((session,opponent))
        try:
            rv=float(row["round"])
            if not math.isfinite(rv) or not rv.is_integer() or rv<0:
                raise ValueError
            round_num=int(rv)
            rounds.add(round_num)
        except (ValueError,TypeError):
            invalid_rounds+=1
            round_num=None
        if round_num is not None and session not in MISSING and player not in MISSING:
            key=(session,player,round_num)
            if key in seen_rounds:
                duplicates+=1
            seen_rounds.add(key)
    if total<2 or not rounds or not sessions:
        raise ValueError("empty session/round universe")
    return {
        "source_git_blob_sha1":expected,
        "bytes":size,
        "source_rows":total,
        "columns":len(names),
        "safe_header_names":[n if n and len(n)<=80 and all(ch.isalnum() or ch in "._:" for ch in n) else "[redacted]" for n in names],
        "actions_player_C":valid_action["C"],
        "actions_player_D":valid_action["D"],
        "actions_player_other_or_missing":valid_action["OTHER_OR_MISSING"],
        "actions_opponent_C":valid_opponent["C"],
        "actions_opponent_D":valid_opponent["D"],
        "actions_opponent_other_or_missing":valid_opponent["OTHER_OR_MISSING"],
        "records_treatment_fix":treatment["fix"],
        "records_treatment_rand":treatment["rand"],
        "records_treatment_other_or_missing":treatment["OTHER_OR_MISSING"],
        "records_who_played_user":who["user"],
        "records_who_played_other_or_missing":who["OTHER_OR_MISSING"],
        "distinct_anonymous_session_count":len(sessions),
        "distinct_anonymous_session_player_count":len(players),
        "distinct_anonymous_session_opponent_count":len(opponent_ids),
        "round_min":min(rounds),
        "round_max":max(rounds),
        "distinct_round_numbers":len(rounds),
        "invalid_round_values":invalid_rounds,
        "session_player_round_repeat_rows":duplicates,
        "missing_session_or_player_rows":empty_id,
        "personal_ids_or_sequences_exported":False,
    }


def evaluate(folder):
    result={}
    for name in FILES:
        content=(folder/name).read_bytes()
        result[name]=audit_csv_bytes(name,content)
    all_valid=all(
        r["actions_player_other_or_missing"]==0 and
        r["invalid_round_values"]==0 and
        r["missing_session_or_player_rows"]==0
        for r in result.values())
    return {
        "research":"R067",
        "stage":"E2_AUTHOR_SUBMISSION_HUMAN_IPD_SOURCE_SCHEMA",
        "protocol":"protocols/R067_E2_AUTHOR_SUBMISSION_IPD_REAL_CSV_2026-10-16.md",
        "repository":"eladiomontero/PairwiseStrategies",
        "tag":"submission","commit":SUBMISSION_COMMIT,
        "status":"SOURCE_SCHEMA_VERIFIED" if all_valid else "ACTION_OR_ID_SEMANTICS_OPEN",
        "files":result,
        "same_bytes_as_final_dryad_v8":"UNKNOWN",
        "original_experiment_payoffs":{"R":3,"S":0,"T":4,"P":1},
        "experimental_payoff_different_from_R067_E1":True,
        "human_IPD_model_fit_performed":False,
        "individual_rows_published":False,
        "pesen_v01":"FROZEN",
    }


def main():
    p=argparse.ArgumentParser()
    p.add_argument("--source-dir",type=Path,required=True)
    p.add_argument("--output",type=Path,required=True)
    args=p.parse_args()
    try:
        result=evaluate(args.source_dir)
    except (OSError,ValueError,UnicodeError,csv.Error) as exc:
        result={"research":"R067",
                "stage":"E2_AUTHOR_SUBMISSION_HUMAN_IPD_SOURCE_SCHEMA",
                "status":"SOURCE_FAIL_CLOSED",
                "reason_type":type(exc).__name__,
                "reason":str(exc)[:200],
                "individual_rows_published":False,
                "pesen_v01":"FROZEN"}
    args.output.write_text(json.dumps(result,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({"status":result["status"],
                      "files":{k:{"rows":v["source_rows"],
                                  "sessions":v["distinct_anonymous_session_count"],
                                  "players":v["distinct_anonymous_session_player_count"],
                                  "actions_C":v["actions_player_C"],
                                  "actions_D":v["actions_player_D"],
                                  "other_actions":v["actions_player_other_or_missing"],
                                  "duplicates":v["session_player_round_repeat_rows"]}
                               for k,v in result.get("files",{}).items()}},sort_keys=True))
    if result["status"]=="SOURCE_FAIL_CLOSED":
        raise RuntimeError("source integrity audit failed")

if __name__=="__main__":
    main()
