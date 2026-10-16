#!/usr/bin/env python3
"""R068: anonymous temporal semantics of four-option social frequency cues.

No model fitting. Temporal cue comes from previous round and self's last
choice is subtracted as in author's fixed R implementation. Outputs only
overall counts; no IDs, single-group stats or trial histories are exported.
"""
from __future__ import annotations
import argparse,csv,hashlib,io,json,math
from collections import Counter,defaultdict
from pathlib import Path
from r068_toyokawa_lfs_schema import FILE_SPEC,COMMIT

CUES=("socialFreq_safe1","socialFreq_safe2","socialFreq_safe3","socialFreq_risky")
REQUIRED=("amazonID","room","round","riskDistributionId","choice_num","payoff")+CUES
MISSING=frozenset(("",".","NA","NaN","null"))
SOURCE_ROWS={"allBehaviour1022_group.csv":12880,
             "allBehaviour1022_indiv.csv":7929}


def maybe_int(v):
    s=str(v).strip()
    if s in MISSING:return None
    try:x=float(s)
    except ValueError:return None
    if not math.isfinite(x) or not x.is_integer():
        return None
    return int(x)


def parse_source(filename,raw):
    spec=FILE_SPEC[filename]
    if len(raw)!=spec["size"] or hashlib.sha256(raw).hexdigest()!=spec["sha256"]:
        raise ValueError("LFS_SOURCE_BYTES_NOT_PINNED")
    rd=csv.DictReader(io.StringIO(raw.decode("utf-8-sig"),newline=""))
    names=rd.fieldnames
    if names is None or len(names)!=len(set(names)) or not set(REQUIRED).issubset(names):
        raise ValueError("MISSING_OR_DUPLICATE_SOURCE_SEMANTIC_FIELDS")
    records=list(rd)
    if len(records)!=SOURCE_ROWS[filename] or any(
       None in row or any(value is None for value in row.values()) for row in records):
        raise ValueError("ORIGINAL_SOURCE_ROW_UNIVERSE_DRIFT")
    return records


def audit_semantics(rows_group,rows_indiv):
    def key(r):
        return r["amazonID"].strip(),maybe_int(r["round"])
    index={}
    duplicate_identity_round=0
    cross_room_people=set()
    people_room=defaultdict(set)
    rooms_conditions=defaultdict(set)
    missing_ids=0
    rounds_bad=0
    task_count=Counter()
    option_codes=Counter()
    for row in rows_group:
        rid=key(row)
        identity,round_num=rid
        if not identity:
            missing_ids+=1
            continue
        if round_num is None or not 1<=round_num<=70:
            rounds_bad+=1
            continue
        if rid in index:
            duplicate_identity_round+=1
        index[rid]=row
        people_room[identity].add(row["room"])
        rooms_conditions[row["room"]].add(row["riskDistributionId"])
        task_count[row["riskDistributionId"]]+=1
        ch=maybe_int(row["choice_num"])
        option_codes[str(ch) if ch in (-1,0,1,2,3) else "OTHER_OR_MISSING"]+=1
    cross_room_people={p for p,ss in people_room.items() if len(ss)>1}
    mixed_rooms={r for r,task in rooms_conditions.items() if len(task)>1}
    mixed_rows=sum(row["room"] in mixed_rooms for row in rows_group)
    count=Counter()
    for row in rows_group:
        count["all_group_source_rows"]+=1
        identity,round_num=key(row)
        if not identity or round_num is None or not 1<=round_num<=70:
            count["unusable_id_or_round_rows"]+=1
            continue
        if round_num==1:
            count["first_trial_unscorable"]+=1
            continue
        prev=index.get((identity,round_num-1))
        if prev is None or prev["room"]!=row["room"]:
            count["missing_same_room_prior_self_choice"]+=1
            continue
        last=maybe_int(prev["choice_num"])
        current=maybe_int(row["choice_num"])
        if last not in (0,1,2,3) or current not in (0,1,2,3):
            count["previous_or_current_choice_invalid"]+=1
            continue
        cues=[maybe_int(row[name]) for name in CUES]
        if any(f is None or f<0 for f in cues):
            count["noninteger_or_missing_social_freq"]+=1
            continue
        count["previous_round_self_choice_and_four_cues_available"]+=1
        cues[last]-=1
        if any(f<0 for f in cues):
            count["negative_after_self_exclusion"]+=1
            continue
        count["valid_author_self_excluded_nonnegative_frequencies"]+=1
        if sum(cues)==0:
            count["zero_observed_peers"]+=1
        else:
            count["at_least_one_observed_peer_choice"]+=1
            if row["room"] in mixed_rooms:
                count["valid_cues_with_mixed_task_room"]+=1
        if row["room"] in mixed_rooms:
            count["all_valid_cues_in_mixed_task_room"]+=1
    indiv_ids=set()
    indiv_rooms=set()
    indiv_rounds=Counter()
    for row in rows_indiv:
        if row["amazonID"].strip():
            indiv_ids.add(row["amazonID"].strip())
        indiv_rooms.add(row["room"])
        num=maybe_int(row["round"])
        if num is None or not 1<=num<=70:
            indiv_rounds["bad_or_missing"]+=1
        else:
            indiv_rounds["valid"]+=1
    safe_task_categories={}
    for task,v in task_count.items():
        label=task if task in ("11","12") else "[other_code]"
        safe_task_categories[label]=safe_task_categories.get(label,0)+v
    return {
        "source_status":"SOURCE_SHA_AND_4_OPTION_TEMPORAL_STRUCTURE_AUDITED",
        "group_source_rows":len(rows_group),
        "individual_source_rows":len(rows_indiv),
        "group_distinct_anonymous_people":len(people_room),
        "group_distinct_anonymous_rooms":len(rooms_conditions),
        "individual_distinct_anonymous_people":len(indiv_ids),
        "individual_distinct_anonymous_rooms":len(indiv_rooms),
        "individual_round_valid_rows":indiv_rounds["valid"],
        "individual_round_bad_rows":indiv_rounds["bad_or_missing"],
        "duplicate_group_person_round_key_rows":duplicate_identity_round,
        "group_people_in_multiple_rooms":len(cross_room_people),
        "group_blank_identity_rows":missing_ids,
        "group_invalid_trial_round_rows":rounds_bad,
        "group_rooms_with_multiple_risk_distribution_codes":len(mixed_rooms),
        "group_rows_in_mixed_task_rooms":mixed_rows,
        "source_group_task_rows":safe_task_categories,
        "group_choice_option_codes":dict(sorted(option_codes.items())),
        "temporal_source_check_counts":dict(sorted(count.items())),
        "trial_level_observed_demonstrator_payoffs_provided_to_learners":False,
        "three_independent_demonstrators_directly_observed":False,
        "semantic_gate":("FOUR_CHOICE_PREVIOUS_TRIAL_CUES_RECOVERABLE" if
                         count["at_least_one_observed_peer_choice"]>0 and
                         duplicate_identity_round==0 and
                         not cross_room_people else "SOURCE_TEMPORAL_MAPPING_BLOCKED"),
        "full_original_hierarchical_R_model_fitted":False,
        "individual_rows_or_ids_redistributed":False,
        "pesen_v01":"FROZEN",
    }


def main():
    p=argparse.ArgumentParser()
    p.add_argument("--source-dir",type=Path,required=True)
    p.add_argument("--output",type=Path,required=True)
    a=p.parse_args()
    try:
        group=parse_source("allBehaviour1022_group.csv",
                           (a.source_dir/"allBehaviour1022_group.csv").read_bytes())
        indiv=parse_source("allBehaviour1022_indiv.csv",
                           (a.source_dir/"allBehaviour1022_indiv.csv").read_bytes())
        metrics=audit_semantics(group,indiv)
        result={"research":"R068",
                "stage":"E2_TOYOKAWA_FOUR_OPTION_TEMPORAL_CUE_AUDIT",
                "protocol":"protocols/R068_E2_TOYOKAWA_SOURCE_TEMPORAL_SEMANTICS_2026-10-16.md",
                "source_repo":"WataruToyokawa/ToyokawaGaissmaier2021",
                "source_commit":COMMIT,
                "source_lfs_sha256":{n:x["sha256"] for n,x in FILE_SPEC.items()},
                **metrics}
    except (OSError,ValueError,UnicodeError,csv.Error) as exc:
        result={"research":"R068",
                "stage":"E2_TOYOKAWA_FOUR_OPTION_TEMPORAL_CUE_AUDIT",
                "source_status":"SOURCE_FAIL_CLOSED",
                "reason_type":type(exc).__name__,
                "reason":str(exc)[:150],
                "pesen_v01":"FROZEN"}
    a.output.write_text(json.dumps(result,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    print(json.dumps({"source_status":result["source_status"],
                     "semantic_gate":result.get("semantic_gate"),
                     "temporal_counts":result.get("temporal_source_check_counts"),
                     "mixed_task_rooms":result.get("group_rooms_with_multiple_risk_distribution_codes")},
                    sort_keys=True))
    if result["source_status"]=="SOURCE_FAIL_CLOSED":
        raise RuntimeError("R068 temporal source structure audit failed")


if __name__=="__main__":
    main()
