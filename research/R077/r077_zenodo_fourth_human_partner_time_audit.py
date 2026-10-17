#!/usr/bin/env python3
"""R077 prospective source gate: original independent Zenodo PD partner-time graph.

No human model scoring. Publish only aggregate identity/symmetry / time shapes.
"""
from __future__ import annotations
import argparse,hashlib,json,pathlib,math
from collections import Counter,defaultdict
from urllib.request import Request,urlopen

SRC="https://zenodo.org/records/15462528/files/cleandata.dta?download=1"
SHA256="1cc9a4f68a51992808d966b118226bb5a66ee3ee6054843a132157df8eeb1985"
BYTES=1514315
COLUMNS=("Session","sessionid","Subject","ID","Period","realperiod","realrounds",
"practiceperiod","game","Group","ClientNumber","LastClientNumber","left","otherleft","treatment","part")

def summarize(data):
    import pandas as pd
    if len(data)!=3620:
        raise ValueError("ORIGINAL_FOURTH_SOURCE_ROW_DRIFT")
    if any(col not in data for col in COLUMNS):
        raise ValueError("ORIGINAL_FOURTH_SOURCE_REQUIRED_FIELDS_MISSING")
    d=data[COLUMNS].copy()
    def unique(cols):
        return int(len(d[list(cols)].drop_duplicates()))
    def distribution(values):
        return {str(k):int(v) for k,v in sorted(Counter(values).items(),key=lambda x:str(x[0]))}
    # Canonical text is private. Session identifiers are never emitted.
    group_1=list(d.groupby(["Session"],dropna=False,observed=True))
    group_2=list(d.groupby(["Session","treatment"],dropna=False,observed=True))
    group_3=list(d.groupby(["sessionid"],dropna=False,observed=True))
    def group_sizes(grouping):
        return distribution(len(part) for _,part in grouping)
    out={
      "phase":"R077_ZENODO_ORIGINAL_FOURTH_HUMAN_PAIR_TIME_AUDIT_PRE_SCORE",
      "rows":len(d),
      "observed_session_keys":unique(["Session"]),
      "session_and_treatment_combinations":unique(["Session","treatment"]),
      "sessionid_keys":unique(["sessionid"]),
      "session_key_to_treatment_multiplicity":distribution(part["treatment"].nunique(dropna=False) for _,part in group_1),
      "sessionid_to_source_session_multiplicity":distribution(part["Session"].nunique(dropna=False) for _,part in group_3),
      "sessionid_to_treatment_multiplicity":distribution(part["treatment"].nunique(dropna=False) for _,part in group_3),
      "sessionid_source_rows_group_sizes":group_sizes(group_3),
      "session+treatment_rows_group_sizes":group_sizes(group_2),
      "source_human_session_participant_keys":unique(["Session","treatment","Subject"]),
      "id_keys":unique(["ID"]),
      "id_to_source_session_cardinality":distribution(part[["Session","treatment"]].drop_duplicates().shape[0]
          for _,part in d.groupby("ID",dropna=False,observed=True)),
      "session+treatment+subject+Period_unique":unique(["Session","treatment","Subject","Period"]),
      "session+treatment+subject+game+practiceperiod_unique":unique(["Session","treatment","Subject","game","practiceperiod"]),
      "period_min_max":[int(d["Period"].min()),int(d["Period"].max())],
      "practiceperiod_min_max":[int(d["practiceperiod"].min()),int(d["practiceperiod"].max())],
      "game_unique":int(d["game"].nunique()),
      "treatment_raw_counts":distribution(d["treatment"].fillna(-999999).astype(int)),
      "left_binary_domain":distribution(d["left"].fillna(-999999).astype(int)),
      "otherleft_binary_domain":distribution(d["otherleft"].fillna(-999999).astype(int)),
      "left_missing":int(d["left"].isna().sum()),
      "otherleft_missing":int(d["otherleft"].isna().sum()),
      "Period_duplicate_within_subject":len(d)-unique(["Session","treatment","Subject","Period"]),
      "game+practiceperiod_duplicate_within_subject":len(d)-unique(["Session","treatment","Subject","game","practiceperiod"]),
      "model_outcome_scores":"NOT_RUN",
      "raw_participant_rows_exported":False,"PESEN_v0.1":"FROZEN"
    }
    # Count complete two-person groups for both plausible key combinations;
    # if Group is a membership label not pair ID, this gate must find out.
    for key_fields in (
        ["Session","treatment","Period","Group"],
        ["sessionid","Period","Group"],
        ["Session","treatment","game","practiceperiod","Group"],
        ["sessionid","game","practiceperiod","Group"]
    ):
        pairs=list(d.groupby(key_fields,dropna=False,observed=True))
        sizes=distribution(len(part) for _,part in pairs)
        consistent=0
        matching=0
        for key,part in pairs:
            if len(part)!=2:continue
            consistent+=1
            a,b=part.iloc[0],part.iloc[1]
            if a["otherleft"]==b["left"] and b["otherleft"]==a["left"]:
                matching+=1
        out["pair_key_"+",".join(key_fields)]={
            "total_groupings":len(pairs),"size_histogram":sizes,
            "two_person_groups":consistent,
            "two_person_exact_opponent_action_reciprocity":matching}
    for key_fields in (
        ["Session","treatment","Subject","game"],
        ["sessionid","Subject","game"],
        ["Session","treatment","Subject"],
        ["sessionid","Subject"],
    ):
        groups=list(d.groupby(key_fields,dropna=False,observed=True))
        repeats=Counter()
        contiguity=Counter()
        for _,part in groups:
            ts=sorted(int(x) for x in part["practiceperiod"])
            if len(ts)<3:continue
            # Count consecutive t>=3 inside each key, not a model outcome.
            repeats["candidate_t_ge_3_within_group"]+=sum(
                ts[i]-ts[i-1]==1 and ts[i-1]-ts[i-2]==1 for i in range(2,len(ts)))
            if len(set(ts))==len(ts):
                contiguity["no_duplicate_practiceperiod_groups"]+=1
            else:
                contiguity["duplicate_practiceperiod_groups"]+=1
        out["within_key_"+",".join(key_fields)]={
            "groups":len(groups),
            "practiceperiod_contiguity":dict(contiguity),
            "potential_t>=3_rows":repeats["candidate_t_ge_3_within_group"]
        }
    return out

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--private-dir",type=pathlib.Path,required=True)
    p.add_argument("--output",type=pathlib.Path,required=True)
    args=p.parse_args()
    request=Request(SRC,headers={"User-Agent":"Psychohistory-R077-Drouvelis-2025-true-pair-observation-source-audit/1.0"})
    with urlopen(request,timeout=65) as h:
        raw=h.read(BYTES+1)
    if len(raw)!=BYTES or hashlib.sha256(raw).hexdigest()!=SHA256:
        raise ValueError("R077_AUTHOR_SOURCE_CONTENT_SHA256_CHANGED")
    import pandas as pd
    args.private_dir.mkdir(parents=True,exist_ok=True)
    fn=args.private_dir/"original_fourth.dta"
    fn.write_bytes(raw)
    df=pd.read_stata(fn,convert_categoricals=False)
    out=summarize(df)
    out["source_zip_alternative"]="ZENODO_AUTHOR_ORIGINAL_CLEANDATA_STATA_MD5_CONFIRMED"
    out["original_sha256"]=SHA256
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(out,sort_keys=True,indent=2)+"\n")
    print(json.dumps(out,sort_keys=True))

if __name__=="__main__":main()
