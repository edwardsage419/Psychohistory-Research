"""R172 original real historical episode table / Stata source eligibility audit.

Only verify official data coding, event indicator and right censoring shape.
Dataset: Pérez-Liñán & Mainwaring (2025), Harvard Dataverse WFO1N1 v1.1,
CC0-1.0. This is prior to any predictive score or model freeze.
"""
from __future__ import annotations
from collections import Counter,defaultdict
from decimal import Decimal,InvalidOperation
from pathlib import Path
import csv,hashlib,io,json,re

HERE=Path(__file__).resolve().parent
SOURCE=HERE/"source"
TAB=SOURCE/"Original_Replication_dataset.tab"
CODE=SOURCE/"Original_Replication_code_Stata.do"
ORIGINAL=SOURCE/"Original_Replication_dataset_as_uploaded.bin"
EXPECTED_SHA256={
    TAB.name:"ed8e29368d06d0fa6d597df567eb21e7ac27fa849e1cdfd90b76167c8b5778ba",
    CODE.name:"664cf425684b97b8a7bf835ed748955e2e34426e8a14c0db8abbf98a4fb2e3ad",
    ORIGINAL.name:"ddca691b25a664ce13ef2471184e3d5ae3ed62cb72521e0593bff770efb0e4e6"
}
EXPECTED_MD5={
    CODE.name:"2dd571e5f94bd1f79158dcd2b53b0b94",
    ORIGINAL.name:"4343114d56124f88bce9d9cc3ce81523",
}
OUTPUT=HERE/"R172_REAL_HISTORICAL_EPISODE_STRUCTURE_AUDIT.json"


def read_verified_source():
    b={}
    for name,expected in EXPECTED_SHA256.items():
        raw=(SOURCE/name).read_bytes()
        actual=hashlib.sha256(raw).hexdigest()
        if actual!=expected:raise ValueError("historical original derived source SHA mismatch: "+name)
        if name in EXPECTED_MD5 and hashlib.md5(raw).hexdigest()!=EXPECTED_MD5[name]:
            raise ValueError("MD5 original upload mismatch: "+name)
        b[name]=raw
    return b


def numeric(value):
    if value is None or str(value).strip() in ("",".","NA"):
        return None
    try:return Decimal(str(value))
    except InvalidOperation:return None


def audit_structure():
    raw=read_verified_source()
    text=raw[TAB.name].decode("utf-8-sig")
    reader=csv.DictReader(io.StringIO(text),delimiter="\t")
    columns=reader.fieldnames or []
    rows=list(reader)
    must={"country_name","country_text_id","year","id","transition","t","t0","breakdown"}
    if not must.issubset(columns):raise ValueError("Original official event fields absent")
    episode=defaultdict(list)
    missing=Counter()
    for row in rows:
        for key in must:
            if not (row.get(key) or "").strip():missing[key]+=1
        episode[row["id"]].append(row)
    events=Counter((row["breakdown"] or "").strip() for row in rows)
    year_freq=Counter(row["year"] for row in rows)
    country_freq=Counter(row["country_text_id"] for row in rows)
    event_rows=[row for row in rows if numeric(row["breakdown"])==1]
    episode_summaries=[]
    for id,entries in sorted(episode.items()):
        years=[int(r["year"]) for r in entries if numeric(r["year"]) is not None]
        indicators=[numeric(r["breakdown"]) for r in entries]
        observed=[i for i,y in enumerate(indicators) if y==1]
        issues=[]
        if len(years)!=len(entries):issues.append("missing_or_noninteger_year")
        if len(years)!=len(set(years)):issues.append("duplicate_episode_year")
        if years!=sorted(years):issues.append("source_rows_not_sorted_chronologically")
        if len(years)>1 and sorted(years)!=list(range(min(years),max(years)+1)):
            issues.append("year_gaps")
        if len(observed)>1:issues.append("repeated_breakdown_in_same_episode")
        if observed and observed[-1]!=len(entries)-1:
            issues.append("breakdown_before_last_observation")
        if len({r["country_text_id"] for r in entries})>1:
            issues.append("multiple_country_codes_in_episode")
        if len({r["transition"] for r in entries})>1:
            issues.append("multiple_transition_dates_in_episode")
        t_errors=0;t0_errors=0
        for r in entries:
            t=numeric(r["t"]);t0=numeric(r["t0"]);y=numeric(r["year"])
            if t is not None and t0 is not None and y is not None and t!=y-t0:
                t_errors+=1
            if t0 is not None and y is not None and t0>y:t0_errors+=1
        if t_errors:issues.append("elapsed_time_t_not_year_minus_t0_in_"+str(t_errors)+"_rows")
        if t0_errors:issues.append("episode_entry_t0_greater_than_year")
        episode_summaries.append({
            "id":id,
            "country_id":entries[0]["country_text_id"],
            "transition_reported":entries[0]["transition"],
            "first_calendar_year":min(years) if years else None,
            "last_calendar_year":max(years) if years else None,
            "n_observed_years":len(entries),
            "breakdown_events":len(observed),
            "breakdown_last_observed_year":bool(observed and observed[-1]==len(entries)-1),
            "possible_right_censoring":bool(not observed),
            "code_issues":issues
        })
    code_text=raw[CODE.name].decode("utf-8-sig",errors="replace")
    evidence_lines=[
        {"line_number":i,"text":line.strip()[:320]}
        for i,line in enumerate(code_text.splitlines(),1)
        if re.search(r"(?i)\b(stset|stcox|streg|sts\s|stsplit|logit|probit|cloglog|xtlogit|breakdown|surviv|failure\(|time\s*=|entry\s*=|id\()",line)
    ]
    selected={
       "research_id":"R172","phase":"REAL_DATA_RISK_SET_AND_ORIGINAL_CODE_ELIGIBILITY_ONLY",
       "source_dataset":"doi:10.7910/DVN/WFO1N1",
       "source_dataset_version":"1.1",
       "license":"CC0-1.0",
       "source_SHA256":EXPECTED_SHA256,
       "rows":len(rows),
       "columns":columns,
       "country_code_count":len(country_freq),
       "country_name_count":len(set(r["country_name"] for r in rows)),
       "episode_id_count":len(episode),
       "unlabeled_breakdown_rows":[{
            "episode_id":r["id"],"country":r["country_name"],
            "year":r["year"],"t":r["t"],"transition":r["transition"],
            "is_last_year_of_episode":r==episode[r["id"]][-1]}
            for r in rows if numeric(r["breakdown"]) is None],
       "country_name_to_code_map":sorted(
            { (r["country_name"],r["country_text_id"]) for r in rows}),
       "minimum_year":min(int(r["year"]) for r in rows if numeric(r["year"]) is not None),
       "maximum_year":max(int(r["year"]) for r in rows if numeric(r["year"]) is not None),
       "breakdown_literal_categories":dict(sorted(events.items())),
       "event_rows_count_if_breakdown_1":len(event_rows),
       "episodes_with_last_year_event":sum(x["breakdown_events"]==1 and x["breakdown_last_observed_year"] for x in episode_summaries),
       "episodes_without_breakdown":sum(x["breakdown_events"]==0 for x in episode_summaries),
       "episodes_with_anomalies":sum(bool(x["code_issues"]) for x in episode_summaries),
       "episode_anomalies":[x for x in episode_summaries if x["code_issues"]],
       "missing_required_values":dict(sorted(missing.items())),
       "source_episode_structures":episode_summaries,
       "baseline_libdem0_missing":sum(numeric(r.get("libdem0")) is None for r in rows),
       "baseline_libdem0_episode_variation_count":sum(
          len({r.get("libdem0") for r in rs})>1 for rs in episode.values()),
       "baseline_libdem0_min":str(min(numeric(r["libdem0"]) for r in rows if numeric(r.get("libdem0")) is not None)),
       "baseline_libdem0_max":str(max(numeric(r["libdem0"]) for r in rows if numeric(r.get("libdem0")) is not None)),
       "t_missing":sum(numeric(r.get("t")) is None for r in rows),
       "t_min":str(min(numeric(r["t"]) for r in rows if numeric(r.get("t")) is not None)),
       "t_max":str(max(numeric(r["t"]) for r in rows if numeric(r.get("t")) is not None)),
       "source_author_Stata_survival_or_breakdown_commands":evidence_lines[:110],
       "original_uploaded_binary_first_24_bytes_hex":raw[ORIGINAL.name][:24].hex(),
       "original_uploaded_binary_byte_length":len(raw[ORIGINAL.name]),
       "person_or_country_event_prediction_scored":False,
       "historical_hazard_model_fitted":False,
       "train_and_holdout_protocol_frozen":False,
       "E2_new_independent_human_prediction":0,
       "E3_new_external_historical_predictions":0
    }
    OUTPUT.write_text(json.dumps(selected,indent=2,ensure_ascii=False,sort_keys=True)+"\n")
    print("R172_STRUCTURAL_COUNTS",json.dumps({
       k:selected[k] for k in (
         "rows","country_code_count","episode_id_count","minimum_year",
         "maximum_year","breakdown_literal_categories","event_rows_count_if_breakdown_1",
         "episodes_with_last_year_event","episodes_without_breakdown",
         "episodes_with_anomalies","missing_required_values")},ensure_ascii=False))
    print("R172_REAL_EPISODE_ANOMALIES",json.dumps(selected["episode_anomalies"][:15],ensure_ascii=False))
    print("R172_UNLABELED_BREAKDOWN_ROWS",json.dumps(selected["unlabeled_breakdown_rows"],ensure_ascii=False))
    print("R172_COUNTRY_COUNTS",selected["country_code_count"],selected["country_name_count"])
    print("R172_HISTORICAL_BASELINE_COVARIATE",json.dumps({
        k:selected[k] for k in ("baseline_libdem0_missing",
        "baseline_libdem0_episode_variation_count","baseline_libdem0_min",
        "baseline_libdem0_max","t_missing","t_min","t_max")},ensure_ascii=False))
    print("R172_SOURCE_STATA_RELEVANT_LINES",json.dumps(evidence_lines[:28],ensure_ascii=False))
    print("R172_REAL_EPISODE_AUDIT_SHA256",hashlib.sha256(OUTPUT.read_bytes()).hexdigest())
    return selected


if __name__=="__main__":
    audit_structure()
