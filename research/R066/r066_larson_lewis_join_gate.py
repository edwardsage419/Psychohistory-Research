#!/usr/bin/env python3
"""R066 E2: strict-source village ego/alter join feasibility and six-item wave audit.

Never emits any individual ID, individual opinion, village-specific row, or edge.
A successful join is NOT an empirically identified DeGroot/FJ/HK influence model.
"""
from __future__ import annotations
import argparse,csv,hashlib,io,json,math
from collections import Counter
from pathlib import Path
from r066_larson_lewis_semantic_mapping import PINNED_SHA256
from r066_larson_lewis_public_schema import FILES

ITEMS=("noprob","fit","burden","values","land","threat")
WAVES={"candidate_baseline":"1","candidate_immediate":"2",
       "candidate_endline":"_e"}
NETWORKS={"visit":("visit1","visit2","visit3","visit4","visit5"),
          "meal":("meal1","meal2","meal3","meal4","meal5"),
          "borrow":("borrow1","borrow2","borrow3","borrow4","borrow5"),
          "rumor":("rumor1","rumor2","rumor3","rumor4","rumor5")}
MISSING=frozenset(("", "NA", "NaN", "\\N", "."))
SCHEMA_ROWS=2125
SCHEMA_COLS=66


def clean_id(val: str) -> str | None:
    s=val.strip()
    return None if s in MISSING else s


def parse_response(raw: str):
    s=raw.strip()
    if s in MISSING:
        return "missing",None
    try:
        x=float(s)
    except ValueError:
        return "non_numeric",None
    if not math.isfinite(x):
        return "non_numeric",None
    return ("within_1_5" if 1<=x<=5 else "outside_1_5"),x


def analyze_rows(headers,rows):
    if len(rows)!=SCHEMA_ROWS or len(headers)!=SCHEMA_COLS:
        raise ValueError("source universe not 2125 rows / 66 fields")
    if len(headers)!=len(set(headers)):
        raise ValueError("duplicate source fieldnames")
    needed={"village_number","ego","trt","in_el"}
    needed.update(x+suffix for suffix in WAVES.values() for x in ITEMS)
    needed.update(name for names in NETWORKS.values() for name in names)
    if not needed.issubset(set(headers)):
        raise ValueError("required field universe missing")
    persons={}
    repeated_keys=0
    invalid_person_keys=0
    for row in rows:
        village=clean_id(row["village_number"])
        ego=clean_id(row["ego"])
        if village is None or ego is None:
            invalid_person_keys+=1
            continue
        key=(village,ego)
        if key in persons:
            repeated_keys+=1
        persons[key]=True
    referenced_villages={key[0] for key in persons}
    waves={}
    valid_by_wave={}
    for phase,suffix in WAVES.items():
        summary={}
        completed=set()
        for prefix in ITEMS:
            name=prefix+suffix
            count=Counter()
            observed=[]
            for row in rows:
                status,x=parse_response(row[name])
                count[status]+=1
                if x is not None:
                    observed.append(x)
            summary[name]={
                "missing_token_rows":count["missing"],
                "non_numeric_rows":count["non_numeric"],
                "outside_1_5_rows":count["outside_1_5"],
                "within_1_5_rows":count["within_1_5"],
                "min_numeric":min(observed) if observed else None,
                "max_numeric":max(observed) if observed else None,
            }
        for i,row in enumerate(rows):
            if all(parse_response(row[x+suffix])[0]=="within_1_5" for x in ITEMS):
                completed.add(i)
        valid_by_wave[phase]=completed
        waves[phase]={"complete_six_item_rows":len(completed),"items":summary}
    edges={}
    any_neighbor=set()
    for label,columns in NETWORKS.items():
        nominations=0
        matched=0
        unmatched=0
        self_nominations=0
        known_targets=set()
        nominators=set()
        for i,row in enumerate(rows):
            village=clean_id(row["village_number"])
            ego=clean_id(row["ego"])
            for name in columns:
                alter=clean_id(row[name])
                if alter is None:
                    continue
                nominations+=1
                if village is not None and (village,alter) in persons:
                    matched+=1
                    nominators.add(i)
                    any_neighbor.add(i)
                    known_targets.add((village,alter))
                    if alter==ego:
                        self_nominations+=1
                else:
                    unmatched+=1
        edges[label]={
            "nonmissing_nomination_slots":nominations,
            "within_village_exact_ego_matches":matched,
            "unmatched_or_outside_village":unmatched,
            "unique_target_nodes_across_all_villages":len(known_targets),
            "nominators_with_matched_edge":len(nominators),
            "self_nominations":self_nominations,
            "match_fraction":matched/nominations if nominations else None
        }
    treatment={}
    for name in ("trt","treatment_type","in_el"):
        if name not in headers:
            continue
        vals=[clean_id(row[name]) for row in rows]
        treatment[name]={
            "nonmissing":sum(v is not None for v in vals),
            "distinct_nonmissing_codes":len({v for v in vals if v is not None}),
        }
    joined=sum(x["within_village_exact_ego_matches"] for x in edges.values())
    unique_keys=repeated_keys==0 and invalid_person_keys==0 and len(persons)==SCHEMA_ROWS
    return {
        "rows":len(rows),"columns":len(headers),"distinct_villages":len(referenced_villages),
        "unique_within_village_ego_keys":len(persons),
        "duplicate_within_village_ego_keys":repeated_keys,
        "missing_village_or_ego_keys":invalid_person_keys,
        "all_nodes_have_at_least_one_matched_nomination":len(any_neighbor)==SCHEMA_ROWS,
        "nodes_with_any_matched_outgoing_nomination":len(any_neighbor),
        "network_nomination_summaries":edges,
        "wave_item_checks":waves,
        "complete_candidate_baseline_and_endline_rows":len(
            valid_by_wave["candidate_baseline"] & valid_by_wave["candidate_endline"]),
        "complete_candidate_all_three_waves_rows":len(
            valid_by_wave["candidate_baseline"] &
            valid_by_wave["candidate_immediate"] &
            valid_by_wave["candidate_endline"]),
        "study_treatment_fields":treatment,
        "join_candidate_status":("JOIN_CANDIDATE_SUPPORTED" if unique_keys and joined>0
                                 else "JOIN_CANDIDATE_BLOCKED"),
        "wave_candidate_status":(
            "WAVE_INDEX_CANDIDATE_SUPPORTED"
            if len(valid_by_wave["candidate_baseline"] & valid_by_wave["candidate_endline"])>0
            else "WAVE_INDEX_CANDIDATE_BLOCKED"),
        "all_source_respondent_rows_kept_private":True,
        "scoring_direction_confirmed":False,
        "real_model_fit_performed":False,
        "model_identification_ready":"OPEN",
    }


def audit_source(source_dir:Path):
    raw={}
    for label,(fname,_,size) in FILES.items():
        b=(source_dir/fname).read_bytes()
        if len(b)!=size or hashlib.sha256(b).hexdigest()!=PINNED_SHA256[label]:
            raise ValueError("FAIL CLOSED: pinned upstream bytes "+label)
        raw[label]=b
    csv_text=raw["data"].decode("utf-8-sig")
    rdr=csv.DictReader(io.StringIO(csv_text,newline=""),delimiter="\t")
    if rdr.fieldnames is None or len(rdr.fieldnames)!=SCHEMA_COLS:
        raise ValueError("expected exactly 66 columns")
    headers=rdr.fieldnames
    records=[]
    for row in rdr:
        if None in row or any(v is None for v in row.values()):
            raise ValueError("unexpected TSV row width")
        records.append(row)
        if len(records)>SCHEMA_ROWS:
            raise ValueError("record count exceeded frozen universe")
    result=analyze_rows(headers,records)
    return {
        "stage":"R066_E2_VILLAGE_NETWORK_AND_ATTITUDE_WAVE_JOIN",
        "source_dataset":"doi:10.7910/DVN/RAHSVM",
        "version":"1.0",
        "fixed_sha256":PINNED_SHA256,
        "status":"SOURCE_VERIFIED",
        "anonymous_aggregate":result,
        "evidence_limit":"SOURCE_SCHEMA_AND_JOIN_FEASIBILITY_ONLY",
        "original_person_records_redistributed":False,
        "pesen_v01":"FROZEN",
    }


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--source-dir",type=Path,required=True)
    ap.add_argument("--output",type=Path,required=True)
    args=ap.parse_args()
    try:
        result=audit_source(args.source_dir)
    except (ValueError,OSError,UnicodeError,csv.Error) as e:
        result={"stage":"R066_E2_VILLAGE_NETWORK_AND_ATTITUDE_WAVE_JOIN",
                "status":"SOURCE_OR_SCHEMA_BLOCKED",
                "reason_type":type(e).__name__,"reason":str(e)[:180],
                "model_identification_ready":"OPEN","pesen_v01":"FROZEN"}
    args.output.write_text(json.dumps(result,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    agg=result.get("anonymous_aggregate",{})
    print(json.dumps({"stage":result["stage"],"status":result["status"],
                      "villages":agg.get("distinct_villages"),
                      "join_candidate":agg.get("join_candidate_status"),
                      "baseline_endline_complete":agg.get("complete_candidate_baseline_and_endline_rows"),
                      "nominations":{k:(v["within_village_exact_ego_matches"],v["nonmissing_nomination_slots"])
                                     for k,v in agg.get("network_nomination_summaries",{}).items()}},
                     sort_keys=True))
    if result["status"]!="SOURCE_VERIFIED":
        raise RuntimeError("source blocked; do not fit real models")


if __name__=="__main__":
    main()
