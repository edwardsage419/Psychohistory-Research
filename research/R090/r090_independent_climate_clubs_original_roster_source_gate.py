#!/usr/bin/env python3
"""R090 new independent authors' original 2,700 decision CSV SOURCE ONLY.

No contribution, payoff, endowment or individual data read for science scores.
Only original SHA/MD5 and anonymized group membership completeness counts.
"""
from __future__ import annotations
import argparse,collections,csv,hashlib,io,json,pathlib,urllib.request,urllib.error
from collections import Counter,defaultdict

RECORD=17610157
DOI="10.5281/zenodo.17610157"
FILE="Climate_Clubs_data.csv"
OFFICIAL_MD5="56931608b717aea06105ad10a58ff937"
MAX_BYTES=900_000
URL="https://zenodo.org/records/17610157/files/Climate_Clubs_data.csv?download=1"
REQUIRED=("participant.id_in_session","participant.code",
  "participant._round_number","player.id_in_group","player.automatic_decision",
  "player.contribution","player.endowment","player.timeout_contr",
  "group.id_in_subsession","subsession.round_number","session.code",
  "group","treatment")
TREATMENTS=("T1","T2","T3","T4")

def check_url(url):
 p=urllib.parse.urlsplit(url)
 if (p.scheme!="https" or p.netloc!="zenodo.org"
     or p.path!=f"/records/{RECORD}/files/{FILE}" or p.fragment):
  raise ValueError("R090_UNOFFICIAL_ZENODO_SOURCE_OR_REDIRECT")
 return True

def check_source_bytes(raw,expected_md5=OFFICIAL_MD5):
 if not isinstance(raw,bytes) or not 0<len(raw)<=MAX_BYTES:
  raise ValueError("R090_ORIGINAL_AUTHOR_CSV_EMPTY_OR_OVERSIZE")
 if hashlib.md5(raw).hexdigest()!=expected_md5:
  raise ValueError("R090_OFFICIAL_AUTHOR_MD5_MISMATCH")
 try:
  s=raw.decode("utf-8-sig")
 except UnicodeDecodeError as e:
  raise ValueError("R090_ORIGINAL_AUTHOR_ENCODING_NOT_UTF8") from e
 rd=csv.DictReader(io.StringIO(s,newline=""))
 if rd.fieldnames is None or len(rd.fieldnames)!=27 or len(set(rd.fieldnames))!=27 or not set(REQUIRED).issubset(rd.fieldnames):
  raise ValueError("R090_ORIGINAL_AUTHOR_COLUMNS_27_EXPECTED_NOT_MET")
 rows=list(rd)
 if len(rows)!=2700:raise ValueError("R090_AUTHOR_PUBLISHED_ROWS_2700_NOT_MET")
 return rows,{"original_source_bytes":len(raw),
   "original_publisher_MD5_verified":True,
   "full_source_SHA256":hashlib.sha256(raw).hexdigest(),
   "source_columns":len(rd.fieldnames),"original_source_rows":len(rows)}

def int_positive(value,label):
 if value is None or not value.isascii() or not value.isdigit() or int(value)<1:
  raise ValueError(label)
 return int(value)

def bool_indicator(s):
 if s in ("0","1"):return int(s)
 if s in ("","NA","na",None):return None
 raise ValueError("R090_AUTHOR_AUTOMATIC_OR_TIMEOUT_UNEXPECTED_SCHEMA")

def original_source_roster(rows,strict_universe=True):
 groups=defaultdict(list)
 persons=defaultdict(list)
 sessions=set()
 treatments=defaultdict(set)
 tr_rows=Counter()
 tr_subjects=defaultdict(set)
 seen=set()
 auto=Counter();timed=Counter()
 for r in rows:
  if not all(k in r for k in REQUIRED):raise ValueError("R090_SOURCE_MISSING_EXPECTED_FIELD")
  tr=r["treatment"];person=r["participant.code"];sid=r["session.code"]
  g=r["group.id_in_subsession"]
  if tr not in TREATMENTS:raise ValueError("R090_UNKNOWN_TREATMENT")
  if not all(isinstance(x,str) and x.strip() for x in (person,sid,g)):
   raise ValueError("R090_EMPTY_PERSON_SESSION_OR_GROUP_CODE")
  p=int_positive(r["participant._round_number"],"R090_INVALID_PARTICIPANT_ROUND")
  sr=int_positive(r["subsession.round_number"],"R090_INVALID_SUBSESSION_ROUND")
  if p!=sr:raise ValueError("R090_PARTICIPANT_AND_SUBSESSION_ROUND_DISAGREE")
  key=(sid,person,p)
  if key in seen:raise ValueError("R090_DUPLICATE_PERSON_SESSION_ROUND")
  seen.add(key)
  if (sid,person) in persons and any(q[0]!=tr for q in persons[(sid,person)]):
   raise ValueError("R090_PERSON_CHANGES_TREATMENT_IN_SESSION")
  a=bool_indicator(r["player.automatic_decision"])
  z=bool_indicator(r["player.timeout_contr"])
  auto[(tr,"one" if a==1 else "zero" if a==0 else "missing")]+=1
  timed[(tr,"one" if z==1 else "zero" if z==0 else "missing")]+=1
  groups[(sid,g,p)].append((person,tr))
  persons[(sid,person)].append((tr,g,p))
  tr_rows[tr]+=1;tr_subjects[tr].add((sid,person))
  sessions.add(sid);treatments[(sid,g)].add(tr)
 if strict_universe and len(rows)!=2700:
  raise ValueError("R090_PUBLISHED_2700_ROWS_REQUIRED")
 sizes=Counter();tgroup=defaultdict(set)
 base_rosters=defaultdict(list)
 for (sid,g,p),members in groups.items():
  n=len(members);sizes[n]+=1
  if len(set(person for person,_ in members))!=n:
   raise ValueError("R090_DUPLICATE_PERSON_IN_GROUP_ROUND")
  condition={v[1] for v in members}
  if len(condition)!=1:raise ValueError("R090_MIXED_TREATMENT_IN_GROUP_ROUND")
  tr=next(iter(condition))
  base_rosters[(sid,g)].append((p,frozenset(x[0] for x in members),tr))
  tgroup[tr].add((sid,g))
 group_round_counts=Counter(len(v) for v in base_rosters.values())
 roster_stability=Counter()
 duplicated_round_id=0
 for g,v in base_rosters.items():
  rounds=[x[0] for x in v]
  if len(rounds)!=len(set(rounds)):duplicated_round_id+=1
  first=v[0][1];stable=all(x[1]==first for x in v)
  roster_stability["stable_membership" if stable else "changed_membership"]+=1
  roster_stability["at_least_two_rounds" if len(v)>=2 else "only_one_round"]+=1
 if duplicated_round_id:raise ValueError("R090_DUPLICATE_GROUP_ROUND")
 # group identifier "group" is a secondary display label and cannot be assumed stable.
 treatment_distribution={k:{"participant_round_rows":tr_rows[k],
  "unique_persons_within_session":len(tr_subjects[k]),
  "unique_session_group_identifiers":len(tgroup[k]),
  "automatic_decision_one":auto[(k,"one")],
  "automatic_decision_missing":auto[(k,"missing")],
  "contribution_timeout_one":timed[(k,"one")],
  "contribution_timeout_missing":timed[(k,"missing")]}
  for k in TREATMENTS}
 return {
  "original_participant_round_rows":len(rows),
  "original_unique_persons_within_session":len(persons),
  "original_distinct_sessions":len(sessions),
  "original_distinct_session_group_keys":len(base_rosters),
  "original_distinct_group_round_keys":len(groups),
  "rounds_observed_sorted":sorted(set(k[2] for k in groups)),
  "group_round_size_distribution":{str(k):v for k,v in sorted(sizes.items())},
  "group_number_of_observed_rounds_distribution":{str(k):v for k,v in sorted(group_round_counts.items())},
  "original_group_roster_stability_summary":dict(roster_stability),
  "by_original_treatment":treatment_distribution,
  "all_source_rows_have_unique_person_session_round":True,
  "no_actor_or_group_id_values_exported":True,
  "source_human_contribution_ever_examined":False}

def evaluate():
 check_url(URL)
 req=urllib.request.Request(URL,headers={"User-Agent":"Psychohistory-R090-climate-clubs-fixed-source-roster-audit/1.0"})
 with urllib.request.urlopen(req,timeout=45) as res:
  check_url(res.geturl())
  original=res.read(MAX_BYTES+1)
 rows,src=check_source_bytes(original)
 return {"research_id":"R090","phase":"A_AUTHOR_ORIGINAL_TWO_THOUSAND_SEVEN_HUNDRED_ROSTER_ONLY",
  "original_author_DOI":DOI,"fixed_Zenodo_record":RECORD,
  "identity":src,"group_source_eligibility":original_source_roster(rows),
  "R089_source_and_model_frozen_unchanged":True,
  "original_human_contribution_prediction_scores_computed":0,
  "any_source_person_or_group_keys_exported":False,
  "real_cross_experiment_transfer":"AWAITING_FROZEN_PHASE_B_SCORING_ELIGIBILITY",
  "PESEN_v0.1":"FROZEN"}

def main():
 p=argparse.ArgumentParser();p.add_argument("--output",type=pathlib.Path,required=True)
 a=p.parse_args()
 try:r=evaluate()
 except (ValueError,OSError,TypeError,urllib.error.HTTPError,urllib.error.URLError) as e:
  reason=str(e)[:100] if isinstance(e,ValueError) and str(e).startswith("R090_") else "R090_NETWORK_OR_SOURCE_DATA_FAILURE"
  r={"research_id":"R090","phase":"A_ORIGINAL_SOURCE_ROSTER_STRICT_FAIL_CLOSED",
     "safe_failure":reason,"real_human_scoring":0,"PESEN_v0.1":"FROZEN"}
 a.output.parent.mkdir(parents=True,exist_ok=True)
 a.output.write_text(json.dumps(r,indent=2,sort_keys=True)+"\n")
 print(json.dumps(r,sort_keys=True))
if __name__=="__main__":main()
