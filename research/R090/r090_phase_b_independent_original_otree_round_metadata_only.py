#!/usr/bin/env python3
"""R090 frozen original source oTree round-field audit; no experimental outcomes."""
from __future__ import annotations
import argparse,collections,json,pathlib,urllib.request,urllib.error
from collections import Counter,defaultdict
from r090_independent_climate_clubs_original_roster_source_gate import (
 URL,MAX_BYTES,check_url,check_source_bytes,int_positive,TREATMENTS,RECORD)

def round_field_audit(rows,expected_n=2700):
 if len(rows)!=expected_n:raise ValueError("R090B_ORIGINAL_ROSTER_SIZE_NOT_CONTRACT")
 rawpair=Counter();a=Counter();b=Counter()
 by_person=defaultdict(list);by_group=defaultdict(list)
 treatment_person=defaultdict(set);tr_rows=Counter()
 for r in rows:
  c=r["treatment"];sid=r["session.code"];gid=r["group.id_in_subsession"];pid=r["participant.code"]
  if c not in TREATMENTS or not sid or not gid or not pid:
   raise ValueError("R090B_SOURCE_UNKNOWN_TREATMENT_OR_KEY")
  pa=int_positive(r["participant._round_number"],"R090B_INVALID_PARTICIPANT_ROUND")
  sb=int_positive(r["subsession.round_number"],"R090B_INVALID_SUBSESSION_ROUND")
  a[pa]+=1;b[sb]+=1;rawpair[(pa,sb)]+=1
  by_person[(sid,pid)].append((c,gid,pa,sb))
  by_group[(sid,gid,sb)].append((pid,c))
  tr_rows[c]+=1;treatment_person[c].add((sid,pid))
 if len(rawpair)>100:raise ValueError("R090B_UNBOUNDED_ROUND_PAIR_DISTRIBUTION")
 if any(len({c for _,c in members})!=1 for members in by_group.values()):
  raise ValueError("R090B_SOURCE_GROUP_CONDITION_CONFLICT")
 changed_person=0;dup_a=dup_b=0
 for person,recs in by_person.items():
  changed_person+=int(len({(c,g) for c,g,_,_ in recs})>1)
  dup_a+=int(len({pa for _,_,pa,sb in recs})<len(recs))
  dup_b+=int(len({sb for _,_,pa,sb in recs})<len(recs))
 pergroup=defaultdict(list)
 groupround_size=Counter()
 same_person_groupround_dups=0
 for (sid,g,sb),rr in by_group.items():
  groupround_size[len(rr)]+=1
  same_person_groupround_dups+=int(len({pid for pid,_ in rr})!=len(rr))
  pergroup[(sid,g)].append((sb,frozenset(pid for pid,_ in rr)))
 stable=Counter()
 for key,rosters in pergroup.items():
  if len(rosters)>1:
   stable["multi_round_stable" if len({a for _,a in rosters})==1 else "multi_round_changed"]+=1
  else:stable["single_round_only"]+=1
 original_rounds=sorted(b)
 return {
  "author_original_2700_rows":len(rows),
  "participant_technical_round_histogram":{str(k):v for k,v in sorted(a.items())},
  "subsession_experimental_round_histogram":{str(k):v for k,v in sorted(b.items())},
  "nonmatching_two_round_fields_rows":sum(v for (x,y),v in rawpair.items() if x!=y),
  "two_round_field_pair_histogram":{f"{i}|{j}":n for (i,j),n in sorted(rawpair.items())},
  "distinct_original_participants_within_sessions":len(by_person),
  "distinct_author_sessions":len({s for s,_ in by_person}),
  "distinct_source_session_group_identifiers":len(pergroup),
  "distinct_subsession_group_rounds":len(by_group),
  "subsession_group_size_distribution":{str(k):v for k,v in sorted(groupround_size.items())},
  "subsession_rounds_observed":original_rounds,
  "person_has_multiple_group_or_treatment_keys_across_rows":changed_person,
  "persons_with_duplicate_participant_technical_rounds":dup_a,
  "persons_with_duplicate_subsession_rounds":dup_b,
  "same_person_duplicated_within_group_round":same_person_groupround_dups,
  "subsession_group_membership_stability_histogram":dict(stable),
  "by_treatment_row_counts":{c:tr_rows[c] for c in TREATMENTS},
  "by_treatment_unique_person_counts":{c:len(treatment_person[c]) for c in TREATMENTS},
  "source_behaviour_contribution_or_endowment_values_computed":False,
  "actor_or_group_identifiers_exported":False,
  "subsession_at_least_2_distinct_round_values":len(original_rounds)>=2}

def execute():
 check_url(URL)
 with urllib.request.urlopen(urllib.request.Request(URL,headers={
    "User-Agent":"Psychohistory-R090-fixed-original-Zenodo-structural-oTree-audit/1.0"}),timeout=45) as resp:
  check_url(resp.geturl());original=resp.read(MAX_BYTES+1)
 rows,identity=check_source_bytes(original)
 return {"research_id":"R090","phase":"B_ORIGINAL_AUTHOR_TWO_ROUND_FIELD_SCHEMA_ONLY",
    "first_true_source_round_field_mismatch_failure_retained":True,
    "official_original_record":RECORD,"original_full_source":identity,
    "round_and_roster_metadata":round_field_audit(rows),
    "original_human_behavior_scored":0,
    "R090_cross_experiment_E2":"NOT_YET_ESTABLISHED",
    "PESEN_v0.1":"FROZEN"}
def main():
 ap=argparse.ArgumentParser();ap.add_argument("--output",type=pathlib.Path,required=True);a=ap.parse_args()
 try:r=execute()
 except (ValueError,OSError,TypeError,urllib.error.HTTPError,urllib.error.URLError) as e:
  safe=str(e)[:100] if isinstance(e,ValueError) and str(e).startswith("R090") else "R090B_SOURCE_IO_OR_STRUCTURE_UNREADABLE"
  r={"research_id":"R090","phase":"B_ORIGINAL_METADATA_FAIL_CLOSED","safe_failure":safe,"human_outcomes":0,"PESEN_v0.1":"FROZEN"}
 a.output.parent.mkdir(parents=True,exist_ok=True)
 a.output.write_text(json.dumps(r,indent=2,sort_keys=True)+"\n")
 print(json.dumps(r,sort_keys=True))
if __name__=="__main__":main()
