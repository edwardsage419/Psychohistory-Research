#!/usr/bin/env python3
"""R075 first-party coauthor action-feedback semantics and session eligibility.

Author archive SHA enforced. Human rows and session/player labels are transient.
Only anonymous numerical domain and mismatch counts leave the runner.
"""
from __future__ import annotations
from collections import Counter,defaultdict
import argparse,csv,io,json,re
from pathlib import Path
from r075_coauthor_original_session_structure import (
    ORIGINAL_TEXT_ROWS,original_text_from_verified_zip,audit_source_text
)

LAGS=("you_p_1","other_p_1","you_p_2","other_p_2")
def analyze(source:bytes):
    base=audit_source_text(source,True)
    rdr=csv.DictReader(io.StringIO(source.decode("utf-8-sig")),delimiter="\t")
    rows=list(rdr)
    if len(rows)!=ORIGINAL_TEXT_ROWS:raise ValueError("SOURCE_ROWS_DRIFT")
    # Exact composite identity ensures reused subject numbers across true sessions
    # never connect sessions in the predictor or this audit.
    unique={}
    pairs=defaultdict(list)
    byseries=defaultdict(dict)
    for x in rows:
        k=(x["file"],x["subject"],x["interaction"],int(x["period"]))
        if k in unique:raise ValueError("SOURCE_DUPLICATE_PERSON_INTERACTION_ROUND")
        unique[k]=x
        group=(x["file"],x["interaction"],x["group"],int(x["period"]))
        pairs[group].append(x)
        byseries[k[:3]][k[3]]=x
    partner={}
    for key,items in pairs.items():
        if len(items)!=2 or items[0]["subject"]==items[1]["subject"]:
            raise ValueError("AUTHOR_PAIR_IS_NOT_TWO_DISTINCT_PEOPLE")
        a,b=items
        partner[(a["file"],a["subject"],a["interaction"],int(a["period"]))]=b
        partner[(b["file"],b["subject"],b["interaction"],int(b["period"]))]=a
    lag_domains={name:Counter(x[name] for x in rows) for name in LAGS}
    def numeric_categories(c):
        if len(c)>12 or any(not re.fullmatch(r"-?[0-9]{1,5}(?:\.[0-9]{1,4})?|NA|NaN|nan|",k) for k in c):
            return {"unique_code_count":len(c),"codes_suppressed":True}
        return dict(sorted(c.items()))
    mismatches=defaultdict(Counter)
    elig=Counter()
    failures=Counter()
    partner_changes=0
    for series,h in byseries.items():
        periods=sorted(h)
        if periods!=list(range(1,len(periods)+1)):
            failures["person_series_noncontiguous"]+=1
        for t in periods:
            r=h[t]
            if t>=2 and t-1 in h:
                old=h[t-1]
                other=partner.get((*series,t-1))
                current_other=partner.get((*series,t))
                if not other or not current_other:
                    failures["partner_unknown"]+=1;continue
                if current_other["subject"]!=other["subject"]:partner_changes+=1
                error=r["error"]
                mismatches[error]["valid_prior_rows"]+=1
                for code, previous_value in (
                    ("you_p_1",old["decision"]),("other_p_1",other["decision"])
                ):
                    actual=r[code]
                    if actual not in ("0","1"):mismatches[error][code+"_nonbinary"]+=1
                    else:
                        mismatches[error][code+"_binary"]+=1
                        if actual!=previous_value:mismatches[error][code+"_mismatch_to_prior_intended"]+=1
            if t>=3 and t-1 in h and t-2 in h:
                last=partner.get((*series,t-1))
                last2=partner.get((*series,t-2))
                if not last or not last2:continue
                error=r["error"]
                elig[error]+=1
                mismatches[error]["scorable_t3"]+=1
                for code,prev in (("you_p_2",h[t-2]["decision"]),
                                  ("other_p_2",last2["decision"])):
                    actual=r[code]
                    if actual not in ("0","1"):mismatches[error][code+"_nonbinary"]+=1
                    else:
                        mismatches[error][code+"_binary"]+=1
                        if actual!=prev:mismatches[error][code+"_mismatch_to_prior_intended"]+=1
    return {
        "research_id":"R075",
        "status":"FIRST_PARTY_SOURCE_SESSION_AND_FEEDBACK_STRUCTURE_AUDITED_NO_SCORING",
        "original_source_text_actions":len(rows),
        "sessions":base["distinct_original_file_session_ids"],
        "session_person_slots":base["person_session_slots"],
        "paired_rounds":len(pairs),
        "distinct_person_interactions":len(byseries),
        "fully_observed_t3_candidate_targets":sum(elig.values()),
        "t3_by_error":dict(sorted(elig.items())),
        "prior_observed_action_domains":{k:numeric_categories(v) for k,v in lag_domains.items()},
        "prior_vs_intended_choice_disagreement_by_error":{
            str(k):dict(sorted(v.items())) for k,v in sorted(mismatches.items())
        },
        "partner_switch_inside_same_interaction_rows":partner_changes,
        "integrity_failures":dict(failures),
        "session_identity":"original file; person scoped by file+subject",
        "choice_mapping_to_cooperation":"ORIGINAL_CODEBOOK_VALIDATION_OPEN",
        "feedback_mapping_to_observed_executed_action":"ORIGINAL_CODEBOOK_VALIDATION_OPEN",
        "raw_human_rows_or_session_ids_published":False,
        "models_scored":False,
        "PESEN_v0.1":"FROZEN",
    }


def main():
    p=argparse.ArgumentParser()
    p.add_argument("--zip",type=Path,required=True)
    p.add_argument("--output",type=Path,required=True)
    a=p.parse_args()
    source=original_text_from_verified_zip(a.zip.read_bytes())
    result=analyze(source)
    a.output.write_text(json.dumps(result,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print(json.dumps(result,sort_keys=True))
if __name__=="__main__":
    main()
