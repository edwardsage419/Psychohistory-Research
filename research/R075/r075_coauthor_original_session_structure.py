#!/usr/bin/env python3
"""R075 coauthor original text structural audit, no human model prediction.

Check only original-author data provenance, treatment/session universe, temporal
and pairing keys, observed-lag field domains. Raw participants remain private.
"""
from __future__ import annotations
import argparse
from collections import Counter,defaultdict
import csv,hashlib,io,json
from pathlib import Path
import re
import zipfile
from urllib.request import urlopen,Request

ORIGINAL_URL="https://davidrand-cooperation.com/s/slow-to-anger-and-fast-to-forgive-data-and-code.zip"
ORIGINAL_SHA256="328346c3cf88a71a3d6cf574f7d6ba741dcea460f3926c16266f1784d3a699ef"
ORIGINAL_ZIP_BYTES=1129409
ORIGINAL_TEXT_ROWS=34446
EXPECTED_HEADERS=(
    "file","bc","error","subject","interaction","group","period","payoff",
    "decision","others1stInt","you_p_1","other_p_1","you_p_2","other_p_2",
    "numInteractions","leniency","forgiveness","overallC_last4_act",
    "firstC_last4_act","overallC_last4","firstC_last4","overallC_all",
    "overallC_all_act","ALLD",
)
SMALL_ACTION_FIELDS=("decision","you_p_1","other_p_1","you_p_2","other_p_2")

def original_text_from_verified_zip(blob:bytes)->bytes:
    if len(blob)!=ORIGINAL_ZIP_BYTES or hashlib.sha256(blob).hexdigest()!=ORIGINAL_SHA256:
        raise ValueError("AUTHOR_ZIP_BYTES_OR_SHA_DRIFT")
    with zipfile.ZipFile(io.BytesIO(blob)) as arc:
        info=arc.infolist()
        if len(info)!=27 or arc.testzip() is not None:raise ValueError("AUTHOR_ZIP_CRC_OR_NUMBER_DRIFT")
        texts=[x for x in info if x.filename.lower().endswith(".txt")]
        if len(texts)!=1 or texts[0].file_size!=3093006:
            raise ValueError("AUTHOR_ORIGINAL_TEXT_UNIVERSE_CHANGED")
        return arc.read(texts[0])


def anonymized_domain(seq):
    counts=Counter(seq)
    if len(counts)>12 or not all(re.fullmatch(r"(?:-?[0-9]{1,4}(?:\.[0-9]{1,4})?|NA|nan|)",s,re.IGNORECASE) for s in counts):
        return {"unique_values":len(counts),"direct_category_counts_suppressed":True}
    return {"unique_values":len(counts),"categories":dict(sorted(counts.items()))}


def audit_source_text(source:bytes, require_real_universe:bool=True):
    try: text=source.decode("utf-8-sig")
    except UnicodeError as e:raise ValueError("ORIGINAL_TEXT_ENCODING") from e
    rdr=csv.DictReader(io.StringIO(text),delimiter="\t")
    if tuple(rdr.fieldnames or ())!=EXPECTED_HEADERS:
        raise ValueError("FIRST_PARTY_24_FIELD_DICTIONARY_CHANGED")
    sessions=defaultdict(list)
    people=defaultdict(set)
    treatment_to_sessions=defaultdict(set)
    session_to_treatments=defaultdict(set)
    person_files=defaultdict(set)
    keys=set()
    duplicate_keys=0
    payoff_domain=Counter()
    fields={x:Counter() for x in SMALL_ACTION_FIELDS}
    target_len=0
    group_sizes=Counter()
    group_map=defaultdict(int)
    maxperiod=0
    missing_required=Counter()
    for row in rdr:
        if None in row or None in row.values():
            raise ValueError("TEXT_ROW_HAS_BAD_WIDTH")
        session=row["file"].strip()
        person=row["subject"].strip()
        interaction=row["interaction"].strip()
        group=row["group"].strip()
        period=row["period"].strip()
        bc=row["bc"].strip()
        err=row["error"].strip()
        if not all((session,person,interaction,group,period,bc,err)):
            raise ValueError("TEXT_MANDATORY_KEY_MISSING")
        if not re.fullmatch(r"[0-9]+",period) or int(period)<1:
            raise ValueError("TEXT_ROUND_MALFORMED")
        maxperiod=max(maxperiod,int(period))
        key=(session,person,interaction,period)
        if key in keys:duplicate_keys+=1
        keys.add(key)
        sessions[session].append(row)
        people[session].add(person)
        person_files[person].add(session)
        treatment=(bc,err)
        treatment_to_sessions[treatment].add(session)
        session_to_treatments[session].add(treatment)
        payoff_domain[row["payoff"].strip()]+=1
        for f in SMALL_ACTION_FIELDS:fields[f][row[f].strip()]+=1
        for f in EXPECTED_HEADERS:
            if row[f].strip()=="":missing_required[f]+=1
        group_map[(session,interaction,period,group)]+=1
        target_len+=1
    if require_real_universe and target_len!=ORIGINAL_TEXT_ROWS:
        raise ValueError("ORIGINAL_HUMAN_ROW_UNIVERSE_CHANGED")
    for g,n in group_map.items():group_sizes[n]+=1
    histogram=Counter(len(ses) for ses in person_files.values())
    treatments=[]
    for (bc,err),groups in sorted(treatment_to_sessions.items()):
        treatments.append({
           "bc":bc,"error":err,"sessions":len(groups),
           "human_action_rows":sum(1 for recs in sessions.values() for r in recs
                                   if r["bc"].strip()==bc and r["error"].strip()==err),
        })
    return {
       "research_id":"R075","stage":"COAUTHOR_SOURCE_TEXT_PERSON_SESSION_STRUCTURAL_AUDIT_ONLY",
       "text_rows":target_len,
       "column_count":len(EXPECTED_HEADERS),
       "distinct_original_file_session_ids":len(sessions),
       "treatment_count":len(treatment_to_sessions),
       "treatments":treatments,
       "session_treatment_count_distribution":dict(sorted(Counter(map(len,session_to_treatments.values())).items())),
       "person_session_slots":sum(len(p) for p in people.values()),
       "distinct_source_person_codes":len(person_files),
       "person_code_occurrence_across_sessions_histogram":dict(sorted(histogram.items())),
       "subject_interaction_round_duplicate_records":duplicate_keys,
       "max_round":maxperiod,
       "pair_group_round_count_distribution":dict(sorted(group_sizes.items())),
       "small_action_code_domains":{f:anonymized_domain(list(v.elements())) for f,v in fields.items()},
       "blank_count_by_field":dict((k,v) for k,v in missing_required.items() if v>0),
       "original_source_byte_identity":"ZIP_SHA_AND_TEXT_ROW_COUNT_ONLY" if require_real_universe else "SYNTHETIC_FIXTURE",
       "individual_human_records_exported":False,
       "model_score_run":False,
       "E3":"OPEN_PENDING_AUTHOR_ACTION_FIELD_CODEBOOK",
    }


def main():
    p=argparse.ArgumentParser()
    p.add_argument("--zip",type=Path,required=True)
    p.add_argument("--output",type=Path,required=True)
    args=p.parse_args()
    blob=args.zip.read_bytes()
    raw=original_text_from_verified_zip(blob)
    out=audit_source_text(raw)
    out["source_zip_sha256"]=ORIGINAL_SHA256
    out["original_zip_bytes"]=len(blob)
    out["original_text_sha256"]=hashlib.sha256(raw).hexdigest()
    args.output.write_text(json.dumps(out,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print(json.dumps(out,sort_keys=True))
if __name__=="__main__":main()
